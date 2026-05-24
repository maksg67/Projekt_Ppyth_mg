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

        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"{self.imie} {self.nazwisko}")
        
def save_pensjonariusze_to_file():
    with open("pensjonariusze.txt", "w", encoding="utf-8") as f:
        for pensjonariusz in pensjonariusze:
            f.write(f"{pensjonariusz.imie};{pensjonariusz.nazwisko};{pensjonariusz.wiek};{pensjonariusz.choroby};{pensjonariusz.dom.nazwa}\n")

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
    entry_nazwsiko_pens.insert(0, nazwisko)
    entry_wiek_pens.insert(0, wiek)
    entry_choroby.insert(0, choroby)
    entry_dom_pens.insert(0, nazwa_domu)

    button_dodaj_pensjonariusza.config(text="Zapisz zmiany", command=lambda: update_pensjonariusz(i))


def update_pensjonariusz(i):
    pensjonariusz = pensjonariusze[i]
    pensjonariusze[i].imie = entry_imie_pens.get()
    pensjonariusze[i].nazwisko = entry_nazwsiko_pens.get()
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
    pensjonariusz.marker = map_widget.set_marker(pensjonariusz.coordinates[0],pensjonariusz.coordinates[1],text=pensjonariusz.imie)

    button_dodaj_pensjonariusza.config(text="Dodaj pensjonariusza", command=add_pensjonariusz)
    entry_imie_pens.delete(0, END)
    entry_nazwsiko_pens.delete(0, END)
    entry_wiek_pens.delete(0, END)
    entry_choroby.delete(0, END)
    entry_dom_pens.delete(0, END)

    entry_imie_pens.focus()
    show_pensjonariusze()


def add_pensjonariusz():
    name = entry_imie_pens.get()
    surname = entry_nazwsiko_pens.get()
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
    entry_nazwsiko_pens.delete(0, END)
    entry_wiek_pens.delete(0, END)
    entry_choroby.delete(0, END)
    entry_dom_pens.delete(0, END)

    entry_imie_pens.focus()
    show_pensjonariusze()