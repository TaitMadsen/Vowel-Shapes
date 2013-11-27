# Application.py

import math
import time
import TBMGraphics as g
from Graph import *
import tkinter as tk
from tkinter import filedialog  # CJR Windows needed this import
from tkinter import messagebox
from tkinter import StringVar
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
        # make the sound object of tkSnack part of the Application class
        self.snd = sound
        #initialize the defaults for the sound processing in draw
        self.sound_length = 2048
        self.sound_pos = 0
        self.id = None
        # Dimensions
        self.width = width
        self.height = height

        # setup the initial canvas for drawing
        self.graphWin = g.GraphWin(self)
        self.graphWin.setCoords(0,0,100,75)
        self.graphWin.grid(column=0,row=0,columnspan=2)

        # The menubar
        self.menubar = tk.Menu(self.parent)
        self.parent.config(menu=self.menubar)
        
        # The menus
        self.setupFileMenu()
        self._currentMode = StringVar()
        self._currentMode.set("Practice")
        self.lastMode = None
        self.setupActionMenu()
        self.setupDemoVowelMenu()
        self.setupDemoVizMenu()
        self.setupMicMenu()
        self.setupHelpMenu()

        # The buttons
        self.recordButton = tk.Button(self.parent, text="Record", command=self.record)
        self.recordButton.grid(column=0, row=1)

        self.saveVowelAnnotation = ""
        self.annotationButton = tk.Button(self.parent, text="Add Annotation", command=self.vowelAnnotationBox)
        self.annotationButton.grid(column=0, row=2)

        self.playButton = tk.Button(self.parent, text="Play", command=self.play)
        self.playButton.grid(column=1, row=1)

        # The name of the vowel that is loaded - what the user is trying to match
        self.matchVowelLabel = tk.Label(self.parent, text="")
        self.matchVowelLabel.grid(column=1, row=2)

        # read the application configuration file
        #self.defaultSetup = self.readConfiguration("./vowelShapeConfig.txt")
        self.currentState = self.readConfiguration("./vowelShapeConfig.txt")

        # find the application root directory
        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)

        # now set the default directory to load or save vowels to
        self.vowel_path = os.path.join(application_path, "baselineFormants")

        # set the mask for saving or loading files
        self.filemask = [
                    ("Vowel files","*.dip"),
                    ("Formant files","*.txt"),
                    ("All files","*.*")]

        # Demo matching vowel
        self.matchVowelLabel = tk.Label(self.parent, text=self.currentState.loadedVowel.getAnnotation())
        self.matchVowelLabel.grid(column=1, row=2)

        #initialize the graphics module
        self.graphModule = GraphicsModule(self.graphWin, self.currentState.viz,
                                        self.currentState.loadedVowel.getAnnotation(), self.currentState.loadedVowel.getF())
        self.setupGraph(self.currentState.viz)

        # disable the Play button if there is not sound for the loaded Vowel
        self.disablePlayOnNoSound()

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
        self.actionMenu = tk.Menu(self.menubar)
    
        self.actionMenu.add_radiobutton(label="Mentor", variable=self._currentMode, command = self.mentorMode, value="Mentor")
        self.actionMenu.add_radiobutton(label="Study",  variable=self._currentMode, command = self.studyMode, value="Study")
        self.actionMenu.add_radiobutton(label="Practice",  variable=self._currentMode, command = self.practiceMode, value="Practice")
        self.actionMenu.add_radiobutton(label="Review",  variable=self._currentMode, command = self.reviewMode, value="Review")
    
        self.menubar.add_cascade(label="Mode", menu = self.actionMenu)
    
    def setupHelpMenu(self):
        helpMenu = tk.Menu(self.menubar)
    
        helpMenu.add_command(label="The Different Modes", command=self.modesHelp)
    
        self.menubar.add_cascade(label="Help", menu=helpMenu)

    # only for the Demo - Vowels and Viza - well maybe it will stay for awhile
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

    def setupMicMenu(self):
        micMenu = tk.Menu(self.menubar)
        if (useTkSnack) :
            # build the menu using the microphones listed
            self.inputDevices = tkSnack.audio.inputDevices()
            self.inputSelected = []
            count = 0
            for mic in self.inputDevices :
                print("mic ", mic, " count ", count)
                micMenu.add_radiobutton(label=mic, command=lambda index=count : self.setInputDevice(index))
                count = count + 1
        self.menubar.add_cascade(label="Input Devices", menu=micMenu)

    def setInputDevice(self, item):
        print("select ", item)
        tkSnack.audio.selectInput(self.inputDevices[item])

    # menu commands
    def saveVowel(self):
        # make sure there is something to save
        if (self.snd.length() > 0) :
            # first check if there is an annotation
            if ( self.currentState.activeVowel.getAnnotation() == "None" ) :
                # If there is an annotation available add it
                # it would be nice to have it pop up here but we are running
                # out of time - CJR improvement
                if ( len(self.saveVowelAnnotation) > 0 ) :
                    self.currentState.activeVowel.setAnnotation(self.saveVowelAnnotation)
                    self.saveVowelAnnotation = ""
            #path = tk.filedialog.asksaveasfilename()
            # CJR Windows needed this form with the import at the start of the file
            fileSave = filedialog.asksaveasfilename(
                title="Save the vowel",
                initialdir=self.vowel_path,
                initialfile="defaultVowel.dip",
                defaultextension=".dip",
                filetypes=self.filemask)
            if (fileSave) :
                # the user did not cancel the operation - get the filename
                path, filename = os.path.split(fileSave)
                file, ext = os.path.splitext(filename)
                # this saves the audio as a wav file
                # it is saved in the same directory, with the same filename
                # as the formant file - but with a wav extention
                sndFilename = file + ".wav"
                #sndPath = path + "/" + sndFileName
                sndPath = os.path.join(path, sndFilename)
                self.snd.write(sndPath)
                self.snd.flush()
                # set the activeVowel sound references
                self.currentState.activeVowel.setSoundFile(sndPath, sndFilename)
                # this saves the formant values of the last note
                self.currentState.activeVowel.saveToFile(fileSave)
        else :
            #request that the user record a vowel first
            messagebox.showinfo("Record a Vowel", "Please record a vowel.")
        self.parent.focus_force()

    def loadVowel(self):
        # path = tk.filedialog.askopenfilename()
        # CJR Windows needed this form with the import at the start of the file
        filename = filedialog.askopenfilename(
                title="Load a vowel",
                initialdir=self.vowel_path,
                initialfile="defaultVowel.dip",
                defaultextension=".dip",
                filetypes=self.filemask)
        if (filename) :
            # the selected file is the formant file
            newVowel = Vowel(0,0,0, filename)
            if (newVowel.fileLoadFailed) :
                # the file failed to load - report a problem
                messagebox.showinfo("Error loading Vowel"," There was an error loading the vowel file.\n Please select a different file.")
                self.parent.focus_force()
                return
            # clear the old vowel from the current state and the graph
            self.clearVowel()
            # set the new loaded vowel
            self.currentState.loadedVowel = newVowel
            # add the vowel annotation to the Label
            self.loadAnyVowel(self.currentState.loadedVowel.getF(), self.currentState.loadedVowel.getAnnotation(),
                                    self.currentState.loadedVowel.getSoundFile(), self.currentState.loadedVowel.getSoundFileName())
            self.parent.focus_force()
            return True # a vowel was loaded successfully
        self.parent.focus_force()
        return False    # a vowel was not loaded successfully

    def clearVowel(self):
        # set the currentState to have no loaded vowel
        self.currentState.loadedVowel = None
        # enable both record and play
        self.recordButton.config(state=tk.NORMAL)
        self.playButton.config(state=tk.NORMAL)
        # remove the vowel text from the loaded(match) vowel label
        self.matchVowelLabel.config(text="")
        # undraw all the vowels - active and example
        self.graphModule.unDrawVowels()

    # CJR added an exit function
    def exitApp(self):
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

    # viz and vowel
    # Changing of preselected, predefined vowels
    # This could be made into a single method by having the vowels in config
    # file and loading any number of them into the menu bar.
    # this will do for now.
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
    def loadAnyVowel(self, formantList, annotation, sndFile="", sndFilename=""):
        # check if there is a loaded vowel
        if (self.currentState.loadedVowel is None) :
            self.currentState.loadedVowel = Vowel(0,0,0,'')
        # change the current vowel state to these vowel parameters
        self.currentState.loadedVowel.setF(formantList[0])
        self.currentState.loadedVowel.setAnnotation(annotation)
        self.currentState.loadedVowel.setSoundFile(sndFile, sndFilename)
        # disable or enable the play button based on sound available
        self.disablePlayOnNoSound()
        self.matchVowelLabel.config(text=self.currentState.loadedVowel.getAnnotation())
        self.graphModule.drawMatchingViz(self.currentState.loadedVowel.getF())

    # for demo vizs menu items
    def doGraph(self):
        self.setupGraph("Graph")

    def doTriangle(self):
        self.setupGraph("Triangle")

    def doOval(self):
        self.setupGraph("Oval")

    # Action menu items - the modes of the application
    # Practice mode
    def practiceMode(self):
        # Practice mode should enable and disable the correct buttons
        # and should make sure that there is a vowel loaded
        if (self.currentState.loadedVowel is None) :
            # no sample vowel let the user know to do this first
            loadVowel = messagebox.askyesno("Need to Load Vowel", "Practice Mode requires a vowel to be loaded.\n Do you want to load a vowel?")
            print("Load Vowel?", loadVowel)
            if (loadVowel == False) :
                # user does not want to continue - return focus to parent and return
                self.parent.focus_force()
                # CJR this is broken - if the selection fails keep the check next
                # to the previous mode - don't have time to fix
                print("current:", self._currentMode.get()," last:", self.lastMode)
                self._currentMode.set(self.lastMode)
                self.parent.update_idletasks() # to make sure that the geometry is set
                print("current:", self._currentMode.get()," last:", self.lastMode)
                return
            # let the user load the vowel then come back here and doe
            # the remainder of the practice mode actions
            vowelLoadedOK = self.loadVowel()
            if (vowelLoadedOK == False) :
                # let the user know something went wrong
                messagebox.showinfo("Problem Loading Vowel", "There was a problem loading the vowel. Please try again.")
                self._currentMode.set(self.lastMode)
                self.parent.focus_force()
                return
        # there is a vowel loaded - disable the Play button
        # enable the record button
        self.playButton.config(state=tk.DISABLED)
        self.recordButton.config(state=tk.NORMAL)
        # set the currect state mode
        self.currentState.mode = "Practice"
        self.lastMode = self.currentState.mode
        self.parent.focus_force()

    # Mentor mode - How should this work?
    def mentorMode(self):
        # it should also clear all previous vowel drawings - clearVowels resets
        # the buttons - do it first
        self.clearVowel()
        # Then Mentor mode should enable and disable the correct buttons
        self.playButton.config(state=tk.DISABLED)
        self.recordButton.config(state=tk.NORMAL)
        # set the currect state mode
        self.currentState.mode = "Mentor"
        self.lastMode = self.currentState.mode

    # Study mode - a vowel with a sound file must be loaded
    def studyMode(self):
        # Study mode should enable and disable the correct buttons
        # and should make sure that there is a vowel loaded with a sound file
        if (self.currentState.loadedVowel is None) :
            # no sample vowel let the user know to do this first
            loadVowel = messagebox.askyesno("Need to Load Vowel", "Study Mode requires a vowel with a sound file to be loaded.\n Do you want to load a vowel?")
            if (loadVowel == False) :
                # user does not want to continue - return focus to parent and return
                self.parent.focus_force()
                self._currentMode.set(self.lastMode)
                self.parent.update_idletasks() # to make sure that the geometry is set
                return
            # let the user load the vowel then come back here and doe
            # the remainder of the study mode actions
            vowelLoadedOK = self.loadVowel()
            if (vowelLoadedOK == False) :
                # let the user know something went wrong
                messagebox.showinfo("Problem Loading Vowel", "There was a problem loading the vowel. Please try again.")
                self.parent.focus_force()
                self._currentMode.set(self.lastMode)
                self.parent.update_idletasks() # to make sure that the geometry is set
                return
        if (len(self.currentState.loadedVowel.getSoundFile()) == 0) :
            # loaded vowel does not have sound - let the user know and exit
            messagebox.showinfo("Loading Vowel - no sound file", "The loaded vowel does not have a sound file.\n Please load a different vowel.")
            self.parent.focus_force()
            self._currentMode.set(self.lastMode)
            self.parent.update_idletasks() # to make sure that the geometry is set
            return
        # there is a sample vowel loadeed with sound
        # disable record - enable play
        self.recordButton.config(state=tk.DISABLED)
        self.disablePlayOnNoSound()
        # set the currect state mode
        self.currentState.mode = "Study"
        self.lastMode = self.currentState.mode
        self.parent.focus_force()

    # Review mode - will not implement
    def reviewMode(self):
        messagebox.showinfo("Review Mode - future", "The Review Mode will be implemented in a future version.\nThank you for your interest.\nPlease let us know your interest in this feature.")
        self.currentMode = self.lastMode
        self.parent.focus_force()

    # Button commands
    def record(self):
        print("in the record method ", self.id)
        if (self.recordButton["text"] == "Record") :
            print ("Record start")
            self.recordButton.config(text="Stop")
            self.playButton.config(state=tk.DISABLED)
            # initialize the activeVowel
            self.currentState.activeVowel = Vowel(10,10,10,"")
            # CJR add in the tkSnack commands to start the recording
            if (useTkSnack) :
                self.snd.flush()
                self.snd.record()
            #self.startRecord()
            self.id = self.parent.after(100,self.draw)
        else:
            print("Record Stop")
            self.recordButton.config(text="Record")
            self.playButton.config(state=tk.NORMAL)
            # CJR add in the tkSnack commands to stop the recording
            if (useTkSnack) :
                self.snd.stop()
            #self.stop()
            self.parent.after_cancel(self.id)
        print("exiting the record method ", self.id)

    def play(self):
        if self.playButton["text"] == "Play":
            self.playButton.config(text="Stop")
            self.recordButton.config(state=tk.DISABLED)
            if (useTkSnack) :
                self.snd.flush()
                self.snd.read(self.currentState.loadedVowel.getSoundFile())
                self.snd.play()
        else:
            self.playButton.config(text="Play")
            self.recordButton.config(state=tk.NORMAL)
            if (useTkSnack) :
                self.snd.stop()

    # disable play if there is not sound for the loaded variable
    def disablePlayOnNoSound(self):
        if ( len(self.currentState.loadedVowel.getSoundFileName()) ==0 ) :
            self.playButton.config(state=tk.DISABLED)
        else :
            self.playButton.config(state=tk.NORMAL)

    # CJR window methods
    def draw(self):
        #print("draw ", self.id)
        audioData = [[274.2, 2022.0, 3012.4]] #i
        if (useTkSnack) :
            if (self.snd.length() > self.sound_length) :
                self.sound_pos = self.snd.length() - self.sound_length
                formants = self.snd.formant(start=self.sound_pos)
                #formants = self.snd.formant(start=self.sound_pos,numformants=4, framelength=0.005, windowtype='Hanning', windowlength=0.024, lpctype=1)
                #print(formants[0][0], formants[0][1], formants[0][2], formants[0][3] )
                fSum = [ sum(x) for x in zip(*formants) ]
                fLength = len(formants)
                fAvg = [x/fLength for x in fSum]
                audioData = [ [ fAvg[0], fAvg[1], fAvg[2] ] ]
                formantList = [ fAvg[0], fAvg[1], fAvg[2] ]
                self.currentState.activeVowel.setF(formantList)
                #print(fLength, formantList)
            else :
                if ( self.currentState.loadedVowel is not None) :
                    audioData = self.currentState.loadedVowel.getF()
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
        #print(self.graphModule.mbx, self.graphModule.mby)

        if (useTkSnack == False) :
            time.sleep(1)
