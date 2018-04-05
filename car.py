from circuit import *
import pickle
cars = []
class Event:
    def __init__(self,event):
        self.type = int(event.type)
        self.key = int(event.key)
def writeFile(fichier,contenu):
    try:
        with open (fichier,"wb") as save:
            pass
    except:
        mon_fichier = open(fichier,"w")
        mon_fichier.close()
        print(fichier+"n'etait pas exsistant, il a ete cree")
    with open (fichier,"wb") as save:
        mon_pickler = pickle.Pickler(save)
        mon_pickler.dump(contenu)
def readFile(fichier):
    try:
        with open (fichier,"rb") as save:
            pass
    except:
        mon_fichier = open(fichier,"w")
        mon_fichier.close()
        print(fichier+"n'etait pas exsistant, il a ete cree")
    with open(fichier,"rb") as save:
        mon_depickler = pickle.Unpickler(save)
        try:
            datas=mon_depickler.load()
        except:
            ecrire(fichier,[])
            print(fichier+" etait vide")
            datas = []
    return datas
def appendFile(fichier,contenu):
    try:
        data = readFile(fichier)
    except: data = []
    data.append(contenu)
    writeFile(fichier,data)
class car:
        number = 0
        def __init__(self,skin,poid,vitesseMax,maniabilite,freins,acceleration, matricule = 0, key = {}):
            try:    
                self.skin = pygame.image.load(skin).convert()
            except:
                self.skin = skin
            self.skin.set_colorkey((255,255,255))
            self.lenght = self.skin.get_width()
            self.height = self.skin.get_height()
            self.poid = poid
            self.vitesseMax = vitesseMax
            self.maniabilite = maniabilite
            self.freins =freins
            self.acceleration = acceleration
            self.vitesse = 0
            self.inertie = 0
            self.pos = [400,200]
            self.orientation = 0
            self.pressedKeys=[]
            self.timer = 0
            self.score = 0
            self.counter = len(key.keys())
            self.k = key
            self.key = {}
            self.readKey = {}
            self.matricule = str(matricule) + " " + str(car.number)
            car.number += 1
            cars.append(self)
        def move(self):
                self.orientation = round(self.orientation,3)
                if -1<self.orientation<181:
                        self.pos[0] += self.vitesse*(1-self.orientation/90)
        		
                else:
                        self.pos[0] += self.vitesse*(1-(180-(self.orientation-180))/90)
                        
                if 0<=self.orientation<=90: self.pos[1]-= self.vitesse*(self.orientation/90)
                elif 90<=self.orientation<=180: self.pos[1]-=self.vitesse*(-((self.orientation-180)/90))
                elif 180<=self.orientation<=270: self.pos[1]+=self.vitesse*((self.orientation-180)/90)
                
                else: self.pos[1]+= self.vitesse*(-((self.orientation-360)/90))
                self.vitesse -= self.vitesse/self.poid
                self.vitesse = round(self.vitesse,5)
                if self.pos[0]>1400:self.pos[0]=1400
                elif self.pos[0]<0:self.pos[0]=0
                if self.pos[1]>700:self.pos[1]=700
                elif self.pos[1]<0:self.pos[1]=0
                
        def accelere(self):
        	self.vitesse += self.acceleration
        	if self.vitesse>self.vitesseMax: self.vitesse = self.vitesseMax
        def freinage(self):
        	self.vitesse -= self.freins
        	if self.vitesse<0:self.vitesse=0
        def show(self):
            fenetre.blit(pygame.transform.rotate(self.skin,self.orientation),self.pos)
            """pygame.draw.circle(fenetre, (0,0,0), [int(self.pos[0]), int(self.pos[1])], 10, 1)"""
        def setKey(self):
            a = 0
            timer = 0
            while a < self.counter:
                timer += self.key[a][0]
                self.readKey[timer] = self.key[a][1]
                a += 1
            self.timer = 0
        def modifyKey(self):
            if self.key != {}:
                self.k = self.key
            for a in range(len(self.k.keys())):
                x = 0
                if not randrange(30):
                    x += 3**(500/(6*(randrange(300)+23)))
                if not randrange(30):
                    x -= 3**(500/(6*(randrange(300)+23)))
                try:
                    self.key[a] = [self.k[a][0] + int(x), self.k[a][1]]
                except:
                    print(self.k.keys())
                    print(self.k[a])
            if not randrange(20):
                nbr = randrange(self.counter)
                if self.key[nbr][0] <= 0:
                    time = 0
                else: time = randrange(self.key[nbr][0])
                event = self.key[randrange(self.counter)][1]
                self.key[nbr][0] -= time
                a = int(self.counter)-1
                while a >= 0:
                    if a >= nbr: self.key[a+1] = self.k[a]
                    a -= 1
                self.key[nbr]= [time,event]
                self.counter += 1
                self.print_liste()
            if not randrange(20):
                nbr = randrange(self.counter-1)
                for a in range(self.counter-1):
                    if a > nbr: self.key[a-1] = self.k[a]
                del self.key[self.counter-1]
                self.counter -= 1
                
        def print_liste(self):
            liste = [self.key[x][0] for x in self.key.keys()]
            print(liste)
            print()
        def __str__(self):
            txt = {K_d:"D",K_a:"Q",K_w:"Z",K_s:"S",K_l:"L",K_p:"P"}
            dic = {}
            for x in self.key.keys():
                try:
                    dic[x] = [self.key[x][0],txt[self.key[x][1].key]]
                except:pass

            return str(dic)+"\n"+str(self.matricule)+"\n"+str(self.score)
        def autoDrive(self):
            self.score += 1
            if self.timer in self.readKey.keys():
                event = self.readKey[self.timer]
                if event.type == KEYDOWN:
                    if event.key == K_d: self.pressedKeys.append("D")
                    elif event.key == K_a: self.pressedKeys.append("A")
                    elif event.key == K_w: self.pressedKeys.append("W")
                    elif event.key == K_s: self.pressedKeys.append("S")
                    elif event.key == K_l: self.pressedKeys.append("L")
                    elif event.key == K_p: self.pressedKeys.append("P")
                    elif event.key == K_q: self.pressedKeys.append("Q")
                elif event.type == KEYUP:
                    try:
                        if event.key == K_d: self.pressedKeys.remove("D")
                        elif event.key == K_a: self.pressedKeys.remove("A")
                        elif event.key == K_w: self.pressedKeys.remove("W")
                        elif event.key == K_s: self.pressedKeys.remove("S")
                        elif event.key == K_l: self.pressedKeys.remove("L")
                        elif event.key == K_p: self.pressedKeys.remove("P")
                        elif event.key == K_q: self.pressedKeys.remove("Q")
                    except:pass
            for key in self.pressedKeys:
                if 0<=self.orientation<=180:
                    if key == "D": self.orientation -= self.maniabilite 
                    elif key == "A": self.orientation += self.maniabilite
                else:
                    if key == "D": self.orientation += self.maniabilite
                    elif key == "A": self.orientation -= self.maniabilite
                if 90<=self.orientation<=270:
                    if key == "W": self.orientation -= self.maniabilite
                    elif key == "S": self.orientation += self.maniabilite
                else:
                    if key == "W": self.orientation += self.maniabilite
                    elif key == "S": self.orientation -= self.maniabilite
                if key == "P":self.accelere()
                elif key == "L":self.freinage()
            if self.orientation>360:self.orientation-=360
            elif self.orientation<0: self.orientation+=360
                
        def drive(self):
            self.score += 1
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self.key[self.counter] = [self.timer, Event(event)]
                    self.timer = 0
                    self.counter += 1
                    if event.key == K_d: self.pressedKeys.append("D")
                    elif event.key == K_a: self.pressedKeys.append("A")
                    elif event.key == K_w: self.pressedKeys.append("W")
                    elif event.key == K_s: self.pressedKeys.append("S")
                    elif event.key == K_l: self.pressedKeys.append("L")
                    elif event.key == K_p: self.pressedKeys.append("P")
                    elif event.key == K_q: self.pressedKeys.append("Q")
                elif event.type == KEYUP:
                    self.key[self.counter] = [self.timer, Event(event)]
                    self.timer = 0
                    self.counter += 1
                    try:
                        if event.key == K_d: self.pressedKeys.remove("D")
                        elif event.key == K_a: self.pressedKeys.remove("A")
                        elif event.key == K_w: self.pressedKeys.remove("W")
                        elif event.key == K_s: self.pressedKeys.remove("S")
                        elif event.key == K_l: self.pressedKeys.remove("L")
                        elif event.key == K_p: self.pressedKeys.remove("P")
                        elif event.key == K_q: self.pressedKeys.remove("Q")
                    except:pass
            for key in self.pressedKeys:
                if 0<=self.orientation<=180:
                        if key == "D": self.orientation -= self.maniabilite 
                        elif key == "A": self.orientation += self.maniabilite
                else:
                        if key == "D": self.orientation += self.maniabilite
                        elif key == "A": self.orientation -= self.maniabilite
                if 90<=self.orientation<=270:
                        if key == "W": self.orientation -= self.maniabilite
                        elif key == "S": self.orientation += self.maniabilite
                else:
                        if key == "W": self.orientation += self.maniabilite
                        elif key == "S": self.orientation -= self.maniabilite
                if key == "P":self.accelere()
                elif key == "L":self.freinage()
            if self.orientation>360:self.orientation-=360
            elif self.orientation<0: self.orientation+=360
        def reproduce(self):
            return car(self.skin,self.poid,self.vitesseMax,self.maniabilite,self.freins,self.acceleration, self.matricule, self.key)

                
