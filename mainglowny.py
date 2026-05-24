from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

domy: list = []
pracownicy: list = []
pensjonariusze: list = []

class DomOpieki:
    def __init__(self, nazwa: str, lokalizacja: str):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.coordinates = DomOpieki.get_coordinates(self)

        # powiazania to WAZNE
        self.pracownicy = []
        self.pensjonariusze = []
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.nazwa)

    def get_coordinates(self) -> list:
        url = f"https://pl.wikipedia.org/wiki/{self.lokalizacja}"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]

class Pracownik:
    def __init__(self, imie: str, nazwisko: str, wiek: int, rola: str, dom: DomOpieki):
        self.imie = imie
        self.nazwisko = nazwisko
        self.wiek = wiek
        self.rola = rola
        self.dom = dom
        #lokalizacja brana z powiazanego domu opieki
        self.lokalizacja = dom.lokalizacja
        self.coordinates = dom.coordinates

        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"{self.imie} {self.nazwisko}")

class Pensjonariusz:
    def __init__(self, imie: str, nazwisko: str, wiek: int, choroby: str, dom: DomOpieki):
        self.imie = imie
        self.nazwisko = nazwisko
        self.wiek = wiek
        self.choroby = choroby
        self.dom = dom
        # lokalizacja brana z powiazanego domu opieki
        self.lokalizacja = dom.lokalizacja
        self.coordinates = dom.coordinates

        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1],
                                            text=f"{self.imie} {self.nazwisko}")
def save_domy_to_file():
    with open("domy.txt", "w", encoding="utf-8") as f:
        for dom in domy:
            f.write(f"{dom.nazwa};{dom.lokalizacja}\n")

def load_domy_from_file():
    try:
        with open("domy.txt", "r", encoding="utf-8") as f:
            for linia in f:
                nazwa, lokalizacja = linia.strip().split(";")
                nowy_dom = DomOpieki(nazwa, lokalizacja)
                domy.append(nowy_dom)
    except FileNotFoundError:
        pass

def show_domy() -> None:
    listbox_lista_domow.delete(0, END)
    for idx, dom in enumerate(domy):
        listbox_lista_domow.insert(idx, dom.nazwa)

def remove_dom() -> None:
    i = listbox_lista_domow.index(ACTIVE)
    dom = domy[i]
    dom.marker.delete()

    # Trzeba usuwac tez pracownikow domu
    for pracownik in dom.pracownicy[:]:
        pracownik.marker.delete()
        pracownicy.remove(pracownik)

    for pensjonariusz in dom.pensjonariusze[:]:
        pensjonariusz.marker.delete()
        pensjonariusze.remove(pensjonariusz)

    domy.pop(i)
    show_domy()

def show_dom_details():
    i = listbox_lista_domow.index(ACTIVE)
    dom = domy[i]

    label_nazwa_szczegoly_domu_wartosc.config(text=dom.nazwa)
    label_lokalizacja_szczegoly_domu_wartosc.config(text=dom.lokalizacja)

    map_widget.set_position(dom.coordinates[0], dom.coordinates[1])
    map_widget.set_zoom(12)

    listbox_pracownicy_domu.delete(0, END)
    for p in dom.pracownicy:
        listbox_pracownicy_domu.insert(END, f"{p.imie} {p.nazwisko}")

    listbox_pensjonariusze_domu.delete(0, END)
    for p in dom.pensjonariusze:
        listbox_pensjonariusze_domu.insert(END, f"{p.imie} {p.nazwisko}")




def edit_dom():
    i = listbox_lista_domow.index(ACTIVE)
    nazwa = domy[i].nazwa
    lokalizacja = domy[i].lokalizacja

    entry_nazwa.insert(0, nazwa)
    entry_lokalizacja.insert(0, lokalizacja)

    button_dodaj_dom.config(text="Zapisz zmiany", command=lambda: update_dom(i))

def update_dom(i):
    domy[i].nazwa = entry_nazwa.get()
    domy[i].lokalizacja = entry_lokalizacja.get()
    domy[i].coordinates = DomOpieki.get_coordinates(domy[i])
    domy[i].marker.delete()
    domy[i].marker = map_widget.set_marker(domy[i].coordinates[0], domy[i].coordinates[1], text=domy[i].nazwa)

    button_dodaj_dom.config(text="Dodaj Dom Opieki", command=add_dom)
    entry_nazwa.delete(0, END)
    entry_lokalizacja.delete(0, END)

    entry_nazwa.focus()
    show_domy()

