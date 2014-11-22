__author__ = 'zen'


class PokemonType(object):

    def __init__(self, data):

        self.data = data
        self.name = data["name"]

        self.ineffective = [element["name"] for element in data["ineffective"]]
        self.no_effect = [element["name"] for element in data["no_effect"]]
        self.resistance = sorted([element["name"] for element in data["resistance"]])
        self.super_effective = [element["name"] for element in data["super_effective"]]
        self.weaknesses = sorted([element["name"] for element in data["weakness"]])


