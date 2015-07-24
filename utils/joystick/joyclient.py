import math
import sys
import pygame

import Pyro4

RATE = 10
SERV_URL = "PYRO:obj_dd319a0cd93242a586878c89a8a95a4e@ieeebeagle.nomads.utk.edu:9091"

def limitToRange(a, b, c):
    if a < b:
        a = b
    if a > c:
        a = c
    return a


class Main:

    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 450
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # you have to change the URI below to match your own host/port.
        self.joyserver = Pyro4.Proxy(SERV_URL)

    def setupGame(self):
        self.clock = pygame.time.Clock()
        self.FPS = RATE
        pygame.joystick.init()
        # numJoys = pygame.joystick.get_count()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self.numButtons = self.joystick.get_numbuttons()
        self.numAxes = self.joystick.get_numaxes()
        self.buttons = [0] * self.numButtons
        self.axes = [0] * self.numButtons

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

    def draw(self):
        self.screen.fill((255, 255, 255))
        pygame.display.flip()

    def compute(self):
        for i in xrange(self.numButtons):
            self.buttons[i] = self.joystick.get_button(i)
        for i in xrange(self.numAxes):
            self.axes[i] = self.joystick.get_axis(i)

        self.x = self.joystick.get_axis(3)
        self.y = self.joystick.get_axis(1)
        self.rot = self.joystick.get_axis(0)
        self.rad = math.hypot(self.x, self.y)
        self.rad = limitToRange(self.rad, 0, 1)
        self.ang = math.atan2(self.y, self.x)
        self.x = self.rad * math.cos(self.ang)
        self.y = self.rad * math.sin(self.ang)

        heading = self.ang + math.pi / 2
        if heading > math.pi:
            heading -= 2 * math.pi
        heading *= 57.2957795
        heading = math.floor(heading + 0.5)
        heading *= -1
        self.joyserver.move(self.rad, heading, -self.rot)
        print 'data', self.buttons, self.axes
        print 'data', (self.rad, heading, -self.rot)


m = Main()
m.setupGame()
m.runGame()

pygame.quit()
