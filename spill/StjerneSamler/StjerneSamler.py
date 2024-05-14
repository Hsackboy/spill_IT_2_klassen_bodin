import pygame
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d, K_SPACE)
import random as rd
import math as m
import os
import sys 

pygame.init()
vindu_bredde = 900
vindu_høyde = 500
vindu = pygame.display.set_mode((vindu_bredde, vindu_høyde))

pygame.display.set_caption("stjernespill")

filnavn = os.path.dirname(os.path.abspath(sys.argv[0])) + r"\data\highscores.txt"

# denne konstanten brukes når man skal skifte mellom valgene, høyere verdi gjør at det tar lengre tid å skifte
menyKonstant = 70

# tom liste med highscores
highscores = []
with open(filnavn, encoding="utf-8") as innfil:
    for linje in innfil:
        highscores.append(int(linje.rstrip()))
    
class Meny():
    """ Klasse for Menyer
    Parametre:
     vindu: vindu menyen tegnes på
     bakgrunnsfarge: bestemmer bakgrunnsfargen på menyen
     valg (int): hvilken tilstand menyen er i 
    """
    def __init__(self, vindu, bakgrunnsfarge, valgfarge,  valg=0):
        """ konstruktør """
        self.vindu = vindu
        self.bakgrunnsfarge = bakgrunnsfarge
        self.valg = valg
        self.valgfarge = valgfarge
    
    def skiftMeny(self, taster, antall, tid):
        """ Metode som sjekker tilstanden i spillet og tastaturet for å skifte meny"""
        return taster[pygame.K_SPACE] and menyKonstant*(antall-1)< self.valg <= menyKonstant*antall and pygame.time.get_ticks() - tid > 1000
        
def skrift(tekst, font, font2, farge, farge2, antall, valg): # lager skrift på menyene, tegner underline hvis valg er innenfor et bestemt intervall
    menyvalg = font.render(tekst, True, farge)
    if menyKonstant*(antall-1)< valg <= menyKonstant*antall:
        font2.set_underline(True)
        menyvalg = font2.render(tekst, True, farge2)
    return menyvalg

def skrift_2valg(tekst, font, font2, farge, farge2, antall, valg, antall2, valg2): # sjekker også valg2 som er altså valg til venstre og høyre
    menyvalg = font.render(tekst, True, farge)
    if menyKonstant*(antall-1)< valg <= menyKonstant*antall and menyKonstant*(antall2-1) < valg2 <= menyKonstant*antall2:
        font2.set_underline(True)
        menyvalg = font2.render(tekst, True, farge2)
    return menyvalg

class StartMeny(Meny):
    def __init__(self, vindu, bakgrunnsfarge, valgfarge, valg):
        super().__init__(vindu, bakgrunnsfarge, valgfarge, valg)
        
    def tegnStartMeny(self, font, font2, taster):
        """ metode for å tegne start menyen """
        vindu.fill(self.bakgrunnsfarge) 
        title = pygame.font.SysFont('arial', 50).render("Stjerne Samler", True, (255, 255, 255))

        self.vindu.blit(title, (vindu_bredde/2 - title.get_width()/2, vindu_høyde/2 - title.get_height()/2))

        if (taster[pygame.K_UP] or taster[pygame.K_w]) and self.valg > 0:
            self.valg -= 1
        if (taster[pygame.K_DOWN] or taster[pygame.K_s]) and self.valg < menyKonstant*3:
            self.valg += 1

        menyvalg = ["1 Person", "2 Personer", "Farge Meny", "Highscores"]
        y_pos = vindu_høyde/2
        
        for i in range(len(menyvalg)):
            menylinje = skrift(menyvalg[i], font, font2, (255,255,255), self.valgfarge, i, self.valg)
            y_pos += menylinje.get_height()
            x_pos = vindu_bredde/2 - menylinje.get_width()/2
            self.vindu.blit(menylinje, (x_pos, y_pos))
            
