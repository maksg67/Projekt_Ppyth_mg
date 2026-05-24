# ============================
# OKNO GŁÓWNE
# ============================

root = Tk()
root.title("Mapbook_AB")
root.geometry("1400x900")

# ============================
# MAPA (musi być przed klasami)
# ============================

ramka_mapa = Frame(root)
ramka_mapa.pack(side=BOTTOM, fill=BOTH, expand=True)

map_widget = tkintermapview.TkinterMapView(
    ramka_mapa, width=1400, height=500, corner_radius=4
)
map_widget.set_zoom(6)
map_widget.set_position(52.2, 21.0)
map_widget.pack(fill=BOTH, expand=True)

# ============================
# TRYBY – PRZYCISKI
# ============================

ramka_trybow = Frame(root)
ramka_trybow.pack(pady=10)

def pokaz_panel(panel):
    panel_domy.pack_forget()
    panel_pracownicy.pack_forget()
    panel_pensjonariusze.pack_forget()
    panel.pack(fill=BOTH, expand=False)

Button(ramka_trybow, text="DOMY", width=20,
       command=lambda: pokaz_panel(panel_domy)).grid(row=0, column=0, padx=10)

Button(ramka_trybow, text="PRACOWNICY", width=20,
       command=lambda: pokaz_panel(panel_pracownicy)).grid(row=0, column=1, padx=10)

Button(ramka_trybow, text="PENSJONARIUSZE", width=20,
       command=lambda: pokaz_panel(panel_pensjonariusze)).grid(row=0, column=2, padx=10)

# ============================
# PANEL DOMÓW
# ============================

panel_domy = Frame(root)

# --- lista domów ---
Label(panel_domy, text="Lista domów:").grid(row=0, column=0)
listbox_lista_domow = Listbox(panel_domy, width=40, height=15)
listbox_lista_domow.grid(row=1, column=0, rowspan=4)

Button(panel_domy, text="Pokaż szczegóły", command=show_dom_details).grid(row=1, column=1)
Button(panel_domy, text="Usuń", command=remove_dom).grid(row=2, column=1)
Button(panel_domy, text="Edytuj", command=edit_dom).grid(row=3, column=1)

# --- formularz dodawania domu ---
Label(panel_domy, text="Formularz domu").grid(row=0, column=2, columnspan=2)

Label(panel_domy, text="Nazwa:").grid(row=1, column=2, sticky=W)
entry_nazwa = Entry(panel_domy)
entry_nazwa.grid(row=1, column=3)

Label(panel_domy, text="Lokalizacja:").grid(row=2, column=2, sticky=W)
entry_lokalizacja = Entry(panel_domy)
entry_lokalizacja.grid(row=2, column=3)

button_dodaj_dom = Button(panel_domy, text="Dodaj Dom Opieki", command=add_dom)
button_dodaj_dom.grid(row=3, column=2, columnspan=2)

# --- szczegóły domu ---
Label(panel_domy, text="Szczegóły domu").grid(row=4, column=2, columnspan=2)

Label(panel_domy, text="Nazwa:").grid(row=5, column=2, sticky=W)
label_nazwa_szczegoly_domu_wartosc = Label(panel_domy, text="---")
label_nazwa_szczegoly_domu_wartosc.grid(row=5, column=3, sticky=W)

Label(panel_domy, text="Lokalizacja:").grid(row=6, column=2, sticky=W)
label_lokalizacja_szczegoly_domu_wartosc = Label(panel_domy, text="---")
label_lokalizacja_szczegoly_domu_wartosc.grid(row=6, column=3, sticky=W)

# ============================
# PANEL PRACOWNIKÓW
# ============================

panel_pracownicy = Frame(root)

Label(panel_pracownicy, text="Lista pracowników:").grid(row=0, column=0)
listbox_lista_pracownikow = Listbox(panel_pracownicy, width=40, height=15)
listbox_lista_pracownikow.grid(row=1, column=0, rowspan=6)

