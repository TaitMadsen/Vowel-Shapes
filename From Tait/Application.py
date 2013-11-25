# Application.py

import math
import time
import TBMGraphics as g
from Graph import *
import tkinter as tk
from tkinter import filedialog  # CJR Windows needed this import
from tkinter import messagebox
import tkSnack as tkSnack
from GraphicsModule import *
from VowelShapeConfig import *
from Vowel import *
import os.path
import sys

#useTkSnack = False
useTkSnack = True
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
        self.setupDemoVowelMenu()
        self.setupDemoVizMenu()
        self.setupHelpMenu()

        # from the tkSnack demo files
        #Button(f, bitmap='snackRecord', fg='red', command=start).pack(side='left')
        #Button(f, bitmap='snackStop', command=stop).pack(side='left')
        #Button(f, text='Exit', command=root.quit).pack(side='left')

        # The buttons
        self.recordButton = tk.Button(self.parent, text="Record", command=self.record)
        self.recordButton.grid(column=0, row=1)

        self.saveVowelAnnotation = None
        self.annotationButton = tk.Button(self.parent, text="Set Save Name", command=self.vowelAnnotationBox)
        self.annotationButton.grid(column=0, row=2)

        self.playButton = tk.Button(self.parent, text="Play", command=self.play)
        self.playButton.grid(column=1, row=1)

        # CJR
        # options for the file dialogs
        self.save_file_opt = options = {}
        options['filetypes'] = [('all files', '.*'), ('audio files', '.mp3')]
        options['initialfile'] = 'myfile_i.mp3'
        options['parent'] = self.parent

        # read the application configuration file
        self.defaultSetup = self.readConfiguration("./vowelShapeConfig.txt")
        # Vowel objects
        f1 = self.defaultSetup.defFormants[0][0]
        f2 = self.defaultSetup.defFormants[0][1]
        f3 = self.defaultSetup.defFormants[0][2]
        self.exampleVowel = Vowel(f1,f2,f3,"")
        self.exampleVowel.setAnnotation(self.defaultSetup.defVowel)
        self.activeVowel = None

        # Demo matching vowel
        self.matchVowel = tk.Label(self.parent, text=self.exampleVowel.getAnnotation())
        self.matchVowel.grid(column=1, row=2)

        #initialize the graphics module
        self.graphModule = GraphicsModule(self.graphWin, self.defaultSetup.viz,
                                        self.exampleVowel.getAnnotation(), self.exampleVowel.getF())
        self.setupGraph(self.defaultSetup.viz)




    def setupCanvas(self):
        self.graphWin = g.GraphWin(self)
        #self.graphWin.setCoords(0,0,100,75)
        self.graphWin.setCoords(0,0,100,75)
        self.graphWin.grid(column=0,row=0,columnspan=2)
        

    # Menus
    
    def setupFileMenu(self):
        fileMenu = tk.Menu(self.menubar)
        
        fileMenu.add_command(label="About", command=self.showAbout)
        fileMenu.add_command(label="Save Vowel", command=self.saveVowel)
        fileMenu.add_command(label="Load Vowel", command=self.loadVowel)
        fileMenu.add_command(label="Clear Vowel", command=self.clearVowel)
        fileMenu.add_command(label="Exit", command=self.exitApp)  # CJR added an exit function

        self.menubar.add_cascade(label="File", menu=fileMenu)
    
    def setupActionMenu(self):
        actionMenu = tk.Menu(self.menubar)
    
        #actionMenu.add_command(label="Test Canvas", command = self.testCanvas)
        actionMenu.add_command(label="Mentor", command = self.mentorMode)
        actionMenu.add_command(label="Study", command = self.studyMode)
        actionMenu.add_command(label="Practice", command = self.practiceMode)
        actionMenu.add_command(label="Review", command = self.reviewMode)
    
        self.menubar.add_cascade(label="Mode", menu = actionMenu)
    
    def setupHelpMenu(self):
        helpMenu = tk.Menu(self.menubar)
    
        helpMenu.add_command(label="The Different Modes", command=self.modesHelp)
    
        self.menubar.add_cascade(label="Help", menu=helpMenu)

    # only for the Demo - Vowels and Viza
    def setupDemoVowelMenu(self):
        demoMenu = tk.Menu(self.menubar)

        demoMenu.add_command(label="i", command=self.loadi)
        demoMenu.add_command(label="I", command=self.loadI)
        demoMenu.add_command(label="E", command=self.loadE)
        demoMenu.add_command(label="ae", command=self.loadae)
        demoMenu.add_command(label="as", command=self.loadas)
        demoMenu.add_command(label="o", command=self.loado)
        demoMenu.add_command(label="u", command=self.loadu)

        self.menubar.add_cascade(label="Vowel", menu=demoMenu)

    def setupDemoVizMenu(self):
        demovizMenu = tk.Menu(self.menubar)

        demovizMenu.add_command(label="Graph", command=self.doGraph)
        demovizMenu.add_command(label="Triangle", command=self.doTriangle)
        demovizMenu.add_command(label="Oval", command=self.doOval)

        self.menubar.add_cascade(label="Viz", menu=demovizMenu)

    # menu commands
    def saveVowel(self):
        # make sure there is something to save
        if (self.snd.length() > 0) :
            # should also check the the formants exist ???
            # need a name to save with the vowel - is this the annotation also?
            if (self.saveVowelAnnotation) :
                self.activeVowel.setAnnotation(self.saveVowelAnnotation)
                #path = tk.filedialog.asksaveasfilename()
                # CJR Windows needed this form with the import at the start of the file
                fileSave = filedialog.asksaveasfilename()
                if (fileSave) :
                    # the user did not cancel the operation
                    if (self.snd.length() > 0) :
                        # this save the formant values of the last note
                        # we could resample the snd object and get the formants from
                        # the whole clip ???
                        self.activeVowel.saveToFile(fileSave)
                        # this saves the audio as a wav file
                        # it is saved in the save directory with the annotation name
                        path, filename = os.path.split(fileSave)
                        # WARNING - this is platform dependent ???
                        sndFileName = self.activeVowel.getAnnotation() + ".wav"
                        sndPath = path + "/" + sndFileName
                        os.path.join(path, sndFileName)
                        self.snd.write(sndPath)
                        self.snd.flush()
                self.saveVowelAnnotation = None
            else :
                #request that the user supply an annotation
                messagebox.showinfo("Need an annotation", "Please click on the Set Save Name button and enter an annotation for this vowel")
        else :
            #request that the user record a vowel first
            messagebox.showinfo("Record a Vowel", "Please record a vowel and use the Set Save Name button to associate an annotation")

    def loadVowel(self):
        # path = tk.filedialog.askopenfilename()
        # CJR Windows needed this form with the import at the start of the file
        filename = filedialog.askopenfilename()
        if (filename) :
            # clear the old vowel
            self.clearVowel()
            # the selected file is the formant file
            self.exampleVowel = Vowel(0,0,0, filename)
            # add the vowel annotation to the Label
            self.matchVowel.config(text=self.exampleVowel.getAnnotation())
            self.setupGraph(self.defaultSetup.viz)

    # load a previously saved sound file
    def loadVowelSound(self):
        filename = filedialog.askopenfilename()
        if (filename) :
            # load the file into the sound object
            # disable record and enable play
            if (useTkSnack) :
                self.snd.flush()
                self.snd.read(filename)
            self.recordButton.config(state=tk.DISABLED)
            self.playButton.config(state=tk.NORMAL)
    
    def clearVowel(self):
        self.exampleVowel = None
        self.recordButton.config(state=tk.NORMAL)
        self.playButton.config(state=tk.NORMAL)
        # remove the vowel text from the Label
        self.matchVowel.config(text="")
        # undraw all the vowels - active and example
        self.graphModule.unDrawVowels()

    # CJR added an exit function
    def exitApp(self):
        # CJR how do we exit a Tcl application cleanly?
        self.parent.destroy()
        self.parent.quit()

    def modesHelp(self):
        f = open("modesHelp.txt", "r")
        msg = f.read()
        self.vowelAnnotationBox(msg, False)
    
    def showAbout(self):
        f = open("about.txt", "r")
        msg = f.read()
        # Use Cyndi's vowelAnnotationBox to display the about information
        self.vowelAnnotationBox(msg, False)

    # demo only - viz and vowel
    # demo changing of the matching vowel
    def loadi(self):
        formants = [ [274.2, 2022.0, 3012.4] ]
        self.loadAnyVowel(formants, "i")

    def loadI(self):
        formants = [ [268.8, 2353.4, 3420.8] ]
        self.loadAnyVowel(formants, "I")

    def loadE(self):
        formants = [ [492.7, 2088.3, 2656.1] ]
        self.loadAnyVowel(formants, "E")

    def loadae(self):
        formants = [ [753.9, 1619.9, 2494.4] ]
        self.loadAnyVowel(formants, "ae")

    def loadas(self):
        formants = [ [707.6, 1027.2, 2695.7] ]
        self.loadAnyVowel(formants, "as")

    def loado(self):
        formants = [ [405.6, 696.7, 2779.6] ]
        self.loadAnyVowel(formants, "o")

    def loadu(self):
        formants = [ [360.2, 858.6,  2654.7] ]
        self.loadAnyVowel(formants, "u")

    # load any vowel with formant and annotation
    def loadAnyVowel(self, formantList, annotation):
        f1 = formantList[0][0]
        f2 = formantList[0][1]
        f3 = formantList[0][2]
        self.exampleVowel = Vowel(f1, f2, f3, '')
        self.exampleVowel.setAnnotation(annotation)
        self.defaultSetup.defFormants = formantList
        self.defaultSetup.defVowel = annotation
        self.matchVowel.config(text=self.defaultSetup.defVowel)
        self.graphModule.drawMatchingViz(formantList)

    # for demo vizs menu items
    def doGraph(self):
        self.setupGraph("Graph")

    def doTriangle(self):
        self.setupGraph("Triangle")

    def doOval(self):
        self.setupGraph("Oval")

    # Action menu items - the modes of the application
    # Practice mode - How should this work?
    def practiceMode(self):
        # Practice mode should enable and disable the correct buttons
        # and should make sure that there is a vowel loaded
        if (self.exampleVowel) :
            # there is a sample vowel loaded - diable the Play button
            self.playButton.config(state=tk.DISABLED)
            self.recordButton.config(state=tk.NORMAL)
        else :
            # no sample vowel let the user know to do this first
            messagebox.showinfo("Need to Load Vowel", "Practice Mode requires a vowel to be loaded. Please load a vowel with File->Load Vowel")

    # Mentor mode - How should this work?
    def mentorMode(self):
        # it should also clear all previous vowel drawings - clearVowels resets
        # the buttons - do it first
        self.clearVowel()
        # Then Mentor mode should enable and disable the correct buttons
        self.playButton.config(state=tk.DISABLED)
        self.recordButton.config(state=tk.NORMAL)

    # Study mode - How should this work
    def studyMode(self):
        # Study mode should enable and disable the correct buttons
        # and should make sure that there is a vowel loaded
        if (self.exampleVowel) :
            # there is a sample vowel loaded - diable the Play button
            self.recordButton.config(state=tk.DISABLED)
            self.playButton.config(state=tk.NORMAL)
        else :
            # no sample vowel let the user know to do this first
            messagebox.showinfo("Need to Load Vowel", "Study Mode requires a vowel to be loaded. Please load a vowel with File->Load Vowel")

    # Review mode - How should this work
    def reviewMode(self):
        # Study mode should enable and disable the correct buttons
        # and should make sure that there is a vowel loaded
        if (self.exampleVowel) :
            # there is a sample vowel loaded - diable the Play button
            self.recordButton.config(state=tk.DISABLED)
            self.playButton.config(state=tk.NORMAL)
        else :
            # no sample vowel let the user know to do this first
            messagebox.showinfo("Need to Load Vowel", "Review Mode requires a vowel to be loaded. Please load a vowel with File->Load Vowel")



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
            # initialize the activeVowel
            self.activeVowel = Vowel(10,10,10,"")
            # CJR add in the tkSnack commands to start the recording
            if (useTkSnack) :
                self.snd.flush()
                self.snd.record()
            #self.id = self.parent.after(100,self.draw())
            #else:
            self.start()
        else:
            print("Stop")
            self.recordButton.config(text="Record")
            self.playButton.config(state=tk.NORMAL)
            # CJR add in the tkSnack commands to stop the recording
            if (useTkSnack) :
                self.snd.stop()
            #self.parent.after_cancel(self.id)
            #else:
            self.stop()
        print("exiting the record method ", self.id)

    def start(self):
        self.id = self.parent.after(100,self.draw)

    def stop(self):
        self.parent.after_cancel(self.id)

    def play(self):
        if self.playButton["text"] == "Play":
            self.playButton.config(text="Stop")
            self.recordButton.config(state=tk.DISABLED)
            if (useTkSnack) :
                self.snd.play()
        else:
            self.playButton.config(text="Play")
            self.recordButton.config(state=tk.NORMAL)
            if (useTkSnack) :
                self.snd.stop()

    # CJR window methods
    def draw(self):
        #print("draw ", self.id)
        if (useTkSnack) :
            if (self.snd.length() > self.sound_length) :
                self.sound_pos = self.snd.length() - self.sound_length
                formants = self.snd.formant(start=self.sound_pos,numformants=4)
                #print(formants[0][0], formants[0][1], formants[0][2], formants[0][3] )
                fSum = [ sum(x) for x in zip(*formants) ]
                fLength = len(formants)
                fAvg = [x/fLength for x in fSum]
                audioData = [ [ fAvg[0], fAvg[1], fAvg[2] ] ]
                formantList = [ fAvg[0], fAvg[1], fAvg[2] ]
                self.activeVowel.setF(formantList)
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

        self.id = self.parent.after(100,self.draw)

    # CJR how to stop the process when the window is closed with the X
    def close(self):
        self.parent.quit()

    # CJR undraw and draw the new configuration
    def setupGraph(self, viz):
        self.graphModule.reDraw(viz)
        if self.graphModule.originViz :
            self.graphModule.axesDraw()
        if (self.defaultSetup.mode == "Practice") :
            self.graphModule.drawMatchingViz(self.exampleVowel.getF())

    # CJR application setup and configuration methods.
    def readConfiguration(self, filename):
        configVars = VowelShapeConfig(filename)
        #print(configVars.viz, configVars.mode)
        #print(configVars.defFormants, configVars.defVowel)
        return configVars

    # CJR pop up window to collect the name to save a vowel under
    # complements of
    # http://stackoverflow.com/questions/10057672/correct-way-to-implement-a-custom-popup-tkinter-dialog-box
    #
    def vowelAnnotationBox(self, msg='Enter an annotation for the Vowel', extra=True):
        top = self.top = tk.Toplevel(self)
        label0 = tk.Label(top, text=msg)
        label0.pack()

        if extra:
            self.entry0 = tk.Entry(top)
            self.entry0.pack()
            self.entry0.focus_set()

            button2 = tk.Button(top, text='Submit', command=self.submitVowelName)
            button2.pack()

        button3 = tk.Button(top, text='Cancel',
                                command=lambda: self.top.destroy())
        button3.pack()
        top.focus_force()

    def submitVowelName(self):
        data = self.entry0.get()
        if data:
            self.saveVowelAnnotation = data
            self.top.destroy()
       
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

