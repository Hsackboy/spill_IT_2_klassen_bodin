import pygame as pg #Importerer forskjellige bibiloteker vi trenger for koden, i rekkefølge Pygame, math, random og pandas
import math as m
import random as rd
import pandas as pd
from pygame.locals import (#Importerer inn de forskjellige knappene vi skal bruke under koden
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_r,
    K_v
)
import os 
import sys 

# finner mappen som filene ligger i
folderPath = os.path.dirname(os.path.abspath(sys.argv[0])) 


# Initialiserer/starter pygame
pg.init()


# Oppretter et vindu der vi skal "tegne" innholdet med en viss bredde og hoyde
VINDU_BREDDE = 1000
VINDU_HOYDE = 600
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])


#Lager klasse for firkant
class Firkant:
    """"
    Oppretter en klasse for en firkant som vil brukes for å velge vanskelighetsgrad og markere valget av vanskelighetsgrad.
    Klassen tar inn en innput for lengden og høyden til firkanten
    """
    def __init__(self, lengde, hoyde,vente):
        """Konstruktør for klassen
        Oppretter self.lengde som er en variabel for lengden til firkanten og defineres av brukeren
        Oppretter self.hoyde som er en variabel for hoyden til firkanten og defineres av brukeren
        Oppretter self.ventetid som er en variabel som er tiden for mellom hvert bytte av posisjonen til firkanten. Dette er for å forhindre at firkanten hopper flere hopp på et lite trykk av piltasten men at hoppingen blir lettere å styre
        Oppretter self.plassering som er en variabel som bestemmer de tre mulige posisjonene til firkanten. Den settes til 1 for å vise at firkanten skal starte på posisjon 1 og derreter kan flyttes/hoppe til de neste posisjonene. 
        Oppretter self.siste_bytte_tid som er en variabel som tar tiden siden sist bytte av posisjonen til firkanten og fungerer da sammen med ventetid for å lage gode bytter
        """
        self.lengde = lengde
        self.hoyde = hoyde
        self.ventetid = vente
        self.plassering = int(1)
        self.siste_bytte_tid = 0

    def flytt(self, taster, nåverende_tid):
        """"Metode inne i klassen for å flytte klassen til en av de andre mulige posisjonene 
        basert på input av tastene som trykkes og nåværende tid og potensielt bytter self.plassering opp eller ned med 1 slik at firkanten får ny posisjon"""
        if taster[K_RIGHT] and self.plassering < 3: #Hvis høyre piltast trykkes og plasseringsvariabelen er mindre enn 3 går koden videre
            if nåverende_tid - self.siste_bytte_tid  > self.ventetid: #Hvis tiden nå - det tiden var ved forrige bytte er mer enn ventetiden som ligger på 300ms går koden videre. 
                #Dette gjør at det må gå 0.3 sek mellom hver gang firkanten kan flyttes og det gjør at firkanten kan flyttes på en mye lettere måte
                self.plassering += 1 #Hvis begge disse if-ene er oppfylt vil plasserings variabelen øke med 1 

                self.siste_bytte_tid  = nåverende_tid #Hvis begge if-ene er oppfylt vil også siste bytte tiden oppdateres til tiden som er ved dette byttet
        if taster[K_LEFT] and self.plassering > 1: #Gjør samme funksjon som if løkken med K_RIGHT og sjekker om venstre pil trykkes inn samtidig som om plassering er større enn 1
            if nåverende_tid - self.siste_bytte_tid  > self.ventetid:#Sjekker helt samme ting som linjen over om tid, altså om tiden som har gått siden siste bytte er større enn 0.3 sekund
                self.plassering -= 1 #Hvis begge er oppfylt minker plassering med 1
                self.siste_bytte_tid  = nåverende_tid #Hvis if-ene er oppfylt oppdateres tiden for siste bytte

    def tegn(self): 
        """"Metode inne i klassen som tegner firkanten basert på hva plasseringsvariabelen er"""
        ypos=500 #Setter y posisjonen til 500
        if self.plassering == 1: #Hvis plasserings variabelen er 1 settes x posisjons variabelen til 100
            xpos=100
        elif self.plassering == 2: #Hvis plasserings variabelen er 2 settes x posisjons variabelen til 400
            xpos=400
        elif self.plassering == 3: #Hvis plasserings variabelen er 3 settes x posisjons variabelen til 800
            xpos=800
        pg.draw.rect(vindu, (253, 127, 57), (xpos, ypos, self.lengde, self.hoyde)) #Tegner firkanten ved bruk av pg.draw.rect med innputtene (vindu,(Farge i rgb format),(x posisjon, y posisjon, lengde, høyde))

    def spillstart(self, taster):
        """"Metode inne i klassen som setter vanskelighetsgraden til spillet basert på firkantens posisjon
           Setter også spillet videre til neste fase. Metoden bruker tastene som trykkes som input"""
        if taster[K_SPACE]: #Hvis Space-knappen trykkes går koden inn
            global Vanskelighetsgrad #Setter vanskelighetsgrad variabelen til global og henter den inn. Det betyr at varibelen ikke bare gjelder innenfor denne metoden men også for hele koden
            if self.plassering == 1: #Hvis plasserings variabelen er 1 settes vanskelighetsgraden til 1
                Vanskelighetsgrad = 1
            elif self.plassering == 2: #Hvis plasserings variabelen er 2 settes vanskelighetsgraden til 2
                Vanskelighetsgrad = 2
            elif self.plassering == 3: #Hvis plasserings variabelen er 3 settes vanskelighetsgraden til 3
                Vanskelighetsgrad = 3
            global Spill_fase #Setter Spill_Fase variabelen til global og henter den inn. Det betyr at varibelen ikke bare gjelder innenfor denne metoden men også for hele koden
            Spill_fase = 1 #Spill_fase variabelen settes til 1 som fører spillet videre til neste fase


