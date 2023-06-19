import pygame

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
        self.apply_force(pygame.math.Vector2(0, 9))

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
        self.entity = Entity(250, 25, 10.0, WHITE)

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
            self.entity.update(self.dt)
            self.entity.draw(self.screen)

            # flip() the display to put your work on screen
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    App().run()
