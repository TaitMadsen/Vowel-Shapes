#
# voiceShapeConfig.py
# configuration class for the VowelShape application
#
import os.path
from Vowel import *

class VowelShapeConfig:

    def __init__(self, file):
        self.fileName = file
        configFile = open(self.fileName)
        # configuration file structure
        # 1) default visualzation type
        line = configFile.readline()
        self.viz = line.rstrip()
        # 2) default application mode
        line = configFile.readline()
        self.mode = line.rstrip()
        # 3) default baseline formant - vowel and formant definition
        #   plus wav file name if avalable
        line = configFile.readline()
        parts = line.split('$')
        vowelName = eval( parts[0] )
        vowelName = vowelName[0]
        vowelFormants = eval( parts[1] )
        # if there is a third part it is the filename for a recording of the vowel
        soundFile = ""
        soundFilename = ""
        if (len(parts) > 2) :
            soundFile = eval( parts[2] )
            soundFile = soundFile[0]
            path, filename = os.path.split(soundFile)
            soundFilename = filename
        # if there is a 4th line then it is the length of the moving average queue
        line = configFile.readline()
        self.defQueueLength = float(line.rstrip())
        # and the final line is the tolerance for matching a vowel
        line = configFile.readline()
        self.defTolerance = float(line.rstrip())
        # create a vowel object from the vowel defaults
        self.loadedVowel = Vowel(0,0,0, "Female", "")
        self.loadedVowel.setF(vowelFormants[0])
        self.loadedVowel.setAnnotation(vowelName)
        if (len(soundFile) > 0) :
            self.loadedVowel.setSoundFile(file, soundFile, soundFilename)
        # set the current active vowel to none
        # the active vowel is the vowel that the user is singing
        self.activeVowel = None
        # set the gender to Female as the default
        self.singerGender = "Female"
        