#Lager klasse for bullet/skuddene
class Bullet:
    """"
    Oppretter en klasse for skuddene som vil skytes som også inneholder metode for å flytte og tegne skuddene
    Klassen tar inn en innput for x posisjon, y posisjon, fart i x retning og bilde. """
    def __init__(self, x, y, fart, bilde):
        """Konstruktør for klassen
        Oppretter self.x som er en variabel for x posisjonen til skuddet og som defineres av brukeren
        Oppretter self.y som er en variabel for y posisjonen til skuddet og som defineres av brukeren
        Oppretter self.fart som er en variabel for farten til skuddet i x retning og som defineres av brukeren
        Oppretter self.bilde som er en variabel som henviser til bildet som skal vise skuddet og som også defineres av brukeren
        """
        self.x = x
        self.y = y
        self.fart = fart
        self.bilde = bilde

    def tegn(self):
        """"Metode som tegner skuddet inn i vinduet basert på egen posisjon og bilde"""
        vindu.blit(self.bilde, (self.x, self.y)) #Tegner inn skuddet i vinduet ved bruk av vindu.blit med inputtene (bilde,(x-posisjon,y-posisjon))

    def flytt(self):
        """"Metode som flytter skuddet basert på farten, siden skuddet bare beveger seg i x retning vil bare x posisjonen endres"""
        self.x += self.fart #Endrer x posisjonen med størrelsen til farten slik at skuddet beveger seg i x retning mot enden av skjermen på høyre side


#Lager klasse for helten som arver fra bullet/skuddene
class Helt(Bullet):
    """Oppretter en klasse for å representere helten/ figuren spilleren bruker. 
    Klassen arver ned variablene x posisjon, y posisjon, fart og bilde fra Bullet klassen
    I tilegg tar klassen også inn variablen bilde 2 som brukeren oppgir + variablene siste_skudd_tid og mellomromholdes som er ferdigdefinert i konstruktøren og som ikke oppgis under skapelsen av objektet"""

    def __init__(self, x, y, fart, bilde,bilde2):
        """"Konstuktør som arver fra Bullet
        Variablene self.x, self.y, self.fart og self.bilde er arvet fra Bullet. 
        Oppretter self.bilde2 som er en variabel som henviser til et bildet som vil brukes når helten skyter et skudd som defineres av brukeren. 
        Oppretter self.siste_skudd_tid som er en variabel for når det siste skuddet ble avfyrt som brukes til at bildet som viser helten som skytes vises litt lengre. Den blir definert til 0 her men vil bli kontinuerlig oppdatert mens selve spillet pågår
        Oppretter self.mellomromholdes som settes her til false og som brukes under selve koden til å forhindre at spilleren bare holder inn mellomrom men faktisk trykker så raskt vedkommene kan. 
        """
        super().__init__(x, y, fart, bilde)
        self.bilde2 = bilde2
        self.siste_skudd_tid = 0
        self.mellomromholdes = False

    def tegn_skyt(self, taster, nåverende_tid):
        """Metode for å tegne Helten men også for å lage skuddene
        Tar inn tastene som trykkes og tiden nå som inputer"""
        if taster[K_SPACE] and not self.mellomromholdes: #Hvis Space blir trykt inn og mellomromholdes inne er false går koden videre
            vindu.blit(self.bilde2, (self.x, self.y)) #Tegner bilde 2 som er bildet som viser helten som skyter i vinduet ved bruk av vindu.blit med input av bildet og x/y posisjonene
            nytt_skudd = Bullet(self.x + 140, self.y + 102, 9, skudd_skalert) #Oppretter ett nytt objekt for skuddet ved bruk av Bullet klassen med inputtene av helten sin x og y posisjon samt bildet til skuddet. 
            #Grunnen til at posisjonene plusses på litt mer er for at skudden skal spawne ved våpenet og ikke ved øvre venstre hjørne av figuren
            Kuler.append(nytt_skudd) #Legger dette nye Bullet objektet inn i en liste som inneholder alle skuddene
            self.siste_skudd_tid = nåverende_tid #Setter variabel for tiden sist skudd var til det tiden er nå
            self.mellomromholdes = True #Setter mellomromholdes til true som forhindrer at spilleren kan holde inne mellomrom og skyte mange skudd men må trykke
        elif nåverende_tid - self.siste_skudd_tid < 200: #Hvis tiden mellom siste skudd og nå er mindre enn 0.2 sekunder vil bildet av helten som skyter vises. 
            #Dette gjør at skyte-bildet vil vises i 0.2 sekunder slik at vi rekker å se det istedet for at det skal flashe over skjermen i en tick/1ms
                vindu.blit(self.bilde2, (self.x, self.y))#Tegner helten som skyter i vinduet ved bruk av blit
        else: #Hvis ingen av de to tilfellene ovenfor er innfridd vil vi istedet for tegne bildet av helten som ikke skyter
            vindu.blit(self.bilde, (self.x, self.y)) #Tegner helten som ikke skyter men holder våpnet ved bruk av blit
        if not taster[K_SPACE]: #Hvis mellomrom/space ikke holdes inne vil mellomromholdes settes tilbake til false og dermed vil man igjen kunne lage et nytt skudd hvis man trykker space inn
            self.mellomromholdes = False #Setter self.mellomromholdes til false

    def flytt(self, taster):
        """Metode for å flytte helten opp og ned mellom de to banene og passe på at helten ikke går utenfor skjermen
        Tar inn trykkede taster som innputt"""
        if taster[K_UP] and self.y > 0: #Hvis pil-opp trykkes inn samtidig som y posisjonen er større en 0 som betyr at helten ikke berører toppen av vinduet går løkken videre
            self.y -= self.fart #Y posisjonen til helten flyttes nedover med størrelsen til heltens fart
        if taster[K_DOWN] and self.y < VINDU_HOYDE - helt1s_skalert.get_height(): #Hvis pil-ned trykkes inn samtidig som y posisjonen er mindre en vinduets høyde - heltens høyde som betyr at helten ikke berører bunnen av vinduet går løkken videre
            self.y += self.fart #Y posisjonen til helten flyttes oppover med størrelsen til heltens fart


