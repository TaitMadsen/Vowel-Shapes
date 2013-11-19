#
# voiceShapeConfig.py
# configuration class for the VowelShape application
#

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
        line = configFile.readline()
        parts = line.split('$')
        self.defVowel = eval( parts[0] )
        self.defVowel = self.defVowel[0]
        self.defFormants = eval( parts[1] )
        

