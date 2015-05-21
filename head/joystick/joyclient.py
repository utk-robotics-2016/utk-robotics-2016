import math
import sys
import pygame

import Pyro.core

import joy

SERV_URL = "PYROLOC://localhost:7766/joyserver"
RATE = 10
if len(sys.argv) > 1 and sys.argv[1] == 'remote':
    SERV_URL = "PYROLOC://utkieee.nomads.utk.edu:7766/joyserver"
    RATE = 5

class Main:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 450
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))

        # you have to change the URI below to match your own host/port.
        self.joyserver = Pyro.core.getProxyForURI(SERV_URL)

        self.objects = []

    def setupGame(self):
        self.clock = pygame.time.Clock()
        self.FPS = RATE
        self.joy = joy.Joystick()

        self.objects.append(self.joy)

    def runGame(self):
        self.gameRunning = 1

        while self.gameRunning:
            self.getInput()
            self.compute()
            self.draw()
            self.clock.tick(self.FPS)

    def getInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameRunning = 0

        
        pygame.display.set_caption(str(self.joy.x) + ', ' + str(self.joy.y) + ', ' + str(self.joy.rad))

    def draw(self):
        self.screen.fill((255,255,255))

        for o in self.objects:
            o.draw(self.screen)

        pygame.display.flip()

    def compute(self):
        i = 0
        while i < len(self.objects):
            self.objects[i].compute()
            i += 1

        heading = self.joy.ang + math.pi/2
        if heading > math.pi: heading -= 2*math.pi
        heading *= 57.2957795
        heading = math.floor(heading + 0.5)
        heading *= -1
        self.joyserver.move(self.joy.rad,heading,-self.joy.rot)



m = Main()
m.setupGame()
m.runGame()

pygame.quit()
