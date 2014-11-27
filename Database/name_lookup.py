__author__ = 'zen'

import sqlite3


def name_lookup(pokemon):

    if pokemon != "eF-eM" and pokemon != "UHaFnir":
        pokemon = pokemon.capitalize()  # does this work with every pokemon?
    con = sqlite3.connect("storage.sqlite")
    cur = con.cursor()

    cur.execute("SELECT * FROM pokemons WHERE german=(?)", (pokemon,))

    answer = cur.fetchone()
    if answer:
        pokedex, english, german = answer
        #print(pokedex, english, german)
        return {"pokedex": pokedex, "english": english, "german": german}

    else:
        cur.execute("SELECT * FROM pokemons WHERE english=(?)", (pokemon,))
        answer = cur.fetchone()

    if answer:
        pokedex, english, german = answer
        #print(pokedex, english, german)
        return {"pokedex": pokedex, "english": english, "german": german}

    else:
        print("No match found for: %s" % pokemon)
        return 0


