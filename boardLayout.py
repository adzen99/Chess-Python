import pygame

class BoardLayout:
    def __init__(self, color1, color2, x, y, highlightColor1, highlightColor2):
        self.__color1 = color1
        self.__color2 = color2
        self.__x = x
        self.__y = y
        self.__highlightColor1 = highlightColor1
        self.__highlightColor2 = highlightColor2

    def getColor1(self):
        return self.__color1

    def getColor2(self):
        return self.__color2

    def getHighlightColor1(self):
        return self.__highlightColor1

    def getHighlightColor2(self):
        return self.__highlightColor2

    """
    display a layout on the screen
    """
    def displayLayout(self, window):
        colors = [self.__color1, self.__color2]
        for row in range(2):
            for col in range(2):
                color = colors[((row + col) % 2)]
                pygame.draw.rect(window, color, pygame.Rect(col * 32 + self.__x, row * 32 + self.__y, 32, 32))

    """
    determine if the mouse is over a certain layout
    """
    def mouseOverLayout(self, position):
        return self.__x < position[0] < self.__x + 64 and self.__y < position[1] < self.__y + 64

    """
    highlight the selected layout
    """
    def highlightLayout(self, window):
        pygame.draw.line(window, (255, 0, 0), (self.__x, self.__y), (self.__x + 64, self.__y))
        pygame.draw.line(window, (255, 0, 0), (self.__x, self.__y), (self.__x, self.__y + 64))
        pygame.draw.line(window, (255, 0, 0), (self.__x + 64, self.__y), (self.__x + 64, self.__y + 64))
        pygame.draw.line(window, (255, 0, 0), (self.__x, self.__y + 64), (self.__x + 64, self.__y + 64))