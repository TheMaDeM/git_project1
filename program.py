import pygame
import sys
import os

# инициализация
FPS = 60
pygame.init()
size = WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
a = False


def terminate():    # выход из игры
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):    # загрузка картинки
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        terminate()
    im = pygame.image.load(fullname)
    if colorkey is not None:
        im = im.convert()
        if colorkey == -1:
            colorkey = im.get_at((0, 0))
        im.set_colorkey(colorkey)
    else:
        im = im.convert_alpha()
    return im


def load_level(filename):   # загрузка уровня
    filename = "data/" + filename

    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):    # создание уровня
    new_player, new_enemy, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Ground(x, y)
            elif level[y][x] == '#':
                Box(x, y)
            elif level[y][x] == '@':
                Ground(x, y)
                new_player = Player(x, y)
            elif level[y][x] == '!':
                Ground(x, y)
                new_enemy = Enemy(x, y)
    return new_player, new_enemy, x, y


def boom(tank, x, y):  # взрыв танка
    global player, enemy, a, b
    if tank == 'player':
        player.rect.x = -100
        player = AnimatedSprite(boom_image, 4, 1, x, y)
        b = 'player'
    else:
        enemy.rect.x = -100
        enemy = AnimatedSprite(boom_image, 4, 1, x, y)
        b = 'enemy'
    a = False


def start_screen():    # главное меню / правила игры
    main_menu = True
    rules = False
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))

    images = [[pygame.Surface([300, 50]), 'black', (450, 350)],
              [pygame.Surface([300, 50]), 'dark green', (455, 355)],
              [pygame.Surface([300, 50]), 'black', (450, 450)],
              [pygame.Surface([300, 50]), 'dark green', (455, 455)],
              [pygame.Surface([300, 50]), 'black', (450, 550)],
              [pygame.Surface([300, 50]), 'dark green', (455, 555)],
              [pygame.Surface([1200, 100]), (20, 20, 20), (0, 0)],
              [pygame.Surface([1200, 700]), (50, 50, 50), (0, 100)],
              [pygame.Surface([300, 50]), (20, 20, 20), (450, 650)],
              [load_image('tank.png'), (50, 350)],
              [load_image('enemy.png'), (50, 450)]]

    lines = [['ТАНЧИКИ', 155, 'black', [350, 50]],
             ['ТАНЧИКИ', 155, 'dark green', [355, 55]],
             ['ИГРАТЬ', 60, 'white', [530, 360]],
             ['ПРАВИЛА', 60, 'white', [510, 460]],
             ['ВЫЙТИ', 60, 'white', [530, 560]],
             ['ПРАВИЛА ИГРЫ', 150, 'white', [180, 10]],
             ['НАЗАД', 60, 'white', [520, 660]],
             ['ИГРА НА ДВОИХ', 80, 'white', [400, 150]],
             ['ЦЕЛЬ: УНИЧТОЖИТЬ СОПЕРНИКА', 60, 'white', [50, 250]],
             ['ИГРОК 1 -> УПРАВЛЕНИЕ: СТРЕЛКАМИ; СТРЕЛЬБА: ЛКМ', 40, 'white', [110, 360]],
             ['ИГРОК 2 -> УПРАВЛЕНИЕ: WASD; СТРЕЛЬБА: ПРОБЕЛ', 40, 'white', [110, 460]],
             ['УРОВЕНЬ ЗАГРУЖАЕТСЯ ИЗ ТЕКСТОВОГО ФАЙЛА', 40, 'white', [50, 540]],
             ['ПОСЛЕ УНИЧТОЖЕНИЯ ОДНОГО ИЗ ТАНКОВ, ИГРА ОСТАНАВЛИВАЕТСЯ', 40, 'white', [50, 600]]]

    while True:
        screen.fill((0, 0, 0))

        if main_menu:
            screen.blit(fon, (0, 0))

            for image in images[:6]:
                image[0].fill(pygame.Color(image[1]))
                screen.blit(image[0], image[2])

            for line in lines[:5]:
                text, font, color, coords = line
                string = pygame.font.Font(None, font).render(text, True, pygame.Color(color))
                text_size = string.get_rect()[2:]
                rect = (*coords, *text_size)
                screen.blit(string, rect)

        if rules:
            for image in images[6:9]:
                image[0].fill(pygame.Color(image[1]))
                screen.blit(image[0], image[2])

            for image in images[9:]:
                screen.blit(image[0], image[1])

            for line in lines[5:]:
                text, font, color, coords = line
                string = pygame.font.Font(None, font).render(text, True, pygame.Color(color))
                text_size = string.get_rect()[2:]
                rect = (*coords, *text_size)
                screen.blit(string, rect)

        for screen_event in pygame.event.get():
            if screen_event.type == pygame.QUIT:
                terminate()
            if main_menu:
                if screen_event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = screen_event.pos
                    if 454 < x < 756:
                        if 354 < y < 406:
                            images[1][2] = (450, 350)
                            lines[2][3] = [525, 355]
                        if 454 < y < 506:
                            images[3][2] = (450, 450)
                            lines[3][3] = [505, 455]
                        if 554 < y < 606:
                            terminate()
                if screen_event.type == pygame.MOUSEBUTTONUP:
                    x, y = screen_event.pos
                    if 454 < x < 756:
                        if 354 < y < 406:
                            images[1][2] = (455, 355)
                            lines[2][3] = [530, 360]
                            return
                        if 454 < y < 506:
                            images[3][2] = (455, 455)
                            lines[3][3] = [510, 460]
                            main_menu = False
                            rules = True
            if rules:
                if screen_event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = screen_event.pos
                    if 449 < x < 751:
                        if 649 < y < 701:
                            main_menu = True
                            rules = False
        pygame.display.flip()
        clock.tick(FPS)


