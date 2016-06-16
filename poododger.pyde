add_library('sound')
add_library('minim')

import os
import time
import random

path = os.getcwd()

class Game:

    def __init__(self, width, height, ground):
        self.width = width
        self.height = height
        self.ground = ground
        ### player init: x_pos, ground, hygienelvl, radius ###
        self.player = Player(self.width / 2, ground, 3, 20)
        self.fallAcceleration = 0.2
        self.poopAcceleration = 0.4
        self.fallObjectList = []
        self.fallObjectGenFreq = random.randint(50, 200)
        self.poopGenFreq = 2
        self.poopCount = 0
        self.score = 0
        self.frame = 0
        self.totalFrame = 0
        self.mode = 'main'
        self.music1 = None
        self.music2 = None
        self.music3 = None
        self.highscoreFile = open(path + '/highscore.txt', 'a')
        self.highscoreFile.close()
        self.highscoreList = []
        self.highscoreFile = open(path + '/highscore.txt', 'r')
        for line in self.highscoreFile:
            # [['simon', '2131'], ['asdf','124']]
            self.highscoreList.append(line.strip().split(','))
        self.highscoreFile.close()
        print self.highscoreList
        self.nametxt = ''
        self.frameCounter = 0
        self.imglist = []
        self.debugMode = False
        
        self.imglist.append(loadImage(path + '/poop.png'))  # 0
        self.imglist.append(loadImage(path + '/player.png'))  # 1
        self.imglist.append(loadImage(path + '/rainbow.png'))  # 2
        self.imglist.append(loadImage(path + '/shampoo.png'))  # 3
        self.imglist.append(loadImage(path + '/umbrella.png'))  # 4
        self.imglist.append(loadImage(path + '/clock.png'))  # 5
        self.imglist.append(loadImage(path + '/start.png'))  # 6
        self.imglist.append(loadImage(path + '/dead.png'))  # 7
        self.imglist.append(loadImage(path + '/instructions.png'))  # 8
        # self.imglist.append(loadImage(path+'/background.png')) #9
        
    def objectGen(self):
        # fallObject(x, y, r)
        if self.totalFrame % self.poopGenFreq == 0:
            self.fallObjectList.append(
                Poop(random.randint(0, self.width), 0, 12))
            if int(log(90000 / self.totalFrame)) > 3:
                self.poopGenFreq = int(log(90000 / self.totalFrame))
            else:
                self.poopGenFreq = random.randint(1, 3)
        if self.totalFrame % self.fallObjectGenFreq == 0:
            self.fallObjectList.append(
                Shampoo(random.randint(0, self.width), 0, 12))
            self.fallObjectList.append(
                Umbrella(random.randint(0, self.width), 0, 12))
            if int(log(90000 / self.totalFrame) * 40) > 200:
                self.fallObjectGenFreq = int(log(90000 / self.totalFrame) * 40)
            else:
                self.fallObjectGenFreq = random.randint(50, 200)

    def display(self):
        # image(game.imglist[9], 0, 0, game.width, game.height)
        # frame becomes a number between 0 and 1.
        self.frame = (self.frame + 0.1) % 2
        if self.mode == 'main':
            if self.debugMode:
                ellipse(200, 200, 20, 20)
            self.player.update()
            self.player.display()
            for fallObject in self.fallObjectList:
                fallObject.update()
                fallObject.display()
            image(self.imglist[8], self.width / 2 - 225,
                  self.height / 2 - 160, 450, 246)
            if self.width / 2 - 100 < mouseX < self.width / 2 + 100 and self.height / 2 + 100 < mouseY < self.height / 2 + 160:
                image(self.imglist[6], self.width / 2 - 100,
                      self.height / 2 + 100, 200, 60, 0, 0, 200, 60)
            else:
                image(self.imglist[6], self.width / 2 - 100,
                      self.height / 2 + 100, 200, 60, 0, 60, 200, 120)
            
        elif self.mode == 'gameplay':
            textSize(30)
            fill(0)
            text('Poops dodged: ' + str(game.poopCount) + '\n' +
                 'Hygiene Level: ' + str(game.player.hygienelvl), game.width - 320, 30)
            game.totalFrame += 1
            self.objectGen()
            self.player.update()
            self.player.display()
            for fallObject in self.fallObjectList:
                fallObject.update()
                fallObject.display()
        elif self.mode == 'gameover':
            for fallObject in self.fallObjectList:
                fallObject.display()
            self.player.display()
            textSize(30)
            fill(0)
            text('Poops dodged: ' + str(game.poopCount) + '\n' + '\n' +
                 'submit', game.width / 2 - 150, game.height / 2 - 100)
            textSize(30)
            fill(0)
            text(self.nametxt, self.width / 2 - 50, self.height / 2 - 50)
        elif self.mode == 'highscore':
            textSize(30)
            fill(0)
            for i in range(len(self.highscoreList)):
                text(self.highscoreList[i][
                     0] + ' : ' + self.highscoreList[i][1], self.width / 2 - 100, 30 + 40 * i)
            

