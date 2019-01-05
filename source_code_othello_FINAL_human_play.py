# Othello
# https://inventwithpython.com/chapter15.html

import random
import sys
#import numpy as np
#import matplotlib.pyplot as plt


def drawBoard(board):
    # This function prints out the board that it was passed. Returns None.
    print()
    HLINE = "  +-------+-------+-------+-------+-------+-------+-------+-------+"
    VLINE = "  |       |       |       |       |       |       |       |       |"
    print("      1       2       3       4       5       6       7       8")
    print(HLINE)
    for x in range(8):
        print(VLINE)
        print(x + 1, end=" ")
        for y in range(8):
            print("|   " + board[x][y], end="   ")
        print("|", end=" ")
        print(x + 1)
        print(VLINE)
        print(HLINE)
    print("      1       2       3       4       5       6       7       8")
    print()


def resetBoard(board):
    # Blanks out the board it is passed, except for the original starting position.
    for x in range(8):
        for y in range(8):
            board[x][y] = " "
    # Starting pieces:
    board[3][3] = "X"
    board[3][4] = "O"
    board[4][3] = "O"
    board[4][4] = "X"


def getNewBoard():
    # Creates a brand new, blank board data structure.
    board = []
    for i in range(8):
        board.append([" "] * 8)
    return board


def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player"s move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player"s if they made a move here.
    if board[xstart][ystart] != " " or not isOnBoard(xstart, ystart):
        return False
    board[xstart][ystart] = tile  # temporarily set the tile on the board.
    if tile == "X":
        otherTile = "O"
    else:
        otherTile = "X"
    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection  # first step in the direction
        y += ydirection  # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):  # break out of while loop, then continue in for loop
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])
    board[xstart][ystart] = " "  # restore the empty space
    if len(tilesToFlip) == 0:  # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= 7 and y >= 0 and y <= 7


def getBoardWithValidMoves(board, tile):
    # Returns a new board with . marking the valid moves the given player can make.
    dupeBoard = getBoardCopy(board)
    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = "."
    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys "X" and "O".
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == "X":
                xscore += 1
            if board[x][y] == "O":
                oscore += 1
    return {"X": xscore, "O": oscore}


def enterPlayerTile():
    # Lets the player type which tile they want to be.
    # Returns a list with the player"s tile as the first item, and the computer"s tile as the second.
    tile = ""
    while not (tile == "X" or tile == "O"):
        print("Do you want to be X or O?")
        tile = input().upper()
    # the first element in the list is the player"s tile, the second is the computer"s tile.
    if tile == "X":
        return ["X", "O"]
    else:
        return ["O", "X"]


def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return "computer"
    else:
        return "player"


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print("Do you want to play again? (yes or no)")
    return input().lower().startswith("y")


def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent"s pieces.
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    dupeBoard = getNewBoard()
    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]
    return dupeBoard


def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def getPlayerMove(board, playerTile):
    # Let the player type in their move.
    # Returns the move as [x, y] (or returns the strings "hints" or "quit")
    DIGITS1TO8 = "1 2 3 4 5 6 7 8".split()
    while True:
        print(
            "Enter your move (row number then column number, for example 18 will be the top right corner), or type quit to end the game, or hints to turn off/on hints.\n")
        move = input().lower()
        if move == "quit":
            return "quit"
        if move == "hints":
            return "hints"
        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                print("Invalid move.\n")
                continue
            else:
                break
        else:
            print("To move, type the row digit (1-8), then the column digit (1-8). [row,column]")
            print("For example, 18 will be the top-right corner.")
    return [x, y]


####################################################################################################

