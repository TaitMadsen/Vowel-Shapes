# Vowel.py

class Vowel:
    def __init__(self, f1, f2, f3, fileName):
        
        # Check to see if the f's are all 0, and a fileName exists
        # CJR - how to we monitor and capture "bad" file formants
        # for a vowel? Do we need to do this for the final prototyp?
        if f1 == 0 and f2 == 0 and f3 == 0 and fileName != '':
            # Load the file
            self.loadFromFile(fileName)
        else:
            self.f1 = f1
            self.f2 = f2
            self.f3 = f3
            self.annotation = ''
        
        self.bx = None
        self.by = None
        self.normalize()
        

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
    
    # This setter method takes a list of the first 3 formants, and then normalizes them to get bx and by
    def getF(self):
        return [ [self.f1, self.f2, self.f3 ] ]

    # Setter methods
    def setAnnotation(self, anno):
        self.annotation = anno
    
    # This setter method takes a list of the first 3 formants, and then normalizes them to get bx and by
    def setF(self, fList):
        self.f1 = fList[0]
        self.f2 = fList[1]
        self.f3 = fList[2]
        self.normalize()

    # I want to be able to return the sound object with the getter method for the soundFile
    
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
        f.write( self.annotation )
        f.close()

    # Load from a file
    # This will be called by init if necessary
    def loadFromFile(self, path):
        f = open(path, "r")
        info = f.read().split('\n')
        self.f1 = float(info[0])
        self.f2 = float(info[1])
        self.f3 = float(info[2])
        self.annotation = info[3]