class FargeMeny(Meny):
    def __init__(self, vindu, bakgrunnsfarge, valgfarge,  valg, valg2):
        super().__init__(vindu, bakgrunnsfarge, valgfarge, valg)
        self.valg2 = valg2
    
    def fargerValgt(self, farger):
        """ metode for å hente fargene som er valgt """
        if farger == 0:
            return (100,100,100)
        if farger == 1:
            return (255,0,0)
        if farger == 2:
            return (230,100,30)
        if farger == 3:
            return (255,255,0)
        if farger == 4:
            return (200,200,200)
        if farger == 5:
            return (0,0,255)
        if farger == 6:
            return (0,255,0)
        if farger == 7:
            return (195,0,195)
        else:   
            return (255,255,255)

    def tegnFargeMeny(self, font, font2, taster):
        """ metode for å tegne farge menyen """
        # endrer verdier for 'valg' slik at fargen endres når du trykker på piltastene
        #ned/opp
        if (taster[pygame.K_UP] or taster[pygame.K_w]) and self.valg > 0:
            self.valg -= 1
        if (taster[pygame.K_DOWN] or taster[pygame.K_s]) and self.valg < menyKonstant*4:
            self.valg += 1
       
        #til venstre/høyre
        if (taster[pygame.K_LEFT] or taster[pygame.K_a]) and self.valg2 > 0:
            self.valg2 -= 1
        if (taster[pygame.K_RIGHT] or taster[pygame.K_d]) and self.valg2 < menyKonstant:
            self.valg2 += 1

        #tittel til fargevalg
        vindu.fill(self.bakgrunnsfarge)
        title = pygame.font.SysFont('arial', 44).render("Farger", True, (255, 255, 255))
        self.vindu.blit(title, (vindu_bredde/2 - title.get_width()/2, title.get_height()/2))

        #tittel for spillere
        player1 = font.render('Farge person 1', True, (255, 255, 255))
        player2 = font.render('Farge person 2', True, (255, 255, 255))
        self.vindu.blit(player1, (100, player1.get_height()+title.get_height()))
        self.vindu.blit(player2, (vindu_bredde - (player2.get_width()+100), player2.get_height()+title.get_height()))

        fargevalg = ["grå", "rød", "oransje", "gul", "lysgrå", "blå", "grønn", "lilla"]

        #tegner farger for spiller 1
        x_pos = 100
        y_pos = player1.get_height()+title.get_height()
        for i in range(4):
            menylinje = skrift_2valg(fargevalg[i], font, font2, self.fargerValgt(i), self.fargerValgt(i), i, self.valg, 0, self.valg2)
            y_pos += menylinje.get_height()
            vindu.blit(menylinje, (x_pos, y_pos))
        
        #tegner fargene for spiller 2
        x_pos2 = vindu_bredde - (player2.get_width()+100)
        y_pos2 = player2.get_height()+title.get_height()
        for i in range(4):
            menylinje = skrift_2valg(fargevalg[i+4], font, font2, self.fargerValgt(i+4), self.fargerValgt(i+4), i, self.valg, 1, self.valg2)
            y_pos2 += menylinje.get_height()
            vindu.blit(menylinje, (x_pos2, y_pos2))
        
        # tilbake til start knapp
        start = skrift("Tilbake til Start", font, font2, (255,255,255), self.valgfarge, 4, self.valg)
        self.vindu.blit(start, (vindu_bredde/2 - start.get_width()/2, vindu_høyde - 2*start.get_height()))
    
    def skiftMeny(self, taster, antall, tid, antall2):
        return super().skiftMeny(taster, antall, tid) and (antall2-1)*menyKonstant < self.valg2 <= antall2*menyKonstant
  
class TaptMeny(Meny):
    def __init__(self, vindu, bakgrunnsfarge, valgfarge, valg):
        super().__init__(vindu, bakgrunnsfarge, valgfarge, valg)

    def tegnTaptMeny(self,font,font2, taster):
        """ metode for å tegne tapt meny """
        vindu.fill(self.bakgrunnsfarge)
        
        title = font.render('Du døde', True, (255, 255, 255))
        
        if (taster[pygame.K_UP] or taster[pygame.K_w]) and self.valg > 0:
            self.valg -= 1
        if (taster[pygame.K_DOWN] or taster[pygame.K_s]) and self.valg < menyKonstant:
            self.valg += 1
        
        restart_tekst = skrift("Tibake til start", font, font2, (100,20,20), self.valgfarge, 0, self.valg)
        quit_tekst = skrift("Quit", font, font2, (100,20,20), self.valgfarge, 1, self.valg)
       
        vindu.blit(title, (vindu_bredde/2 - title.get_width()/2, vindu_høyde/2 - title.get_height()/3))
        vindu.blit(restart_tekst, (vindu_bredde/2 - restart_tekst.get_width()/2, vindu_høyde/2 + restart_tekst.get_height() ))
        vindu.blit(quit_tekst, (vindu_bredde/2 - quit_tekst.get_width()/2, vindu_høyde/2 + quit_tekst.get_height()+ restart_tekst.get_height()))

