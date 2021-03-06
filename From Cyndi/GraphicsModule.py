# GraphicsModule.py

import math
#import time
from graphics import *
from Graph import *

# need an initial state for triangle, oval and points to undraw correctly
#t = None;o = None;p = None

class GraphicsModule:

    def __init__(self, viz="Graph", defVowel="i", defFormants = [ [274.2, 2022.0, 3012.4] ], w=800, h=600):
        self.window = GraphWin('Vowel Shapes', width=w, height=h)

        # set the coordinates for the lower left and upper right corners
        self.window.setCoords(0, 0, 100, 75)

        # initialize the visualization shapes to none so undraw works
        self.t = None
        self.o = None
        self.p = None
        self.m = None # the matching draw viz if Practive mode

        # set the visualization for the module
        self.useViz = viz
        self.originViz = None

        # set the origins for the Triangle and Oval visualizations
        if self.useViz == "Triangle" :
            self.originViz = Point(40, 10)
        elif self.useViz == "Oval" :
            self.originViz = Point(50, 37)

        # set the baseline vowel by character and baseline for practice mode
        self.vowel = defVowel
        self.audioFormants = defFormants
        self.drawMatching = False

    def drawMatchingViz(self, formant):
        self.drawMatching = True
        if self.useViz == "Graph" :
            self.drawWithGraph(formant)
        elif self.useViz == "Oval" :
            self.drawWithOval(formant)
        elif self.useViz == "Triangle" :
            self.drawWithTriangle(formant)
        self.drawMatching = False

    def drawWithOval(self, audioData):
        #o = None
        #global o
        for d in audioData:
            if self.o:
                self.o.undraw()

            bx, by = self.normalize(d[0], d[1], d[2])
            #o = createOval( Point(50, 37), 25, bx, by)
            if (self.drawMatching) :
                self.m = self.createOval( self.originViz, 25, bx, by)
                self.m.draw(self.window)
            else :
                self.o = self.createOval( self.originViz, 25, bx, by)
                self.o.draw(self.window)

            print("f1: %s\nf2: %s\nf3: %s" % (d[0], d[1], d[2]) )
            print("bx: %s\nby: %s\n" % (bx, by) )
            #time.sleep(1)

    def drawWithTriangle(self, audioData):
        #global t
        #t = None
        for d in audioData:
            if self.t :
                self.t.undraw()

            bx, by = self.normalize(d[0], d[1], d[2])
            #t = createTriangle( Point(40, 10), 70, bx, by)
            if (self.drawMatching) :
                self.m = self.createTriangle( self.originViz, 70, bx, by)
                self.m.draw(self.window)
            else :
                self.t = self.createTriangle( self.originViz, 70, bx, by)
                self.t.draw(self.window)

            #time.sleep(1)

    def drawWithGraph(self, audioData):
        #global p
        graph = Graph( Point(75, 50), 50)
        graph.draw(self.window)
        #p = None
        for d in audioData:
            if self.p:
                self.p.undraw()

            bx, by = self.normalize(d[0], d[1], d[2])

            # change the color if drawing the matching vowel point
            # then save it and return p to None
            if (self.drawMatching) :
                self.m =  graph.createPoint(bx, by)
                self.m.setFill('green')
                self.m.setOutline('green')
                self.m.draw(self.window)
            else :
                self.p =  graph.createPoint(bx, by)
                self.p.draw(self.window)
            #time.sleep(1)


    def createOval(self, center, size, bx, by):
        divider1 = 4/size
        divider2 = 8/size

        p1 = Point(center.getX() - bx/divider2, center.getY() - by/divider1)
        p2 = Point(center.getX() + bx/divider2, center.getY() + by/divider1)

        vowel = Oval(p1, p2)
        if (self.drawMatching) :
            vowel.setFill('green')
        else :
            vowel.setFill('yellow')

        return vowel

    def createTriangle(self, origin, size, bx, by):
        constantSide = size/2

        sideMultiplier = size/7
        angleMultiplier = float(160)/15

        side = by * sideMultiplier
        angle = math.radians(bx * angleMultiplier)


        # calculate point r
        r = Point(origin.getX() + constantSide, origin.getY() )

        # calculating point q
        t = side*math.sin(angle)
        s = side*math.cos(angle)

        q = Point(origin.getX() + s, origin.getY() + t)

        # Create the trinagle
        triangle = Polygon(origin, r, q)
        if (self.drawMatching) :
            triangle.setFill('green')
        else :
            triangle.setFill('blue')


        return triangle


    def normalize(self, f1, f2, f3):

        # Get Z values for the Balk Difference Metric
        fList = [f1, f2, f3]
        zList = [None, None, None]
        for i in range(3):
            zList[i] = 26.81/(1 + 1960/fList[i]) -0.53

        z1 = zList[0]
        z2 = zList[1]
        z3 = zList[2]

        bX = 10 - (z3 - z2)
        bY = (15 - (z3 - z1)) / 2

        return bX, bY

    def axesDraw(self):
        # draw the X axis
        startAxis = Point(0, self.originViz.getY())
        endAxis = Point(self.window.getHeight(), self.originViz.getY())
        Line(startAxis, endAxis).draw(self.window)

        # draw the Y axis
        startAxis = Point(self.originViz.getX(), 0)
        endAxis = Point(self.originViz.getX(), self.window.getWidth())
        Line(startAxis, endAxis).draw(self.window)


    

        
        













