import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
import os 
import sys 

data_for_verden =[]
# finner mappen som filene ligger i
folderPath = os.path.dirname(os.path.abspath(sys.argv[0])) 

filnavn = folderPath+r'\rekorder.txt'

muted = False

#rekorder 
rekorder = []
with open(filnavn, encoding="utf-8") as innfil:
    for linje in innfil:
        rekorder.append(int(linje.strip()))

#konfigurerer lyd 
pygame.mixer.pre_init(44100, -16, 2, 512)
#mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

vindu_bredde = 600
vindu_hoyde = 600

vindu = pygame.display.set_mode((vindu_bredde, vindu_hoyde))
pygame.display.set_caption("eventyrspill")

#definerer font 
font = pygame.font.SysFont('Bauhaus 93', 70)
font_poeng = pygame.font.SysFont('Bauhaus 93', 30)



#definer spill variabler
blokk_størrelse = 30
spill_over = 0
hoved_meny = True
rekorder_meny = False
nivå = 1
max_nivå = 7
poeng = 0

#definerer farge
farge_grå = (128, 128, 128)
farge_hvit = (255, 255, 255)
farge_svart = (0, 0, 0)
farge_rød = (255, 0, 0)
farge_blå = (0, 0, 255)

# her legger jeg inn bildene jeg vil bruke i koden
bakgrunn_bilde = pygame.image.load(folderPath+r'\img/bakgrunn.jpg')
restart_bilde = pygame.image.load(folderPath+r'\img/restart_btn.png')
start_bilde = pygame.image.load(folderPath+r'\img/start_btn.png')
forlat_bilde = pygame.image.load(folderPath+r'\img/exit_btn.png')
rekorder_bilde = pygame.image.load(folderPath+r'\img/rekorderknapp.png')
rekorder_bilde = pygame.transform.scale(rekorder_bilde, (300, 100))
lagre_bilde = pygame.image.load(folderPath+r'\img/LAGRE_REKORD.png')
lagre_bilde = pygame.transform.scale(lagre_bilde, (300, 100))
tilbake_bilde = pygame.image.load(folderPath+r'\img/tilbakeknapp.png')

lyd_bilde =  pygame.image.load(folderPath+r'\img/lyd.png')
lyd_bilde = pygame.transform.scale(lyd_bilde, (50, 50))
lydav_bilde = pygame.image.load(folderPath+r'\img/lydav.png')
lydav_bilde = pygame.transform.scale(lydav_bilde, (50, 50))
hjem_bilde = pygame.image.load(folderPath+r'\img/home_knapp.png')
hjem_bilde = pygame.transform.scale(hjem_bilde, (50, 50))

#last inn lyder
pygame.mixer.set_num_channels(2)
bakgrunnsmusikk_Channel = pygame.mixer.Channel(0)
bakgrunnsmusikk = pygame.mixer.Sound(folderPath+r'\img\CozyKingdom.mp3')

effekt_channel = pygame.mixer.Channel(1)
#pygame.mixer.music.load('img\CozyKingdom.mp3')

#pygame.mixer.music.play(-1, 0.0, 5000)

mynt_lyd = mixer.Sound(folderPath+r'\img/coin.wav')
#skrur ned lyden
mynt_lyd.set_volume(0.5)
hoppe_lyd = mixer.Sound(folderPath+r'\img/jump.wav')
hoppe_lyd.set_volume(0.5)
game_over_lyd = mixer.Sound(folderPath+r'\img/game_over.wav')
game_over_lyd.set_volume(0.5)

def tegn_tekst(text, font, farge, x, y):
    bilde = font.render(text, True, farge)
    vindu.blit(bilde, (x, y))

#funksjon til å starte nivået på nytt
def restart_nivå(nivå):
    spiller.reset(100, vindu_hoyde / 2 + 150)
    lava_gruppe.empty()
    blob_gruppe.empty()
    utgang_gruppe.empty()
    plattform_gruppe.empty()

    #laste inn nivået og lager verden
    if path.exists(folderPath+ f'/level{nivå}_data'):
        pickle_in = open(folderPath+f'/level{nivå}_data', 'rb')
        data_for_verden = pickle.load(pickle_in)
    else:
        print('filen finnes ikke')
    verden = Verden(data_for_verden)

    return verden
    
