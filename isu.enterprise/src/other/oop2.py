from interfaces import IFigure
from zope.interface import implementer

@implementer(IFigure)
class Figure(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __str__(self):
        return "{}(x={},y={y})".format(self.__class__.__name__,
            self.x,y=self.y)

    def move(self, dx,dy):
        self.hide()
        self.x+=dx
        self.y+=dy
        self.show()

    def show(self):
        raise RuntimeError("shold be implemented in a subclass")

    def hide(self):
        raise RuntimeError("shold be implemented in a subclass")


class Point(Figure):
    def __init__(self, x,y, col="black"):
        super(Point,self).__init__(x,y)
        self.col=col

    def hide(self):
        print("Hide point")

    def show(self):
        print("Show point")

class Circle(Point):
    def __init__(self, x,y,r,col="black"):
        super(Circle,self).__init__(x,y,col=col)
        self.r=r

    def hide(self):
        print("Hide circle")

    def show(self):
        print("Show circle")

class Rectangle(Point):
    def __init__(self, x,y, w,h, col="black"):
        super(Rectangle, self).__init__(x,y,col=col)
        self.h=h
        self.w=w

    def hide(self):
        print("Hide rectange")

    def show(self):
        print("Show rectange")

class Composition(Figure):
    def __init__(self, x,y):
        super(Composition, self).__init__(x,y)
        self.figures=[]

    def printcomp(self):
        print("A coposition")
        print("-"*20)
        for fig in self.figures:
            print(fig)
        print("-"*20,end="\n\n")

    def add(self, fig):
        self.figures.append(fig)

    def moveall(self, dx,dy):
        for fig in self.figures:
            fig.move(dx,dy)

    def hide(self):
        for obj in self.figures:
            obj.hide()

    def show(self):
        for obj in self.figures:
            obj.show()

circle=Circle(10,10,30,col="red")
rect=Rectangle(20,20, h=100, w=200, col="green")

scr=Composition(0,0)
scr.add(circle)
scr.add(rect)

scr.printcomp()
scr.show()
scr.moveall(10,10)
