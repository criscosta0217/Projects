board = [' ' for x in range(10)] #create a list called board that will start off with 10 empty values. Reason for empty values rather than 9 is because when we get input from the user they can type numbers 1-9 NOT 0-8. Making the first value in the list an empty string so when indexing elements in the list we use 1-9 NOT 0-8

def insertLetter(letter, pos): #this function is going to take 2 parameters: letter & position. It is going to insert the given letter at the given position
    board[pos] = letter

def spaceIsFree(pos): #this function tells us if the space if the given space is free - which means it does not already contain a letter. It has one parameter: pos, which will be an integer from 1-9
    return board[pos] == ' '

def printBoard(board): #this function takes the board as a parameter and will display it to the console
    print('   |   |') #"board" is a list of 10 strings representing the board (ignore index 0)
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')

def isWinner(bo, le): #this function tells me if the given letter has won based on the current board. It has 2 parameters: bo(board) & le(letter). The letter must be an X or an O. We checking each possible winning line on the board and see if its populated by the given letter
#given a board and a player's letter, this function returns True if that player has won.
#using bo instead of board and le instead of letter so i dont have to type as much 
    return((bo[7] == le and bo[8] == le and bo[9] == le) or #across the top
    (bo[4]  == le and bo[5] == le and bo[6] == le) or #across the middle
    (bo[1]  == le and bo[2] == le and bo[3] == le) or #across the bottom
    (bo[7]  == le and bo[4] == le and bo[1] == le) or #down the left side
    (bo[8]  == le and bo[5] == le and bo[2] == le) or #down the middle
    (bo[9]  == le and bo[6] == le and bo[3] == le) or #down the right side
    (bo[7]  == le and bo[5] == le and bo[3] == le) or #diagonal
    (bo[9]  == le and bo[5] == le and bo[1] == le)) #diagonal


def main():
    #main game logic
    print('Welcome to Tic Tac Toe, to win complete a straight line of your letter (Diagonal, Horizontal, Vertical). The board has positions from 1-9 starting at the top left.')
    printBoard()

    while not(isBoardFull(board)):
        if not(isWinner(board, 'O')):
            playerMove()
            printBoard()
        else:
            print('O\'s win this time...')
            break

        if not(isWinner(board, 'X')):
            move = compMove()
            if move == 0:
                print('Game is a Tie! No more spaces left to move.')
            else:
                insertBoard('O', move)
                print('Computer placed an \'O\' in position', move, ':')
                printBoard()
        else:
            print('X\'s win, good job!')
            break

    if isBoardFull(board):
        print('Game is a Tie! No more spaces left to move.')


def isBoardFull(board):
    if board.count(' ') > 1: #since there is always one blank element in board, must use > 1
        return False
    else:
        return True
    

def playerMove(): #in this function, we asking the user to input a move and validating it. If the move is valid, then add that letter to the board. Otherwise we will continue to ask the user for input. 
    run = True
    while run: #keep looping until we get a valid move
        move = input('Please select a position to place an \'X\' (1-9): ')
        try:
            move = int(move)
            if move > 0 and move < 10: #makes sure we type in a number between 1-9
                if spaceIsFree(move): #check if the move we choose is valid (no other letter is there already)
                    run = False
                    insertBoard('X', move)
                else:
                    print('This position is already occupied!')
            else:
                print('Please type a number within the range!')
        except:
            print('Please type a number!')


#This part is responsible for making the computer move. It will examine the board and determine which move is best to make. The algorithm used to do this is: 
#if the next step cannot be completed proceed to the next.
#step 1 - if there is a winning move, take it. 
#step 2 - if the player has a possible winning move on their next turn move into that position. 
#step 3 - take any one of the corners. If more than one is available randomly decide. 
#step 4 - take the center position 
#step 5 - take one of the edges. If more than one is available randomly decide
#step 6 - if no move is possible the game is a tie. 
def compMove():
    possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 0] #create a list of possible moves
    move = 0

    #check for possible winning move to take or to block opponents winning move
    for let in ['O','X']:
        for i in possibleMoves:
            boardCopy = board[:]
            boardCopy[i] = let
            if isWinner(boardCopy, let):
                move = i
                return move
    
    #try to take one of the corners
    cornersOpen = []
    for i in possibleMoves:
        if i in [1,3,7,9]:
            cornersOpen.append(i)
    if len(cornersOpen) > 0:
        move = selectRandom(cornersOpen)
        return move
    
    #try to take the center
    if 5 in possibleMoves:
        move = 5
        return move
    
    #take any edge
    edgesOpen = []
    for i in possibleMoves:
        if i in [2,4,6,8]:
            edgesOpen.append(i)

    if len(edgesOpen) > 0:
        move = selectRandom(edgesOpen)

    return move


def selectRandom(li): #this function will randomly decide on a move to take given a list of possible positions
    import random
    ln = len(li)
    r = random.randrange(0, ln)
    return li[r]

#now, all functions are completed, all needed to do is start the game. If I just wanted to run the game once all I would have to is call main but in this case I want the game to keep running until the user doesnt want to play anymore so I will create a small while loop in the main line. 
while True:
    answer = input('Do you want to play again? (Y/N)')
    if answer.lower() == 'y' or answer.lower == 'yes':
        board = [' ' for x in range(10)]
        print('--------------------------------------')
        main()
    
    else:
        break

    
        
    
    
    
    
    


