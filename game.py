import pygame
from time import time

pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption("First Game")


# This goes outside the while loop, near the top of the program
walkRight = [pygame.image.load('sprites/R1.png'), pygame.image.load('sprites/R2.png'), pygame.image.load('sprites/R3.png'), pygame.image.load('sprites/R4.png'), pygame.image.load('sprites/R5.png'), pygame.image.load('sprites/R6.png'), pygame.image.load('sprites/R7.png'), pygame.image.load('sprites/R8.png'), pygame.image.load('sprites/R9.png')]

walkLeft = [pygame.image.load('sprites/L1.png'), pygame.image.load('sprites/L2.png'), pygame.image.load('sprites/L3.png'), pygame.image.load('sprites/L4.png'), pygame.image.load('sprites/L5.png'), pygame.image.load('sprites/L6.png'), pygame.image.load('sprites/L7.png'), pygame.image.load('sprites/L8.png'), pygame.image.load('sprites/L9.png')]

bg = pygame.image.load('sprites/bg.jpg')
char = pygame.image.load('sprites/standing.png')
dagger_right = pygame.image.load("sprites/dagger-straight-right.png")
dagger_left = pygame.image.load("sprites/dagger-straight-left.png")

clock = pygame.time.Clock()

bullet_Sound = pygame.mixer.Sound("audio/bullet.wav")
hit_Sound = pygame.mixer.Sound("audio/hit.wav")

music = pygame.mixer.music.load("audio/music.mp3")
pygame.mixer.music.play(-1)

score = 0

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 9
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        
        
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox,2)


    def hit(self):
        self.isJump = False
        self.jumpCount = 9
        self.x  = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont("comicsans", 100)
        text = font1.render("-5", 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 60:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 61
                    pygame.quit()


class Projectile(object):
    def __init__(self, x, y, width, height, facing):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # self.radius = radius
        # self.color = color
        self.facing = facing
        self.vel = 20 * facing
    
    def draw(self, win):
        # pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        if player.right:
            win.blit(dagger_right, (self.x, self.y))
        
        if player.left:
            win.blit(dagger_left, (self.x, self.y))


class Enemy(object):
    walkRight = [pygame.image.load("sprites/R1E.png"), pygame.image.load("sprites/R2E.png"), pygame.image.load("sprites/R3E.png"), pygame.image.load("sprites/R4E.png"), pygame.image.load("sprites/R5E.png"), pygame.image.load("sprites/R6E.png"), pygame.image.load("sprites/R7E.png"), pygame.image.load("sprites/R8E.png"), pygame.image.load("sprites/R9E.png"), pygame.image.load("sprites/R10E.png"), pygame.image.load("sprites/R11E.png")]
    
    walkLeft = [pygame.image.load("sprites/L1E.png"), pygame.image.load("sprites/L2E.png"), pygame.image.load("sprites/L3E.png"), pygame.image.load("sprites/L4E.png"), pygame.image.load("sprites/L5E.png"), pygame.image.load("sprites/L6E.png"), pygame.image.load("sprites/L7E.png"), pygame.image.load("sprites/L8E.png"), pygame.image.load("sprites/L9E.png"), pygame.image.load("sprites/L10E.png"), pygame.image.load("sprites/L11E.png")]


    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walk_Count = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True
        self.last = pygame.time.get_ticks()
        self.cooldown = 2000
        
    
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walk_Count + 1 >= 33:
                self.walk_Count = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walk_Count//3], (self.x, self.y))
                self.walk_Count += 1
            else:
                win.blit(self.walkLeft[self.walk_Count//3], (self.x, self.y))
                self.walk_Count += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox,2)


    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_Count = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_Count = 0


    def hit(self):        
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False


    def spawnEnemy(self):
        pass


player = Player(300, 410, 64, 64)

def redrawGameWindow():

    win.blit(bg, (0,0))
    text = font.render("Score: " + str(score), 1, (0,0,0))
    win.blit(text, (350, 10))
    
    player.draw(win)

    en.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()

# Drawing to screen

font = pygame.font.SysFont("comicsans", 32, True)

player = Player(360, 410, 64, 64)
en = Enemy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = []
run = True

while run:
    clock.tick(27)

    if en.visible == True:
        if player.hitbox[1] < en.hitbox[1] + en.hitbox[3] and player.hitbox[1] + player.hitbox[3] > en.hitbox[1]:
            if player.hitbox[0] + player.hitbox[2] > en.hitbox[0] and player.hitbox[0] < en.hitbox[0] + en.hitbox[2]:
                player.hit()
                score -= 5

    if en.visible == False:
        now = pygame.time.get_ticks()
        if now - en.last >= en.cooldown:
            en.last = now
            en = Enemy(100, 410, 64, 64, 450)
            print("New enemy has spawned")
    else:
        en.last = pygame.time.get_ticks()
        en.cooldown = 2000
    
    
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        radius = (bullet.width / 2)

        if bullet.y - radius < en.hitbox[1] + en.hitbox[3] and bullet.y + radius > en.hitbox[1]:
            if bullet.x - radius > en.hitbox[0] and bullet.x - radius < en.hitbox[0] + en.hitbox[2]:
                hit_Sound.play()
                en.hit()
                score += 1
                
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bullet_Sound.play()
        if player.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(Projectile(round(player.x+player.width//2), round(player.y + player.height//2), 24, 24, facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
        player.left = True
        player.right = False
        player.standing = False
    elif keys[pygame.K_RIGHT] and player.x < 500 - player.width - player.vel:
        player.x += player.vel
        player.right = True
        player.left = False
        player.standing = False

    else:
        player.standing = True
        player.walk_Count = 0

    if not (player.isJump):        
        if keys[pygame.K_UP]:
            player.isJump = True
            player.right = False
            player.left = False
            player.walk_Count = 0    
    else:
        if player.jumpCount >= -9:
            neg = 1
            if player.jumpCount < 0:
                neg = -1
            player.y -= (player.jumpCount ** 2) * 0.5 * neg
            player.jumpCount -= 1
        else:
            player.isJump = False
            player.jumpCount = 9

    redrawGameWindow()

pygame.quit()


