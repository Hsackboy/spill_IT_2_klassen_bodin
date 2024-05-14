import pygame as pg
from pygame.locals import K_d,K_SPACE
import random
from playerClassv2 import *
from obsticalClassv2 import *
from filLeserBiblotek2 import *
import os 
import sys 

# finner mappen som filene ligger i
folderPath = os.path.dirname(os.path.abspath(sys.argv[0])) 

#starter pygame
pg.init()

#varibaler som brukes til lyd
pg.mixer.set_num_channels(2)
startSangIndex =0
antallSanger = 6
backgroundTrackChannel = pg.mixer.Channel(0)
effectsChannel = pg.mixer.Channel(1)
jumpSound = pg.mixer.Sound(folderPath+r"/data/jump.mp3")
powerUpSound = pg.mixer.Sound(folderPath+r"/data/powerUp.mp3")

effectsChannel.set_volume(2)
backgroundTrackChannel.set_volume(0.5)

#lager sangliste
sangListe = []
for i in range(1,antallSanger+1):
    sangListe.append(pg.mixer.Sound(folderPath+r"/data/soundTrack"+str(i)+".mp3"))

#starter første sang
backgroundTrackChannel.play(sangListe[startSangIndex])

# Highscore Variabler
highScorePath =  folderPath+r"/data/highscore.txt"
prevHighScore = float(lesHelFil(highScorePath))
hasWritten = False


# font til tekst
font = pg.font.SysFont("Arial", 24)

# variabler til vindu
VINDU_BREDDE = 800
VINDU_HOYDE = 300
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])

# variabler til bakken
groundHeight = VINDU_HOYDE / 4
groundWidth = VINDU_BREDDE
groundStartPos = [0, (VINDU_HOYDE / 4) * 3]
groundPos = groundStartPos.copy()
riseFallAmountGroundSpeed = 5

# variabler til klokke og FPS
clock = pg.time.Clock()
startTime = -2500
ingameTime = startTime
FPS = 60
clockPos = (VINDU_BREDDE / 2, 20)
marginBackgroundClock = 5

# debugVariabler
debugmode = False

# bilder:
background = pg.image.load(folderPath+r"/data/background.jpeg")
ground = pg.image.load(folderPath+r"/data/ground.jpg")
playerImg = pg.image.load(folderPath+r"/data/lovley_dino.png")
playerDeadImg = pg.image.load(folderPath+r"/data/ded.png")
obstical = pg.image.load(folderPath+r"/data/meteor.png")
flyingDinoImg = pg.image.load(folderPath+r"/data/saved.png")
buffImg = pg.image.load(folderPath+r"/data/pray.png")

# variabler for pos og størrelse spiller, disse kunne jeg endret for å lage spillet variabel størrelse
playerSize = (50, 80)
playerDeadSize = (80, 80)
playerSizeFly = [playerSize[0], playerSize[1] / 1.5]
playerStartPos = (40, groundStartPos[1] - playerSize[1] / 2)

# variabler for pos, fart og størrelse til hinder, disse kunne jeg endret for å lage spillet varibel størrelse og variabel fps
obsticalSize = (70, 70)
obsticalPosY = groundStartPos[1] - obsticalSize[1] / 3
obstiaclSpeedReducutionBuff = 1
obstiaclStartSpeed = 6
obsticalSpeed = obstiaclStartSpeed+obstiaclSpeedReducutionBuff
speedIncreesRunningMode =0.1
safeSpacesFlying = 3
metorCountFlying = 10

# variabler for når hinder spawner
minMeteorSpawnTimeFlying = 1000
maxMeteorSpawnTimeFlting = 2000
runningMeotorBaseTime = 1250
minMeteorSpawnTimeGround = 0
maxMeteorSpawnTimeGround = 500
lastSpawnedMeteor = 0
nextMeteorSpawn = random.randint(minMeteorSpawnTimeFlying, maxMeteorSpawnTimeFlting)

# variabler for når neste buff spawner
lastRan = 0
buffCooldownTime = 30 * 1000

# Variabler for flyving og hopping

runningJumpPower = 5
flyingJumpPower = 3
playerGravity =0.15


