import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("./background-2.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80
PLAYER_VEL = 5

STAR_WIDTH = 70
STAR_HEIGHT = 70
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)

player_image = pygame.image.load('rocket-2-removed.png')
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

star_image = pygame.image.load("stone-removebg-preview.png")
star_image = pygame.transform.scale(star_image, (STAR_WIDTH, STAR_HEIGHT))

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    WIN.blit(player_image, player.topleft)

    for star in stars:
        WIN.blit(star_image, (star.x, star.y))  # Blit star image at star's position

    pygame.display.update()

def start_screen():
    run = True
    while run:
        WIN.fill((0, 0, 0))  # Fill screen with black

        title_text = FONT.render("Space Dodge", 1, "white")
        control_text = FONT.render("Controls:", 1, "white")
        up_text = FONT.render("Up: Move Up", 1, "white")
        down_text = FONT.render("Down: Move Down", 1, "white")
        left_text = FONT.render("Left: Move Left", 1, "white")
        right_text = FONT.render("Right: Move Right", 1, "white")
        win_condition_text = FONT.render("Survive more than 40 seconds to win!", 1, "white")
        start_text = FONT.render("Press any key to start", 1, "white")

        WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, 100))
        WIN.blit(control_text, (100, 250))
        WIN.blit(up_text, (150, 300))
        WIN.blit(down_text, (150, 350))
        WIN.blit(left_text, (150, 400))
        WIN.blit(right_text, (150, 450))
        WIN.blit(win_condition_text, (WIDTH/2 - win_condition_text.get_width()/2, 550))
        WIN.blit(start_text, (WIDTH/2 - start_text.get_width()/2, 700))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                run = False
                break
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

def main():
    start_screen()  # Show the start screen before starting the game

    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + player.height <= HEIGHT:
            player.y += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        if elapsed_time > 40:
            win_text = FONT.render("You Won!", 1, "white")
            WIN.blit(win_text, (WIDTH/2 - win_text.get_width()/2, HEIGHT/2 - win_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()
