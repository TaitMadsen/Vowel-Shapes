# 
# VowelShapes - application for comparing "baseline" formants
# to an external or recoded audio file for practive with singing or saying
# vowels.
#
# This module integrates the remaining subsystems of the application
#

__author__="C. Ryan"
__date__ ="$Nov 17, 2013 10:43:50 AM$"
from VowelShapesState import *
from VowelShapeConfig import *
from GraphicsModule import *

# introduce the sound support
from tkinter import *
from tkSnack import *

# initialize the global variables for the sound
root = tkinter.Tk()
initializeSnack(root)
snd = Sound()

#initialize the defaults for graphics
w = 800
h = 600

#initialize the defaults for the sound
n = 1024
pos = 0

# initialize the global modules to None for access
graphModule = None
stateOfApp = None

def stop():
    snd.stop()
    root.after_cancel(id)

def draw():
    global graphModule
    if (snd.length() > n) :
        pos = snd.length() - n
        formants = snd.formant(start=pos,numformants=4)
        print(formants[0][0], formants[0][1], formants[0][2], formants[0][3] )

        #audioData = [ [ formants[0][2], formants[0][3], formants[0][4] ] ]
        audioData = [ [ formants[0][1], formants[0][2], formants[0][3] ] ]
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
        stop()
    id = root.after(100,draw)

def start():
    #pos = 0
    snd.record()
    #c.update_idletasks()
    id = root.after(100,draw)

def readConfiguration(filename):
    configVars = VowelShapeConfig(filename)
    print(configVars.viz, configVars.mode)
    print(configVars.defFormants, configVars.defVowel)
    return configVars

if __name__ == '__main__':
    # read the configuration file
    defaultSetup = readConfiguration("./vowelShapeConfig.txt")
    # initialize the state of the application
    stateOfApp = VowelShapesState(defaultSetup.viz, sound=snd)
    #initialize the graphics module
    graphModule = GraphicsModule(stateOfApp.useViz, defaultSetup.defVowel, defaultSetup.defFormants, w, h)
    if graphModule.originViz :
        graphModule.axesDraw()
    if (defaultSetup.mode == "Practice") :
        graphModule.drawMatchingViz(defaultSetup.defFormants)
    #c = SnackCanvas(height=h, width=w, bg='black')
    #c.pack()
    #f = Frame()
    #f.pack()
    #draw()
    start()
    #Button(f, bitmap='snackRecord', fg='red', command=start).pack(side='left')
    #Button(f, bitmap='snackStop', command=stop).pack(side='left')
    #Button(f, text='Exit', command=root.quit).pack(side='left')
    #root.mainloop()
    #draw()
    graphModule.window.mainloop()
    stop()
    graphModule.window.close()
