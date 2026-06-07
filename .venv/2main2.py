from tkinter import *
import tkintermapview
import controller

root = Tk()
root.title("Mapbook_AB")
root.geometry("1400x900")

ramka_mapa = Frame(root)
ramka_mapa.pack(side=BOTTOM, fill=BOTH, expand=True)

map_widget = tkintermapview.TkinterMapView(
    ramka_mapa, width=1400, height=350, corner_radius=4
)
map_widget.set_zoom(6)
map_widget.set_position(52.2, 21.0)
map_widget.pack(fill=X)

controller.load_model(map_widget)

ramka_trybow = Frame(root)
ramka_trybow.pack(pady=10)

panel_domy = Frame(root)
panel_pracownicy = Frame(root)
panel_pensjonariusze = Frame(root)

current_mode = "domy"


def show_domy():
    listbox_lista_domow.delete(0, END)
    for idx, dom in enumerate(controller.domy):
        listbox_lista_domow.insert(idx, dom.nazwa)


def show_pracownicy():
    listbox_lista_pracownikow.delete(0, END)
    for idx, pracownik in enumerate(controller.pracownicy):
        listbox_lista_pracownikow.insert(idx, pracownik.imie)


def show_pensjonariusze():
    listbox_lista_pensjonariuszy.delete(0, END)
    for idx, pensjonariusz in enumerate(controller.pensjonariusze):
        listbox_lista_pensjonariuszy.insert(idx, pensjonariusz.imie)


def pokaz_panel(panel, mode):
    global current_mode
    current_mode = mode
    panel_domy.pack_forget()
    panel_pracownicy.pack_forget()
    panel_pensjonariusze.pack_forget()
    panel.pack(side=TOP, fill=BOTH, expand=False)

    if mode == "domy":
        controller.show_all_domy(map_widget)
    elif mode == "pracownicy":
        controller.show_all_pracownicy(map_widget)
    elif mode == "pensjonariusze":
        controller.show_all_pensjonariusze(map_widget)


Button(ramka_trybow, text="DOMY", width=20,
       command=lambda: pokaz_panel(panel_domy, "domy")).grid(row=0, column=0, padx=10)

Button(ramka_trybow, text="PRACOWNICY", width=20,
       command=lambda: pokaz_panel(panel_pracownicy, "pracownicy")).grid(row=0, column=1, padx=10)

Button(ramka_trybow, text="PENSJONARIUSZE", width=20,
       command=lambda: pokaz_panel(panel_pensjonariusze, "pensjonariusze")).grid(row=0, column=2, padx=10)
# PANEL DOMY
Label(panel_domy, text="Lista domów:").grid(row=0, column=0)

Label(panel_domy, text="Filtr:").grid(row=1, column=0, sticky="w")
entry_filter_domy = Entry(panel_domy)
entry_filter_domy.grid(row=2, column=0, sticky="w")

listbox_lista_domow = Listbox(panel_domy, width=40, height=20)
listbox_lista_domow.grid(row=3, column=0, rowspan=10, sticky="n")

Button(panel_domy, text="Pokaż szczegóły", command=lambda: show_dom_details()).grid(row=3, column=1, sticky="w")
Button(panel_domy, text="Usuń", command=lambda: remove_dom()).grid(row=4, column=1, sticky="w")
Button(panel_domy, text="Edytuj", command=lambda: edit_dom()).grid(row=5, column=1, sticky="w")

Label(panel_domy, text="Formularz domu").grid(row=0, column=2, columnspan=2)

Label(panel_domy, text="Nazwa:").grid(row=1, column=2, sticky="w")
entry_nazwa = Entry(panel_domy)
entry_nazwa.grid(row=1, column=3, sticky="w")

Label(panel_domy, text="Lokalizacja:").grid(row=2, column=2, sticky="w")
entry_lokalizacja = Entry(panel_domy)
entry_lokalizacja.grid(row=2, column=3, sticky="w")

button_dodaj_dom = Button(panel_domy, text="Dodaj Dom Opieki", command=lambda: add_dom())
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


def add_dom():
    name = entry_nazwa.get()
    lokalizacja = entry_lokalizacja.get()
    controller.add_dom(name, lokalizacja, map_widget)
    entry_nazwa.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_nazwa.focus()
    show_domy()
    controller.save_model()


def remove_dom():
    i = listbox_lista_domow.index(ACTIVE)
    controller.remove_dom(i, map_widget)
    show_domy()
    controller.save_model()


def edit_dom():
    i = listbox_lista_domow.index(ACTIVE)
    dom = controller.domy[i]
    entry_nazwa.insert(0, dom.nazwa)
    entry_lokalizacja.insert(0, dom.lokalizacja)
    button_dodaj_dom.config(text="Zapisz zmiany", command=lambda: update_dom(i))


