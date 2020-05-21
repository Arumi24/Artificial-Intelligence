import numpy
import sys
import random
import time
import copy


class Board(object):

    def __init__(self, copy=False, board=None):

        if copy == True:
            self.board = board
        else:
            self.board = numpy.empty([6, 7], dtype="<U20")
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    self.board[i][j] = "_"

    def putRed(self, pos):
        col = 0
        if self.board[0][pos-1] != "_":
            print("Move Not Allowed")
        else:
            while True:
                if col == len(self.board)-1:
                    self.board[col][pos-1] = "\x1b[31mO\x1b[0m"
                    break
                elif self.board[col][pos-1] == "_" and self.board[col+1][pos-1] != "_":
                    self.board[col][pos-1] = "\x1b[31mO\x1b[0m"
                    break
                else:
                    col = col+1

    def putYellow(self, pos):

        col = 0
        if self.board[0][pos-1] != "_":
            print("Move Not Allowed")
        else:
            while True:
                if col == len(self.board)-1:
                    self.board[col][pos-1] = "\x1b[33mO\x1b[0m"
                    break
                elif self.board[col][pos-1] == "_" and self.board[col+1][pos-1] != "_":
                    self.board[col][pos-1] = "\x1b[33mO\x1b[0m"
                    break
                else:
                    col = col+1

    def printBoard(self):

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if(j != len(self.board[0])-1):
                    print("|{}".format(self.board[i][j]), end='')
                else:
                    print("|{}|".format(self.board[i][j]))

    def returnBoard(self):
        return self.board


class Player(object):

    def __init__(self):
        pass

    def availableMoves(self, Board):
        moves = []
        for i in range(len(Board.board[0])):
            if Board.board[0][i] == "_":
                moves.append(i+1)
        return moves

    def simulateRedMove(self, Board, pos):
        board = Board.board.copy()
        col = 0
        if board[0][pos-1] != "_":
            return None
        else:
            while True:
                if col == len(board)-1:
                    board[col][pos-1] = "\x1b[31mO\x1b[0m"
                    break
                elif board[col][pos-1] == "_" and board[col+1][pos-1] != "_":
                    board[col][pos-1] = "\x1b[31mO\x1b[0m"
                    break
                else:
                    col = col+1
        return board

    def simulateYellowMove(self, Board, pos):
        board = Board.board.copy()
        col = 0
        if board[0][pos-1] != "_":
            return None
        else:
            while True:
                if col == len(board)-1:
                    board[col][pos-1] = "\x1b[33mO\x1b[0m"
                    break

                elif board[col][pos-1] == "_" and board[col+1][pos-1] != "_":
                    board[col][pos-1] = "\x1b[33mO\x1b[0m"
                    break

                else:
                    col = col+1

        return board


class RandomPlayer(Player):

    def __init__(self):
        super().__init__()

    def pickMove(self, Board, turn):
        moves = self.availableMoves(Board)

        if turn == "Yellow":
            Board.putYellow(random.choice(moves))

        else:
            Board.putRed(random.choice(moves))


