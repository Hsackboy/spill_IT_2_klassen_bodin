import pygame as pg
import math
from pygame.locals import K_SPACE

#jeg vurderte å bruke arv men dette var ikke hensiksmessig siden så lite av koden var felles for klassene

class Player:
    def __init__( self, pos, size, fartY, gravity, jumpPower, aliveImg, dedImg, flyImg, isAlive=True, flappyMode=False,) -> None:
        """Setter variabler"""
        self.pos = [pos[0], pos[1]]
        self.gravity = gravity
        self.jumpPower = jumpPower
        self.isAlive = isAlive
        self.aliveImg = aliveImg
        self.flyImg = flyImg
        self.deadImg = dedImg
        self.size = size
        self.fartY = fartY
        self.fartX = 0
        self.groundPos = pos[1]
        self.hitboxRadius = size[0] / 2
        self.hitboxPos = [
            self.pos[0] + self.hitboxRadius,
            self.pos[1] + self.size[1] / 1.5,
        ]
        self.flappyMode = flappyMode
        pass

    def drawHitbox(self, vindu):
        """debugging funskjon for hitbox
        """
        pg.draw.circle(vindu, (255, 0, 0), self.hitboxPos, self.hitboxRadius, width=2)

    def drawPlayer(self, vindu):
        """tegner spiller"""
        imgToUse = self.aliveImg

        if self.flappyMode:
            imgToUse = self.flyImg

        if self.isAlive == False:
            imgToUse = self.deadImg
        scaledPlayer = pg.transform.scale(imgToUse, self.size)
        vindu.blit(scaledPlayer, self.pos)

    def move(self):
        """flytterSpiller utifra fart"""
        self.pos[1] += self.fartY
        self.pos[0] += self.fartX
        self.fartY += self.gravity
        if self.pos[1] > self.groundPos and (self.flappyMode == False):
            self.fartY = 0
            self.fartX = 0
            self.pos[1] = self.groundPos

        if self.pos[1] < -self.size[1]:
            self.pos[1] = -self.size[1]

        if self.flappyMode:
            self.hitboxPos = [
                self.pos[0] + self.hitboxRadius,
                self.pos[1] + self.size[1] / 2,
            ]
        else:
            self.hitboxPos = [
                self.pos[0] + self.hitboxRadius,
                self.pos[1] + self.size[1] / 1.5,
            ]

    def jump(self, keys):
        """tar inn taster og sjekker om spiller kan hoppe og utfører hoppingen. retunerer True hvis spiller hopper"""
        if keys[K_SPACE]:
            if self.fartY == 0 and (self.flappyMode == False):
                self.fartY = -1 * self.jumpPower
                return True
            elif self.flappyMode == True:
                self.fartY = -1 * self.jumpPower
                return True

    def changeSize(self, newSize):
        """endrer størrelse på spiller"""
        self.hitboxRadius = newSize[0] / 2
        self.hitboxPos = [
            self.pos[0] + self.hitboxRadius,
            self.pos[1] + self.size[1] / 1.5,
        ]
        self.size = newSize

    def testCollison(self, meteor):
        """Tester kollisjon med hinder"""
        xDist = meteor.pos[0] - self.pos[0]
        yDist = meteor.pos[1] - self.pos[1]
        dist = math.sqrt(xDist**2 + yDist**2)
        if dist < (meteor.hitboxRadius + self.hitboxRadius):
            return True
        return False

    def gameOver(self):
        """Funksjon som setter spiller i game over modus og gjør gameover animasjon"""
        self.isAlive = False
        # kode for gameover animasjon
        self.fartX = 6
        self.fartY = -4
        self.pos[1] = self.groundPos - 10

    def drawAndMove(self, vindu):
        """Kobinasjon av to funksjoner for ryddigere kode"""
        self.move()
        self.drawPlayer(vindu)
