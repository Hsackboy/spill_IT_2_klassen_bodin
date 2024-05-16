import os 
import sys 
import kultBiblotek2 as kB
import subprocess
import pygame
import random as rd

forsett = True
muteed = False
# finner mappen som filene ligger i
folderPath = os.path.dirname(os.path.abspath(sys.argv[0]))  #path til der filen fins
folderPathSpill = folderPath+r"/spill"  # path til spill folder
folderPathSound = folderPath+r"/data/sound"
spillListe = os.listdir(folderPathSpill) #liste over alle spill i folder

vindu_bredde = 900
vindu_høyde = 500

ingameTime = 0
clock = pygame.time.Clock()


# dette er en konstant som kontrollerer hvor raskt det skal gå når vi trykker på piltastene basically - høyere tall = tregere
menyKonstant = 30

spillPath = ""
spillnavn = ""

def skrift(tekst, font, font2, farge, farge2, antall, valg): # lager skrift på menyene, tegner underline hvis valg er innenfor et bestemt intervall
    menyvalg = font.render(tekst, True, farge)
    if menyKonstant*(antall-1)< valg <= menyKonstant*antall:
        font2.set_underline(True)
        menyvalg = font2.render(tekst, True, farge2)
    return menyvalg
class Meny():
    """ Klasse for Menyer
    Parametre:
     bakgrunnsfarge: bestemmer bakgrunnsfargen på menyen
     tittelfarge
     tekstfarge
     valgfarge
     valg (int): hvilken tilstand menyen er i 
    """
    def __init__(self, bakgrunnsfarge, tittelfarge, tekstfarge, valgfarge,  valg=0):
        """ konstruktør """
        self.bakgrunnsfarge = bakgrunnsfarge
        self.tittelfarge = tittelfarge
        self.tekstfarge = tekstfarge
        self.valg = valg
        self.valgfarge = valgfarge
    
    def skiftMeny(self, taster, antall):
        """ Metode som sjekker tilstanden i spillet og tastaturet for å skifte meny"""
        return (taster[pygame.K_SPACE] or taster[pygame.K_RETURN]) and menyKonstant*(antall-1)< self.valg <= menyKonstant*antall #and pygame.time.get_ticks() - tid > 1000
        
def skrift(tekst, font, font2, farge, farge2, antall, valg): # lager skrift på menyene, tegner underline hvis valg er innenfor et bestemt intervall
    menyvalg = font.render(tekst, True, farge)
    if menyKonstant*(antall-1)< valg <= menyKonstant*antall:
        font2.set_underline(True)
        menyvalg = font2.render(tekst, True, farge2)
    return menyvalg


