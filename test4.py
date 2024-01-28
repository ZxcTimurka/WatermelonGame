import math
import random
import sys

import pygame
import pymunk
import pymunk.pygame_util


def c_skin(skin, n):
    skin_list = ['base_skin', 'furry_skin']
    num = skin_list.index(skin)
    if num + n > len(skin_list) - 1:
        num = 0
    elif num + n < 0:
        num = len(skin_list) - 1
    return skin_list[num]


# Загрузка изображения
def load_image(radius, image='imgs/smile.png'):
    ball_image = pygame.image.load(image)
    ball_image = pygame.transform.scale(ball_image, (radius * 2, radius * 2))
    return ball_image


def terminate():
    pygame.quit()
    sys.exit()


# Переменная для отслеживания количества шаров
ball_count = 0
sp_coord = (0, 0)
score = 0
pygame.init()
my_font = pygame.font.SysFont(None, 40)
space = pymunk.Space()
pause = True


def start_screen():
    global pause

    fon = pygame.transform.scale(pygame.image.load('imgs/fon.png'), (width, height))
    screen.blit(fon, (0, 0))

    intro_text = ["FurryGame", "",
                  "Правила игры",
                  "Шарики туда сюда,",
                  "Удачной игры!"]

    text_coord = 50

    for line in intro_text:
        global string_rendered
        string_rendered = my_font.render(line, 1, (255, 192, 203))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    start_but = Button(width / 2 - 100, height / 2 + 100, 200, 50, 'Начать игру', clear)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        start_but.process()
        pygame.display.flip()