def update_dom(i):
    controller.update_dom(i, entry_nazwa.get(), entry_lokalizacja.get(), map_widget)
    button_dodaj_dom.config(text="Dodaj Dom Opieki", command=add_dom)
    entry_nazwa.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_nazwa.focus()
    show_domy()
    controller.save_model()


def show_dom_details():
    i = listbox_lista_domow.index(ACTIVE)
    dom = controller.domy[i]
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


def on_filter_domy(event):
    query = entry_filter_domy.get()
    if query == "":
        wyniki = controller.show_all_domy(map_widget)
    else:
        wyniki = controller.filter_domy(query, map_widget)
    listbox_lista_domow.delete(0, END)
    for d in wyniki:
        listbox_lista_domow.insert(END, d.nazwa)


entry_filter_domy.bind("<KeyRelease>", on_filter_domy)


# PANEL PRACOWNICY
Label(panel_pracownicy, text="Lista pracowników:").grid(row=0, column=0)

Label(panel_pracownicy, text="Filtr:").grid(row=1, column=0, sticky="w")
entry_filter_prac = Entry(panel_pracownicy)
entry_filter_prac.grid(row=2, column=0, sticky="w")

listbox_lista_pracownikow = Listbox(panel_pracownicy, width=40, height=20)
listbox_lista_pracownikow.grid(row=3, column=0, rowspan=10, sticky="n")

Button(panel_pracownicy, text="Pokaż szczegóły", command=lambda: show_pracownik_details()).grid(row=3, column=1, sticky="w")
Button(panel_pracownicy, text="Usuń", command=lambda: remove_pracownik()).grid(row=4, column=1, sticky="w")
Button(panel_pracownicy, text="Edytuj", command=lambda: edit_pracownik()).grid(row=5, column=1, sticky="w")

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

button_dodaj_pracownika = Button(panel_pracownicy, text="Dodaj pracownika", command=lambda: add_pracownik())
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


def add_pracownik():
    ok = controller.add_pracownik(
        entry_imie_prac.get(),
        entry_nazwisko_prac.get(),
        entry_wiek_prac.get(),
        entry_rola.get(),
        entry_dom_prac.get(),
        map_widget
    )
    if not ok:
        return
    entry_imie_prac.delete(0, END)
    entry_nazwisko_prac.delete(0, END)
    entry_wiek_prac.delete(0, END)
    entry_rola.delete(0, END)
    entry_dom_prac.delete(0, END)
    entry_imie_prac.focus()
    show_pracownicy()
    controller.save_model()


def remove_pracownik():
    i = listbox_lista_pracownikow.index(ACTIVE)
    controller.remove_pracownik(i, map_widget)
    show_pracownicy()
    controller.save_model()


def edit_pracownik():
    i = listbox_lista_pracownikow.index(ACTIVE)
    p = controller.pracownicy[i]
    entry_imie_prac.insert(0, p.imie)
    entry_nazwisko_prac.insert(0, p.nazwisko)
    entry_wiek_prac.insert(0, p.wiek)
    entry_rola.insert(0, p.rola)
    entry_dom_prac.insert(0, p.dom.nazwa)
    button_dodaj_pracownika.config(text="Zapisz zmiany", command=lambda: update_pracownik(i))


def update_pracownik(i):
    controller.update_pracownik(
        i,
        entry_imie_prac.get(),
        entry_nazwisko_prac.get(),
        entry_wiek_prac.get(),
        entry_rola.get(),
        entry_dom_prac.get(),
        map_widget
    )
    button_dodaj_pracownika.config(text="Dodaj pracownika", command=add_pracownik)
    entry_imie_prac.delete(0, END)
    entry_nazwisko_prac.delete(0, END)
    entry_wiek_prac.delete(0, END)
    entry_rola.delete(0, END)
    entry_dom_prac.delete(0, END)
    entry_imie_prac.focus()
    show_pracownicy()
    controller.save_model()


def show_pracownik_details():
    i = listbox_lista_pracownikow.index(ACTIVE)
    p = controller.pracownicy[i]
    label_imie_szczegoly_pracownika_wartosc.config(text=p.imie)
    label_nazwisko_szczegoly_pracownika_wartosc.config(text=p.nazwisko)
    label_wiek_szczegoly_pracownika_wartosc.config(text=p.wiek)
    label_rola_szczegoly_pracownika_wartosc.config(text=p.rola)
    label_dom_szczegoly_pracownika_wartosc.config(text=p.dom.nazwa)
    label_lokalizacja_szczegoly_pracownika_wartosc.config(text=p.dom.lokalizacja)
    map_widget.set_position(p.coordinates[0], p.coordinates[1])
    map_widget.set_zoom(12)


def on_filter_prac(event):
    query = entry_filter_prac.get()
    if query == "":
        wyniki = controller.show_all_pracownicy(map_widget)
    else:
        wyniki = controller.filter_pracownicy(query, map_widget)
    listbox_lista_pracownikow.delete(0, END)
    for p in wyniki:
        listbox_lista_pracownikow.insert(END, p.imie)


