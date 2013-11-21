# Graph.py

from graphics import *

class Graph:
    
    def __init__(self, origin, size):
        self.origin = origin
        self.size = size
        self.xAxis = Line( Point(origin.getX() - size, origin.getY()), origin )
        self.yAxis = Line( origin, Point(origin.getX(), origin.getY() - size/2) )
        self.q = 8/size

    def draw(self, window):
        self.xAxis.draw(window)
        self.yAxis.draw(window)

    def undrawAxis(self):
        if self.xAxis :
            self.xAxis.undraw()
        if self.yAxis :
            self.yAxis.undraw()

    def createPoint(self, bx, by):
        x = self.origin.getX() - bx/(self.q)
        y = self.origin.getY() - by/(self.q)

        c = Circle( Point(x, y), self.size/150)
        c.setFill('red')
        c.setOutline('red')

        return c