# def getPlayerMove(board, playerTile, playerHeuristic, playerTime):
#     # Given a board and the computer"s tile, determine where to
#     # move and return that move as a [x, y] list.
#     possibleMoves = getValidMoves(board, playerTile)
#     # randomize the order of the possible moves
#     random.shuffle(possibleMoves)
#     # always go for a corner if available.
#     for x, y in possibleMoves:
#         if isOnCorner(x, y):
#             return [x, y]
#     # Go through all the possible moves and remember the best scoring move
#     bestScore = -500
#     for x, y in possibleMoves:
#         dupeBoard = getBoardCopy(board)
#         makeMove(dupeBoard, playerTile, x, y)
#         if playerHeuristic == 'greedy':
#             score = getScoreOfBoard(dupeBoard)[playerTile]  # for greedy
#         elif playerHeuristic == 'weighted':
#             score = getWeightedScoreOfBoard(dupeBoard)[playerTile]  # for weighted
#         elif playerHeuristic == 'adaptive':
#             score = getAdaptiveHeuristicScore(dupeBoard, playerTile, "O", len(possibleMoves), playerTime)  # for adaptive
#         else:
#             score = getHybridHeuristicScore(dupeBoard, playerTile, "O", len(possibleMoves), playerTime)
#
#         if score > bestScore:
#             bestMove = [x, y]
#             bestScore = score
#     return bestMove
##################################################################################################


def getWeightedScoreOfBoard(board):
    # Weights
    W = [
        [4, -3, 2, 2, 2, 2, -3, 4],
        [-3, -4, -1, -1, -1, -1, -4, -3],
        [2, -1, 1, 0, 0, 1, -1, 2],
        [2, -1, 0, 1, 1, 0, -1, 2],
        [2, -1, 0, 1, 1, 0, -1, 2],
        [2, -1, 1, 0, 0, 1, -1, 2],
        [-3, -4, -1, -1, -1, -1, -4, -3],
        [4, -3, 2, 2, 2, 2, -3, 4],
    ]
    # Determine the score by counting the tiles. Returns a dictionary with keys "X" and "O" with weight.
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == "X":
                xscore += W[x][y]
            if board[x][y] == "O":
                oscore += W[x][y]
    return {"X": xscore, "O": oscore}


def getNumberOfCorners(board, computerTile):
    score = 0
    if board[0][0] == computerTile:
        score += 1
    if board[0][7] == computerTile:
        score += 1
    if board[7][0] == computerTile:
        score += 1
    if board[7][7] == computerTile:
        score += 1
    return score


def getNumberOfValidMoves(board, tile):
    score = 0
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                score += 1
    return score


def getCoinHeuristicScore(board, computerTile):
    # Number of coins heuristic:
    computer_coin_score = getScoreOfBoard(board)[computerTile]
    return computer_coin_score


def getCornerHeuristicScore(board, computerTile):
    # Number of corners heuristic:
    computer_corner_score = getNumberOfCorners(board, computerTile)
    return computer_corner_score


def getMobilityHeuristicScore(board, playerTile, computer_mobility_score):
    # Number of next moves the opponent has (mobility) heuristic:
    player_mobility_score = getNumberOfValidMoves(board, playerTile)
    return computer_mobility_score - player_mobility_score


def getAdaptiveHeuristicScore(board, computerTile, playerTile, computerMobilityValue, compTime):
    heuristic_score = compTime[0] * getCoinHeuristicScore(board, computerTile) + compTime[1] * getCornerHeuristicScore(
        board, computerTile) + compTime[2] * getMobilityHeuristicScore(board, playerTile, computerMobilityValue)
    return heuristic_score


def getStabilityHeuristicScore(board, playerTile, computerTile):
    computerCoins = getScoreOfBoard(board)[computerTile]
    possibleMoves = getValidMoves(board, playerTile)
    maxDifferent = 0
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, playerTile, x, y)
        howManyDifferent = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] != dupeBoard[i][j]:
                    howManyDifferent += 1
        if howManyDifferent > maxDifferent:
            maxDifferent = howManyDifferent
    staticScore = computerCoins - maxDifferent
    return staticScore


def getAdaptiveHeuristicScoreWithStability(board, computerTile, playerTile, computerMobilityValue, compTime):
    heuristic_score = compTime[0] * getCoinHeuristicScore(board, computerTile) + compTime[1] * getCornerHeuristicScore(
        board, computerTile) + compTime[2] * getMobilityHeuristicScore(board, playerTile, computerMobilityValue) + \
                      compTime[3] * getStabilityHeuristicScore(board, playerTile, computerTile)
    return heuristic_score