class VantMeny(Meny):
    def __init__(self, vindu, bakgrunnsfarge, valgfarge,  valg):
        super().__init__(vindu, bakgrunnsfarge, valgfarge,  valg)
    def tegnVantMeny(self, font, font2, taster):
        """ metode for å tegne vant meny """
        vindu.fill((200, 150, 190))
        
        title = font.render("Du vant!", True, (255, 255, 255))
        vindu.blit(title, (vindu_bredde/2 - title.get_width()/2, vindu_høyde/2 - title.get_height()/3))

        if (taster[pygame.K_UP] or taster[pygame.K_w]) and self.valg > 0:
            self.valg -= 1
        if (taster[pygame.K_DOWN] or taster[pygame.K_s]) and self.valg < menyKonstant*2:
            self.valg += 1

        menyvalg = ["Fortsett å spille", "Tilbake til start", "Quit"]
        y_pos = vindu_høyde/2
        for i in range(len(menyvalg)):
            menylinje = skrift(menyvalg[i], font, font2, (255, 255, 255), self.valgfarge, i, self.valg)
            y_pos += menylinje.get_height()
            x_pos = vindu_bredde/2 - menylinje.get_width()/2
            self.vindu.blit(menylinje, (x_pos, y_pos))

def visHighscores(tall, font):
    tekst = f"{tall}. "
    if len(highscores) >= int(tall):
        tekst += str(highscores[(tall-1)])
    else:
        tekst += '-'
    return font.render(tekst, True, (255,255,255))

class HighscoresMeny(Meny):
    def __init__(self, vindu, bakgrunnsfarge, valgfarge, valg):
        super().__init__(vindu, bakgrunnsfarge, valgfarge,  valg)

    def tegnHighscoresMeny(self, font, font2):
        """ metode for å tegne highscores meny """
        vindu.fill(self.bakgrunnsfarge) 
        title = pygame.font.SysFont('arial', 50).render("Highscores", True, (255, 255, 255))
        self.vindu.blit(title, (vindu_bredde/2 - title.get_width()/2, title.get_height()/2))
        
        font2.set_underline(True)
        startknapp = font2.render("Tilbake til start", True, self.valgfarge)
        self.vindu.blit(startknapp, (vindu_bredde/2 - startknapp.get_width()/2, vindu_høyde- 2*startknapp.get_height()))
        
        highscores.sort(reverse = True)
        y_pos = title.get_height()
        x_pos= 100
        for i in range(10):
            menylinje = visHighscores(i+1, font)
            if i==5:
                x_pos += vindu_bredde/2
                y_pos = title.get_height()
            y_pos += menylinje.get_height()
            self.vindu.blit(menylinje, (x_pos, y_pos))

class VanskelighetsgradMeny(Meny):
    def __init__(self, vindu, bakgrunnsfarge, valgfarge, valg=0):
        super().__init__(vindu, bakgrunnsfarge, valgfarge, valg)
    def tegnVanskelighetsgradMeny(self,taster,  font, font2):
        vindu.fill(self.bakgrunnsfarge)
        title = pygame.font.SysFont('arial', 50).render("Velg vanskelighetsnivå", True, (255, 255, 255))
        self.vindu.blit(title, (vindu_bredde/2 - title.get_width()/2, title.get_height()/2))

        if (taster[pygame.K_UP] or taster[pygame.K_w]) and self.valg > 0:
            self.valg -= 1
        if (taster[pygame.K_DOWN] or taster[pygame.K_s]) and self.valg < menyKonstant*2:
            self.valg += 1

        menyvalg = ["Enkelt", "Middels", "Vanskelig"]
        y_pos = vindu_høyde/2
        for i in range(len(menyvalg)):
            menylinje = skrift(menyvalg[i], font, font2, (255, 255, 255), self.valgfarge, i, self.valg)
            y_pos += menylinje.get_height()
            x_pos = vindu_bredde/2 - menylinje.get_width()/2
            self.vindu.blit(menylinje, (x_pos, y_pos))


