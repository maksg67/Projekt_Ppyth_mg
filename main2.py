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
    nazwa = domy[i].nazwa
    lokalizacja = domy[i].lokalizacja

    label_nazwa_szczegoly_domu_wartosc.config(text=nazwa)
    label_lokalizacja_szczegoly_domu_wartosc.config(text=lokalizacja)
    map_widget.set_position(domy[i].coordinates[0], domy[i].coordinates[1])
    map_widget.set_zoom(12)

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