def add_dom():
    name = entry_nazwa.get()
    lokalizacja = entry_lokalizacja.get()

    # print(name, lokalizacja)
    new_dom = DomOpieki(nazwa=name, lokalizacja=lokalizacja)
    domy.append(new_dom)
    # print(domy)

    entry_nazwa.delete(0, END)
    entry_lokalizacja.delete(0, END)

    entry_nazwa.focus()
    show_domy()
def save_pracownicy_to_file():
    with open("pracownicy.txt", "w", encoding="utf-8") as f:
        for pracownik in pracownicy:
            f.write(f"{pracownik.imie};{pracownik.nazwisko};{pracownik.wiek};{pracownik.rola};{pracownik.dom.nazwa}\n")

def load_pracownicy_from_file():
    try:
        with open("pracownicy.txt", "r", encoding="utf-8") as f:
            for linia in f:
                imie, nazwisko, wiek, rola, nazwa_domu = linia.strip().split(";")

                # znajdź obiekt domu
                dom = next((d for d in domy if d.nazwa == nazwa_domu), None)
                if dom is None:
                    continue

                nowy = Pracownik(imie, nazwisko, wiek, rola, dom)
                pracownicy.append(nowy)
                dom.pracownicy.append(nowy)
    except FileNotFoundError:
        pass

def show_pracownicy() -> None:
    listbox_lista_pracownikow.delete(0, END)
    for idx, pracownik in enumerate(pracownicy):
        listbox_lista_pracownikow.insert(idx, pracownik.imie)


def remove_pracownik() -> None:
    i = listbox_lista_pracownikow.index(ACTIVE)
    pracownik = pracownicy[i]
    pracownik.marker.delete()
    # USUWANIE PRacownika z listy pracownikow domu
    if pracownik in pracownik.dom.pracownicy:
        pracownik.dom.pracownicy.remove(pracownik)
    pracownicy.pop(i)
    show_pracownicy()


def show_pracownik_details():
    i = listbox_lista_pracownikow.index(ACTIVE)
    pracownik = pracownicy[i]

    # pobranie danych
    imie = pracownik.imie
    nazwisko = pracownik.nazwisko
    wiek = pracownik.wiek
    rola = pracownik.rola
    nazwa_domu = pracownik.dom.nazwa
    lokalizacja = pracownik.dom.lokalizacja

    # ustawienie labeli
    label_imie_szczegoly_pracownika_wartosc.config(text=imie)
    label_nazwisko_szczegoly_pracownika_wartosc.config(text=nazwisko)
    label_wiek_szczegoly_pracownika_wartosc.config(text=wiek)
    label_rola_szczegoly_pracownika_wartosc.config(text=rola)
    label_dom_szczegoly_pracownika_wartosc.config(text=nazwa_domu)
    label_lokalizacja_szczegoly_pracownika_wartosc.config(text=lokalizacja)

    # ustawienie mapy
    map_widget.set_position(pracownik.coordinates[0], pracownik.coordinates[1])
    map_widget.set_zoom(12)



def edit_pracownik():
    i = listbox_lista_pracownikow.index(ACTIVE)
    imie = pracownicy[i].imie
    nazwisko = pracownicy[i].nazwisko
    wiek = pracownicy[i].wiek
    rola = pracownicy[i].rola
    nazwa_domu = pracownicy[i].dom.nazwa

    entry_imie_prac.insert(0, imie)
    entry_nazwisko_prac.insert(0, nazwisko)
    entry_wiek_prac.insert(0, wiek)
    entry_rola.insert(0, rola)
    entry_dom_prac.insert(0, nazwa_domu)

    button_dodaj_pracownika.config(text="Zapisz zmiany", command=lambda: update_pracownik(i))

