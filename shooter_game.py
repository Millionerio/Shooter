
from pygame import *
from random import randint

# переменные
lost = 0
score = 0
weight = 700
height = 500
run = True
finish = False
FPS = 60
clock = time.Clock()
# классы
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
# класс Player
class Player(GameSprite):
    # метод для управления спрайтом
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
    # метод "выстрел"
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 15, 20)
        bullets.add(bullet)
#класс Enemy
class Enemy(GameSprite): 
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(5, 630)
            self.rect.y = 0
            lost = lost + 1
# класс Bullet
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# создаем окно, даем ему название
window = display.set_mode((weight, height))
display.set_caption("Shuter")
# создаем объект картнку и адаптируем под размер окна и 
# и отображаем в окне
bg = transform.scale(image.load('galaxy.jpg'), (weight, height))
# подключение музыки
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

#шрифты и надписи
font.init()
font1 = font.SysFont('Arial', 70)
font2 = font.SysFont('Arial', 36)
lose = font1.render('YOU LOSE! TRY AGAIN!', True, (255,50,0))
win = font1.render('YOY WIN! GOOOOD JOB!', True, (0,255,0))


# игровые объекты
rocket = Player('rocket.png', 320, 400, 10, 50, 100)
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy('asteroid.png', randint(80, 700 - 80), -40, randint(1, 10), 50, 50)
   monsters.add(monster)
bullets = sprite.Group()
# игровой цикл
while run:
    # проверяем нажата ли кнопка закрыть окно
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()

    if finish != True:
        window.blit(bg, (0,0))
        rocket.reset()
        rocket.update()

        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()
        
        #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        sprite_list = sprite.spritecollide( rocket, monsters, False)
        #возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if sprite_list or lost >= 3:
            finish = True
            window.blit(lose, (50, 250))

        #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        sprite_list_group = sprite.groupcollide(monsters, bullets, True, True)
        for s_l_g in sprite_list_group:
            score += 1
            monster = Enemy('asteroid.png', randint(80, 700 - 80), 0, randint(1, 10), 50, 50)
            monsters.add(monster)

        #проверка выигрыша: сколько очков набрали?
        if score >= 10:
            finish = True
            window.blit(win, (50, 250))



        # пишем текст на экране
        text_score = font2.render('Счет: '+ str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 10))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 40))

        display.update()
        clock.tick(FPS)
    #бонус: автоматический перезапуск игры
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
    
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy('asteroid.png', randint(80, 700 - 80), -40, randint(1, 10), 50, 50)
            monsters.add(monster)
        
    
    time.delay(50)




        #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
       
        #возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        

        #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        

        #проверка выигрыша: сколько очков набрали?

        #бонус: автоматический перезапуск игры
       