class Player:

    def __init__(self, x_pos, ground, hygienelvl, radius):
        self.x_pos = x_pos
        self.radius = radius
        self.vx = 0
        self.ground = ground
        self.hygienelvl = hygienelvl
        self.mode = 'godMode'
        self.keyInput = {'LEFT': False, 'RIGHT': False, 'DOWN': False}

    def update(self):
        if self.keyInput['LEFT']:
            if self.mode == 'godMode':
                self.vx = -5
            elif self.mode != 'godMode':
                self.vx = -7
        elif self.keyInput['RIGHT']:
            if self.mode == 'godMode':
                self.vx = 5
            elif self.mode != 'godMode':
                self.vx = 7
        elif game.mode == 'main' and self.keyInput['DOWN']:
            game.fallObjectList.append(
                Poop(random.randint(0, game.width), 0, 20))
        else:
            self.vx = 0

        self.x_pos += self.vx
        if self.x_pos < 0:
            self.x_pos = 0
        elif self.x_pos > game.width:
            self.x_pos = game.width

        if game.frameCounter > 180 and self.mode == 'clockMode':
            self.mode = None
            game.poopAcceleration = 0.4
        if game.frameCounter > 180 and self.mode == 'umbrellaMode':
            if game.debugMode:
                print('reset umbrellamode1')
            self.mode = None
            game.music2.stop()
            game.music1.loop()
        if timer.queryGodTime() > 10 and self.mode == 'godMode' and game.mode == 'gameplay':
            if game.debugMode:
                print('reset umbrellamode2')
            self.mode = None
            timer.godTime = 0

    def display(self):
        
        stroke(0)
        noFill()
        if game.debugMode:
            ellipse(self.x_pos, self.ground, self.radius * 2, self.radius * 2)
        
        # int(frame) makes frame value (=indext of imglist) either 0 or 1
        if game.mode != 'gameover':
            if self.mode == 'godMode' or self.mode == 'umbrellaMode':
                if self.vx == 0:
                    image(game.imglist[2], self.x_pos - self.radius, self.ground - self.radius, self.radius *
                          2, self.radius * 2, 28 * int(game.frame), 48 * 0, 28 * (1 + int(game.frame)), 48 * 1)
                elif self.vx < 0:
                    image(game.imglist[2], self.x_pos - self.radius, self.ground - self.radius, self.radius *
                          2, self.radius * 2, 28 * int(game.frame), 48 * 1, 28 * (1 + int(game.frame)), 48 * 2)
                elif self.vx > 0:
                    image(game.imglist[2], self.x_pos - self.radius, self.ground - self.radius, self.radius *
                          2, self.radius * 2, 28 * int(game.frame), 48 * 2, 28 * (1 + int(game.frame)), 48 * 3)
            elif self.mode != 'godMode' or self.mode != 'umbrellaMode':
                if self.vx == 0:
                    image(game.imglist[1], self.x_pos - self.radius, self.ground - self.radius, self.radius *
                          2, self.radius * 2, 28 * int(game.frame), 48 * 0, 28 * (1 + int(game.frame)), 48 * 1)
                    # image(self.imglist[int(game.frame)], self.x_pos -
                    # self.radius, self.ground - self.radius, self.radius*2,
                    # self.radius*2, 0, 0, 28, 44)
                elif self.vx < 0:
                    image(game.imglist[1], self.x_pos - self.radius, self.ground - self.radius, self.radius *
                          2, self.radius * 2, 28 * int(game.frame), 48 * 1, 28 * (1 + int(game.frame)), 48 * 2)
                    # image(self.imglist[2+int(game.frame)], self.x_pos -
                    # self.radius, self.ground - self.radius, self.radius*2,
                    # self.radius*2, 0, 0, 28, 44)
                elif self.vx > 0:
                    image(game.imglist[1], self.x_pos - self.radius, self.ground - self.radius, self.radius *
                          2, self.radius * 2, 28 * int(game.frame), 48 * 2, 28 * (1 + int(game.frame)), 48 * 3)
                    # image(self.imglist[4+int(game.frame)], self.x_pos -
                    # self.radius, self.ground - self.radius, self.radius*2,
                    # self.radius*2, 0, 0, 28, 44)
        elif game.mode == 'gameover':
            image(game.imglist[7], self.x_pos - self.radius * 1.5,
                  self.ground - self.radius, self.radius * 3, self.radius * 2)


