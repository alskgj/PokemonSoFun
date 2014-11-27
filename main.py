__author__ = 'zen'

from Database.build_dictionary import download_data
# from core.pokemon import Pokemon
# import cmd
from gui import Tesla1

# refresh stuff
download_data()



# class PokemonShell(cmd.Cmd):
#     intro = "Welcome! Type help or ? to list commands.\n"
#     prompt = '> '
#
#     def default(self, line):
#         self.do_pokemon(line)
#
#     # commands
#     @staticmethod
#     def do_pokemon(arg):
#         """Search for a pokemon.
#         syntax: pokemon [pokemonname]"""
#         Pokemon(arg)
#
#     def do_p(self, arg):
#         """Search for a pokemon.
#         syntax: pokemon [pokemonname]"""
#         self.do_pokemon(arg)
#
#
#     def do_type(self, arg):
#         """Search for a type.
#         syntax: type [typename]"""
#         pass
#
#
# if __name__ == '__main__':
#     PokemonShell().cmdloop()

Tesla1().mainloop()