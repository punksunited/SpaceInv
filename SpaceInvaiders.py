import pygame
import random
import sys

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

# Groups
player = Player()
player_group = pygame.sprite.GroupSingle(player)

player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

enemies = pygame.sprite.Group()

# Create enemies
def create_enemies(rows, cols):
    for row in range(rows):
        for col in range(cols):
            enemy = Enemy(50 + col * 60, 50 + row * 40)
            enemies.add(enemy)

create_enemies(3, 8)

# Game variables
enemy_speed = 1
enemy_direction = 1
fire_timer = 0
fire_interval = random.randint(1000, 3000)  # Random interval between shots

# Main game loop
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = Bullet(player.rect.centerx, player.rect.top, RED, -7)
            player_bullets.add(bullet)

    # Update player
    player_group.update(keys)

    # Update bullets
    player_bullets.update()
    enemy_bullets.update()

    # Move enemies
    move_down = False
    for enemy in enemies:
        enemy.rect.x += enemy_speed * enemy_direction
        if enemy.rect.right >= SCREEN_WIDTH or enemy.rect.left <= 0:
            move_down = True

    if move_down:
        enemy_direction *= -1
        for enemy in enemies:
            enemy.rect.y += 20
        enemy_speed += 0.2

    # Enemy shooting
    fire_timer += clock.get_time()
    if fire_timer > fire_interval:
        fire_timer = 0
        fire_interval = random.randint(1000, 3000)
        if enemies:
            shooting_enemy = random.choice(enemies.sprites())
            bullet = Bullet(shooting_enemy.rect.centerx, shooting_enemy.rect.bottom, YELLOW, 5)
            enemy_bullets.add(bullet)

    # Check collisions
    for bullet in player_bullets:
        hit = pygame.sprite.spritecollideany(bullet, enemies)
        if hit:
            hit.kill()
            bullet.kill()

    if pygame.sprite.spritecollideany(player, enemy_bullets):
        print("Game Over")
        running = False

    # Draw everything
    screen.fill(BLACK)
    player_group.draw(screen)
    player_bullets.draw(screen)
    enemy_bullets.draw(screen)
    enemies.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
