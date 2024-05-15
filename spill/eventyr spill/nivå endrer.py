import pygame
import pickle
from os import path
import os
import sys 

# finner mappen som filene ligger i
folderPath = os.path.dirname(os.path.abspath(sys.argv[0])) 


pygame.init()

klokke = pygame.time.Clock()
fps = 60

#game window
brikke_størrelse = 30
kolonne = 20
margin = 100
skjerm_bredde = brikke_størrelse * kolonne
skjerm_hoyde = (brikke_størrelse * kolonne) + margin

skjerm = pygame.display.set_mode((skjerm_bredde, skjerm_hoyde))
pygame.display.set_caption('level endrer')


#llast inn bilder
bg_bilde= pygame.image.load(folderPath+r'\img/bakgrunn.jpg')
bg_bilde = pygame.transform.scale(bg_bilde, (skjerm_bredde, skjerm_hoyde - margin))
jord_bilde = pygame.image.load(folderPath+r'\img/jord.png')
gress_bilde = pygame.image.load(folderPath+r'\img/gress.png')
blob_bilde = pygame.image.load(folderPath+r'\img/blob.png')
platform_x_bilde = pygame.image.load(folderPath+r'\img/plattform_x.png')
platform_y_bilde = pygame.image.load(folderPath+r'\img/plattform_y.png')
lava_bilde = pygame.image.load(folderPath+r'\img/lava.png')
penge_bilde = pygame.image.load(folderPath+r'\img/coin.png')
utgang_bilde = pygame.image.load(folderPath+r'\img/exit.png')
lagre_bilde = pygame.image.load(folderPath+r'\img/save_btn.png')
lastinn_bilde = pygame.image.load(folderPath+r'\img/load_btn.png')


#definerer noen spille variabler
klikket = False
level = 3

#definerer farge
hvit = (255, 255, 255)
grønn = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

#lager tom spille liste
verden_data = []
for rad in range(20):
	r = [0] * 20
	verden_data.append(r)

#lager rammen
for brikke in range(0, 20):
	verden_data[19][brikke] = 2
	verden_data[0][brikke] = 1
	verden_data[brikke][0] = 1
	verden_data[brikke][19] = 1

#funsksjon for at det skal være tekst på skjermen 
def tegn_tekst(tekst, font, tekst_kolonne, x, y):
	bilde = font.render(tekst, True, tekst_kolonne)
	skjerm.blit(bilde, (x, y))

def tegn_hvite_linjer():
	for c in range(21):
		#vertikale linjer
		pygame.draw.line(skjerm, hvit, (c * brikke_størrelse, 0), (c * brikke_størrelse, skjerm_hoyde - margin))
		#horisontale linjer
		pygame.draw.line(skjerm, hvit, (0, c * brikke_størrelse), (skjerm_bredde, c * brikke_størrelse))


