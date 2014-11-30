__author__ = 'zen'

from Database.build_dictionary import download_data
from core.gui import Tesla1
from tkinter import *
import os

# refresh stuff
if not "storage.sqlite":
    download_data()

# run gui forever
root = Tk()
root.iconbitmap(os.path.realpath("Database/Ultra-Ball.ico"))
root.title("Hi there!")

t = Tesla1(root)
t.pack()
root.mainloop()

