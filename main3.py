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

    entry_imie.insert(0, imie)
    entry_nazwisko.insert(0, nazwisko)
    entry_wiek.insert(0, wiek)
    entry_rola.insert(0, rola)
    entry_dom.insert(0, nazwa_domu)

    button_dodaj_pracownika.config(text="Zapisz zmiany", command=lambda: update_pracownik(i))


def update_pracownik(i):
    pracownik = pracownicy[i]
    pracownicy[i].imie = entry_imie.get()
    pracownicy[i].nazwisko = entry_nazwisko.get()
    pracownicy[i].wiek = entry_wiek.get()
    pracownicy[i].rola = entry_rola.get()
    nazwa_domu = entry_dom.get()

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
    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_wiek.delete(0, END)
    entry_rola.delete(0, END)
    entry_dom.delete(0, END)

    entry_imie.focus()
    show_pracownicy()


def add_pracownik():
    name = entry_imie.get()
    surname = entry_nazwisko.get()
    wiek = entry_wiek.get()
    rola = entry_rola.get()
    nazwa_domu = entry_dom.get()

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

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_wiek.delete(0, END)
    entry_rola.delete(0, END)
    entry_dom.delete(0, END)

    entry_imie.focus()
    show_pracownicy()