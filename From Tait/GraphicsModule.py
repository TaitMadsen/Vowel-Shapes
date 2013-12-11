# GraphicsModule.py

import math
#import time
from graphics import *
from Graph import *

# need an initial state for triangle, oval and points to undraw correctly
#t = None;o = None;p = None

class GraphicsModule:

    def __init__(self, appWindow, viz="Graph", defVowel="i",
                    defFormants = [ [274.2, 2022.0, 3012.4] ], defTolerance = 0.1,
                    defQueueSize = 25, defGender = "Female"):
        #self.window = GraphWin('Vowel Shapes', width=w, height=h)
        self.window = appWindow

        # set the coordinates for the lower left and upper right corners
        #self.window.setCoords(0, 0, 100, 75)

        # initialize the visualization shapes to none so undraw works
        self.t = None
        self.o = None
        self.p = None
        self.m = None # the loaded draw viz if Practice mode
        self.mby = 0
        self.mbx = 0
        self.mArea = 0.0
        # try using a moving average of bx and by
        self.queueBx = []
        self.queueBy = []
        self.queueSize = defQueueSize
        self.vTolerance = defTolerance
        # set the default formant calculation - Female=1, Male=2
        self.gender = defGender

        # initializa the graph object and axis lines to none
        self.xA = None
        self.yA = None
        self.graph = None

        # setup the canvas
        #self.reDraw(viz)

        # set the boolean to determine the color of the viz based on
        # it being a loaded(matching) or active viz
        self.drawMatching = False
        # set the baseline vowel by character and baseline for practice mode
        #self.setVowelInfo(defVowel, defFormants)

    def drawMatchingViz(self, formant):
        self.drawMatching = True
        if self.m :
            self.m.undraw()
            self.mby = 0
            self.mbx = 0
            self.mArea = 0.0

        if self.useViz == "Graph" :
            bx, by = self.drawWithGraph(formant)
        elif self.useViz == "Oval" :
            bx, by = self.drawWithOval(formant)
            self.mArea = math.pi*(bx/2.0)*(by/2.0)
        elif self.useViz == "Triangle" :
            bx, by = self.drawWithTriangle(formant)
            self.mArea = (bx*by)/2.0
        self.mbx = bx
        self.mby = by
        self.drawMatching = False

    def drawWithOval(self, audioData):
        #o = None
        #global o
        for d in audioData:
            undrawo = False
            if self.o:
                #self.o.undraw()
                undrawo = True

            bx, by, delta = self.normalize(d[0], d[1], d[2])
            #o = createOval( Point(50, 37), 25, bx, by)
            if (self.drawMatching) :
                self.m = self.createOval( self.originViz, 25, bx, by, 10)
                self.m.draw(self.window)
            else :
                #self.o = self.createOval( self.originViz, 25, bx, by, delta)
                newO = self.createOval( self.originViz, 25, bx, by, delta)
                if (undrawo) :
                    self.o.undraw()
                self.o = newO
                self.o.draw(self.window)
            #print("Oval:", bx, by)
            return bx, by

            #print("f1: %s\nf2: %s\nf3: %s" % (d[0], d[1], d[2]) )
            #print("bx: %s\nby: %s\n" % (bx, by) )
            #time.sleep(1)

    def drawWithTriangle(self, audioData):
        #global t
        #t = None
        for d in audioData:
            undrawt = False
            if self.t :
                #self.t.undraw()
                undrawt = True

            bx, by, delta = self.normalize(d[0], d[1], d[2])
            #print("bx Triangle: ", self.queueBx)
            #t = createTriangle( Point(40, 10), 70, bx, by)
            if (self.drawMatching) :
                self.m = self.createTriangle( self.originViz, 70, bx, by)
                self.m.draw(self.window)
            else :
                #self.t = self.createTriangle( self.originViz, 70, bx, by, delta)
                newT = self.createTriangle( self.originViz, 70, bx, by, delta)
                if (undrawt) :
                    self.t.undraw()
                self.t = newT
                self.t.draw(self.window)
            #print("Triangle:", bx, by)
            return bx, by

            #time.sleep(1)

    def drawWithGraph(self, audioData):
        #undraw the previous graph if any
        if self.graph :
            self.graph.undrawAxis()
        self.graph = Graph( Point(75, 50), 50)
        self.graph.draw(self.window)
        for d in audioData:
            undrawp = False
            if self.p:
                #self.p.undraw()
                undrawp = True

            bx, by, delta = self.normalize(d[0], d[1], d[2])

            # change the color if drawing the matching vowel point
            # then save it and return p to None
            if (self.drawMatching) :
                self.m =  self.graph.createPoint(bx, by)
                self.m.setFill('blue')
                self.m.setOutline('blue')
                self.m.draw(self.window)
            else :
                #self.p =  self.graph.createPoint(bx, by)
                newp = self.graph.createPoint(bx, by)
                if (undrawp) :
                    self.p.undraw()
                self.p = newp
                if (delta < (self.vTolerance*3)) :
                    self.p.setFill('green')
                    self.p.setOutline('green')
                else :
                    self.p.setFill('red')
                    self.p.setOutline('red')
                self.p.draw(self.window)
            #time.sleep(1)
            #print("Graph:", bx, by)
            return bx, by


    def createOval(self, center, size, bx, by, delta = 10):
        divider1 = 4/size
        divider2 = 8/size

        p1 = Point(center.getX() - bx/divider2, center.getY() - by/divider1)
        p2 = Point(center.getX() + bx/divider2, center.getY() + by/divider1)

        vowel = Oval(p1, p2)
        if (self.drawMatching) :
            vowel.setFill('blue')
        else :
            if (delta < self.vTolerance) :
                vowel.setFill('green')
            else :
                vowel.setFill('yellow')

        return vowel

    def createTriangle(self, origin, size, bx, by, delta=10):
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
            triangle.setFill('blue')
        else :
            if (delta < self.vTolerance) :
                triangle.setFill('green')
            else :
                triangle.setFill('yellow')

        return triangle


    def normalize(self, f1, f2, f3):

        # Get Z values for the Balk Difference Metric
        fList = [f1, f2, f3]
        zList = [None, None, None]
        for i in range(3):
            # gender Male = 2
            if (self.gender == 2) :
                zList[i] = ( ( 26.81/(1 + 1960/fList[i]) ) -0.53 )  # for male
            else : # gender Female = 1
                zList[i] = ( ( 26.81/(1 + 1960/fList[i]) ) -0.53 ) - 1.0 # for female

        z1 = zList[0]
        z2 = zList[1]
        z3 = zList[2]

        bX = 10 - (z3 - z2)
        bY = (15 - (z3 - z1)) / 2
        #bX = (z3 - z2) *0.25
        #bY = (z3 - z1) *0.25

        # find the moving average to assist with the jitter
        self.queueBx.append(bX)
        self.queueBy.append(bY)
        if (len(self.queueBx) > self.queueSize ) :
            self.queueBx.reverse()
            self.queueBx.pop()
            self.queueBx.reverse()
            self.queueBy.reverse()
            self.queueBy.pop()
            self.queueBy.reverse()
        bSum = sum(self.queueBx)/len(self.queueBx)
        bX = bSum
        bSum = sum(self.queueBy)/len(self.queueBy)
        bY = bSum

        # calculate the delta between the current bX/bY and the match bx/by
        if (self.useViz == "Oval") :
            # find the area of the current ellipse
            area = math.pi*(bX/2.0)*(bY/2.0)
            delta = 1.0
            if (self.mArea > 0) :
                # should approaches 1 - want to approach 0 - so subract from 1
                delta = abs( (1.0 - (area/self.mArea)) )
            # find the ratio of the bx to bys - each should be 1 the difference
            # approaches 0
            bRatio = 1.0; bxRatio = 1.0; byRatio = 0.0
            if (self.mbx > 0) :
                bxRatio = 10*(bX/self.mbx)
            if (self.mby > 0) :
                byRatio = 10*(bY/self.mby)
            bRatio = abs( bxRatio - byRatio )
            # not only the area but bx and by ratio needs to approach 0
            delta = delta*bRatio
        elif (self.useViz == "Triangle") :
            area = (bX*bY)/2.0
            # should approaches 1 - want to approach 0 - so subract from 1
            delta = 1.0
            if (self.mArea > 0) :
                delta = abs( (1.0 - (area/self.mArea)) )  # should approach 0 - so subract from 1
            # find the ratio of the bx to bys - each should be 1 the difference
            # approaches 0
            bRatio = 1.0; bxRatio = 1.0; byRatio = 0.0
            if (self.mbx > 0) :
                bxRatio = 10*( math.radians(bX)/math.radians(self.mbx) )
            if (self.mby > 0) :
                byRatio = 10*(bY/self.mby)
            bRatio = abs( bxRatio - byRatio )
            # not only the area but bx and by ratio needs to approach 0
            delta = delta*bRatio
        else :
            # distance betwen the points should approach 0
            area = 0
            delta = math.sqrt(math.pow(abs(self.mbx - bX),2) + math.pow(abs(self.mby - bY),2))
            #print("delta: ", delta)
        #print("mArea area: ", self.mArea, area)
        #print("ratio xratio yratio: ", bRatio, bxRatio, byRatio)
        #print("delta:", delta)

        return bX, bY, delta

    def setGender(self, gender):
        self.gender = gender
        print("GraphModule Gender set to ", self.gender)

    def axesDraw(self):
        # Draw the x and y axes for the triangle and oval
        self.xA = Line(Point(0, self.originViz.getY()), Point(self.window.width, self.originViz.getY()))
        self.xA.draw(self.window)

        self.yA = Line(Point(self.originViz.getX(), 0), Point(self.originViz.getX(), self.window.height))
        self.yA.draw(self.window)

    def reDraw(self, viz):
        # first remove any loaded or active vowel vizs
        self.unDrawVowels()

        # second clean off the canvas of any previous drawing
        if self.graph :
            self.graph.undrawAxis()
            self.graph = None
        if self.xA :
            self.xA.undraw()
        if self.yA :
            self.yA.undraw()

        # set the current visualization for the module
        self.useViz = viz

        # next setup the vizualization orgin parameters if any
        self.originViz = None   # for the Graph visz
        if self.useViz == "Triangle" :
            self.originViz = Point(40, 10)
            self.axesDraw()
        elif self.useViz == "Oval" :
            self.originViz = Point(50, 37)
            self.axesDraw()

    # undraw all the possible vowel representations
    # clear any vowel information
    def unDrawVowels(self):
        if self.m :
            self.m.undraw()
            self.mbx = 0.0
            self.mby = 0.0
        if self.o :
            self.o.undraw()
        if self.t :
            self.t.undraw()
        if self.p :
            self.p.undraw()
        self.queueBx = []
        self.queueBy = []

#    def setVowelInfo(self, defV, defF):
#        self.vowel = defV
#        self.audioFormants = defF
#        self.drawMatching = False

    

        
        













