import copy

EMPTY = 0
BLACK = 1
WHITE = -1

DIRECTIONS = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))

def print_board(board): 
    print(" ",end= " ")
    for i in range(1,9):
        print(i,end= " ")
    print()
    for i in range(8):
        print(i+1,end=" ")
        for j in range(8):
            if board[i][j] == 1:
                print("B",end=" ")
            elif board[i][j] == -1:
                print("W",end=" ")
            else:
                print(".",end=" ")
        print("")
 
def board_init():
    board = [[EMPTY for i in range(8)] for j in range(8)]
    board[3][3] = WHITE
    board[4][4] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    return board

def calculator_score(board):
    score = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0:
                score += board[i][j]
          
    return score

def valid_moves(board, player):
    moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == EMPTY:
                for d in DIRECTIONS:
                    x, y = i + d[0], j + d[1]
                    if (x >= 0 and x < 8)  and   (y >= 0 and y < 8)   and   board[x][y] == -player:
                        x, y = x + d[0], y + d[1]
                        while (x >= 0 and x < 8)  and   (y >= 0 and y < 8)  and   board[x][y] == -player:
                            x, y = x + d[0], y + d[1]

                        if (x >= 0 and x < 8)  and   (y >= 0 and y < 8)  and   board[x][y] == player:
                            moves.append([i, j])
                            break
    return moves

def make_new_state(Board, move,player):
    board = copy.deepcopy(Board)
    board[move[0]][move[1]] = player
    for d in DIRECTIONS:
        x, y = move[0] + d[0], move[1] + d[1]
        if (x >= 0 and x < 8) and (y >= 0 and y < 8) and  (board[x][y] == -player):
            x, y = x + d[0], y + d[1]
            while (x >= 0 and x < 8) and (y >= 0 and y < 8) and  (board[x][y] == -player):
                x, y = x + d[0], y + d[1]
            if (x >= 0 and x < 8) and (y >= 0 and y < 8) and  (board[x][y] == player):
                #find direction's that selected
                x, y = move[0] + d[0], move[1] + d[1]
                while (x >= 0 and x < 8) and (y >= 0 and y < 8) and  (board[x][y] == -player):
                    board[x][y] = player
                    x, y = x + d[0], y + d[1]
    return board


def alpha_beta_pruning(board, depth, alpha, beta,player,maximize):
    valid = copy.deepcopy( valid_moves(board,player) )
    if depth == 0 or valid is None :
        return calculator_score(board), None
    if maximize:
        max_val = float('-inf')
        best_move = None
        for move in valid:
            new_board = copy.deepcopy(make_new_state(board,move,player))
            
            score, _ = alpha_beta_pruning(new_board, depth - 1, alpha, beta, -player,False)
            if score > max_val:
                max_val = score
                best_move = move

            alpha = max(alpha, max_val)
            #pruning
            if beta <= alpha:
                break 
        return max_val, best_move
    else:
        min_val = float('inf')
        best_move = None
        for move in valid:
            new_board = copy.deepcopy(make_new_state(board,move,player))
            score, _ = alpha_beta_pruning(new_board, depth - 1, alpha, beta, -player,True)
            # print(score)
            if score < min_val:
                min_val = score
                best_move = move

            beta = min(beta, min_val)
            if beta <= alpha:
                break
        return min_val, best_move


my_board = board_init()
print("***********************START GAME************************")
print_board(my_board)

# Player1 and 2 play together
for i in range(61):
    print(f"**************round{i+1}************* ")
    if i %2 == 0:
        best_move = copy.deepcopy(alpha_beta_pruning(my_board,4, float("-inf"), float("+inf"), BLACK,True))
        if best_move[1] == None:
            continue
        my_board = copy.deepcopy(make_new_state(my_board, best_move[1],BLACK) )
        print(f"select move  black's plyer :[{best_move[1][0]+1} ,{best_move[1][1]+1}] and score game is {calculator_score(my_board)}")
        print_board(my_board)
    else:
        best_move = copy.deepcopy(alpha_beta_pruning(my_board,2, float("-inf"), float("+inf"), WHITE,False))
        if best_move[1] == None:
            continue
        my_board = copy.deepcopy(make_new_state(my_board, best_move[1],WHITE) )
        print(f"select move  white's plyer :[{best_move[1][0]+1} ,{best_move[1][1]+1}] and score game is {calculator_score(my_board)}")
        print_board(my_board)

    