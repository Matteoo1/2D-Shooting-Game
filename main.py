
import pygame
from game_entities import Player, Enemy, Bullet, PowerUp
from game_functions import initialize_game, handle_events, update_game, render_game


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("2D Shoot 'em up")

        # Initialize fonts
    score_font = pygame.font.SysFont('Arial', 24)
    health_font = pygame.font.SysFont('Arial', 20)

    player, enemies, bullets, power_ups, special_enemies, game_info = initialize_game()

    clock = pygame.time.Clock()
    
    running = True
    while running:
        clock.tick(60)
        running = handle_events(player, bullets, game_info)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or (player.has_power_up() and player.power_up_type == "auto_fire"):
            bullets.extend(player.shoot(auto_fire=True))
        if not update_game(player, enemies, bullets, power_ups, special_enemies, game_info):
            print("Exiting game loop due to game over.")
            break
        render_game(screen, player, enemies, bullets, power_ups, special_enemies, score_font, health_font, game_info)

    pygame.quit()

if __name__ == "__main__":
    main()
