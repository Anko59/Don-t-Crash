limit = 580
from car import *
from rnn import *
continuer = 1
circuit = Circuit("circuit.txt")        
pygame.display.flip()
"""skin,poid,vitesseMax,maniabilite,freins,acceleration"""
formula1 = car("formula1Skin.png",400,10,1,0.002,0.05) 
formula2 = car("formula2Skin.png",800,15,0.5,0.1,0.3)
formula3 = car("formula3Skin.png",200,7,2,2,0.5)
formula4 = car("formula4Skin.png",400,8,4.5, 0.1,0.3)
yolo = {K_1:formula1,K_2:formula2,K_3:formula3,K_4:formula4}
graphicObjects = []
reproducingPool = []
allKeys = []
class Graphics(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.name = "Thread"+str(randrange(100))
        self.turn  = True
    def run(self):
        while self.turn:
            time.sleep(0.01)
            fenetre.fill((255,255,255))
            try:
                for obj in graphicObjects: obj.show()
            except: print("OOOHHHH OOOHHHH OOOHHHH GOTAGAAAAA")
            pygame.display.flip()
        print("STOP")
graphics = Graphics()
graphics.start()

def copule(car1,car2):
    def pick():
        if randrange(2): return car1
        else: return car2
    k = {}
    rand = pick()
    for x in range(rand.counter):
        try:
            k[x] = pick().key[x]
        except: k[x] = rand.key[x]
    print(k.keys())
    return car(pick().skin,pick().poid,pick().vitesseMax,pick().maniabilite,pick().freins,pick().acceleration, pick().matricule, k)
        
def start(tcar):
    tcar.vitesse = 0
    tcar.orientation = 0
    tcar.inertie = 0
    tcar.pos = [10,20]
    tcar.pressedKeys = []
    tcar.timer = 0
    TIMER = 0
def chooseCar():
    formula1 = car("formula1Skin.png",400,10,1,0.002,0.05) 
    formula2 = car("formula2Skin.png",800,15,0.5,0.1,0.3)
    formula3 = car("formula3Skin.png",200,7,2,2,0.5)
    formula4 = car("formula4Skin.png",400,8,4.5, 0.1,0.3)
    yolo = {K_1:formula1,K_2:formula2,K_3:formula3,K_4:formula4}
    c = 1
    while c:
        for event in pygame.event.get():
            if event.type == KEYUP and event.key in yolo.keys():
                r = yolo[event.key]
                c = 0
    return r
            
def play(c, mode, graphic = True, maxTime = 15000):
    TIMER = 0
    start(c)
    print('YOOOO')
    print(c.pos)
    if graphic:
        graphicObjects.append(circuit)
        graphicObjects.append(c)
    def condition():
        if mode  == "AUTO": return ((c.pos[1] < 700 or not 390 < c.pos[0] < 500) and TIMER < maxTime)
        elif mode == "MANUAL": return (c.pos[1] < 700 or not 390 < c.pos[0] < 500)
        elif mode == "SHOW": return ((c.pos[1] < 700 or not 390 < c.pos[0] < 500) and TIMER < maxTime)
    while condition():
        if mode == "MANUAL":
            c.drive()
            time.sleep(.015)
        elif mode == "AUTO":
            for event in pygame.event.get(): pass
            c.autoDrive()
        elif mode == "SHOW":
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_q: break
            c.autoDrive()
            time.sleep(.025)
        c.move()
        circuit.check_collision(c)
        TIMER += 1
        c.timer+=1
        storeData(c, startPos, c.pressedKeys, TIMER)

    genDataset()
    evaluate(c)
    graphicObjects.remove(circuit)
    graphicObjects.remove(c)
    print(c)
    return TIMER

def multiPlay(cars, mods, maxTime, graphics = True):
    TIMER = 0
    if graphics:
        graphicObjects.append(circuit)
        for car in cars:
            start(car)
            graphicObjects.append(car)
    while TIMER < maxTime:
        a=0
        while a < len(cars):
            mode = mods[a]
            car = cars[a]
            if mode == "MANUAL":
                car.drive()
            elif mode == "AUTO" or mode == "SHOW":
                for event in pygame.event.get(): pass
                car.autoDrive()
            car.move()
            circuit.check_collision(car)
            car.timer += 1
            a+= 1
        TIMER += 1
        if "MANUAL" in mods or "SHOW" in mods:
            time.sleep(0.015)
    for car in cars:
        evaluate(car)
        graphicObjects.remove(car)
    graphicObjects.remove(circuit)
                
   
def evaluate(c):
    global bestScore
    if len(reproducingPool) > 15:
        for x in range(15):
            if c.score < reproducingPool[x].score:
                reproducingPool.append(c)
                smaller = reproducingPool[0]
                higher = reproducingPool[0]
                for x in reproducingPool:
                    if x.score > smaller.score: smaller = x
                    if x.score < higher.score: higher = x
                reproducingPool.remove(smaller)
                bestScore = higher
                break
    else:
        reproducingPool.append(c)
        higher = reproducingPool[0]
        for x in reproducingPool:
            if x.score < higher.score: higher = x
        bestScore = higher
        

def generateGeneration():
    ranCars = []
    for c in reproducingPool:
        for x in range(5):
            x = c.reproduce()
            y = 0
            while True:
                if y > 0:
                    print("ooo")
                x.modifyKey()
                x.setKey()
                if x.key not in allKeys:
                    allKeys.append(x.key)
                    break
                y+=1
                if y >= 100:
                    reproducingPool.remove(c)
                    break
            ranCars.append(x)
    return ranCars

def ovulateGeneration():
    ranCars = []
    for c in reproducingPool:
        for x in range(5):
            x = copule(c, reproducingPool[randrange(len(reproducingPool))])
            y = 0
            while True:
                if y > 0:
                    print("ooo")
                x.modifyKey()
                x.setKey()
                if x.key not in allKeys:
                    allKeys.append(x.key)
                    break
                y+=1
                if y >= 100:
                    reproducingPool.remove(c)
                    break
            ranCars.append(x)
    return ranCars
"""
def main():   """     
for x in range(1):
    for x in reproducingPool: reproducingPool.remove(x)
    choosedCar = chooseCar()
    bestScore = choosedCar
    TIMER = play(choosedCar, "MANUAL")
    ranCars  = generateGeneration()
    for x in range(100):
        for newCar in ranCars:
            print()
            play(newCar,"AUTO", maxTime = bestScore.score + 100)
        ranCars = generateGeneration()
    print(bestScore)
    #appendFile("optimizedCars.txt",bestScore)
    continuer = 0
    #input("Ready ?")
for x in reproducingPool: reproducingPool.remove(x)
bestCars = [bestScore]
for c in bestCars:
    c.skin = formula4.skin
    reproducingPool.append(c)
for x in range(50):
    ranCars = ovulateGeneration()
    for newCar in ranCars:
        print()
        play(newCar,"AUTO", maxTime = bestScore.score + 200)
print(bestCars)
shows = []


for x in bestCars:
    shows.append("SHOW")
"""
with open('data.txt','w') as file:
    file.write(dataset.convert())
"""
while 1:
    choosedCar.setKey()
    print("WHATTTT ?????")
    multiPlay(bestCars, shows,800)
graphics.turn = False
pygame.display.quit()
"""
if __name__ == '__main__':
    main()"""
    