def getHybridHeuristicScore(board, computerTile, playerTile, computerMobilityValue, time):
    if countPieces(board) < time[3]:
        return getWeightedScoreOfBoard(board)[computerTile]
    else:
        return getAdaptiveHeuristicScore(board, computerTile, playerTile, computerMobilityValue, time[0:3])


def getHybridHeuristicScoreWithStability(board, computerTile, playerTile, computerMobilityValue, time):
    if countPieces(board) < time[4]:
        return getWeightedScoreOfBoard(board)[computerTile]
    else:
        return getAdaptiveHeuristicScoreWithStability(board, computerTile, playerTile, computerMobilityValue, time[0:4])


def countPieces(board):
    count = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == "X" or board[x][y] == "O":
                count += 1
    return count


#################################################################################################

def getComputerMove(board, computerTile):
    # Given a board and the computer"s tile, determine where to
    # move and return that move as a [x, y] list.

    bestScore = MIN_SCORE
    bestMove = []

    possibleMoves = getValidMoves(board, computerTile)
    # randomize the order of the possible moves
    random.shuffle(possibleMoves)
    # always go for a corner if available.
    # for x, y in possibleMoves:
    #    if isOnCorner(x, y):
    #        return [x, y]
    # Go through all the possible moves and remember the best scoring move
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        # greedy approach:
        # score = getScoreOfBoard(dupeBoard)[computerTile]

        # greedy approach with differents weights on positions:
        # score = getWeightedScoreOfBoard(dupeBoard)[computerTile]

        # adaptive function:
        # score = getAdaptiveHeuristicScore(dupeBoard, computerTile, "X", len(possibleMoves))

        # hybrid between weights and adaptive function:
        # if countPieces(board) < 50:
        #    score = getWeightedScoreOfBoard(dupeBoard)[computerTile]
        # else:
        #    score = getAdaptiveHeuristicScore(dupeBoard, computerTile, "X", len(possibleMoves))

        score = getAdaptiveHeuristicScore(dupeBoard, computerTile, "X", len(possibleMoves), compTime)
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return [bestMove, bestScore]


def showPoints(playerTile, computerTile, mainBoard):
    # Prints out the current score.
    scores = getScoreOfBoard(mainBoard)
    # print("You have %s points. The computer has %s points." % (scores[playerTile], scores[computerTile]))
    print("Current score:")
    print("  Player = %s" % (scores[playerTile]))
    print("Computer = %s" % (scores[computerTile]))
    print()


# computer is moving first and computerTile is O       # playerTile, computerTile = enterPlayerTile()
playerTile, computerTile = ["X", "O"]
MIN_SCORE = -5000
MAX_SCORE = 5000
ComputerMovesEvaluated = 0
PlayerMovesEvaluated = 0


# MIN-MAX-SEARCH
def getMinMaxMove(board, compHeuristic, compTime, depth, abPrune):
    return getMaxMove(board, depth, compHeuristic, compTime, abPrune, a=MIN_SCORE, b=MAX_SCORE, root=True)


