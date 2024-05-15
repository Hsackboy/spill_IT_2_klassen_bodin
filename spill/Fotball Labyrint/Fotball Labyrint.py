import pygame
import os 
import sys 

# finner mappen som filene ligger i
folderPath = os.path.dirname(os.path.abspath(sys.argv[0])) 

class Vegg(object):
    """
    Klasse for å opprette veggene i labyrinten
    
    Parametre:
        pos (int): posisjonen veggene skal legges til i labyrinten

    """
    def __init__(self, pos):
        vegger.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16) # Rektangelet har en størrelse på 16x16 piksler, og er plassert på (pos[0], pos[1])

class Player(object):
    """
    #Klasse for spillerobjektet, inneholder funksjon for kollisjoner og bevegelse av spillerobjektet
    
    Parametre: 
        dx (int): x- koordinatet til spillerobjektet
        dy (int): y- koordinatet til spillerobjektet
    
    """
    def __init__(self):
        self.rect = pygame.Rect(32, 305, 16, 16) # Spiller-rektangelet starter på¨posisjon 32(x-akse),305(y-akse) og har en størrelse på 16x16 piksler
    
    def kræsj(self, dx, dy):
        """Funksjon for å finne ut når spillerobjektet kolliderer med veggene"""
        for vegg in vegger:
            if self.rect.colliderect(vegg.rect):
                if dx > 0:
                    self.rect.right = vegg.rect.left
                if dx < 0:
                    self.rect.left = vegg.rect.right
                if dy > 0:
                    self.rect.bottom = vegg.rect.top
                if dy < 0:
                    self.rect.top = vegg.rect.bottom

    def beveg_single_axis(self, dx, dy):
        """Funksjon for å bevege spillerobjektet og stopper spillerobjektet for å gå utenfor banen"""
        
        # Flytt spillerobjektet på en akse
        self.rect.x += dx  # Endre x-posisjon med dx
        self.rect.y += dy  # Endre y-posisjon med dy
        
        # Sjekk for kollisjoner
        self.kræsj(dx, dy)
        
        #Stopper ballen fra å gå ut av banen
        if self.rect.left<4:
            self.rect.left=4
        if self.rect.right > vindusbredde-4:
            self.rect.right = vindusbredde-4
        if self.rect.top < 4:
            self.rect.top = 4
        if self.rect.bottom > vindushøyde-4:
            self.rect.bottom = vindushøyde-4
        
    def beveg(self, dx, dy):
        """Funksjon for å registrere bevegelser og flytt spillerobjektet"""
        # Hvis det er en endring i x-retning
        if dx != 0:
            self.beveg_single_axis(dx, 0)
        # Hvis det skjer endring i y-retning
        if dy != 0:
            self.beveg_single_axis(0, dy)

pygame.init()

pygame.display.set_caption("Finn veien ut av labyrinten og score mål!")

vindusbredde=800
vindushøyde=600
vindu=pygame.display.set_mode((vindusbredde, vindushøyde)) #Setter dimensjonen for spill-vinduet


#Oppretter en liste for å legge inn veggene
vegger = []
player = Player()

# tegner utseendet på labyrinten
nivå = """    
        
      VVVVVVVVVVVVVVVVVVVVVVVVVVVVV 
      V                    V      V
      V   V  VVVVVVVV VVV  VVV VVVV
      V   V  V  V       V         V
      V   V  V  V  V  VVVVV VVVV VV
      V   VVVV  V  V        V  V  V 
      V      V  VV   V   VVVV VVVVV
      V   VVVV       VVVVV  V     V
      V   V     V VVVVV     V  V  V                 
      V VVV  VVVV V   VVVVVVV  VVVV
      V         V V   V V      V  V
   VVVV   V     V   VVV VV VV VV  V
          V V VVV   V V     V        S
   VVVV   V V   V   V V  VVVVV VVVV                  
      VVV   V   VVVVV V  V   VVV  V
      V        VV   V    V   V V  V
      V VVVVVV V   VVV  VV   V V  V       
      V              V       V    V
      V VVVVVVVV VVVVVV VV VVVV   V
      V V                V    VVV V
      V VVVVVVVVVVV VVVVVV      V V
      V             V             V
      VVVVVVVVVVVVVVVVVVVVVVVVVVVVV
      
""".splitlines() #Splitter hver linje inn i en liste og hopper over første linje, kunne evt kuttet ut første linje

Spill_ferdig=0 #Definerer variabel som får spillet til å gå

# Definerer vegger og sluttpunkt
x=1
y=1

