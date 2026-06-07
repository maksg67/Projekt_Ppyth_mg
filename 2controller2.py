from bs4 import BeautifulSoup
import requests

domy = []
pracownicy = []
pensjonariusze = []


def get_coordinates(location: str) -> list:
    url = f"https://pl.wikipedia.org/wiki/{location}"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(response.text, 'html.parser')
    lat = float(html.select(".latitude")[1].text.replace(",", "."))
    lon = float(html.select(".longitude")[1].text.replace(",", "."))
    return [lat, lon]


class DomOpieki:
    def __init__(self, nazwa, lokalizacja):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.coordinates = get_coordinates(lokalizacja)
        self.pracownicy = []
        self.pensjonariusze = []


class Pracownik:
    def __init__(self, imie, nazwisko, wiek, rola, dom):
        self.imie = imie
        self.nazwisko = nazwisko
        self.wiek = wiek
        self.rola = rola
        self.dom = dom
        self.coordinates = dom.coordinates


class Pensjonariusz:
    def __init__(self, imie, nazwisko, wiek, choroby, dom):
        self.imie = imie
        self.nazwisko = nazwisko
        self.wiek = wiek
        self.choroby = choroby
        self.dom = dom
        self.coordinates = dom.coordinates


markers = {
    "domy": [],
    "pracownicy": [],
    "pensjonariusze": []
}


def clear_all_markers(map_widget):
    map_widget.delete_all_marker()
    markers["domy"].clear()
    markers["pracownicy"].clear()
    markers["pensjonariusze"].clear()


def create_dom_marker(dom, map_widget):
    m = map_widget.set_marker(dom.coordinates[0], dom.coordinates[1], text=dom.nazwa)
    markers["domy"].append(m)


def create_pracownik_marker(p, map_widget):
    m = map_widget.set_marker(p.coordinates[0], p.coordinates[1], text=f"{p.imie} {p.nazwisko}")
    markers["pracownicy"].append(m)


def create_pensjonariusz_marker(p, map_widget):
    m = map_widget.set_marker(p.coordinates[0], p.coordinates[1], text=f"{p.imie} {p.nazwisko}")
    markers["pensjonariusze"].append(m)


def add_dom(nazwa, lokalizacja, map_widget):
    d = DomOpieki(nazwa, lokalizacja)
    domy.append(d)
    create_dom_marker(d, map_widget)


def remove_dom(index, map_widget):
    d = domy[index]
    for p in d.pracownicy:
        pracownicy.remove(p)
    for p in d.pensjonariusze:
        pensjonariusze.remove(p)
    domy.pop(index)
    clear_all_markers(map_widget)


def update_dom(index, nazwa, lokalizacja, map_widget):
    d = domy[index]
    d.nazwa = nazwa
    d.lokalizacja = lokalizacja
    d.coordinates = get_coordinates(lokalizacja)
    clear_all_markers(map_widget)
    for x in domy:
        create_dom_marker(x, map_widget)


def add_pracownik(imie, nazwisko, wiek, rola, nazwa_domu, map_widget):
    d = next((x for x in domy if x.nazwa == nazwa_domu), None)
    if d is None:
        return False
    p = Pracownik(imie, nazwisko, wiek, rola, d)
    pracownicy.append(p)
    d.pracownicy.append(p)
    create_pracownik_marker(p, map_widget)
    return True


def remove_pracownik(index, map_widget):
    p = pracownicy[index]
    p.dom.pracownicy.remove(p)
    pracownicy.pop(index)
    clear_all_markers(map_widget)


def update_pracownik(index, imie, nazwisko, wiek, rola, nazwa_domu, map_widget):
    p = pracownicy[index]
    p.imie = imie
    p.nazwisko = nazwisko
    p.wiek = wiek
    p.rola = rola
    if p.dom.nazwa != nazwa_domu:
        p.dom.pracownicy.remove(p)
        d = next((x for x in domy if x.nazwa == nazwa_domu), None)
        if d:
            p.dom = d
            d.pracownicy.append(p)
            p.coordinates = d.coordinates
    clear_all_markers(map_widget)


def add_pensjonariusz(imie, nazwisko, wiek, choroby, nazwa_domu, map_widget):
    d = next((x for x in domy if x.nazwa == nazwa_domu), None)
    if d is None:
        return False
    p = Pensjonariusz(imie, nazwisko, wiek, choroby, d)
    pensjonariusze.append(p)
    d.pensjonariusze.append(p)
    create_pensjonariusz_marker(p, map_widget)
    return True