class StartMeny(Meny):
    def __init__(self, bakgrunnsfarge, tittelfarge, tekstfarge, valgfarge, valg):
        super().__init__(bakgrunnsfarge,tittelfarge, tekstfarge, valgfarge, valg)
        self.antallSpillLoads =8
        self.internalPos = 0
    def tegnStartMeny(self, font, font2, taster,vindu,selectSound,soundchannel):
        """ metode for å tegne start menyen """
        vindu.fill(self.bakgrunnsfarge) 
        title = pygame.font.SysFont('arial', 50).render("Alle Spill Samlet", True,self.tittelfarge)
        vindu.blit(title, (vindu_bredde/2 - title.get_width()/2, title.get_height()/2))

        if (taster[pygame.K_UP] or taster[pygame.K_w]) and self.valg > 0:
            self.valg -= 1
            soundchannel.play(selectSound)
        if (taster[pygame.K_DOWN] or taster[pygame.K_s]) and self.valg <= menyKonstant*(self.antallSpillLoads-1):
            self.valg += 1
            soundchannel.play(selectSound)
        if (taster[pygame.K_DOWN] or taster[pygame.K_s]) and self.valg == menyKonstant*(self.antallSpillLoads-1):
            if self.internalPos+self.antallSpillLoads < len(spillListe):
                self.internalPos+=1
                self.valg -=1
        
        if taster[pygame.K_1]:
            self.valg = self.internalPos * menyKonstant
        elif taster[pygame.K_2]:
            self.valg = (1 + self.internalPos) * menyKonstant
        elif taster[pygame.K_3]:
            self.valg = (2 + self.internalPos) * menyKonstant
        elif taster[pygame.K_4]:
            self.valg = (3 + self.internalPos) * menyKonstant
        elif taster[pygame.K_5]:
            self.valg = (4 + self.internalPos) * menyKonstant
        elif taster[pygame.K_6]:
            self.valg = (5 + self.internalPos) * menyKonstant
        elif taster[pygame.K_7]:
            self.valg = (6 + self.internalPos) * menyKonstant
        elif taster[pygame.K_8]:
            self.valg = (7 + self.internalPos) * menyKonstant -10

        if (taster[pygame.K_UP] or taster[pygame.K_w]) and self.valg == 0:
            self.internalPos-=1
            self.valg -= 1
            if self.internalPos<0:
                self.internalPos =0
        
        instruksjonstekst1 = (pygame.font.SysFont('arial', 30).render("Trykk på pil-opp for å gå opp &", True,self.tittelfarge))
        instruksjonstekst2 = (pygame.font.SysFont('arial', 30).render("pil-ned for å gå ned", True,self.tittelfarge))
        
        vindu.blit(instruksjonstekst1, ((vindu_bredde - instruksjonstekst1.get_width()) - 10, 2*title.get_height()))
        vindu.blit(instruksjonstekst2, (vindu_bredde - instruksjonstekst2.get_width()-10, 2*title.get_height()+instruksjonstekst1.get_height()))

        y_pos = title.get_height()
        x_pos = 100
      
        for i in range(self.internalPos,self.internalPos+self.antallSpillLoads):
            menylinje = skrift(str(i+1) + ". " + spillListe[i], font, font2, self.tekstfarge, self.valgfarge, i, self.valg) 
            y_pos += menylinje.get_height()
            vindu.blit(menylinje, (x_pos, y_pos))

    
class Knapp():
    def __init__(self, x, y, bilde):
        self.bilde = bilde
        self.rect = self.bilde.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.trykket = False

    def draw(self, vindu):
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


# ordbok for alle farger, kan legge til farger senere
color_combinations = {
    "Sunset Glow": {
        "Deep Blue": (3, 4, 94),
        "Crimson Red": (220, 20, 60),
        "Orange": (255, 165, 0),
        "Gold": (255, 215, 0)
    },
    "Forest Whisper": {
        "Forest Green": (34, 139, 34),
        "Moss Green": (173, 223, 173),
        "Earth Brown": (101, 67, 33),
        "Soft Beige": (245, 245, 220)
    },
    "Ocean Breeze": {
        "Navy Blue": (0, 0, 128),
        "Aqua": (0, 255, 255),
        "Sea Green": (46, 139, 87),
        "Coral": (255, 127, 80)
    },
    "Royal Elegance": {
        "Royal Purple": (120, 81, 169),
        "Lavender": (230, 230, 250),
        "Champagne": (247, 231, 206),
        "Dark Gold": (184, 134, 11)
    },
    "Tropical Paradise": {
        "Turquoise": (64, 224, 208),
        "Mango": (255, 130, 67),
        "Palm Leaf": (106, 190, 48),
        "Coconut White": (255, 255, 240)
    },
    "Modern Chic": {
        "Charcoal": (54, 69, 79),
        "Blush Pink": (255, 192, 203),
        "Rose Gold": (183, 110, 121),
        "Ivory": (255, 255, 240)
    },
    "Winter Wonderland": {
        "Ice Blue": (173, 216, 230),
        "Snow White": (255, 250, 250),
        "Frost Gray": (210, 210, 255),
        "Silver": (192, 192, 192)
    },
    "Autumn Harvest": {
        "Burnt Orange": (204, 85, 0),
        "Harvest Gold": (218, 165, 32),
        "Olive Green": (128, 128, 0),
        "Chestnut Brown": (139, 69, 19)
    },
    "Vintage Retro": {
        "Mustard Yellow": (255, 219, 88),
        "Teal": (0, 128, 128),
        "Brick Red": (203, 65, 84),
        "Cream": (255, 253, 208)
    },
    "Neon Vibes": {
        "Neon Pink": (255, 20, 147),
        "Neon Green": (57, 255, 20),
        "Electric Blue": (125, 249, 255),
        "Bright Purple": (191, 0, 255)
    },
    "Jorunn's Farger": {
        "jorunns valg": (225, 138, 212),
        "jorunns tittel": (47, 24, 71),
        "jorunns tekst": (98, 71, 99),
        "jorunns bakgrunn": (212,217,237)
    },
     "Katharina's Farger": {
        "Katharina valg": (107, 5, 4),
        "Katharina tittel": (20, 33, 61),
        "Katharina tekst": (139, 139, 174),
        "Katharina bakgrunn": (241,233,218)
    },
     "Christian's Farger": {
        "Christian valg": (67,87,39),
        "Christian tittel": (0, 0, 255),
        "Christian tekst": (139, 139, 174),
        "Christian bakgrunn": (200,200,255)
    }
}

