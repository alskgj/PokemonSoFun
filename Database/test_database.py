import unittest
import os
import sqlite3
from json import loads

from Database.build_dictionary_new import download_translation
from Database.download_pokemon_info import download_info
from definitions import DATABASE_DIR


class DataBaseTestCase(unittest.TestCase):

    def setUp(self):
        if os.path.exists(DATABASE_DIR):
            os.remove(DATABASE_DIR)
        self.con = sqlite3.connect(DATABASE_DIR)
        self.cur = self.con.cursor()

    def test_translator(self):
        download_translation()

        self.cur.execute("SELECT * FROM localization WHERE pokedex=?", (20,))
        pokedex, english, german = self.cur.fetchone()
        self.assertEqual(pokedex, 20)
        self.assertEqual(english, "Raticate")
        self.assertEqual(german, "Rattikarl")

    def test_pokemon_info(self):
        self.assertTrue(download_info("Dragonite"))
        row = self.cur.execute("SELECT pokedex, name, types FROM pokedex WHERE name=?", ("dragonite",))
        pokedex, name, types = row.fetchone()
        types = loads(types)
        self.assertEqual(pokedex, 149)
        self.assertEqual(name, "dragonite")
        self.assertListEqual(types, ["Dragon", "Flying"])

    def tearDown(self):
        self.cur.close()
        self.con.close()
