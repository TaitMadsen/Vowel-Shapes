# GraphicsModule.py

import math
#import time
from graphics import *
from Graph import *

# need an initial state for triangle, oval and points to undraw correctly
#t = None;o = None;p = None

class GraphicsModule:

    def __init__(self, appWindow, viz="Graph", defVowel="i", defFormants = [ [274.2, 2022.0, 3012.4] ]):
        #self.window = GraphWin('Vowel Shapes', width=w, height=h)
        self.window = appWindow

        # set the coordinates for the lower left and upper right corners
        #self.window.setCoords(0, 0, 100, 75)

        # initialize the visualization shapes to none so undraw works
        self.t = None
        self.o = None
        self.p = None
        self.m = None # the matching draw viz if Practive mode

        # initializa thegraph object and axis lines to none
        self.xA = None
        self.yA = None
        self.graph = None

        # setup the canvas
        self.reDraw(viz)

        # set the baseline vowel by character and baseline for practice mode
        self.setVowelInfo(defVowel, defFormants)

    def drawMatchingViz(self, formant):
        self.drawMatching = True
        if self.m :
            self.m.undraw()

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

            #print("f1: %s\nf2: %s\nf3: %s" % (d[0], d[1], d[2]) )
            #print("bx: %s\nby: %s\n" % (bx, by) )
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
        #undraw the previous graph if any
        if self.graph :
            self.graph.undrawAxis()
        self.graph = Graph( Point(75, 50), 50)
        self.graph.draw(self.window)
        #p = None
        for d in audioData:
            if self.p:
                self.p.undraw()

            bx, by = self.normalize(d[0], d[1], d[2])

            # change the color if drawing the matching vowel point
            # then save it and return p to None
            if (self.drawMatching) :
                self.m =  self.graph.createPoint(bx, by)
                self.m.setFill('green')
                self.m.setOutline('green')
                self.m.draw(self.window)
            else :
                self.p =  self.graph.createPoint(bx, by)
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
        # Draw the x and y axes for the triangle and oval
        self.xA = Line(Point(0, self.originViz.getY()), Point(self.window.width, self.originViz.getY()))
        self.xA.draw(self.window)

        self.yA = Line(Point(self.originViz.getX(), 0), Point(self.originViz.getX(), self.window.height))
        self.yA.draw(self.window)

    def reDraw(self, viz):
        # first clean off the canvas of any previous drawing
        if self.graph :
            self.graph.undrawAxis()
            self.graph = None
        if self.xA :
            self.xA.undraw()
        if self.yA :
            self.yA.undraw()
        if self.m :
            self.m.undraw()
        if self.o :
            self.o.undraw()
        if self.t :
            self.t.undraw()
        if self.p :
            self.p.undraw()

        # set the visualization for the module
        self.useViz = viz
        self.originViz = None

        # next setup the vizualization orgin parameters
        if self.useViz == "Triangle" :
            self.originViz = Point(40, 10)
        elif self.useViz == "Oval" :
            self.originViz = Point(50, 37)

    def setVowelInfo(self, defV, defF):
        self.vowel = defV
        self.audioFormants = defF
        self.drawMatching = False

    

        
        













