import pygame
from menu import menuLoop

width = 512 + 128
height = 512 + 128 + 64

"""
the main function
"""
def main():
    pygame.init()
    window = pygame.display.set_mode((width, height))
    menuLoop(window)


if __name__ == "__main__":
    main()