# oppretter spiller
spiller = Player(
    pos=playerStartPos,
    size=playerSize,
    fartY=-4,
    gravity=playerGravity,
    jumpPower=runningJumpPower,
    aliveImg=playerImg,
    dedImg=playerDeadImg,
    flyImg=flyingDinoImg,
    isAlive=True,
    flappyMode=True,
)


# oppretter gulvet som tester om spiller går for langt ned når de flyr
deathFloor = []
for i in range(int((VINDU_BREDDE / 4) / obsticalSize[0])):
    deathFloor.append(
        Obstical(
            pos=[obsticalSize[0] * i, VINDU_HOYDE + VINDU_HOYDE / 6],
            size=obsticalSize,
            fart=0,
            img=obstical,
        )
    )

# lister til programmet
meteorList = []
# legger inn en buff i starten for animasjon
buffList = [
    Obstical(
        pos=(VINDU_BREDDE + obsticalSize[0], obsticalPosY),
        size=obsticalSize,
        fart=obsticalSpeed,
        img=buffImg,
    )
]
buffFallOffAnimationList = []


#funskjon for når man plukker opp buff/går inn i flappybird mode
def buffPickUpTransistion():
    global obsticalSpeed
    spiller.flappyMode = True
    spiller.pos[1] = VINDU_HOYDE / 2
    spiller.changeSize(playerSize)
    spiller.fartY = -4
    effectsChannel.play(powerUpSound)
    obsticalSpeed -=obstiaclSpeedReducutionBuff

#funksjon for når man går ut av flappybird mode
def buffLostTransistion():
    spiller.flappyMode = False
    spiller.pos[1] = spiller.groundPos - 10
    # lager objekt for animasjon med fase endring
    buffFallOffAnimationList.append(
        Obstical(
            pos=spiller.pos.copy(),
            size=obsticalSize,
            fart=-5,
            img=buffImg,
        )
    )


