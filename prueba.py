import os, copy
from random import randint
import math
#import socketio
import random
import numpy as np

tileRep = ['_', 'X', 'O']
N = 8
minEvalBoard = -1 # min - 1
maxEvalBoard = N * N + 4 * N + 4 + 1 # max + 1

def MakeMove(board, x, y, player): # assuming valid move
    totctr = 0 # total number of opponent pieces taken
    board[y][x] = player
    for d in range(8): # 8 directions
        ctr = 0
        for i in range(n):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            if dx < 0 or dx > n - 1 or dy < 0 or dy > n - 1:
                ctr = 0; break
            elif board[dy][dx] == player:
                break
            elif board[dy][dx] == '0':
                ctr = 0; break
            else:
                ctr += 1
        for i in range(ctr):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            board[dy][dx] = player
        totctr += ctr
    return (board, totctr)

def ValidMove(board, x, y, player):
    if x < 0 or x > N - 1 or y < 0 or y > N - 1:
        return False
    if board[x][y] != '_':
        return False
    (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
    if totctr == 0:
        return False
    return True


def EvalBoard(board, player):
    tot = 0
    for y in range(N):
        for x in range(N):
            if board[y][x] == player:
                if (x == 0 or x == N - 1) and (y == 0 or y == N - 1):
                    tot += 4 # corner
                elif (x == 0 or x == N - 1) or (y == 0 or y == N - 1):
                    tot += 2 # side
                else:
                    tot += 1
    return tot

def Minimax(board, depth, maximizingPlayer):
    player = 2
    if maximizingPlayer:
        bestValue = minEvalBoard
        for y in range(N):
            for x in range(N):
                if ValidMove(board, x, y, player):
                    (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
                    v = Minimax(boardTemp, player, depth - 1, False)
                    bestValue = max(bestValue, v)
    else: # 
        bestValue = maxEvalBoard
        for y in range(N):
            for x in range(N):
                if ValidMove(board, x, y, player):
                    (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
                    v = Minimax(boardTemp, player, depth - 1, True)
                    bestValue = min(bestValue, v)
    return bestValue

def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <=7

def isValidMove(board, tile, x, y):
    index = x * N + y

    if board[index] != 0 or not isOnBoard(x, y):
        return False

    testboard = copy.deepcopy(board)
    testboard[index] = tile

    otherTile = 1
    if tile == 1:
        otherTile = 2

    tilesToFlip = []
    nextMoves = []
    for xd, yd in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        i, j = x, y

        i += xd
        j += yd
        if isOnBoard(i, j) and testboard[i*N+j] == otherTile:
            i += xd
            j += yd
            if not isOnBoard(i, j):
                continue
            while testboard[i*N + j] == otherTile:
                i += xd
                j += yd

                if not isOnBoard(i, j):
                    break
            if not isOnBoard(i, j):
                continue
            if testboard[i*N + j] == tile:
                while True:
                    i -= xd
                    j -= yd

                    if i == x and j == y:
                        break
                    tilesToFlip.append([i, j])
                    nextMoves.append([x, y])

    if len(tilesToFlip) > 0: 
        for i in tilesToFlip : 
            testboard[i[0] * N + i[1]] = tile
        return testboard, nextMoves
    else:

        return False

def alphabeta(board, depht, a, b, maximizingPlayer, tile):
    if depht == 0:
        return heuristic(board, tile)

    if maximizingPlayer == True:
        testboard, moves = validMove2()
        for n in testboard:
            a = max(a, alphabeta(n, depht - 1, a, b, False))
            if a >= b:
                break
        print(a)
        return a
    
    elif maximizingPlayer == False:
        for n in testboard:
            b = min(b, alphabeta(n, depht - 1, a, b, True))
            if a >= b:
                break
        print(b)
        return b

def heuristic(testboard, mine):
    if mine == 1:
        other = 2
    else:
        other = 1
    
    ones = 0
    twos = 0
    heuristics = 0

    for i in range(len(testboard)):
        if testboard[i] == mine:
            ones += 1
            heuristics += ones - twos
        elif testboard[i] != mine:
            twos += 1
            heuristics += ones - twos
    return heuristics

board2 = [[' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ '],

[' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ '],

[' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ '],

[' _ ', ' _ ', ' _ ', ' O ', ' X ', ' _ ', ' _ ', ' _ '],

[' _ ', ' _ ', ' _ ', ' X ', ' O ', ' _ ', ' _ ', ' _ '],

[' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ '],

[' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ '],

[' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ ', ' _ ']]

board = [0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 1, 2, 0, 0, 0, 
        0, 0, 0, 2, 1, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0]

# board3 = [[0, 0, 0, 0, 0, 0, 0, 0], 
#         [0, 0, 0, 0, 0, 0, 0, 0], 
#         [0, 0, 0, 0, 0, 0, 0, 0], 
#         [0, 0, 0, 1, 2, 0, 0, 0], 
#         [0, 0, 0, 2, 1, 0, 0, 0], 
#         [0, 0, 0, 0, 0, 0, 0, 0], 
#         [0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0]]

#board = np.matrix(board)
#print(board)
#movement = Minimax(board, 4, False)

def validMove2():
        for x in range(0, 8):
            for y in range(0, 8):
                posible  = isValidMove(board, 1, x, y)
                if(posible != False):
                    return posible
                else:
                    return False


validMove2()