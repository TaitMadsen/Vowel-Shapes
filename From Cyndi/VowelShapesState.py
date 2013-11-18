# VowelShapesState.py
#
# Tracks the state of the VowelShape application
# There are potentially 4 states:
#   1) Record - this is a mode for instructors to record the formants
#       that the student should try to replicate.
#   2) Practice - this is a mode for the student to select the vowel to
#       practice from an instructor or other source (such as coach).
#   3)
#   4)
#
#__author__="C. Ryan"
#__date__ ="$Nov 17, 2013 10:43:50 AM$"

class VowelShapesState:

    def __init__(self, viz, sound):
        # track the current visualization - default of Graph
        self.useViz = viz

        # track the current sound
        self.sound = sound



