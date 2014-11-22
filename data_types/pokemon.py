import sys

__author__ = 'zen'

from Database.lookup import lookup
from Database.get_data import download_data

from json import loads
from termcolor import colored

import requests
from data_types.pokemon_type import PokemonType

class Pokemon(object):
    API_GET_POKEMON = "http://pokeapi.co/api/v1/pokemon/"
    API_BASE = "http://pokeapi.co"

    def __init__(self, name):

        # get data
        lookup_result = lookup(name)
        if not lookup_result:
            return
        else:
            print("Match found. Fetching data...")

        raw = requests.get(Pokemon.API_GET_POKEMON + str(lookup_result["pokedex"])).content
        self.data = loads(raw.decode("utf-8"))

        # verify data
        assert (lookup_result["english"] in self.data["name"]), "Fatal error"

        self.pokedex = lookup_result["pokedex"]
        self.name = self.data["name"]
        self.german_name = lookup_result["german"]

        self.poke_types = self.get_types()

        self.pretty_print()


    def get_types(self):
        """
        :rtype: list[PokemonType]
        """
        pokemon_types = []
        for element in self.data["types"]:
            api_call = element["resource_uri"]
            data = loads(requests.get(self.API_BASE+api_call).content.decode("UTF-8"))
            pokemon_types.append(PokemonType(data))
        return pokemon_types


    def pretty_print(self):
        """
        Outputs info.
        """

        print("[{self.pokedex:0>3}]: {self.name}/{self.german_name}\n".format(**locals()))

        print(colored("Type analysis:", "blue"))
        # for each type
        for i, pt in enumerate(self.poke_types):
            output = "[{index}]: {name}".format(index=i+1, name=pt.name)
            print(colored(output, "magenta"))

            # print weakness
            print("\tWeaknesses:")
            print("\t"+", ".join(pt.weaknesses))

            # print resistances
            # print weakness
            # print("\tResistances:")
            # print("\t" + ", ".join(pt.resistance))
            # print(pt.resistance)

        print(colored("\nStats analysis:", "blue"))

        color = "red" if self.data["hp"] > 105 else "cyan" if self.data["hp"] < 80 else "grey"
        print(colored("\tHP:     [{HP:0>3}]".format(HP=self.data["hp"]), color))

        color = "red" if self.data["attack"] > 105 else "cyan" if self.data["attack"] < 80 else "grey"
        print(colored("\tAtk:    [{ATK:0>3}]".format(ATK=self.data["attack"]), color))

        color = "red" if self.data["defense"] > 105 else "cyan" if self.data["defense"] < 80 else "grey"
        print(colored("\tDef:    [{DEF:0>3}]".format(DEF=self.data["defense"]), color))

        color = "red" if self.data["sp_atk"] > 105 else "cyan" if self.data["sp_atk"] < 80 else "grey"
        print(colored("\tSp. A.: [{SPA:0>3}]".format(SPA=self.data["sp_atk"]), color))

        color = "red" if self.data["sp_def"] > 105 else "cyan" if self.data["sp_def"] < 80 else "grey"
        print(colored("\tSp. D.: [{SPD:0>3}]".format(SPD=self.data["sp_def"]), color))

        color = "red" if self.data["speed"] > 105 else "cyan" if self.data["speed"] < 80 else "grey"
        print(colored("\tInit:   [{INIT:0>3}]".format(INIT=self.data["speed"]), color))











