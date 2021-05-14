import pygame

class Button:
    def __init__(self, width, height, x, y, text, textColor, textSize):
        self.__width = width
        self.__height = height
        self.__x = x
        self.__y = y
        self.__text = text
        self.__textColor = textColor
        self.__textSize = textSize

    def setTextSize(self, other):
        self.__textSize = other

    def getTextSize(self):
        return self.__textSize

    def getText(self):
        return self.__text

    """
    determine if the mouse is over a certain button
    """
    def mouseOverButton(self, position):
        return self.__x < position[0] < self.__x + self.__width and self.__y < position[1] < self.__y + self.__height

    """
    display a button on the screen
    """
    def displayButton(self, window):
        font = pygame.font.SysFont("comicsansms", self.__textSize)
        text = font.render(self.__text, True, self.__textColor)
        window.blit(text, (self.__x, self.__y))

    """
    animate a button if the mouse is over it
    """
    def animateButton(self, position, initialTextSize):
        if self.mouseOverButton(position):
            self.__textSize = 80
        else:
            self.__textSize = initialTextSize

    """
    animate the undo button
    """
    def animateUndoButton(self, position, initialTextSize):
        if self.mouseOverButton(position):
            self.__textSize = 25
        else:
            self.__textSize = initialTextSize
    """
    highlight a button if it is selected
    """
    def highlightButton(self, window):
        pygame.draw.line(window, (255, 0, 0), (self.__x, self.__y), (self.__x + self.__width, self.__y))
        pygame.draw.line(window, (255, 0, 0), (self.__x, self.__y), (self.__x, self.__y + self.__height))
        pygame.draw.line(window, (255, 0, 0), (self.__x + self.__width, self.__y), (self.__x + self.__width, self.__y + self.__height))
        pygame.draw.line(window, (255, 0, 0), (self.__x, self.__y + self.__height), (self.__x + self.__width, self.__y + self.__height))