def remove_pensjonariusz(index, map_widget):
    p = pensjonariusze[index]
    p.dom.pensjonariusze.remove(p)
    pensjonariusze.pop(index)
    clear_all_markers(map_widget)


def update_pensjonariusz(index, imie, nazwisko, wiek, choroby, nazwa_domu, map_widget):
    p = pensjonariusze[index]
    p.imie = imie
    p.nazwisko = nazwisko
    p.wiek = wiek
    p.choroby = choroby
    if p.dom.nazwa != nazwa_domu:
        p.dom.pensjonariusze.remove(p)
        d = next((x for x in domy if x.nazwa == nazwa_domu), None)
        if d:
            p.dom = d
            d.pensjonariusze.append(p)
            p.coordinates = d.coordinates
    clear_all_markers(map_widget)


def filter_domy(q, map_widget):
    clear_all_markers(map_widget)
    w = [d for d in domy if q.lower() in d.nazwa.lower()]
    for d in w:
        create_dom_marker(d, map_widget)
    return w


def filter_pracownicy(q, map_widget):
    clear_all_markers(map_widget)
    w = [p for p in pracownicy if q.lower() in p.imie.lower()]
    for p in w:
        create_pracownik_marker(p, map_widget)
    return w


def filter_pensjonariusze(q, map_widget):
    clear_all_markers(map_widget)
    w = [p for p in pensjonariusze if q.lower() in p.imie.lower()]
    for p in w:
        create_pensjonariusz_marker(p, map_widget)
    return w


def show_all_domy(map_widget):
    clear_all_markers(map_widget)
    for d in domy:
        create_dom_marker(d, map_widget)
    return domy


def show_all_pracownicy(map_widget):
    clear_all_markers(map_widget)
    for p in pracownicy:
        create_pracownik_marker(p, map_widget)
    return pracownicy


def show_all_pensjonariusze(map_widget):
    clear_all_markers(map_widget)
    for p in pensjonariusze:
        create_pensjonariusz_marker(p, map_widget)
    return pensjonariusze


def save_model():
    with open("model.py", "w", encoding="utf-8") as f:
        f.write("domy = [\n")
        for d in domy:
            f.write(f"    {{'nazwa': '{d.nazwa}', 'lokalizacja': '{d.lokalizacja}'}},\n")
        f.write("]\n\n")

        f.write("pracownicy = [\n")
        for p in pracownicy:
            f.write(f"    {{'imie': '{p.imie}', 'nazwisko': '{p.nazwisko}', 'wiek': {p.wiek}, 'rola': '{p.rola}', 'dom': '{p.dom.nazwa}'}},\n")
        f.write("]\n\n")

        f.write("pensjonariusze = [\n")
        for p in pensjonariusze:
            f.write(f"    {{'imie': '{p.imie}', 'nazwisko': '{p.nazwisko}', 'wiek': {p.wiek}, 'choroby': '{p.choroby}', 'dom': '{p.dom.nazwa}'}},\n")
        f.write("]\n")


def load_model(map_widget=None):
    global domy, pracownicy, pensjonariusze

    namespace = {}
    exec(open("model.py", "r", encoding="utf-8").read(), namespace)

    data_domy = namespace["domy"]
    data_prac = namespace["pracownicy"]
    data_pens = namespace["pensjonariusze"]

    domy.clear()
    pracownicy.clear()
    pensjonariusze.clear()

    for d in data_domy:
        dom = DomOpieki(d["nazwa"], d["lokalizacja"])
        domy.append(dom)

    for p in data_prac:
        dom = next((x for x in domy if x.nazwa == p["dom"]), None)
        prac = Pracownik(p["imie"], p["nazwisko"], p["wiek"], p["rola"], dom)
        pracownicy.append(prac)
        dom.pracownicy.append(prac)

    for p in data_pens:
        dom = next((x for x in domy if x.nazwa == p["dom"]), None)
        pen = Pensjonariusz(p["imie"], p["nazwisko"], p["wiek"], p["choroby"], dom)
        pensjonariusze.append(pen)
        dom.pensjonariusze.append(pen)

    if map_widget:
        show_all_domy(map_widget)
