__author__ = 'zen'

import sqlite3
from json import dumps
from core.pokemon_db import pokemondb_lookup

class Downloader(object):
    """
    Downloads pokemon if it isn't already saved in storage.sqlite
    """

    def __init__(self, pokemon):

        pokemon = pokemon.lower()

        con = sqlite3.connect("pokedex.sqlite")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS pokedex (pokedex integer primary key, name text,"
                    "hp integer, attack integer, defense integer, s_attack integer, s_defense integer, speed integer,"
                    "types text, no_effect text, v_resistant text, resistant text, weak text, v_weak text)")

        print(pokemon)
        db_lookup = cur.execute("SELECT * FROM pokedex WHERE name=(?)", (pokemon,))

        if db_lookup.fetchone():
            print("pokemon already saved")
            return


        # example dragonite lookup
        #
        # answer_dict = {'pokedex': 149, 'no_effect': {'Ground'},
        #  'stats': {'total': '600', 'attack': '134', 'defense': '95', 'speed': '80', 'hp': '91', 's_attack': '100',
        #            's_defense': '100'}, 'v_weak': {'Ice'}, 'weak': {'Rock', 'Fairy', 'Dragon'},
        #  'type': {'Dragon', 'Flying'}, 'resist': {'Water', 'Fire', 'Fighting', 'Bug'}, 'v_resist': {'Grass'}}

        print("looking up "+pokemon)
        ans = pokemondb_lookup(pokemon)


        cur.execute("INSERT OR REPLACE INTO pokedex VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (ans["pokedex"], pokemon, ans["stats"]["hp"], ans["stats"]["attack"], ans["stats"]["defense"],
             ans["stats"]["s_attack"], ans["stats"]["s_defense"], ans["stats"]["speed"], dumps(ans["type"]),
             dumps(ans["no_effect"]), dumps(ans["v_resist"]), dumps(ans["resist"]), dumps(ans["weak"]),
             dumps(ans["v_weak"])))


        con.commit()
        cur.close()
        con.close()
        print("Saved "+pokemon)


if __name__ == "__main__":
    Downloader("dragonite")