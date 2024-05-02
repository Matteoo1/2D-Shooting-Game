import pygame
import random

# Constants for screen dimensions and colors
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_COLOR = (0, 255, 0)  # Green color for the player
ENEMY_COLOR = (255, 0, 0)   # Red color for the enemy
BULLET_COLOR = (255, 255, 255)  # White color for bullets
AUTO_FIRE_INTERVAL = 50  # Time interval (ms) between automatic shots

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 30
        self.width = 30
        self.height = 30
        self.velocity = 5
        self.lives = 3
        self.power_up_type = None
        self.power_up_start_time = 0
        self.power_up_duration = 0
        self.last_shot_time = 0
        self.last_hit_time = 0
        self.hit_cooldown = 1000

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.velocity
        elif direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.velocity
        elif direction == "up" and self.y > 0:
            self.y -= self.velocity
        elif direction == "down" and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.velocity

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, (self.x, self.y, self.width, self.height))

    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def activate_power_up(self, power_up_type, duration):
        self.power_up_type = power_up_type
        self.power_up_duration = duration
        self.power_up_start_time = pygame.time.get_ticks()

    def has_power_up(self):
        if self.power_up_type and pygame.time.get_ticks() - self.power_up_start_time < self.power_up_duration:
            return True
        else:
            self.power_up_type = None
            return False

    def shoot(self, auto_fire=False):
        current_time = pygame.time.get_ticks()
        if (auto_fire or (self.has_power_up() and self.power_up_type == "auto_fire")) and (current_time - self.last_shot_time > AUTO_FIRE_INTERVAL):
            self.last_shot_time = current_time
            return [Bullet(self.x + self.width // 2 - 2.5, self.y)]
        return []

    def hit(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.hit_cooldown:
            self.lives -= 1
            self.last_hit_time = current_time
            if self.lives <= 0:
                print("Player died!")  
                return True
            return False
        return False

class Enemy:
    def __init__(self):
        self.width = 30  # Define width before calling reset_position()
        self.height = 30  # Define height before calling reset_position()
        self.reset_position()
        self.velocity = random.randint(1, 3)  # Set velocity
        self.health = 3  # Add a health attribute with an initial value


    def reset_position(self):
        # Now self.width is defined, so this should work without error
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(-150, -30)  # This places the enemy off-screen initially

    def move(self):
        self.y += self.velocity
        if self.y > SCREEN_HEIGHT:
            self.reset_position()

    def draw(self, screen):
        pygame.draw.rect(screen, ENEMY_COLOR, (self.x, self.y, self.width, self.height))

    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def hit(self):
        self.health -= 1  # Decrement health when hit
        if self.health <= 0:
            return True  # If health is zero or less, return True to indicate the enemy is destroyed
        else:
            return False  # Otherwise, return False


class BlueEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.width = 50
        self.height = 50
        self.velocity = random.randint(1, 2)
        self.health = 3
        self.color = (0, 0, 255)

    def hit(self):
        self.health -= 1
        return self.health <= 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def reset_position(self):
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(-150, -30)
        self.velocity = random.randint(1, 2)

class SpecialEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, SCREEN_WIDTH - 60)
        self.y = 50
        self.width = 60
        self.height = 60
        self.health = 10
        self.color = (255, 165, 0)
        self.velocity = 1
        self.direction = random.choice([-1, 1])

    def move(self):
        self.x += self.velocity * self.direction
        if self.x <= 0 or self.x + self.width >= SCREEN_WIDTH:
            self.direction *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def shoot(self, player_x):
        bullet_velocity = 5
        dx = player_x - (self.x + self.width // 2)
        dy = SCREEN_HEIGHT - self.y
        distance = max(abs(dx), abs(dy))
        bullet_dx = bullet_velocity * dx / distance
        bullet_dy = bullet_velocity * dy / distance
        return Bullet(self.x + self.width // 2, self.y, bullet_dx, bullet_dy, source='enemy')

    def hit(self):
        self.health -= 1
        print(f"SpecialEnemy hit, remaining health: {self.health}")
        return self.health <= 0

class Bullet:
    def __init__(self, x, y, dx=0, dy=-7, source='player'):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = 5
        self.height = 10
        self.source = source

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.rect(screen, BULLET_COLOR, (self.x, self.y, self.width, self.height))

    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class PowerUp:
    def __init__(self, type, duration=5000):
        self.x = random.randint(0, SCREEN_WIDTH - 20)
        self.y = random.randint(0, SCREEN_HEIGHT - 20)
        self.width = 20
        self.height = 20
        self.type = type
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        if self.type == "auto_fire":
            self.color = (255, 255, 0)
        elif self.type == "multi_direction":
            self.color = (0, 255, 255)
        else:
            self.color = (255, 165, 0)  # Default color if type not recognized

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_active(self):
        return pygame.time.get_ticks() - self.start_time < self.duration
