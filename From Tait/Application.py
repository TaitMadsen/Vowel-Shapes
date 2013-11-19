# Application.py

import math
import time
import TBMGraphics as g
from Graph import *
import tkinter as tk
import sys

class Application(tk.Frame):
    def __init__(self, parent, width, height):
        tk.Frame.__init__(self, parent, background="white") # Call the superclass' constructor method
        self.parent = parent
        self.parent.title("Vowel Shapes")
        #self.pack(fill=tk.BOTH, expand=1) # set expand=0 if you don't want the window to be resizable
        
        # Dimensions
        self.width = width
        self.height = height
        
        # The graphWin canvas
        self.graphWin = None
        self.setupCanvas()
        
        # The menubar
        self.menubar = tk.Menu(self.parent)
        self.parent.config(menu=self.menubar)
        
        # The menus
        self.setupFileMenu()
        self.setupActionMenu()
        self.setupHelpMenu()

        # The buttons
        self.recordButton = tk.Button(self.parent, text="Record", command=self.record)
        self.recordButton.grid(column=0, row=1)
        
        self.playButton = tk.Button(self.parent, text="Play", command=self.play)
        self.playButton.grid(column=1, row=1)
    
        # Vowel objects
        self.exampleVowel = None
        self.activeVowel = None
    
    
    def setupCanvas(self):
        self.graphWin = g.GraphWin(self)
        self.graphWin.setCoords(0,0,100,75)
        self.graphWin.grid(column=0,row=0,columnspan=2)
        

    # Menus
    def setupFileMenu(self):
        fileMenu = tk.Menu(self.menubar)
        
        fileMenu.add_command(label="Save Vowel", command=self.saveVowel)
        fileMenu.add_command(label="Load Vowel", command=self.loadVowel)
        fileMenu.add_command(label="Clear Vowel", command=self.clearVowel)

        self.menubar.add_cascade(label="File", menu=fileMenu)
    
    def setupActionMenu(self):
        actionMenu = tk.Menu(self.menubar)
    
        actionMenu.add_command(label="Test Canvas", command = self.testCanvas)
    
        self.menubar.add_cascade(label="Action", menu = actionMenu)
    
    def setupHelpMenu(self):
        helpMenu = tk.Menu(self.menubar)
    
        helpMenu.add_command(label="Help", command=self.help)
    
        self.menubar.add_cascade(label="Help", menu=helpMenu)




    # menu commands
    def saveVowel(self):
        path = tk.filedialog.asksaveasfilename()
        self.activeVowel.saveToFile(path)

    def loadVowel(self):
        path = tk.filedialog.askopenfilename()
        self.exampleVowel = Vowel(0,0,0, path)
    
    def clearVowel(self):
        self.exampleVowel = None

    def help(self):
        #nothing yet
        return

    def testCanvas(self):
        box = g.Rectangle( Point(1,1), Point(99,74))
        box.draw(self.graphWin)
                          
    
    # Button commands
    def record(self):
        if self.recordButton["text"] == "Record":
            self.recordButton.config(text="Stop")
            self.playButton.config(state=tk.DISABLED)
        else:
            self.recordButton.config(text="Record")
            self.playButton.config(state=tk.NORMAL)

    def play(self):
        if self.playButton["text"] == "Play":
            self.playButton.config(text="Stop")
            self.recordButton.config(state=tk.DISABLED)
        else:
            self.playButton.config(text="Play")
            self.recordButton.config(state=tk.NORMAL)






def main():
    
    root = tk.Tk()
    width = 800
    height = 700
    # ("<width>x<height>+<xcoords>+<ycoords>")
    root.geometry("%sx%s+80+70" % (width, height) )
    app = Application(root,width, height)
    root.mainloop()

main()

