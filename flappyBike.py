#Fall 2015: OOP and Animation - FlappyBird 
import random
from Tkinter import *
import serial



#########################################################################
#### Bird 
#########################################################################

class Bird(object):
    def __init__(self, x, y, size, canvasWidth, canvasHeight, color):
        self.x = x
        self.y = y
        self.size = size
        self.velocity = 0
        self.gravity = 1
        self.canvasHeight = canvasHeight
        self.canvasWidth = canvasWidth
        self.color = color
        
    def draw(self, canvas):
        canvas.create_oval(self.x - self.size, self.y - self.size, 
            self.x + self.size, self.y + self.size, fill = self.color)
    
    def onThrust(self):
        self.velocity = -10

    def move(self):
        self.velocity += self.gravity
        self.y = self.y + self.velocity
        if (self.y + self.size > self.canvasHeight):
            self.y = self.canvasHeight - self.size
        elif (self.y - self.size < 0):
            self.y = self.size

    def getLocation(self):
        return self.x, self.y

    def getSize(self):
        return self.size
    
    
#########################################################################
#### Obstacle
#########################################################################

class Obstacle(object):
    def __init__(self, gapSize, width, canvasWidth, canvasHeight):
        self.gapSize = gapSize
        self.width = width
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight
        self.y = random.randrange(gapSize, canvasHeight - gapSize)
        self.x = canvasWidth + gapSize
        self.speed = 5
        
    def draw(self, canvas):
        canvas.create_rectangle(self.x - self.width // 2, 0, 
            self.x + self.width // 2, self.y - self.gapSize // 2, fill="green")

        canvas.create_rectangle(self.x - self.width // 2, 
            self.y + self.gapSize // 2, self.x + self.width // 2, 
            self.canvasHeight, fill="green")
                                    
    def move(self):
        self.x -= self.speed

    def isColliding(self, birdX, birdY, birdSize):
        birdCorners = [(birdX - birdSize, birdY - birdSize),
                    (birdX + birdSize, birdY - birdSize),
                    (birdX - birdSize, birdY + birdSize),
                    (birdX + birdSize, birdY + birdSize)]

        obstacleX1, obstacleY1 = (self.x - self.width // 2, 
                                  self.y - self.gapSize // 2)
        obstacleX2, obstacleY2 = (self.x + self.width // 2, 
                                 self.y + self.gapSize // 2)

        for (cornerX, cornerY) in birdCorners:
            if ((obstacleX1 <= cornerX <= obstacleX2) and 
                not (obstacleY1 <= cornerY <= obstacleY2)):
                return True
        return False

    def isOffScreen(self):
        if self.x <= self.gapSize // 2:
            return True
        return False

###########################################################

def keyPressed(event, data):
    if (event.keysym == "Up"):
        data.omega += 10
        #data.bird1.onThrust()
    elif(event.keysym == "Down"):
        data.omega -= 10
    elif (event.keysym == "b"):
        data.bird2.onThrust()
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
        if (obstacle.isColliding(birdX1, birdY1, birdSize1)):
            data.bird1Dead = True
            return
        elif(obstacle.isColliding(birdX2, birdY2, birdSize2)):
            data.bird2Dead = True
            return

def moveObstacles(data):
    for obstacle in data.obstacles:
        if obstacle.isOffScreen():
            data.obstacles.remove(obstacle)
    for obstacle in data.obstacles:
        obstacle.move()

def makeNewObstacle(data):
    if (data.totalTime % data.obstacleFreq == 0):
        data.obstacles.append(Obstacle(data.gapSize, data.obstacleWidth, 
            data.width, data.height))

def timerFired(data):
    #data.omega = data.ser.readline()
    #map the function to the height
    if(data.omega <= 500):
        data.bird1.y = 0
    elif(data.omega >= 1500):
        data.bird1.y = data.height
    else:
        print("middle")
        data.bird1.y = data.intercept + data.slope*(data.omega)
        print(data.bird1.y)

    if(data.bird1Dead and data.bird2Dead):
        data.gameOver = True
    data.totalTime += data.timerDelay
    if (not data.gameOver):
        makeNewObstacle(data)
        #data.bird1.move()
        data.bird2.move()
        moveObstacles(data)
        checkCollision(data)

def redrawAll(canvas, data):
    if (not data.gameOver):
        if(not(data.bird1Dead)):
            data.bird1.draw(canvas)
        if(not(data.bird2Dead)):
            data.bird2.draw(canvas)
        for obstacle in data.obstacles:
            obstacle.draw(canvas)
    else:
        canvas.create_rectangle(0, 0, data.width, data.height, fill="yellow")


def init(data):
    #data.ser = serial.Serial('/dev/cu.usbmodem1421', 115200)
    birdX1, birdY1 = data.width // 3, data.height // 2
    birdX2, birdY2 = data.width // 3, data.height // 4
    birdSize = data.height // 20
    data.bird1 = Bird(birdX1, birdY1, birdSize, data.width, data.height, "red")
    data.bird2 = Bird(birdX2, birdY2, birdSize, data.width, data.height, "blue")
    data.bird1Dead = False
    data.bird2Dead = False
    data.input = 500
    data.omega = 1000
    x1 = 500
    x2 = 1500
    omegaRange = x2 - x1
    data.slope = float((data.height))/omegaRange
    data.intercept = -x1*data.slope


    data.obstacles = []
    data.obstacleFreq = 800
    data.obstacleWidth = data.width // 6 
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
    data.timerDelay = 10 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
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

run(800, 800)