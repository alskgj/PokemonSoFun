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
    url = url.replace("é", "e")
    url = url.replace("'", "")
    url = url.replace("mime jr.", "mime-jr")
    url = url.replace("♂", "-m")
    url = url.replace("♀", "-f")
    url = url.replace("mr. mime", "mr-mime")

    print("Url: "+url)
    html = requests.get(url).content
    soup = BeautifulSoup(html)


    # getting pokedex stuff (should we parse more here?)
    pokedex_data = soup.find("h2", text="Pokédex data").parent
    types = set(pokedex_data.find("th", text="Type").parent.td.text.split())
    pokedex_number = int(pokedex_data.find("th", text="National №").parent.td.text)

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

    # getting stats
    stats = soup.find("h2", text="Base stats").parent
    stat_dict = {
        "hp": stats.find("th", text="HP").parent.td.text,
        "attack": stats.find("th", text="Attack").parent.td.text,
        "defense": stats.find("th", text="Defense").parent.td.text,
        "s_attack": stats.find("th", text="Sp. Atk").parent.td.text,
        "s_defense": stats.find("th", text="Sp. Def").parent.td.text,
        "speed": stats.find("th", text="Speed").parent.td.text,
        "total": stats.find("th", text="Total").parent.td.text
    }

    answer_dict = {
        "type": list(types),
        "no_effect": list(no_effect),
        "v_resist": list(v_resist),
        "resist": list(resist),
        "weak": list(weak),
        "v_weak": list(v_weak),
        "stats": stat_dict,
        "pokedex": pokedex_number
    }
    return answer_dict
