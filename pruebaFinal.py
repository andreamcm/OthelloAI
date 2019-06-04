import os, copy
from random import randint
import math
import socketio
import random
import numpy as np

tileRep = ['_', 'X', 'O']
N = 8


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

def validMove2():
    posible = []
    final = []
    for x in range(0, 8):
        for y in range(0, 8):
            moving = isValidMove(board, 1, x, y)
            posible.append(moving)
    for n in range(len(posible)):
        if posible[n] != False:
            final.append(posible[n])
    return final

def alphabeta(board, depht, a, b, maximizingPlayer, tile):
    testboard = []
    moves = []
    indice = 0
    if depht == 0:
        temp = heuristic(board, tile)
        return heuristic(board, tile), indice
    

    othertile =1
    if tile == 1:
        othertile = 2
    finals = validMove2()
    # for z in finals:
    #     testboard.append(finals[0])
    #     moves.append(finals[1])
    # for n in finals:
    #     temp = alphabeta(n, depht - 1, a, b, False, tile)
    if maximizingPlayer:
        for n in finals:
            temp, index = alphabeta(n, depht - 1, a, b, False, tile)
            if a < temp:
                indice = n[1]
                a = temp
            if a >= b:
                break
        return a, indice
    
    else:
        for n in finals:
            temp, index = alphabeta(n, depht - 1, a, b, True, othertile)
            if b > temp:
                indice = n[1]
                b = temp
            if a >= b:
                break
        return b, indice

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
        0, 0, 0, 1, 2, 1, 0, 0, 
        0, 2, 1, 1, 2, 0, 0, 0, 
        0, 0, 1, 0, 2, 0, 0, 0, 
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


prueba, index = alphabeta(board, 1, -5000, 5000, True, 1)
columnillas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
filillas = ['1', '2', '3', '4', '5', '6', '7', '8']
columnita = random.randint(0, 7)
filita = random.randint(0, 7)
movement = filillas[filita] + columnillas[columnita]
print(movement)

# bad = filita*8 + columnita
# if(board[bad] != 0):
#     fili = random.randint(0, 7)
#     coli = random.randint(0, 7)
#     movement = filillas[fili] + columnillas[coli]
#     print(movement)