Button(panel_pracownicy, text="Pokaż szczegóły", command=show_pracownik_details).grid(row=1, column=1)
Button(panel_pracownicy, text="Usuń", command=remove_pracownik).grid(row=2, column=1)
Button(panel_pracownicy, text="Edytuj", command=edit_pracownik).grid(row=3, column=1)

# --- formularz pracownika ---
Label(panel_pracownicy, text="Formularz pracownika").grid(row=0, column=2, columnspan=2)

Label(panel_pracownicy, text="Imię:").grid(row=1, column=2, sticky=W)
entry_imie = Entry(panel_pracownicy)
entry_imie.grid(row=1, column=3)

Label(panel_pracownicy, text="Nazwisko:").grid(row=2, column=2, sticky=W)
entry_nazwisko = Entry(panel_pracownicy)
entry_nazwisko.grid(row=2, column=3)

Label(panel_pracownicy, text="Wiek:").grid(row=3, column=2, sticky=W)
entry_wiek = Entry(panel_pracownicy)
entry_wiek.grid(row=3, column=3)

Label(panel_pracownicy, text="Rola:").grid(row=4, column=2, sticky=W)
entry_rola = Entry(panel_pracownicy)
entry_rola.grid(row=4, column=3)

Label(panel_pracownicy, text="Dom:").grid(row=5, column=2, sticky=W)
entry_dom = Entry(panel_pracownicy)
entry_dom.grid(row=5, column=3)

button_dodaj_pracownika = Button(panel_pracownicy, text="Dodaj pracownika", command=add_pracownik)
button_dodaj_pracownika.grid(row=6, column=2, columnspan=2)

# --- szczegóły pracownika ---
Label(panel_pracownicy, text="Szczegóły pracownika").grid(row=7, column=2, columnspan=2)

Label(panel_pracownicy, text="Imię:").grid(row=8, column=2, sticky=W)
label_imie_szczegoly_pracownika_wartosc = Label(panel_pracownicy, text="---")
label_imie_szczegoly_pracownika_wartosc.grid(row=8, column=3, sticky=W)

Label(panel_pracownicy, text="Nazwisko:").grid(row=9, column=2, sticky=W)
label_nazwisko_szczegoly_pracownika_wartosc = Label(panel_pracownicy, text="---")
label_nazwisko_szczegoly_pracownika_wartosc.grid(row=9, column=3, sticky=W)

Label(panel_pracownicy, text="Wiek:").grid(row=10, column=2, sticky=W)
label_wiek_szczegoly_pracownika_wartosc = Label(panel_pracownicy, text="---")
label_wiek_szczegoly_pracownika_wartosc.grid(row=10, column=3, sticky=W)

Label(panel_pracownicy, text="Rola:").grid(row=11, column=2, sticky=W)
label_rola_szczegoly_pracownika_wartosc = Label(panel_pracownicy, text="---")
label_rola_szczegoly_pracownika_wartosc.grid(row=11, column=3, sticky=W)

Label(panel_pracownicy, text="Dom:").grid(row=12, column=2, sticky=W)
label_dom_szczegoly_pracownika_wartosc = Label(panel_pracownicy, text="---")
label_dom_szczegoly_pracownika_wartosc.grid(row=12, column=3, sticky=W)

Label(panel_pracownicy, text="Lokalizacja:").grid(row=13, column=2, sticky=W)
label_lokalizacja_szczegoly_pracownika_wartosc = Label(panel_pracownicy, text="---")
label_lokalizacja_szczegoly_pracownika_wartosc.grid(row=13, column=3, sticky=W)

# ============================
# PANEL PENSJONARIUSZY
# ============================

panel_pensjonariusze = Frame(root)

Label(panel_pensjonariusze, text="Lista pensjonariuszy:").grid(row=0, column=0)
listbox_lista_pensjonariuszy = Listbox(panel_pensjonariusze, width=40, height=15)
listbox_lista_pensjonariuszy.grid(row=1, column=0, rowspan=6)

