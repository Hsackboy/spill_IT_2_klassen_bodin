import pygame as pg


class Obstical:
    def __init__(self, pos, size, fart, img) -> None:
        """Setter variabler"""
        self.pos = [pos[0], pos[1]]
        self.img = img
        self.size = size
        self.fart = fart
        self.hitboxRadius = self.size[1] / 2.5
        self.hitboxPos = [
            self.pos[0] + self.size[0] / 2,
            self.pos[1] + self.size[1] / 2,
        ]
        pass

    def drawObstical(self, vindu):
        """tegner hinderet
        """
        scaledObstical = pg.transform.scale(self.img, self.size)
        vindu.blit(scaledObstical, self.pos)

    def move(self):
        """Flytter hinder utifra fart"""
        self.pos[0] -= self.fart
        self.hitboxPos = [
            self.pos[0] + self.size[0] / 2,
            self.pos[1] + self.size[1] / 2,
        ]

    def drawAndMove(self,vindu):
        """kobinerer to koder for ryddigere kode"""
        self.move()
        self.drawObstical(vindu)
    
    def drawHitbox(self, vindu):
        """debugging funskjon for hitbox
        """
        pg.draw.circle(vindu, (255, 0, 0), self.hitboxPos, self.hitboxRadius, width=2)

