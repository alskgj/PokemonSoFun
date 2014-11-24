__author__ = 'zen'

from Database.lookup import lookup
from approach2.prototype import pokemondb_lookup
from termcolor import colored

class Pokemon2(object):

    def __init__(self, name):

        # get english data
        lookup_result = lookup(name)
        if not lookup_result:
            return
        else:
            print("Match found. Fetching data...")

        pokemondb_data = pokemondb_lookup(lookup_result["english"])

        print("\n"+"Types:")
        print(", ".join(pokemondb_data["type"])+"\n")

        if pokemondb_data["no_effect"]:
            print(colored("No Effect: ", "red", on_color="on_grey"))
            print(", ".join(pokemondb_data["no_effect"]) + "\n")

        if pokemondb_data["v_resist"]:
            print(colored("Very resistant: ", "red", on_color="on_grey"))
            print(", ".join(pokemondb_data["v_resist"]) + "\n")

        if pokemondb_data["resist"]:
            print(colored("Resistant: ", "yellow", on_color="on_grey"))
            print(", ".join(pokemondb_data["resist"])+"\n")

        if pokemondb_data["weak"]:
            print(colored("Weak: ", "cyan", on_color="on_grey"))
            print(", ".join(pokemondb_data["weak"]) + "\n")

        if pokemondb_data["v_weak"]:
            print(colored("Very weak: ", "magenta", on_color="on_grey"))
            print(", ".join(pokemondb_data["v_weak"]) + "\n")

