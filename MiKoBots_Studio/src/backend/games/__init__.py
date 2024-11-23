from backend.games.solve_tac_tact_toe import solveTicTacToe
solve_tic_tac_toe = solveTicTacToe()


def get_result_ttt(board, a):
    result = solve_tic_tac_toe.GetResult(board, a)
    return result
    
def print_board_ttt(board):
    solve_tic_tac_toe.print_board(board)

def minimax_ttt(board):
    result = solve_tic_tac_toe.minimax(board)
    return result

def terminial_ttt(board):
    result = solve_tic_tac_toe.terminal(board)
    return result