#Løkke som går gjennom labyrint-listene
for rad in nivå:
    for kolonne in rad:
        if kolonne == "V":
            Vegg((x, y))
        if kolonne == "S":
            end_rect = pygame.Rect(x, 229, 10, 145) # setter størrelse for 
        x += 22 #Endrer mellomrommet mellom veggene, x-koordinat
    y += 22     #Endrer mellomrommet mellom veggene, y-koordinat
    x = -50     #Endrer startposisjonen til labyrinten, x-koordinat

endscreen=pygame.image.load(folderPath+r"\partybakgrunn2.jpg") #Importerer sluttskjermbilde
endscreen = pygame.transform.scale(endscreen, (800, 600))  # Endre størrelsen etter behov

highscore=1E6 #Brukes senere for å lagre highscore

running = True #Brukes for å holde spillet gående
tidtaker_startet = pygame.time.get_ticks()  # Starter tidtakeren

#Spill-løkken
while running:    
    # Løkke for å lukke spillet eller restarte
    for lukk in pygame.event.get():
        if lukk.type == pygame.QUIT:
            running = False
        if lukk.type == pygame.KEYDOWN and lukk.key == pygame.K_ESCAPE:
            running = False
        if lukk.type == pygame.KEYDOWN and lukk.key == pygame.K_r and Spill_ferdig>0:
            running = True
            Spill_ferdig=0
            tidtaker_startet = pygame.time.get_ticks()  # Oppdaterer tidtakeren
            player.rect.x = 32
            player.rect.y = 305

    # Fart og bevegelse for spiller-objektet
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.beveg(-6, 0)
    if key[pygame.K_RIGHT]:
        player.beveg(6, 0)
    if key[pygame.K_UP]:
        player.beveg(0, -6)
    if key[pygame.K_DOWN]:
        player.beveg(0, 6)
    
    # Tegner bakgrunnen
    fotballbane_bilde = pygame.image.load(folderPath+r"\fotballbane.jfif")
    fotballbane_størrelse=(800,600)
    fotballbane_bilde=pygame.transform.scale(fotballbane_bilde, fotballbane_størrelse)
    vindu.blit(fotballbane_bilde,(0,0))

    # Tegner veggene og sluttrektangelet
    for vegg in vegger:
        pygame.draw.ellipse(vindu, (20, 28, 64), vegg.rect)
    pygame.draw.rect(vindu, (255, 0, 0), end_rect) # Tegner sluttrektangelet
    
    #Tegner spiller-objektet
    pygame.draw.rect(vindu, (255, 195, 0), player.rect)

    mittBilde = pygame.image.load(folderPath+r"\Fotball.png") #Laster inn bilde av fotballen
    mittBilde = pygame.transform.scale(mittBilde, (26, 26))  # Endre størrelsen etter behov
    bilde_størrelse = mittBilde.get_rect().size
    bilde_posisjon = (player.rect.x - bilde_størrelse[0] // 6, player.rect.y - bilde_størrelse[1] // 6)
    vindu.blit(mittBilde, bilde_posisjon)

    tidtaker_nå = pygame.time.get_ticks() #Henter nåværende tid
    tid_gått = round((tidtaker_nå - tidtaker_startet)/1000,1)
    
    # Tegner tidtakeren i øvre høyre hjørne
    font = pygame.font.SysFont('Arial',36)
    tidtekst = font.render("Tid: " + str(tid_gått), True, (255, 255, 255))
    vindu.blit(tidtekst, (650, 10))

    #Når spillet er ferdig
    if player.rect.colliderect(end_rect) or Spill_ferdig > 0: 
        if Spill_ferdig == 0: #Stopper tidtakeren hvis spillet er ferdig
            Spill_ferdig = 1
            tidtaker_stoppet = pygame.time.get_ticks()
        vindu.blit(endscreen, (0, 0))
        gratulasjon = font.render("Gratulerer - Du scoret!!", True, (255, 255, 255))
        vindu.blit(gratulasjon, (245, 120))
        restart = font.render("Trykk 'R' for å restarte", True, (255, 255, 255))
        vindu.blit(restart, (250, 180))
        hade = font.render("Trykk escape-tasten for å avslutte", True, (255, 255, 255))
        vindu.blit(hade, (195, 240))
        tid_gått = round((tidtaker_stoppet - tidtaker_startet) / 1000,1)  # Total tid brukt i sekunder
        sluttid = font.render("Tid brukt: " + str(tid_gått) + " sekunder", True, (255, 255, 255))
        vindu.blit(sluttid, (240, 310))
        if tid_gått < highscore:
            highscore_tekst=font.render("Highscore: "+ str(tid_gått) +" sekunder", True, (255, 255, 255))
            highscore=tid_gått
        vindu.blit(highscore_tekst, (235, 380))
    
    pygame.display.flip()

pygame.quit()