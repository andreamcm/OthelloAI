import os, copy
from random import randint
import math
import socketio
import random

tileRep = ['_', 'X', 'O']
N = 8

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

#socket =  socketio.Client()
socket = socketio.Client()
socket.connect('http://192.168.0.37:4000')
userName = 'Andrea Cordon'
tournamentID = 12

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
    columnillas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    filillas = ['1', '2', '3', '4', '5', '6', '7', '8']
    columnita = random.randint(0, 7)
    filita = random.randint(0, 7)
    #movement = filillas[filita] + columnillas[columnita]
    #print(movement)
    movement = Minimax(myBoard, 4, True)
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