# gets max move decision in MIN_MAX algorithm and returns [[x,y], Score]
# if no moe is possile returns [[], MIN_SCORE]
def getMaxMove(board, depth, compHeuristic, compTime, abPrune, a, b, root):
    # print("MaxMove depth: ", depth)
    bestScore = MIN_SCORE
    bestMove = []

    if depth == 0:
        return [bestMove, bestScore]
    else:
        depth -= 1

    # Given a board and the computer"s tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)
    # print("Max Move Posible Moves: ", possibleMoves)

    # randomize the order of the possible moves
    random.shuffle(possibleMoves)

    if len(possibleMoves) == 0:
        return [bestMove, bestScore]

    for x, y in possibleMoves:
        global ComputerMovesEvaluated
        ComputerMovesEvaluated += 1

        # print("Max possible Move: ", x, y)
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)

        move, score = getMinMove(dupeBoard, depth, compHeuristic, compTime, abPrune, a, b)
        # getMinMove will return MIN_SCORE if no move is possible
        if score == MAX_SCORE:
            # hybrid between weights and adaptive function:
            # if countPieces(board) < 50:
            #   score = getWeightedScoreOfBoard(dupeBoard)[computerTile]
            # else:
            #    score = getAdaptiveHeuristicScore(dupeBoard, computerTile, "X", len(possibleMoves))

            if compHeuristic == 'greedy':
                score = getScoreOfBoard(dupeBoard)[computerTile]
            elif compHeuristic == 'weighted':
                score = getWeightedScoreOfBoard(dupeBoard)[computerTile]
            elif compHeuristic == 'adaptive':
                score = getAdaptiveHeuristicScore(dupeBoard, computerTile, "X", len(possibleMoves), compTime)
            elif compHeuristic == 'stable_adaptive':
                score = getAdaptiveHeuristicScoreWithStability(dupeBoard, computerTile, "X", len(possibleMoves),
                                                               compTime)
            elif compHeuristic == 'stable_hybrid':
                score = getHybridHeuristicScoreWithStability(dupeBoard, computerTile, "X", len(possibleMoves), compTime)
            else:
                score = getHybridHeuristicScore(dupeBoard, computerTile, "X", len(possibleMoves), compTime)

            # score = getAdaptiveHeuristicScore(dupeBoard, computerTile, "X", len(possibleMoves))
            # print("Max Possible Move and Score: ", x, y, score)

        else:
            # getMinMove returned a score
            if abPrune is True:
                if a < score:
                    a = score
                    # print("Max abMinMax: ", (a, b), file=log_file)

        if score > bestScore:
            bestMove = [x, y]
            bestScore = score

        # never prune root
        if abPrune is True and root is not True:
            if bestScore >= b:
                # print("Max: Pruning bestScore, abMinMax", bestScore, (a, b), file=log_file)
                break;

    # print("Max: Best Move and Score: ", bestMove, bestScore)
    return [bestMove, bestScore]


def getMinMove(board, depth, compHeuristic, compTime, abPrune, a, b):
    bestScore = MAX_SCORE
    bestMove = []

    # print("MinMove depth: ", depth)
    if depth == 0:
        return [bestMove, bestScore]
    else:
        depth -= 1

    # Given a board and the computer"s tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, playerTile)
    # print("Min Move Posible Moves: ", possibleMoves)

    # randomize the order of the possible moves
    random.shuffle(possibleMoves)

    if len(possibleMoves) == 0:
        return [bestMove, MAX_SCORE]

    for x, y in possibleMoves:
        global ComputerMovesEvaluated
        ComputerMovesEvaluated += 1
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, playerTile, x, y)
        # print("Min Possible Move: ", x, y)

        move, score = getMaxMove(dupeBoard, depth, compHeuristic, compTime, abPrune, a, b, root=False)

        # if Max's score is less than Min Max Value update Min's max value
        if abPrune is True and score != MIN_SCORE:
            if b > score:
                b = score
                # print("Min abMinMax: ", (a,b), file=log_file )

        # getMaxMove will return MIN_SCORE if no move is possible
        if score == MIN_SCORE:
            # hybrid between weights and adaptive function:
            # if countPieces(board) < 50:
            #    score = getWeightedScoreOfBoard(dupeBoard)[computerTile]
            # else:
            #    score = getAdaptiveHeuristicScore(dupeBoard, computerTile, "X", len(possibleMoves))

            if compHeuristic == 'greedy':
                score = getScoreOfBoard(dupeBoard)[computerTile]
            elif compHeuristic == 'weighted':
                score = getWeightedScoreOfBoard(dupeBoard)[computerTile]
            elif compHeuristic == 'adaptive':
                score = getAdaptiveHeuristicScore(dupeBoard, computerTile, "X", len(possibleMoves), compTime)
            else:
                score = getHybridHeuristicScore(dupeBoard, computerTile, "X", len(possibleMoves), compTime)

            # score = getAdaptiveHeuristicScore(dupeBoard, computerTile, "X", len(possibleMoves))
            # print("Min Possible Move and score : ", x, y, score)

        if score < bestScore:
            bestMove = [x, y]
            bestScore = score

        if abPrune is True:
            if bestScore <= a:
                # print("Min: Pruning bestScore, abMinMax", bestScore, (a, b), file=log_file)
                break;

    # print("Min: Best Move and Score: ", bestMove, bestScore)
    return [bestMove, bestScore]