#            if (self.snd.length(unit='sec') > 20) :
#                print("calling stop")
#                # CJR calling record as if it was clicked will stop the recording
#                # as the predetermined time.
#                self.record()
#                 # CJR let's see if pausing for a second helps the jitter display
#            time.sleep(0.25)
#        else :

        self.id = self.parent.after(100,self.draw)

    # CJR how to stop the process when the window is closed with the X
    def close(self):
        self.parent.quit()

    # CJR undraw and draw the new configuration
    def setupGraph(self, viz):
        self.graphModule.reDraw(viz)
        #if self.graphModule.originViz :
        #    self.graphModule.axesDraw()
        if (self.currentState.mode == "Practice") :
            if (self.currentState.loadedVowel) :
                # make sure that a vowel is loaded - on start up the config
                # file should have had a vowel - when changing to Practice
                # mode the user should be asked to load a vowel before
                # entering the Practice mode
                self.graphModule.drawMatchingViz(self.currentState.loadedVowel.getF())

    # CJR application setup and configuration methods.
    def readConfiguration(self, filename):
        configVars = VowelShapeConfig(filename)
        #print(configVars.viz, configVars.mode)
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
    root.update_idletasks() # to make sure that the geometry is set
    app = Application(root, snd, width, height)
    # CJR testing to see if this will stop the process on X window closure
    root.protocol('WM_DELETE_WINDOW', app.exitApp)
    root.mainloop()

main()