# variabler for index til å velge farger
select_color_index = 0
title_color_index = 1
text_color_index = 2
background_color_index = 3

# velger tilfeldig farge
colorNamesList =list(color_combinations.keys())
colorIndex = rd.randint(0,len(colorNamesList)-1)
prevColorIndex = colorIndex
randomColorName = colorNamesList[colorIndex]
randomFarge =[]
for color in color_combinations[randomColorName].values():
    randomFarge.append(color)

# funksjon for å endre farge på meny, tekst, overskrift og valgt tekst - velger tilfeldig farge
def endreFarge(startmeny, taster):
    global prevColorIndex
    
    if taster == "reload":
        colorNamesList =list(color_combinations.keys())
        colorIndex = rd.randint(0,len(colorNamesList)-1)

        while colorIndex ==prevColorIndex:
            colorIndex = rd.randint(0,len(colorNamesList)-1)

        prevColorIndex = colorIndex
        randomColorName = colorNamesList[colorIndex]
        randomFarge =[]
        for color in color_combinations[randomColorName].values():
            randomFarge.append(color)
        startmeny.bakgrunnsfarge=randomFarge[background_color_index]
        startmeny.tittelfarge=randomFarge[title_color_index]
        startmeny.tekstfarge=randomFarge[text_color_index]
        startmeny.valgfarge=randomFarge[select_color_index]
        
    elif taster[pygame.K_f]:
        colorNamesList =list(color_combinations.keys())
        colorIndex = rd.randint(0,len(colorNamesList)-1)

        while colorIndex ==prevColorIndex:
            colorIndex = rd.randint(0,len(colorNamesList)-1)

        prevColorIndex = colorIndex
        randomColorName = colorNamesList[colorIndex]
        print(randomColorName)
        randomFarge =[]
        for color in color_combinations[randomColorName].values():
            randomFarge.append(color)
        startmeny.bakgrunnsfarge=randomFarge[background_color_index]
        startmeny.tittelfarge=randomFarge[title_color_index]
        startmeny.tekstfarge=randomFarge[text_color_index]
        startmeny.valgfarge=randomFarge[select_color_index]
        
        pygame.time.delay(250)
        

# lager objekt for startmeny
startM = StartMeny(bakgrunnsfarge=randomFarge[background_color_index], tittelfarge=randomFarge[title_color_index], tekstfarge=randomFarge[text_color_index], valgfarge=randomFarge[select_color_index], valg=0)

#bilder
lyd_bilde = pygame.image.load(folderPath+r"/data/bilder/lyd.png")
lyd_av_bilde = pygame.image.load(folderPath+r"/data/bilder/lyd_av.png")

fly_bilde = pygame.image.load(folderPath+r"/data/bilder/fly.png")

# endre størrelse på bilder
lyd_bilde = pygame.transform.scale(lyd_bilde, (60, 60))
lyd_av_bilde = pygame.transform.scale(lyd_av_bilde, (50, 50))




