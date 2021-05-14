import pygame
from button import Button
from boardLayout import BoardLayout
from chessMain import gameLoop
from tableImage import TableImage

width = 512 + 128
height = 512 + 128 + 64

"""
display the back arror
"""
def displayBackArrow(window, backArrow):
    window.blit(backArrow, (10, 10))

"""
determine if the mouse is over the back arrow
"""
def mouseOverBackArrow(position):
    return 10 < position[0] < 10 + 64 and 10 < position[1] < 10 + 64

"""
display some text on the screen
"""
def displayText(window, text, x, y, textSize, color):
    font = pygame.font.SysFont("comicsansms", textSize)
    txt = font.render(text, True, color)
    window.blit(txt, (x, y))

"""
create some layouts for the board
"""
def createLayouts():
    x = 160
    y = 30
    layout1 = BoardLayout(pygame.Color("white"), pygame.Color("gray"), x, y, pygame.Color("blue"), pygame.Color("yellow"))
    x += 80
    layout2 = BoardLayout((255, 204, 204), (255, 80, 80), x, y, pygame.Color("black"), pygame.Color("blue"))
    x += 80
    layout3 = BoardLayout((153, 230, 153), (41, 163, 41), x, y, pygame.Color("black"), pygame.Color("blue"))
    x += 80
    layout4 = BoardLayout((204, 224, 255), (77, 148, 255), x, y, pygame.Color("black"), pygame.Color("purple"))
    x += 80
    layout5 = BoardLayout((255, 204, 179), (255, 102, 26), x, y, pygame.Color("black"), pygame.Color("brown"))
    x += 80
    layout6 = BoardLayout((255, 179, 236), (255, 51, 204), x, y, pygame.Color("black"), pygame.Color("green"))
    x = 160
    y += 80
    layout7 = BoardLayout((255, 255, 102), (153, 153, 0), x, y, pygame.Color("black"), pygame.Color("green"))
    x += 80
    layout8 = BoardLayout((204, 153, 255), (115, 0, 230), x, y, pygame.Color("black"), pygame.Color("white"))
    x += 80
    layouts = [layout1, layout2, layout3, layout4, layout5, layout6, layout7, layout8]
    return layouts

"""
display all the layouts for the board
"""
def displayLayouts(window, layouts):
    displayText(window, "Layouts:", 20, 75, 32, pygame.Color("yellow"))
    for layout in layouts:
        layout.displayLayout(window)

def loadTableImages():
    tableImages = []
    x, y = 140, 300
    w = h = 100
    table1 = TableImage(x, y, w, h, "1")
    tableImages.append(table1)
    x += 120
    table2 = TableImage(x, y, w, h, "2")
    tableImages.append(table2)
    x += 120
    table3 = TableImage(x, y, w, h, "3")
    tableImages.append(table3)
    return tableImages

"""
display the tables on the screen
"""
def displayTables(window, tableImages):
    displayText(window, "Tables:", 20, 325, 32, pygame.Color("yellow"))
    for image in tableImages:
        image.displayTableImage(window)

"""
display timers on the screen
"""
def displayTimers(window, button1, button2, button3, button4):
    displayText(window, "Timer:", 20, 425, 32, pygame.Color("yellow"))
    button1.displayButton(window)
    button2.displayButton(window)
    button3.displayButton(window)
    button4.displayButton(window)

"""
create a list composed of all timers
"""
def createTimers():
    timers = []
    noTimeButton = Button(150, 50, 125, 425, "Unlimited", pygame.Color("yellow"), 32)
    timers.append(noTimeButton)
    timeButton3mins = Button(100, 50, 125, 475, "3 mins", pygame.Color("yellow"), 32)
    timers.append(timeButton3mins)
    timeButton10mins = Button(120, 50, 125, 525, "10 mins", pygame.Color("yellow"), 32)
    timers.append(timeButton10mins)
    timeButton30mins = Button(120, 50, 125, 575, "30 mins", pygame.Color("yellow"), 32)
    timers.append(timeButton30mins)
    return timers