def update_pracownik(i):
    pracownik = pracownicy[i]
    pracownicy[i].imie = entry_imie_prac.get()
    pracownicy[i].nazwisko = entry_nazwisko_prac.get()
    pracownicy[i].wiek = entry_wiek_prac.get()
    pracownicy[i].rola = entry_rola.get()
    nazwa_domu = entry_dom_prac.get()

    # Aktualizacja domu
    for dom in domy:
        if dom.nazwa == nazwa_domu:
            if pracownik in pracownik.dom.pracownicy:
                pracownik.dom.pracownicy.remove(pracownik)

            pracownik.dom = dom
            dom.pracownicy.append(pracownik)

            pracownik.coordinates = dom.coordinates

            break

    pracownik.marker.delete()
    pracownik.marker = map_widget.set_marker(pracownik.coordinates[0],pracownik.coordinates[1],text=pracownik.imie)

    button_dodaj_pracownika.config(text="Dodaj pracownika", command=add_pracownik)
    entry_imie_prac.delete(0, END)
    entry_nazwisko_prac.delete(0, END)
    entry_wiek_prac.delete(0, END)
    entry_rola.delete(0, END)
    entry_dom_prac.delete(0, END)

    entry_imie_prac.focus()
    show_pracownicy()


def add_pracownik():
    name = entry_imie_prac.get()
    surname = entry_nazwisko_prac.get()
    wiek = entry_wiek_prac.get()
    rola = entry_rola.get()
    nazwa_domu = entry_dom_prac.get()

    wybrany_dom = None
    for dom in domy:
        if dom.nazwa == nazwa_domu:
            wybrany_dom = dom
            break

    if wybrany_dom is None:
        print("Błąd: nie znaleziono domu o podanej nazwie.")
        return

    # print(name, surname, wiek, rola, dom)
    new_pracownik = Pracownik(imie=name, nazwisko=surname, wiek=wiek, rola=rola, dom=wybrany_dom)
    pracownicy.append(new_pracownik)
    # print(pracownicy)

    entry_imie_prac.delete(0, END)
    entry_nazwisko_prac.delete(0, END)
    entry_wiek_prac.delete(0, END)
    entry_rola.delete(0, END)
    entry_dom_prac.delete(0, END)

    entry_imie_prac.focus()
    show_pracownicy()

def save_pensjonariusze_to_file():
    with open("pensjonariusze.txt", "w", encoding="utf-8") as f:
        for pensjonariusz in pensjonariusze:
            f.write(
                f"{pensjonariusz.imie};{pensjonariusz.nazwisko};{pensjonariusz.wiek};{pensjonariusz.choroby};{pensjonariusz.dom.nazwa}\n")


def load_pensjonariusze_from_file():
    try:
        with open("pensjonariusze.txt", "r", encoding="utf-8") as f:
            for linia in f:
                imie, nazwisko, wiek, choroby, nazwa_domu = linia.strip().split(";")

                # znajdź obiekt domu
                dom = next((d for d in domy if d.nazwa == nazwa_domu), None)
                if dom is None:
                    continue

                nowy = Pensjonariusz(imie, nazwisko, wiek, choroby, dom)
                pensjonariusze.append(nowy)
                dom.pensjonariusze.append(nowy)
    except FileNotFoundError:
        pass


def show_pensjonariusze() -> None:
    listbox_lista_pensjonariuszy.delete(0, END)
    for idx, pensjonariusz in enumerate(pensjonariusze):
        listbox_lista_pensjonariuszy.insert(idx, pensjonariusz.imie)


def remove_pensjonariusz() -> None:
    i = listbox_lista_pensjonariuszy.index(ACTIVE)
    pensjonariusz = pensjonariusze[i]
    pensjonariusz.marker.delete()
    # USUWANIE pensjonariusza z listy pensjonariuszy domu
    if pensjonariusz in pensjonariusz.dom.pensjonariusze:
        pensjonariusz.dom.pensjonariusze.remove(pensjonariusz)
    pensjonariusze.pop(i)
    show_pensjonariusze()


