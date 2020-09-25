import ctypes
import os
from tkinter import *
import tkinter as tk

if __name__ == "__main__":
    if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        root = Tk()
        root.title("Patch Generator Tool by ExLog")

    #getting input
    def validation(*args):
        y = stringvar1.get()
        if y:
            but.config(state='normal')
        elif y == "":
            but.config(state='disabled')
        else:
            but.config(state='disabled')

    stringvar1 = tk.StringVar(root)
    stringvar1.trace("w", validation)
    inp = Entry(root, width=50, textvariable=stringvar1)
    inp.pack()

    def makepatch():
    #make directory/folder
        path = "00000{}".format(inp.get())
        try:
            os.mkdir(path)
    #except if error
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)
    #making txt file
        file = open("00000{}/Patch00000{}.txt".format(inp.get(),inp.get()), "w") 
        file.write(inp.get())
        file.close()
    #showing what was the input
        lab = Label(root, text="The text you input is {}".format(inp.get()))
        lab.pack()
        print("Succesfully created text file!")
    #making md5
        file = open("00000{}/Patch00000{}.pak.md5".format(inp.get(), inp.get()), "w") 
        file.write("MD5 HERE")
        file.close()
        print("Succesfully created md5 file!")

but = Button(root, text="Click to make text file.", command=makepatch)
but.pack()
root.mainloop()