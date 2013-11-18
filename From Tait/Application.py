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
        self.pack(fill=tk.BOTH, expand=1) # set expand=0 if you don't want the window to be resizable
        
        # Dimensions
        self.width = width
        self.height = height
        
        # The menubar
        self.menubar = tk.Menu(self.parent)
        self.parent.config(menu=self.menubar)
        
        # The graphWin canvas
        self.graphWin = None
        self.setupCanvas()
        
        self.setupFileMenu()
        self.setupActionMenu()
        self.setupHelpMenu()
    
    
    def setupCanvas(self):
        self.graphWin = g.GraphWin(self)
        self.graphWin.setCoords(0,0,100,75)
        self.graphWin.pack(fill=tk.BOTH, expand=1)

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

    def loadVowel(self):
        path = tk.filedialog.askopenfilename()
    
    def clearVowel(self):
        #nothing yet
        return

    def help(self):
        #nothing yet
        return


    def testCanvas(self):
        box = g.Rectangle( Point(1,1), Point(99,74))
        box.draw(self.graphWin)






def main():
    
    root = tk.Tk()
    width = 800
    height = 600
    # ("<width>x<height>+<xcoords>+<ycoords>")
    root.geometry("%sx%s+150+100" % (width, height) )
    app = Application(root,width, height)
    root.mainloop()

main()