def show_pensjonariusz_details():
    i = listbox_lista_pensjonariuszy.index(ACTIVE)
    pensjonariusz = pensjonariusze[i]

    # pobranie danych
    imie = pensjonariusz.imie
    nazwisko = pensjonariusz.nazwisko
    wiek = pensjonariusz.wiek
    choroby = pensjonariusz.choroby
    nazwa_domu = pensjonariusz.dom.nazwa
    lokalizacja = pensjonariusz.dom.lokalizacja

    # ustawienie labeli
    label_imie_szczegoly_pensjonariusza_wartosc.config(text=imie)
    label_nazwisko_szczegoly_pensjonariusza_wartosc.config(text=nazwisko)
    label_wiek_szczegoly_pensjonariusza_wartosc.config(text=wiek)
    label_choroby_szczegoly_pensjonariusza_wartosc.config(text=choroby)
    label_dom_szczegoly_pensjonariusza_wartosc.config(text=nazwa_domu)
    label_lokalizacja_szczegoly_pensjonariusza_wartosc.config(text=lokalizacja)

    # ustawienie mapy
    map_widget.set_position(pensjonariusz.coordinates[0], pensjonariusz.coordinates[1])
    map_widget.set_zoom(12)


def edit_pensjonariusz():
    i = listbox_lista_pensjonariuszy.index(ACTIVE)
    imie = pensjonariusze[i].imie
    nazwisko = pensjonariusze[i].nazwisko
    wiek = pensjonariusze[i].wiek
    choroby = pensjonariusze[i].choroby
    nazwa_domu = pensjonariusze[i].dom.nazwa

    entry_imie_pens.insert(0, imie)
    entry_nazwisko_pens.insert(0, nazwisko)
    entry_wiek_pens.insert(0, wiek)
    entry_choroby.insert(0, choroby)
    entry_dom_pens.insert(0, nazwa_domu)

    button_dodaj_pensjonariusza.config(text="Zapisz zmiany", command=lambda: update_pensjonariusz(i))


def update_pensjonariusz(i):
    pensjonariusz = pensjonariusze[i]
    pensjonariusze[i].imie = entry_imie_pens.get()
    pensjonariusze[i].nazwisko = entry_nazwisko_pens.get()
    pensjonariusze[i].wiek = entry_wiek_pens.get()
    pensjonariusze[i].choroby = entry_choroby.get()
    nazwa_domu = entry_dom_pens.get()

    # Aktualizacja domu
    for dom in domy:
        if dom.nazwa == nazwa_domu:
            if pensjonariusz in pensjonariusz.dom.pensjonariusze:
                pensjonariusz.dom.pensjonariusze.remove(pensjonariusz)

            pensjonariusz.dom = dom
            dom.pensjonariusze.append(pensjonariusz)

            pensjonariusz.coordinates = dom.coordinates

            break

    pensjonariusz.marker.delete()
    pensjonariusz.marker = map_widget.set_marker(pensjonariusz.coordinates[0], pensjonariusz.coordinates[1],
                                                 text=pensjonariusz.imie)

    button_dodaj_pensjonariusza.config(text="Dodaj pensjonariusza", command=add_pensjonariusz)
    entry_imie_pens.delete(0, END)
    entry_nazwisko_pens.delete(0, END)
    entry_wiek_pens.delete(0, END)
    entry_choroby.delete(0, END)
    entry_dom_pens.delete(0, END)

    entry_imie_pens.focus()
    show_pensjonariusze()


def add_pensjonariusz():
    name = entry_imie_pens.get()
    surname = entry_nazwisko_pens.get()
    wiek = entry_wiek_pens.get()
    choroby = entry_choroby.get()
    nazwa_domu = entry_dom_pens.get()

    wybrany_dom = None
    for dom in domy:
        if dom.nazwa == nazwa_domu:
            wybrany_dom = dom
            break

    if wybrany_dom is None:
        print("Błąd: nie znaleziono domu o podanej nazwie.")
        return

    # print(name, surname, wiek, choroby, dom)
    new_pensjonariusz = Pensjonariusz(imie=name, nazwisko=surname, wiek=wiek, choroby=choroby, dom=wybrany_dom)
    pensjonariusze.append(new_pensjonariusz)
    # print(pensjonariusze)

    entry_imie_pens.delete(0, END)
    entry_nazwisko_pens.delete(0, END)
    entry_wiek_pens.delete(0, END)
    entry_choroby.delete(0, END)
    entry_dom_pens.delete(0, END)

    entry_imie_pens.focus()
    show_pensjonariusze()
