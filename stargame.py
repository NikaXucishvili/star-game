import pygame
import time
import random


WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("./background-2.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80

player_image = pygame.image.load('rocket-2-removed.png').convert_alpha()
player_image.set_colorkey((55, 155, 100))


player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))




def draw(player):
    WIN.blit(BG, (0, 0))

    WIN.blit(player_image, player.topleft)

    pygame.display.update()


def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(player)

    pygame.quit()

if __name__ == "__main__":
    main()