# kjører spillet 
fortsett = True
while fortsett:
    # stopper spillet hvis man lukker det
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False

    #tester om sangen er ferdig og spiller en ny
    if backgroundTrackChannel.get_busy()==False:
        randomSangIndex = random.randint(0,antallSanger-1)
        backgroundTrackChannel.play(sangListe[randomSangIndex])
        
        
    # setter FPS
    clock.tick(FPS)

    # debugKode for å sjekke om spillet har lag
    if clock.get_time() - clock.get_rawtime() == 0:
        print("lag!: ", clock.get_rawtime())

    # henter ut tastetrykk
    trykkede_taster = pg.key.get_pressed()
        
    # skrur på debugmode. Litt laggy
    if trykkede_taster[K_d]:
        if debugmode:
            debugmode = False
        else:
            debugmode = True
        pg.time.delay(300)

    # setter bakgrunn til hvit, strengt tatt ikke nødvendig
    vindu.fill((255, 255, 255))

    # kode som flytter bakken til fastsatte punkter utifra hvilken modus spilleren er i
    if spiller.flappyMode == True:
        groundPos[1] += riseFallAmountGroundSpeed
        if groundPos[1] > VINDU_HOYDE:
            groundPos[1] = VINDU_HOYDE
    else:
        groundPos[1] -= riseFallAmountGroundSpeed
        if groundPos[1] < groundStartPos[1]:
            groundPos[1] = groundStartPos[1]

    # Tegner inn bakgrunn og bakke
    backgroundScaled = pg.transform.scale(background, [VINDU_BREDDE, VINDU_HOYDE])
    vindu.blit(backgroundScaled, (0, groundPos[1] - VINDU_HOYDE))

    scaledGround = pg.transform.scale(ground, [groundWidth, groundHeight])
    vindu.blit(scaledGround, groundPos)

    #klokke tekst under spilling
    highScoreTime = str(round(prevHighScore,1))
    tidTekst = font.render(str(round(abs(ingameTime) / 1000, 1)), True, (0, 0, 0))
    if ingameTime / 1000 > prevHighScore:
        tidTekst = font.render(
            "New highscore: " + str(round(abs(ingameTime) / 1000, 1)), True, (0, 0, 0)
        )
        highScoreTime = str(round(abs(ingameTime) / 1000, 1))
    #klokketekst etter game over
    if spiller.isAlive==False:
                tidTekst = font.render(
            "Highscore: "+highScoreTime+". Your Score: "+str(round(abs(ingameTime) / 1000, 1)), True, (0, 0, 0)
        )

    tidTekstSize = tidTekst.get_size()
    centerPosTime = [
        clockPos[0] - tidTekstSize[0] / 2,
        clockPos[1] - tidTekstSize[1] / 2,
    ]
    pg.draw.rect(
        vindu,
        "white",
        (
            centerPosTime[0] - marginBackgroundClock,
            centerPosTime[1] - marginBackgroundClock,
            tidTekstSize[0] + marginBackgroundClock * 2,
            tidTekstSize[1] + marginBackgroundClock * 2,
        ),
    )
    vindu.blit(tidTekst, centerPosTime)

    #animasjon for intro
    if ingameTime < 0:
        spiller.flappyMode = False
        ingameTime += clock.get_time()

        spiller.drawPlayer(vindu)
        for buff in buffList:
            # flytter og tegner buff
            buff.pos[0] = spiller.pos[0] + (VINDU_BREDDE / abs(startTime)) * abs(
                ingameTime
            )
            buff.pos[1] = spiller.pos[1]
            buff.drawObstical(vindu)

    # kjører hvis spiller er i løpeModus
    elif spiller.isAlive and (spiller.flappyMode == False):
        # kjører klokke
        ingameTime += clock.get_time()

        # setter variabler til spiller for løpe modus og kjører nødvendige funksjoner for tegning og bevegelse
        spiller.jumpPower = runningJumpPower
        spiller.changeSize(playerSize)
        spiller.drawAndMove(vindu)
        
        #spiller hoppelyd hvis spiller hopper og sjekker om spiller ønsker å hoppe
        if spiller.jump(trykkede_taster):
            effectsChannel.play(jumpSound)

        # debug kode for hitbox
        if debugmode:
            spiller.drawHitbox(vindu)

        # flytter, tegner, fjerner hinder og sjekker om spiller kolliderer med hindre og setter spiller til game over modus
        for meteor in meteorList:
            # flytter og tegner hinder
            meteor.drawAndMove(vindu)

            # debug kode for hitbox
            if debugmode:
                meteor.drawHitbox(vindu)

            # fjerner unøfvendige hinder
            if meteor.pos[0] < -meteor.size[0] * 2:
                meteorList.remove(meteor)

            #tester om spiller kolliderer med hinder
            if spiller.testCollison(meteor) == True:
                spiller.gameOver()

        # flytter, tegner og fjerner buff objekt
        for buff in buffList:
            # flytter og tegner buff
            buff.drawAndMove(vindu)

            # tester for kollisjon med buff og endrer spiller sin modus til flyving
            if spiller.testCollison(buff) == True:
                buffPickUpTransistion()
                buffList = []
                meteorList = []

            # debug kode for hitbox
            if debugmode:
                buff.drawHitbox(vindu)

            # fjerner unødvedige buff
            if buff.pos[0] < -buff.size[0] * 2:
                buffList.remove(buff)

        # animasjon for når man mister buff
        for fallOffObject in buffFallOffAnimationList:
            fallOffObject.drawAndMove(vindu)
            fallOffObject.pos[1] += 1
            if (
                fallOffObject.pos[0] > VINDU_BREDDE
                or fallOffObject.pos[1] > VINDU_HOYDE
            ):
                buffFallOffAnimationList.remove(fallOffObject)

        

        # sjekker om nokk tid har gått til å spawne buff
        if ingameTime - lastRan > buffCooldownTime:
            buffList.append(
                Obstical(
                    pos=(VINDU_BREDDE + obsticalSize[0], obsticalPosY),
                    size=obsticalSize,
                    fart=obsticalSpeed,
                    img=buffImg,
                )
            )
            lastRan = ingameTime
            lastSpawnedMeteor = ingameTime
        # sjekker om tiden er inne for å spawne ny hinder og sjekker at den ikke spawer hinder på buff
        # elif ingameTime - lastSpawnedMeteor >= nextMeteorSpawn and changeList == []:
        elif len(meteorList) < 5 and ingameTime - lastSpawnedMeteor >= nextMeteorSpawn:
            spawnMode = random.randint(1, 3)  # bestemmer hvor mange meteorer
            # spawner hinder
            for i in range(spawnMode):
                meteorList.append(
                    Obstical(
                        pos=(VINDU_BREDDE + obsticalSize[0] * i * 0.6, obsticalPosY),
                        size=obsticalSize,
                        fart=obsticalSpeed,
                        img=obstical,
                    )
                )
            # velger hvor lang tid til neste hinder
            nextMeteorSpawn = runningMeotorBaseTime + random.randint(minMeteorSpawnTimeGround, maxMeteorSpawnTimeGround)

            lastSpawnedMeteor = ingameTime  # lagrer når hinder ble spawn
            obsticalSpeed += speedIncreesRunningMode  # øker hinder hastighet

    # kode som kjører for flyvemodus
    elif spiller.flappyMode:
        lastRan = ingameTime  # setter variabel som brukes til å bestemme når neste buff skal spawne i løpe modus

        # kjører klokke
        ingameTime += clock.get_time()

        # setter variabler til spiller for flyve modus og kjører nødvendige funksjoner for tegning og bevegelse
        spiller.changeSize(playerSizeFly)
        spiller.jumpPower = flyingJumpPower
        spiller.drawAndMove(vindu)
        
        #spiller hoppelyd hvis spiller hopper og sjekker om spiller ønsker å hoppe
        if spiller.jump(trykkede_taster):
            effectsChannel.play(jumpSound)

        # debug kode for hitbox
        if debugmode:
            spiller.drawHitbox(vindu)

        # debug kode for hitbox
        if debugmode:
            for i in range(int(VINDU_HOYDE / metorCountFlying)):
                pg.draw.line(
                    vindu,
                    "red",
                    (0, (VINDU_HOYDE / metorCountFlying) * i),
                    (VINDU_BREDDE, (VINDU_HOYDE / metorCountFlying) * i),
                )

        # sjekker om tiden er inne for å spawne ny hinder
        if ingameTime - lastSpawnedMeteor >= nextMeteorSpawn:
            # bestemmer hvor åpningen skal være
            safePos = random.randint(1, metorCountFlying - safeSpacesFlying)
            # spawner hinder
            for i in range(-2, metorCountFlying + 2):
                if (safePos <= i <= safePos + safeSpacesFlying) == False:
                    meteorList.append(
                        Obstical(
                            pos=(VINDU_BREDDE, VINDU_HOYDE / metorCountFlying * i),
                            size=(VINDU_HOYDE / metorCountFlying * 1.5, VINDU_HOYDE / metorCountFlying * 1.5),
                            fart=obsticalSpeed,
                            img=obstical,
                        )
                    )

            # bestemmer når neste hinder skal spawne
            nextMeteorSpawn = random.randint(minMeteorSpawnTimeFlying, maxMeteorSpawnTimeFlting)
            lastSpawnedMeteor = ingameTime

        #går igjennom hinder og kjører nøvendige fuksjoner
        for meteor in meteorList:
            # flytter og tegner hinder
            meteor.drawAndMove(vindu)

            # debug kode for hitbox
            if debugmode:
                meteor.drawHitbox(vindu)

            # fjerner unøfvendige hinder
            if meteor.pos[0] < -meteor.size[0] * 2:
                meteorList.remove(meteor)

            if spiller.testCollison(meteor) == True:
                # setter spiller til løpemodus
                buffLostTransistion()
                # fjerner alle hinder
                meteorList = []

        # sjekker om spiller går for langt ned, kunne også bare sjekket høyde men jaja
        for deathFloorObject in deathFloor:
            if spiller.testCollison(deathFloorObject) == True:
                # setter spiller til løpemodus
                buffLostTransistion()
                # fjerner alle hinder
                meteorList = []

    else:
        # Setter variabler og kjører funksjoner som trengs til gameOver animasjon
        spiller.changeSize(playerDeadSize)
        spiller.flappyMode = False
        spiller.drawAndMove(vindu)

        # kjører funskjoner for å flytte de siste meteorene av skjermen
        for meteor in meteorList:
            meteor.drawAndMove(vindu)
            if debugmode:
                meteor.drawHitbox(vindu)

        if (prevHighScore < ingameTime / 1000) and (hasWritten == False):
            skrivTilNyFil(highScorePath, str(ingameTime / 1000), False)
            hasWritten = True

    # oppdatderer skjermen
    pg.display.flip()


pg.quit()
