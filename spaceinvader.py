import pygame
import random
import math
from pygame import mixer

# #backgroundmusic
# mixer.music.load('falling4.wav')
# mixer.music.play(-1)


# Initialize the pygame
pygame.init()

# creating the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invader")
Icon = pygame.image.load("ufo.png")
pygame.display.set_icon(Icon)

# background
background = pygame.image.load("background.png")

# player
playerimg = pygame.image.load("spaceship.png")
playerx = 390
playery = 520
playerX_change = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyx.append(random.randint(0, 765))
    enemyy.append(random.randint(50, 200))
    enemyX_change.append(5)
    enemyY_change.append(20)

# bullet
bulletimg = pygame.image.load("bullet.png")
bulletx = 0
bullety = 500
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"  # u can't see the bullet and "fire" we can see


def enemy(x, y, i):
    # blit means to drw the image on screen
    screen.blit(enemyimg[i], (x, y))


over_font = pygame.font.Font('freesansbold.ttf', 64)


def gameover():
    over_text = over_font.render("Game over", True, (255, 255, 255))
    screen.blit(over_text, (250, 250))


def player(x, y):
    # blit means to drw the image on screen
    screen.blit(playerimg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x, y))


def iscollision(bulletx, bullety, enemyx, enemyy):
    distance = math.sqrt(math.pow(enemyx - bulletx, 2) + math.pow(enemyy - bullety, 2))
    if distance < 20:
        return True
    return False


# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textx = 10
texty = 10


def show_score(x, y):
    score_value = font.render("Score :" + str(score), True, (0, 0, 255))
    screen.blit(score_value, (x, y))


running = True
# Game loop
while running:

    # background image
    screen.blit(background, (0, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # for closing the program
            running = False
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":  # checks whether bullet is on the screen
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player movement
    playerx += playerX_change

    # checking for boundaries of spaceship
    if playerx <= 0 or playerx >= 781:
        playerX_change = 0

    # controlling for boundaries of enemy
    for i in range(num_of_enemies):
        if enemyy[i] > 400:
            for j in range(num_of_enemies):
                enemyy[i] = 2000
            gameover()
            break

        if enemyx[i] <= 0:
            enemyX_change[i] = 4
            enemyy[i] += enemyY_change[i]
        elif enemyx[i] >= 765:
            enemyX_change[i] = -4
            enemyy[i] += enemyY_change[i]
        # enemy movement
        enemyx[i] += enemyX_change[i]
        # collision and score
        collision = iscollision(bulletx, bullety, enemyx[i], enemyy[i])
        if collision:
            bullety = 500
            bullet_state = "ready"
            score += 1
            enemyx[i] = random.randint(0, 800)
            enemyy[i] = random.randint(50, 200)
        enemy(enemyx[i], enemyy[i], i)

    # bullet movement
    if bullety <= 0:
        bullety = 500
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bulletY_change


    # enemy movement
    enemyx += enemyX_change

    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()