class Spiller:
    """Klasse for å lage en spiller"""
    def __init__(self, vindu, farge, x, y, radius, opp, ned, venstre, høyre, fart):
        """Konstruktør"""
        self.vindusobjekt = vindu
        self.farge = farge
        self.x = x
        self.y = y

        self.radius = radius
        self.opp = opp
        self.ned = ned
        self.venstre = venstre
        self.høyre = høyre

        self.fart = fart
        
    def tegn(self):
        """Metode for å tegne spilleren"""
        pygame.draw.circle(self.vindusobjekt, self.farge, (self.x, self.y), self.radius)

        pygame.draw.ellipse(self.vindusobjekt, (255,255,255), (self.x- self.radius,self.y - self.radius/2, self.radius*0.9,self.radius*0.5)) #syn

        pygame.draw.rect(self.vindusobjekt, self.farge, (self.x+self.radius*0.59, self.y - self.radius*0.2,self.radius/2,self.radius)) #oksygentank

        pygame.draw.ellipse(self.vindusobjekt, self.farge, (self.x - self.radius*0.7,self.y, self.radius*0.5,self.radius*1.4)) #bein 1
        pygame.draw.ellipse(self.vindusobjekt, self.farge, (self.x + self.radius*0.2,self.y, self.radius*0.5,self.radius*1.4)) #bein 2
    

    def flytt(self, taster):
        """Metode for å flytte spilleren"""
        fart_faktor = 20 / (self.radius*2)  # Juster farten basert på radiusen
        fart = self.fart * fart_faktor

        if taster[self.opp]:
            self.y -= fart
        if taster[self.ned]:
            self.y += fart
        if taster[self.venstre]:
            self.x -= fart
        if taster[self.høyre]:
            self.x += fart
        
        #sjekk at den ikke er utenfor på x
        if (self.x - self.radius) <= 0: 
            self.x += 1
        if (self.x + self.radius) >= self.vindusobjekt.get_width():
            self.x -= 1
        
        #sjekk at den ikke er utenfor på y
        if (self.y - self.radius) <= 0: 
            self.y += 1
        if (self.y + self.radius) >= self.vindusobjekt.get_height():
            self.y -= 1

class Stjerne:
    """Klasse for å representere en Stjerne"""

    def __init__(self, x, y, fart, radius, vindusobjekt, farge, respawn_delay):
        """Konstruktør"""
        self.x = x
        self.y = y
        self.fart = fart
    
        self.radius = radius
        self.vindusobjekt = vindusobjekt
        self.farge = farge

        self.respawn_timer = 0  # Timer for å kontrollere respawn-tidspunktet
        self.respawn_delay = respawn_delay*1000  # Tidsforsinkelse før respawn i millisekunder

    def tegn(self):
        """Metode for å tegne stjernen"""
        pygame.draw.circle(self.vindusobjekt, self.farge, (self.x, self.y), self.radius)

    def respawn(self):
        """Metode for å tilbakestille stjernens posisjon"""
        self.x = self.vindusobjekt.get_width() 
        self.y = rd.randint(self.radius, self.vindusobjekt.get_height() - self.radius)
        self.respawn_timer = pygame.time.get_ticks()  # Oppdaterer respawn-timer

    def flytt(self):
        """Metode for å flytte stjernen"""
        # Flytter stjernen
        
        self.x -= self.fart

        # Sjekker kollisjon med vinduskanter og om respawn-tiden er gått ut
        if (self.x - self.radius) < 0 and pygame.time.get_ticks() - self.respawn_timer >= self.respawn_delay:
            self.respawn()

