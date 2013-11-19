# Application.py

import math
import time
import TBMGraphics as g
from Graph import *
import tkinter as tk
from tkinter import filedialog  # CJR Windows needed this import
#import tkSnack as tkSnack
from GraphicsModule import *
from VowelShapeConfig import *
import sys

useTkSnack = False
id = None

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

        # CJR
        # options for the file dialogs
        self.save_file_opt = options = {}
        options['filetypes'] = [('all files', '.*'), ('audio files', '.mp3')]
        options['initialfile'] = 'myfile_i.mp3'
        options['parent'] = self.parent

        # read the application configuration file
        self.defaultSetup = self.readConfiguration("./vowelShapeConfig.txt")
        #initialize the graphics module
        self.graphModule = GraphicsModule(self.graphWin, self.defaultSetup.viz,
                                        self.defaultSetup.defVowel, self.defaultSetup.defFormants)
        if self.graphModule.originViz :
            self.graphModule.axesDraw()
        if (self.defaultSetup.mode == "Practice") :
            self.graphModule.drawMatchingViz(self.defaultSetup.defFormants)

    
    
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
        fileMenu.add_command(label="Exit", command=self.exitApp)  # CJR added an exit function

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
        #path = tk.filedialog.asksaveasfilename()
        # CJR Windows needed this form with the import at the start of the file
        filename = filedialog.asksaveasfilename()
        print(filename)
        if (filename) :
            if (self.snd.length() > 0) :
                fileSave = open(filename, 'w')
                # CJR I left this alone because it looks like you are
                # planning a activeVowel class - except to add the sound object
                #
                #self.activeVowel.saveToFile(fileSave, self.snd)
                fileSave.close()
            else :
                # this was just for testing
                fileTest = open(filename, 'w')
                fileTest.write("test\n")
                fileTest.close()

    def loadVowel(self):
        path = tk.filedialog.askopenfilename()
        self.exampleVowel = Vowel(0,0,0, path)
    
    def clearVowel(self):
        self.exampleVowel = None

    # CJR added an exit function
    def exitApp(self):
        # CJR how do we exit a Tcl application cleanly?
        self.parent.destroy()
        self.parent.quit()

    def help(self):
        #nothing yet
        return

    def testCanvas(self):
        box = g.Rectangle( Point(1,1), Point(99,74))
        box.draw(self.graphWin)

    # Button commands
    def record(self):
        print("in the record method ", self.id)
        if (self.recordButton["text"] == "Record") :
            print ("Record")
            self.recordButton.config(text="Stop")
            self.playButton.config(state=tk.DISABLED)
            # CJR add in the tkSnack commands to start the recording
            if (useTkSnack) :
                self.snd.record()
            self.id = self.parent.after(100,self.draw())
            #else:
            #    self.start()
        else:
            print("Stop")
            self.recordButton.config(text="Record")
            self.playButton.config(state=tk.NORMAL)
            # CJR add in the tkSnack commands to stop the recording
            if (useTkSnack) :
                self.snd.stop()
            print("stop the id object:", self.id)
            self.parent.after_cancel(self.id)
            #else:
            #    self.stop()
        print("exiting the record method ", self.id)

    def start(self):
        global id
        id = self.parent.after(100,self.draw())

    def stop(self):
        global id
        self.parent.after_cancel(id)

    def play(self):
        if self.playButton["text"] == "Play":
            self.playButton.config(text="Stop")
            self.recordButton.config(state=tk.DISABLED)
        else:
            self.playButton.config(text="Play")
            self.recordButton.config(state=tk.NORMAL)


    # CJR window methods
    def draw(self):
        #global graphModule
        if (useTkSnack) :
            if (self.snd.length() > self.sound_length) :
                self.sound_pos = self.snd.length() - self.sound_length
                formants = self.snd.formant(start=self.sound_pos,numformants=4)
                #print(formants[0][0], formants[0][1], formants[0][2], formants[0][3] )

                #audioData = [ [ formants[0][2], formants[0][3], formants[0][4] ] ]
                #audioData = [ [ formants[0][1], formants[0][2], formants[0][3] ] ]
                audioData = [ [ formants[0][0], formants[0][1], formants[0][2] ] ]
            else :
            # CJR [f1, f2, f3] duplicate for now - change later when Mac works
                audioData = [
                         [274.2, 2022.0, 3012.4], #i
                         [268.8, 2353.4, 3420.8], #I
                         [492.7, 2088.3, 2656.1], #E
                         [753.9, 1619.9, 2494.4], #ae
                         [707.6, 1027.2, 2695.7], #\as
                         [405.6, 696.7, 2779.6], #o
                         [360.2, 858.6,  2654.7] #u
                         ]
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

        if self.graphModule.useViz == "Graph" :
            self.graphModule.drawWithGraph(audioData)
        elif self.graphModule.useViz == "Oval" :
            self.graphModule.drawWithOval(audioData)
        elif self.graphModule.useViz == "Triangle" :
            self.graphModule.drawWithTriangle(audioData)

        if (useTkSnack) :
            if (self.snd.length(unit='sec') > 20) :
                print("calling stop")
                # CJR calling record as if it was clicked will stop the recording
                # as the predetermined time.
                self.record()
                 # CJR let's see if pausing for a second helps the jitter display
            time.sleep(0.25)
        else :
            time.sleep(1)

        self.id = self.parent.after(100,self.draw())

    # CJR how to stop the process when the window is closed with the X
    def close(self):
        self.parent.quit()

    # CJR application setup and configuration methods.
    def readConfiguration(self, filename):
        configVars = VowelShapeConfig(filename)
        #print(configVars.viz, configVars.mode)
        #print(configVars.defFormants, configVars.defVowel)
        return configVars

        
def main():
    root = tk.Tk()
    if (useTkSnack) :
        print("using TkSnack")
        tkSnack.initializeSnack(root)
        snd = tkSnack.Sound()
    else :
        print("not using TkSnack")
        snd = None
    width = 800
    height = 700
    # ("<width>x<height>+<xcoords>+<ycoords>")
    root.geometry("%sx%s+80+70" % (width, height) )
    app = Application(root, snd, width, height)
    # CJR testing to see if this will stop the proces on X window closure
    root.protocol('WM_DELETE_WINDOW', app.exitApp)
    root.mainloop()

main()

