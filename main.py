import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CHARACTER_SIZE = 32
OBSTACLE_SIZE = 32
ENEMY_SIZE = 32
GOAL_SIZE = 32
CHARACTER_SPEED = 5
ENEMY_SPEED = 2

level = 1

def draw_goal(screen, goal):
    pygame.draw.rect(screen, (255, 255, 0), goal)

def draw_level(screen, level):
    font = pygame.font.Font(None, 24)
    text = font.render(f"Level: {level}", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH - text.get_width() - 10, 10))

def draw_objects(screen, character, enemies, obstacles, goal):
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), character)
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), enemy)
    for obstacle in obstacles:
        pygame.draw.rect(screen, (0, 255, 0), obstacle)
    draw_goal(screen, goal)
    draw_level(screen, level)
    pygame.display.flip()

def reset_game_state(level):
    character = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, CHARACTER_SIZE, CHARACTER_SIZE)

    enemies = [pygame.Rect(random.randint(0, SCREEN_WIDTH - ENEMY_SIZE), random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE),
                           ENEMY_SIZE, ENEMY_SIZE) for _ in range(5)]

    obstacles = [pygame.Rect(random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE),
                             random.randint(0, SCREEN_HEIGHT - OBSTACLE_SIZE), OBSTACLE_SIZE, OBSTACLE_SIZE)
                 for _ in range(10 + level * 2)]

    goal = pygame.Rect(random.randint(0, SCREEN_WIDTH - GOAL_SIZE),
                       random.randint(0, SCREEN_HEIGHT - GOAL_SIZE), GOAL_SIZE, GOAL_SIZE)

    return character, enemies, obstacles, goal

def game_over(screen):
    global level
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over! Press R to Restart", True, (0, 0, 0))
    screen.fill((255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    level = 1
                    main()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def main():
    global level
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple Game")

    character, enemies, obstacles, goal = reset_game_state(level)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character.x -= CHARACTER_SPEED
        if keys[pygame.K_RIGHT]:
            character.x += CHARACTER_SPEED
        if keys[pygame.K_UP]:
            character.y -= CHARACTER_SPEED
        if keys[pygame.K_DOWN]:
            character.y += CHARACTER_SPEED

        character.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        if character.colliderect(goal):
            level += 1
            character, enemies, obstacles, goal = reset_game_state(level)
        for enemy in enemies:
            if enemy.colliderect(character):
                game_over(screen)
                keys = pygame.key.get_pressed()
                while not keys[pygame.K_r]:
                    pygame.event.pump()
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        pygame.quit()
                        sys.exit()
                main()

            if enemy.x < character.x:
                enemy.x += ENEMY_SPEED
            elif enemy.x > character.x:
                enemy.x -= ENEMY_SPEED

            if enemy.y < character.y:
                enemy.y += ENEMY_SPEED
            elif enemy.y > character.y:
                enemy.y -= ENEMY_SPEED

            for obstacle in obstacles:
                if enemy.colliderect(obstacle):
                    enemy.x -= ENEMY_SPEED
                    enemy.y -= ENEMY_SPEED

        for obstacle in obstacles:
            if character.colliderect(obstacle):
                character.x -= CHARACTER_SPEED
                character.y -= CHARACTER_SPEED

        draw_objects(screen, character, enemies, obstacles, goal)

        pygame.time.delay(20)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()
