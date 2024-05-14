# Importerer alle bibliotekene vi trenger i spillet
import math as m
import pygame as pg
from pygame.locals import (K_LEFT, K_RIGHT, K_SPACE, K_a)
import os 
import sys 

# finner mappen som filene ligger i
folderPath = os.path.dirname(os.path.abspath(sys.argv[0])) 

# Starter pygame
pg.init()

# Lager et vindu der vi skal "tegne" spillet
vindu_bredde = 700
vindu_høyde = 650
vindu = pg.display.set_mode((vindu_bredde, vindu_høyde))

# Laster opp alle bildene vi skal bruke i spillet 
GåsH = pg.image.load(folderPath+r"\Gås mot høyre.png")
GåsV = pg.image.load(folderPath+r"\Gås mot venstre.png")
Tomato = pg.image.load(folderPath+r"\Tomat.png")
Bakgrunn = pg.image.load(folderPath+r"\Bakgrunn.png")
Gameover = pg.image.load(folderPath+r"\Gameover.jpg")

class spillobjekt:
    """
    Klasse for generelle egenskaper til ulike spillobjekt

    Parameter:
        x (int): X-kordinatet til spillobjektet
        y (int): Y-kordinatet til spillobjektet
        fart (int): Farten til spillobjektet
        bilde (pygame.Surface): Selve spillobjektet
    """
    def __init__(self, x, y, fart, bilde):
        """
        Konstruktør
        """
        self.x = x
        self.y = y
        self.fart = fart
        self.bilde = bilde

    def tegn(self):
        """
        Metode for å tegne spillobjektet / bilde
        """
        vindu.blit(self.bilde,(self.x, self.y))
    
    def flytt(self):
        """
        Metode for å flytte spillobjektet / bilde
        """
        # Sjekker om spillobjektet / bilde havner utenfor venstre eller høyre kant
        if self.x <= 0 or self.x >= vindu_bredde - self.bilde.get_width():
            self.fart = -self.fart
        
        # Flytter spillobjektet / bilde
        self.x += self.fart

class Tomat(spillobjekt):
    """
    Klasse for å representere tomat spillobjektet

    Parameter:
        x (int): X-kordinatet til tomaten
        y (int): Y-kordinatet til tomaten
        fart (int): Farten til tomaten
        bilde (pygame.Surface): Bilde av tomaten
    """
    def __init__(self, x, y, fart, bilde):
        """
        Konstruktør
        """
        # Arver paramterer fra spillobjekt klassen
        super().__init__(x,y, fart, bilde) 

    def tegn(self):
        """
        Metode for å tegne tomaten
        """
        # Arver tegne metode fra spillobjekt klassen
        super().tegn() 

    def flytt(self, taster):
        """
        Metode for å flytte tomaten med piltaster

        Paramteter:
            taster (bibliotek): Importerer pil tast funksjoner fra pygame.locals biblioteket
        """
        # Sjekker om tomaten havner utenfor venstre eller høyre kant
        if self.x <= 0 or self.x >= vindu_bredde - self.bilde.get_width():
            self.x = -self.x
        
        # Flytter tomaten
        self.y += self.fart

        # if setninger for å styre hvilken vei tomaten går etter hvilken pil tast som blir trykket
        if taster[K_LEFT]:
            self.x -= self.fart
        if taster[K_RIGHT]:
            self.x += self.fart

class Gås(spillobjekt):
    """
    Klasse for å representere gås spillobjektet

    Parameter:
        x (int): X-kordinatet til gåsen
        y (int): Y-kordinatet til gåsen
        fart (int): Farten til gåsen
        bildeH (pygame.Surface): Bilde av gåsen når den går mot høyre
        bildeV (pygame.Surface): Bilde av gåsen når den går mot venstre
    """
    def __init__(self, x, y, fart, bildeH, bildeV):
        """
        Konstruktør
        """
        # Arver paramterer fra spillobjekt klassen
        super().__init__(x, y, fart, bildeH) 
        self.bildeV = bildeV

    def flytt(self):
        """
        Metode for å flytte gåsen og skife bilde etter hvilken vei gåsen går
        """
        # Arver flytte metode fra spillobjekt klassen
        super().flytt() 
        
        # Endrer hvilket bilde av gåsen som skal vises etter hvilken vei gåsen beveger seg
        if self.fart <= 0:
            vindu.blit(self.bildeV,(self.x, self.y))
        else:
            vindu.blit(self.bilde,(self.x, self.y))