class HeuristicPlayer(Player):

    def __init__(self):
        super().__init__()

    def pickMove(self, Board, turn):

        moves = self.availableMoves(Board)

        random.shuffle(moves)

        boards = []
        evaluations = []

        for i in moves:

            if turn == "Yellow":
                boards.append(self.simulateYellowMove(Board, i))

            if turn == "Red":
                boards.append(self.simulateRedMove(Board, i))

        for board in boards:

            evaluations.append(self.EvaluationFunction(board, turn))

        if turn == "Yellow":

            Board.putYellow(moves[evaluations.index(max(evaluations))])

        if turn == "Red":

            Board.putRed(moves[evaluations.index(max(evaluations))])

    def EvaluationFunction(self, board, turn):

        if turn == "Yellow":
           
            maxRows = []
            maxRows.append(self.rightDiagonal(board, "Yellow"))
            maxRows.append(self.leftDiagonal(board, "Yellow"))
            maxRows.append(self.horizontal(board, "Yellow"))
            maxRows.append(self.vertical(board, "Yellow"))

            if max(maxRows) >= 4:
                return 1000000
            elif max(maxRows) == 3:
                return 1000
            elif max(maxRows) == 2:
                return 100
            elif max(maxRows) == 1:
                return 10
            else:
                return 0

        if turn == "Red":

           
            maxRows = []
            maxRows.append(self.rightDiagonal(board, "Red"))
            maxRows.append(self.leftDiagonal(board, "Red"))
            maxRows.append(self.horizontal(board, "Red"))
            maxRows.append(self.vertical(board, "Red"))

            if max(maxRows) >= 4:
                return 1000000
            elif max(maxRows) == 3:
                return 1000
            elif max(maxRows) == 2:
                return 100
            elif max(maxRows) == 1:
                return 10
            else:
                return 0

    def Statistics(self, Board):

        print("")

        print("\x1b[31mRed Statistics:\x1b[0m", end='        ')
        print("\x1b[33mYellow Statistics:\x1b[0m")
        print("Right Diagonal: {}      Right Diagonal: {}".format(self.rightDiagonal(
            Board.board, "Red"), self.rightDiagonal(Board.board, "Yellow")))
        print("Left Diagonal: {}       Left Diagonal: {}".format(self.leftDiagonal(
            Board.board, "Red"), self.leftDiagonal(Board.board, "Yellow")))
        print("Horizontal: {}          Horizontal: {}".format(self.horizontal(
            Board.board, "Red"), self.horizontal(Board.board, "Yellow")))
        print("Vertical: {}            Vertical: {}".format(self.vertical(
            Board.board, "Red"), self.vertical(Board.board, "Yellow")))

    """
    def chancesToWin(self,board,turn):

    def inARows(self,board,turn):
    """

    def rightDiagonal(self, board, turn):

        if turn == "Yellow":

            max = 0

            for i in range(len(board)):
                for j in range(len(board[0])):

                    if board[i][j] == "\x1b[33mO\x1b[0m":

                        inARow = 1
                        a = 1
                        b = 1

                        while i-a >= 0 and j+b < 7:

                            if board[i-a][j+b] == "\x1b[33mO\x1b[0m":
                                inARow = inARow+1
                                a = a+1
                                b = b+1
                            else:

                                break

                        if inARow > max:
                            max = inARow
            return max

        else:

            max = 0

            for i in range(len(board)):
                for j in range(len(board[0])):

                    if board[i][j] == "\x1b[31mO\x1b[0m":

                        inARow = 1
                        a = 1
                        b = 1

                        while i-a >= 0 and j+b < 7:

                            if board[i-a][j+b] == "\x1b[31mO\x1b[0m":
                                inARow = inARow+1
                                a = a+1
                                b = b+1
                            else:

                                break

                        if inARow > max:
                            max = inARow
            return max

    def leftDiagonal(self, board, turn):

        if turn == "Yellow":

            max = 0

            for i in range(len(board)):
                for j in range(len(board[0])):

                    if board[i][j] == "\x1b[33mO\x1b[0m":

                        inARow = 1
                        a = 1
                        b = 1

                        while i-a >= 0 and j-b >= 0:

                            if board[i-a][j-b] == "\x1b[33mO\x1b[0m":
                                inARow = inARow+1
                                a = a+1
                                b = b+1
                            else:

                                break

                        if inARow > max:
                            max = inARow
            return max

        else:

            max = 0

            for i in range(len(board)):
                for j in range(len(board[0])):

                    if board[i][j] == "\x1b[31mO\x1b[0m":

                        inARow = 1
                        a = 1
                        b = 1

                        while i-a >= 0 and j-b >= 0:

                            if board[i-a][j-b] == "\x1b[31mO\x1b[0m":
                                inARow = inARow+1
                                a = a+1
                                b = b+1
                            else:

                                break

                        if inARow > max:
                            max = inARow
            return max

    def horizontal(self, board, turn):

        if turn == "Yellow":

            max = 0

            for i in range(len(board)):
                for j in range(len(board[0])):

                    if board[i][j] == "\x1b[33mO\x1b[0m":

                        inARow = 1

                        b = 1

                        while j+b < 7:

                            if board[i][j+b] == "\x1b[33mO\x1b[0m":
                                inARow = inARow+1

                                b = b+1
                            else:

                                break

                        if inARow > max:
                            max = inARow
            return max

        else:

            max = 0

            for i in range(len(board)):
                for j in range(len(board[0])):

                    if board[i][j] == "\x1b[31mO\x1b[0m":

                        inARow = 1

                        b = 1

                        while j+b < 7:

                            if board[i][j+b] == "\x1b[31mO\x1b[0m":
                                inARow = inARow+1

                                b = b+1
                            else:

                                break

                        if inARow > max:
                            max = inARow
            return max

    def vertical(self, board, turn):

        if turn == "Yellow":

            max = 0

            for i in range(len(board)):
                for j in range(len(board[0])):

                    if board[i][j] == "\x1b[33mO\x1b[0m":

                        inARow = 1
                        a = 1

                        while i-a >= 0:

                            if board[i-a][j] == "\x1b[33mO\x1b[0m":
                                inARow = inARow+1
                                a = a+1

                            else:

                                break

                        if inARow > max:
                            max = inARow
            return max

        else:

            max = 0

            for i in range(len(board)):
                for j in range(len(board[0])):

                    if board[i][j] == "\x1b[31mO\x1b[0m":

                        inARow = 1
                        a = 1

                        while i-a >= 0:

                            if board[i-a][j] == "\x1b[31mO\x1b[0m":
                                inARow = inARow+1
                                a = a+1

                            else:

                                break

                        if inARow > max:
                            max = inARow
            return max