def leggTilHighscore(tall):  
    highscores.append(tall)
    with open(filnavn, "a") as fil:
        fil.write(f"{tall}\n")

def kollisjon(obj1, obj2):
    xAvstand2 = (obj1.x - obj2.x) ** 2  # x-avstand opphøyd i andre
    yAvstand2 = (obj1.y - obj2.y) ** 2  # y-avstand i andre

    avstand = m.sqrt(xAvstand2 + yAvstand2)
    if avstand < ((obj1.radius + obj2.radius) / 1.8): # deler på 1.8 siden hitboxen til spillerene er litt større enn bare radiusen til sirkelen
        return True
    return False       

def countdown(tid):
    tid_igjen = tid - pygame.time.get_ticks() // 1000
    return tid_igjen

def tegncredits(font, navn):
    credits = font.render("Laget av "+navn, True, (255, 255, 255))
    vindu.blit(credits, (vindu_bredde - credits.get_width(), vindu_høyde- credits.get_height()))

# objekter for menyene
startM = StartMeny(vindu, (0,0,0),(132,165,247), 0)
fargeM = FargeMeny(vindu, (0,0,0), (132,165,247),  0, 0)
taptM = TaptMeny(vindu, (200, 100, 100), (80, 10, 10), 0)
vantM = VantMeny(vindu, (200, 150, 190),(170, 70, 170), 0)
highscoresM = HighscoresMeny(vindu, (0,0,0),(132,165,247), 0)

vanskelighetsgradM = VanskelighetsgradMeny(vindu, (0,0,0), (132,165,247), 0)

#variabler for fart
spillerfart = 0.7
stjernefart = 0.7

# objekter for stjerner
stjerner = Stjerne((vindu.get_height() - 10), 200, stjernefart, 10, vindu, (255,255,255), 1)
oksygenStjerner = Stjerne((vindu.get_height() - 10), 200, stjernefart, 10, vindu, (0,0,255), 6)
bombeStjerner = Stjerne((vindu.get_height() - 10), 200, stjernefart, 10, vindu, (255,0,0), 10)

#objekter for sirkler som viser hvilken farge du har valgt
valgstjerne1 = Stjerne(80,155,0,10,vindu,fargeM.fargerValgt(0), 1)
valgstjerne2 = Stjerne(vindu_bredde/2 + 130,155,0,10,vindu,fargeM.fargerValgt(4), 1)

#objekter for spiller
spiller1 = Spiller(vindu, (100,100,100), vindu_bredde/2, 100, 20, K_w, K_s, K_a, K_d, spillerfart)
spiller2 = Spiller(vindu, (200,200,200), vindu_bredde/2, 140, 20, K_UP, K_DOWN, K_LEFT, K_RIGHT, spillerfart)

spillStatus = "startMeny"

maxpoeng = 10

tid_nåStart=0
tid_nåAnnet=0

font = pygame.font.SysFont('arial', 36)
font2 = pygame.font.SysFont('arial', 36)

typerSpillStatus = ["startMeny", "spill1","spill2", "farger", "highscore"]
valgstjerneposisjoner = [155, 200, 245, 285]

hastigheter = [0.3,0.7,1]

tidligerevunnet = False 
antall_spillere = 1
startSpill = False