class Button():
    global my_font

    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.fillColors = {
            'normal': '#ffc0cb',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = my_font.render(buttonText, True, (20, 20, 20))

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                    return True
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


def clear():
    global space, pause, score
    for ball in space.shapes:
        if isinstance(ball, pymunk.shapes.Circle):
            space.remove(ball, ball.body)
    pause = False
    score = 0
    pygame.mixer.music.unpause()


# Функция для создания шарика

def create_ball(space, pos, radius):
    global ball_count, sp_coord
    mass = 0.1
    sp_coord = (pos[0], pos[1])
    inertia = pymunk.moment_for_circle(mass, 10, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = pos
    body.time = 0
    shape = pymunk.Circle(body, radius, (0, 0))
    shape.elasticity = 0.4
    shape.friction = 0.5
    space.add(body, shape)
    ball_count += 1
    return shape


def blitRotate(surf, image, pos, originPos, angle):
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    rotated_offset = offset_center_to_pivot.rotate(-angle)

    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    surf.blit(rotated_image, rotated_image_rect)


# Функция для удаления шаров и создания нового
def update_ball(arbiter, space, data):
    global ball_count, score, win_sound, bounce_soun
    if isinstance(arbiter.shapes[0], pymunk.Circle) and isinstance(arbiter.shapes[1], pymunk.Circle):
        shape = arbiter.shapes[0]
        shape2 = arbiter.shapes[1]
        if shape.radius == max(radius) and shape2.radius == max(radius):
            space.remove(shape, shape.body)
            space.remove(shape2, shape2.body)
            score += 4
            win_sound.play()
            return True
        if shape.radius == shape2.radius and shape.radius != max(radius):
            space.remove(shape, shape.body)
            space.remove(shape2, shape2.body)
            ball_count -= 2
            create_ball(space, (shape2.body.position.x, shape2.body.position.y), round(shape.radius * 1.5))
            ball_count += 1
            if shape.radius >= 45:
                score += 3
            else:
                score += 1
            return True
        # if shape.body.position.y > 100 and shape2.body.position.y > 100:
        #     bounce_sound.play()
    return True


def main():
    global radius, ball_count, screen, width, height, animation_timer, \
        score, my_font, pause

    pygame.init()
    width, height = 400, 600
    screen = pygame.display.set_mode((width, height))
    pygame.font.init()
    start_screen()
    game_fon = pygame.image.load('furry/fon_game.png')
    pygame.mixer.music.load("sounds/background_music.mp3")
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
    pygame.mixer.music.set_volume(0.1)
    global win_sound, bounce_sound
    win_sound = pygame.mixer.Sound('sounds/win_sound.wav')
    # bounce_sound = pygame.mixer.Sound('sounds/bounce.wav')
    # bounce_sound.set_volume(0.1)
    win_sound.set_volume(0.1)
    FPS = 0
    clock = pygame.time.Clock()
    but1 = Button(width / 2 - 100, height / 2 + 100, 200, 50, 'Начать заново', clear)

    space.gravity = (0, 500)
    radius = [20, 30, 45, 68, 102, 153]

    skin = 'base_skin'
    base_skin = {20: 'imgs/ball1.png', 30: 'imgs/ball2.png', 45: 'imgs/ball3.png', 68: 'imgs/ball4.png',
                 102: 'imgs/ball5.png',
                 153: 'imgs/ball6.png'}
    furry_skin = {20: 'furry/fur1.png', 30: 'furry/fur2.png', 45: 'furry/fur3.png', 68: 'furry/fur4.png',
                  102: 'furry/fur5.png',
                  153: 'furry/fur6.png'}

    # Обработка столкновения шаров
    space.collision_handler = space.add_collision_handler(0, 0)
    space.collision_handler.begin = update_ball

    # Создание краев окна
    static_lines = [
        pymunk.Segment(space.static_body, (0, height - 1), (width, height - 1), 5.0),
        pymunk.Segment(space.static_body, (1, 1), (1, height), 0.0),
        pymunk.Segment(space.static_body, (width - 1, 1), (width - 1, height), 0.0), ]

    # Добовление краев окна
    for l in static_lines:
        l.friction = 0.5
    space.add(*static_lines)

    random_rad = min(radius)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    skin = c_skin(skin, 1)
                elif event.key == pygame.K_LEFT:
                    skin = c_skin(skin, -1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Создание шарика при нажатии кнопки мыши
                if FPS >= 50:
                    create_ball(space, (event.pos[0], 0 + random_rad), random_rad)
                    random_rad = random.choice(radius[:3])
                    FPS = 0
        FPS += 3

        screen.fill('white')
        # screen.blit(game_fon, (0, 0))

        # Отрисовка изображения на шарике
        for ball in space.shapes:
            if isinstance(ball, pymunk.shapes.Circle):
                if ball.body.position.y < 100:
                    ball.body.time += 1
                    if ball.body.time > 100:
                        pause = True

                w = h = ball.radius * 2
                image = load_image(ball.radius, locals().get(skin)[ball.radius])
                blitRotate(screen, image, ball.body.position, (w / 2, h / 2), -ball.body.angle * 180 / math.pi)

        # Отрисовка шара сверху
        if ball_count == 0 or ball.body.position.y > 200:
            x = pygame.mouse.get_pos()[0] - random_rad
            pygame.draw.line(screen, 'black', (pygame.mouse.get_pos()[0], 10), (pygame.mouse.get_pos()[0], height), 2)
            screen.blit(load_image(random_rad, locals().get(skin)[random_rad]), (x, 0))

        # Обновление физики
        space.step(1 / 50.0)

        # Отрисовка краев окна
        pygame.draw.line(screen, 'black', (0, height - 1), (width, height - 1), 5)
        pygame.draw.line(screen, 'black', (1, 1), (1, height), 5)
        pygame.draw.line(screen, 'black', (width - 1, 1), (width - 1, height), 5)
        pygame.draw.line(screen, 'red', (0, 100), (width, 100), 5)

        text_surface = my_font.render(str(score), False, (0, 0, 0))
        screen.blit(text_surface, (20, 20))

        if pause:
            lose_text = my_font.render('Ты проиграл!', False, (0, 0, 0))
            score_text = my_font.render(f'У тебя {score} очков.', False, (0, 0, 0))
            text_rects = [lose_text.get_rect(center=(width / 2, height / 2)),
                          score_text.get_rect(center=(width / 2, (height / 2) + 40))]
            pygame.mixer.music.pause()

            while pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    screen.blit(lose_text, text_rects[0])
                    screen.blit(score_text, text_rects[1])
                    but1.process()
                    pygame.display.flip()

        pygame.display.flip()
        clock.tick(50)


if __name__ == '__main__':
    main()
