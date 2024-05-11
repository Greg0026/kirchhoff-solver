import customtkinter as ctk
from abc import ABC, abstractmethod
import re

class Component(ABC):
    @abstractmethod
    def __init__():
        '''
        Defines the starting values
        Excecutes the draw() method
        '''
    
    @abstractmethod
    def draw():
        '''
        Draw the canvas component
        '''

    @abstractmethod
    def delete():
        '''
        Deletes all the canvas component
        Deallocates memory
        '''

class Wire(Component):

    component = "Conduttore"

    def __init__(self, breadboard: ctk.CTkCanvas, start: list, end: list):
        self.breadboard = breadboard
        self.start = start
        self.end = end
        self.draw()

    def draw(self):
        try:
            self.canvasID = self.breadboard.create_line(self.start[0], self.start[1], self.end[0], self.end[1], width=5, fill="black")
            self.startingCircle = self.breadboard.create_aa_circle(self.start[0], self.start[1], 8, fill="black")
            self.endingCircle = self.breadboard.create_aa_circle(self.end[0], self.end[1], 8, fill="black")
            self.text = self.breadboard.create_text((self.start[0]+self.end[0])/2 - 25, (self.start[1]+self.end[1])/2 - 10, text=self.canvasID, font=("Fantasy 10"))
        except Exception:
            pass

    def delete(self):
        try:
            self.breadboard.delete(self.canvasID)
            self.breadboard.delete(self.startingCircle)
            self.breadboard.delete(self.endingCircle)
            self.breadboard.delete(self.text)
            del self
        except Exception:
            pass

class Resistor(Component):

    component = "Resistore"

    def __init__(self, breadoard: ctk.CTkCanvas, start: list, end: list):
        self.breadboard = breadoard
        self.start = start
        self.end = end
        self.draw()

    def draw(self):
        if self.end[0]==self.start[0]:
            points = [self.start[0], [self.start[1]+5 if self.start[1]<self.end[1] else self.start[1]-5]]
            for i in range(1, 7):
                if i%2==0:
                    points.append(self.start[0]-15)
                else:
                    points.append(self.start[0]+15)
                points.append([self.start[1]+120/7*i if self.start[1]<self.end[1] else self.start[1]-120/7*i])
            points.append(self.start[0])
            points.append([self.start[1]+115 if self.start[1]<self.end[1] else self.start[1]-115])
        else:
            points = [[self.start[0]+5 if self.start[0]<self.end[0] else self.start[0]-5], self.start[1]]
            for i in range(1, 7):
                points.append([self.start[0]+120/7*i if self.start[0]<self.end[0] else self.start[0]-120/7*i])
                if i%2==0:
                    points.append(self.start[1]+15)
                else:
                    points.append(self.start[1]-15)
            points.append([self.start[0]+115 if self.start[0]<self.end[0] else self.start[0]-115])
            points.append(self.start[1])
        self.canvasID = self.breadboard.create_line(points, width=5, fill="black")
        self.text = self.breadboard.create_text((self.start[0]+self.end[0])/2 - 30, (self.start[1]+self.end[1])/2 - 30, text=self.canvasID, font=("Fantasy 10"))
    
    def delete(self):
        try:
            self.breadboard.delete(self.canvasID)
            self.breadboard.delete(self.text)
            del self
        except:
            pass

class Generator(Component):

    component = "Generatore"

    def __init__(self, breadboard: ctk.CTkCanvas, start: list, end: list):
        self.breadboard = breadboard
        self.start = start
        self.end = end
        self.draw()

    def draw(self):
        if self.end[0]==self.start[0]:
            # negative pole points
            points1 = [self.start, self.start[0]]
            points1.append(self.start[1]+25) if self.start[1]<self.end[1] else points1.append(self.start[1]-25)
            points1.append(self.start[0]+15) if self.start[1]<self.end[1] else points1.append(self.start[0]-15)
            points1.append(points1[-2])
            points1.append(self.start[0]-15) if self.start[1]<self.end[1] else points1.append(self.start[0]+15)
            points1.append(points1[-2])

            # positive pole points
            points2 = []
            points2.append(points1[-2]+40) if self.start[1]<self.end[1] else points2.append(points1[-2]+10)
            points2.append(points1[-1]+10) if self.start[1]<self.end[1] else points2.append(points1[-1]-10)
            points2.append(points1[-2]-10) if self.start[1]<self.end[1] else points2.append(points1[-2]-40)
            points2.append(points2[-2])
            points2.append(points1[0][0])
            points2.append(points2[-2])
            points2.append(points2[-2])
            points2.append(points2[1]+25) if self.start[1]<self.end[1] else points2.append(points2[1]-25)
        else:
            # negative
            points1 = [self.start]
            points1.append(self.start[0]+25) if self.start[0]<self.end[0] else points1.append(self.start[0]-25)
            points1.append(self.start[1])
            points1.append(points1[-2])
            points1.append(self.start[1]+15) if self.start[0]<self.end[0] else points1.append(self.start[1]-15)
            points1.append(points1[-2])
            points1.append(self.start[1]-15) if self.start[0]<self.end[0] else points1.append(self.start[1]+15)
            
            # positive
            points2 = []
            points2.append(points1[-2]+10) if self.start[0]<self.end[0] else points2.append(points1[-2]-10)
            points2.append(points1[-1]+40) if self.start[0]<self.end[0] else points2.append(points1[-1]+10)
            points2.append(points2[-2])
            points2.append(points1[-1]-10) if self.start[0]<self.end[0] else points2.append(points1[-1]-40)
            points2.append(points2[-2])
            points2.append(points1[0][1])
            points2.append(points2[0]+25) if self.start[0]<self.end[0] else points2.append(points2[0]-25)
            points2.append(points2[-2])
                
        self.canvasID = self.breadboard.create_line(points1, width=5, fill="black")
        self.canvasID2 = self.breadboard.create_line(points2, width=5, fill="black")
        self.text = self.breadboard.create_text((self.start[0]+self.end[0])/2 - 30, (self.start[1]+self.end[1])/2 - 30, text=self.canvasID, font=("Fantasy 10"))

    def delete(self):
        try: 
            self.breadboard.delete(self.canvasID)
            self.breadboard.delete(self.canvasID2)
            self.breadboard.delete(self.text)
            del self
        except:
            pass