while True:
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           quit()
    
    

    taster = pygame.key.get_pressed()
    
    if spillStatus == typerSpillStatus[0]: #tegner start meny
        
        tid = 10 + pygame.time.get_ticks() // 1000 #restarter oksygentanken
        poeng = 0 #restarter poengsum

        spiller1.x = vindu_bredde/2     #restarter posisjon til spiller 1
        spiller1.y = 100

        spiller2.x = vindu_bredde/2     #restarter posisjon til spiller 2
        spiller2.y = 140

        startM.tegnStartMeny(font, font2, taster) #tegner startmeny
        tegncredits(pygame.font.SysFont('arial', 30), "Jorunn E.T")
        
        for i in range(len(typerSpillStatus)): # skifter mellom menyene
            if startM.skiftMeny(taster, i, tid_nåAnnet):
                spillStatus = (typerSpillStatus[i+1])
                tid_nåStart = pygame.time.get_ticks() 
             
    elif spillStatus == typerSpillStatus[3]: #fargemeny
        
        fargeM.tegnFargeMeny(font, font2, taster)
        valgstjerne1.tegn()
        valgstjerne2.tegn()

        # skift farge på spillere
        for i in range(8):
            if i < 4: # spiller 1
                if fargeM.skiftMeny(taster, i, tid_nåStart, 0):
                    spiller1.farge = fargeM.fargerValgt(i)
                    valgstjerne1.farge = fargeM.fargerValgt(i)
                    valgstjerne1.y = valgstjerneposisjoner[i]
            if i >= 4: # spiller 2
                if fargeM.skiftMeny(taster, (i-4), tid_nåStart, 1):
                    spiller2.farge = fargeM.fargerValgt(i)
                    valgstjerne2.farge = fargeM.fargerValgt(i)
                    valgstjerne2.y = valgstjerneposisjoner[i-4]
        tegncredits(pygame.font.SysFont('arial', 30), "Jorunn E.T")
        #gå tilbake til start
        if fargeM.skiftMeny(taster, 4, tid_nåStart, 0) or fargeM.skiftMeny(taster, 4, tid_nåStart, 1): 
            tid_nåAnnet = pygame.time.get_ticks()
            spillStatus = "startMeny"
            fargeM.valg = 0
            fargeM.valg2 = 0
        
    elif spillStatus == typerSpillStatus[4]: # tegner highscores meny
        highscoresM.tegnHighscoresMeny(font, font2)
        
        if highscoresM.skiftMeny(taster, 0, tid_nåStart):
            spillStatus = "startMeny"
            tid_nåAnnet = pygame.time.get_ticks()
        tegncredits(pygame.font.SysFont('arial', 30), "Jorunn E.T")
                      
    elif spillStatus == "spillTapt": #tegner tapt meny når du har tapt
        startSpill = False
        taptM.tegnTaptMeny(font,font2, taster)
       
        if taptM.skiftMeny(taster, 0, tid_nåStart):         #tilbake til start meny
            spillStatus = "startMeny"
            tid_nåAnnet = pygame.time.get_ticks()
            taptM.valg = 0

        if taptM.skiftMeny(taster, 1, tid_nåStart): #Slutt spillet
            pygame.quit()
            quit()
        visPoeng = font.render(f"Poengsum: {str(poeng)}", True, (255, 255, 255))
        vindu.blit(visPoeng, (vindu_bredde - 200, 20))

    elif spillStatus == "spillVant": #tegner du vant
        vantM.tegnVantMeny(font,font2,taster)

        if vantM.skiftMeny(taster, 0, tid_nåStart):         # fortsett å spille
            spillStatus = typerSpillStatus[antall_spillere]
            tid_nåAnnet = pygame.time.get_ticks()
             # legger til poengsum slik at spillet ikke tror du har vunnet
            tid += 10
            tidligerevunnet = True
            
        if vantM.skiftMeny(taster, 1, tid_nåStart):         #tilbake til start meny
            spillStatus = "startMeny"
            tid_nåAnnet = pygame.time.get_ticks()
            taptM.valg = 0

        if vantM.skiftMeny(taster, 2, tid_nåStart): #Slutt spillet
            pygame.quit()
            quit()
    

    elif startSpill == True and antall_spillere == 1: #spillet er igang med 1 person!
        vindu.fill((20, 20, 40))
        antall_spillere = 1

        #oksygentank
        oksygen = countdown(tid)
        if oksygen < 0:
            leggTilHighscore(poeng)
            spillStatus = "spillTapt"
        
        #spiller
        spiller1.tegn()
        spiller1.flytt(taster)

        #stjerner
        stjerner.tegn()
        stjerner.flytt()

        oksygenStjerner.tegn()
        oksygenStjerner.flytt()

        bombeStjerner.tegn()
        bombeStjerner.flytt()

        if kollisjon(spiller1, bombeStjerner):
            leggTilHighscore(poeng)
            bombeStjerner.respawn()
            spillStatus = "spillTapt"

        #legg til mer oksygen
        if kollisjon(spiller1, oksygenStjerner):
            tid += 5
            oksygenStjerner.respawn()

        #poengsum
        if kollisjon(spiller1, stjerner):
            poeng += 1
            stjerner.respawn()
        
        
        #vant
        if poeng == maxpoeng and not tidligerevunnet:
            leggTilHighscore(poeng)
            spillStatus = "spillVant"
        
        # tekst 
        objektiv = font.render(f"Samle {str(maxpoeng)} hvite stjerner!", True, (255, 255, 255))
        oksygenIgjen = font.render(f"Oksygen: {oksygen}", True, (0, 0, 255))
        visPoeng = font.render(f"Stjerner samlet: {str(poeng)}", True, (255, 255, 255))

        vindu.blit(objektiv, (20, 20))
        vindu.blit(visPoeng, (vindu_bredde - (visPoeng.get_width()+20), 20))
        vindu.blit(oksygenIgjen, (vindu_bredde - 200, 20+visPoeng.get_height()))
        
    elif startSpill and antall_spillere == 2: #spillet er igang med 2 personer!
        vindu.fill((20, 20, 40))
        antall_spillere = 2
        #oksygentank
        oksygen = countdown(tid)
        if oksygen < 0:
            leggTilHighscore(poeng)
            spillStatus = "spillTapt"
            
        # spillere
        spiller1.tegn()
        spiller1.flytt(taster)

        spiller2.tegn()
        spiller2.flytt(taster)

        #stjerner
        stjerner.tegn()
        stjerner.flytt()

        #oksygen stjerner
        oksygenStjerner.tegn()
        oksygenStjerner.flytt()
        if kollisjon(spiller1, oksygenStjerner) or kollisjon(spiller2, oksygenStjerner):
            tid += 5
            oksygenStjerner.respawn()

        #bombestjerner
        bombeStjerner.tegn()
        bombeStjerner.flytt()
        if kollisjon(spiller1, bombeStjerner) or kollisjon(spiller2, bombeStjerner):
            leggTilHighscore(poeng)
            bombeStjerner.respawn()
            spillStatus = "spillTapt"

        #poengsum
        if kollisjon(spiller1, stjerner) or kollisjon(spiller2, stjerner):
            poeng += 1
            stjerner.respawn()

        #vant
        if poeng == maxpoeng*2 and not tidligerevunnet:
            leggTilHighscore(poeng)
            spillStatus = "spillVant"
        
        # tekst 
        objektiv = font.render(f"Samle {str(maxpoeng*2)} hvite stjerner!", True, (255, 255, 255))
        oksygenIgjen = font.render(f"Oksygen: {oksygen}", True, (0, 0, 255))
        visPoeng = font.render(f"Stjerner samlet: {str(poeng)}", True, (255, 255, 255))

        vindu.blit(objektiv, (20, 20))
        vindu.blit(visPoeng, (vindu_bredde - (visPoeng.get_width()+20), 20))
        vindu.blit(oksygenIgjen, (vindu_bredde - 200, 20+visPoeng.get_height()))
    
    elif spillStatus == typerSpillStatus[1]:
        tid = 10 + pygame.time.get_ticks() // 1000
        antall_spillere = 1 
        vanskelighetsgradM.tegnVanskelighetsgradMeny(taster, font, font2)
        
        for i in range(len(hastigheter)):
            if vanskelighetsgradM.skiftMeny(taster, i, tid_nåStart):
                startSpill = True
                spiller1.fart = hastigheter[i]
                stjerner.fart = hastigheter[i]
                bombeStjerner.fart = hastigheter[i]
                oksygenStjerner.fart = hastigheter[i]

            

    elif spillStatus == typerSpillStatus[2]:
        tid = 10 + pygame.time.get_ticks() // 1000
        antall_spillere = 2
        vanskelighetsgradM.tegnVanskelighetsgradMeny(taster, font, font2)
        for i in range(len(hastigheter)):
            if vanskelighetsgradM.skiftMeny(taster, i, tid_nåStart):
                startSpill = True
                spiller1.fart = hastigheter[i]
                spiller2.fart = hastigheter[i]
                stjerner.fart = hastigheter[i]
                bombeStjerner.fart = hastigheter[i]
                oksygenStjerner.fart = hastigheter[i]

    pygame.display.update()