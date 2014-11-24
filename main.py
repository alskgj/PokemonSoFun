__author__ = 'zen'

from data_types.pokemon import Pokemon
from Database.get_data import download_data
from approach2.prototype import pokemondb_lookup
from approach2.pokemon2 import Pokemon2
# refresh stuff
download_data()


while 1:
    #P = Pokemon(input("> "))
    P = Pokemon2(input("> "))

    print("\n"+"#"*200)