#Lager klasse for monstrene som arver fra bullet/skuddene
class Monster(Bullet):
    """Oppretter en klasse for å representere monsteret/ figuren som er motstanderen til spilleren. 
    Klassen arver ned variablene x posisjon, y posisjon, fart og bilde fra Bullet klassen
    I tilegg tar klassen også inn variablene monster_liv og start_liv der monster_liv defineres av inputten til å skape objektet og start_liv settes til monster_liv"""
    def __init__(self, x, y, fart, bilde, monster_liv):
        """"Konstuktør som arver fra Bullet
        Variablene self.x, self.y, self.fart og self.bilde er arvet fra Bullet. 
        Oppretter self.monster_liv som er en variabel for hvor mange liv monsteret har og som defineres av brukeren men som også går ned når monsteret blir skutt
        Oppretter self.start_liv som er en variabel som settes til hvor mange liv monsteret starter med men som ikke endres når monsteret blir skutt. Den blir brukt for å lage fine healthbars. 
        """
        super().__init__(x, y, fart, bilde)
        self.monster_liv = monster_liv
        self.start_liv = self.monster_liv

    def flytt(self):
        """"Metode for å flytte monsteret, sidenm monsteret bare beveger seg i x retning vil denne bare påvirke x posisjonen"""
        self.x -= 2*self.fart #Endres x posisjonen med dobbelte av den negative verdien av farten til monsteret

    def tegn(self):
        """"Metode for å tegne monsteret samt også tegne healthbar over hodet til monsteret"""
        vindu.blit(self.bilde, (self.x, self.y)) #Tegner inn selve monsteret ved blit og self variablene for x, y og bilde
        #Nedenfor brukes pg.draw.rect som tegner inn rektangler, her basert på innputtene(vindu,(farge i rgb format),(x posisjon,y posisjon, bredde,høyde))
        pg.draw.rect(vindu, (255, 255, 255), (self.x, self.y - 12, self.bilde.get_width(), 8)) #Tegner inn selve hvite outlinen til healthbaren med utgangspunkt i heltens x posisjon, 12 pixler over helten, heltens bredde og 8 pixler i høyde.
        #Fargen(255,255,255) er maks av alle farger og gir en hvit farge som vi ønsker til outlinen
        pg.draw.rect(vindu,(0, 128, 0),(self.x + 1,self.y - 11,self.bilde.get_width() * (self.monster_liv / self.start_liv)-2,6)) #Tegner inn selve grønne markøren for hvor mange liv som er igjen med fargen (0,128,0) som da gir grønn fargen vi ønsker
        #Videre tar den også inn (x posisjonen til monsteret +1,y posisjon -11,monsterets bredde * brøken som skapes av resterende liv delt på liv i starten minus 2,6) 
        #Hvis du ser etter er forskjellen mellom denne grønne healtbaren og den hvite outlinen 1 i de to første feltene og 2 i de to siste feltene og dette er slik at den grønne alltid blir litt mindre og den hvite alltid blir en outline