#UI
root = Tk()
root.title("Mapbook_AB")
root.geometry("1400x900")
listbox_pracownicy_domu = Listbox(width=30, height=20)
listbox_pensjonariusze_domu = Listbox(width=30, height=20)

ramka_mapa = Frame(root)
ramka_mapa.pack(side=BOTTOM, fill=BOTH, expand=True)

map_widget = tkintermapview.TkinterMapView(
    ramka_mapa, width=1400, height=350, corner_radius=4
)
map_widget.set_zoom(6)
map_widget.set_position(52.2, 21.0)
map_widget.pack(fill=X)

ramka_trybow = Frame(root)
ramka_trybow.pack(pady=10)

def pokaz_panel(panel):
    panel_domy.pack_forget()
    panel_pracownicy.pack_forget()
    panel_pensjonariusze.pack_forget()
    panel.pack(side=TOP, fill=BOTH, expand=False)

Button(ramka_trybow, text="DOMY", width=20,
       command=lambda: pokaz_panel(panel_domy)).grid(row=0, column=0, padx=10)

Button(ramka_trybow, text="PRACOWNICY", width=20,
       command=lambda: pokaz_panel(panel_pracownicy)).grid(row=0, column=1, padx=10)

Button(ramka_trybow, text="PENSJONARIUSZE", width=20,
       command=lambda: pokaz_panel(panel_pensjonariusze)).grid(row=0, column=2, padx=10)

load_domy_from_file()
load_pracownicy_from_file()
load_pensjonariusze_from_file()

panel_domy = Frame(root)

Label(panel_domy, text="Lista domów:").grid(row=0, column=0)
listbox_lista_domow = Listbox(panel_domy, width=40, height=20)
listbox_lista_domow.grid(row=1, column=0, rowspan=10, sticky="n")

Button(panel_domy, text="Pokaż szczegóły", command=show_dom_details).grid(row=1, column=1, sticky="w")
Button(panel_domy, text="Usuń", command=remove_dom).grid(row=2, column=1, sticky="w")
Button(panel_domy, text="Edytuj", command=edit_dom).grid(row=3, column=1, sticky="w")

Label(panel_domy, text="Formularz domu").grid(row=0, column=2, columnspan=2)

Label(panel_domy, text="Nazwa:").grid(row=1, column=2, sticky="w")
entry_nazwa = Entry(panel_domy)
entry_nazwa.grid(row=1, column=3, sticky="w")

Label(panel_domy, text="Lokalizacja:").grid(row=2, column=2, sticky="w")
entry_lokalizacja = Entry(panel_domy)
entry_lokalizacja.grid(row=2, column=3, sticky="w")

button_dodaj_dom = Button(panel_domy, text="Dodaj Dom Opieki", command=add_dom)
button_dodaj_dom.grid(row=3, column=2, columnspan=2)

Label(panel_domy, text="Szczegóły domu").grid(row=0, column=4, columnspan=2)

Label(panel_domy, text="Nazwa:").grid(row=1, column=4, sticky="w")
label_nazwa_szczegoly_domu_wartosc = Label(panel_domy, text="---")
label_nazwa_szczegoly_domu_wartosc.grid(row=1, column=5, sticky="w")

Label(panel_domy, text="Lokalizacja:").grid(row=2, column=4, sticky="w")
label_lokalizacja_szczegoly_domu_wartosc = Label(panel_domy, text="---")
label_lokalizacja_szczegoly_domu_wartosc.grid(row=2, column=5, sticky="w")

Label(panel_domy, text="Pracownicy domu").grid(row=0, column=6)
listbox_pracownicy_domu = Listbox(panel_domy, width=30, height=20)
listbox_pracownicy_domu.grid(row=1, column=6, rowspan=10, sticky="n")

Label(panel_domy, text="Pensjonariusze domu").grid(row=0, column=7)
listbox_pensjonariusze_domu = Listbox(panel_domy, width=30, height=20)
listbox_pensjonariusze_domu.grid(row=1, column=7, rowspan=10, sticky="n")

panel_pracownicy = Frame(root)

