import pygame
import time
import random

pygame.font.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 768

# Initialize the display window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

# Load background images
bg_image = pygame.image.load("bg.png").convert_alpha()
BG = pygame.transform.scale(pygame.image.load("sky.jpg"), (WIDTH, HEIGHT))
STARTBG = pygame.transform.scale(pygame.image.load("bg.png"), (WIDTH, HEIGHT))

# Player settings
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80
PLAYER_VEL = 5

# Star settings
STAR_WIDTH = 70
STAR_HEIGHT = 70
STAR_VEL = 3

# Font settings
FONT = pygame.font.SysFont("comicsans", 30)

# Load player image
player_image = pygame.image.load('rocket-2-removed.png')
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Load star image
star_image = pygame.image.load("stone-removebg-preview.png")
star_image = pygame.transform.scale(star_image, (STAR_WIDTH, STAR_HEIGHT))

pygame.mixer.init()
pygame.mixer.music.load('music.mp3')

# Play the music indefinitely (-1 means loop indefinitely)
pygame.mixer.music.play(-1)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, (255, 255, 255))
    WIN.blit(time_text, (10, 10))

    WIN.blit(player_image, player.topleft)

    for star in stars:
        WIN.blit(star_image, (star.x, star.y))  # Blit star image at star's position

    pygame.display.update()

def start_screen():
    run = True
    title_font = pygame.font.SysFont("comicsans", 80)
    control_font = pygame.font.SysFont("comicsans", 40)
    instruction_font = pygame.font.SysFont("comicsans", 30)

    title_text = title_font.render("Space Dodge", 1, (255, 255, 255))
    control_text = control_font.render("Controls:", 1, (255, 255, 255))
    up_text = instruction_font.render("Up: Move Up", 1, (255, 255, 255))
    down_text = instruction_font.render("Down: Move Down", 1, (255, 255, 255))
    left_text = instruction_font.render("Left: Move Left", 1, (255, 255, 255))
    right_text = instruction_font.render("Right: Move Right", 1, (255, 255, 255))
    start_text = instruction_font.render("Press any key to start", 1, (255, 255, 255))

    title_text_rect = title_text.get_rect(center=(WIDTH // 2, 150))
    control_text_rect = control_text.get_rect(topleft=(100, 250))
    up_text_rect = up_text.get_rect(topleft=(150, 300))
    down_text_rect = down_text.get_rect(topleft=(150, 350))
    left_text_rect = left_text.get_rect(topleft=(150, 400))
    right_text_rect = right_text.get_rect(topleft=(150, 450))
    start_text_rect = start_text.get_rect(center=(WIDTH // 2, 700))

    anim_count = 0
    anim_speed = 60

    while run:
        WIN.blit(STARTBG, (0, 0))

        # Blinking effect for "Press any key to start"
        if anim_count < anim_speed // 2:
            WIN.blit(start_text, start_text_rect)
        if anim_count >= anim_speed // 2:
            anim_count = 0
        anim_count += 1

        WIN.blit(title_text, title_text_rect)
        WIN.blit(control_text, control_text_rect)
        WIN.blit(up_text, up_text_rect)
        WIN.blit(down_text, down_text_rect)
        WIN.blit(left_text, left_text_rect)
        WIN.blit(right_text, right_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                countdown_timer()  # Start countdown on any key press
                return
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.time.delay(30)

def countdown_timer():
    countdown_font = pygame.font.SysFont("comicsans", 100, bold=True)
    countdown_texts = [countdown_font.render("Get Ready!", 1, (255, 255, 255)),
                       countdown_font.render("3", 1, (255, 255, 255)),
                       countdown_font.render("2", 1, (255, 255, 255)),
                       countdown_font.render("1", 1, (255, 255, 255))]

    countdown_rects = [text.get_rect(center=(WIDTH // 2, HEIGHT // 2)) for text in countdown_texts]

    for i, text in enumerate(countdown_texts):
        WIN.blit(STARTBG, (0, 0))  # Clear screen
        WIN.blit(text, countdown_rects[i])
        pygame.display.update()
        if i < len(countdown_texts) - 1:
            pygame.time.delay(1000)  # Wait 1 second between countdown steps

def restart_game():
    global player, start_time, elapsed_time, stars, star_count, star_add_increment, hit

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False

    pygame.mixer.music.play(-1)

def main():
    start_screen()  # Show the start screen before starting the game

    global player, start_time, elapsed_time, stars, star_count, star_add_increment, hit

    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False
    game_over = False

    while run:
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart_game()
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        run = False
                        break
                elif event.type == pygame.QUIT:
                    run = False
                    break
        else:
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
                    game_over = True
                    break

            if hit:
                lost_text = FONT.render("You Lost! Press R to Restart or ESC to Quit", 1, (255, 255, 255))
                WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(2000)

            if elapsed_time > 40:
                win_text = FONT.render("You Won! Press R to Restart or ESC to Quit", 1, (255, 255, 255))
                WIN.blit(win_text, (WIDTH/2 - win_text.get_width()/2, HEIGHT/2 - win_text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(2000)

            draw(player, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()
