SIZE = (700,500)
WHITE = (255,255,255)

import pygame
import random
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("tank game")
backing = pygame.image.load("backing.jpg")
tank = pygame.image.load("tankpic.png")
badguy = pygame.image.load("badguy.png")
bomb = pygame.image.load("bombpic.png")
bomb2 = pygame.image.load("bomb2.png")
explosion = pygame.image.load("explosion.png")
lightning = pygame.image.load("lightning.png")
score = 0
difficulty = 0

#CLASSES
class Tank(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.spd = 10
        self.hitbox = (self.x, self.y, tank.get_width(), tank.get_height())

    def draw(self,screen):
        screen.blit(tank, (self.x, self.y))
        self.hitbox = (self.x, self.y, tank.get_width(), tank.get_height())
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

class Badguy(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self,screen):
        screen.blit(badguy, (self.x, self.y))

class Bomb(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.spd = int(1+difficulty//1)
        self.hitbox = (self.x, self.y, bomb.get_width(), bomb.get_height() - 5)

    def draw(self,screen):
        screen.blit(bomb, (self.x, self.y))
        self.hitbox = (self.x, self.y, bomb.get_width(), bomb.get_height())
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        global score
        score += 1

class Bomb2(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.spd = int(2+difficulty//1)
        self.hitbox = (self.x, self.y, bomb2.get_width(), bomb2.get_height())

    def draw(self,screen):
        screen.blit(bomb2, (self.x, self.y))
        self.hitbox = (self.x, self.y, bomb2.get_width(), bomb2.get_height() - 5)
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        global score
        score += 2

class Lightning (object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.spd = 8

    def draw(self,screen):
        screen.blit(lightning, (self.x, self.y))

    def dodged(self):
        global score
        score += 3

class Projectile(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.spd = 9

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)

#REDRAW
def redraw_game_window():
    screen.blit(backing, (0,0))
    player.draw(screen)
    enemy.draw(screen)
    for shell in bombs:
        shell.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for bolt in lightnings:
        bolt.draw(screen)
    font = pygame.font.SysFont('Calibri', 25, True, False)
    text = font.render("score: " + str(score),True,(0, 0, 0))
    screen.blit(text, [20, 20])
    pygame.display.flip()
    

player = Tank( 315, 440, tank.get_width(), tank.get_height())
enemy = Badguy( 300, 5, badguy.get_width(), badguy.get_height())
bullets = []
bombs = []
lightnings = []
boss_battle = pygame.USEREVENT
pygame.time.set_timer(boss_battle, 10000)
bombdrop = pygame.USEREVENT + 1
pygame.time.set_timer(bombdrop, 1700)
shootLoop = 0
#Main Loop
game_over = False
running = True
while running:

    if shootLoop > 0:
        shootLoop +=1
    if shootLoop > 2:
        shootLoop = 0

    pygame.time.delay(10)

    bullet_limit = int(score/5 + 5//1)
    difficulty += score/10000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == boss_battle:
            r = 0
            while r< random.randint(3,8):
                lightnings.append(Lightning(random.randint(0,661), 0, lightning.get_width(), lightning.get_height()))
                r+=1

        if event.type == bombdrop:
            if random.randint(0,2) == 0:
                bombs.append(Bomb(random.randint(0,661), 0, bomb.get_width(), bomb.get_height()))
            else:
                bombs.append(Bomb2(random.randint(0,661), 0, bomb2.get_width(), bomb2.get_height()))

    for bolt in lightnings:
        if bolt.y - lightning.get_height() < player.hitbox[1] + player.hitbox[3] and bolt.y +lightning.get_height() > player.hitbox[1]:
            if bolt.x + lightning.get_width() > player.hitbox[0] and bolt.x < player.hitbox[0] + player.hitbox[2]:
                game_over = True
        if bolt.y < 450:
            bolt.y+=bolt.spd
        else:
            bolt.dodged()
            lightnings.pop((lightnings.index(bolt)))

    for bullet in bullets:
        if bullet.y > 0:
            bullet.y-=bullet.spd
        else:
            bullets.pop((bullets.index(bullet)))

    for shell in bombs:
        if shell.y < 450:
            shell.y+=shell.spd
        else:
            game_over = True

    if len(bombs) != 0:
        for shell in bombs:
            for bullet in bullets:
                if bullet.y - bullet.radius < shell.hitbox[1] + shell.hitbox[3] and bullet.y + bullet.radius > shell.hitbox[1]:
                    if bullet.x + bullet.radius > shell.hitbox[0] and bullet.x - bullet.radius < shell.hitbox[0] + shell.hitbox[2]:
                        bullets.pop((bullets.index(bullet)))
                        shell.hit()
                        if shell in bombs:
                            bombs.pop((bombs.index(shell)))

    button = pygame.key.get_pressed()

    if button[pygame.K_SPACE] and shootLoop == 0:  
        if len(bullets) < bullet_limit :
            bullets.append(Projectile(round(player.x + player.width //2), round(player.y + player.height //2), 6, (164,84,255)))
        shootLoop = 1

    if button[pygame.K_RIGHT] and player.x<(700-tank.get_width()):
        player.x += player.spd 
    if button[pygame.K_LEFT] and player.x>0:
        player.x-=player.spd

    if game_over:
        bullets = []
        lightnings = []
        screen.blit(backing, (0,0))
        screen.blit(explosion, (player.x-200,170))
        enemy.draw(screen)
        font = pygame.font.SysFont('Calibri', 75, True, False)
        text = font.render(" Game Over! " + "Score: " + str(score),True,(164, 84, 255))
        screen.blit(text, [20, 230])
        pygame.display.flip()
    else:
        redraw_game_window()



screen.fill(WHITE)
pygame.display.flip()
pygame.quit()