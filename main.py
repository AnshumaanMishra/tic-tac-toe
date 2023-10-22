# from pandas import DataFrame, read_csv
from numpy import array, rot90
import shelve
from random import randint

usermovelist = []
boardarray = []
userboard = array([['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']])
userboard2 = array([['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']])
winner = ''
board = array([['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']])
moves = []
sf=shelve.open('firstrun')
sf2 = shelve.open('moves')
try: 
    sf2['moves']
    print('success')
except KeyError:
    index = ' '.join(list(array([['.', '.', '.'], ['.', '.', '.'], ['X', 'X', '.']])[0]))+' '.join(list(array([['.', '.', '.'], ['.', '.', '.'], ['X', 'X', '.']])[1]))+' '.join(list(array([['.', '.', '.'], ['.', '.', '.'], ['X', 'X', '.']])[2]))
    sf2['moves'] = {index : 3}
    sf['FirstRun'] = True
moveData = sf2['moves']
print(moveData)
# moveData = DataFrame([['1 2', 3]], columns=['prevMove', 'nextMove'])


def checkSeries(sequence, character):
    for i in sequence:
        if i != character:
            return False
    return True 

def checkUser(board):
    if checkSeries(board[0], 'X'):
        return 1
    elif checkSeries(board[1], 'X'):
        return 1
    elif checkSeries(board[2], 'X'):
        return 1
    elif checkSeries(rot90(board)[0], 'X'):
        return 1
    elif checkSeries(rot90(board)[1], 'X'):
        return 1
    elif checkSeries(rot90(board)[2], 'X'):
        return 1
    elif board[0][0] == board[1][1] == board[2][2] == 'X' or board[2][0] == board[1][1] == board[0][2]=='X':
        return 1
    global winner
    winner = 'User'
    return 0


def checkAI(board):
    if checkSeries(board[0], 'O'):
        return 1
    elif checkSeries(board[1], 'O'):
        return 1
    elif checkSeries(board[2], 'O'):
        return 1
    elif checkSeries(rot90(board)[0], 'O'):
        return 1
    elif checkSeries(rot90(board)[1], 'O'):
        return 1
    elif checkSeries(rot90(board)[2], 'O'):
        return 1
    elif board[0][0] == board[1][1] == board[2][2] == 'O' or board[2][0] == board[1][1] == board[0][2]=='O':
        return 1
    return 0


def checkWin():
    global moves, board
    if checkUser(board):
        print("User Wins")
        return 1
    if checkAI(board):
        print("AI Wins")
        return 1
    if len(moves)==9:
        return 1


def fillBoard(usermove, character, index=1):
    global board, moves
    
    print('Move = ', usermove)
    board = rot90(board, index)
    print(usermove, moves, usermove in moves)
    if usermove not in moves:
        print('Filled')
        board[(usermove-1)//3][(usermove-1)%3] = character
        moves.append(usermove)
        board = rot90(board, 4-index)
        displayboard(board)
        return True
    else:
        return False


def fillUserBoard(usermove, character):
    global userboard, boardarray, userboard2
    userboard[(usermove-1)//3][(usermove-1)%3] = character
    userboard2 = userboard[::]
    boardarray.append(' '.join(list(userboard[0]))+' '.join(list(userboard[1]))+' '.join(list(userboard[2])))
    return userboard

def displayboard(board):
    # print(board[2], board[1], board[0], sep = '\n')
    print('\n', board[2][0], '|', board[2][1], '|', board[2][2], '\n', '---------\n' , board[1][0], '|', board[1][1], '|', board[1][2], '\n', '---------\n' , board[0][0], '|', board[0][1], '|', board[0][2])


def firstmove():
    if not fillBoard(randint(1, 9), 'O'):
        firstmove()
        return


def patternExixts(nextMove):
    if not fillBoard(nextMove, 'O'):
        firstmove()
        return False
    return True


def patternNotFound():
    return firstmove()


def checkPattern(userboard, index):
    global userboard2
    # lastThreeMoves = [str(i) for i in lastThreeMoves]
    strMoves = ' '.join(list(userboard[0]))+' '.join(list(userboard[1]))+' '.join(list(userboard[2]))
    strMoves2 = ' '.join(list(userboard2[0]))+' '.join(list(userboard2[1]))+' '.join(list(userboard2[2]))
    global moveData
    # print('checked')
    # print('MoveData', moveData.keys())
    if strMoves in moveData.keys():
        nextmove = moveData[strMoves]
        print('Next Move ', nextmove)
        return patternExixts(nextmove)
    # elif moveData.nextMove[moveData.prevMove == strMoves
    else:
        if index!=1 and strMoves==strMoves2: 
            print('strmoves',index, strMoves)
            print('strmoves2', strMoves2)
            return patternNotFound()
        return checkPattern(rot90(userboard), index+1)
        


def move(lastThreeMoves):
    global userboard
    if sf['FirstRun']:
        return firstmove()
    else:
        return checkPattern(userboard, 1)

def userMove():
    global boardarray, usermovelist
    usermove = int(input("Enter Move:"))
    if not fillBoard(usermove, 'X'):
        print('Place Already Occupied')
        print(moves)
        userMove()
    fillUserBoard(usermove, 'X')
    usermovelist.append(usermove)
    return usermove

displayboard(board)
userMove()
while True:
    move(moves[-4:-2])
    # firstmove()
    if checkWin():
        break
    userMove()
    if checkWin():
        break
    print(moves)
# usermovelist = [str(i) for i in usermovelist]
if winner == 'User':
    print('Moves = ', usermovelist)
    print(boardarray[-2])
    print(*boardarray, sep ='\n')
    addelement = boardarray[-2]
    if len(moves)>3:
        
        moveData[addelement] = usermovelist[-1]
        sf2['moves'] = moveData
    else:
        moveData[addelement] = usermovelist[-1]
        sf2['moves'] = moveData
sf['FirstRun'] = False
sf.close()
sf2.close()