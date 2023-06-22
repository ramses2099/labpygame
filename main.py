import pygame
import random

TITLE = "TEST GAME"
WINDOW_SIZE = (1280, 720)
FPS = 60
BLACK = (0, 0, 0)
RED = (255, 30, 70)
BLUE = (10, 20, 200)
GREEN = (50, 230, 40)
WHITE = (255, 255, 255)


class Entity:
    def __init__(self, x, y, mass, color):
        self.location = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.size = (25, 25)
        self.color = color
        self.rect = pygame.rect.Rect((x, y), self.size)
        self.mass = mass

    def apply_force(self, force):
        self.acceleration.x = force.x
        self.acceleration.y = force.y

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self, dt):
        self.velocity.x += self.acceleration.x / self.mass
        self.velocity.y += self.acceleration.y / self.mass
        # po
        self.location.x += self.velocity.x * dt
        self.location.y += self.velocity.y * dt

        self.rect.x = int(self.location.x)
        self.rect.y = int(self.location.y)

        self.acceleration.x *= 0
        self.acceleration.y *= 0

        # bounds
        if self.rect.right + self.rect.w > WINDOW_SIZE[0] or self.rect.left - self.rect.w < 0:
            self.velocity.x *= -1
        if self.rect.bottom + self.rect.h > WINDOW_SIZE[1] or self.rect.top - self.rect.h < 0:
            self.velocity.y *= -1


class Box:
    def __init__(self, x, y, mass, color):
        self.image = pygame.Surface((25, 25))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        # physics
        self.location = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.mass = mass

    def apply_force(self, force):
        self.acceleration.x = force.x
        self.acceleration.y = force.y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(surface, WHITE, (self.rect.x, self.rect.y, 26, 26), 2)

    def update(self, dt):
        self.velocity.x += self.acceleration.x / self.mass
        self.velocity.y += self.acceleration.y / self.mass
        # po
        self.location.x += self.velocity.x * dt
        self.location.y += self.velocity.y * dt

        self.rect.x = int(self.location.x)
        self.rect.y = int(self.location.y)

        self.acceleration.x *= 0
        self.acceleration.y *= 0

        # bounds
        if self.rect.right + self.rect.w > WINDOW_SIZE[0] or self.rect.left - self.rect.w < 0:
            self.velocity.x *= -1
        if self.rect.bottom + self.rect.h > WINDOW_SIZE[1] or self.rect.top - self.rect.h < 0:
            self.velocity.y *= -1


class Test(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((25, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((50, 50))
        # self.image.fill(RED)
        pygame.draw.circle(self.image, BLUE, (self.image.get_width()//2, self.image.get_height()//2), 25)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class App:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0.0
        # test objes
        self.entities = []
        self.numberofentity = 20

        self.box = Box(25, 35, 100, RED)
        self.box.apply_force(pygame.math.Vector2(1, 9))
        self.entities.append(self.box)
        # self.init_entities()
        self.test = Test(252, 250)
        self.circle = Circle(300, 25)
        self.group = pygame.sprite.Group()
        self.group.add(self.test, self.circle)

    def collition_rect(self):
        for i in range(len(self.entities)):
            rect1 = self.entities[i]
            for j in range((i + 1), len(self.entities)):
                rect2 = self.entities[j]
                if pygame.Rect.colliderect(rect1.rect, rect2.rect):
                    rect2.velocity.x *= -1
                    rect1.velocity.y *= -1

    def init_entities(self):
        for i in range(self.numberofentity):
            x = random.randint(25, WINDOW_SIZE[0])
            y = random.randint(25, WINDOW_SIZE[1])
            mass = random.randint(1, 10)
            color = self.random_color()
            f1 = random.randint(1, 3)
            f2 = random.randint(5, 9)
            f = pygame.math.Vector2(f1, f2)
            e = Entity(x, y, mass, color)
            e.apply_force(f)
            self.entities.append(e)

    def random_color(self) -> tuple[int, int, int]:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)

    def run(self):
        while self.running:
            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(FPS) * .001 * FPS
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill(BLACK)

            # RENDER YOUR GAME HERE
            for entity in self.entities:
                entity.update(self.dt)
                entity.draw(self.screen)

            # collision
            self.collition_rect()

            # group sprite
            self.group.draw(self.screen)

            # flip() the display to put your work on screen
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    App().run()
