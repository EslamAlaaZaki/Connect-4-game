import copy
import os
                              #####       the board is represented by 2d array     #####
                              #####      the cells may have 1s , -1s, or 0s        #####
                              #####  1s for computer and -1s for user 0s for empty #####

## NO OF COLUMNS
columns = 7
## NO OF ROWS
rows = 6

### check if the board is full ###
def fullBoard(board):
    for x in range(rows):
        for y in range(columns):
            if board[x][y] == 0:
                return False
    return True

### gets input from user ### user can undo the last move if he press Z or r ###
def GetInput():
    Input=input()
    if Input=="Z" or Input=="z":
        return "z"
    if Input.isdigit():
        return int(Input)
    return -1

### checks if there is winner in this state of the board and return 1 if algorithm wins and -1 if the user wins and 0 if no one wins ###
def Getwinner(board):
    for x in range(rows):
        for y in range(columns):
            if y+3<columns: ### horizontal ###
                if board[x][y] == 1 and board[x][y+1] ==1 and board[x][y+2] == 1 and board[x][y+3] == 1:
                    return 1
                if board[x][y] == -1 and board[x][y+1] == -1 and board[x][y+2] == -1 and board[x][y+3] == -1:
                    return -1
            if x+3<rows: ### vertical ###
                if board[x][y] == 1 and board[x+1][y] ==1 and board[x+2][y] == 1 and board[x+3][y] == 1:
                     return 1
                if board[x][y] == -1 and board[x+1][y] ==-1 and board[x+2][y] ==-1 and board[x+3][y] == -1:
                    return -1
            if x+3<rows and y-3>=0: ### / shape ###
                if board[x][y] == 1 and board[x+1][y-1] ==1 and board[x+2][y-2] ==1 and board[x+3][y-3] == 1:
                    return 1
                if board[x][y] == -1 and board[x+1][y-1] ==-1 and board[x+2][y-2] ==-1 and board[x+3][y-3] ==-1:
                    return -1
            if y+3<columns and x+3<rows: ### \ shape ###
                if board[x][y] ==1 and board[x+1][y+1] ==1 and board[x+2][y+2] == 1 and board[x+3][y+3] == 1:
                    return 1
                if board[x][y] ==-1 and board[x+1][y+1] ==-1 and board[x+2][y+2] ==-1 and board[x+3][y+3] ==-1:
                    return -1
    return 0

### gets all possible next states whether its computer turn or users's  ###
def nextPossibleBoards(board, ComputerTurn):
    coinValue=0
    output=[]
    if ComputerTurn:
        coinValue=1
    else:
         coinValue=-1
    for columnchoice in range(columns):
        state = copy.deepcopy(board)
        if board[0][columnchoice-1] !=0:
            continue
        else:
            i = rows -1
            while(board[i][columnchoice-1] !=0):
                i = i- 1
            state[i][columnchoice-1] = coinValue
            output.append(state)
    return output

### evaluate how good each 4 adjacent cells are ###
def utilityOfSlice(slice):
    
    ### if the 4 cells are empty OR have Xs and Os Return 0 ###
    if slice.count(0) == 0 or slice.count(0) == 4:
        return 0
    
    weight = 0
    
    ### if the 4 cells have no -1s and 3 zeros then increase the weight by 1 ###
    ### if the 4 cells have no  1s and 3 zeros then decrease the weight by 1 ###
    if slice.count(-1) == 0 and slice.count(0) == 3:
        weight += 1
    if slice.count(-1) == 1 and slice.count(0) == 3:
        weight += -1
        
    ### if the 4 cells have no -1s and 2 zeros then increase the weight by 3 ###
    ### if 2 consecutive cells are 1s then increase the weight by 2 ###
    if slice.count(-1) == 0 and slice.count(0) == 2:
        weight += 3
        if (slice[0] == 1 and slice[1] == 1) or (slice[1] == 1 and slice[2] == 1) or (slice[2] == 1 and slice[3] == 1):
            weight += 2
            
    ### if the 4 cells have no  -1s and 2 zeros then decrease the weight by 3 ###
    ### if 2 consecutive cells are -1s then decrease the weight by 2 ###
    if slice.count(-1) == 2 and slice.count(0) == 2:
        weight += -3
        if (slice[0] == -1 and slice[1] == -1) or (slice[1] == -1 and slice[2] == -1) or (
                slice[2] == -1 and slice[3] == -1):
            weight += -2
            
    ### if the 4 cells have no -1s and 1 zero then increase the weight by 10 ###
    ### if 3 consecutive cells are 1s then increase the weight by 5 ###
    if slice.count(-1) == 0 and slice.count(0) == 1:
        weight += 10
        if (slice[0] == 1 and slice[1] == 1 and slice[2] == 1) or (slice[1] == 1 and slice[2] == 1 and slice[3] == 1):
            weight += 5
            
    ### if the 4 cells have no  -1s and 1 zeros then decrease the weight by 10 ###
    ### if 3 consecutive cells are -1s then decrease the weight by 5 ###        
    if slice.count(-1) == 3 and slice.count(0) == 1:
        weight += -10
        if (slice[0] == -1 and slice[1] == -1 and slice[2] == -1) or (
                slice[1] == -1 and slice[2] == -1 and slice[3] == -1):
            weight += -5
            
    return weight