def tegn_verden():
	for rad in range(20):
		for kolonne in range(20):
			if verden_data[rad][kolonne] > 0:
				if verden_data[rad][kolonne] == 1:
					#jord brikkene 
					bilde = pygame.transform.scale(jord_bilde, (brikke_størrelse, brikke_størrelse))
					skjerm.blit(bilde, (kolonne * brikke_størrelse, rad * brikke_størrelse))
				if verden_data[rad][kolonne] == 2:
					#gress brikkene 
					bilde = pygame.transform.scale(gress_bilde, (brikke_størrelse, brikke_størrelse))
					skjerm.blit(bilde, (kolonne * brikke_størrelse, rad * brikke_størrelse))
				if verden_data[rad][kolonne] == 3:
					#motstander brikker 
					bilde = pygame.transform.scale(blob_bilde, (brikke_størrelse, int(brikke_størrelse * 0.75)))
					skjerm.blit(bilde, (kolonne * brikke_størrelse, rad * brikke_størrelse + (brikke_størrelse * 0.25)))
				if verden_data[rad][kolonne] == 4:
					#horisontalt flyttende platformer 
					bilde = pygame.transform.scale(platform_x_bilde, (brikke_størrelse, brikke_størrelse // 2))
					skjerm.blit(bilde, (kolonne * brikke_størrelse, rad * brikke_størrelse))
				if verden_data[rad][kolonne] == 5:
					#vertikalt flyttende platformer
					bilde = pygame.transform.scale(platform_y_bilde, (brikke_størrelse, brikke_størrelse // 2))
					skjerm.blit(bilde, (kolonne * brikke_størrelse, rad * brikke_størrelse))
				if verden_data[rad][kolonne] == 6:
					#lava
					bilde = pygame.transform.scale(lava_bilde, (brikke_størrelse, brikke_størrelse // 2))
					skjerm.blit(bilde, (kolonne * brikke_størrelse, rad * brikke_størrelse + (brikke_størrelse // 2)))
				if verden_data[rad][kolonne] == 7:
					#penge
					bilde = pygame.transform.scale(penge_bilde, (brikke_størrelse // 2, brikke_størrelse // 2))
					skjerm.blit(bilde, (kolonne * brikke_størrelse + (brikke_størrelse // 4), rad * brikke_størrelse + (brikke_størrelse // 4)))
				if verden_data[rad][kolonne] == 8:
					#utgang
					bilde = pygame.transform.scale(utgang_bilde, (brikke_størrelse, int(brikke_størrelse * 1.5)))
					skjerm.blit(bilde, (kolonne * brikke_størrelse, rad * brikke_størrelse - (brikke_størrelse // 2)))



class Knapp():
	def __init__(self, x, y, bilde):
		self.bilde = bilde
		self.rect = self.bilde.get_rect()
		self.rect.topleft = (x, y)
		self.klikket = False

	def tegn(self):
		handling = False

		#skaff muse posisjon 
		pos = pygame.mouse.get_pos()

		#sjekker om musen er over knappen og om knappen er trykket
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.klikket == False:
				handling = True
				self.klikket = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.klikket = False

		#tegner knappen inn i brettet
		skjerm.blit(self.bilde, (self.rect.x, self.rect.y))

		return handling

#lager load og save knappene 
save_Knapp = Knapp(skjerm_bredde // 2 - 150, skjerm_hoyde - 80, lagre_bilde)
load_Knapp = Knapp(skjerm_bredde // 2 + 50, skjerm_hoyde - 80, lastinn_bilde)

#hovedspill løkke
run = True
while run:

	klokke.tick(fps)

	#tegn bakgrunn 
	skjerm.fill(grønn)
	skjerm.blit(bg_bilde, (0, 0))

	#last inn og lagre level data
	if save_Knapp.tegn():
		#save level data
		pickle_ut = open(f'level{level}_data', 'wb')
		pickle.dump(verden_data, pickle_ut)
		pickle_ut.close()
	if load_Knapp.tegn():
		#last inn level data
		if path.exists(f'level{level}_data'):
			pickle_inn = open(f'level{level}_data', 'rb')
			verden_data = pickle.load(pickle_inn)


	#show the grid and draw the level brikkes
	tegn_hvite_linjer()
	tegn_verden()


	#tekst som viser hvilket level
	tegn_tekst(f'level: {level}', font, hvit, brikke_størrelse, skjerm_hoyde - 60)
	tegn_tekst('Press UP or DOWN to change level', font, hvit, brikke_størrelse, skjerm_hoyde - 40)

	#fikser alle trykk 
	for event in pygame.event.get():
		#slutt spill hvis x er trykket
		if event.type == pygame.QUIT:
			run = False
		#museklikk for å endre brikker
		if event.type == pygame.MOUSEBUTTONDOWN and klikket == False:
			klikket = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // brikke_størrelse
			y = pos[1] // brikke_størrelse
			#sjekk om koordinatene er innenfor brikke området 
			if x < 20 and y < 20:
				#oppdater brikke verdi ved museklikk
				if pygame.mouse.get_pressed()[0] == 1:
					verden_data[y][x] += 1
					if verden_data[y][x] > 8:
						verden_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					verden_data[y][x] -= 1
					if verden_data[y][x] < 0:
						verden_data[y][x] = 8
		if event.type == pygame.MOUSEBUTTONUP:
			klikket = False
		#opp og ned for å endre level
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	#oppdaterer brettet
	pygame.display.update()

pygame.quit()