class FallObject():

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.g = game.ground
        self.v = 0
    
    def update(self):
        self.y += self.v
        self.v += game.fallAcceleration
        if self.y > self.g:
            game.fallObjectList.remove(self)
        self.hitPlayer()
        
    def display(self):
        stroke(0)
        noFill()
        if game.debugMode:
            ellipse(self.x, self.y, self.r * 2, self.r * 2)

    def hitPlayer(self):
        pass
        

class Poop(FallObject):

    def __init__(self, x, y, r):
        FallObject.__init__(self, x, y, r)
        self.v = 1
    
    def update(self):
        self.y += self.v
        self.v += game.poopAcceleration
        if self.y > self.g:
            game.fallObjectList.remove(self)
            game.poopCount += 1
            
        self.hitPlayer()

    def hitPlayer(self):
        if ((self.x - game.player.x_pos) ** 2 + (self.y - (game.player.ground - game.player.radius)) ** 2) ** 0.5 < self.r + game.player.radius:
            if not (game.player.mode == 'godMode' or game.player.mode == 'umbrellaMode'):
                if game.debugMode:
                    print('poo!')
                game.fallObjectList.remove(self)
                if game.player.hygienelvl > 1:
                    game.player.hygienelvl -= 1
                    game.player.mode = 'godMode'
                    timer.startGodTime()

                elif game.player.hygienelvl == 1:
                    game.music1.pause()
                    game.player.hygienelvl -= 1
                    if game.debugMode:
                        print('gameover')
                    game.mode = 'gameover'
            elif game.player.mode == 'godMode' or game.player.mode == 'umbrellaMode':
                pass
                    
    def display(self):
        FallObject.display(self)
        image(game.imglist[0], self.x - self.r, self.y -
              self.r, self.r * 2, self.r * 2, 0, 0, 40, 40)
                
class Shampoo(FallObject):

    def __init__(self, x, y, r):
        FallObject. __init__(self, x, y, r)
      
    def hitPlayer(self):
        if game.player.mode != 'umbrellaMode' and game.player.mode != 'clockMode':
            if ((self.x - game.player.x_pos) ** 2 + (self.y - (game.player.ground - game.player.radius)) ** 2) ** 0.5 < self.r + game.player.radius:
                game.fallObjectList.remove(self)
                if game.player.hygienelvl < 3:
                    game.player.hygienelvl += 1
                    if game.debugMode:
                        print('shampoo!')
    
    def display(self):
        FallObject.display(self)
        image(game.imglist[3], self.x - self.r, self.y -
              self.r, self.r * 2, self.r * 2, 0, 0, 50, 50)
    # def display
        # 50x50

class Umbrella(FallObject):

    def __init__(self, x, y, r):
        FallObject. __init__(self, x, y, r)
    
    def hitPlayer(self):
        if game.player.mode != 'umbrellaMode' and game.player.mode != 'clockMode':
            if ((self.x - game.player.x_pos) ** 2 + (self.y - (game.player.ground - game.player.radius)) ** 2) ** 0.5 < self.r + game.player.radius:
                game.fallObjectList.remove(self)
                if game.debugMode:
                    print('umbrella!')
                game.frameCounter = 0
                game.player.mode = 'umbrellaMode'
                game.music1.pause()
                game.music2 = SoundFile(this, path + '/godMode.mp3')
                game.music2.play()
                
    def display(self):
        FallObject.display(self)
        image(game.imglist[4], self.x - self.r, self.y -
              self.r, self.r * 2, self.r * 2, 0, 0, 50, 50)
               
    
class Clock(FallObject):

    def __init__(self, x, y, r):
        FallObject. __init__(self, x, y, r)

    def hitPlayer(self):
        if game.player.mode != 'umbrellaMode' and game.player.mode != 'clockMode':
            if ((self.x - game.player.x_pos) ** 2 + (self.y - (game.player.ground - game.player.radius)) ** 2) ** 0.5 < self.r + game.player.radius:
                game.fallObjectList.remove(self)
                game.frameCounter = 0
                game.player.mode = 'clockMode'
                game.poopAcceleration = 0

    def display(self):
        FallObject.display(self)
        image(game.imglist[5], self.x - self.r, self.y -
              self.r, self.r * 2, self.r * 2, 0, 0, 40, 45)


