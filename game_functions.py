import pygame
import random
from game_entities import Player, Enemy, BlueEnemy, SpecialEnemy, Bullet, PowerUp, SCREEN_WIDTH, SCREEN_HEIGHT


def initialize_game():
    from game_entities import Player, Enemy, BlueEnemy, SpecialEnemy  # Import BlueEnemy and SpecialEnemy
    player = Player()
    enemies = [Enemy() for _ in range(5)]
    blue_enemies = [BlueEnemy() for _ in range(2)]  # Create instances of BlueEnemy
    special_enemies = [SpecialEnemy()]  # Create an instance of SpecialEnemy

    bullets = []
    power_ups = []
    special_enemies = []
    game_info = {
        "bullets": bullets,
        "score": 0,
        "special_enemy_active": False,
        "next_special_enemy_score": 2,
        "last_power_up_time": pygame.time.get_ticks(),  # Initialize last power-up spawn time
        "power_up_spawn_interval": 10000  # 10 seconds between spawns
    }
    enemies.extend(blue_enemies)  # Add BlueEnemies to the enemies list
    special_enemies.extend(special_enemies)  # Add SpecialEnemies to the special_enemies list

    return player, enemies, bullets, power_ups, special_enemies, game_info

def handle_events(player, bullets, game_info):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Check for auto-fire condition inside the key press event
                if not (player.has_power_up() and player.power_up_type == "auto_fire"):
                    new_bullets = player.shoot()
                    bullets.extend(new_bullets)
    return True


def spawn_power_ups(power_ups, game_info, current_time):
    # Check if enough time has passed since the last power-up spawn
    if current_time - game_info['last_power_up_time'] > game_info['power_up_spawn_interval']:
        if random.randint(1, 100) <= 20:  # 20% chance to spawn a power-up
            type = random.choice(["auto_fire", "multi_direction"])  # Randomly choose type
            power_ups.append(PowerUp(type))
            game_info['last_power_up_time'] = current_time  # Reset the spawn timer


def check_power_up_collisions(player, power_ups):
    for power_up in power_ups[:]:  # Copy list for safe removal
        if player.get_hitbox().colliderect(power_up.get_hitbox()):
            player.activate_power_up(power_up.type, power_up.duration)
            power_ups.remove(power_up)
            print(f"Activated power-up: {power_up.type}")



def update_game(player, enemies, bullets, power_ups, special_enemies, game_info):
    # Check for player input and update player position
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move("left")
    if keys[pygame.K_RIGHT]:
        player.move("right")
    if keys[pygame.K_UP]:
        player.move("up")
    if keys[pygame.K_DOWN]:
        player.move("down")

    # Update all bullets
    for bullet in bullets[:]:  # Use a slice copy for safe removal during iteration
        bullet.move()
        if bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
            bullets.remove(bullet)
        else:
            if bullet.source == 'player':
                # Check bullet collisions with all types of enemies
                for enemy in enemies[:] + special_enemies[:]:
                    if bullet.get_hitbox().colliderect(enemy.get_hitbox()):
                        if enemy.hit():
                            if enemy in enemies:
                                enemies.remove(enemy)
                                game_info['score'] += 1
                            elif enemy in special_enemies:
                                special_enemies.remove(enemy)
                                game_info['score'] += 5
                        bullets.remove(bullet)
                        break

            elif bullet.source == 'enemy':
                # Check bullet collisions with player
                if bullet.get_hitbox().colliderect(player.get_hitbox()):
                    if player.hit():
                        print("Player hit! Remaining lives: ", player.lives)
                        if player.lives <= 0:
                            print("Game Over!")
                            return False  # Exit the game loop if the player is dead
                    bullets.remove(bullet)

    # Update all enemies and special enemies
    for enemy in enemies:
        enemy.move()
        if enemy.get_hitbox().colliderect(player.get_hitbox()):
            if player.hit():
                if player.lives <= 0:
                    print("Game Over!")
                    return False  # Exit the game loop if the player is dead

    for enemy in special_enemies:
        enemy.move()
        # Special enemies might shoot at intervals
        if random.randint(0, 100) < 2:  # 5% chance per frame to shoot
            bullets.append(enemy.shoot(player.x))

        if enemy.get_hitbox().colliderect(player.get_hitbox()):
            if player.hit():
                if player.lives <= 0:
                    print("Game Over!")
                    return False  # Exit the game loop if the player is dead

    # Update power-ups and check for collection
    for power_up in power_ups[:]:
        if power_up.get_hitbox().colliderect(player.get_hitbox()):
            player.activate_power_up(power_up.type, power_up.duration)
            power_ups.remove(power_up)
            print(f"Power-up {power_up.type} activated!")

    # Handle power-up effects expiration
    if player.has_power_up() and not player.has_power_up():
        print(f"Power-up {player.power_up_type} expired!")
        player.power_up_type = None  # Reset power-up type

    # Check game-over conditions
    if player.lives <= 0:
        print("Game Over!")
        return False  # Stop the game loop if the player is out of lives

    # Check if all enemies are destroyed
    if not enemies and not special_enemies:
        print("All enemies destroyed! Respawning...")
        # Respawn enemies and special enemies
        for _ in range(3):
            enemies.append(Enemy())
        for _ in range(2):
            special_enemies.append(SpecialEnemy())

    return True  # Continue the game loop




def render_game(screen, player, enemies, bullets, power_ups, special_enemies, score_font, health_font, game_info):
    screen.fill((0, 0, 0))  # Clear screen
    # Draw all game objects
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for power_up in power_ups:
        power_up.draw(screen)
    for special_enemy in special_enemies:
        special_enemy.draw(screen)

    # Draw UI elements like score and health
    health_text = health_font.render(f'Health: {player.lives}', True, (255, 255, 255))
    score_text = score_font.render(f'Score: {game_info["score"]}', True, (255, 255, 255))
    screen.blit(health_text, (SCREEN_WIDTH - health_text.get_width() - 10, 10))
    screen.blit(score_text, (10, 10))

    pygame.display.update()  # Update the display

