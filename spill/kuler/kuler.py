import pygame as pg
from pygame.locals import K_w, K_s, K_a, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_n, K_m
import math as m
import random as rd

pg.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 620

window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg.RESIZABLE)
pg.display.set_caption("Kule Kuler BETA v 1.8")

WINDOW_WIDTH = pg.display.get_surface().get_size()[0]
WINDOW_HEIGHT = pg.display.get_surface().get_size()[1]

# Font
font = pg.font.SysFont("Arial", 42)


# Player health
max_healt = 250
health_points = max_healt

# obstacle health
# obstacle_health = 25


# speed + fps
speed_multiplier = 5
fps = 144

# Time variables
clock = pg.time.Clock()
start_time = pg.time.get_ticks()
elapsed_time = 0
last_spawn_booster = 0
last_spawn_obstacle = 0
last_spawn_bullet = 0

# Holder styr på tiden minen er i vinduet
mine_timer = 0

# Variabel for å holde tiden på hvor lenge meldingen for boost er i vinduet
display_boost_message_timer = 0

# Variabel for prosjektiler
gun_timer = 0
display_gun_message = 0
projectileSpeed = 10
ammo_timer = 0
# max_ammo = player.ammo_count
ammo_cost = 1
weapon_activate = 45000

# variabler for spillerens pos
prev_x = 0
prev_y = 0
lastMoved = 0

# beam var
beam_timer = 0
last_spawn_beam = 0
beam_amount = 4

last_spawn_beam_indicator = 0
beam_indicator_count = 0

# snipermode
sniperMode = False


# Classes and subclasses
class Ball:
    """Klasse for å vise en generell ball og teste for kollisjon"""

    def __init__(self, x, y, color, radius, windowsObject):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.windowsObject = windowsObject

    def draw(self):
        pg.draw.circle(self.windowsObject, self.color, (self.x, self.y), self.radius)

    def hinder_collision(self, otherBall):
        xDistance = (self.x - otherBall.x) ** 2
        yDistance = (self.y - otherBall.y) ** 2
        centerDistance = m.sqrt(xDistance + yDistance)

        radius = self.radius + otherBall.radius

        distance = centerDistance - radius

        if distance <= 0:
            return True
        else:
            return False


class Hinder(Ball):
    """Klasse for å fremstille hinder"""

    def __init__(self, x, y, color, radius, windowsObject, xSpeed, ySpeed):
        super().__init__(x, y, color, radius, windowsObject)
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.health = self.radius * 3

    def move(self):
        if ((self.x - self.radius) <= 0) or (
            (self.x + self.radius) >= self.windowsObject.get_width()
        ):

            self.xSpeed *= -1
            if (self.x - self.radius) <= 0:
                self.x = self.radius
            else:
                self.x = self.windowsObject.get_width() - self.radius

        if ((self.y - self.radius) <= 0) or (
            (self.y + self.radius) >= self.windowsObject.get_height()
        ):

            self.ySpeed *= -1
            if (self.y - self.radius) <= 0:
                self.y = self.radius
            else:
                self.y = self.windowsObject.get_height() - self.radius

        self.x += self.xSpeed
        self.y += self.ySpeed

    def ballCollision(self, otherBall):
        tempX_Speed = self.xSpeed
        tempY_Speed = self.ySpeed

        self.xSpeed = otherBall.xSpeed
        self.ySpeed = otherBall.ySpeed
        otherBall.xSpeed = tempX_Speed
        otherBall.ySpeed = tempY_Speed


class Buff(Ball):
    """Klasse for å fremstille en boost"""

    def __init__(self, x, y, color, radius, windowsObject, xSpeed, ySpeed):
        super().__init__(x, y, color, radius, windowsObject)
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.color = color

    def move(self):
        if ((self.x - self.radius) <= 0) or (
            (self.x + self.radius) >= self.windowsObject.get_width()
        ):

            self.xSpeed *= -1
            if (self.x - self.radius) <= 0:
                self.x = self.radius
            else:
                self.x = self.windowsObject.get_width() - self.radius

        if ((self.y - self.radius) <= 0) or (
            (self.y + self.radius) >= self.windowsObject.get_height()
        ):

            self.ySpeed *= -1
            if (self.y - self.radius) <= 0:
                self.y = self.radius
            else:
                self.y = self.windowsObject.get_height() - self.radius

        self.x += self.xSpeed
        self.y += self.ySpeed


