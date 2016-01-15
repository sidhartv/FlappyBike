#Fall 2015: OOP and Animation - FlappyBird 
#Framework for FlappyBird by Rudina Morina :)
import random
from Tkinter import *
import serial
import math
import PIL
from PIL import Image


#########################################################################
#### Bird 
#########################################################################

class Bird(object):
    def __init__(self, x, y, size, canvasWidth, canvasHeight, color, bird):
        self.x = x
        self.y = y
        self.size = size
        self.velocity = 0
        self.gravity = 1
        self.canvasHeight = canvasHeight
        self.canvasWidth = canvasWidth
        self.color = color
        self.bird = bird
        self.birdWidth = bird.width()
        self.birdHeight = bird.height()
 

    def draw(self, canvas, timer):
        amplitude = 10
        period = 50 
        height = self.y + amplitude*math.sin(period*timer)
        canvas.create_image(self.x - self.birdWidth/2, 
            height - self.birdHeight/2, anchor = NW, image=self.bird)

    def move(self, x, slope, intercept):
        if(x <= 500):
            self.y = 0
        elif(x >= 1500):
            self.y = data.height
        else:
            self.y = intercept + slope*(x)
            


    def getLocation(self):
        return self.x, self.y

    def getSize(self):
        return self.size
    
    
#########################################################################
#### Obstacle
#########################################################################

