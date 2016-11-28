import requests
import sqlite3
from os import path

from bs4 import BeautifulSoup
from definitions import ROOT_DIR


def download_data(silent=True):
    # connect to source
    source = "http://bulbapedia.bulbagarden.net/wiki/List_of_German_Pok%C3%A9mon_names"
    html = requests.get(source).content
    print("Fetching [{source}]".format(**locals()))

    # connect to db
    con = sqlite3.connect(path.join(ROOT_DIR, "Database", "storage.sqlite"))
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS pokemons (pokedex integer primary key, english text, german text)")

    # parse source
    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("table", class_="roundy")
    for table in tables:
        rows = table.find_all("tr", style="background:#fff;")
        for row in rows:
            if "Egg" in row.text:
                print("break")
                break
            print(row)
            row = [r.strip() for r in row.text.split("\n") if r.strip()]
            pokedex_id, english_name, german_name = row

            if not silent:
                print(pokedex_id, english_name, german_name)
            cur.execute("INSERT OR REPLACE INTO pokemons VALUES (?, ?, ?)",
                        (int(pokedex_id), english_name, german_name))

    con.commit()
    con.close()

    print("\nSetup successful.")

if __name__ == "__main__":
    download_data(silent=False)