start_screen()  # начальный экран

ground_image = load_image('ground.png')
box_image = load_image('box.png')
player_image = load_image('tank.png')
enemy_image = load_image('enemy.png')
shell_image = pygame.Surface([10, 10])
shell_image.fill(pygame.Color('red'))
boom_image = load_image('boom.png', -1)

tile_width = tile_height = 50   # размер клетки

all_sprites = pygame.sprite.Group()
ground_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
shell_group = pygame.sprite.Group()

a = True
b = True
n = 0


class Ground(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(ground_group, all_sprites)
        self.image = ground_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Box(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(box_group, all_sprites)
        self.image = box_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):  # первый игрок
    def __init__(self, pos_x, pos_y):
        self.a = True
        self.x_move, self.y_move = 0, 0
        self.rot, self.stop = 0, 0
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, player_event):
        if player_event.type == pygame.KEYDOWN:
            if player_event.key == pygame.K_UP:
                self.y_move -= 1
            if player_event.key == pygame.K_DOWN:
                self.y_move += 1
            if player_event.key == pygame.K_LEFT:
                self.x_move -= 1
            if player_event.key == pygame.K_RIGHT:
                self.x_move += 1

        if player_event.type == pygame.KEYUP:
            if player_event.key == pygame.K_UP:
                self.y_move += 1
                self.stop = self.rot
            if player_event.key == pygame.K_DOWN:
                self.y_move -= 1
                self.stop = self.rot
            if player_event.key == pygame.K_LEFT:
                self.x_move += 1
                self.stop = self.rot
            if player_event.key == pygame.K_RIGHT:
                self.x_move -= 1
                self.stop = self.rot

    def move(self):  # непрерывное движение
        self.rect.x += self.x_move  # по оси X
        if pygame.sprite.spritecollideany(self, box_group)\
                or pygame.sprite.spritecollideany(self, enemy_group)\
                or self.rect.x < 0 or self.rect.x > 1150:  # проверка не столкновение
            self.rect.x -= self.x_move  # откат

        self.rect.y += self.y_move  # по оси Y
        if pygame.sprite.spritecollideany(self, box_group)\
                or pygame.sprite.spritecollideany(self, enemy_group)\
                or self.rect.y < 0 or self.rect.y > 750:  # проверка не столкновение
            self.rect.y -= self.y_move  # откат

        # расчёт угла поворота картинки в зависимости от направления движения
        if self.y_move == -1:
            self.rot = -45 * self.x_move
        elif self.y_move == 1:
            self.rot = 180 + 45 * self.x_move
        else:
            self.rot = -90 * self.x_move

        # поворот картинки
        if self.a:
            if self.y_move == self.x_move == 0:
                self.image = pygame.transform.rotate(player_image, self.stop)
            else:
                self.image = pygame.transform.rotate(player_image, self.rot)


