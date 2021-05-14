import pygame

class TableImage:
    def __init__(self, x, y, width, height, n):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__n = n
        self.__tableImage = pygame.transform.scale(pygame.image.load("images/tables/table" + n + ".jpg").convert(), (self.__width, self.__height))

    def getN(self):
        return self.__n

    def displayTableImage(self, window):
        window.blit(self.__tableImage, (self.__x, self.__y))

    def mouseOverTableImage(self, position):
        return self.__x < position[0] < self.__x + self.__width and self.__y < position[1] < self.__y + self.__height

    def highlightTableImage(self, window):
        pygame.draw.line(window, (255, 0, 0), (self.__x, self.__y), (self.__x + self.__width, self.__y))
        pygame.draw.line(window, (255, 0, 0), (self.__x, self.__y), (self.__x, self.__y + self.__height))
        pygame.draw.line(window, (255, 0, 0), (self.__x + self.__width, self.__y), (self.__x + self.__width, self.__y + self.__height))
        pygame.draw.line(window, (255, 0, 0), (self.__x, self.__y + self.__height), (self.__x + self.__width, self.__y + self.__height))