Label(panel_pracownicy, text="Lista pracowników:").grid(row=0, column=0)
listbox_lista_pracownikow = Listbox(panel_pracownicy, width=40, height=20)
listbox_lista_pracownikow.grid(row=1, column=0, rowspan=10, sticky="n")

Button(panel_pracownicy, text="Pokaż szczegóły", command=show_pracownik_details).grid(row=1, column=1, sticky="w")
Button(panel_pracownicy, text="Usuń", command=remove_pracownik).grid(row=2, column=1, sticky="w")
Button(panel_pracownicy, text="Edytuj", command=edit_pracownik).grid(row=3, column=1, sticky="w")

Label(panel_pracownicy, text="Formularz pracownika").grid(row=0, column=2, columnspan=2)

Label(panel_pracownicy, text="Imię:").grid(row=1, column=2, sticky="w")
entry_imie_prac = Entry(panel_pracownicy)
entry_imie_prac.grid(row=1, column=3, sticky="w")

Label(panel_pracownicy, text="Nazwisko:").grid(row=2, column=2, sticky="w")
entry_nazwisko_prac = Entry(panel_pracownicy)
entry_nazwisko_prac.grid(row=2, column=3, sticky="w")

Label(panel_pracownicy, text="Wiek:").grid(row=3, column=2, sticky="w")
entry_wiek_prac = Entry(panel_pracownicy)
entry_wiek_prac.grid(row=3, column=3, sticky="w")

Label(panel_pracownicy, text="Rola:").grid(row=4, column=2, sticky="w")
entry_rola = Entry(panel_pracownicy)
entry_rola.grid(row=4, column=3, sticky="w")

Label(panel_pracownicy, text="Dom:").grid(row=5, column=2, sticky="w")
entry_dom_prac = Entry(panel_pracownicy)
entry_dom_prac.grid(row=5, column=3, sticky="w")

button_dodaj_pracownika = Button(panel_pracownicy, text="Dodaj pracownika", command=add_pracownik)
button_dodaj_pracownika.grid(row=6, column=2, columnspan=2)

Label(panel_pracownicy, text="Szczegóły pracownika").grid(row=0, column=4, columnspan=2)

Label(panel_pracownicy, text="Imię:").grid(row=1, column=4, sticky="w")
label_imie_szczegoly_pracownika_wartosc = Label(panel_pracownicy, text="---")
label_imie_szczegoly_pracownika_wartosc.grid(row=1, column=5, sticky="w")

Label(panel_pracownicy, text="Nazwisko:").grid(row=2, column=4, sticky="w")
label_nazwisko_szczegoly_pracownika_wartosc = Label(panel_pracownicy, text="---")
label_nazwisko_szczegoly_pracownika_wartosc.grid(row=2, column=5, sticky="w")

Label(panel_pracownicy, text="Wiek:").grid(row=3, column=4, sticky="w")
label_wiek_szczegoly_pracownika_wartosc = Label(panel_pracownicy, text="---")
label_wiek_szczegoly_pracownika_wartosc.grid(row=3, column=5, sticky="w")

Label(panel_pracownicy, text="Rola:").grid(row=4, column=4, sticky="w")
label_rola_szczegoly_pracownika_wartosc = Label(panel_pracownicy, text="---")
label_rola_szczegoly_pracownika_wartosc.grid(row=4, column=5, sticky="w")

Label(panel_pracownicy, text="Dom:").grid(row=5, column=4, sticky="w")
label_dom_szczegoly_pracownika_wartosc = Label(panel_pracownicy, text="---")
label_dom_szczegoly_pracownika_wartosc.grid(row=5, column=5, sticky="w")

Label(panel_pracownicy, text="Lokalizacja:").grid(row=6, column=4, sticky="w")
label_lokalizacja_szczegoly_pracownika_wartosc = Label(panel_pracownicy, text="---")
label_lokalizacja_szczegoly_pracownika_wartosc.grid(row=6, column=5, sticky="w")

panel_pensjonariusze = Frame(root)

Label(panel_pensjonariusze, text="Lista pensjonariuszy:").grid(row=0, column=0)
listbox_lista_pensjonariuszy = Listbox(panel_pensjonariusze, width=40, height=20)
listbox_lista_pensjonariuszy.grid(row=1, column=0, rowspan=10, sticky="n")

