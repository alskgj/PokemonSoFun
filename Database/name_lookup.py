__author__ = 'zen'

import sqlite3
from binascii import hexlify

def name_lookup(pokemon):
    pokemon = pokemon.strip()
    con = sqlite3.connect("storage.sqlite")
    cur = con.cursor()

    # try without changing pokemon name
    cur.execute("SELECT * FROM pokemons WHERE german=(?) OR english=(?)", (pokemon, pokemon))
    answer = cur.fetchone()
    if answer:
        pokedex, english, german = answer
        return {"pokedex": pokedex, "english": english, "german": german}

    # try with pokemon.capitalize()
    else:
        pokemon = pokemon.capitalize()
        cur.execute("SELECT * FROM pokemons WHERE german=(?) OR english=(?)", (pokemon, pokemon))
        answer = cur.fetchone()

    if answer:
        pokedex, english, german = answer
        return {"pokedex": pokedex, "english": english, "german": german}

    else:
        print("[DEBUG1]: lookup for ["+pokemon+"] failed")
        print("[DEBUG2]: "+str(hexlify(pokemon.encode("UTF-8"))))
        print("No match found for: %s" % pokemon)
        return 0


