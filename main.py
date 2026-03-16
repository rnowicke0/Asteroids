import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCORE_BOARD_WIDTH, SCORE_BOARD_HEIGHT
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event
from cshape import CircleShape
import sys
from shot import Shot

# to run: uv run main.py in terminal


def main():
    print("Starting Asteroids with pygame version:", pygame.version.ver)
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    # trying to add a scoreboard to keep track of player score
    font = pygame.font.SysFont('Arial', 20)
    text_box_rect = pygame.Rect(SCREEN_WIDTH / 2 - (SCORE_BOARD_WIDTH / 2), 0, SCORE_BOARD_WIDTH, SCORE_BOARD_HEIGHT)
    score_board = pygame.Rect(SCREEN_WIDTH / 2 - (SCORE_BOARD_WIDTH / 2), 0, SCORE_BOARD_WIDTH, SCORE_BOARD_HEIGHT)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, drawable, updatable)

    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    score_count = 0

    running = True
    while running:
        log_state()

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print(f"Game over!")
                print(f"Your score was: {score_count}")
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    score_count += 1

        screen.fill("black")

        pygame.draw.rect(screen, "white", score_board)
        pygame.draw.rect(screen, "black", text_box_rect, 2)

        current_text = f"Score: {score_count}"
        text_surface = font.render(current_text, True, "black")
        text_rect = text_surface.get_rect(center=text_box_rect.center)
        screen.blit(text_surface, text_rect)
        
        for object in drawable:
            object.draw(screen)
        
        pygame.display.flip()


if __name__ == "__main__":
    main()
