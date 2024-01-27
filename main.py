import pygame
import random

all_sprites = pygame.sprite.Group()


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y=20, r=None):
        super().__init__(all_sprites)
        self.lst_radius = [30, 40, 50, 60, 70, 80]
        self.y_motion = False
        self.x_motion = True
        if not r:
            self.radius = random.choice(self.lst_radius[:3])
        else:
            print(r)
            print(self.lst_radius.index(r))
            self.radius = self.lst_radius[self.lst_radius.index(r) + 1]
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (self.radius, self.radius), self.radius)
        self.rect = pygame.Rect(x, y, 2 * self.radius, 2 * self.radius)

    # asd
    def unification(self, ball1, ball2):
        ball = Ball((ball2.rect.x + ball1.rect.x) / 2, ball2.rect.y - ball2.radius // 2, ball1.radius)
        ball.y_motion = True
        ball1.kill()
        ball2.kill()

    def update(self):
        if self.y_motion:
            self.rect.y += 3
        if pygame.sprite.spritecollide(self, all_sprites, False):
            lst = pygame.sprite.spritecollide(self, all_sprites, False)
            for i in lst:
                if pygame.sprite.collide_circle(self, i) and i != self:
                    if self.radius == i.radius:
                        self.unification(self, i)
                    self.y_motion = False


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


if __name__ == '__main__':
    pygame.init()
    balls = []
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    running = True
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 10)
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    mouse_ball = Ball(pygame.mouse.get_pos()[0])
    balls.append(mouse_ball)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION and mouse_ball.x_motion == True:
                mouse_ball.rect.x = event.pos[0] - mouse_ball.radius
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_ball.y_motion = True
                mouse_ball.x_motion = False
            if event.type == MYEVENTTYPE:
                screen.fill((255, 255, 255))
                all_sprites.update()
                all_sprites.draw(screen)
            if mouse_ball.rect.y > 200:
                mouse_ball = Ball(pygame.mouse.get_pos()[0])
                balls.append(mouse_ball)

        pygame.display.flip()