class Enemy(pygame.sprite.Sprite):  # второй игрок
    def __init__(self, pos_x, pos_y):
        self.x_move, self.y_move = 0, 0
        self.rot, self.stop = 0, 0
        super().__init__(enemy_group, all_sprites)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, player_event):
        if player_event.type == pygame.KEYDOWN:
            if player_event.key == pygame.K_w:
                self.y_move -= 1
            if player_event.key == pygame.K_s:
                self.y_move += 1
            if player_event.key == pygame.K_a:
                self.x_move -= 1
            if player_event.key == pygame.K_d:
                self.x_move += 1

        if player_event.type == pygame.KEYUP:
            if player_event.key == pygame.K_w:
                self.y_move += 1
                self.stop = self.rot
            if player_event.key == pygame.K_s:
                self.y_move -= 1
                self.stop = self.rot
            if player_event.key == pygame.K_a:
                self.x_move += 1
                self.stop = self.rot
            if player_event.key == pygame.K_d:
                self.x_move -= 1
                self.stop = self.rot

    def move(self):  # непрерывное движение
        self.rect.x += self.x_move  # по оси X
        if pygame.sprite.spritecollideany(self, box_group)\
                or pygame.sprite.spritecollideany(self, player_group)\
                or self.rect.x < 0 or self.rect.x > 1150:  # проверка не столкновение
            self.rect.x -= self.x_move  # откат

        self.rect.y += self.y_move  # по оси Y
        if pygame.sprite.spritecollideany(self, box_group)\
                or pygame.sprite.spritecollideany(self, player_group)\
                or self.rect.y < 0 or self.rect.y > 750:  # проверка не столкновение
            self.rect.y -= self.y_move  # откат

        if self.y_move == -1:
            self.rot = -45 * self.x_move
        elif self.y_move == 1:
            self.rot = 180 + 45 * self.x_move
        else:
            self.rot = -90 * self.x_move

        if self.y_move == self.x_move == 0:
            self.image = pygame.transform.rotate(enemy_image, self.stop)
        else:
            self.image = pygame.transform.rotate(enemy_image, self.rot)


class Shell(pygame.sprite.Sprite):  # снаряд танка
    def __init__(self, shooter, target, x, y):
        self.x_move, self.y_move, self.rot = 0, 0, 0
        super().__init__(shell_group, all_sprites)
        self.shooter = shooter
        self.target = target
        if target == player:
            self.target_group = player_group
        else:
            self.target_group = enemy_group
        self.dir = shooter.rot
        if shooter.y_move == shooter.x_move == 0:
            self.dir = shooter.stop
        self.image = shell_image
        if 180 > self.dir > 0:
            self.x_move = -3
        elif self.dir < 0 or self.dir > 180:
            self.x_move = 3
        if self.dir < -90 or self.dir > 90:
            self.y_move = 3
        elif 90 > self.dir > -90:
            self.y_move = -3
        self.rect = self.image.get_rect().move(x + 25, y + 25)

    def update(self):
        self.rect.x += self.x_move
        self.rect.y += self.y_move
        self.image = pygame.transform.rotate(shell_image, self.rot)
        if pygame.sprite.spritecollideany(self, self.target_group):
            if self.target == player:
                boom('player', self.target.rect.x, self.target.rect.y)
            else:
                boom('enemy ', self.target.rect.x, self.target.rect.y)
        if pygame.sprite.spritecollideany(self, box_group):
            self.rect.x = -100
            self.rect.y = -100
            self.x_move = 0
            self.y_move = 0


class AnimatedSprite(pygame.sprite.Sprite):  # взрыв танка
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


player, enemy, level_x, level_y = generate_level(load_level('map.txt'))  # данные уровня в текстовом формате

while True:
    for event in pygame.event.get():
        if a:
            player_group.update(event)
            enemy_group.update(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shell = Shell(enemy, player, enemy.rect.x, enemy.rect.y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    shell = Shell(player, enemy, player.rect.x, player.rect.y)
        if event.type == pygame.QUIT:
            terminate()
    screen.fill((0, 0, 0))
    if a:
        player.move()
        enemy.move()
        shell_group.update()
    else:
        if n < 4:
            if b == 'player':
                player.update()
            else:
                enemy.update()
            n += 1
            clock.tick(10)
        else:
            if b == 'player':
                player.rect.x = -100
            else:
                enemy.rect.x = -100

    all_sprites.draw(screen)
    shell_group.draw(screen)
    player_group.draw(screen)
    enemy_group.draw(screen)

    pygame.display.flip()