__author__ = 'zen'

import requests
from bs4 import BeautifulSoup

def pokemondb_lookup(pokemon):
    """

    :param pokemon:
    :return:
    :rtype: dict of [str, C]
    """

    url = "http://pokemondb.net/pokedex/"+pokemon.lower()
    print("Online Pokedex:")
    print(url)
    html = requests.get(url).content
    soup = BeautifulSoup(html)


    # getting pokedex stuff (should we parse more here?)
    pokedex_data = soup.find("h2", text="Pokédex data").parent
    types = set(pokedex_data.find("th", text="Type").parent.td.text.split())

    # getting weaknesses // resistances
    type_defenses = soup.find("h2", text="Type defenses").parent
    v_resist, resist, v_weak, weak, no_effect = set(), set(), set(), set(), set()

    for element in type_defenses.find_all("td"):
        raw_data = element["title"]  # raw data example: 'Fire → Fire/Flying = not very effective'
        pokemon_type = raw_data.split()[0]
        effectiveness = element.text

        if not effectiveness:
            pass

        elif effectiveness == "0":
            no_effect.add(pokemon_type)

        elif effectiveness == "¼":
            v_resist.add(pokemon_type)

        elif effectiveness == "½":
            resist.add(pokemon_type)

        elif effectiveness == "2":
            weak.add(pokemon_type)

        elif effectiveness == "4":
            v_weak.add(pokemon_type)

    answer_dict = {
        "type": types,
        "no_effect": no_effect,
        "v_resist": v_resist,
        "resist": resist,
        "weak": weak,
        "v_weak": v_weak
    }
    return answer_dict
