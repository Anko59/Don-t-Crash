import pygame
from pygame.locals import *
from math import *
from random import randrange
from threading import Thread
import time
pygame.init()
fenetre=pygame.display.set_mode((1400,700))
fenetre.fill((255,255,255))
startPos = [10,20]
def draw_line(pos):
    pygame.draw.line(fenetre,(0,0,0),pos[0],pos[1])
def gen_y(car):
    if -1<car.orientation<181:
        y = car.pos[0] + car.vitesse*(1-car.orientation/90)
    else:
        y = car.pos[0] + car.vitesse*(1-(180-(car.orientation-180))/90)
    return y
def gen_x(car):
    if 0<=car.orientation<=90: x = car.pos[1]- car.vitesse*(car.orientation/90)
    elif 90<=car.orientation<=180: x = car.pos[1]-car.vitesse*(-((car.orientation-180)/90))
    elif 180<=car.orientation<=270: x = car.pos[1]+car.vitesse*((car.orientation-180)/90)
    else: x = car.pos[1]+ car.vitesse*(-((car.orientation-360)/90))
    return x

class Circuit:
    def __init__(self,file):
        self.file = file
        with open(file,"r") as circuit:
            self.fileContent = circuit.read().split("\n")
            self.didgets = []
            for x in self.fileContent:
                self.didgets.append(x.split(","))
        self.squareSize = 50
    def show(self):
        s = self.squareSize
        y = 0
        for line in self.didgets:
            x = 0
            for didget in line:
                if didget != "0":
                    if "1" not in didget: draw_line(([x+s,y],[x+s,y+s]))
                    if "2" not in didget: draw_line(([x,y+s],[x+s,y+s]))
                    if "3" not in didget: draw_line(([x+10,y],[x+10,y+s]))
                    if "4" not in didget: draw_line(([x,y+10],[x+s,y+10]))
                x+=50
            y+=50
    def get_square(self,car):
        column = int(car.pos[0] / self.squareSize)
        line = int(car.pos[1] / self.squareSize)
        return column, line
    
    def get_rest(self,car):
        x = (car.pos[0] % self.squareSize)
        y = (car.pos[1] % self.squareSize)
        return x, y
    def check_collision(self,car):
        column, line = self.get_square(car)
        x, y = self.get_rest(car)
        try:
            w = self.didgets[line][column]
        except: w ="0"
        if w != "0":
            if "1" not in self.didgets[line][column]: 
                if car.orientation<=90:
                    x += car.height*car.orientation/90
                    if car.lenght * sin(pi * (90 - car.orientation) / 180) > self.squareSize - x:
                        car.vitesse /= 2-(car.orientation) / 90
                        while car.lenght * sin(pi * (90 - car.orientation) / 180) > self.squareSize - x:
                            car.orientation += 1
                elif 270<=car.orientation:
                    x += car.height * (360-car.orientation)/90
                    if car.lenght * sin(pi*(car.orientation - 270)/180) > self.squareSize - x:
                        car.vitesse /= 1+((car.orientation - 270) / 90)
                        while car.lenght * sin(pi*(car.orientation - 270)/180) > self.squareSize - x:
                            car.orientation -= 1
                            
            if "2" not in self.didgets[line][column]:
                if car.orientation>=270:
                    y += car.height*(car.orientation - 270)/90
                    if car.lenght * sin(pi * (90 - (car.orientation-270)) / 180) > self.squareSize - y:
                        car.vitesse /= 1+(360-car.orientation)/90
                        while car.lenght * sin(pi * (90 - (car.orientation-270)) / 180) > self.squareSize - y:
                            car.orientation += 1
                elif 180<=car.orientation<=270:
                    y += car.height * (270 - car.orientation)/90
                    if car.lenght * sin(pi*(90-(270-car.orientation))/180) > self.squareSize - y:
                        car.vitesse/= 1 +(car.orientation-180)/90
                        while car.lenght * sin(pi*(90-(270-car.orientation))/180) > self.squareSize - y:
                            car.orientation -= 1
                            
            if "3" not in self.didgets[line][column]:
                if 180<=car.orientation<=270:
                    if x <= 10:
                        car.vitesse /= 2-(car.orientation - 180)/90
                        u = gen_y(car)
                        while u <= column * 50 + 9 and u <= car.pos[0]:
                            car.orientation += 1
                            u = gen_y(car)
                elif 90<=car.orientation<=180:
                    if x <= 10:
                        car.vitesse/= 1 +(car.orientation-90)/90
                        u = gen_y(car)
                        while u <= column * 50 + 9 and u <= car.pos[0]:
                            car.orientation -= 1
                            u = gen_y(car)
                    if car.pos[0] < column*50 +10:
                        car.pos[0] = column*50 + 10
            if "4" not in self.didgets[line][column]:
                if 90<=car.orientation<=180:
                    if y <= 10:
                        car.vitesse /= 2-(car.orientation - 90)/90
                        x = gen_x(car)
                        while x <= line * 50 + 9 and x <= car.pos[1]:
                            car.orientation += 1
                            x = gen_x(car)
                elif 0<=car.orientation<=90:
                    if y <= 10:
                        car.vitesse/= 1 +(car.orientation)/90
                        x = gen_x(car)
                        while x <= line * 50 + 9 and x <= car.pos[1]:
                            car.orientation -= 1
                            x = gen_x(car)
                    if car.pos[1] < line*50 +10:
                        car.pos[1] = line * 50 + 10
        elif w == "0":
            car.vitesse = 0
            if car.pos[1] < 650: car.pos[1] -=1
