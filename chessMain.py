import pygame
from boardLayout import BoardLayout
from chessGame import ChessGame, Move
from button import Button
from tableImage import TableImage
import time

width = height = 512
dimension = 8
squareSize = 64
maxFPS = 15
"""
load images for pieces from the images package
"""
def loadImages(images):
    pieces = ["whitePawn", "whiteRook", "whiteKnight", "whiteBishop", "whiteQueen", "whiteKing",
              "blackPawn", "blackRook", "blackKnight", "blackBishop", "blackQueen", "blackKing"]
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load("images/pieces/" + piece + ".png"), (squareSize, squareSize))

"""
load images for the pieces that has been captured from the images package
"""
def loadImagesCapturedPieces(imagesCapturedPieces):
    pieces = ["whitePawn", "whiteRook", "whiteKnight", "whiteBishop", "whiteQueen", "whiteKing",
              "blackPawn", "blackRook", "blackKnight", "blackBishop", "blackQueen", "blackKing"]
    for piece in pieces:
        imagesCapturedPieces[piece] = pygame.transform.scale(pygame.image.load("images/pieces/" + piece + ".png"), (squareSize // 2, squareSize // 2))

"""
draw chess board
"""
def drawBoard(window, selectedLayout):
    colors = [selectedLayout.getColor1(), selectedLayout.getColor2()]
    for row in range(dimension):
        for col in range(dimension):
            color = colors[((row+col) % 2)]
            pygame.draw.rect(window, color, pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))

"""
draw all the pieces on the board
"""
def drawPieces(window, board, images):
    for row in range(dimension):
        for col in range(dimension):
            piece = board[row][col]
            if piece != " ":
                window.blit(images[piece], pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))

"""
draw the pieces that has been captured
"""
def drawCapturedPieces(window, chess, imagesCapturedPieces):
    xWhite, xBlack = 60, 60
    for piece in chess.getCapturedPieces():
        if piece.find("white") != -1:
            window.blit(imagesCapturedPieces[piece], pygame.Rect(xWhite, 32, 16, 16))
            xWhite += 25
        else:
            window.blit(imagesCapturedPieces[piece], pygame.Rect(xBlack, 576, 16, 16))
            xBlack += 25

"""
highlight all the valid positions for a pieces located at squareSelected
"""
def highlightValidMoves(window, chess, validMoves, squareSelected, selectedLayout):
    if squareSelected != ():  # if the player has selected a square
        row, col = squareSelected
        if (chess.getWhiteTurn() and chess.getBoard()[row][col].find("white") != -1) or\
                (not chess.getWhiteTurn() and chess.getBoard()[row][col].find("black") != -1):
            if chess.getBoard()[row][col] != " ":
                s = pygame.Surface((squareSize, squareSize))
                s.set_alpha(100)
                s.fill(selectedLayout.getHighlightColor1())
                window.blit(s, (col * squareSize + 64, row * squareSize + 64))
                s.fill(selectedLayout.getHighlightColor2())
                for move in validMoves:  # highlight all the possible moves for a piece
                    if move.getStartRow() == row and move.getStartCol() == col:
                        window.blit(s, (squareSize * move.getEndCol() + 64, squareSize * move.getEndRow() + 64))

"""
highlight the last move that has been made
"""
def highlightLastMove(window, chess):
    if len(chess.getMovesLog()) != 0:  # if there is at least one move that has been made
        iStart = chess.getMovesLog()[-1].getStartRow()
        jStart = chess.getMovesLog()[-1].getStartCol()
        iEnd = chess.getMovesLog()[-1].getEndRow()
        jEnd = chess.getMovesLog()[-1].getEndCol()
        s = pygame.Surface((squareSize, squareSize))
        s.set_alpha(75)
        s.fill(pygame.Color("blue"))
        window.blit(s, (jStart * squareSize + 64, iStart * squareSize + 64))
        window.blit(s, (jEnd * squareSize + 64, iEnd * squareSize + 64))

"""
highlight the king if it is in check
"""
def highlightCheck(window, chess):
    if chess.isCheck():
        s = pygame.Surface((squareSize, squareSize))
        s.set_alpha(100)
        s.fill(pygame.Color("red"))
        if chess.getWhiteTurn():
            i, j = chess.getWhiteKingLocation()
            window.blit(s, (j * squareSize + 64, i * squareSize + 64, squareSize, squareSize))
        else:
            i, j = chess.getBlackKingLocation()
            window.blit(s, (j * squareSize + 64, i * squareSize + 64, squareSize, squareSize))

"""
display whose turn is under the board
"""
def displayPlayerTurn(window, chess):
    font = pygame.font.SysFont("comicsansms", 32)
    if chess.getWhiteTurn():
        text = font.render("White's turn!", True, (255, 255, 255))
        if chess.isCheck():
            checkText = font.render("Check!", True, (255, 255, 255))
            window.blit(checkText, (265, 650))
    else:
        text = font.render("Black's turn!", True, (0, 0, 0))
        if chess.isCheck():
            checkText = font.render("Check!", True, (0, 0, 0))
            window.blit(checkText, (265, 650))
    window.blit(text, (224, 610))