class Obstacle(object):
    def __init__(self, gapSize, width, canvasWidth, canvasHeight, top, body):
        self.gapSize = gapSize
        self.width = width
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight
        self.y = random.randrange(gapSize, canvasHeight - gapSize)
        self.x = canvasWidth + gapSize
        self.speed = 10
        self.top = top
        self.body = body
        self.topWidth = top.width()
        self.topHeight = top.height()
        self.bodyWidth = body.width()
        self.bodyHeight = body.height()
        self.topRects = int(math.ceil((self.y - self.gapSize/2)/self.bodyHeight))
        self.bottomRects = int(math.ceil((self.y + self.gapSize/2)/self.bodyHeight))

        
    def draw(self, canvas):
        canvas.create_image(self.x - self.topWidth/2, 
            self.y - self.gapSize // 2 - self.topHeight, 
            anchor=NW, image=self.top)
        canvas.create_image(self.x - self.topWidth/2, 
            self.y + self.gapSize // 2, 
            anchor=NW, image=self.top)
        #draw top rectangles
        for i in xrange(self.topRects+1):
            canvas.create_image(self.x - self.bodyWidth/2, 
                self.y - self.gapSize/2 - self.topHeight - (i+1)*self.bodyHeight, 
                anchor = NW,
                image=self.body)
        for j in xrange(self.bottomRects+1):
            canvas.create_image(self.x - self.bodyWidth/2,
                self.y + self.gapSize/2 + self.topHeight+ j*self.bodyHeight,
                anchor = NW, image=self.body)
                                    
    def move(self):
        self.x -= self.speed

    def isColliding(self, birdX, birdY, birdWidth, birdHeight):
        birdWidth = (1.0/3)*birdWidth
        birdHeight = (1.0/3)*birdHeight
        birdCorners = [(birdX - birdWidth/2, birdY - birdHeight/2),
                    (birdX + birdWidth/2, birdY - birdHeight/2),
                    (birdX - birdWidth/2, birdY + birdHeight/2),
                    (birdX + birdWidth/2, birdY + birdHeight/2)]

        obstacleX1, obstacleY1 = (self.x - self.bodyWidth // 2, 
                                  self.y - self.gapSize // 2)
        obstacleX2, obstacleY2 = (self.x + self.bodyWidth // 2, 
                                 self.y + self.gapSize // 2)

        for (cornerX, cornerY) in birdCorners:
            if ((obstacleX1 <= cornerX <= obstacleX2) and 
                not (obstacleY1 <= cornerY <= obstacleY2)):
                return True
        return False

    def isOffScreen(self):
        if self.x <= -self.gapSize // 2:
            return True
        return False

###########################################################

def keyPressed(event, data):
    if (event.keysym == "Up"):
        data.omegaBike -= 50
    elif(event.keysym == "Down"):
        data.omegaBike += 50
    elif (event.keysym == "Left"):
        data.omegaFlap -= 50
    elif (event.keysym == "Right"):
        data.omegaFlap += 50
    elif(event.keysym == "r"):
        init(data)

def mousePressed(event, data):
    pass

def checkCollision(data):
    birdX1, birdY1 = data.bird1.getLocation()
    birdX2, birdY2 = data.bird2.getLocation()
    birdSize1 = data.bird1.getSize()
    birdSize2 = data.bird2.getSize()

    for obstacle in data.obstacles:
        if (obstacle.isColliding(birdX1, birdY1, data.bird1.birdWidth,
            data.bird1.birdHeight)):
            data.bird1Dead = True
            return
        elif(obstacle.isColliding(birdX2, birdY2, data.bird2.birdWidth,
            data.bird2.birdHeight)):
            data.bird2Dead = True
            return

def moveObstacles(data):
    for obstacle in data.obstacles:
        i = data.obstacles.index(obstacle)
        if(not(data.scoreList[i]) and 
            obstacle.x + obstacle.width/2 < data.bird1.x):
            data.scoreList[i] = True
            data.score += 1
            print("you did it!")
        if obstacle.isOffScreen():
            data.obstacles.pop(0)
            data.scoreList.pop(0)
        obstacle.move()


def makeNewObstacle(data):
    if (data.totalTime % data.obstacleFreq == 0):
        data.obstacles.append(Obstacle(data.gapSize, data.obstacleWidth, 
            data.width, data.height, data.top, data.body))
        data.scoreList.append(False)

def timerFired(data):
    #data.omega = data.ser.readline()
    #map the function to the height
    data.flapTimer += 1
    if(data.bird1Dead and data.bird2Dead):
        data.gameOver = True
    if(data.bird1Dead):
        if(data.bird1.y + data.bird1.birdHeight/2 < data.height):
            data.bird1.y += 25
    if(data.bird2Dead):
        if(data.bird2.y + data.bird2.birdHeight/2 < data.height):
            data.bird2.y += 25
    data.totalTime += data.timerDelay
    if (not data.gameOver):
        makeNewObstacle(data)
        data.bird1.move(data.omegaBike, data.slope, data.intercept)
        data.bird2.move(data.omegaFlap, data.slope, data.intercept)
        moveObstacles(data)
        checkCollision(data)

def redrawAll(canvas, data):
    canvas.create_image(0, -100, anchor = NW, image=data.backdrop)
    canvas.create_image(797, -100, anchor = NW, image=data.backdrop)
    if(not(data.bird1Dead)):
        data.bird1.draw(canvas, data.flapTimer)
    if(not(data.bird2Dead)):
        data.bird2.draw(canvas, data.flapTimer)
    for obstacle in data.obstacles:
        obstacle.draw(canvas)
    if(data.gameOver):
        
        canvas.create_image(data.width/2 - data.scoresign.width()/2
            - data.scoresign.width()/6, 
            data.height/2 - data.scoresign.height()/2, anchor = NW, 
            image=data.scoresign)
        canvas.create_image(data.width/2 - data.overImg.width()/2 -
            data.overImg.width()/6, -100,
            anchor=NW, image=data.overImg)
        data.bird1.draw(canvas, data.flapTimer)


def init(data):
    data.score = 0
    #data.ser = serial.Serial('/dev/cu.usbmodem1421', 115200)
    data.flapTimer = 0
    data.imagex = 0
    birdX1, birdY1 = data.width // 3, data.height // 2
    birdX2, birdY2 = data.width // 3, data.height // 4
    birdSize = data.height // 20
    data.bird1 = Bird(birdX1, birdY1, birdSize, data.width, data.height, 
        "red", data.Fabi)
    data.bird2 = Bird(birdX2, birdY2, birdSize, data.width, data.height,
     "blue", data.Fobi)
    data.bird1Dead = False
    data.bird2Dead = False
    data.input = 500
    data.omegaBike = 1000
    data.omegaFlap = 750
    x1 = 500
    x2 = 1500
    omegaRange = x2 - x1
    data.slope = float((data.height))/omegaRange
    data.intercept = -x1*data.slope


    data.obstacles = []
    data.scoreList = []
    data.obstacleFreq = 400
    data.obstacleWidth = data.width // 12 
    data.gapSize = data.height // 4

    data.totalTime = 0
    data.gameOver = False

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 5 # milliseconds
    
    # create the root and the canvas
    root = Tk()
    data.Fabi = PhotoImage(file="FlappyBirds/test_copy.gif")
    data.Fobi = PhotoImage(file="FlappyBirds/purplebird.gif")
    data.backdrop = PhotoImage(file="FlappyBirds/back.gif")
    data.overImg = PhotoImage(file="FlappyBirds/gover.gif")
    data.top = PhotoImage(file="FlappyPipes/top.gif")
    data.body = PhotoImage(file="FlappyPipes/body.gif")
    data.scoresign = PhotoImage(file="FlappyBirds/flap.gif")
    init(data)
    
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1600, 800)