def othello_human_play(compHeuristic, compTime, depth, abPrune):
    print("\n--WELCOME TO OTHELLO--")
    print("----------------------\n")

    while True:
        # Reset the board and game.
        mainBoard = getNewBoard()
        resetBoard(mainBoard)

        # playerTile, computerTile = enterPlayerTile()
        playerTile, computerTile = ["X", "O"]
        print("Thank you for playing!\n")
        print("You will place the X tiles.")
        print("To move, type the row digit (1-8), then the column digit (1-8). [row,column]")
        print("For example, 18 will be the top-right corner.")

        # Show possible moves for the user
        showHints = False

        # turn = whoGoesFirst()
        turn = "computer"
        print("The " + turn + " will move first.")

        nComputerMoves = 0
        while True:

            if turn == "player":
                # Player"s turn.
                if showHints:
                    validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(mainBoard)

                showPoints(playerTile, computerTile, mainBoard)
                # input("Input your move and press Enter to see the players's move.\n\n")
                move = getPlayerMove(mainBoard, playerTile)
                # move = getPlayerMove(mainBoard, playerTile, playerHeuristic, playerTime)

                if move == "quit":
                    print("Thank you for playing!")
                    sys.exit()  # terminate the program
                elif move == "hints":
                    showHints = not showHints
                    continue
                else:
                    makeMove(mainBoard, playerTile, move[0], move[1])
                # makeMove(mainBoard, playerTile, move[0], move[1])

                if getValidMoves(mainBoard, computerTile) != []:
                    turn = "computer"
                elif getValidMoves(mainBoard, playerTile) != []:
                    print('The computer has no moves.  Your turn again.')
                    turn = "player"
                else:
                    break


            else:
                # Computer"s turn.
                nComputerMoves += 1
                drawBoard(mainBoard)
                showPoints(playerTile, computerTile, mainBoard)
                input("Press Enter to see the computer's move.\n\n")
                # move, score =  getComputerMove(mainBoard, computerTile)
                # print("Computer move was: ", move, score)
                # move, score = getMinMaxMove(mainBoard, compHeuristic, compTime, depth)
                move, score = getMinMaxMove(mainBoard, compHeuristic, compTime, depth, abPrune)
                # print("Min Max move was: ", move, score)
                if score != MIN_SCORE:
                    makeMove(mainBoard, computerTile, move[0], move[1])
                # print("Computer move was: [", move[0]+1, ',' move[1]+1 , ']')#, score)
                print("Computer move was:", str(move[0] + 1) + str(move[1] + 1))  # , score)

                # print("Computer move was: ", move)
                # print("row = %s"    %(x+1))
                # print("column = %s" %(y+1))

                if getValidMoves(mainBoard, playerTile) != []:
                    turn = "player"
                elif getValidMoves(mainBoard, computerTile) != []:
                    print('You have no moves. It is the computers turn again.')
                    turn = "computer"
                else:
                    break

        print("Computer Moves: ", nComputerMoves)
        # Display the final score.
        drawBoard(mainBoard)
        scores = getScoreOfBoard(mainBoard)
        print("X (you) scored %s points. O (computer) scored %s points." % (scores["X"], scores["O"]))
        showPoints(playerTile, computerTile, mainBoard)

        if scores[playerTile] > scores[computerTile]:
            print("You won. You beat the computer by %s points! Congratulations!" % (
                        scores[playerTile] - scores[computerTile]))
            print("PLAYER won!")
        elif scores[playerTile] < scores[computerTile]:
            print("You lost. The computer beat you by %s points." % (scores[computerTile] - scores[playerTile]))
            print("COMPUTER won!")
            return 1
        else:
            print("The game was a tie!")
            print("TIE!")
        if scores[playerTile] < scores[computerTile]:
            return 1

        if not playAgain():
            break
        break
    return 0


othello_human_play('stable_hybrid', [1, 80, 30, 10, 50], 5, abPrune=True)


