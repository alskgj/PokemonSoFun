__author__ = 'zen'

import sqlite3

def name_lookup(pokemon):
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
        print("No match found for: %s" % pokemon)
        return 0