class HitboxTomat(Tomat):
    """
    Klasse for å representere hitboxen bak tomaten som gås hitboxen skal treffe

    Parameter:
        x (int): X-kordinatet til hitboxen til tomaten
        y (int): Y-kordinatet til hitboxen til tomaten
        fart (int): Farten til hitboxen til tomaten
        bilde (pygame.Surface): Bilde av tomaten
    """
    def __init__(self, x, y, fart, bilde): 
        """
        Konstruktør
        """
        # Arver parameterer fra tomat klassen
        super().__init__(x, y, fart, bilde) 
        # Radiusen til hitboxen til tomaeten
        self.radius = 20 
    
    def flytt(self):
        """
        Metode for å flytte hitboxen til tomaten med piltaster
        """
        # Arver flytte metode fra tomat klassen
        super().flytt(trykkede_taster) 

    def tegn(self):
        """
        Metode for å tegne hitboxen til tomaten
        """
        pg.draw.circle(vindu, (255,0,0), (self.x + (self.bilde.get_width() / 2) - 1, self.y + (self.bilde.get_height() / 2) - 3), self.radius)

class HitboxGås(spillobjekt):
    """
    Klasse for å representere hitboxen bak gåsen som tomat hitboxen skal treffe

    Parameter:
        x (int): X-kordinatet til hitboxen til gåsen
        y (int): Y-kordinatet til hitboxen til gåsen
        fart (int): Farten til hitboxen til gåsen
        vindusobjekt (pygame.Surface): Vinduet som hitboxen til gåsen skal tegnes i
        bilde (pygame.Surface): Bilde av gåsen
    """
    def __init__(self, x, y, fart, vindusobjekt, bilde):
        """
        Konstruktør
        """
        # Arver parameterer fra spillobjekt klassen
        super().__init__(x, y, fart, bilde) 
        # Hitboxen til gåsens kordinater
        self.hitbox = (self.x, self.y)
        self.vindusobjekt = vindusobjekt
        # Radiusen til hitboxen til gåsen
        self.radius = 15

    def flytt(self):
        """
        Metode for å flytte på hitboxen
        """
        # Arver flytte metode fra spillobjekt klassen
        super().flytt() 

    def tegn(self):
        """
        Metode for å tegne hitboxen
        """
        # Tegner hitboxen etter hvilken vei gåsen går
        if self.fart <= 0:
            self.hitbox = (self.x + 45, self.y + 17)
            pg.draw.circle(self.vindusobjekt, (255,0,0), self.hitbox, self.radius)
        else:
            self.hitbox = (self.x + 160, self.y + 15)
            pg.draw.circle(self.vindusobjekt, (255,0,0), self.hitbox, self.radius)        

class Utfall():
    """
    Klasse for å representere de ulike uftallene som kan skje i spillet; enten treffer tomaten gåsas hode, eller ikke

    Parameter:
        objekt_hitboxGås (spillobjekt): Objektet hitboxen til gåsen
        objekt_tomat (spillobjekt): Objektet tomat
        objekt_gås (spillobjekt): Objektet gås
        objekt_hitboxTomat (spillobjekt): Objektet hitboxen til tomaten
    """
    def __init__(self, objekt_hitboxGås, objekt_tomat, objekt_gås, objekt_hitboxTomat):
        """
        Konstruktør
        """
        self.hitboxTomat = objekt_hitboxTomat
        self.hitboxGås = objekt_hitboxGås
        self.tomat = objekt_tomat
        self.gås = objekt_gås
        # Poeng tjent i spillet
        self.poeng = 0 

    def treffer(self):
        """
        Metode for å sjekke om tomaten treffer gåsens hode 

        """
        # Bruker pytagorasetning for å finne ut hvor langt hitboxene til gåsen og tomaten er hverandre
        xAvstand = (self.hitboxGås.x - self.hitboxTomat.x)**2
        yAvstand = ((self.hitboxGås.y) - self.hitboxTomat.y)**2
        avstand = m.sqrt(xAvstand + yAvstand) 

        if self.hitboxGås.fart <= 0:
            avstand = avstand - 5
        else:
            avstand = avstand - 95

        # Radiusen til tomaten og gåsens hitbox sumert
        radier = self.hitboxTomat.radius + self.hitboxGås.radius

        # Lager teksten som forteller hvor mye poeng brukeren har
        font = pg.font.Font('freesansbold.ttf', 32)
        Skrift = font.render(f"Du har {self.poeng} poeng", True, (255, 255, 255))
        vindu.blit(Skrift, (0,0)) 

        # if setning for når hitboxen til tomaten og hitboxen til gåsen treffer hverandre
        if avstand <= radier:
            # Oppdaterer kordinatene til tomaten og hitboxen til tomaten til å gå tilbake til start posisjonen
            self.tomat.x = 335
            self.tomat.y = 1
            self.hitboxTomat.x = 335
            self.hitboxTomat.y = 1
            # Øker poeng mengden med 1 
            self.poeng += 1
            # Øker farten til alle objektene med 0.1 slik at det blir litt og litt vanskeligere for hvert poeng
            self.gås.fart += 0.1
            self.hitboxGås.fart += 0.1
            self.tomat.fart += 0.1
            self.hitboxTomat.fart += 0.1 

    def ikketreffer(self):
        """
        Metode for å sjekke om tomaten ikke treffer gåsen hode
        """
        # Viser gameover skjermen og to bilder av gåsen når tomaten har truffet bakken, og ikke hodet til gåsen
        if vindu_høyde - self.tomat.y <= 50:
            vindu.blit(Gameover, (0,0))   
            vindu.blit(GåsH, (0,0))
            vindu.blit(GåsV,(490, 400))

