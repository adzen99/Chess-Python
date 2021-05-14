class ChessGame:
    def __init__(self):
        self.__board = [
            ["blackRook", "blackKnight", "blackBishop", "blackQueen", "blackKing", "blackBishop", "blackKnight", "blackRook"],
            ["blackPawn", "blackPawn", "blackPawn", "blackPawn", "blackPawn", "blackPawn", "blackPawn", "blackPawn"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["whitePawn", "whitePawn", "whitePawn", "whitePawn", "whitePawn", "whitePawn", "whitePawn", "whitePawn"],
            ["whiteRook", "whiteKnight", "whiteBishop", "whiteQueen", "whiteKing", "whiteBishop", "whiteKnight", "whiteRook"]
        ]
        self.__whiteTurn = True
        self.__movesLog = []
        self.__blackKingLocation = (0, 4)  # the initial location of the black king
        self.__whiteKingLocation = (7, 4)  # the initial location of the white king
        self.__checkmate = False
        self.__stalemate = False
        self.__capturedPieces = []  # the list of all captured pieces
        # the initial status of all possible castlings
        self.__castlingRules = {"whiteKingSide": True, "whiteQueenSide": True, "blackKingSide": True, "blackQueenSide": True}

    def swapTurn(self):
        self.__whiteTurn = not self.__whiteTurn

    def setPiece(self, i, j, other):
        self.__board[i][j] = other

    def getWhiteKingLocation(self):
        return self.__whiteKingLocation

    def getBlackKingLocation(self):
        return self.__blackKingLocation

    def getMovesLog(self):
        return self.__movesLog

    def getCapturedPieces(self):
        return self.__capturedPieces

    def getBoard(self):
        return self.__board

    def getWhiteTurn(self):
        return self.__whiteTurn

    def getCheckmate(self):
        return self.__checkmate

    def swapCheckmate(self):
        self.__checkmate = not self.__checkmate

    def getStalemate(self):
        return self.__stalemate

    def swapStalemate(self):
        self.__stalemate = not self.__stalemate

    def setTimer(self, other):
        self.__timer = other
    """
    undo the last move that has been made
    """
    def undoMove(self):
        if len(self.__movesLog) != 0:  # if there are moves that has been made
            move = self.__movesLog.pop()
            self.__board[move.getStartRow()][move.getStartCol()] = move.getPieceMoved()
            self.__board[move.getEndRow()][move.getEndCol()] = move.getPieceCaptured()
            self.__whiteTurn = not self.__whiteTurn
            # keep tracking of both kings' positions
            if move.getPieceMoved() == "whiteKing":
                self.__whiteKingLocation = (move.getStartRow(), move.getStartCol())
                if move.getEndCol() - move.getStartCol() == 2:  # white king-side castling undo
                    self.__board[7][7] = "whiteRook"
                    self.__board[7][5] = " "
                    self.__castlingRules["whiteKingSide"] = True
                elif move.getStartCol() - move.getEndCol() == 2:  # white queen-side castling undo
                    self.__board[7][0] = "whiteRook"
                    self.__board[7][3] = " "
                    self.__castlingRules["whiteQueenSide"] = True
            elif move.getPieceMoved() == "blackKing":
                self.__blackKingLocation = (move.getStartRow(), move.getStartCol())
                if move.getEndCol() - move.getStartCol() == 2:  # black king-side castling undo
                    self.__board[0][7] = "whiteRook"
                    self.__board[0][5] = " "
                    self.__castlingRules["blackKingSide"] = True
                elif move.getStartCol() - move.getEndCol() == 2:  # black queen-side castling undo
                    self.__board[0][0] = "whiteRook"
                    self.__board[0][3] = " "
                    self.__castlingRules["blackQueenSide"] = True

    """
    return all the possible moves for all the pieces on the board
    """
    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.__board)):
            for col in range(len(self.__board[row])):
                #  generate all the possible moves for every piece
                piece = self.__board[row][col]
                if piece != " ":
                    piece = piece[5:]
                    if piece == "Pawn":
                        self.pawnMoves(row, col, moves)  # all pawn moves
                    elif piece == "Bishop":
                        self.bishopMoves(row, col, moves)  # all bishop moves
                    elif piece == "Knight":
                        self.knightMoves(row, col, moves)  # all knight moves
                    elif piece == "Rook":
                        self.rookMoves(row, col, moves)  # all rook moves
                    elif piece == "Queen":
                        self.queenMoves(row, col, moves)  # all queen moves
                    elif piece == "King":
                        self.kingMoves(row, col, moves)  # all king moves
        return moves
    """
    determine if the piece located at (row, col) is under attack
    """
    def pieceUnderAttack(self, row, col):
        moves = self.getAllPossibleMoves()
        for move in moves:  # search through all moves for a possible attack
            if move.getEndRow() == row and move.getEndCol() == col:
                return True
        return False
    """
    determine if the king is in check
    """
    def isCheck(self):
        if self.__whiteTurn:  # determine if the white king is under attack
            return self.pieceUnderAttack(self.__whiteKingLocation[0], self.__whiteKingLocation[1])
        else:  # determine if the black king is under attack
            return self.pieceUnderAttack(self.__blackKingLocation[0], self.__blackKingLocation[1])
    """
    return all the valid moves for all the pieces on the board
    """
    def getAllValidMoves(self):
        validMoves = self.getAllPossibleMoves()
        # determine all the castling moves for both kings (if they are valid)
        if self.__whiteTurn:
            self.castlingMoves(7, 4, validMoves)
        else:
            self.castlingMoves(0, 4, validMoves)
        for i in range(len(validMoves) - 1, -1, -1):  # search through all possible moves
            self.makeMove(validMoves[i])  # make a move
            self.__whiteTurn = not self.__whiteTurn  # change turn
            if self.isCheck():  # determine if after a move the king is attacked
                validMoves.remove(validMoves[i])  # if king is under attack, remove the move
            self.undoMove()  # undo the last move that has been made
            self.__whiteTurn = not self.__whiteTurn
        return validMoves
    """
    determine if there is a checkmate or a stalemate
    """
    def checkmateStalemate(self):
        validMoves = self.getAllValidMoves()
        movesAvailable = False  # assume that there are still available moves to make
        if self.__whiteTurn:
            for move in validMoves:
                if self.__board[move.getStartRow()][move.getStartCol()].find("white") != -1:  # if there is at least one, the game continue
                    movesAvailable = True
                    break
        else:
            for move in validMoves:
                if self.__board[move.getStartRow()][move.getStartCol()].find("black") != -1:  # if there is at least one, the game continue
                    movesAvailable = True
                    break
        if not movesAvailable:
            if self.isCheck():  # if there are no moves available and the king is under attack, it is checkmate
                self.__checkmate = True
            else:
                self.__stalemate = True  # otherwise, it is a draw, a stalemate

    """
    determine if the left enemy pawn can be captured using "en passant" move
    """
    def validLeftEnemyPawnForEnPassant(self, row, col, color):
        for move in self.__movesLog:
            if move.getPieceMoved().find(color + "Pawn") != -1:
                if move.getStartRow() == 1:
                    if move.getEndRow() - move.getStartRow() == 2:
                        if col - 1 >= 0 and row == 3 and self.__board[row][col - 1] == color + "Pawn":
                            return True
                elif move.getStartRow() == 6:
                    if move.getStartRow() - move.getEndRow() == 2:
                        if col - 1 >= 0 and row == 4 and self.__board[row][col - 1] == color + "Pawn":
                            return True
        return False

    """
    determine if the right enemy pawn can be captured using "en passant" move
    """
    def validRightEnemyPawnForEnPassant(self, row, col, color):
        for move in self.__movesLog:
            if move.getPieceMoved().find(color + "Pawn") != -1:
                if move.getStartRow() == 1:
                    if move.getEndRow() - move.getStartRow() == 2:
                        if col + 1 < 8 and row == 3 and self.__board[row][col + 1] == color + "Pawn":
                            return True
                elif move.getStartRow() == 6:
                    if move.getStartRow() - move.getEndRow() == 2:
                        if col + 1 < 8 and row == 4 and self.__board[row][col + 1] == color + "Pawn":
                            return True
        return False

    """
    determine "en passant" moves of a pawn (if there are) 
    """
    def enPassantMove(self, row, col, moves):
        if self.__board[row][col].find("white") != -1:
            if col - 1 >= 0 and self.validLeftEnemyPawnForEnPassant(row, col, "black"):
                moves.append(Move((row, col), (row - 1, col - 1), self.__board))
            if col + 1 < 8 and self.validRightEnemyPawnForEnPassant(row, col, "black"):
                moves.append(Move((row, col), (row - 1, col + 1), self.__board))
        elif self.__board[row][col].find("black") != -1:
            if col - 1 >= 0 and self.validLeftEnemyPawnForEnPassant(row, col, "white"):
                moves.append(Move((row, col), (row + 1, col - 1), self.__board))
            if col + 1 < 8 and self.validRightEnemyPawnForEnPassant(row, col, "white"):
                moves.append(Move((row, col), (row + 1, col + 1), self.__board))

    """
    determine all the pawn's moves
    """
    def pawnMoves(self, row, col, moves):
        if self.__board[row][col].find("white") != -1:  # all the possible moves for a white pawn
            if row - 1 >= 0 and self.__board[row - 1][col] == " ":  # 1 square move forward for a white pawn
                moves.append(Move((row, col), (row - 1, col), self.__board))
            if row == 6 and self.__board[row - 2][col] == " ":  # 2 squares move forward for a white pawn
                moves.append(Move((row, col), (row - 2, col), self.__board))
            # the two possible attacks for a white pawn
            if row - 1 >= 0 and col - 1 >= 0 and self.__board[row - 1][col - 1].find("black") != -1:  # left diagonal possible capture
                moves.append(Move((row, col), (row - 1, col - 1), self.__board))
            if row - 1 >= 0 and col + 1 < 8 and self.__board[row - 1][col + 1].find("black") != -1:  # right diagonal possible capture
                moves.append(Move((row, col), (row - 1, col + 1), self.__board))
        elif self.__board[row][col].find("black") != -1:  # all the possible moves for a black pawn
            if row + 1 < 8 and self.__board[row + 1][col] == " ":  # 1 square move forward for a black pawn
                moves.append(Move((row, col), (row + 1, col), self.__board))
            if row == 1 and self.__board[row + 2][col] == " ":  # 2 squares move forward for a black pawn
                moves.append(Move((row, col), (row + 2, col), self.__board))
            # the two possible attacks for a black pawn
            if row + 1 < 8 and col - 1 >= 0 and self.__board[row + 1][col - 1].find("white") != -1:  # left diagonal possible capture
                moves.append(Move((row, col), (row + 1, col - 1), self.__board))
            if row + 1 < 8 and col + 1 < 8 and self.__board[row + 1][col + 1].find("white") != -1:  # right diagonal possible capture
                moves.append(Move((row, col), (row + 1, col + 1), self.__board))
        self.enPassantMove(row, col, moves)  # "en passant" possible moves

    """
    get the position of a pawn that could be promoted after a certain move
    """
    def getPawnPromotionPosition(self):
        for i in range(8):
            if self.__board[0][i] == "whitePawn":
                return 0, i  # white pawn promotion
            if self.__board[7][i] == "blackPawn":
                return 7, i  # black pawn promotion
        return -1, -1

    """
    determine all the bishops's moves
    """
    def bishopMoves(self, row, col, moves):
        # all the possible directions for a bishop
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if self.__board[row][col].find("white") != -1:  # determine the enemy color
            color = "black"
        else:
            color = "white"
        for d in directions:
            for x in range(1, 8):  # all the possible positions in a certain direction
                i = row + x * d[0]
                j = col + x * d[1]
                if 0 <= i < 8 and 0 <= j < 8:  # valid position
                    if self.__board[i][j] == " ":  # if there is an empty square
                        moves.append(Move((row, col), (i, j), self.__board))
                    elif self.__board[i][j].find(color) != -1:  # if there is an enemy piece
                        moves.append(Move((row, col), (i, j), self.__board))
                        break
                    else:
                        break
                else:
                    break
    """
    determine all the knight's moves
    """
    def knightMoves(self, row, col, moves):
        # all the possible directions for a knight
        directions = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2))
        if self.__board[row][col].find("white") != -1:  # determine the enemy color
            color = "black"
        else:
            color = "white"
        for d in directions:
            i = row + d[0]
            j = col + d[1]
            if 0 <= i < 8 and 0 <= j < 8:  # valid postition
                if self.__board[i][j] == " ":  # if there is an empty square
                    moves.append(Move((row, col), (i, j), self.__board))
                elif self.__board[i][j].find(color) != -1:  # if there is an enemy piece
                    moves.append(Move((row, col), (i, j), self.__board))
    """
    determine all the rook's moves
    """
    def rookMoves(self, row, col, moves):
        # all the possible directions for a rook
        directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
        if self.__board[row][col].find("white") != -1:  # determine the enemy color
            color = "black"
        else:
            color = "white"
        for d in directions:
            for x in range(1, 8):  # all the possible moves in a certain direction
                i = row + x * d[0]
                j = col + x * d[1]
                if 0 <= i < 8 and 0 <= j < 8:  # valid position
                    if self.__board[i][j] == " ":  # if there is an empty square
                        moves.append(Move((row, col), (i, j), self.__board))
                    elif self.__board[i][j].find(color) != -1:  # if there is an enemy piece
                        moves.append(Move((row, col), (i, j), self.__board))
                        break
                    else:
                        break
                else:
                    break
    """
    determine all the queen's moves
    """
    def queenMoves(self, row, col, moves):
        # a queen is basically a rook and a bishop combined
        self.bishopMoves(row, col, moves)
        self.rookMoves(row, col, moves)
    """
    determine all the king's moves
    """
    def kingMoves(self, row, col, moves):
        # all the possible moves for a king
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
        if self.__board[row][col].find("white") != -1:  # determine the enemy color
            color = "black"
        else:
            color = "white"
        for d in directions:
            i = row + d[0]
            j = col + d[1]
            if 0 <= i < 8 and 0 <= j < 8:  # valid position
                if self.__board[i][j] == " " or self.__board[i][j].find(color) != -1:  #if there is an empty space or an enemy piece
                    moves.append(Move((row, col), (i, j), self.__board))
    """
    promotion of the pawn
    """
    def pawnPromotion(self, row, col, newPiece):
        if self.__board[row][col] == "whitePawn" and row == 0:
            self.__board[row][col] = newPiece  # promote the white pawn with the new piece
        elif self.__board[row][col] == "blackPawn" and row == 7:
            self.__board[row][col] = newPiece  # promote the black pawn with the new piece
    """
    uptading the castling moves situations depending on a move
    """
    def updateCastlingSituation(self, move):
        if move.getPieceMoved() == "whiteKing":  # if the white king has been moved before
            self.__castlingRules["whiteKingSide"] = False
            self.__castlingRules["whiteQueenSide"] = False
        elif move.getPieceMoved() == "whiteRook":  # if the white rook has been moved before
            if move.getStartRow() == 7 and move.getStartCol() == 7:  # white king-side rook
                self.__castlingRules["whiteKingSide"] = False
            elif move.getStartRow() == 7 and move.getStartCol() == 0:  # white queen-side rook
                self.__castlingRules["whiteQueenSide"] = False
        elif move.getPieceMoved() == "blackKing":  # if the black king has been moved before
            self.__castlingRules["blackKingSide"] = False
            self.__castlingRules["blackQueenSide"] = False
        elif move.getPieceMoved() == "blackRook":  # if the white rook has been moved before
            if move.getStartRow() == 0 and move.getStartCol() == 7:  # black king-side rook
                self.__castlingRules["blackKingSide"] = False
            elif move.getStartRow() == 0 and move.getStartCol() == 0:  # black queen-side rook
                self.__castlingRules["blackQueenSide"] = False
    """
    determine if every position that involes king-side castling is not attacked
    """
    def kingSideNotCheck(self, row, col):
        self.makeMove(Move((row, col), (row, col + 1), self.__board))  # simulate the move towards the king-side rook
        if self.pieceUnderAttack(row, col + 1):  # if that square is under attack
            self.undoMove()
            return False
        self.undoMove()
        self.makeMove(Move((row, col), (row, col + 2), self.__board))  #simulate the move towards the king-side rook
        if self.pieceUnderAttack(row, col + 2):  # if the square is under attack
            self.undoMove()
            return False
        self.undoMove()
        return True
    """
    determine the king-side castling moves
    """
    def kingSideCastling(self, row, col, moves):
        if self.__board[row][col] == "whiteKing":
            if self.__castlingRules["whiteKingSide"]:  # if the white king-side castling rules are ok
                if self.__board[7][5] == " " and self.__board[7][6] == " ":  # if there are all empty squares between the white king and the rook
                    if self.kingSideNotCheck(row, col):  # if the king-side positions are not under attack
                        moves.append(Move((7, 4), (7, 6), self.__board))
        elif self.__board[row][col] == "blackKing":
            if self.__castlingRules["blackKingSide"]:  # if the black king-side castling rules are ok
                if self.__board[0][5] == " " and self.__board[0][6] == " ":  #if there are all empty squares between the black king and the rook
                    if self.kingSideNotCheck(row, col):  # if the king-side positions are not under attack
                        moves.append(Move((0, 4), (0, 6), self.__board))
    """
    determine if every position that involes king-side castling is not attacked
    """
    def queenSideNotCheck(self, row, col):
        self.makeMove(Move((row, col), (row, col - 1), self.__board))  # simulate the move towards the queen-side rook
        if self.pieceUnderAttack(row, col - 1):  # if the square is under attack
            self.undoMove()
            return False
        self.undoMove()
        self.makeMove(Move((row, col), (row, col - 2), self.__board))  # simulate the move towards the queen-side rook
        if self.pieceUnderAttack(row, col - 2):  # if the square is under attack
            self.undoMove()
            return False
        self.undoMove()
        return True
    """
    determine the queen-side castling moves
    """
    def queenSideCastling(self, row, col, moves):
        if self.__board[row][col] == "whiteKing":
            if self.__castlingRules["whiteQueenSide"]:
                if self.__board[7][3] == " " and self.__board[7][2] == " " and self.__board[7][1] == " ":
                    if self.queenSideNotCheck(row, col):
                        moves.append(Move((7, 4), (7, 2), self.__board))
        elif self.__board[row][col] == "blackKing":
            if self.__castlingRules["blackQueenSide"]:
                if self.__board[0][3] == " " and self.__board[0][2] == " " and self.__board[0][1] == " ":
                    if self.queenSideNotCheck(row, col):
                        moves.append(Move((0, 4), (0, 2), self.__board))
    """
    determine the castling moves
    """
    def castlingMoves(self, row, col, moves):
        self.kingSideCastling(row, col, moves)
        self.queenSideCastling(row, col, moves)
    """
    make a move
    """
    def makeMove(self, move):
        self.__board[move.getStartRow()][move.getStartCol()] = " "
        self.__board[move.getEndRow()][move.getEndCol()] = move.getPieceMoved()
        self.__movesLog.append(move)
        self.__whiteTurn = not self.__whiteTurn
        if move.getPieceMoved() == "whiteKing":
            self.__whiteKingLocation = (move.getEndRow(), move.getEndCol())
        elif move.getPieceMoved() == "blackKing":
            self.__blackKingLocation = (move.getEndRow(), move.getEndCol())
    """
    move a piece on the board
    """
    def movePiece(self, move):
        self.__board[move.getStartRow()][move.getStartCol()] = " "
        self.__board[move.getEndRow()][move.getEndCol()] = move.getPieceMoved()
        self.__movesLog.append(move)
        self.__whiteTurn = not self.__whiteTurn
        if move.getPieceMoved() == "whiteKing":
            self.__whiteKingLocation = (move.getEndRow(), move.getEndCol())
            if move.getEndCol() - move.getStartCol() == 2:
                self.__board[7][7], self.__board[7][5] = self.__board[7][5], self.__board[7][7]
            elif move.getStartCol() - move.getEndCol() == 2:
                self.__board[7][0], self.__board[7][3] = self.__board[7][3], self.__board[7][0]
        elif move.getPieceMoved() == "blackKing":
            self.__blackKingLocation = (move.getEndRow(), move.getEndCol())
            if move.getEndCol() - move.getStartCol() == 2:
                self.__board[0][7], self.__board[0][5] = self.__board[0][5], self.__board[0][7]
            elif move.getStartCol() - move.getEndCol() == 2:
                self.__board[0][0], self.__board[0][3] = self.__board[0][3], self.__board[0][0]
        elif move.getPieceMoved() == "whitePawn":
            if move.getStartCol() != move.getEndCol() and move.getPieceCaptured() == " ":
                self.__capturedPieces.append(self.__board[move.getEndRow() + 1][move.getEndCol()])
                self.__board[move.getEndRow() + 1][move.getEndCol()] = " "
        elif move.getPieceMoved() == "blackPawn":
            if move.getStartCol() != move.getEndCol() and move.getPieceCaptured() == " ":
                self.__capturedPieces.append(self.__board[move.getEndRow() - 1][move.getEndCol()])
                self.__board[move.getEndRow() - 1][move.getEndCol()] = " "
        if move.getPieceCaptured() != " ":
            self.__capturedPieces.append(move.getPieceCaptured())
        # keep validating castling possible moves
        self.updateCastlingSituation(move)


class Move:
    def __init__(self, startSquare, endSquare, board):
        self.__startRow = startSquare[0]
        self.__startCol = startSquare[1]
        self.__endRow = endSquare[0]
        self.__endCol = endSquare[1]
        self.__pieceMoved = board[self.__startRow][self.__startCol]
        self.__pieceCaptured = board[self.__endRow][self.__endCol]
        self.__moveID = self.__startRow*1000 + self.__startCol*100 + self.__endRow*10 + self.__endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.__moveID == other.__moveID
        return False

    def __str__(self):
        return '('+str(self.__startRow)+', '+str(self.__startCol)+"), ("+str(self.__endRow)+', '+str(self.__endCol)+')'

    def getStartRow(self):
        return self.__startRow

    def getStartCol(self):
        return self.__startCol

    def getEndRow(self):
        return self.__endRow

    def getEndCol(self):
        return self.__endCol

    def getPieceMoved(self):
        return self.__pieceMoved

    def getPieceCaptured(self):
        return self.__pieceCaptured