Button(panel_pensjonariusze, text="Pokaż szczegóły", command=show_pensjonariusz_details).grid(row=1, column=1, sticky="w")
Button(panel_pensjonariusze, text="Usuń", command=remove_pensjonariusz).grid(row=2, column=1, sticky="w")
Button(panel_pensjonariusze, text="Edytuj", command=edit_pensjonariusz).grid(row=3, column=1, sticky="w")

Label(panel_pensjonariusze, text="Formularz pensjonariusza").grid(row=0, column=2, columnspan=2)

Label(panel_pensjonariusze, text="Imię:").grid(row=1, column=2, sticky="w")
entry_imie_pens = Entry(panel_pensjonariusze)
entry_imie_pens.grid(row=1, column=3, sticky="w")

Label(panel_pensjonariusze, text="Nazwisko:").grid(row=2, column=2, sticky="w")
entry_nazwisko_pens = Entry(panel_pensjonariusze)
entry_nazwisko_pens.grid(row=2, column=3, sticky="w")

Label(panel_pensjonariusze, text="Wiek:").grid(row=3, column=2, sticky="w")
entry_wiek_pens = Entry(panel_pensjonariusze)
entry_wiek_pens.grid(row=3, column=3, sticky="w")

Label(panel_pensjonariusze, text="Choroby:").grid(row=4, column=2, sticky="w")
entry_choroby = Entry(panel_pensjonariusze)
entry_choroby.grid(row=4, column=3, sticky="w")

Label(panel_pensjonariusze, text="Dom:").grid(row=5, column=2, sticky="w")
entry_dom_pens = Entry(panel_pensjonariusze)
entry_dom_pens.grid(row=5, column=3, sticky="w")

button_dodaj_pensjonariusza = Button(panel_pensjonariusze, text="Dodaj pensjonariusza", command=add_pensjonariusz)
button_dodaj_pensjonariusza.grid(row=6, column=2, columnspan=2)

Label(panel_pensjonariusze, text="Szczegóły pensjonariusza").grid(row=0, column=4, columnspan=2)

Label(panel_pensjonariusze, text="Imię:").grid(row=1, column=4, sticky="w")
label_imie_szczegoly_pensjonariusza_wartosc = Label(panel_pensjonariusze, text="---")
label_imie_szczegoly_pensjonariusza_wartosc.grid(row=1, column=5, sticky="w")

Label(panel_pensjonariusze, text="Nazwisko:").grid(row=2, column=4, sticky="w")
label_nazwisko_szczegoly_pensjonariusza_wartosc = Label(panel_pensjonariusze, text="---")
label_nazwisko_szczegoly_pensjonariusza_wartosc.grid(row=2, column=5, sticky="w")

Label(panel_pensjonariusze, text="Wiek:").grid(row=3, column=4, sticky="w")
label_wiek_szczegoly_pensjonariusza_wartosc = Label(panel_pensjonariusze, text="---")
label_wiek_szczegoly_pensjonariusza_wartosc.grid(row=3, column=5, sticky="w")

Label(panel_pensjonariusze, text="Choroby:").grid(row=4, column=4, sticky="w")
label_choroby_szczegoly_pensjonariusza_wartosc = Label(panel_pensjonariusze, text="---")
label_choroby_szczegoly_pensjonariusza_wartosc.grid(row=4, column=5, sticky="w")

Label(panel_pensjonariusze, text="Dom:").grid(row=5, column=4, sticky="w")
label_dom_szczegoly_pensjonariusza_wartosc = Label(panel_pensjonariusze, text="---")
label_dom_szczegoly_pensjonariusza_wartosc.grid(row=5, column=5, sticky="w")

Label(panel_pensjonariusze, text="Lokalizacja:").grid(row=6, column=4, sticky="w")
label_lokalizacja_szczegoly_pensjonariusza_wartosc = Label(panel_pensjonariusze, text="---")
label_lokalizacja_szczegoly_pensjonariusza_wartosc.grid(row=6, column=5, sticky="w")

show_domy()
show_pracownicy()
show_pensjonariusze()
pokaz_panel(panel_domy)

def on_close():
    save_domy_to_file()
    save_pracownicy_to_file()
    save_pensjonariusze_to_file()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()