entry_filter_prac.bind("<KeyRelease>", on_filter_prac)


# PANEL PENSJONARIUSZE
Label(panel_pensjonariusze, text="Lista pensjonariuszy:").grid(row=0, column=0)

Label(panel_pensjonariusze, text="Filtr:").grid(row=1, column=0, sticky="w")
entry_filter_pens = Entry(panel_pensjonariusze)
entry_filter_pens.grid(row=2, column=0, sticky="w")

listbox_lista_pensjonariuszy = Listbox(panel_pensjonariusze, width=40, height=20)
listbox_lista_pensjonariuszy.grid(row=3, column=0, rowspan=10, sticky="n")

Button(panel_pensjonariusze, text="Pokaż szczegóły", command=lambda: show_pensjonariusz_details()).grid(row=3, column=1, sticky="w")
Button(panel_pensjonariusze, text="Usuń", command=lambda: remove_pensjonariusz()).grid(row=4, column=1, sticky="w")
Button(panel_pensjonariusze, text="Edytuj", command=lambda: edit_pensjonariusz()).grid(row=5, column=1, sticky="w")

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

button_dodaj_pensjonariusza = Button(panel_pensjonariusze, text="Dodaj pensjonariusza", command=lambda: add_pensjonariusz())
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


def add_pensjonariusz():
    ok = controller.add_pensjonariusz(
        entry_imie_pens.get(),
        entry_nazwisko_pens.get(),
        entry_wiek_pens.get(),
        entry_choroby.get(),
        entry_dom_pens.get(),
        map_widget
    )
    if not ok:
        return
    entry_imie_pens.delete(0, END)
    entry_nazwisko_pens.delete(0, END)
    entry_wiek_pens.delete(0, END)
    entry_choroby.delete(0, END)
    entry_dom_pens.delete(0, END)
    entry_imie_pens.focus()
    show_pensjonariusze()
    controller.save_model()


def remove_pensjonariusz():
    i = listbox_lista_pensjonariuszy.index(ACTIVE)
    controller.remove_pensjonariusz(i, map_widget)
    show_pensjonariusze()
    controller.save_model()


def edit_pensjonariusz():
    i = listbox_lista_pensjonariuszy.index(ACTIVE)
    p = controller.pensjonariusze[i]
    entry_imie_pens.insert(0, p.imie)
    entry_nazwisko_pens.insert(0, p.nazwisko)
    entry_wiek_pens.insert(0, p.wiek)
    entry_choroby.insert(0, p.choroby)
    entry_dom_pens.insert(0, p.dom.nazwa)
    button_dodaj_pensjonariusza.config(text="Zapisz zmiany", command=lambda: update_pensjonariusz(i))


def update_pensjonariusz(i):
    controller.update_pensjonariusz(
        i,
        entry_imie_pens.get(),
        entry_nazwisko_pens.get(),
        entry_wiek_pens.get(),
        entry_choroby.get(),
        entry_dom_pens.get(),
        map_widget
    )
    button_dodaj_pensjonariusza.config(text="Dodaj pensjonariusza", command=add_pensjonariusz)
    entry_imie_pens.delete(0, END)
    entry_nazwisko_pens.delete(0, END)
    entry_wiek_pens.delete(0, END)
    entry_choroby.delete(0, END)
    entry_dom_pens.delete(0, END)
    entry_imie_pens.focus()
    show_pensjonariusze()
    controller.save_model()


def show_pensjonariusz_details():
    i = listbox_lista_pensjonariuszy.index(ACTIVE)
    p = controller.pensjonariusze[i]
    label_imie_szczegoly_pensjonariusza_wartosc.config(text=p.imie)
    label_nazwisko_szczegoly_pensjonariusza_wartosc.config(text=p.nazwisko)
    label_wiek_szczegoly_pensjonariusza_wartosc.config(text=p.wiek)
    label_choroby_szczegoly_pensjonariusza_wartosc.config(text=p.choroby)
    label_dom_szczegoly_pensjonariusza_wartosc.config(text=p.dom.nazwa)
    label_lokalizacja_szczegoly_pensjonariusza_wartosc.config(text=p.dom.lokalizacja)
    map_widget.set_position(p.coordinates[0], p.coordinates[1])
    map_widget.set_zoom(12)


def on_filter_pens(event):
    query = entry_filter_pens.get()
    if query == "":
        wyniki = controller.show_all_pensjonariusze(map_widget)
    else:
        wyniki = controller.filter_pensjonariusze(query, map_widget)
    listbox_lista_pensjonariuszy.delete(0, END)
    for p in wyniki:
        listbox_lista_pensjonariuszy.insert(END, p.imie)


entry_filter_pens.bind("<KeyRelease>", on_filter_pens)

show_domy()
show_pracownicy()
show_pensjonariusze()
pokaz_panel(panel_domy, "domy")

root.mainloop()
