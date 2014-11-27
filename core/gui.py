__author__ = 'zen'

from bs4 import BeautifulSoup
from tkinter import *
from Database.name_lookup import name_lookup
import os.path
import requests
import sqlite3
from json import loads
from Database.download_pokemon_info import Downloader



class Tesla1(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)


        # entry
        self.ent = Entry(self, width=50, relief=SUNKEN, font=('Courier New', 14, ))
        self.ent.insert(0, 'Enter Pokemon here [press enter to clear this]')
        self.ent.bind('<Return>', (lambda event: self.fetch()))

        # label - sprite
        png = PhotoImage(file="sprites/dragonite.png")
        self.sprite = Label(self, image=png, bg="LightYellow2")
        self.sprite.image = png  # prevent garbage collection?

        # label - stats
        self.stats = Text(self, relief=RIDGE, height=12, width=20, bg="darkgray")
        self.stats.config(font=('consolas', 14))
        self.stats.insert('1.0', "\nstats will be here\n")

        # label - name
        self.name_label = Text(self, height=1, relief=SUNKEN, width=10, bg="wheat2")
        self.name_label.config(font=('consolas', 20, 'bold'))
        self.name_label.insert('1.0', "No pokemon selected")

        # label - type defenses
        self.type_defenses = Text(self, relief=RIDGE, height=12, width=70, bg="darkgray")
        self.type_defenses.config(font=('consolas', 14))
        self.type_defenses.insert('1.0', open("Database/defaulttextstats.txt").read())

        # second pokemon
        self.create_second_pokemon_widgets()

        # first pokemon
        self.ent.pack(side=TOP, fill=X, expand=NO)
        self.ent.focus()
        self.name_label.pack(side=TOP, fill=X, expand=NO)
        self.sprite.pack(side=RIGHT, fill=BOTH, expand=YES)
        self.stats.pack(side=LEFT, expand=YES, fill=BOTH)
        self.type_defenses.pack(side=RIGHT, expand=YES, fill=BOTH)

        # second pokemon
        self.name_label2.pack(side=TOP, fill=X, expand=NO)
        self.sprite2.pack(side=RIGHT, fill=BOTH, expand=YES)
        self.stats2.pack(side=LEFT, expand=YES, fill=BOTH)
        self.type_defenses2.pack(side=RIGHT, expand=YES, fill=BOTH)

        self.state = {
            "pokemon": None
        }


    def create_second_pokemon_widgets(self):
        # copy name, stats, type defenses and sprite to widget below
        frame2 = Frame(self)
        frame2.pack(side=BOTTOM, expand=YES, fill=BOTH)
        self.name_label2 = Text(frame2, height=1, relief=SUNKEN, font=('consolas', 20, 'bold'), bg="wheat3")
        self.name_label2.insert('1.0', "old pokemon")

        self.stats2 = Text(frame2, relief=RIDGE, height=12, width=20, bg="darkgray")
        self.stats2.config(font=('consolas', 14))
        self.stats2.insert('1.0', "\nstats will be here\n")

        self.type_defenses2 = Text(frame2, relief=RIDGE, height=12, width=70, bg="darkgray")
        self.type_defenses2.config(font=('consolas', 14))
        self.type_defenses2.insert('1.0', open("Database/defaulttextstats.txt").read())

        png2 = PhotoImage(file="sprites/dragonite.png")
        self.sprite2 = Label(frame2, image=png2, bg="LightYellow3")
        self.sprite2.image = png2  # prevent garbage collection?

    def fetch(self):
        input_value = self.ent.get()
        print("Input => '%s'" % input_value)
        self.ent.delete(0, END)

        lookup_result = name_lookup(input_value)
        if not lookup_result:
            print("invalid")
            self.invalid_pokemon(input_value)
            return 0

        pkm = lookup_result["english"]

        # update bottom pokemon
        if self.state["pokemon"]:
            self.update_bottom()

        print("valid")
        # new pokemon selected
        self.update_pokemon_name(pkm)
        # sprite updating
        self.redraw(pkm, "sprite")
        # base stats updating
        self.insert_stats(pkm, "stats")
        # base defenses updating
        self.update_defenses(pkm, "type_defenses")

        self.state["pokemon"] = pkm
        self.ent.focus()


    def update_bottom(self):
        # pokemon name
        text = self.name_label.get("1.0", END)
        if not "is not a valid pokemon" in text:
            self.name_label2.delete('1.0', END)
            self.name_label2.insert('1.0', text)

        pkm = self.state["pokemon"]
        # stats
        self.insert_stats(pkm, "stats2")
        # type_Defenses
        self.update_defenses(pkm, "type_defenses2")
        # sprite
        self.redraw(pkm, "sprite2")

    def invalid_pokemon(self, pokemon):
        if pokemon == "Enter Pokemon here [press enter to clear this]":
            return
        if len(pokemon) > 15:
            pokemon = pokemon[:15]+"..."
        self.name_label.config(state=NORMAL)
        self.name_label.delete('1.0', END)
        self.name_label.insert('1.0', "'" + pokemon + "' is not a valid pokemon")
        self.name_label.config(state=DISABLED)

    def update_pokemon_name(self, pokemon):
        # make sure db is updated and ready
        pokemon = pokemon.lower()
        Downloader(pokemon)

        con = sqlite3.connect("pokedex.sqlite")
        cur = con.cursor()
        cur.execute("SELECT * FROM pokedex WHERE name=(?)", (pokemon,))

        pokedex, name, hp, attack, defense, s_attack, s_defense, speed, type_, no_effect, v_resist, \
        resist, weak, v_weak = cur.fetchone()

        self.name_label.config(state=NORMAL)
        self.name_label.delete('1.0', END)
        self.name_label.insert('1.0', "["+str(pokedex)+"] "+pokemon.capitalize() + ":"+" "*10+", ".join(loads(type_)))
        self.name_label.config(state=DISABLED)

    def redraw(self, pokemon, label):
        path = "sprites/" + pokemon.lower() + ".png"
        print(path)
        if os.path.exists(path):
            try:
                png = PhotoImage(file=path)
            except Exception as e:
                print(e)
                print("img corrupted. deleting it.")
                os.path.os.remove(path)
                return

            sprite = getattr(self, label)
            sprite.configure(image=png)
            sprite.image=png
        else:
            self.download_sprite(pokemon)
            self.redraw(pokemon, label)

    def download_sprite(self, pokemon):
        """
        Saves a sprite of a pokemon to sprites/{pokename}.png
        """
        pokemon = pokemon.lower()
        url = "http://pokemondb.net/sprites/"+pokemon
        html = requests.get(url).content
        soup = BeautifulSoup(html)
        image_url = soup.img["data-original"]

        url = image_url
        path = "sprites/"+pokemon+".png"
        image = requests.get(url)
        if image.status_code != 200:
            print(url)

        open(path, "wb").write(image.content)
        print("Saved sprite to "+path)

    def insert_stats(self, pokemon, label):
        # make sure db is updated and ready
        pokemon = pokemon.lower()
        Downloader(pokemon)

        con = sqlite3.connect("pokedex.sqlite")
        cur = con.cursor()
        cur.execute("SELECT * FROM pokedex WHERE name=(?)", (pokemon,))

        pokedex, name, hp, attack, defense, s_attack, s_defense, speed, type_, no_effect, v_resist, \
        resist, weak, v_weak = cur.fetchone()

        total = attack + hp + defense + s_attack + s_defense + speed

        # yep, the hacking is real
        stats = getattr(self, label)
        stats.config(state=NORMAL)
        stats.delete("1.0", END)

        # let's build our text
        text = list()
        text.append("")
        text.append("HP:          "+str(hp))
        text.append("Attack:      "+str(attack))
        text.append("Defense:     "+str(defense))
        text.append("Sp. Attack:  "+str(s_attack))
        text.append("Sp. Defense: "+str(s_defense))
        text.append("Speed:       "+str(speed))
        text.append("")
        text.append("Total:        "+str(total))

        text = "\n".join(text)
        stats.insert("1.0", text)

        # let's color some stuff
        stats.tag_add("hp", '2.0', '2.30')
        stats.tag_add("attack", '3.0', '3.30')
        stats.tag_add("defense", '4.0', '4.30')
        stats.tag_add("s_attack", '5.0', '5.30')
        stats.tag_add("s_defense", '6.0', '6.30')
        stats.tag_add("speed", '7.0', '7.30')
        stats.tag_add("total", '9.0', '9.30')


        stats.tag_config('hp', foreground=self.colorrating(hp))
        stats.tag_config('attack', foreground=self.colorrating(attack))
        stats.tag_config('defense', foreground=self.colorrating(defense))
        stats.tag_config('s_attack', foreground=self.colorrating(s_attack))
        stats.tag_config('s_defense', foreground=self.colorrating(s_defense))
        stats.tag_config('speed', foreground=self.colorrating(speed))
        stats.tag_config('total', foreground=self.colorrating(total/5))

        stats.config(state=DISABLED)

    @staticmethod
    def colorrating(value):
        value = int(value)
        if value < 65:
            return "red"
        elif value < 85:
            return "orange"
        elif value < 105:
            return "green"
        elif value < 140:
            return "cyan"
        else:
            return "magenta"

    def update_defenses(self, pokemon, label):
        # make sure db is updated and ready
        pokemon = pokemon.lower()
        Downloader(pokemon)

        con = sqlite3.connect("pokedex.sqlite")
        cur = con.cursor()
        cur.execute("SELECT * FROM pokedex WHERE name=(?)", (pokemon,))

        pokedex, name, hp, attack, defense, s_attack, s_defense, speed, type_, no_effect, v_resist, \
        resist, weak, v_weak = cur.fetchone()

        no_effect, v_resist, resist, weak, v_weak = map(loads, [no_effect, v_resist, resist, weak, v_weak])

        type_defenses = getattr(self, label)
        type_defenses.config(state=NORMAL)
        type_defenses.delete("1.0", END)

        # let's build our text
        text = list()
        text.append("")
        text.append("No Effect:      " + ", ".join(no_effect))
        text.append("Very resistant: " + ", ".join(v_resist))
        text.append("Resistant:      " + ", ".join(resist))
        text.append("Weak:           " + ", ".join(weak))
        text.append("Very weak:      " + ", ".join(v_weak))

        text = "\n".join(text)
        type_defenses.insert("1.0", text)
        type_defenses.config(state=DISABLED)

if __name__ == "__main__":

    t = Tesla1().mainloop()