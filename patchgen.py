from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from TkinterDnD2 import *
import tkinter as tk
import ctypes
import os
import hashlib
import shutil

if __name__ == "__main__":
    if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        root = TkinterDnD.Tk()
        root.geometry('{}x{}'.format(300, 100))
        root.resizable(width=False, height=False)
        root.title("Patch Generator Tool")

    # getting input
    def validation(*args):
        y = stringvar1.get()
        if y:
            but.config(state='normal')
        else:
            but.config(state='disabled')

    def drop(event):
        global file_Name
        file_Name = event.data

    def makepatch():
        # make directory/folder
        path = "00000{}".format(inp.get())
        try:
            os.mkdir(path)
        # except if error
        except OSError:
            pass

        # modify patchinfoserver.cfg
        file = open("PatchInfoServer.cfg", "w")
        file.write("Version {}".format(inp.get()))

        # making txt file

        file = open("00000{}/Patch00000{}.txt".format(inp.get(), inp.get()), "w")
        file.write("C DragonNest.exe")
        file.close()

        # making md5

        file = open("00000{}/Patch00000{}.pak.md5".format(inp.get(), inp.get()), "w")
        file.write("{}\n".format(hashlib.md5(open(file_Name, 'rb').read()).hexdigest()))
        file.close()

        # copy file
        try:
            shutil.copy2(file_Name, "00000{}/Patch00000{}.pak".format(inp.get(), inp.get()))
        except shutil.SameFileError:
            pass

        root.destroy()

    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', drop)
    stringvar1 = tk.StringVar(root)
    stringvar1.trace("w", validation)
    inp = Entry(root, width=30, textvariable=stringvar1)
    inp.pack()
    inp.place(relx=0.5, rely=0.5, anchor=CENTER)

but = Button(root, text="Click to Patch", command=makepatch, state='disabled')
but.place(relx=0.5, rely=0.8, anchor=CENTER)

root.mainloop()