class Projectile(Ball):
    """Klasse for å fremstille et skudd"""

    def __init__(self, x, y, color, speedX, speedY, radius, windowsObject):
        super().__init__(x, y, color, radius, windowsObject)
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = speedY
        self.radius = radius
        self.hitWall = False

    def draw(self):
        pg.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self):
        if ((self.x - self.radius) <= 0) or (
            (self.x + self.radius) >= self.windowsObject.get_width()
        ):

            # self.speedX *= -1
            if (self.x - self.radius) <= 0:
                self.x = self.radius
            else:
                self.x = self.windowsObject.get_width() - self.radius
            self.hitWall = True

        if ((self.y - self.radius) <= 0) or (
            (self.y + self.radius) >= self.windowsObject.get_height()
        ):

            # self.ySpeed *= -1
            if (self.y - self.radius) <= 0:
                self.y = self.radius
            else:
                self.y = self.windowsObject.get_height() - self.radius
            self.hitWall = True

        self.x += self.speedX
        self.y += self.speedY


# Liste for å legge til ammo
bullets = []


class Player(Ball):
    """Spiller klassen"""

    def __init__(self, x, y, color, radius, windowsObject, speed):
        super().__init__(x, y, color, radius, windowsObject)
        self.speed = speed
        self.ammo_count = 80

    def wallCollision(self):
        """Sjekker for kollisjon med spilleren og veggen"""

        if ((self.x - self.radius) <= 0) or (
            (self.x + self.radius) >= self.windowsObject.get_width()
        ):
            if (self.x - self.radius) <= 0:
                self.x = self.radius
            else:

                self.x = self.windowsObject.get_width() - self.radius

        if ((self.y - self.radius) <= 0) or (
            (self.y + self.radius) >= self.windowsObject.get_height()
        ):
            if (self.y - self.radius) <= 0:
                self.y = self.radius
            else:
                self.y = self.windowsObject.get_height() - self.radius

    def move(self, keys):
        """ "Beveger spilleren ut i fra hvilke knapper"""
        if keys[K_w]:
            self.y -= self.speed
        if keys[K_s]:
            self.y += self.speed
        if keys[K_a]:
            self.x -= self.speed
        if keys[K_d]:
            self.x += self.speed
        self.wallCollision()

    def look(self, keys):
        """Legger til en prosjektil ut i fra hvilke pilknapp blir trykt"""
        if keys[K_UP] and keys[K_LEFT]:
            bullets.append(
                Projectile(
                    player.x,
                    player.y,
                    (255, 169, 20),
                    -projectileSpeed,
                    -projectileSpeed,
                    10,
                    window,
                )
            )
            self.ammo_count -= ammo_cost
        elif keys[K_UP] and keys[K_RIGHT]:
            bullets.append(
                Projectile(
                    player.x,
                    player.y,
                    (255, 169, 20),
                    projectileSpeed,
                    -projectileSpeed,
                    10,
                    window,
                )
            )
            self.ammo_count -= ammo_cost
        elif keys[K_DOWN] and keys[K_LEFT]:
            bullets.append(
                Projectile(
                    player.x,
                    player.y,
                    (255, 169, 20),
                    -projectileSpeed,
                    projectileSpeed,
                    10,
                    window,
                )
            )
            self.ammo_count -= ammo_cost
        elif keys[K_DOWN] and keys[K_RIGHT]:
            bullets.append(
                Projectile(
                    player.x,
                    player.y,
                    (255, 169, 20),
                    projectileSpeed,
                    projectileSpeed,
                    10,
                    window,
                )
            )
            self.ammo_count -= ammo_cost
        elif keys[K_UP]:
            bullets.append(
                Projectile(
                    player.x, player.y, (255, 169, 20), 0, -projectileSpeed, 10, window
                )
            )
            self.ammo_count -= ammo_cost
        elif keys[K_DOWN]:
            bullets.append(
                Projectile(
                    player.x, player.y, (255, 169, 20), 0, projectileSpeed, 10, window
                )
            )
            self.ammo_count -= ammo_cost
        elif keys[K_RIGHT]:
            bullets.append(
                Projectile(
                    player.x, player.y, (255, 169, 20), projectileSpeed, 0, 10, window
                )
            )
            self.ammo_count -= ammo_cost
        elif keys[K_LEFT]:
            bullets.append(
                Projectile(
                    player.x, player.y, (255, 169, 20), -projectileSpeed, 0, 10, window
                )
            )
            self.ammo_count -= ammo_cost

        # self.ammo_count -= 5

    def beam_collision(self, beam):
        """Sjekker kollisjon mellom en stråle og spilleren"""
        closest_x = max(beam.xPos, min(self.x, beam.xPos + beam.width))
        closest_y = max(beam.yPos, min(self.y, beam.yPos + beam.height))

        distance = m.sqrt((self.x - closest_x) ** 2 + (self.y - closest_y) ** 2)

        return distance <= self.radius


