import os 
import sys 
import kultBiblotek2 as kB
import subprocess
import pygame
import random as rd

forsett = True

# finner mappen som filene ligger i
folderPath = os.path.dirname(os.path.abspath(sys.argv[0]))  #path til der filen fins
folderPathSpill = folderPath+r"/spill"  # path til spill folder
spillListe = os.listdir(folderPathSpill) #liste over alle spill i folder

vindu_bredde = 900
vindu_høyde = 500

# dette er en konstant som kontrollerer hvor raskt det skal gå når vi trykker på piltastene basically - høyere tall = tregere
menyKonstant = 70

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
        return taster[pygame.K_SPACE] and menyKonstant*(antall-1)< self.valg <= menyKonstant*antall #and pygame.time.get_ticks() - tid > 1000
        
def skrift(tekst, font, font2, farge, farge2, antall, valg): # lager skrift på menyene, tegner underline hvis valg er innenfor et bestemt intervall
    menyvalg = font.render(tekst, True, farge)
    if menyKonstant*(antall-1)< valg <= menyKonstant*antall:
        font2.set_underline(True)
        menyvalg = font2.render(tekst, True, farge2)
    return menyvalg


class StartMeny(Meny):
    def __init__(self, bakgrunnsfarge, tittelfarge, tekstfarge, valgfarge, valg):
        super().__init__(bakgrunnsfarge,tittelfarge, tekstfarge, valgfarge, valg)

        
    def tegnStartMeny(self, font, font2, taster,vindu):
        """ metode for å tegne start menyen """
        vindu.fill(self.bakgrunnsfarge) 
        title = pygame.font.SysFont('arial', 50).render("Alle Spill Samlet", True,self.tittelfarge)
        vindu.blit(title, (vindu_bredde/2 - title.get_width()/2, title.get_height()/2))

        if (taster[pygame.K_UP] or taster[pygame.K_w]) and self.valg > 0:
            self.valg -= 1
        if (taster[pygame.K_DOWN] or taster[pygame.K_s]) and self.valg < menyKonstant*(len(spillListe)-1):
            self.valg += 1

        y_pos = title.get_height()
        x_pos = 100
        
        
        for i in range(len(spillListe)):
            menylinje = skrift(str(i+1) + ". " + spillListe[i], font, font2, self.tekstfarge, self.valgfarge, i, self.valg) 
            if i == 8:
                x_pos += vindu_bredde/2
                y_pos = title.get_height()
            y_pos += menylinje.get_height()
            vindu.blit(menylinje, (x_pos, y_pos))


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



def startMenyen():
    global spillnavn
    pygame.init()
    
    pygame.display.set_caption("Alle spillene er samlet her!")

    
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
        taster = pygame.key.get_pressed()
        endreFarge(startM,taster)
        startM.tegnStartMeny(font,font2,taster,vindu)
        for i in range(len(spillListe)):
            if startM.skiftMeny(taster, i):
                spillnavn =spillListe[i]
                spillPath = r"/spill"+"/"+spillnavn+"/"+spillnavn+".py"
                fortsett=False
                
        pygame.display.update()
    else: 
        pygame.quit()
        # quit()


# command = ['python', folderPath+spillPath]
# process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# # Wait for the process to finish and get the return code
# return_code = process.wait()

# # Check if the process exited successfully
# if return_code == 0:
#     print("Script executed successfully.")
# else:
#     print(f"Error: Script exited with return code {return_code}.")




# #spør bruker hvilket spill man skal kjøre
# print("")
# print("-"*20)
# print("Her er en liste over filer:")
# kB.print1DList(spillListe)

# brukerInput = kB.betterInput(variableType="int",inputText=f"Hvilken fil vil du ha?(0-{len(spillListe)-1}): ",errorText="Dette var ikke et heltall",forventet=[i for i in range(len(spillListe))])
# spillnavn =spillListe[brukerInput]




# #generer path til spillet
# spillPath = r"/spill"+"/"+spillnavn+"/"+spillnavn+".py"
# print(folderPath+ spillPath)






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


