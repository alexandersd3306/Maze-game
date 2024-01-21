from pygame import *
import time as tm

FPS = 300
win_width = 800
win_height = 700
max_attempts = 3  # Максимальное количество попыток
serdec = max_attempts  # Изначальное количество сердец
window = display.set_mode((win_width, win_height))
display.set_caption("Labirynth")
clock = time.Clock()
mixer.init()
mixer.music.load('music/muz.mp3')
mixer.music.play()
mixer.music.set_volume(0.1)
font.init()
font = font.Font(None, 36)

player_image = 'img/player.png'
player_image2 = 'img/player2.png'
background = transform.scale(image.load('img/background.png'), (win_width, win_height))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, gram_min=0, gram_max=0, right=False):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.gram_max = gram_max
        self.gram_min = gram_min
        self.right = right

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)

    def reset(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x + 70 < win_width:
            if sprite.collide_rect(player, w1) == False and sprite.collide_rect(player, w2) == False:
                self.rect.x += self.speed
                if self.right == False:
                    self.image = transform.scale(image.load(player_image2), (65, 65))
                self.right = True
        elif keys[K_LEFT] and self.rect.x > 0:
            if sprite.collide_rect(player, w1) == False and sprite.collide_rect(player, w2) == False:
                self.rect.x -= self.speed
                if self.right == True:
                    self.image = transform.scale(image.load(player_image), (65, 65))
                self.right = False
        elif keys[K_DOWN] and self.rect.y + 70 < win_height:
            self.rect.y += self.speed
        elif keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed


class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, gram_min, gram_max):
        super().__init__(player_image, player_x, player_y, player_speed, gram_min, gram_max)
        self.motion = "left"

    def reset(self):
        if self.rect.x < self.gram_min:
            self.motion = "right"
        elif self.rect.x > self.gram_max - 70:
            self.motion = "left"
        if self.motion == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Wall(sprite.Sprite):
    def __init__(self, win_h, win_w, col1, col2, col3, wall_x, wall_y):
        super().__init__()
        self.col1 = col1
        self.col2 = col2
        self.col3 = col3
        self.image = Surface((win_h, win_w))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Wall2(sprite.Sprite):
    def __init__(self, win_h, win_w, col1, col2, col3, wall_x, wall_y):
        super().__init__()
        self.col1 = col1
        self.col2 = col2
        self.col3 = col3
        self.image = Surface((win_h, win_w))
        self.image.fill((50, 100, 10))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


player = Player(player_image, 50, 50, 1)
enemy = Enemy('img/enemu.jfif', 70, 150, 1, 0, 235)
enemy2 = Enemy('img/enemu.jfif', 300, 300, 1, 300, 500)
gold = GameSprite('img/konec.png', 900, 700, 2)
g = win_height - 100
w1 = Wall(25, g, 0, 2, 150, 500, 100)
w2 = Wall2(25, g, 0, 0, 50, 250, 1)

game = True
while game and serdec > 0:
    window.blit(background, (0, 0))
    text = font.render('Жизней : ' + str(serdec), True, (255, 0, 255))
    window.blit(text, (5, 5))
    w1.update()
    w2.update()
    player.update()
    player.reset()
    enemy.update()
    enemy2.update()
    enemy.reset()
    enemy2.reset()
    gold.update()
    display.update()

    if sprite.collide_rect(player, enemy):
        serdec -= 1
        tm.sleep(1)
        # Перезапуск игры
        player.rect.x = 50
        player.rect.y = 50
        enemy.rect.x = 70
        enemy.rect.y = 150

    if sprite.collide_rect(player, enemy2):
        serdec -= 1
        tm.sleep(1)
        # Перезапуск игры
        player.rect.x = 50
        player.rect.y = 50
        enemy2.rect.x = 300
        enemy2.rect.y = 300

    if sprite.collide_rect(player, gold):
        img = transform.scale(image.load('img/youwin.jpg'), (win_width // 2, win_height // 2))
        window.fill((255, 255, 255))
        window.blit(img, (win_width // 4, win_height // 4))
        display.update()
        tm.sleep(1)

    for i in event.get():
        if i.type == QUIT:
            game = False

    clock.tick(FPS)

# Завершение игры
img = transform.scale(image.load('img/gameover.png'), (win_width // 2, win_height // 2))
window.fill((255, 255, 255))
window.blit(img, (win_width // 4, win_height // 4))
display.update()
tm.sleep(1)
