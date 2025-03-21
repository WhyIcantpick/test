from pygame import *


#клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
   #конструктор класу
   def __init__(self, sprite_image, sprite_x, sprite_y, size_x, size_y):
       # Викликаємо конструктор класу (Sprite):
       sprite.Sprite.__init__(self)
       #кожен спрайт повинен зберігати властивість image - зображення
       self.image = transform.scale(image.load(sprite_image), (size_x, size_y))


       #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
       self.rect = self.image.get_rect()
       self.rect.x = sprite_x
       self.rect.y = sprite_y
   #метод, що малює героя на вікні
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))




class Player(GameSprite):
   #метод, у якому реалізовано управління спрайтом за кнопками стрілочкам клавіатури
   def __init__(self, sprite_image, sprite_x, sprite_y, size_x, size_y, player_x_speed,player_y_speed):
       # Викликаємо конструктор класу (Sprite):
       GameSprite.__init__(self, sprite_image, sprite_x, sprite_y, size_x, size_y)


       self.x_speed = player_x_speed
       self.y_speed = player_y_speed
   ''' переміщає персонажа, застосовуючи поточну горизонтальну та вертикальну швидкість'''
   def update(self):
       # Спершу рух по горизонталі
       if player.rect.x <= win_width-80 and player.x_speed > 0 or player.rect.x >= 0 and player.x_speed < 0:
           self.rect.x += self.x_speed
           # якщо зайшли за стінку, то встанемо впритул до стіни
       platforms_touched = sprite.spritecollide(self, barriers, False)
       if self.x_speed > 0: # йдемо праворуч, правий край персонажа - впритул до лівого краю стіни
           for p in platforms_touched:
               self.rect.right = min(self.rect.right, p.rect.left) # якщо торкнулися відразу кількох, то правий край - мінімальний із можливих
       elif self.x_speed < 0: # йдемо ліворуч, ставимо лівий край персонажа впритул до правого краю стіни
           for p in platforms_touched:
               self.rect.left = max(self.rect.left, p.rect.right) # якщо торкнулися кількох стін, то лівий край - максимальний
       if player.rect.y <= win_height-80 and player.y_speed > 0 or player.rect.y >= 0 and player.y_speed < 0:
           self.rect.y += self.y_speed
       # якщо зайшли за стінку, то встанемо впритул до стіни
       platforms_touched = sprite.spritecollide(self, barriers, False)
       if self.y_speed > 0: # йдемо вниз
           for p in platforms_touched:
               self.y_speed = 0
               # Перевіряємо, яка з платформ знизу найвища, вирівнюємося по ній, запам'ятовуємо її як свою опору:
               if p.rect.top < self.rect.bottom:
                   self.rect.bottom = p.rect.top
       elif self.y_speed < 0: # йдемо вгору
           for p in platforms_touched:
               self.y_speed = 0 # при зіткненні зі стіною вертикальна швидкість гаситься
               self.rect.top = max(self.rect.top, p.rect.bottom) # вирівнюємо верхній край по нижніх краях стінок, на які наїхали
   def fire(self):
       bullet = Bullet("sword.png", self.rect.right, self.rect.centery, 15, 30, 15)
       bullets.add(bullet)

class Enemy(GameSprite):
    direction = "left"
    def __init__(self, enemy_image, enemy_x, enemy_y, size_x, size_y, enemy_speed):
        GameSprite.__init__(self, enemy_image, enemy_x, enemy_y, size_x, size_y)
        self.speed = enemy_speed
    def update(self):
        if self.rect.x <= 150:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, bullet_image, bullet_x, bullet_y, size_x, size_y, bullet_speed):
        GameSprite.__init__(self, bullet_image, bullet_x, bullet_y, size_x, size_y)
        self.speed = bullet_speed
        self.image = transform.rotate(self.image, 270)
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()

#Створюємо віконце
win_width = 700
win_height = 500
display.set_caption("Лабіринт")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("dfYhE7.jpg"), (win_width, win_height))


#Створюємо групу для стін
barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()

#Створюємо стіни картинки
w1 = GameSprite('platform.png',win_width/2 - win_width/3, win_height/5, 250, 50)
w2 = GameSprite('platform.png', 100, 100, 50, 400)
w3 = GameSprite('platform.png', 350, 270, 500, 40)
w4 = GameSprite('platform.png', 500, win_height/5, 250, 50)

#додаємо стіни до групи
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)

#створюємо спрайти
player = Player('knight.png', 5, win_height - 80, 80, 80, 0, 0)
monster1 = Enemy('monster_4.png', 150, 165, 80, 80, 5)
monster2 = Enemy('monster_4.png', win_width - 80, 360, 80, 80, 10)
final_sprite = GameSprite('treasure2.png', win_width - 100, win_height - 100, 100, 60)

monsters.add(monster1)
monsters.add(monster2)

#змінна, що відповідає за те, як закінчилася гра
finish = False
#ігровий цикл
run = True
while run:


    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                player.x_speed = -10
            elif e.key == K_RIGHT:
                player.x_speed = 10
            elif e.key == K_UP :
                player.y_speed = -10
            elif e.key == K_DOWN :
                player.y_speed = 10
            elif e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT :
                player.x_speed = 0
            elif e.key == K_RIGHT:
                player.x_speed = 0
            elif e.key == K_UP:
                player.y_speed = 0
            elif e.key == K_DOWN:
                player.y_speed = 0

    if not finish:
        window.blit(background, (0,0))#зафарбовуємо вікно кольором
        #малюємо об'єкти
        # w1.reset()
        # w2.reset()
        barriers.draw(window)
        bullets.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, monsters, True, True)
        monsters.draw(window)
        final_sprite.reset()
        player.reset()
        #включаємо рух
        player.update()
        monsters.update()
        bullets.update()
        #Перевірка зіткнення героя з ворогом та стінами
        if sprite.spritecollide(player, monsters, False):
            finish = True
            # обчислюємо ставлення
            img = image.load('game_over2.jpg')
            window.fill((255, 255, 255))
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))


        if sprite.collide_rect(player, final_sprite):
            finish = True
            img = image.load('victory.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
            #цикл спрацьовує кожну 0.05 секунд
    time.delay(30)
    display.update()
