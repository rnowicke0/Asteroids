import pygame
import random
from cshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        score_count = 0
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        random_num = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_asteroid1 = Asteroid(self.position[0], self.position[1], new_radius)
        new_asteroid2 = Asteroid(self.position[0], self.position[1], (new_radius - ASTEROID_MIN_RADIUS))
        new_asteroid1.velocity = pygame.math.Vector2.rotate(self.velocity, random_num) * 1.2
        new_asteroid2.velocity = pygame.math.Vector2.rotate(self.velocity, -random_num) * 1.2
        score_count += 1
