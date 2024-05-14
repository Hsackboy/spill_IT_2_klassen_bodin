from filLeserBiblotek2 import *
import pygame as pg
import os 
import sys 

FPS = 30
clock = pg.time.Clock()
ingameTime = 0

folderPath = os.path.dirname(os.path.abspath(sys.argv[0]))  #path til der filen fins

count =1
lyricPath = r"/data/dinoLyrics.txt"
songPath = r"/data/soundTrack1.mp3"
timeingPath = r"/data/lineTimeing.json"

lyrics = lesHelFil(folderPath+lyricPath)
lyrics= lyrics.split("\n")

backgroundColor = (230,230,230)

timeing = lesJson(folderPath+timeingPath)
# print(timeing)

pg.init()
    
pg.mixer.set_num_channels(2)
backgroundTrackChannel = pg.mixer.Channel(0)
song = pg.mixer.Sound(folderPath+songPath)
backgroundTrackChannel.play(song)

# print(backgroundTrackChannel.get_busy())


vindu_bredde, vindu_høyde = 500,500

# lager 2 fonts, den andre fonten brukes til å ha understrek under slik at ikke all teksten får understrek under seg
font = pg.font.SysFont('arial', 36)

vindu = pg.display.set_mode((vindu_bredde, vindu_høyde))
#starter spill
fortsett = True
while fortsett:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
    
    if backgroundTrackChannel.get_busy()==False:
        fortsett=False
    
    vindu.fill(backgroundColor)
    
    clock.tick(FPS)
    ingameTime+=clock.get_time()
    
    trykkede_taster = pg.key.get_pressed()
    if trykkede_taster[pg.K_SPACE]:
        print(str(count)+":"+str(ingameTime))
        pg.time.delay(300)
        count+=1
    
    pg.display.flip()