class Timer():

    def __init__(self):
        self.startTime = 0
        self.godTime = 0

    def start(self):
        # starts the timer, starts when 'gamestart' button pressed'
        self.startTime = int(time.time())

    def query(self):
        # returns how many 0.1 seconds have past since start
        return int(time.time() * 10 - self.startTime * 10)

    def startGodTime(self):
        self.godTime = int(time.time())

    def queryGodTime(self):
        return int(time.time() * 10 - self.godTime * 10)
     
        
def keyPressed():
    if game.mode != 'gameover':
        if keyCode == LEFT:
            game.player.keyInput['LEFT'] = True
        elif keyCode == RIGHT:
            game.player.keyInput['RIGHT'] = True
        elif keyCode == DOWN:
            game.player.keyInput['DOWN'] = True
    else:
        if len(game.nametxt) > 0:
            if keyCode == 8:  # BACKSPACE
                game.nametxt = game.nametxt[:len(game.nametxt) - 1]
        if len(game.nametxt) < 4:
            if str(key).isalpha():
                game.nametxt = game.nametxt + str(key).upper()
            # elif isinstance(key, int):
            #   game.nametxt += str(key)
        if key == ENTER or key == RETURN:
            if len(game.highscoreList) > 0:
                for i in range(len(game.highscoreList)):
                    if i == len(game.highscoreList)-1:
                        game.highscoreList.append([game.nametxt, str(game.poopCount)])
                    elif game.poopCount > int(game.highscoreList[i][1]):
                        game.highscoreList.insert(i, [game.nametxt, str(game.poopCount)])
                        break
            elif len(game.highscoreList) == 0:
                game.highscoreList.append([game.nametxt, str(game.poopCount)])
                                                                            
            game.highscoreFile = open(path+'/highscore.txt','w')
            for recordList in game.highscoreList:
                game.highscoreFile.write(recordList[0]+','+recordList[1]+'\n')
            game.highscoreFile.close()
            game.mode = 'highscore'
            
     
def keyReleased():
    if keyCode == LEFT:
        game.player.keyInput['LEFT'] = False
        if game.debugMode:
             print('LEFT')
    elif keyCode == RIGHT:
        game.player.keyInput['RIGHT'] = False
    elif keyCode == DOWN:
        game.player.keyInput['DOWN'] = False

def mouseClicked():
    if game.mode == 'main' and game.width/2 - 100 < mouseX < game.width/2 +100 and game.height/2 + 100 < mouseY < game.height/2 + 160:
        game.mode = 'gameplay'
        game.player.mode = None
        game.poopCount = 0
        game.player.x_pos = game.width/2
        timer.start()
        minim = Minim(this)
        game.music1 = minim.loadFile('background.mp3', 2048)
       # game.music1.amp(0.1)
        game.music1.loop()
    elif game.mode == 'gameover' and game.width/2 - 150 < mouseX < game.width/2 and game.height/2 - 60 < mouseY < game.height/2 -20:
        #[['simon', '2131'], ['asdf','124']]
        if len(game.highscoreList) > 0:
            for i in range(len(game.highscoreList)):
                if i == len(game.highscoreList)-1:
                    game.highscoreList.append([game.nametxt, str(game.poopCount)])
                elif game.poopCount > int(game.highscoreList[i][1]):
                    game.highscoreList.insert(i, [game.nametxt, str(game.poopCount)])
                    break
        elif len(game.highscoreList) == 0:
            game.highscoreList.append([game.nametxt, str(game.poopCount)])
                                                                        
        game.highscoreFile = open(path+'/highscore.txt','w')
        for recordList in game.highscoreList:
            game.highscoreFile.write(recordList[0]+','+recordList[1]+'\n')
        game.highscoreFile.close()
        game.mode = 'highscore'
            
    elif game.mode == 'highscore':
        game.mode = 'gameplay'
        game.totalFrame = 0
        timer.start()
        game.music1.loop()
        game.fallObjectList = []
        game.poopCount = 0
        game.player.x_pos = game.width/2
        game.player.hygienelvl = 3
        game.player.mode = None
        

#     if gamestart pressed then chagne mode and start timer 

                                                                    
   
        

game = Game(1200,600,550)
timer = Timer()

def setup():
    background(255)
    size(game.width,game.height)
    

def draw():
    background(255)
    game.display()
    
    if game.player.mode == 'umbrellaMode' or game.player.mode == 'clockMode':
        game.frameCounter += 1
    if game.debugMode:
        print('poogcount', game.poopCount, 'time.query', timer.query(), 'frame', game.totalFrame, 'frameCounter', game.frameCounter, 'mode', game.player.mode, 'HP', game.player.hygienelvl)