obstacles = []
mines = []
for i in range(4):
    radius = rd.randint(4, 30)
    xPos = rd.randint(0, WINDOW_WIDTH - radius)
    yPos = rd.randint(0, WINDOW_HEIGHT - radius)

    if radius <= 5:
        xSpeed = rd.uniform(0.7 * speed_multiplier, 1.3 * speed_multiplier)
        ySpeed = rd.uniform(0.7 * speed_multiplier, 1.3 * speed_multiplier)
    elif radius <= 15 and radius > 5:
        xSpeed = rd.uniform(0.3 * speed_multiplier, 0.9 * speed_multiplier)
        ySpeed = rd.uniform(0.3 * speed_multiplier, 0.9 * speed_multiplier)
    else:
        xSpeed = rd.uniform(0.1 * speed_multiplier, 0.6 * speed_multiplier)
        ySpeed = rd.uniform(0.1 * speed_multiplier, 0.6 * speed_multiplier)

    obstacles.append(Hinder(xPos, yPos, "red", radius, window, xSpeed, ySpeed))

boosters = []
ammo = []


player = Player(0, 0, "blue", 25, window, 0.5 * speed_multiplier)
max_ammo = player.ammo_count


class Beam:
    def __init__(self, color, width, height, xPos, yPos):
        self.color = color
        self.width = width
        self.height = height
        self.xPos = xPos
        self.yPos = yPos
        self.vertical = False

    def draw(self):
        pg.draw.rect(
            window, self.color, (self.xPos, self.yPos, self.width, self.height)
        )


beams = []
beam_indicators = []


# Velger en melding ut ifra hvilke tall blir gitt, til boost objekter
def boostMessage(number):
    if number == 1:

        return font.render("+ Speed!", True, "green")
    elif number == 2:

        return font.render("+ Health!", True, "green")
    elif number == 3:

        return font.render("- Size!", True, "green")
    elif number == 4:

        return font.render("- 1 Enemy!", True, "green")