"""
options loop
"""
def optionsLoop(window, backgroundImage):
    pygame.display.set_caption("Options")
    backArrow = pygame.transform.scale(pygame.image.load("images/options/backArrow.png").convert(), (64, 64))
    layouts = createLayouts()
    selectedLayout = layouts[0]  # default board layout (white and gray)
    undo = False
    undoButton = Button(75, 50, 20, 200, "Undo", pygame.Color("yellow"), 32)
    noUndoButton = Button(130, 50, 120, 200, "No Undo", pygame.Color("yellow"), 32)
    tableImages = loadTableImages()
    selectedTableImage = tableImages[0]
    timers = createTimers()
    selectedTimer = timers[0]
    run = True
    while run:
        window.blit(backgroundImage, (0, 0))
        displayBackArrow(window, backArrow)
        displayLayouts(window, layouts)
        undoButton.displayButton(window)
        noUndoButton.displayButton(window)
        selectedLayout.highlightLayout(window)
        if undo:
            undoButton.highlightButton(window)
        else:
            noUndoButton.highlightButton(window)
        displayTables(window, tableImages)
        selectedTableImage.highlightTableImage(window)
        displayTimers(window, timers[0], timers[1], timers[2], timers[3])
        selectedTimer.highlightButton(window)
        for e in pygame.event.get():
            position = pygame.mouse.get_pos()
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if mouseOverBackArrow(position):  # if the back arrow is pressed
                    run = False
                for layout in layouts:
                    if layout.mouseOverLayout(position):
                        selectedLayout = layout
                        break
                for image in tableImages:
                    if image.mouseOverTableImage(position):
                        selectedTableImage = image
                        break
                for i in range(len(timers)):
                    if timers[i].mouseOverButton(position):
                        selectedTimer = timers[i]
                        break
                if undoButton.mouseOverButton(position):
                    undo = True
                elif noUndoButton.mouseOverButton(position):
                    undo = False
            elif e.type == pygame.MOUSEMOTION:
                pass
        pygame.display.flip()
    pygame.display.set_caption("Chess menu")
    return selectedLayout, undo, selectedTableImage, selectedTimer

"""
return the selected number of minutes for the timer
"""
def getSelectedTimerMinutes(selectedTimer):
    if selectedTimer.getText().find("3") != -1:
        return 3
    elif selectedTimer.getText().find("10") != -1:
        return 10
    elif selectedTimer.getText().find("30") != -1:
        return 30
    else:
        return 0

"""
main menu loop
"""
def menuLoop(window):
    pygame.display.set_caption("Chess menu")
    selectedLayout = BoardLayout(pygame.Color("white"), pygame.Color("gray"), 160, 30, pygame.Color("blue"), pygame.Color("yellow"))
    selectedTableImage = TableImage(140, 300, 100, 100, "1")
    selectedTimer = Button(150, 50, 125, 425, "Unlimited", pygame.Color("yellow"), 32)
    selectedTimerMinutes = getSelectedTimerMinutes(selectedTimer)
    undo = False
    backgroundImage = pygame.transform.scale(pygame.image.load("images/menu/background.jpg").convert(), (width, height))
    run = True
    playButton = Button(200, 100, width // 2 - 50, height // 3 + 50, "Play", pygame.Color("red"), 48)
    optionsButton = Button(200, 100, width // 2 - 85, height // 3 + 150, "Options", pygame.Color("red"), 48)
    quitButton = Button(200, 100, width // 2 - 50, height // 3 + 250, "Quit", pygame.Color("red"), 48)
    playButtonInitialSize = playButton.getTextSize()
    buttonInitialSize = optionsButton.getTextSize()
    while run:
        window.blit(backgroundImage, (0, 0))
        displayText(window, "CHESS", 180, 50, 100, pygame.Color("green"))
        playButton.displayButton(window)
        optionsButton.displayButton(window)
        quitButton.displayButton(window)
        position = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if playButton.mouseOverButton(position):
                    gameLoop(window, selectedLayout, undo, selectedTableImage, selectedTimerMinutes)
                elif optionsButton.mouseOverButton(position):
                    selectedLayout, undo, selectedTableImage, selectedTimer = optionsLoop(window, backgroundImage)
                    selectedTimerMinutes = getSelectedTimerMinutes(selectedTimer)
                elif quitButton.mouseOverButton(position):
                    run = False
            elif e.type == pygame.MOUSEMOTION:
                playButton.animateButton(position, playButtonInitialSize)
                optionsButton.animateButton(position, buttonInitialSize)
                quitButton.animateButton(position, buttonInitialSize)
        pygame.display.flip()
