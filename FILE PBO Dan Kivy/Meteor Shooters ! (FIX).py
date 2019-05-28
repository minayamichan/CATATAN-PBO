import pygame,random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteor Shooter!")
clock = pygame.time.Clock()



paused = False
def pausescreen():
    draw_text(screen, "PAUSED GAME", 30, WIDTH/2, HEIGHT*1/4)
    draw_text(screen, "Press any key to continue", 30, WIDTH/2, HEIGHT*2/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False
def infoscreen():
    screen.fill(WHITE)
    screen.blit(background, background_rect)
    #Controls
    draw_text(screen, "CONTROLS", 17, WIDTH*1/2, 50)
    draw_text(screen, "ARROW KEYS      =  Up, Down, Left, Right", 18,WIDTH*1/2, 80)
    draw_text(screen, "SPACEBAR       =  Shooting the guns", 18, WIDTH*1/2, 110)
    draw_text(screen, "P                =  Pause Menu", 18, WIDTH*1/2, 140)
    #Powerups
    draw_text(screen, "POWERUPS", 18, WIDTH*1/2, 200)
    draw_text(screen, "BULLETS =", 18, 150, 230)
    bullet = pygame.image.load(path.join(img_dir, 'bolt_gold.png'))
    screen.blit(bullet, (230, 230))
    pygame.display.flip()
    draw_text(screen, "EXTRA LIFE =", 18, 150, 280)
    life = pygame.image.load(path.join(img_dir, 'life.png'))
    screen.blit(life, (230, 275))
    draw_text(screen, "SHIELD     =", 18, 150, 330)
    shield = pygame.image.load(path.join(img_dir, 'shield_gold.png'))
    screen.blit(shield, (230, 320))

def newmob2():
    s = Starlord()
    all_sprites.add(s)
    mobs.add(s)

class Starlord(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, "boss3.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = random.randrange(0, WIDTH-10)
        self.rect.bottom = random.randrange(10, 20)
        self.speedx = random.randrange(4,8)
        self.speedy = random.randrange(-4,-2)
        self.lives = 1
        self.power = 1


    def update(self):
        self.rect.centerx += self.speedx
        self.rect.bottom += self.speedy
        #Staying on the screen
        if self.rect.right >= WIDTH:
            self.speedx = random.randrange(-8,-3)
        if self.rect.left <= 0:
            self.speedx = random.randrange(3,8)
        if self.rect.top <= +15:
            self.speedy = random.randrange(2,4)
        if self.rect.bottom >= HEIGHT / 4:
            self.speedy = random.randrange(-4,-2)

        #Randomly shoot
        if self.power == 1:
            if random.randrange(0,75) == 0:
                self.shoot()
        if self.power == 2:
            if random.randrange(0,30) == 0:
                self.shoot()


    def shoot(self):
        if self.power == 1:
            bullet = Enemybullet(self.rect.left, self.rect.centery)
            all_sprites.add(bullet)
            enemybullets.add(bullet)
        if self.power == 2:
            leftbullet = Enemybullet(self.rect.left, self.rect.centery)
            rightbullet = Enemybullet(self.rect.right, self.rect.centery)
            all_sprites.add(leftbullet)
            all_sprites.add(rightbullet)
            enemybullets.add(leftbullet)
            enemybullets.add(rightbullet)


"""
Class: Enemybullet

This is the class for the bullets that shoot from the ship.\
"""
class Enemybullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load(path.join(img_dir, "laserRed.png")).convert()
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = 20

        #pygame.draw.rect(self.image, RED, (x, y, 100, 100), self.radius)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 0
        self.speedy = 8
        pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #Delete if it moves off of the bottom of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -4
        if keystate[pygame.K_RIGHT]:
            self.speedx = 4
        if keystate[pygame.K_UP]:
            self.speedy = -4
        if keystate[pygame.K_DOWN]:
            self.speedy = 4
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if keystate[pygame.K_p]:
            pausescreen()
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet1 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                shoot_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet_Biru(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()
    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()
class Bullet_Biru(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_imgBiru
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun','life'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Meteor Shooter", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Credit : MAYL dan JMR.ID", 22,
              WIDTH / 2, HEIGHT / 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if 170 + 100 > mouse[0] > 70 and 500 + 50 > mouse[1] > 500:
                    waiting = False
                if 370+100 > mouse[0] > 270 and 500 + 50 > mouse[1] > 500:
                    infoscreen()
        mouse = pygame.mouse.get_pos()
        if 70 + 100 > mouse[0] > 70 and 500 + 50 > mouse[1] > 500:
            pygame.draw.rect(screen, RED, (90, 500, 100, 50))
        else:
            pygame.draw.rect(screen, BLUE, (90, 500, 100, 50))
        if 270 + 100 > mouse[0] > 185 and 500 + 50 > mouse[1] > 500:
            pygame.draw.rect(screen, RED, (270, 500, 100, 50))
        else:
            pygame.draw.rect(screen, BLUE, (270, 500, 100, 50))
        draw_text(screen, "P L A Y", 22, 140, 510)
        draw_text(screen, "R U L E S",22, 320,510)
        pygame.display.flip()

# Load all game graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "laserRed13.png")).convert()
bullet_imgBiru = pygame.image.load(path.join(img_dir,"laserRed13.png")).convert()
bullet_imgIjo = pygame.image.load(path.join(img_dir,"laserRed13.png")).convert()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
enemybullets = pygame.sprite.Group()
starlord_sprites = pygame.sprite.Group()

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
powerup_images['life'] = pygame.image.load(path.join(img_dir, 'life.png')).convert()

# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir,'sfx_laser1.ogg'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir,'pow4.ogg'))
power_sound = pygame.mixer.Sound(path.join(snd_dir,'pow4.ogg'))
life_sound = pygame.mixer.Sound(path.join(snd_dir,'pow4.ogg'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir,snd)))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir,'sfx_lose.ogg'))
pygame.mixer.music.load(path.join(snd_dir,'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1)

# Game loop
game_over = True
running = True
paused = False
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(4):
            newmob2()
        score = 0

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score +=  random.randrange(100, 1000) - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob2()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        player.power -= 1
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob2()
        if player.power == 0:
            player.power += 1
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
    hits = pygame.sprite.spritecollide(player, enemybullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        player.power -= 1
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.power == 0:
            player.power += 1
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.power == 1
            player.shield = 100

    # check to see if player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(30, 50)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            power_sound.play()
        if hit.type == 'life':
            if player.lives <=2:
                player.lives += 1
            life_sound.play()
            if player.lives >= 4:
                player.lives -= 1
    # if the player died and the explosion has finished playing
    if player.lives == 0 :
        game_over = True

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
