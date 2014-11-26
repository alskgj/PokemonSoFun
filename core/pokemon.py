__author__ = 'zen'

from Database.lookup import lookup
from core.pokemon_db import pokemondb_lookup
from termcolor import colored


class Pokemon(object):

    def __init__(self, name):

        # get english data
        lookup_result = lookup(name)
        if not lookup_result:
            return

        pokemondb_data = pokemondb_lookup(lookup_result["english"])

        ################################### Type #########################################################
        print("\n"+colored("Types:", attrs={"bold"}))
        print(", ".join(pokemondb_data["type"])+"\n")

        ################################### Type Defenses ################################################
        # colorstrings take 14 chars
        print(colored("Type defenses:", attrs={"bold"}))
        print("%-64s%-64s%-64s" % (colored("No Effect:", "red", on_color="on_grey"),
                                   colored("Very resistant: ", "red", on_color="on_grey"),
                                   colored("Resistant: ", "yellow", on_color="on_grey")))
        print("%-50s%-50s%-50s" % (", ".join(pokemondb_data["no_effect"]),
                                   ", ".join(pokemondb_data["v_resist"]),
                                   ", ".join(pokemondb_data["resist"])))
        #print()
        print("%-64s%-64s" % (colored("Weak:", "cyan", on_color="on_grey"),
                              colored("Very weak: ", "magenta", on_color="on_grey")))

        print("%-50s%-50s" % (", ".join(pokemondb_data["weak"]),
                              ", ".join(pokemondb_data["v_weak"])))

        ################################### Base stats ###################################################

        print("\n" + colored("Base stats:", attrs={"bold"}))
        stats = pokemondb_data["stats"]
        print(colored("HP:      "+stats["hp"].ljust(7), self.colorrating(stats["hp"]), on_color="on_grey"))
        print(colored("Attack:  "+stats["attack"].ljust(7), self.colorrating(stats["attack"]), on_color="on_grey"))
        print(colored("Defense: "+stats["defense"].ljust(7), self.colorrating(stats["defense"]), on_color="on_grey"))
        print(colored("Sp. Atk: "+stats["s_attack"].ljust(7), self.colorrating(stats["s_attack"]), on_color="on_grey"))
        print(colored("Sp. Def: "+stats["s_defense"].ljust(7), self.colorrating(stats["s_defense"]), on_color="on_grey"))
        print(colored("Speed:   "+stats["speed"].ljust(7), self.colorrating(stats["speed"]), on_color="on_grey"))

        stats["total"] = int(stats["total"])
        if stats["total"] < 450:
            color = "red"
        elif stats["total"] < 500:
            color = "yellow"
        elif stats["total"] < 550:
            color = "green"
        elif stats["total"] < 610:
            color = "cyan"
        else:
            color = "magenta"
        print(colored("Total:   " + str(stats["total"]).ljust(7), color, on_color="on_grey"))
        print()
        print("~ Magenta > Cyan > Green > Yellow > Red")



    def colorrating(self, value):
        value = int(value)
        if value < 65:
            return "red"
        elif value < 85:
            return "yellow"
        elif value < 105:
            return "green"
        elif value < 140:
            return "cyan"
        else:
            return "magenta"
