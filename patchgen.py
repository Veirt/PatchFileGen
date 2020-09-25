import ctypes
import os
import hashlib
import shutil
from tkinter import *
from tkinter import filedialog
import tkinter as tk

if __name__ == "__main__":
    if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        root = Tk()
        root.title("Patch Generator Tool")

    #getting input
    def validation(*args):
        y = stringvar1.get()
        if y:
            but.config(state='normal')
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
        file.write("C DragonNest.exe")
        file.close()
    #showing what was the input
        lab = Label(root, text="The text you input is {}".format(inp.get()))
        lab.pack()
        
    #making md5
        file = open("00000{}/Patch00000{}.pak.md5".format(inp.get(), inp.get()), "w") 
        file.write("{}\n".format(hashlib.md5(open(root.filename,'rb').read()).hexdigest()))
        file.close()
        
    #copy file
        shutil.copy2(root.filename, "00000{}/Patch00000{}.pak".format(inp.get(), inp.get()))

root.filename = filedialog.askopenfilename(initialdir=".", title="Select PAK File", filetypes=(("PAK Files", "*.PAK"),))
but = Button(root, text="Click to Patch", command=makepatch, state='disabled')
but.pack()

root.mainloop()