fortsett = True
while fortsett:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False
        elif event.type == pg.KEYDOWN:
            if event.key == K_n:
                sniperMode = True
            if event.key == K_m:
                sniperMode = False

    keys_pressed = pg.key.get_pressed()

    window.fill(("white"))

    WINDOW_WIDTH = pg.display.get_surface().get_size()[0]
    WINDOW_HEIGHT = pg.display.get_surface().get_size()[1]

    # Hvert 9200 millisek legges til en indikator for den kommende strålen til i listen beam_indicators.
    if elapsed_time - last_spawn_beam_indicator >= 9200:
        beam_indicator_count = 100
        for i in range(beam_amount):
            # Tilfeldig variabel som tester for vertikal eller horisontal stråle
            vert_check = rd.randint(0, 1)

            # Hvis vert_check er lik 0 vil den lage vertikal og motsatt
            if vert_check == 0:
                beam_indicators.append(
                    Beam("orange", 30, WINDOW_HEIGHT, rd.randint(0, WINDOW_WIDTH), 0)
                )
            elif vert_check == 1:
                beam_indicators.append(
                    Beam("orange", WINDOW_WIDTH, 30, 0, rd.randint(0, WINDOW_HEIGHT))
                )

        last_spawn_beam_indicator = elapsed_time

    # Legger til stråler hvert 10. sekund.
    if elapsed_time - last_spawn_beam >= 10000:

        beam_timer = fps
        # legger til antall beams
        for indecatorBeem in beam_indicators:
            # legger til enten vertikale eller horisontale stråler
            beams.append(
                Beam(
                    "red",
                    indecatorBeem.width,
                    indecatorBeem.height,
                    indecatorBeem.xPos,
                    indecatorBeem.yPos,
                )
            )

        last_spawn_beam = elapsed_time
        last_spawn_beam_indicator = elapsed_time

    if beam_indicator_count > 0:
        if len(beam_indicators) > beam_amount:
            beam_indicators.pop(0)

        for indicator in beam_indicators:
            indicator.draw()
        beam_indicator_count -= 0.5

    # Tegner strålene, maksimal antall er beam_amount
    if beam_timer > 0:
        if len(beams) > beam_amount:
            beams.pop(0)

        for beam in beams:
            beam.draw()
            if player.beam_collision(beam):
                health_points -= 1.6
        beam_timer -= 0.3

    # Time
    current_time = pg.time.get_ticks()
    elapsed_time = current_time - start_time

    # TIME COUNTER
    text = font.render(
        f"{elapsed_time/1000:.2f}", True, "black"
    )  # text that counts time in game

    # text_x får senter av skjermen i x aksen
    text_x = (window.get_width() // 2) - (text.get_width() // 2)

    window.blit(text, (text_x, 10))  # Viser timer på skjermen

    # draws player
    player.draw()
    player.move(keys_pressed)

    # player health
    # Healthbar over player
    rectHelathLen = ((50) / max_healt) * health_points
    pg.draw.rect(
        window, (255, 0, 0), (player.x - 25, player.y - 40, rectHelathLen, 7)
    )  # adds healthbar

    # Health bar on top of screen
    rectHelathLen = ((WINDOW_WIDTH) / max_healt) * health_points
    pg.draw.rect(window, (255, 0, 0), (0, 0, rectHelathLen, 12))  # adds healthbar

    # MINE
    # Tester skjekker om posisjonen som er lagret er den samme som spillerens posisjon
    if (prev_x != player.x) or (prev_y != player.y):
        lastMoved = elapsed_time

    prev_x = player.x
    prev_y = player.y

    if elapsed_time > 2000:
        # finner tiden i millisekunder. Hvor lenge det er gått fra spillerens posisjon ikke er endret
        if elapsed_time - lastMoved > 500:
            health_points -= 0.6
            mine_timer = 100
            mine_x = player.x
            mine_y = player.y

        # Timer til minen går ned, og fargen endrer seg gradvis.
        if mine_timer > 0:
            mineColor = (230, 100 + mine_timer, 0)

            # Hvis nedtellingen er under 10, blir den rød og gir mye skade til helse.
            if mine_timer < 35:
                mines.append(
                    Hinder(
                        mine_x, mine_y, mineColor, 100 - (mine_timer - 50), window, 0, 0
                    )
                )

                if player.hinder_collision(mine):
                    health_points -= 5
                    # print("eksplosjon!!!")

            mine_timer -= 1
            mine = Hinder(
                mine_x, mine_y, mineColor, 100 - (mine_timer - 50), window, 0, 0
            )

            pg.draw.circle(window, "red", (mine_x, mine_y), 40.0 - (mine_timer - 70))

            mine.draw()

    # Adds obstacles
    for hinder in obstacles:

        if player.hinder_collision(hinder):  # Reduserer helse ut i fra kollisjon
            window.fill((255, 57, 18))

            health_points -= (hinder.radius / 7.5) + 1

        hinder.draw()
        hinder.move()

    if elapsed_time - last_spawn_obstacle >= 25000:

        radius = rd.randint(4, 30)
        xPos = rd.randint(0, WINDOW_WIDTH - radius)
        yPos = rd.randint(0, WINDOW_HEIGHT - radius)

        if radius <= 5:
            xSpeed = rd.uniform(0.7 * speed_multiplier, 1.3 * speed_multiplier)
            ySpeed = rd.uniform(0.7 * speed_multiplier, 1.3 * speed_multiplier)
        elif radius <= 15 and radius > 5:
            xSpeed = rd.uniform(0.3 * speed_multiplier, 0.9 * speed_multiplier)
            ySpeed = rd.uniform(0.3 * speed_multiplier, 0.9 * speed_multiplier)
        else:
            xSpeed = rd.uniform(0.1 * speed_multiplier, 0.5 * speed_multiplier)
            ySpeed = rd.uniform(0.1 * speed_multiplier, 0.5 * speed_multiplier)

        obstacles.append(Hinder(xPos, yPos, "red", radius, window, xSpeed, ySpeed))

        last_spawn_obstacle = elapsed_time

    # if elapsed_time >= 10000:
    #     speed_multiplier += 0.5

    if elapsed_time - ammo_timer >= 60000:
        radius = 15
        xPos = rd.randint(0, WINDOW_WIDTH - radius)
        yPos = rd.randint(0, WINDOW_HEIGHT - radius)

        ammo.append(Buff(xPos, yPos, "orange", radius, window, 6.5, 6.5))

        ammo_timer = elapsed_time

    for i in ammo:
        i.draw()
        i.move()

        if player.hinder_collision(i):
            player.ammo_count = max_ammo
            print(player.ammo_count)

            ammo.remove(i)

    # Legger til boosters
    if elapsed_time - last_spawn_booster >= 20000:

        radius = rd.randint(20, 25)
        xPos = rd.randint(0, WINDOW_WIDTH - radius)
        yPos = rd.randint(0, WINDOW_HEIGHT - radius)

        boosters.append(
            Buff(
                xPos,
                yPos,
                "green",
                radius,
                window,
                0.93 * speed_multiplier,
                0.93 * speed_multiplier,
            )
        )
        last_spawn_booster = elapsed_time

    # Tegner boosters, gir buffs
    for boost in boosters:
        boost.draw()
        boost.move()

        if player.hinder_collision(boost):
            # Tester hvis spilleren kolliderer med booster

            rdBoost = rd.randint(1, 4)

            health_points += 20  # gir HP

            display_boost_message_timer = 50

            if rdBoost == 1:
                player.speed *= 1.3
                if player.speed >= 6:
                    player.speed = 6

            elif rdBoost == 2:
                health_points += rd.randint(80, 200)
                if health_points > max_healt:
                    health_points = max_healt

            elif rdBoost == 3:
                player.radius -= 5
                if player.radius < 5:
                    player.radius = player.radius + 5

            elif rdBoost == 4:
                # obstacles.pop(0)
                if len(obstacles) == 0:
                    print("obstacle list empty")
                else:
                    obstacles.pop(0)

            boosters.remove(boost)

    # Sender tekst for hvilke boost
    if display_boost_message_timer > 0:
        window.blit(boostMessage(rdBoost), (player.x + 20, player.y + 20))
        display_boost_message_timer -= 0.2

    # Går igjennom listene for hinder og legger til funksjoner om de kolliderer
    for i in range(len(obstacles)):
        for j in range(i + 1, len(obstacles)):
            if obstacles[i].hinder_collision(obstacles[j]):
                
                # Denne koden gjør at de røde vil overføre farten til den andre.
                obstacles[i].ballCollision(obstacles[j])

                # Denne koden holder farten til hvert hinder, men de skifter retning, slik som i ballCollision()
                # obstacles[i].xSpeed -=  obstacles[i].xSpeed * 2
                # obstacles[i].ySpeed -= obstacles[i].ySpeed * 2

                # obstacles[j].xSpeed -=  obstacles[j].xSpeed * 2
                # obstacles[j].ySpeed -= obstacles[j].ySpeed * 2


    
        
    

    # Sniper mode endrer variabler hvis en knapp blir trykt
    if sniperMode:
        bulletDmg = 8
        bulletFreq = 850
        projectileSpeed = 22
        ammo_cost = 7
    else:
        bulletDmg = 2
        bulletFreq = 170
        projectileSpeed = 11
        ammo_cost = 2.5

    # Hvis det har gått en viss tid går koden for å gi våpen til spilleren
    if elapsed_time >= weapon_activate:

        if player.ammo_count > 0:

            # hver angitt tid i millisekund vil spilleren ha mulighet til å skyte
            if elapsed_time - last_spawn_bullet >= bulletFreq:

                player.look(keys_pressed)

                last_spawn_bullet = elapsed_time

            # Går igjennom listen som blir laget av player.look(), tegner skuddene
            for bullet in bullets:
                bullet.draw()
                bullet.move()

                # Fjerner et skudd når den treffer en vegg
                if bullet.hitWall == True:
                    bullets.remove(bullet)

                # Går igjennom hinder, hvis et skudd treffer et hinder fjerner litt helse, og hinderet fjernes hvis helsen dens går til null
                for obstacle in obstacles:

                    if bullet.hinder_collision(obstacle):
                        obstacle.health -= bulletDmg
                        # print(obstacle.health)

                        if obstacle.health <= 0:
                            obstacles.remove(obstacle)

    # Tegner mengden skudd spilleren har ved en oransje rektangel under spiller hp
    pg.draw.rect(
        window, "orange", (0, 12, (WINDOW_WIDTH / max_ammo) * player.ammo_count, 8.5)
    )

    # Melding som viser at skyting er aktivert
    gun_message = font.render("GUN ACTIVATED", True, (18, 150, 225))

    # Kode for å vise gun_message til skjermen i mellom to tider
    if elapsed_time >= weapon_activate and elapsed_time <= weapon_activate + 3000:
        window.blit(gun_message, (player.x - 150, player.y - 100))

    points = (
        elapsed_time / 1000
    )  # Var poeng blir gitt opp i sekunder, elapsed time er milli sek.
    if health_points <= 0:
        fortsett = False
        print(f"Your time was {points} seconds! \n")

    # Spillet stopper hvis det ikke finnes flere hinder
    if len(obstacles) == 0:
        fortsett = False
        print(f"Your time was {points} seconds! \n")

    player.draw()
    pg.display.flip()

    clock.tick(fps)
    # print(clock.get_rawtime())

pg.quit()
#
