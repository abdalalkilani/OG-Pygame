from turtle import screensize
import pygame
pygame.init()
screenWidth = 1024
screenLength = 768
win = pygame.display.set_mode((screenWidth,screenLength))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('background.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('ShotEffect.mp3')
hitSound = pygame.mixer.Sound('hit.mp3')
playerHit = pygame.mixer.Sound('Bruh.mp3')
music = pygame.mixer.music.load('FightMusic.mp3')
pygame.mixer.music.play(-1)

score1 = 0
score2 = 0

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 50
        self.y = screenLength-230
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        playerHit.play()
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()
                


class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        #pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)s
        pygame.draw.ellipse(win, self.color, (self.x,self.y, 15, 5))


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, start, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.path = [self.start, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 9
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (9 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')

        

def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('Player 1 score: ' + str(score1), 1, (0,0,255))
    win.blit(text, (50, 10))
    text1 = font.render('Player 2 score: ' + str(score2), 1, (255,0,0))
    win.blit(text1, (screenWidth-200, 10))
    man.draw(win)
    man2.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    for bullet2 in bullets2:
        bullet2.draw(win)
    pygame.display.update()


#mainloop
font = pygame.font.SysFont('comicsans', 20, True)
man = player(50, screenLength-230, 64,64)
man2 = player(screenWidth-100, screenLength-230, 64,64)
goblin = enemy(screenWidth/2, screenLength-225, 64, 64, 100, screenWidth-164)
shootLoop = 0
shootLoop2 = 0
bullets = []
bullets2 = []
run = True
while run:
    clock.tick(27)
#man1
    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score1 -= 5

        for bullet in bullets:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    hitSound.play()
                    goblin.hit()
                    score1 += 1
                    bullets.pop(bullets.index(bullet))
                
            if bullet.x < screenWidth and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
    else:
        for bullet in bullets:
            if bullet.x < screenWidth and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 15:
        shootLoop = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    

    keys = pygame.key.get_pressed()

    if keys[pygame.K_f] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,0,255), facing))

        shootLoop = 1

    if keys[pygame.K_a] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_d] and man.x < screenWidth - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
        
    if not(man.isJump):
        if keys[pygame.K_w]:
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

#man2

    if goblin.visible == True:
        if man2.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man2.hitbox[1] + man2.hitbox[3] > goblin.hitbox[1]:
            if man2.hitbox[0] + man2.hitbox[2] > goblin.hitbox[0] and man2.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man2.hit()
                score2 -= 5

            for bullet2 in bullets2:
                if bullet2.y - bullet2.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet2.y + bullet2.radius > goblin.hitbox[1]:
                    if bullet2.x + bullet2.radius > goblin.hitbox[0] and bullet2.x - bullet2.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                        hitSound.play()
                        goblin.hit()
                        score2 += 1
                        bullets2.pop(bullets2.index(bullet2))
                        
                if bullet2.x < screenWidth and bullet2.x > 0:
                    bullet2.x += bullet2.vel
                else:
                    bullets2.pop(bullets2.index(bullet2))
    else:
        for bullet2 in bullets2:
            if bullet2.x < screenWidth and bullet2.x > 0:
                bullet2.x += bullet2.vel
            else:
                bullets2.pop(bullets2.index(bullet2))

    if shootLoop2 > 0:
        shootLoop2 += 1
    if shootLoop2 >  15:
        shootLoop2 = 0


    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop2 == 0:
        bulletSound.play()
        if man2.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets2) < 5:
            bullets2.append(projectile(round(man2.x + man2.width //2), round(man2.y + man2.height//2), 6, (255,0,0), facing))

        shootLoop2 = 1

    if keys[pygame.K_LEFT] and man2.x > man2.vel:
        man2.x -= man2.vel
        man2.left = True
        man2.right = False
        man2.standing = False
    elif keys[pygame.K_RIGHT] and man2.x < screenWidth - man2.width - man2.vel:
        man2.x += man.vel
        man2.right = True
        man2.left = False
        man2.standing = False
    else:
        man2.standing = True
        man2.walkCount = 0
        
    if not(man2.isJump):
        if keys[pygame.K_UP]:
            man2.isJump = True
            man2.walkCount = 0
    else:
        if man2.jumpCount >= -10:
            neg2 = 1
            if man2.jumpCount < 0:
                neg2 = -1
            man2.y -= (man2.jumpCount ** 2) * 0.5 * neg2
            man2.jumpCount -= 1
        else:
            man2.isJump = False
            man2.jumpCount = 10
    
    redrawGameWindow()

pygame.quit()