### evaluate how good a certain state is ###
def utility(board):
    weight = 0
    for x in range(rows):
        for y in range(columns):
            if y+3<columns:
                weight+=utilityOfSlice([board[x][y], board[x][y+1], board[x][y+2], board[x][y+3]])
            if x+3<rows:
                weight+=utilityOfSlice([board[x][y], board[x+1][y], board[x+2][y], board[x+3][y]])
            if x+3<rows and y-3>=0:
                weight+=utilityOfSlice([board[x][y], board[x+1][y-1], board[x+2][y-2], board[x+3][y-3]])
            if y+3<columns and x+3<rows:
                weight+=utilityOfSlice([board[x][y], board[x+1][y+1], board[x+2][y+2], board[x+3][y+3]])
    return weight

### Only called in computer's turn ###
### initialize alpha witn -100000000, and beta with 100000000 ###
### depth determines the difficulty level of the game ###
### board is the current state ###
### table is a map with an assigned weight(from utility function) to each state ### 
def alphabeta_algorithm(board, table, depth):
    return MaxState(board,table, -100000000, 100000000, depth)

### called at maximum nodes ###
### return the max weight of its children ###
def MaxState(board,table, alpha, beta, depth):
    if Getwinner(board)==-1:
        return -10000
    elif fullBoard(board) is True:
        return 0
    elif depth == 0:
        return utility(board)
    v = -100000000
    statesArray =nextPossibleBoards(board,True)
    for item in statesArray:
        v = max(v, MinState(item,table, alpha, beta, depth - 1))
        if v>= beta: 
            return v
        alpha = max(alpha, v)
    return v

### called at minimum nodes ###
### return the min weight of its children ###
def MinState(board, table, alpha, beta, depth):
    if Getwinner(board)==1:
        if depth==(Globaldepth-1):
            table[str(board)] = 10000
        return 10000
    elif fullBoard(board) is True:
        if depth==(Globaldepth-1):
            table[str(board)] =0
        return 0
    elif depth == 0:
        value=utility(board)
        if depth==(Globaldepth-1):
            table[str(board)] = value
        return value
    v = 100000000
    statesArray =nextPossibleBoards(board,False)
    for item in statesArray:
        v = min(v, MaxState(item,table, alpha, beta, depth - 1))
        if v<= alpha:
            if depth==(Globaldepth-1):
                table[str(board)] =v
            return v
        beta = min(beta, v)
    if depth==(Globaldepth-1):
            table[str(board)] = v
    return v

def insertcoin(board):
    print("In which column would player2 like to insert coin?(Any value between 1-7) OR Press Z to Undo")
    while True:
        columnchoice = GetInput()
        if columnchoice=="z":
            return True
        elif (columnchoice <1 or columnchoice >columns):
            print("Invalid input. Enter new input: ")
        elif board[0][columnchoice-1] !=0:
            print("Invalid input. Enter new input: ")
        else:
            break
    i = rows -1
    while(board[i][columnchoice-1] !=0):
        i = i- 1
    board[i][columnchoice-1] = -1
    return False

def printBoard(board):
    os.system('cls')
    print("")
    for x in range(rows):
        for y in range(columns):
            if board[x][y]==1:
                print("| O ",end="")
            elif board[x][y]==-1:
                print("| X ",end="")
            else:
                print("|   ",end="")
        print("|")
    print("")
    for i in range(columns):
            print("| "+str(i+1)+" ",end="")
    print("|")
    print("\nYou are 'X' and Computer is 'O'\n")

def main():
    BoardHistroies = []  # for redo option
    result = 0
    ## DIFFICULTY OF THE GAME
    print("Choose The Level of difficulty : \n1 Easy \n2 Medium \n3 Hard")
    difficulty = GetInput()
    if difficulty == 1:
        depth = 1
    elif difficulty == 2:
        depth = 2
    elif difficulty == 3:
        depth = 4
    else:
        depth = 2
    global Globaldepth
    Globaldepth=depth
    board = [[0 for y in range(columns)] for x in range(rows)]

    ##Whom to start First
    print("Whom do You wanna start the Game : \n1 You \n2 Computer")
    starter = GetInput()
    if starter == 1:
        ComputerTurn = False
        BoardHistroies.append(copy.deepcopy(board))
        printBoard(board)
    else:
        ComputerTurn = True

    while result == 0 and fullBoard(board) is False:
        table = {}
        if ComputerTurn:
            bestState=[]
            alphabeta_algorithm(board,table, depth)
            statesArray =nextPossibleBoards(board,True)
            score = -100000000000
            for item in statesArray:
                x = str(item)
                if x in table:
                    if table[x] > score:
                        score = table[x]
                        bestState= item
            board = bestState
            printBoard(board)
            BoardHistroies.append(copy.deepcopy(board))
        else:
            Redo = insertcoin(board)
            if Redo:
                if len(BoardHistroies) == 1:
                    board = copy.deepcopy(BoardHistroies[0])
                else:
                    del BoardHistroies[len(BoardHistroies) - 1]
                    board = copy.deepcopy(BoardHistroies[len(BoardHistroies) - 1])
                ComputerTurn = not ComputerTurn
                printBoard(board)
        result = Getwinner(board)
        ComputerTurn = not ComputerTurn

    if result == -1:
        printBoard(board)
        print("You Won")
    elif result == 1:
        print("You Lost")
    else:
        print("Finished")

    print("Press 0 to try again , 1 to finish ")
    try_again = GetInput()
    if try_again == 0:
        main()
if __name__ == '__main__':
    main()