# Vowel.py

class Vowel:
    def __init__(self, f1, f2, f3, gender, fileName):

        # check for if the file format is bad and the object is bad
        self.fileLoadFailed = False

        # default values for sound variables
        self.soundFile = ""
        self.soundFilename = ""
        self.annotation = "None"
        self.gender = gender     # default the gender to Female == 1

        # Check to see if the f's are all 0, and a fileName exists
        # CJR - how to we monitor and capture "bad" file formants
        # for a vowel? Do we need to do this for the final prototyp?
        if f1 == 0 and f2 == 0 and f3 == 0 and fileName != '':
            # Load the file
            ok = self.loadFromFile(fileName)
            if (ok == False) :
                print("Vowel returning None")
                self.fileLoadFailed = True
                return
        else :
            self.f1 = f1
            self.f2 = f2
            self.f3 = f3
        
        self.bx = None
        self.by = None
        if ( (f1 == 0 and f2 == 0 and f3 == 0) == False ) :
            self.normalize()
        print("Gender new vowel ", self.gender)


    # Getter methods
    def getF1(self):
        return self.f1
    def getF2(self):
        return self.f2
    def getF3(self):
        return self.f3
    def getBx(self):
        return self.bx
    def getBy(self):
        return self.by
    def getAnnotation(self):
        return self.annotation
    
    # This get method return a list of the three formants that define the vowel
    def getF(self):
        return [ [self.f1, self.f2, self.f3 ] ]

    # get methods for the sound filename and file location
    def getSoundFile(self):
        return self.soundFile
    def getSoundFileName(self):
        return self.soundFilename

    # Setter methods
    def setAnnotation(self, anno):
        self.annotation = anno
    
    # This setter method takes a list of the first 3 formants, and then normalizes them to get bx and by
    def setF(self, fList):
        self.f1 = fList[0]
        self.f2 = fList[1]
        self.f3 = fList[2]
        self.normalize()

    # set the filename and file location for any associated sound file
    def setSoundFile(self, file, filename):
        self.soundFile = file
        self.soundFilename = filename
    
    # Sets the bx and by instance variables
    def normalize(self):
        
        # Get Z values for the Balk Difference Metric
        fList = [self.f1, self.f2, self.f3]
        zList = [None, None, None]
        for i in range(3):
            zList[i] = 26.81/(1 + 1960/fList[i]) -0.53
        
        z1 = zList[0]
        z2 = zList[1]
        z3 = zList[2]
        
        self.bx = 10 - (z3 - z2)
        self.by = (15 - (z3 - z1)) / 2


    # Save to a file
    def saveToFile(self, path):
        f = open(path, "w")
        f.write( str(self.f1) + '\n')
        f.write( str(self.f2) + '\n')
        f.write( str(self.f3) + '\n')
        f.write( self.annotation + '\n' )
        if (self.gender == 1) :
            f.write( "Female" + '\n')
        else :
            f.write( "Female" + '\n')
        if (len(self.soundFile) > 0) :
            # save the sound and sound filename information
            f.write( self.soundFile + '\n')
            f.write(self.soundFilename + '\n')
        f.close()

    # Load from a file
    # This will be called by init if necessary
    def loadFromFile(self, path):
        f = open(path, "r")
        info = f.read().split('\n')
        if (len(info)<3) :
            # not enough information in the file
            return False
        try :
            self.f1 = float(info[0])
            self.f2 = float(info[1])
            self.f3 = float(info[2])
        except ValueError:
            return False
        if (len(info)>3) :
            self.annotation = info[3]
        # check if the gender was provided
        if (len(info) > 4) :
            if (info[4] == "Female") :
                self.gender = 1
            else :
                self.gender = 2
        # check if there is an associated sound file and filename
        if (len(info) > 5) :
            self.soundFile = info[5]
            self.soundFilename = info[6]
        return True