class AlphaBetaPlayer(HeuristicPlayer):

    def __init__(self):
        super().__init__()

    def pickMove(self, Board, turn):

        if turn == "Yellow":
            move = self.minimax(Board, 8, "Yellow", alpha=float(
                "-inf"), beta=float("inf"))[0]
            Board.putYellow(move)

        else:
            move = self.minimax(Board, 8, "Red", alpha=float(
                "-inf"), beta=float("inf"))[0]
            Board.putRed(move)

    def eval(self, Board):

        return self.EvaluationFunction(Board.board, "Red")-self.EvaluationFunction(Board.board, "Yellow")

    def minimax(self, Boardd, depth, turn, alpha, beta):

        if depth == 0 or self.EvaluationFunction(Boardd.board, "Yellow") == 1000000 or self.EvaluationFunction(Boardd.board, "Red") == 1000000 or len(self.availableMoves(Boardd)) == 0:
            return [None, self.eval(Boardd)]

        if turn == "Red":
            maxEval = float("-inf")
            tuple = []

            moves = self.availableMoves(Boardd)
            random.shuffle(moves)

            for i in moves:

                simulatedBoard = Board(
                    copy=True, board=self.simulateRedMove(Boardd, i))
                evaluation = self.minimax(
                    simulatedBoard, depth-1, "Yellow", alpha, beta)[1]

                if evaluation > maxEval:
                    maxEval = evaluation
                    tuple = [i, evaluation]

                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break

            return tuple

        else:

            minEval = float("inf")
            moveIndex = float("-inf")

            moves = self.availableMoves(Boardd)
            random.shuffle(moves)

            for i in moves:

                simulatedBoard = Board(
                    copy=True, board=self.simulateYellowMove(Boardd, i))

                evaluation = self.minimax(
                    simulatedBoard, depth-1, "Red", alpha, beta)[1]

                if evaluation < minEval:
                    minEval = evaluation
                    tuple = [i, evaluation]

                beta = min(beta, evaluation)

                if beta <= alpha:
                    break

            return tuple