# objekt for volume knapper
lyd_knapp = Knapp(x = vindu_bredde - 60, y = 0, bilde = lyd_bilde)
lyd_av_knapp = Knapp(x = vindu_bredde - 60, y = 0, bilde = lyd_av_bilde)

def startMenyen():
    global spillnavn
    global muteed
    global ingameTime
    pygame.init()
    
    pygame.mixer.set_num_channels(3)
    # backgroundTrackChannel = pygame.mixer.Channel(0)
    effectsChannel = pygame.mixer.Channel(2)
    backgroundTrackChannel = pygame.mixer.Channel(0)
    prankChannel = pygame.mixer.Channel(1)
    selectSound = pygame.mixer.Sound(folderPathSound+r"/selectMenu.wav")
    gameSelectedSound = pygame.mixer.Sound(folderPathSound+r"/gameSelected.wav")
    backgroundTrack = pygame.mixer.Sound(folderPathSound+r"/backgroundTrack.wav")
    esterTrack = pygame.mixer.Sound(folderPathSound+r"/ester.wav")
    planeSound = pygame.mixer.Sound(folderPathSound+r"/kult fly.ogg")
    
    # print(backgroundTrackChannel.get_busy())
    
    vindu_bredde = 900
    vindu_høyde = 500
    
    pygame.display.set_caption("Alle spillene er samlet her!")

    planeFlying = False
    
    if backgroundTrackChannel.get_busy()==False:
            # if rd.randint(0,1)==0:
            # prankChannel.play(planeSound)
            backgroundTrackChannel.play(backgroundTrack)
    
    
    # lager 2 fonts, den andre fonten brukes til å ha understrek under slik at ikke all teksten får understrek under seg
    font = pygame.font.SysFont('arial', 36)
    font2 = pygame.font.SysFont('arial', 36)
    vindu = pygame.display.set_mode((vindu_bredde, vindu_høyde))
    #starter spill
    fortsett = True
    while fortsett:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        ingameTime += clock.get_rawtime()
        clock.tick(10000)
        
        backgroundTrackChannel.set_volume(1)
        if muteed:
            backgroundTrackChannel.set_volume(0)
        
        if backgroundTrackChannel.get_busy()==False:
            if rd.randint(0,3)==0:
                prankChannel.play(planeSound)
                ingameTime = 0
                planeFlying=True
            backgroundTrackChannel.play(backgroundTrack)

        taster = pygame.key.get_pressed()
        
        endreFarge(startM,taster)
        startM.tegnStartMeny(font,font2,taster,vindu,selectSound,effectsChannel)
        if not muteed and lyd_knapp.draw(vindu):
            muteed = True
            if rd.randint(0,100)==1:
                prankChannel.set_volume(100)
                prankChannel.play(esterTrack)
        elif muteed and lyd_av_knapp.draw(vindu):
            muteed = False
        
        for i in range(len(spillListe)):
            if startM.skiftMeny(taster, i):
                spillnavn =spillListe[i]
                spillPath = r"/spill"+"/"+spillnavn+"/"+spillnavn+".py"
                effectsChannel.play(gameSelectedSound)
                pygame.time.delay(1000)
                fortsett=False
        
        # tekst = font.render(str(ingameTime),True,(0,0,0))
        # vindu.blit(tekst, (200,200))

        if planeFlying:
            vindu.blit(fly_bilde, [vindu_bredde -(vindu_bredde/10000)*ingameTime,vindu_høyde/2 -100])
                
        pygame.display.update()
    else: 
        pygame.quit()
        # quit()

while True:
    startMenyen()
    ## starter spillet
    endreFarge(startM, "reload")

    spillPath = r"/spill"+"/"+spillnavn+"/"+spillnavn+".py"
    print(folderPath+ spillPath)

    command = ['python', folderPath+spillPath]


    # Use subprocess to start the other Python script
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the process to finish and get the return code
    return_code = process.wait()

    # Check if the process exited successfully
    if return_code == 0:
        print("Script executed successfully.")
    else:
        print(f"Error: Script exited with return code {return_code}.")
    forsett = True


  