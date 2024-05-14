import os 
import sys 
import kultBiblotek2 as kB
import subprocess
import pygame

# Specify the command to start the other Python script

forsett = True


# finner mappen som filene ligger i
folderPath = os.path.dirname(os.path.abspath(sys.argv[0]))  #path til der filen fins
folderPathSpill = folderPath+r"/spill"  # path til spill folder
spillListe = os.listdir(folderPathSpill) #liste over alle spill i folder


#for pygame
# pygame.init()
vindu_bredde = 900
vindu_høyde = 500
# vindu = pygame.display.set_mode((vindu_bredde, vindu_høyde))
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
    def __init__(self, vindu, bakgrunnsfarge, valgfarge, valg):
        super().__init__(vindu, bakgrunnsfarge, valgfarge, valg)
        self.vindu = -1
        
    def tegnStartMeny(self, font, font2, taster,vindu):
        """ metode for å tegne start menyen """
        vindu.fill(self.bakgrunnsfarge) 
        title = pygame.font.SysFont('arial', 50).render("Alle Spill Samlet", True, (255, 255, 255))

        vindu.blit(title, (vindu_bredde/2 - title.get_width()/2, title.get_height()/2))

        if (taster[pygame.K_UP] or taster[pygame.K_w]) and self.valg > 0:
            self.valg -= 1
        if (taster[pygame.K_DOWN] or taster[pygame.K_s]) and self.valg < menyKonstant*1:
            self.valg += 1

        y_pos = title.get_height()
        
        for i in range(len(spillListe)):
            menylinje = skrift(spillListe[i], font, font2, (255,255,255), self.valgfarge, i, self.valg)
            y_pos += menylinje.get_height()
            x_pos = 100
            vindu.blit(menylinje, (x_pos, y_pos))

# lager objekt for startmeny
startM = StartMeny(0, (0,0,0),(132,165,247), 0)




def startMenyen():
    global spillnavn
    pygame.init()
    
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
        startM.tegnStartMeny(font,font2,taster,vindu)
        for i in range(len(spillListe)):
            if startM.skiftMeny(taster, i):
                spillnavn =spillListe[i]
                spillPath = r"/spill"+"/"+spillnavn+"/"+spillnavn+".py"
                fortsett=False
                # pygame.quit()
                # quit()

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