class Knapp():
    def __init__(self, x, y, bilde):
        self.bilde = bilde
        self.rect = self.bilde.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.trykket = False

    def draw(self):
        trykk = False

        #hent museposisjon
        pos = pygame.mouse.get_pos()

        #sjekk om musen er over knappen
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.trykket == False:
                trykk = True
                #print("Trykket")
                self.trykket = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.trykket = False

        #tegner knappen inn i brettet
        vindu.blit(self.bilde, self.rect)

        return trykk

class Spiller():
    def __init__(self, x, y):
        self.reset(x, y)

    def oppdater(self, spill_over):
        dx = 0
        dy = 0
        gå_cooldown = 5
        kolli_max = 20

        if spill_over == 0:
            #ta ut tastetrykk
            nøkkel = pygame.key.get_pressed()
            if nøkkel[pygame.K_UP] and self.hoppet == False and self.i_luften == False:
                hoppe_lyd.play()
                self.vel_y = -15
                self.hoppet = True

            if nøkkel [pygame.K_SPACE] and self.hoppet == False and self.i_luften == False:
                hoppe_lyd .play()
                self.vel_y = -15
                self.hoppet = True

            if nøkkel[pygame.K_UP] == False:
                self.hoppet = False

            if nøkkel[pygame.K_LEFT]:
                dx = -5
                self.motarbeide += 1
                self.rettning = -1
            if nøkkel[pygame.K_RIGHT]:
                dx = 5
                self.motarbeide += 1
                self.rettning = 1

            if nøkkel[pygame.K_LEFT] == False and nøkkel[pygame.K_RIGHT] == False:
                self.motarbeide = 0
                self.indeks = 0
                if self.rettning == -1:
                    self.bilde = self.bilder_venstre[self.indeks]
                if self.rettning == 1:
                    self.bilde = self.bilder_høyre[self.indeks]

            #håndter animasjoner 
        
            if self.motarbeide >= gå_cooldown:
                self.motarbeide = 0
                self.indeks += 1
                if self.indeks >= len(self.bilder_høyre):
                    self.indeks = 0
                if self.rettning == -1:
                    self.bilde = self.bilder_venstre[self.indeks]
                if self.rettning == 1:
                    self.bilde = self.bilder_høyre[self.indeks]

            #legg til gravitasjon
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #sjekk for kollisjon
            self.i_luften = True
            for brikke in verden.brikke_liste:
                #sjekk for kollisjon i x rettning
                if brikke[1].colliderect(self.rect.x + dx, self.rect.y, self.bredde, self.hoyde):
                    dx = 0
                #sjekk for kollisjon i y rettning 
                if brikke[1].colliderect(self.rect.x, self.rect.y + dy, self.bredde, self.hoyde):
                    #sjekk hvis karakter er under bakken 
                    if self.vel_y < 0:
                        dy = brikke[1].bottom - self.rect.top
                        self.vel_y = 0
                    
                    #sjekk hvis karakter er over bakken
                    elif self.vel_y > 0:
                        dy = brikke[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.i_luften = False

            #sjekk for kollisjon med motstandere 
            if pygame.sprite.spritecollide(self, blob_gruppe, False):
                spill_over = -1
                game_over_lyd.play()

            #sjekk for kollisjon med lava
            if pygame.sprite.spritecollide(self, lava_gruppe, False):
                spill_over = -1
                game_over_lyd.play()

            #sjekk for kollisjon med utgangen
            if pygame.sprite.spritecollide(self, utgang_gruppe, False):
                #1 er positivt 
                #0 er ingenting 
                #-1 er er at karakteren dør
                spill_over = 1
 
            #sjekk for kollisjon med plattformer
            for plattform in plattform_gruppe:
                #sjekk for kollisjon i x rettning
                if plattform.rect.colliderect(self.rect.x + dx, self.rect.y, self.bredde, self.hoyde):
                    dx = 0
                #sjekk for kollisjon i y rettning
                if plattform.rect.colliderect(self.rect.x, self.rect.y + dy, self.bredde, self.hoyde):
                    #sjekk hvis karakter er under plattformen
                    if abs((self.rect.top + dy) - plattform.rect.bottom) < kolli_max:
                        self.vel_y = 0
                        dy = plattform.rect.bottom - self.rect.top
                    #sjekk hvis karakter er over plattformen
                    elif abs((self.rect.bottom + dy) - plattform.rect.top) < kolli_max:
                        self.rect.bottom = plattform.rect.top - 1
                        self.i_luften = False
                        dy = 0
                    #flytt sideleng langs plattformen
                    if plattform.flytt_x != 0:
                        self.rect.x += plattform.flytt_rettning * plattform.flytt_x
                         
            #oppdaterer spiller kordinater
            self.rect.x += dx
            self.rect.y += dy

        elif spill_over == -1:
            self.bilde = self.død_bilde
            tegn_tekst('DU ER DØD', font, farge_blå, (vindu_bredde / 2) - 180, (vindu_hoyde / 3))
            #if self.rect.y >= :
            self.rect.y -= 5

        #tegner spilleren inn i brettet 
        vindu.blit(self.bilde, self.rect)

        return spill_over

    def reset(self, x, y):
        self.bilder_høyre = []
        self.bilder_venstre = []
        self.indeks = 0
        self.motarbeide = 0 
        for num in range(1, 5):
            bilde_hoyre = pygame.image.load(folderPath+f'/img/apekatt{num}.png')
            bilde_hoyre = pygame.transform.scale(bilde_hoyre, (24, 48))
            bilde_venstre = pygame.transform.flip(bilde_hoyre, True, False)
            self.bilder_høyre.append(bilde_hoyre) 
            self.bilder_venstre.append(bilde_venstre)
        self.død_bilde = pygame.image.load(folderPath+r'\img/ghost.png')
        self.død_bilde = pygame.transform.scale(self.død_bilde, (24, 48))
        self.bilde = self.bilder_høyre[self.indeks]
 
        self.rect = self.bilde.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bredde = self.bilde.get_width()
        self.hoyde = self.bilde.get_height()
        self.vel_y = 0
        self.hoppet = False
        self.rettning = 0
        self.i_luften = True

class Verden():
    def __init__(self, data):
        self.brikke_liste = [] 

        #laster inn flere bilder 
        self.jord_bilde = pygame.image.load(folderPath+r'\img/jord.png')
        self.gress_bilde = pygame.image.load(folderPath+r'\img/gress.png')
        
        rad_teller = 0
        for rad in data:
            kolonne_teller = 0
            for brikke in rad:
                if brikke == 1:
                    bilde = pygame.transform.scale(self.jord_bilde, (blokk_størrelse, blokk_størrelse))
                    bilde_rektangel = bilde.get_rect()
                    bilde_rektangel.x = kolonne_teller * blokk_størrelse
                    bilde_rektangel.y = rad_teller * blokk_størrelse
                    brikke = (bilde, bilde_rektangel)
                    self.brikke_liste.append(brikke)

                if brikke == 2:
                    bilde = pygame.transform.scale(self.gress_bilde, (blokk_størrelse, blokk_størrelse))
                    bilde_rektangel = bilde.get_rect()
                    bilde_rektangel.x = kolonne_teller * blokk_størrelse
                    bilde_rektangel.y = rad_teller * blokk_størrelse
                    brikke = (bilde, bilde_rektangel)
                    self.brikke_liste.append(brikke)
                if brikke == 3:
                    blob = Enemy(kolonne_teller * blokk_størrelse, rad_teller * blokk_størrelse)
                    blob_gruppe.add(blob)
                if brikke == 4:
                    plattform = Plattform(kolonne_teller * blokk_størrelse, rad_teller * blokk_størrelse, 1, 0)
                    plattform_gruppe.add(plattform)
                if brikke == 5:
                    platform = Plattform(kolonne_teller * blokk_størrelse, rad_teller * blokk_størrelse, 0, 1)
                    plattform_gruppe.add(platform)
                if brikke == 6:
                    lava = Lava(kolonne_teller * blokk_størrelse, rad_teller * blokk_størrelse + (blokk_størrelse // 2))
                    lava_gruppe.add(lava)
                if brikke == 7:
                    mynt = Mynt(kolonne_teller * blokk_størrelse, rad_teller * blokk_størrelse + (blokk_størrelse // 2))
                    mynt_gruppe.add(mynt)
                if brikke == 8:
                    utgang = Utgang(kolonne_teller * blokk_størrelse, rad_teller * blokk_størrelse-(blokk_størrelse // 2))
                    utgang_gruppe.add(utgang)
                kolonne_teller += 1
            rad_teller += 1

    def draw(self):
        for brikke in self.brikke_liste:
            vindu.blit(brikke[0], brikke[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(folderPath+r'\img/blob.png')
        self.image = pygame.transform.scale(self.image, (blokk_størrelse * 1.2, blokk_størrelse * 1.2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flytte_rettning = 1
        self.flytte_teller = 0

    def update(self):
        self.rect.x += self.flytte_rettning
        self.flytte_teller += 1
        if abs(self.flytte_teller) > 50:
            self.flytte_rettning *= -1
            self.flytte_teller *= -1

class Plattform (pygame.sprite.Sprite):
    def __init__(self, x, y, flytt_x, flytt_y):
        pygame.sprite.Sprite.__init__(self)
        bilde = pygame.image.load(folderPath+r'\img/plattform.png')
        self.image = pygame.transform.scale(bilde, (blokk_størrelse, blokk_størrelse // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flytt_teller = 0
        self.flytt_rettning = 1
        self.flytt_x = flytt_x
        self.flytt_y = flytt_y 

    def update(self):
        self.rect.x += self.flytt_rettning * self.flytt_x
        self.rect.y += self.flytt_rettning * self.flytt_y
        self.flytt_teller += 1
        if abs(self.flytt_teller) > 50:
            self.flytt_rettning *= -1
            self.flytt_teller *= -1

class Lava (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        bilde = pygame.image.load(folderPath+r'\img/lava.png')
        self.image = pygame.transform.scale(bilde, (blokk_størrelse, blokk_størrelse//2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Mynt (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        bilde = pygame.image.load(folderPath+r'\img/coin.png')
        self.image = pygame.transform.scale(bilde, (blokk_størrelse // 2, blokk_størrelse//2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
class Utgang (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        bilde = pygame.image.load(folderPath+r'\img/exit.png')
        self.image = pygame.transform.scale(bilde, (blokk_størrelse, int(blokk_størrelse*1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def visHighscores(nummer, font, farge):
    tekst = f"{nummer}."
    if len(rekorder) >= int(nummer):
        tekst += str(rekorder[(nummer - 1)])
    else:
        tekst += ' -'
    return font.render(tekst, True, farge)

spiller  = Spiller(100, vindu_hoyde - 78)

blob_gruppe = pygame.sprite.Group()
plattform_gruppe = pygame.sprite.Group()
lava_gruppe = pygame.sprite.Group()
mynt_gruppe = pygame.sprite.Group()
utgang_gruppe = pygame.sprite.Group()

#lag en penge for å gjøre poengsummen kulere 
poeng_mynt = Mynt(blokk_størrelse // 2, blokk_størrelse // 2)
mynt_gruppe.add(poeng_mynt)


#laster inn data for verden og lag verden
if path.exists(folderPath+f'/level{nivå}_data'):
    pickle_in = open(folderPath+f'/level{nivå}_data', 'rb')
    data_for_verden = pickle.load(pickle_in)
else:
    print('filen finnes ikke')
verden = Verden(data_for_verden)

#lager knapper
restart_knapp = Knapp(vindu_bredde // 2 -65, vindu_hoyde // 2 + 50, restart_bilde)
start_knapp = Knapp(vindu_bredde // 2 - 285, vindu_hoyde // 2, start_bilde)
forlat_knapp = Knapp(vindu_bredde // 2 + 50, vindu_hoyde // 2, forlat_bilde)
rekorder_knapp = Knapp(vindu_bredde// 2 - 125, vindu_hoyde//2 - 115, rekorder_bilde)
lagre_rekord = Knapp(vindu_bredde //2 - 150, vindu_hoyde// 2 + 100, lagre_bilde)
tilbake_knapp = Knapp(vindu_bredde //2, vindu_hoyde - 100 , tilbake_bilde)

lyd_på_knapp = Knapp(vindu_bredde-50, 0, lyd_bilde)
lyd_av_knapp = Knapp(vindu_bredde-50, 0, lydav_bilde)

hjem_knapp = Knapp(vindu_bredde-100, 0, hjem_bilde)

# kjører koden i en løkke
kjører = True

while kjører:
    
    bakgrunnsmusikk_Channel.set_volume(1)
    if muted:
        bakgrunnsmusikk_Channel.set_volume(0)

    if bakgrunnsmusikk_Channel.get_busy()==False:
        bakgrunnsmusikk_Channel.play(bakgrunnsmusikk)

    clock.tick(fps)
    
        
    if rekorder_meny:
        vindu.blit(bakgrunn_bilde, (0, 0))

        rekorder.sort(reverse=True)
        overskrift = font.render("rekorder", True, (255,255,255))
        vindu.blit(overskrift, (vindu_bredde // 2 - overskrift.get_width() // 2, 0))
        
        x_pos = 20
        y_pos = overskrift.get_height()
        for i in range(10):
            tekst = visHighscores(i+1, pygame.font.SysFont('Bauhaus 93', 40), (255,255,255))
            vindu.blit(tekst, (x_pos,y_pos))
            y_pos += tekst.get_height()
        
        if tilbake_knapp.draw():
            rekorder_meny = False
            hoved_meny = True
            
    if hoved_meny == True and not rekorder_meny:
        
            # tegner bakgrunnen
        vindu.blit(bakgrunn_bilde, (0, 0))
        bakgrunn_bilde = pygame.transform.scale(bakgrunn_bilde, (vindu_bredde, vindu_hoyde))
        
        if  not muted and lyd_på_knapp.draw():
            muted = True
        elif  muted and lyd_av_knapp.draw():
            muted = False
        
        if not rekorder_meny and forlat_knapp.draw():
            kjører = False
        if not rekorder_meny and  start_knapp.draw():
            hoved_meny = False
        if not rekorder_meny and rekorder_knapp.draw():
            rekorder_meny = True
            hoved_meny = False
        
    
    
    
    elif not rekorder_meny:
        
            # tegner bakgrunnen
        vindu.blit(bakgrunn_bilde, (0, 0))
        bakgrunn_bilde = pygame.transform.scale(bakgrunn_bilde, (vindu_bredde, vindu_hoyde))
        
        verden.draw()
        
        if  not muted and lyd_på_knapp.draw():
            muted = True
        elif  muted and lyd_av_knapp.draw():
            muted = False
        
        if hjem_knapp.draw():
            data_for_verden = []
            verden = restart_nivå(nivå)
            spill_over = 0
            poeng = 0
            hoved_meny = True

        if spill_over == 0:
            blob_gruppe.update()
            plattform_gruppe.update()
            #oppdatere poeng sum 
            #sjekk om en mynt er kollidert med spiller
            #true argumentet fjerner penge
            if pygame.sprite.spritecollide(spiller, mynt_gruppe, True):
                poeng += 1
                mynt_lyd.play()
            tegn_tekst('X ' + str(poeng), font_poeng, farge_svart, blokk_størrelse , 0)

        blob_gruppe.draw(vindu)
        plattform_gruppe.draw(vindu)
        lava_gruppe.draw(vindu)
        mynt_gruppe.draw(vindu)
        utgang_gruppe.draw(vindu)
        
        spill_over = spiller.oppdater(spill_over)

        # hvis spiller dør
        if spill_over == -1:
            if restart_knapp.draw():
                data_for_verden = []
                verden = restart_nivå(nivå)
                spill_over = 0
                poeng = 0
        #hvis spiller vinner
        if spill_over == 1:
            #går til neste nivå
            nivå += 1
            if nivå <= max_nivå:
                
                #start på nytt
                data_for_verden = []
                verden = restart_nivå(nivå)
                spill_over = 0   
            else:
                tegn_tekst('DU VANT', font, farge_blå, (vindu_bredde // 2)- 115, (vindu_hoyde // 2 - 100))
            
                if lagre_rekord and lagre_rekord.draw():
                    rekorder.append(int(poeng))
                    with open(filnavn, "a") as fil:
                        fil.write(f"{poeng}\n")
                    lagre_rekord = None
                    

                if restart_knapp.draw():
                    nivå = 1
                    data_for_verden = []
                    verden = restart_nivå(nivå)
                    spill_over = 0
                    poeng = 0
                    hoved_meny = True

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            kjører = False

    pygame.display.update()

pygame.quit()