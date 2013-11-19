# Application.py

import math
import time
import TBMGraphics as g
from Graph import *
import tkinter as tk
import tkSnack as tkSnack
import GraphicsModule as gModule
import sys

class Application(tk.Frame):
    def __init__(self, parent, sound, width, height):
        tk.Frame.__init__(self, parent, background="white") # Call the superclass' constructor method
        self.parent = parent
        self.parent.title("Vowel Shapes")
        #self.pack(fill=tk.BOTH, expand=1) # set expand=0 if you don't want the window to be resizable
        # CJR make the sound object of tkSnack part of the Application class
        self.snd = sound
        #initialize the defaults for the sound
        self.sound_length = 1024
        self.sound_pos = 0
        self.id = None
        # read the configuration file
        self.defaultSetup = self.readConfiguration("./vowelShapeConfig.txt")
        #initialize the graphics module
        self.graphModule = GraphicsModule(parent, defaultSetup.useViz, defaultSetup.defVowel, defaultSetup.defFormants)
        if self.graphModule.originViz :
            self.graphModule.axesDraw()
        if (defaultSetup.mode == "Practice") :
            self.graphModule.drawMatchingViz(defaultSetup.defFormants)

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

        # from the tkSnack demo files
        #Button(f, bitmap='snackRecord', fg='red', command=start).pack(side='left')
        #Button(f, bitmap='snackStop', command=stop).pack(side='left')
        #Button(f, text='Exit', command=root.quit).pack(side='left')

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
            # CJR add in the tkSnack commands to start the recording
            self.snd.record()
            self.id = self.parent.after(100,self.draw())
        else:
            self.recordButton.config(text="Record")
            self.playButton.config(state=tk.NORMAL)
            # CJR add in the tkSnack commands to stop the recording
            self.snd.stop()
            self.parent.after_cancel(self.id)

    def play(self):
        if self.playButton["text"] == "Play":
            self.playButton.config(text="Stop")
            self.recordButton.config(state=tk.DISABLED)
        else:
            self.playButton.config(text="Play")
            self.recordButton.config(state=tk.NORMAL)


    # CJR setup and drawing methods
    def draw(self):
        global graphModule
        if (self.snd.length() > self.sound_length) :
            self.sound_pos = self.snd.length() - self.sound_length
            formants = self.snd.formant(start=self.sound_pos,numformants=4)
            print(formants[0][0], formants[0][1], formants[0][2], formants[0][3] )

            #audioData = [ [ formants[0][2], formants[0][3], formants[0][4] ] ]
            audioData = [ [ formants[0][1], formants[0][2], formants[0][3] ] ]
            #audioData = [ [ formants[0][0], formants[0][1], formants[0][2] ] ]
        else:
        # [f1, f2, f3]
            audioData = [
                         [274.2, 2022.0, 3012.4], #i
                         [268.8, 2353.4, 3420.8], #I
                         [492.7, 2088.3, 2656.1], #E
                         [753.9, 1619.9, 2494.4], #ae
                         [707.6, 1027.2, 2695.7], #\as
                         [405.6, 696.7, 2779.6], #o
                         [360.2, 858.6,  2654.7] #u
                         ]

        if graphModule.useViz == "Graph" :
            graphModule.drawWithGraph(audioData)
        elif graphModule.useViz == "Oval" :
            graphModule.drawWithOval(audioData)
        elif graphModule.useViz == "Triangle" :
            graphModule.drawWithTriangle(audioData)

        if (snd.length(unit='sec') > 20) :
            print("calling stop")
            # CJR calling record as if it was clicked will stop the recording
            # as the predetermined time.
            self.record()
        # CJR let's see if pausing for a second helps the jitter display
        time.sleep(1)
        self.id = self.parent.after(100,self.draw())

    def readConfiguration(filename):
        configVars = VowelShapeConfig(filename)
        print(configVars.viz, configVars.mode)
        print(configVars.defFormants, configVars.defVowel)
        return configVars

def main():
    
    root = tk.Tk()
    tkSnack.initializeSnack(root)
    snd = tkSnack.Sound()
    width = 800
    height = 700
    # ("<width>x<height>+<xcoords>+<ycoords>")
    root.geometry("%sx%s+80+70" % (width, height) )
    app = Application(root, snd, width, height)
    root.mainloop()

main()