Button(panel_pensjonariusze, text="Pokaż szczegóły", command=show_pensjonariusz_details).grid(row=1, column=1)
Button(panel_pensjonariusze, text="Usuń", command=remove_pensjonariusz).grid(row=2, column=1)
Button(panel_pensjonariusze, text="Edytuj", command=edit_pensjonariusz).grid(row=3, column=1)

# --- formularz pensjonariusza ---
Label(panel_pensjonariusze, text="Formularz pensjonariusza").grid(row=0, column=2, columnspan=2)

Label(panel_pensjonariusze, text="Imię:").grid(row=1, column=2, sticky=W)
entry_imie = Entry(panel_pensjonariusze)
entry_imie.grid(row=1, column=3)

Label(panel_pensjonariusze, text="Nazwisko:").grid(row=2, column=2, sticky=W)
entry_nazwisko = Entry(panel_pensjonariusze)
entry_nazwisko.grid(row=2, column=3)

Label(panel_pensjonariusze, text="Wiek:").grid(row=3, column=2, sticky=W)
entry_wiek = Entry(panel_pensjonariusze)
entry_wiek.grid(row=3, column=3)

Label(panel_pensjonariusze, text="Choroby:").grid(row=4, column=2, sticky=W)
entry_choroby = Entry(panel_pensjonariusze)
entry_choroby.grid(row=4, column=3)

Label(panel_pensjonariusze, text="Dom:").grid(row=5, column=2, sticky=W)
entry_dom = Entry(panel_pensjonariusze)
entry_dom.grid(row=5, column=3)

button_dodaj_pensjonariusza = Button(panel_pensjonariusze, text="Dodaj pensjonariusza", command=add_pensjonariusz)
button_dodaj_pensjonariusza.grid(row=6, column=2, columnspan=2)

# --- szczegóły pensjonariusza ---
Label(panel_pensjonariusze, text="Szczegóły pensjonariusza").grid(row=7, column=2, columnspan=2)

Label(panel_pensjonariusze, text="Imię:").grid(row=8, column=2, sticky=W)
label_imie_szczegoly_pensjonariusza_wartosc = Label(panel_pensjonariusze, text="---")
label_imie_szczegoly_pensjonariusza_wartosc.grid(row=8, column=3, sticky=W)

Label(panel_pensjonariusze, text="Nazwisko:").grid(row=9, column=2, sticky=W)
label_nazwisko_szczegoly_pensjonariusza_wartosc = Label(panel_pensjonariusze, text="---")
label_nazwisko_szczegoly_pensjonariusza_wartosc.grid(row=9, column=3, sticky=W)

Label(panel_pensjonariusze, text="Wiek:").grid(row=10, column=2, sticky=W)
label_wiek_szczegoly_pensjonariusza_wartosc = Label(panel_pensjonariusze, text="---")
label_wiek_szczegoly_pensjonariusza_wartosc.grid(row=10, column=3, sticky=W)

Label(panel_pensjonariusze, text="Choroby:").grid(row=11, column=2, sticky=W)
label_choroby_szczegoly_pensjonariusza_wartosc = Label(panel_pensjonariusze, text="---")
label_choroby_szczegoly_pensjonariusza_wartosc.grid(row=11, column=3, sticky=W)

Label(panel_pensjonariusze, text="Dom:").grid(row=12, column=2, sticky=W)
label_dom_szczegoly_pensjonariusza_wartosc = Label(panel_pensjonariusze, text="---")
label_dom_szczegoly_pensjonariusza_wartosc.grid(row=12, column=3, sticky=W)

Label(panel_pensjonariusze, text="Lokalizacja:").grid(row=13, column=2, sticky=W)
label_lokalizacja_szczegoly_pensjonariusza_wartosc = Label(panel_pensjonariusze, text="---")
label_lokalizacja_szczegoly_pensjonariusza_wartosc.grid(row=13, column=3, sticky=W)

# ============================
# START – pokazujemy panel domów
# ============================

pokaz_panel(panel_domy)

root.mainloop()

# Zapis do TXT
def on_close():
    save_domy_to_file()
    save_pracownicy_to_file()
    save_pensjonariusze_to_file()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)