# Lager ulike objekter til spillet
Gåsen = Gås(2, 410, 0.5, GåsH, GåsV)
Tomaten = Tomat(335, 1, 0.5, Tomato)
HitboxenTomat = HitboxTomat(335, 1, 0.5, Tomato)
HitboxenGås = HitboxGås(2, 410, 0.5, vindu, GåsH)
Resultat = Utfall(HitboxenGås, Tomaten, Gåsen, HitboxenTomat)

# En variabel satt til falsk for å vise om spillet har startet eller ikke
spill_startet = False    

# Skrift som skal være på start skjermen
tekstlinjer = [
    "Spillet går utpå at man skal kaste tomater på gåsen",
    "Bruk venstre og høyre piltaster for å bevege tomaten",
    "Du får ett poeng for hver gang du treffer hodet til gåsen",
    "Trykk på mellomromstasten for å starte spillet",
    "Lykke til!!"
]

# Gjentar helt til brukeren lukker vinduet
fortsett = True
while fortsett:

    # Sjekker om brukeren har lukket vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False
    
    # Importerer tastatur tastene vi trenger til spillet 
    trykkede_taster = pg.key.get_pressed()

    # Sjekker om space tasten er trykket slik at spill_start blir satt til True, og spillet blir startet
    if trykkede_taster[K_SPACE] and not spill_startet:
        spill_startet = True
    
    if trykkede_taster[K_a] and not spill_startet:
        spill_startet = True

    # Farger startvinduet oransje og setter inn et bile av både tomaten og gåsen i startskjermen
    vindu.fill((255, 165, 0))
    vindu.blit(Tomato, (70,50))
    vindu.blit(GåsV,(490, 400))
    #Lager en font og skriftstørrelse til teksten på startskjermen
    font = pg.font.Font('freesansbold.ttf', 25) 

    # for i løkke for å skrive ut teksten på start skjermen
    # enumerate(tekstlinjer) er en funksjon som lager et indeksnummer (i) og et tilhørende element (tekst) for hver bokstav i listen tekstlinjer
    for i, tekst in enumerate(tekstlinjer): 
        # Lager et overflateojekt for teksten med render funksjonen
        tekst_render = font.render(tekst, True, (255, 255, 255))
        # Tegner teksten, her oppgir vi x og y kordinatene til teksten også. 
        # Y-posisjonen blir justert etter hvilken indeks tekst elementet har
        vindu.blit(tekst_render, (10, 250 + i * 30))

    # if setning for å starte spillet når spill_startet er lik True
    if spill_startet:   
        
        # Lager spillvindu med en fin bakgrunn
        vindu.blit(Bakgrunn, (0,0))

        # Tegner og flytter hitboxen til gåsen
        HitboxenGås.flytt()
        HitboxenGås.tegn()

        # Tegner og flytter hitboxen til tomaten
        HitboxenTomat.tegn()
        HitboxenTomat.flytt()

        # Flytter gåsen 
        Gåsen.flytt()

        # Tegner og flytter tomaten
        Tomaten.tegn()
        Tomaten.flytt(trykkede_taster)

        # Sjekker om tomaten og gåsen har treffet hverandre eller ikke
        Resultat.treffer()
        Resultat.ikketreffer()

    # Oppdaterer alt innholdet i vinduet
    pg.display.flip()

# Avslutter pygame
pg.quit()