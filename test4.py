import math
import os
import random
import sys

import pygame
import pymunk
import pymunk.pygame_util


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
    text = my_font.render('Watermelon game', False, (0, 0, 0))
    start_but = Button(width / 2 - 100, height / 2 + 100, 200, 50, 'Начать игру', clear)
    fon = pygame.transform.scale(pygame.image.load('imgs/fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    text_coord = 50
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        start_but.process()
        screen.blit(text, (75, 50))
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
            'normal': '#ffffff',
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
            pymunk.Space.remove(space, ball.body)
            pymunk.Space.remove(space, ball)
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
def remove_ball(arbiter, space, data):
    global ball_count, animation_timer, animation_speed, animation_frames, animation_index, score, win_sound
    if isinstance(arbiter.shapes[0], pymunk.Circle) and isinstance(arbiter.shapes[1], pymunk.Circle):
        shape = arbiter.shapes[0]
        shape2 = arbiter.shapes[1]
        if shape.radius == max(radius) and shape2.radius == max(radius):
            space.remove(shape, shape.body)
            space.remove(shape2, shape2.body)
            score += 4
            win_sound.play()
        if shape.radius == shape2.radius and shape.radius != max(radius):
            space.remove(shape, shape.body)
            space.remove(shape2, shape2.body)
            ball_count -= 2
            create_ball(space, (shape2.body.position.x, shape2.body.position.y), shape.radius + 10)
            ball_count += 1
            if shape.radius >= 45:
                score += 3
            else:
                score += 1
            # for i in range(1000):
            #     animation_timer += animation_speed
            #     if animation_timer >= 1:
            #         animation_timer -= 1
            #         animation_index = (animation_index + 1) % len(animation_frames)
            #     current_frame = animation_frames[animation_index]
            #     screen.blit(current_frame, shape.body.position)
            #     pygame.display.flip()
    return True


def main():
    global radius, ball_count, screen, width, height, animation_timer, animation_speed, animation_frames, animation_index, score, my_font, pause
    pygame.init()
    width, height = 400, 600
    screen = pygame.display.set_mode((width, height))
    pygame.font.init()
    start_screen()
    pygame.mixer.music.load("sounds/background_music.mp3")
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
    pygame.mixer.music.set_volume(0.1)
    global win_sound
    win_sound = pygame.mixer.Sound('sounds/win_sound.wav')
    win_sound.set_volume(0.1)
    clock = pygame.time.Clock()
    but1 = Button(width / 2 - 100, height / 2 + 100, 200, 50, 'Начать заново', clear)

    # animation_frames = []
    # animation_folder = 'gifs'
    # for i in range(1, 10):
    #     frame_path = os.path.join(animation_folder, f'{i}.png')
    #     frame_image = pygame.image.load(frame_path)
    #     animation_frames.append(frame_image)
    #
    # animation_index = 0
    # animation_speed = 0.1
    # animation_timer = 0

    space.gravity = (0, 500)
    radius = [25, 35, 45, 55, 65, 75]
    dic = {25: 'imgs/ball1.png', 35: 'imgs/ball2.png', 45: 'imgs/ball3.png', 55: 'imgs/ball4.png', 65: 'imgs/ball5.png',
           75: 'imgs/ball6.png'}

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
        # animation_timer += animation_speed
        # if animation_timer >= 1:
        #     animation_timer -= 1
        #     animation_index = (animation_index + 1) % len(animation_frames)

        # current_frame = animation_frames[animation_index]
        # screen.blit(current_frame, (100, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Создание шарика при нажатии кнопки мыши
                create_ball(space, (event.pos[0], 0 + random_rad), random_rad)
                random_rad = random.choice(radius[:3])

        screen.fill('white')

        # Отрисовка изображения на шарике
        for ball in space.shapes:
            if isinstance(ball, pymunk.shapes.Circle):
                if ball.body.position.y < 100:
                    ball.body.time += 1
                    if ball.body.time > 100:
                        pause = True
                w = h = ball.radius * 2
                image = load_image(ball.radius, dic[ball.radius])
                blitRotate(screen, image, ball.body.position, (w / 2, h / 2), -ball.body.angle * 180 / math.pi)

        # Отрисовка шара сверху
        if ball_count == 0 or ball.body.position.y > 200:
            x = pygame.mouse.get_pos()[0] - random_rad
            pygame.draw.line(screen, 'black', (pygame.mouse.get_pos()[0], 10), (pygame.mouse.get_pos()[0], height), 2)
            screen.blit(load_image(random_rad, dic[random_rad]), (x, 0))

        # Обновление физики
        space.step(1 / 50.0)

        # Отрисовка краев окна
        pygame.draw.line(screen, 'black', (0, height - 1), (width, height - 1), 5)
        pygame.draw.line(screen, 'black', (1, 1), (1, height), 5)
        pygame.draw.line(screen, 'black', (width - 1, 1), (width - 1, height), 5)
        pygame.draw.line(screen, 'red', (0, 100), (width, 100), 5)

        # Обработка столкновения шаров
        space.collision_handler = space.add_collision_handler(0, 0)
        space.collision_handler.begin = remove_ball
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
