
from pygame import*
from random import randint
from time import time as timer
window = display.set_mode((700, 500))
display.set_caption('шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
fire_sound = mixer.Sound('fire.ogg')
font.init()
font2 = font.SysFont('Comic Sans MS', 35)
font1 = font.SysFont('Comic Sans MS', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE', True, (180, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, w, h,  player_speed):
        super().__init__()      
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys [K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
        if keys [K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys [K_DOWN] and self.rect.y < 420:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15 , 20, 15)
        bullets.add(bullet)


class Enumy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost 
        if  self.rect.y  > 700:
            self.rect.x =  randint(80, 420)
            self.rect.y = 0
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()



score = 0
lost = 0
asteroids = sprite.Group()
player = Player('rocket.png', 5, 400, 80, 100, 4)
monsters = sprite.Group()
for i in range(5):
    monster = Enumy('ufo.png', randint(80, 420), -40, 80, 50, randint(2, 2))
    monsters.add(monster)
for i in range(3):
    asteroid = Enumy('asteroid.png', randint(70, 420), -30, 70, 50, randint(2,2))
    asteroids.add(asteroid)

    
  
   

finish = False
run = True
life = 3
rel_time = False
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif  e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()
   
            
    if not finish:
        window.blit(background, (0,0))
        monsters.draw(window)
        monsters.update()
        player.reset()
        asteroids.draw(window)
        asteroids.update()
        player.update()
        bullets.draw(window)
        bullets.update()

        if  rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('перезарядка', True, (150, 0, 0))
                window.blit(reload, (255, 400))
            else:
                num_fire = 0
                rel_time = False

        if sprite.groupcollide(monsters, bullets, True, True):
            score += 1
            monster = Enumy('ufo.png', randint(80, 420), -40, 80, 50, randint(2, 2))
            monsters.add(monster)
        if score > 9:
            window.blit(win, (250, 250))
            finish = True
            
        if  sprite.spritecollide(player, monsters, False):
            finish = True

        if  sprite.spritecollide(player, asteroids, True):
            life -= 1

        if life < 1:
            window.blit(lose, (250,250))
            finish = True

        text_lose = font2.render('Пропущено: ' +str(lost), True, (225, 225, 225))
        window.blit(text_lose, (10, 50))
        text_score = font2.render('очки:' +str(score), True, (225, 225, 225))
        window.blit(text_score, (10, 20))
        life_score = font2.render('хп:' +str(life), True, (225, 225, 225))
        window.blit(life_score, (10, 80))


    display.update()
    time.delay(30)