#Lager en metode for å lage monstre
def Lag_Monster(tid_nå):
    """"Oppretter en metode/funksjon som lager monstrene ved hjelp av Monster klassen
    Metoden tar inn tiden nå som input"""
    global start_lage_monster #Setter variabelen start_lage_monster til global som betyr at den gjelder også for inni denne koden og endringer inni funksjon vil da også gjelde utenfor
    if start_lage_monster == 0: #Hvis start lage monster er 0 vil start_lage_monster settes til å være tiden når denne funksjonen først brukes. Dermed vil den bare bli satt en gang.
        start_lage_monster = tid_nå#Start lage monster tid settes til tiden som er når funksjonen blir brukt
    raskere_av_tid = (tid_nå - start_lage_monster) / 50 #Oppretter en variabel kalt raskere av tid som defineres av tiden mellom første monster og nå delt på 50. 
    #Denne variabelen vil hele tiden vokse og bruker lengre ned slik at spillet blir vanskeligere etterhvert som tiden går

    global siste_monster_tid  #Setter variabelen siste_monster_tid til global som betyr at den gjelder også for inni denne koden og endringer inni funksjon vil da også gjelde utenfor metoden
    maks_forsinkelse = 2500 #Maks forsinkelse mellom 2 monster settes til 2500 ms
    tilfeldig_forsinkelse = rd.randint(0, maks_forsinkelse) #En tilfeldig forsinkelse velges basert på random.randint fra 0 til maks forsinkelse(2500 ms)

    if Vanskelighetsgrad == 1: #Hvis vanskelighetsgraden er 1 går koden videre
        start_tid = 1000 - raskere_av_tid #Variabelen starttid settes til å være 1000ms - raskere av tid variabelen
        monster_fart = 1 + ((rd.randint(0, 500)) / 1000) #Farten til monsteret blir satt til 1 + et tilfeldig tall som til slutt blir mellom 0-0.5
        monster_liv = rd.randint(2, 4) #Livene monsteret skal ha blir et tilfeldig tall fra og med 2 til og med 4
    elif Vanskelighetsgrad == 2: #Denne pluss de tre neste linjene gjør nøytaktig samme tingen som linjene ovenfor bare med litt andre tall som gjør at spillet skal bli vanskeligere, 
        #dermed kan man bare se på kommentarene ovenfor og se om noen av tallene er byttet om. Samme gjelder for når vanskelighetsgrad=3 elif-en.
        start_tid = 750 - raskere_av_tid
        monster_fart = 1 + ((rd.randint(0, 1000)) / 1000)
        monster_liv = rd.randint(2, 5)
    elif Vanskelighetsgrad == 3:
        start_tid = 600 - raskere_av_tid
        monster_fart = 1 + ((rd.randint(0, 1500)) / 1000)
        monster_liv = rd.randint(3, 6)

    monster_forsinkelse = start_tid + tilfeldig_forsinkelse #Variabelen monster_forsinkelse settes til å være start_tid + tilfeldig forsinkelse, begge som er variabler som ble definert ovenfor
    if tid_nå - siste_monster_tid > monster_forsinkelse: #Hvis tiden mellom nå og forrige monster er større enn monster_forsinkelse vil koden gå videre og et nytt monster vil bli skapt
        tilfeldig_monster = rd.randint(1, 6) #Velger et tilfeldig tall fra og med 1 til og med 6 og basert på dette tallet velges det hvordan bildet det nye monsteret får slik at det er tilfeldig hvordan rekkefølge de ulike monster-utseende kommer i
        if tilfeldig_monster == 1: #Sjekker om det tilfeldige tallet er 1, og hvis ja blir det monster1_skalert som blir bildet for monsteret. Dette samme skjer med nye tall for de 11 neste linjene
            monster_skalert = monster1_skalert
        elif tilfeldig_monster == 2:
            monster_skalert = monster2_skalert
        elif tilfeldig_monster == 3:
            monster_skalert = monster3_skalert
        elif tilfeldig_monster == 4:
            monster_skalert = monster4_skalert
        elif tilfeldig_monster == 5:
            monster_skalert = monster5_skalert
        else:
            monster_skalert = monster6_skalert

        tilfeldig_tall = rd.randint(1, 2)#Velger et tilfeldig tall fra og med 1 til og med 2.
        if tilfeldig_tall == 1: #Hvis tallet er 1 går koden videre og monsteret blir "spawnet" i nederste monsterbane
            høyde=350 #Setter høyde til 350 slik at monsteret kommer i nedre bane
        elif tilfeldig_tall == 2:#Hvis tallet er 2 går koden videre og monsteret blir "spawnet" i øverste monsterbane
            høyde=80 #Setter høyde til 80 slik at monsteret kommer i øvre bane
        nytt_monster = Monster(VINDU_BREDDE, høyde, monster_fart, monster_skalert, monster_liv) #Skaper et nytt monster-objekt med innputtene Vindu_Bredde slik at monsteret spawner helt på høyre side, 
        # Høyde for y slik at den spawner i riktig høyde, monster_fart som ble definert ovenfor som farten, monster_skalert som bildet til monsteret også definert ovenfor og til slutt monster_liv som også ble definert ovenfor
        Monstre.append(nytt_monster) #Legger til dette nye monsteret inn i listen for monstre
        siste_monster_tid = tid_nå  # Oppdaterer verdien av siste_monster_tid til det tiden er nå


