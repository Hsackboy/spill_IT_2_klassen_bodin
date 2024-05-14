import pygame # spillfunksjoner
import random
import sys # funksjon for å lukke vindu

class Ball:
    """Klasse for å holde informasjon om alle ballene: radius, plassering, fart, farge"""
    def __init__(self, radius, plassering, fart, farge):
        self.radius = radius
        self.plassering = pygame.Vector2(plassering)
        self.fart = pygame.Vector2(fart)
        self.farge = farge

    def flytt(self):
        """Funksjon for å bevege ballene ved å øke posisjon med fart. Denne brukes på motstanderballene"""
        self.plassering += self.fart
        self.sjekk_grenser()

    def sjekk_grenser(self):
        """Funksjon for å hindre at ting beveger seg utenfor rammene på skjermen.
        Sjekker om ballen er utenfor 0x/y eller gitt høyde/bredde"""
        if self.plassering.x <= 0 or self.plassering.x >= SKJERM_BREDDE:
            self.fart.x *= -1
        if self.plassering.y <= 0 or self.plassering.y >= SKJERM_HOYDE:
            self.fart.y *= -1

    def tegn(self, skjerm):
        """Funksjon for å tegne ballen innenfor skjermen, med farge, x/y-posisjon og radius"""
        pygame.draw.circle(skjerm, self.farge, (int(self.plassering.x), int(self.plassering.y)), self.radius)

class SpillSkjerm:
    """Klasse for å lage et GUI: skjerm og skriftstørrelse"""
    def __init__(self, skjerm):
        self.skjerm = skjerm
        self.font = pygame.font.Font(None, 36)

    def tegn_tekst(self, tekst, farge, x, y):
        """Lager tekst"""
        tekst_objekt = self.font.render(tekst, 1, farge)
        tekst_rekt = tekst_objekt.get_rect()
        tekst_rekt.topleft = (x, y)
        self.skjerm.blit(tekst_objekt, tekst_rekt)

    def knapp(self, melding, x, y, bredde, hoyde, ic, ac, handling=None):
        """Lager knapp: x, y, bredde, høyde, farge tekst, farge knapp"""
        mus = pygame.mouse.get_pos()
        klikk = pygame.mouse.get_pressed()
        if x + bredde > mus[0] > x and y + hoyde > mus[1] > y:
            pygame.draw.rect(self.skjerm, ac, (x, y, bredde, hoyde))
            if klikk[0] == 1 and handling is not None:
                handling()
        else:
            pygame.draw.rect(self.skjerm, ic, (x, y, bredde, hoyde))

        liten_tekst = pygame.font.Font(None, 20)
        tekst_surf = liten_tekst.render(melding, True, (0, 0, 0))
        tekst_rekt = tekst_surf.get_rect()
        tekst_rekt.center = ((x + (bredde / 2)), (y + (hoyde / 2)))
        self.skjerm.blit(tekst_surf, tekst_rekt)

class Spill:
    """Spillklasse: skjerm, tid, GUI"""
    def __init__(self):
        pygame.init()
        self.skjerm = pygame.display.set_mode((SKJERM_BREDDE, SKJERM_HOYDE))
        self.klokke = pygame.time.Clock()
        self.skjerm_manager = SpillSkjerm(self.skjerm)   # Skjerm, lager skjermen

    def start(self):
        """Starter startskjermen"""
        self.intro()

    def intro(self):
        """Lager startskjermen"""
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.skjerm.fill(BAKGRUNNS_FARGE)
            self.skjerm_manager.knapp('Start!!', SKJERM_BREDDE/2 - 50, SKJERM_HOYDE/2 ,  100, 50, (144, 238, 144), (105, 255, 105), self.hoved_spill)
            pygame.display.update()
            self.klokke.tick(15) # FPS

    def slutt_spill(self, poeng, melding='Game over :('):
        """Lager sluttskjermen"""
        slutt = True
        while slutt:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.skjerm.fill((255,255,255)) # Gjør vinnskjermen hvit for en kul transformasjon
            self.skjerm_manager.tegn_tekst(melding, (0, 0, 0),  SKJERM_BREDDE/2 - 60, SKJERM_HOYDE/2 - 150)
            self.skjerm_manager.tegn_tekst(f'Poeng: {poeng}', (0, 0, 0), SKJERM_BREDDE/2 - 45, SKJERM_HOYDE/2 - 50)
            self.skjerm_manager.knapp('restart?', SKJERM_BREDDE/2 - 50, SKJERM_HOYDE/2, 100, 50, (255, 127, 127), (255, 100, 100), self.hoved_spill)
            pygame.display.update()
            self.klokke.tick(15)

    def hoved_spill(self):
        """Implementerer spilllogikken"""
        spiller = Ball(10, pygame.mouse.get_pos(), (0, 0), SPILLER_FARGE)
        tilfeldige_baller = []   # Ballene som spawnes
        poeng = 0  # Antall baller som er spist
        kjorer = True  
        ball_timer = 0  

        while kjorer:
            for event in pygame.event.get(): # Paranoid .-.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            spiller.plassering = pygame.Vector2(pygame.mouse.get_pos()) # Posisjon til mus

            # Lager nye baller
            if ball_timer <= 0:
                ny_ball = Ball(random.randint(5, 50), 
                                (random.randint(0, SKJERM_BREDDE), random.randint(0, SKJERM_HOYDE)),
                                [random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])],
                                BALL_FARGE)
                tilfeldige_baller.append(ny_ball)
                ball_timer = 50 # Tid mellom hver ball
            else:
                ball_timer -= 1 # - for hver ball

            for ball in tilfeldige_baller[:]:
                ball.flytt()
                # Sjekker om ballen er spiselig
                if spiller.radius > ball.radius and spiller.plassering.distance_to(ball.plassering) < spiller.radius + ball.radius:
                    spiller.radius += ball.radius // 2  # Øker radius
                    tilfeldige_baller.remove(ball)
                    poeng += 1  # Legger til poeng når en ball spises
                elif spiller.radius <= ball.radius and spiller.plassering.distance_to(ball.plassering) < spiller.radius + ball.radius:
                    self.slutt_spill(poeng)  # Enderspillet om ballen treffer en større ball
                    kjorer = False
                    break

            # Om spilleren dekker mesteparten av skjermen, vinner de
            if spiller.radius >= min(SKJERM_HOYDE, SKJERM_BREDDE) / 1.5:
                self.slutt_spill(poeng, melding='Du vant!') 
                break

            if not kjorer:
                break

            # Tegner alt
            self.skjerm.fill(BAKGRUNNS_FARGE)
            spiller.tegn(self.skjerm)
            for ball in tilfeldige_baller:
                ball.tegn(self.skjerm)

            pygame.display.flip()
            self.klokke.tick(FPS)

if __name__ == '__main__':
    SKJERM_BREDDE, SKJERM_HOYDE = 700, 700
    BAKGRUNNS_FARGE = (0, 0, 0)
    SPILLER_FARGE = (255, 255, 255)
    BALL_FARGE = (255, 50, 255)
    FPS = 60
    spill = Spill()
    spill.start()