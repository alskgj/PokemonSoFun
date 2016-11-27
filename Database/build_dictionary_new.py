import requests
import sqlite3


from bs4 import BeautifulSoup
from definitions import DATABASE_DIR


def download_translation(silent=True):
    # connect to source
    source = "http://bulbapedia.bulbagarden.net/wiki/List_of_German_Pok%C3%A9mon_names"
    html = requests.get(source).content

    # connect to db
    con = sqlite3.connect(DATABASE_DIR)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS localization (pokedex integer primary key, english text, german text)")

    # parse source
    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("table", class_="roundy")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows[1:]:
            if "Egg" in row.text:
                break
            row = [r.strip() for r in row.text.split("\n") if r.strip()]

            pokedex_id, english_name, german_name = row

            cur.execute("INSERT OR REPLACE INTO localization VALUES (?, ?, ?)",
                        (int(pokedex_id), english_name, german_name))

    con.commit()
    con.close()


if __name__ == "__main__":
    download_translation(silent=False)
