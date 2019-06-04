import os, copy
from random import randint
import math
import socketio
import random

tileRep = ['_', 'X', 'O']
N = 8
minEvalBoard = -1 # min - 1
maxEvalBoard = N * N + 4 * N + 4 + 1 # max + 1

def ix(row, col):
    print(row)
    print(col)
    print('abcdefgh'.index(col))
    return (row-1)*N + 'abcdefgh'.index(col)

def humanBoard(board):
    result = 'A B C D E F G H'
    for i in range(len(board)):
        if i%N == 0:
            result += '\n \n' + str((int(math.floor(i/N)) + 1 )) + ' '
        
        result += ' ' + tileRep[board[i]] + ' '
        
    return result

def validateHumanPosition(position):
    validated = len(position) == 2
    
    if validated:
        row = int(position[0])
        col = position[1].lower()
        return (1 <= row and row <= N) and ('abcdefgh'.index(col) >= 0)
    
    else:
        return False

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

def validMove2(board, tile):
    posible = []
    final = []
    for x in range(0, 8):
        for y in range(0, 8):
            moving = isValidMove(board, tile, x, y)
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
    finals = validMove2(board, tile)
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


#socket =  socketio.Client()
socket = socketio.Client()
socket.connect('http://192.168.1.148:4000')
userName = 'Andrea Cordon'
tournamentID = 142857

##cliente conectado 
print("Conecta: " + userName)

@socket.on('connect')
def on_connect():
    print("Conecta: " + userName)
    socket.emit('signin',{
            'user_name': userName,
            'tournament_id': tournamentID,
            'user_role': 'player'
        })

@socket.on('ready')
def on_ready(data):
    print('About to move. Board: \n')
    myBoard = humanBoard(data['board'])
    print(myBoard)
    print('\n Requisting move....')
    boardsito = data['board']
    prueba, index = alphabeta(boardsito, 1, -5000, 5000, True, data['player_turn_id'])
    columnillas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    filillas = ['1', '2', '3', '4', '5', '6', '7', '8']
    columnita = index[0][0]
    filita = index[0][1]
    movement = filillas[filita] + columnillas[columnita]
    print(movement)
    

    while(not(validateHumanPosition(movement))):
        movement = input("Insert your next move (1A = 8G): ")
        
    socket.emit('play',{
        'player_turn_id': data['player_turn_id'],
        'tournament_id': tournamentID,
        'game_id': data['game_id'],
        'movement': ix(int(movement[0]), movement[1].lower())
        })

@socket.on('finish')
def on_finish(data):
    print('Game '+ str(data['game_id'])+' has finished')
    print('Ready to play again!')
    
        
    socket.emit('player_ready',{
        'tournament_id': tournamentID,
        'game_id': data['game_id'],
        'player_turn_id': data['player_turn_id']
        })