"""
draw the pieces to be chosen in a pawn is promoted
"""
def drawPawnPromotionPieces(window, row, col, images):
    if row == 0:
        pygame.draw.rect(window, pygame.Color("white"),
                         pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
        window.blit(images["whiteQueen"],
                    pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
        row += 1
        pygame.draw.rect(window, pygame.Color("white"),
                         pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
        window.blit(images["whiteRook"],
                    pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
        row += 1
        pygame.draw.rect(window, pygame.Color("white"),
                         pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
        window.blit(images["whiteKnight"],
                    pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
        row += 1
        pygame.draw.rect(window, pygame.Color("white"),
                         pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
        window.blit(images["whiteBishop"],
                    pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
    elif row == 7:
        pygame.draw.rect(window, pygame.Color("white"),
                         pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
        window.blit(images["blackQueen"],
                    pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
        row -= 1
        pygame.draw.rect(window, pygame.Color("white"),
                         pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
        window.blit(images["blackRook"],
                    pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
        row -= 1
        pygame.draw.rect(window, pygame.Color("white"),
                         pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
        window.blit(images["blackKnight"],
                    pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
        row -= 1
        pygame.draw.rect(window, pygame.Color("white"),
                         pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
        window.blit(images["blackBishop"],
                    pygame.Rect(col * squareSize + 64, row * squareSize + 64, squareSize, squareSize))
"""
get the selected promoted piece
"""
def getPromotedPieceSelected(row, col):
    pieces = ["whiteQueen", "whiteRook", "whiteKnight", "whiteBishop", "blackBishop", "blackKnight", "blackRook", "blackQueen"]
    location = pygame.mouse.get_pos()
    j = location[0] // squareSize - 1
    i = location[1] // squareSize - 1
    if row == 0:
        pos = [0, 1, 2, 3]
        while j != col and i not in pos:
            location = pygame.mouse.get_pos()
            j = location[0] // squareSize - 1
            i = location[1] // squareSize - 1
        return pieces[i]
    elif row == 7:
        pos = [7, 6, 5, 4]
        while j != col and i not in pos:
            location = pygame.mouse.get_pos()
            j = location[0] // squareSize - 1
            i = location[1] // squareSize - 1
        return pieces[i]

"""
the promotion of a pawn
"""
def pawnPromotion(window, chess, images):
    row, col = chess.getPawnPromotionPosition()
    if row != -1:
        drawPawnPromotionPieces(window, row, col, images)
        piece = getPromotedPieceSelected(row, col)
        chess.setPiece(row, col, piece)
"""
display the end of the game (when it is checkmate or stalemate)
"""
def displayEndgame(window, chess):
    font = pygame.font.SysFont("comicsansms", 32)
    if chess.getStalemate():
        text = font.render("Stalemate! Draw!", True, pygame.Color("gray"))
    elif not chess.getWhiteTurn():
        text = font.render("Checkmate! White won!", True, (255, 255, 255))
    else:
        text = font.render("Checkmate! Black won!", True, (0, 0, 0))
    window.blit(text, (160, 610))
"""
animating a move
"""
def animateMove(window, chess, move, clock, images, selectedLayout):
    colors = [selectedLayout.getColor1(), selectedLayout.getColor2()]
    dRow = move.getEndRow() - move.getStartRow()
    dCol = move.getEndCol() - move.getStartCol()
    framesPerSquare = 2
    frameCount = (abs(dRow) + abs(dCol)) * framesPerSquare
    for frame in range(frameCount + 1):
        row, col = (move.getStartRow() + dRow * frame/frameCount + 1, move.getStartCol() + dCol * frame/frameCount + 1)
        drawBoard(window, selectedLayout)
        drawPieces(window, chess.getBoard(), images)
        # erase the pieces moved from its endSquare
        color = colors[(move.getEndRow() + move.getEndCol()) % 2]
        endSquare = pygame.Rect(move.getEndCol() * squareSize + 64, move.getEndRow() * squareSize + 64, squareSize, squareSize)
        pygame.draw.rect(window, color, endSquare)
        # draw captured piece into rectangle
        if move.getPieceCaptured() != " ":
            window.blit(images[move.getPieceCaptured()], endSquare)
        # draw the moving piece
        window.blit(images[move.getPieceMoved()], pygame.Rect(col * squareSize, row * squareSize, squareSize, squareSize))
        pygame.display.flip()
        clock.tick(60)
"""
draw all the components for the game
"""
def drawChessGame(window, chess, validMoves, squareSelected, images, imagesCapturedPieces, selectedLayout):
    drawBoard(window, selectedLayout)
    highlightValidMoves(window, chess, validMoves, squareSelected, selectedLayout)
    #highlightLastMove(window, chess)
    highlightCheck(window, chess)
    drawPieces(window, chess.getBoard(), images)
    chess.checkmateStalemate()
    if chess.getCheckmate() or chess.getStalemate():
        displayEndgame(window, chess)
    else:
        displayPlayerTurn(window, chess)
    drawCapturedPieces(window, chess, imagesCapturedPieces)
"""
check if the certain positions are on the board
"""
def validPositions(row, col):
    return 0 <= row < 8 and 0 <= col < 8

"""
determine if a certain move is valid or not
"""
def validMove(chess, move):
    return (chess.getWhiteTurn() and move.getPieceMoved().find("white") != -1) or (
                not chess.getWhiteTurn() and move.getPieceMoved().find("black") != -1)

"""
create a timer given a certain number of seconds
"""
def createTimer(timer):
    mins, secs = divmod(timer, 60)
    timeFormat = '{:02d}:{:02d}'.format(mins, secs)
    return timeFormat

"""
display the timer for white player
"""
def displayWhiteTimer(window, whiteTimer):
    whiteTimerFormat = createTimer(whiteTimer)
    font = pygame.font.SysFont("comicsansms", 32)
    txt = font.render(whiteTimerFormat, True, pygame.Color("white"))
    window.blit(txt, (500, 576))

"""
display the timer for black player
"""
def displayBlackTimer(window, blackTimer):
    blackTimerFormat = createTimer(blackTimer)
    font = pygame.font.SysFont("comicsansms", 32)
    txt = font.render(blackTimerFormat, True, pygame.Color("black"))
    window.blit(txt, (500, 20))

"""
main game loop
"""
def gameLoop(window, selectedLayout, undo, selectedTableImage, selectedTimerMinutes):
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()
    chess = ChessGame()
    images = {}
    loadImages(images)  # load the images for all the pieces
    tableImage = pygame.transform.scale(pygame.image.load("images/tables/table" + selectedTableImage.getN() + ".jpg").convert(), (512 + 128, 512 + 128 + 64))
    imagesCapturedPieces = {}
    loadImagesCapturedPieces(imagesCapturedPieces)
    squareSelected = ()
    clicks = []
    validMoves = []
    moveMade = False
    undoMade = False
    undoButton = Button(100, 100, 580, (64 + 64 * 8) // 2 + 16, "Undo", pygame.Color("green"), 20)
    whiteTimer = blackTimer = selectedTimerMinutes * 60  # transform the minutes selected into seconds
    run = True
    checkSound = pygame.mixer.Sound("sounds/check.wav")
    checkmateSound = pygame.mixer.Sound("sounds/checkmate.wav")
    stalemateSound = pygame.mixer.Sound("sounds/stalemate.wav")
    while run:
        window.blit(tableImage, (0, 0))
        if selectedTimerMinutes != 0:
            displayWhiteTimer(window, whiteTimer)  # display the white's timer
            displayBlackTimer(window, blackTimer)  # display the black's timer
        if undo:
            undoButton.displayButton(window)
            undoMade = False
        for e in pygame.event.get():
            position = pygame.mouse.get_pos()  # get the current position of the mouse
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                col = position[0] // squareSize - 1
                row = position[1] // squareSize - 1
                validMoves = chess.getAllValidMoves()
                if squareSelected == (row, col):  # if the same square has been selected
                    squareSelected = ()
                    clicks = []
                elif validPositions(row, col):  # if the position that has been selected is a valid one
                    squareSelected = (row, col)
                    clicks.append(squareSelected)
                if len(clicks) == 2:  # if 2 squares had been selected
                    move = Move(clicks[0], clicks[1], chess.getBoard())
                    if move in validMoves and validMove(chess, move):  # if a move is valid
                        chess.movePiece(move)
                        moveMade = True
                        pygame.mixer.music.load("sounds/piece_move.mp3")
                        pygame.mixer.music.play()
                        pawnPromotion(window, chess, images)
                    squareSelected = ()
                    clicks = []
                if undo and undoButton.mouseOverButton(position):  # if the undo functionality has been selected
                    moveMade = False
                    undoMade = True
                    chess.undoMove()
                    if chess.getCheckmate():
                        chess.swapCheckmate()
                    if chess.getStalemate():
                        chess.swapStalemate()
                if not undoMade:
                    if chess.getCheckmate():
                        checkmateSound.play()  # play a sound if it is checkmate
                    elif chess.getStalemate():
                        stalemateSound.play()  # play a sound if it is stalemate
                    elif chess.isCheck():
                        checkSound.play()  # play a sound if it is check
            elif e.type == pygame.MOUSEMOTION:
                undoButton.animateUndoButton(position, 20)  # highlight the undo button at mouse motion event
        if moveMade:  # if a move has been made
            animateMove(window, chess, chess.getMovesLog()[-1], clock, images, selectedLayout)  # animate the last move made
            moveMade = False
        if selectedTimerMinutes != 0:  # if the game has a timer
            if len(chess.getMovesLog()) != 0:
                if chess.getWhiteTurn() and whiteTimer:  # decreasing white's timer
                    time.sleep(1)
                    whiteTimer -= 1
                elif not chess.getWhiteTurn() and blackTimer:  # decreasing black's timer
                    time.sleep(1)
                    blackTimer -= 1
        clock.tick(maxFPS)
        # draw all the components of the game
        drawChessGame(window, chess, validMoves, squareSelected, images, imagesCapturedPieces, selectedLayout)
        pygame.display.flip()


