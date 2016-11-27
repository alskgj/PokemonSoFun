from Database.build_dictionary import download_data
from core.gui import Tesla1
from tkinter import *
import os

from definitions import DATABASE_DIR

# refresh stuff
if not os.path.exists(os.path.join(DATABASE_DIR)):
    download_data()

# run gui forever
root = Tk()
root.iconbitmap(os.path.realpath("Database/Ultra-Ball.ico"))
root.title("Hi there!")

t = Tesla1(root)
t.pack()
root.mainloop()

