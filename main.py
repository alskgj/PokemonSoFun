__author__ = 'zen'

from data_types.pokemon import Pokemon
from Database.get_data import download_data

from termcolor import colored

# refresh stuff
# download_data()


while 1:
    P = Pokemon(input("> "))

    print("\n"+"#"*200)