#Lager en metode for å sjekke om highscoren er slått og justere csv-filen
def highscoresjekker(Vanskelighetsgrad, Scoren):
    """"Oppretter en metode/funksjon som sjekker om scoren din er stor nok til å slå highscoren som står i csv-filen
    Metoden tar inn vanskelighetsgraden og scoren som innputter"""
    global df #Setter df variabelen til global som gjør at den gjelder for hele koden
    Score = float(Scoren)#Scoren settes til en float variabel
    if Vanskelighetsgrad == 1:#Hvis vanskelighetsgraden er 1 sjekker vi scoren opp mot highscore1 som gjelder for nivå 1
        if Score > highscore1: #Hvis scoren er større enn highscore1 går vi videre
            df.loc[0, 'Highscore1'] = Score #Vi går inn i df som er et sett for highscorene og går  i kollonne highscore1 og tallet 0 sier vi skal gå i første rad under. I denne cellen endrer vi nå verdien til score
            df.to_csv(folderPath+r"/Highscore.csv", index=False) #Denne linjer laster opp endringene vi gjorde i linjen over i datasettet opp til csvfilen kalt highscore.csv, Index=false gjør at indexene til radene ikke skal lastes opp til csv-filen
    if Vanskelighetsgrad == 2:#Hvis vanskelighetsgraden er 2 sjekker vi scoren opp mot highscore2 som gjelder for nivå 3
        if Score > highscore2:#Hvis scoren er større enn highscore3 går vi videre
            df.loc[0, 'Highscore2'] = Score#Vi går inn i df som er et sett for highscorene og går  i kollonne highscore2 og tallet 0 sier vi skal gå i første rad under. I denne cellen endrer vi nå verdien til score
            df.to_csv(folderPath+r"/Highscore.csv", index=False)#Denne linjer laster opp endringene vi gjorde i linjen over i datasettet opp til csvfilen kalt highscore.csv, Index=false gjør at indexene til radene ikke skal lastes opp til csv-filen
    if Vanskelighetsgrad == 3:#Hvis vanskelighetsgraden er 3 sjekker vi scoren opp mot highscore3 som gjelder for nivå 3
        if Score > highscore3:#Hvis scoren er større enn highscore3 går vi videre
            df.loc[0, 'Highscore3'] = Score#Vi går inn i df som er et sett for highscorene og går  i kollonne highscore3 og tallet 0 sier vi skal gå i første rad under. I denne cellen endrer vi nå verdien til score
            df.to_csv(folderPath+r"/Highscore.csv", index=False)#Denne linjer laster opp endringene vi gjorde i linjen over i datasettet opp til csvfilen kalt highscore.csv, Index=false gjør at indexene til radene ikke skal lastes opp til csv-filen


# Linjene under laster inn bilder for bakgrunn, helten, skudd og monster ved bruk av pg.image.load
bakgrunn = pg.image.load(folderPath+r"/bakgrunn.png")
monster1 = pg.image.load(folderPath+r"/monster1.png")
monster2 = pg.image.load(folderPath+r"/monster2.png")
monster3 = pg.image.load(folderPath+r"/monster3.png")
monster4 = pg.image.load(folderPath+r"/monster4.png")
monster5 = pg.image.load(folderPath+r"/monster5.png")
monster6 = pg.image.load(folderPath+r"/monster6.png")
helt1 = pg.image.load(folderPath+r"/helt1.png")
helt1s = pg.image.load(folderPath+r"/helt1s.png")
skudd = pg.image.load(folderPath+r"/skudd.png")
slutt = pg.image.load(folderPath+r"/taper.png")
start = pg.image.load(folderPath+r"/start.png")
beskrivelse = pg.image.load(folderPath+r"/beskriv.png")


