# GraphicsModule.py

import math
#import time
from graphics import *
from Graph import *
#initialize the global variables
window = None   # window will be defined later

# need an initial state for triangle, oval and points to undraw correctly
t = None
o = None
p = None

# which vizualization to use and the origin for the vizualization
# these should be tracked by the application state - VowelShapesState
useViz = StringVar()
originViz = None
n = 1024
w = 300
h = 300
pos = 0

class GraphicsModule:

    def __init__(self, w=800, h=600):
        self.window = GraphWin('Vowel Shapes', width=w, height=h)
        # set the coordinates for the lower left and upper right corners
        self.window.setCoords(0, 0, 100, 75)
        return self.window

    def draw():
        global useViz
        if (snd.length() > n) :
            pos = snd.length() - n
            formants = snd.formant(start=pos,numformants=4)
            print(formants[0][0], formants[0][1], formants[0][2], formants[0][3] )

            audioData = [ [ formants[0][0], formants[0][1], formants[0][2], formants[0][3] ] ]
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

        if useViz == "Graph" :
            drawWithGraph(window, audioData)
        elif useViz == "Oval" :
            drawWithOval(window, audioData)
        elif useViz == "Triangle" :
            drawWithTriangle(window, audioData)

        if (snd.length(unit='sec') > 20) :
            print("calling stop")
            stop()
        id = root.after(100,draw)

    def drawWithOval(window, audioData):
        #o = None
        global o
        for d in audioData:
            if o:
                o.undraw()

            bx, by = normalize(d[0], d[1], d[2])
            #o = createOval( Point(50, 37), 25, bx, by)
            o = createOval( originViz, 25, bx, by)
            o.draw(window)

            print("f1: %s\nf2: %s\nf3: %s" % (d[0], d[1], d[2]) )
            print("bx: %s\nby: %s\n" % (bx, by) )
            #time.sleep(1)

    def drawWithTriangle(window, audioData):
        global t
        #t = None
        for d in audioData:
            if t :
                t.undraw()

            bx, by = normalize(d[0], d[1], d[2])
            #t = createTriangle( Point(40, 10), 70, bx, by)
            t = createTriangle( originViz, 70, bx, by)
            t.draw(window)

            #time.sleep(1)

    def drawWithGraph(window, audioData):
        global p
        graph = Graph( Point(75, 50), 50)
        graph.draw(window)
        #p = None
        for d in audioData:
            if p:
                p.undraw()

            bx, by = normalize(d[0], d[1], d[2])

            p =  graph.createPoint(bx, by)
            p.draw(window)

            #time.sleep(1)


    def createOval(center, size, bx, by):
        divider1 = 4/size
        divider2 = 8/size

        p1 = Point(center.getX() - bx/divider2, center.getY() - by/divider1)
        p2 = Point(center.getX() + bx/divider2, center.getY() + by/divider1)

        vowel = Oval(p1, p2)
        vowel.setFill('yellow')

        return vowel

    def createTriangle(origin, size, bx, by):
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
        triangle.setFill('blue')


        return triangle


    def normalize(f1, f2, f3):

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

    def axesDraw(win):
        # draw the X axis
        startAxis = Point(0, originViz.getY())
        endAxis = Point(win.getHeight(), originViz.getY())
        Line(startAxis, endAxis).draw(win)

        # draw the Y axis
        startAxis = Point(originViz.getX(), 0)
        endAxis = Point(originViz.getX(), win.getWidth())
        Line(startAxis, endAxis).draw(win)


    

        
        