class Game(object):

    def __init__(self):
        pass

    def checkRightDiagonal(self, Board, color):

        if color == "Yellow":

            for i in range(len(Board.board)):
                for j in range(len(Board.board[0])):

                    if Board.board[i][j] == "\x1b[33mO\x1b[0m":

                        inARow = 1
                        a = 1
                        b = 1

                        while i-a >= 0 and j+b < 7:

                            if Board.board[i-a][j+b] == "\x1b[33mO\x1b[0m":
                                inARow = inARow+1
                                a = a+1
                                b = b+1
                            else:
                                break

                        if inARow >= 4:
                            return True

        else:

            for i in range(len(Board.board)):

                for j in range(len(Board.board[0])):

                    if Board.board[i][j] == "\x1b[31mO\x1b[0m":

                        inARow = 1
                        a = 1
                        b = 1

                        while i-a >= 0 and j+b < 7:

                            if Board.board[i-a][j+b] == "\x1b[31mO\x1b[0m":
                                inARow = inARow+1
                                a = a+1
                                b = b+1
                            else:
                                break

                        if inARow >= 4:
                            return True

        return False

    def checkLeftDiagonal(self, Board, color):

        if color == "Yellow":

            for i in range(len(Board.board)):
                for j in range(len(Board.board[0])):

                    if Board.board[i][j] == "\x1b[33mO\x1b[0m":

                        inARow = 1
                        a = 1
                        b = 1

                        while i-a >= 0 and j-b >= 0:

                            if Board.board[i-a][j-b] == "\x1b[33mO\x1b[0m":
                                inARow = inARow+1
                                a = a+1
                                b = b+1
                            else:
                                break

                        if inARow >= 4:
                            return True

        else:

            for i in range(len(Board.board)):

                for j in range(len(Board.board[0])):

                    if Board.board[i][j] == "\x1b[31mO\x1b[0m":

                        inARow = 1
                        b = 1
                        a = 1

                        while i-a >= 0 and j-b >= 0:

                            if Board.board[i-a][j-b] == "\x1b[31mO\x1b[0m":
                                inARow = inARow+1
                                a = a+1
                                b = b+1
                            else:
                                break

                        if inARow >= 4:
                            return True

        return False

    def checkVertical(self, Board, color):

        if color == "Yellow":

            for i in range(len(Board.board)):
                for j in range(len(Board.board[0])):

                    if Board.board[i][j] == "\x1b[33mO\x1b[0m":

                        inARow = 1
                        a = 1

                        while i-a >= 0:

                            if Board.board[i-a][j] == "\x1b[33mO\x1b[0m":
                                inARow = inARow+1
                                a = a+1
                            else:
                                break

                        if inARow >= 4:
                            return True

        else:

            for i in range(len(Board.board)):

                for j in range(len(Board.board[0])):

                    if Board.board[i][j] == "\x1b[31mO\x1b[0m":

                        inARow = 1
                        a = 1

                        while i-a >= 0:

                            if Board.board[i-a][j] == "\x1b[31mO\x1b[0m":
                                inARow = inARow+1
                                a = a+1
                            else:
                                break

                        if inARow >= 4:
                            return True

        return False

    def checkHorizontal(self, Board, color):

        if color == "Yellow":

            for i in range(len(Board.board)):
                for j in range(len(Board.board[0])):

                    if Board.board[i][j] == "\x1b[33mO\x1b[0m":

                        inARow = 1

                        b = 1

                        while j+b < 7:

                            if Board.board[i][j+b] == "\x1b[33mO\x1b[0m":
                                inARow = inARow+1
                                b = b+1
                            else:
                                break

                        if inARow >= 4:
                            return True

        else:

            for i in range(len(Board.board)):

                for j in range(len(Board.board[0])):

                    if Board.board[i][j] == "\x1b[31mO\x1b[0m":

                        inARow = 1

                        b = 1

                        while j+b < 7:

                            if Board.board[i][j+b] == "\x1b[31mO\x1b[0m":
                                inARow = inARow+1
                                b = b+1
                            else:
                                break

                        if inARow >= 4:
                            return True

        return False

    def checkWinner(self, Board):
        if(self.checkHorizontal(Board, "Red") or self.checkVertical(Board, "Red") or self.checkLeftDiagonal(Board, "Red") or self.checkRightDiagonal(Board, "Red")):
            return "Red"
        elif(self.checkHorizontal(Board, "Yellow") or self.checkVertical(Board, "Yellow") or self.checkLeftDiagonal(Board, "Yellow") or self.checkRightDiagonal(Board, "Yellow")):
            return "Yellow"
        else:
            return None

    def TwoPlayer(self):

        print("Welcome to Two Player Game")
        board = Board()
        player = Player()
        statistics = HeuristicPlayer()

        turn = 2

        while True:

            statistics.Statistics(board)
            print("")
            board.printBoard()
            if self.checkWinner(board) == "Red":
                print("")
                print("\x1b[31mRed Won!!!\x1b[0m")
                print("Game Over")
                break
            elif self.checkWinner(board) == "Yellow":
                print("")
                print("\x1b[33mYellow Won!!!\x1b[0m")
                print("Game Over")
                break

            if(turn % 2 == 0):

                print("_____________________________")
                print("\x1b[31mRed Turn:\x1b[0m")
                print("Please pick available moves")
                print(player.availableMoves(board))
                print("")

                move = int(input())

                board.putRed(move)

            else:

                print("_____________________________")
                print("\x1b[33mYellow Turn:\x1b[0m")
                print("Please pick available moves")
                print(player.availableMoves(board))
                print("")

                move = int(input())

                board.putYellow(move)

            turn = turn+1
            if turn == 45:

                print("")
                print("Tie Game!!!")
                print("Game Over")
                break

    def VsRandomPlayer(self):

        print("Welcome to Vs Random Player")
        board = Board()
        player = RandomPlayer()

        turn = 2

        while True:

            board.printBoard()
            if self.checkWinner(board) == "Red":
                print("")
                print("\x1b[31mRed Won!!!\x1b[0m")
                print("Game Over")
                break
            elif self.checkWinner(board) == "Yellow":
                print("")
                print("\x1b[33mYellow Won!!!\x1b[0m")
                print("Game Over")
                break

            if(turn % 2 == 0):

                print("_____________________________")
                print("\x1b[31mRed Turn:\x1b[0m")
                print("Please pick available moves")
                print(player.availableMoves(board))
                print("")

                move = int(input())

                board.putRed(move)

            else:

                time.sleep(0.5)
                print("_____________________________")
                print("\x1b[33mYellow Turn:\x1b[0m")
                print("Please wait....")

                print("")

                player.pickMove(board, "Yellow")

            turn = turn+1

            if turn == 45:
                print("")
                print("Tie Game!!!")
                print("Game Over")
                break

    def VsHeuristicPlayer(self):

        print("Welcome to Vs Heuristic Player")
        board = Board()
        player = HeuristicPlayer()

        turn = 2

        while True:

            board.printBoard()
            if self.checkWinner(board) == "Red":
                print("")
                print("\x1b[31mRed Won!!!\x1b[0m")
                print("Game Over")
                break
            elif self.checkWinner(board) == "Yellow":
                print("")
                print("\x1b[33mYellow Won!!!\x1b[0m")
                print("Game Over")
                break

            if(turn % 2 == 0):

                print("_____________________________")
                print("\x1b[31mRed Turn:\x1b[0m")
                print("Please pick available moves")
                print(player.availableMoves(board))
                print("")

                move = int(input())

                board.putRed(move)

            else:

                time.sleep(0.5)
                print("_____________________________")
                print("\x1b[33mYellow Turn:\x1b[0m")
                print("Please wait....")

                print("")

                player.pickMove(board, "Yellow")

            turn = turn+1

            if turn == 45:
                print("")
                print("Tie Game!!!")
                print("Game Over")
                break

    def VsAlphaBetaPlayer(self):

        print("Welcome to Vs AlphaBeta Player")
        board = Board()
        player = AlphaBetaPlayer()

        turn = 2

        while True:

            board.printBoard()
            print("")
            print("Current Board Eval: {}".format(player.eval(board)))
            print("")
            if self.checkWinner(board) == "Red":
                print("")
                print("\x1b[31mRed Won!!!\x1b[0m")
                print("Game Over")
                break
            elif self.checkWinner(board) == "Yellow":
                print("")
                print("\x1b[33mYellow Won!!!\x1b[0m")
                print("Game Over")
                break

            if(turn % 2 == 0):

                print("_____________________________")
                print("\x1b[31mRed Turn:\x1b[0m")
                print("Please pick available moves")
                print(player.availableMoves(board))
                print("")

                move = int(input())

                board.putRed(move)

            else:

                print("_____________________________")
                print("\x1b[33mYellow Turn:\x1b[0m")
                print("Please wait....")
                print("")

                player.pickMove(board, "Yellow")

            turn = turn+1

            if turn == 45:
                print("")
                print("Tie Game!!!")
                print("Game Over")
                break

    def RandomVsRandom(self):

        print("Welcome to Random vs Random")
        board = Board()
        player = RandomPlayer()

        turn = 2

        while turn <= 44:

            board.printBoard()
            if self.checkWinner(board) == "Red":
                print("")
                print("\x1b[31mRed Won!!!\x1b[0m")
                print("Game Over")
                break
            elif self.checkWinner(board) == "Yellow":
                print("")
                print("\x1b[33mYellow Won!!!\x1b[0m")
                print("Game Over")
                break

            if(turn % 2 == 0 and turn < 44):

                print("_____________________________")
                print("\x1b[31mRed Turn:\x1b[0m")
                print("Please wait...")
                print("")

                player.pickMove(board, "Red")

            elif(turn < 44):

                print("_____________________________")
                print("\x1b[33mYellow Turn:\x1b[0m")
                print("Please wait...")
                print("")

                player.pickMove(board, "Yellow")

            time.sleep(0.5)
            turn = turn+1

            if turn == 45:
                print("")
                print("Tie Game!!!")
                print("Game Over")
                break


    def RandomVsHeuristic(self):

        print("Welcome to Random vs Heuristic")
        board = Board()
        randomPlayer = RandomPlayer()
        heuristicPlayer= HeuristicPlayer()

        turn = 2

        while turn <= 44:

            board.printBoard()
            if self.checkWinner(board) == "Red":
                print("")
                print("\x1b[31mHeuristic Player Won!!!\x1b[0m")
                print("Game Over")
                break
            elif self.checkWinner(board) == "Yellow":
                print("")
                print("\x1b[33mRandom Player Won!!!\x1b[0m")
                print("Game Over")
                break

            if(turn % 2 == 0 and turn < 44):

                print("_____________________________")
                print("\x1b[31mRed Turn(Heuristic Player):\x1b[0m")
                print("Please wait...")
                print("")

                heuristicPlayer.pickMove(board, "Red")

            elif(turn < 44):

                print("_____________________________")
                print("\x1b[33mYellow Turn(Random Player):\x1b[0m")
                print("Please wait...")
                print("")

                randomPlayer.pickMove(board, "Yellow")

            time.sleep(0.5)
            turn = turn+1

            if turn == 45:
                print("")
                print("Tie Game!!!")
                print("Game Over")
                break


    def RandomVsAlphaBeta(self):

        print("Welcome to Random vs Alpha Beta")
        board = Board()
        randomPlayer = RandomPlayer()
        alphaPlayer = AlphaBetaPlayer()

        turn = 2

        while turn <= 44:

            board.printBoard()
            if self.checkWinner(board) == "Red":
                print("")
                print("\x1b[31mAlpha Beta Player Won!!!\x1b[0m")
                print("Game Over")
                break
            elif self.checkWinner(board) == "Yellow":
                print("")
                print("\x1b[33mRandom Player Won!!!\x1b[0m")
                print("Game Over")
                break

            if(turn % 2 == 0 and turn < 44):

                print("_____________________________")
                print("\x1b[31mRed Turn(Alpha Beta Player):\x1b[0m")
                print("Please wait....")
                print("")

                alphaPlayer.pickMove(board, "Red")

            elif(turn < 44):

                print("_____________________________")
                print("\x1b[33mYellow Turn(Random Player):\x1b[0m")
                print("Please wait....")
                print("")
                time.sleep(1)

                randomPlayer.pickMove(board, "Yellow")

            turn = turn+1

            if turn == 45:
                print("")
                print("Tie Game!!!")
                print("Game Over")
                break


    def HeuristicVsAlphaBeta(self):

        print("Welcome to Heuristic vs Alpha Beta")
        board = Board()
        heuristicPlayer = HeuristicPlayer()
        alphaPlayer = AlphaBetaPlayer()

        turn = 2

        while turn <= 44:

            board.printBoard()
            if self.checkWinner(board) == "Red":
                print("")
                print("\x1b[31mAlpha Beta Player Won!!!\x1b[0m")
                print("Game Over")
                break
            elif self.checkWinner(board) == "Yellow":
                print("")
                print("\x1b[33mRandom Player Won!!!\x1b[0m")
                print("Game Over")
                break

            if(turn % 2 == 0 and turn < 44):

                print("_____________________________")
                print("\x1b[31mRed Turn(AlphaBeta Player):\x1b[0m")
                print("Please wait....")
                print("")

                alphaPlayer.pickMove(board, "Red")

            elif(turn < 44):

                print("_____________________________")
                print("\x1b[33mYellow Turn(Heuristic Player):\x1b[0m")
                print("Please wait....")
                print("")
                time.sleep(1)

                heuristicPlayer.pickMove(board, "Yellow")

            turn = turn+1

            if turn == 45:
                print("")
                print("Tie Game!!!")
                print("Game Over")
                break

    def AlphaBetaVsAlphaBeta(self):

        print("Welcome to Alpha Beta vs Alpha Beta")
        board = Board()
        alphaPlayer1 = AlphaBetaPlayer()
        alphaPlayer2 = AlphaBetaPlayer()

        turn = 2

        while turn <= 44:

            board.printBoard()
            print("")
            print("Current Board Eval: {}".format(alphaPlayer1.eval(board)))
            print("")
            if self.checkWinner(board) == "Red":
                print("")
                print("\x1b[31mRed Won!!!\x1b[0m")
                print("Game Over")
                break
            elif self.checkWinner(board) == "Yellow":
                print("")
                print("\x1b[33mYellow Won!!!\x1b[0m")
                print("Game Over")
                break

            if(turn % 2 == 0 and turn < 44):

                print("_____________________________")
                print("\x1b[31mRed Turn:\x1b[0m")
                print("Please wait....")
                print("")

                alphaPlayer1.pickMove(board, "Red")

            elif(turn < 44):

                print("_____________________________")
                print("\x1b[33mYellow Turn:\x1b[0m")
                print("Please wait....")
                print("")

                alphaPlayer2.pickMove(board, "Yellow")

            turn = turn+1

            if turn == 45:
                print("")
                print("Tie Game!!!")
                print("Game Over")
                break

    def PlayGame(self):

        print("Welcome to Connect 4 !!!")

        while True:
            print("Please pick one of the following option below:")
            print("")
            print("1: Two Player")
            print("2: Vs Random Player")
            print("3: Vs Heuristic Player")
            print("4: Vs Alpha Beta Player (Caution: Unbeatable)")
            print("5: Vs Reinforcement Learning Player (Caution: Unbeatable)")
            print("6: Random Player Vs Random Player")
            print("7: Random Player Vs Heuristic Player")
            print("8: Random Player Vs Alpha Beta Player")
            print("9: Heuristic Player Vs Alpha Beta Player")
            print("10: Alpha Beta Player Vs Alpha Beta Player")

            mode = int(input())

            if mode == 1:
                print("")
                self.TwoPlayer()

            elif mode == 2:
                print("")
                self.VsRandomPlayer()

            elif mode == 3:
                print("")
                self.VsHeuristicPlayer()

            elif mode == 4:
                print("")
                self.VsAlphaBetaPlayer()

            elif mode == 6:
                print("")
                self.RandomVsRandom()

            elif mode == 7:
                print("")
                self.RandomVsHeuristic()

            elif mode == 8:
                print("")
                self.RandomVsAlphaBeta()

            elif mode == 9:
                print("")
                self.HeuristicVsAlphaBeta()

            elif mode == 10:
                print("")
                self.AlphaBetaVsAlphaBeta()

            print("")
            print("Would you like to play again?")
            print("")
            print("enter: continue")
            print("q: quit")

            if ((input())) == "q":
                break


def main():

    game = Game()

    game.PlayGame()


if __name__ == '__main__':
    main()