# Skalerer alle bildene til riktig størrelse for å passe inn til spillet. Dette gjøres ved pg.transform med inputene(orginalbildet,(tall for bredde, tall for hoyde))
Monsterhoyde = 150 #Lager en konstant for høyden til monstrene slik at de får lik høyde under skaleringen
Monsterbredde = 80 #Lager en konstant for bredden til monstrene slik at de får lik bredde under skaleringen
bakgrunn_skalert = pg.transform.scale(bakgrunn, (VINDU_BREDDE, VINDU_HOYDE))
monster1_skalert = pg.transform.scale(monster1, (Monsterbredde, Monsterhoyde))
monster2_skalert = pg.transform.scale(monster2, (Monsterbredde, Monsterhoyde))
monster3_skalert = pg.transform.scale(monster3, (Monsterbredde, Monsterhoyde))
monster4_skalert = pg.transform.scale(monster4, (Monsterbredde, Monsterhoyde))
monster5_skalert = pg.transform.scale(monster5, (Monsterbredde, Monsterhoyde))
monster6_skalert = pg.transform.scale(monster6, (Monsterbredde, Monsterhoyde))
helt1_skalert = pg.transform.scale(helt1, (helt1.get_width() / 1.8, helt1.get_height() / 1.8))
helt1s_skalert = pg.transform.scale(helt1s, (helt1s.get_width() / 1.8, helt1s.get_height() / 1.8))
skudd_skalert = pg.transform.scale(skudd, (skudd.get_width() / 3, skudd.get_height() / 3))
slutt_skalert = pg.transform.scale(slutt, (VINDU_BREDDE, VINDU_HOYDE))
start_skalert = pg.transform.scale(start, (VINDU_BREDDE, VINDU_HOYDE))
beskrivelse_skalert = pg.transform.scale(beskrivelse, (VINDU_BREDDE, VINDU_HOYDE))


# Lager verdi for Vanskelighetsgrad:
Vanskelighetsgrad = 0


# Lager klokke for å holde styr på tiden for når det skal lages skudd og monstre ved bruk av time.clock fra pygame biblioteket
klokke = pg.time.Clock()


#Lager variabel for å laste inn highscore ved start av spillet
Highscorelad=True

#Oppretter to variabler som begge trengs for å lage monstre
start_lage_monster = 0 #Variabel 1 vil under monster lager funksjonen bli satt til tiden da det startes å produsere monstre
siste_monster_tid = 0 #Variabel 2 vil under monster lager funksjonen bli satt til det tiden var når forrige monster ble laget


# Lager objektene til spillet, en helt som lages av helt klassen og et rektangel som opprettes av firkant klassen
Helten = Helt(70, 200, 5, helt1_skalert, helt1s_skalert)
Firkanten = Firkant(90, 70,300)


# Lager liste for å inneholde alle skudd og alle monstre vi skal bruke/ha under spillet
Kuler = []
Monstre = []


# Lager score variabel som holder tellingen på hva scoren er og lager en variabel som brukes for å ta opp en start tid som starter når selve spillet starter
Score = 0
starte_score = True


#Lager en variabel som tracker hvilket fase spillet er i(introskjerm, sluttskjerm, hovedspill, loadingscreen), og en variabel som brukes for å starte tiden under loading screenen slik at den slutter etter riktig tid
Spill_fase = 0
Bytte_fase = True


# Starter spillet ved å sette fortsett til true og kjøre spillet så lenge fortsett fortsatt er true
fortsett = True
while fortsett:
    # Sjekker om brukeren har lukket vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False   #Setter fortsett til false som da betyr at spillet avsluttes


    # Lager to variabler
    nåverende_tid = pg.time.get_ticks()   #Variabel 1 inneholder nåværende tid som settes ved antall ticks(ticks er det samme som millisekund) som da holder tellingen på hvor lenge spillet har gått
    trykkede_taster = pg.key.get_pressed()#Variabel 2 inneholder alle taster som blir trykket på nåværende tidspunkt

    
    #Starter første spillfase som da er introbilde som lar deg bestemme vanskelighetsgrad
    if Spill_fase == 0: #Hvis spillfase er 0 vil denne koden kjøre

        if Highscorelad==True: #Hvis highscorelad er 0 lastes highscorene inn
            #Laster inn highscorene fra en csv fil
            df = pd.read_csv(folderPath+r"/Highscore.csv", delimiter=",")#Vi bruker read_csv fra pandas biblioteket til å lagre dataen fra csv-filen inn i df variabelen og vi definerer også at variablene er skillet med ,
            highscore1 = df["Highscore1"][0] #De tre neste linjene gjør det samme og går til kolonnen market med highscore 1,2 eller 3 og henter verdien fra første rad under overskriften og lagrer de som highscor 1,2 og 3
            highscore2 = df["Highscore2"][0]
            highscore3 = df["Highscore3"][0]
            Highscorelad=False #Settes til følse slik at det ikke lastes flere ganger

        vindu.blit(start_skalert, (0, 0)) #Tegner inn bakgrunnsskjermen til introen
        Firkanten.tegn() #Tegner inn firkantvariabelen
        Firkanten.flytt(trykkede_taster, nåverende_tid)#Bruker funksjonen til firkanten som da flytter firkanten basert på tastenen som trykkes og nåværende tid
        Firkanten.spillstart(trykkede_taster)#Bruker metoden spillstart i firkant til å sjekke om space trykkes og spillet skal starte

        font = pg.font.SysFont("Arial", 60) #Definerer fonten vi ønsker når vi skriver inn highscoren
        tidtekst = font.render(str(highscore1), True, (255, 255, 255))#Denne og de 5 linjene under tar alle å lager en variabel tidtekst som inneholder det vi vil tenge og derreter tegner inn tidtekst i vinduet. Disse linjene tegner altså da inn de 3 tidligere highscorene
        vindu.blit(tidtekst, (110, 345))
        tidtekst = font.render(str(highscore2), True, (255, 255, 255))
        vindu.blit(tidtekst, (450, 350))
        tidtekst = font.render(str(highscore3), True, (255, 255, 255))
        vindu.blit(tidtekst, (800, 350))


    elif Spill_fase == 1: #Hvis spillfase er 1 starter denne delen
        loading_tid=3000 #Lager en variabel kalt loading tid som er for hvor lenge denne fasen skal vare
        if Bytte_fase == True: #Hvis byttefase er sant settes byttetid til det tiden er når denne gjennomgås og byttefase settes til false igjen. 
            #Dette gjør at byttetid blir en variabel for tiden for første gjennomgang av spillfase og brukes til å kalkulere hvor lenge det skal gå før vi går videre
            byttetid = nåverende_tid
            Bytte_fase = False

        vindu.blit(beskrivelse_skalert, (0, 0))#Tegner inn bildet beskrivelse skalert som blir bakgrunnen og inneholder innstrukser for hvordan spillet funker
        pg.draw.rect(vindu, (255, 255, 255), (50, 300, 900, 150)) #På samme måte som healthbarene til mostrene tegner vi inn her en loadingbar der denne linjen er den hvite outlinen og linjen under er den grønne loadingbaren
        pg.draw.rect(vindu,(0, 130, 0),(70, 320, 840 * ((nåverende_tid - byttetid) / loading_tid), 110),) #Se kommentarene i metoden tegn til monsterklassen for mer nøyaktig. 
        #Eneste forskjellen er at her lages bredden basert på tiden som går gått siden byttet, delt på totale tiden som skal gå, det gjør baren mer fin i endringen

        if nåverende_tid - byttetid > loading_tid:#Når tiden fra starten av denne fasen når loading_tid settes spillet videre til hovedfasen som er Spill_fase 2
            Spill_fase = 2


    elif Spill_fase == 2: #Hvis spillfase er 2 starter selve spillet

        if Highscorelad==True: #Hvis highscorelad er 0 lastes highscorene inn
            #Laster inn highscorene fra en csv fil
            df = pd.read_csv(folderPath+r"/Highscore.csv", delimiter=",")#Vi bruker read_csv fra pandas biblioteket til å lagre dataen fra csv-filen inn i df variabelen og vi definerer også at variablene er skillet med ,
            highscore1 = df["Highscore1"][0] #De tre neste linjene gjør det samme og går til kolonnen market med highscore 1,2 eller 3 og henter verdien fra første rad under overskriften og lagrer de som highscor 1,2 og 3
            highscore2 = df["Highscore2"][0]
            highscore3 = df["Highscore3"][0]
            Highscorelad=False #Settes til følse slik at det ikke lastes flere ganger

        Lag_Monster(nåverende_tid)#Vi kjører gjennom Lag_monster for å lage monstre til Monster_listen
        vindu.blit(bakgrunn_skalert, (0, 0)) #Vi tegner inn bakgrunnsbildet

        if starte_score == True: #Vi gjør helt samme tingen som i spillfase 1 som er at vi definerer Start_score_tid som blir tiden for når spillfase 2 startet. 
            Start_score_tid = nåverende_tid
            starte_score = False

        Score = round((nåverende_tid - Start_score_tid) / 1000, 1)#Definerer score variabelen som tiden som har gått /1000 slik at vi får den i sekund istedet for ms
        font = pg.font.SysFont("Arial", 36) #Definerer fonten
        tidtekst = font.render("Score:" + str(Score), True, (255, 255, 255)) #Oppretter tekstvariabelen vi vil plotte opp på skjermen for scoren
        vindu.blit(tidtekst, (850, 15)) #Tegner inn score variabelen i vinduet

        Helten.tegn_skyt(trykkede_taster, nåverende_tid)#Tegner helten inn i vinduet og potensielt lager skudd basert på input av tastene og tiden
        Helten.flytt(trykkede_taster) #Flytter helten basert på piltastene opp og ned
        
        monstre_som_skal_beholdes = [] #Lager en liste for alle skuddene vi skal beholde
        for monst in Monstre: #Går igjennom listen som inneholder alle monstrene
            monst.tegn() #Tegner hvert eneste monster inn i vinduet basert på monster klassens tegn metode
            monst.flytt() #Flytter hvert eneste monster basert på monster klassens flytt metode
            if  monst.monster_liv > 0: #Hvis monsteret har over 0 liv igjen altså minst 1 liv så vil monsteret bli lagt til i listen over monstre som skal beholdes
                monstre_som_skal_beholdes.append(monst)
            if monst.x < 250: #250 er omentrent grensen der monsterbanen slutter. Dermed så vil koden gå videre hvis et monster når enden og da har du basicaly tapt
                Spill_fase = 3 #Siden et monster nådde slutten taper du spillet og spill_fase settes til 3 som er verdien som gjelder for sluttskjermen
        Monstre = monstre_som_skal_beholdes #Monster listen settes til å være listen av monstre som skal beholdes. På denne måten vil bare monstre med minst 1 liv forbli igjen

        skuddene_som_skal_beholdes = []#Lager en liste for skuddene som skal beholdes
        for skudd in Kuler: #Går gjennom alle skuddene som er i listen for skudd
            skudd.tegn() #Tegner inn allle skuddene basert på bullet klassens tegn metode
            skudd.flytt() #Flytter alle skuddene basert på Bullet klassens flytt metode
            treff = False  #Legger til variabel for å sjekke om skuddet treffer et monster
            for monst in Monstre: # Går gjennom listen med monstre og de neste fire linjene sjekker om et skudd treffer et av monstrene
                if (
                    skudd.x + skudd.bilde.get_width() >= monst.x #Denne linjen sjekker om skuddet er kommet langt nok bortover skjermen i x retning for å treffe et skudd ved å ta x posisjonen+ bildets bredde og sjekke om det er like langt som monsterets x posisjon
                    and skudd.y + skudd.bilde.get_height() >= monst.y #Denne linjen sjekker om bunnen av skuddet som vi får fra skudd.y+bildets høyde er lengre ned enn toppen av bildet til monstre(monst.y)
                    and skudd.y <= monst.y + monst.bilde.get_height() #Denne linjen sjekker om toppen av skuddet(skudd.y) er lengre opp en bunnen av monsteret (monst.y + monsterets høyde)
                    ):
                    monst.monster_liv -= 1 #Hvis et skudd innfrir de tre betingelsene får monsteret dette skuddet traff 1 mindre liv
                    treff = True #Vi setter også treff variabelen til True
                    break  # Avslutt løkken siden skuddet har truffet et monster og et skudd kan bare treffe et monster
            if (not treff and skudd.x < VINDU_BREDDE):  #Hvis skuddet ikke har truffet et monster og er ikke nådd enden av skjermen vil skuddet bli lagt til i listen over skuddene som skal beholdes
                skuddene_som_skal_beholdes.append(skudd) 
        Kuler = skuddene_som_skal_beholdes #Oppdaterer listen med alle skuddene til å bare være skuddene vi vil beholde
        

    elif Spill_fase == 3: #Hvis spillfase er tre går vi videre
        Monstre=[] #Vi tømmer listene for monstre og kuler i tilfelle spilleren vil spille på nytt
        Kuler=[]
        start_lage_monster = 0 #Både denne og neste variabel må også være 0 for at spillet skal starte opp riktig hvis spilleren vil restarte
        siste_monster_tid = 0 
        starte_score = True #Start score og bytte fase settes begge til true siden de må være det for at spillet skal starte på riktig måte
        Bytte_fase = True
        Highscorelad = True
        vindu.blit(slutt_skalert, (0, 0)) #Tegner inn slutt bakgrunnen
        highscoresjekker(Vanskelighetsgrad, Score) #Sjekker om scoren din har slått highscoren ved highscoresjekker funksjonen og muligens oppdaterer csv filen da
        font = pg.font.SysFont("Arial", 80) #Lager font
        scoretekst = font.render("Scoren din ble:" + str(Score), True, (255, 255, 255))#Lager selve teskten du vil tegne på sluttskjermen for å vise det scoren din ble
        vindu.blit(scoretekst,(200,200)) #Tenger inn sluttscoren din på sluttskjermen
        font = pg.font.SysFont("Arial", 35) #Lager en ny font
        infotekst = font.render("Trykk på R for å restarte samme nivå og V for å endre vanskelighetsgrad", True, (255, 255, 255)) #Lager teksten med intrukser for hvordan starte på nytt
        vindu.blit(infotekst,(50,320)) #Tegner inn disse instruksene
        if trykkede_taster[K_v] or trykkede_taster[K_r]: #Hvis R eller V trykkes går koden videre
            Score = 0 #Score nullstilles
            if trykkede_taster[K_r]: #Hvis R ble trykket settes spillfase til 2 som betyr du starter rett inn på spillet igjen
                Spill_fase=2
            elif trykkede_taster[K_v]: #Hvis V ble trykket går du tilbake til skjermen for å velge vanskelighetsgrad
                Spill_fase=0
    pg.display.flip() #Viser inn endringene du har gjort på skjermen
    klokke.tick(60) #Setter det slik at spillet skal ha en fps(Frames per sekund) på 60
pg.quit()#Avslutter pygame