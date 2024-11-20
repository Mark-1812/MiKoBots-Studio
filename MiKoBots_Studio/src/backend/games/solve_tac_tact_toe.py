from collections import Counter

class solveTicTacToe():
    def __init__(self):
        self.BOARD_EMPTY = 0
        self.BOARD_PLAYER_X = 1
        self.BOARD_PLAYER_O = -1

    def player(self, board):
        counter = Counter(board)
        x_places = counter[1]
        o_places = counter[-1]

        if x_places + o_places == 9:
            # board is full
            return None
        elif x_places > o_places:
            
            return self.BOARD_PLAYER_O 
        else:
            return self.BOARD_PLAYER_X

    def actions(self, board):
        play = self.player(board)
        actions_list = [(play, i) for i in range(len(board)) if board[i] == self.BOARD_EMPTY]
        return actions_list

    def GetResult(self, board, a):
        (play, index) = a
        board_copy = board.copy()
        board_copy[index] = play
        return board_copy

    def terminal(self, board):
        for i in range(3):
            if board[3 * i] == board[3 * i + 1] == board[3 * i + 2] != self.BOARD_EMPTY:
                return board[3 * i]
            if board[i] == board[i + 3] == board[i + 6] != self.BOARD_EMPTY:
                return board[i]

        if board[0] == board[4] == board[8] != self.BOARD_EMPTY:
            return board[0]
        if board[2] == board[4] == board[6] != self.BOARD_EMPTY:
            return board[2]

        if self.player(board) is None:
            return 0
        
        return None

    def utility(self, board, cost):
        term = self.terminal(board)
        if term is not None:
            return (term, cost)
        
        action_list = self.actions(board)
        utils = []
        for action in action_list:
            new_board = self.GetResult(board, action)
            utils.append(self.utility(new_board, cost + 1))

        score = utils[0][0]
        idx_cost = utils[0][1]
        play = self.player(board)
        
        if play == self.BOARD_PLAYER_X:
            for i in range(len(utils)):
                if utils[i][0] > score:
                    score = utils[i][0]
                    idx_cost = utils[i][1]
                    
        else:
            for i in range(len(utils)):
                if utils[i][0] < score:
                    score = utils[i][0]
                    idx_cost = utils[i][1]
        return (score, idx_cost) 

    def minimax(self, board):
        action_list = self.actions(board)
        utils = []
        for action in action_list:
            new_board = self.GetResult(board, action)
            
            
            utils.append((action, self.utility(new_board, 1)))

        if len(utils) == 0:
            return ((0,0), (0, 0))

        sorted_list = sorted(utils, key=lambda l : l[0][1])
        action = min(sorted_list, key = lambda l : l[1])
        
        return action

    def print_board(self, s):
        def convert(num):
            if num == self.BOARD_PLAYER_X:
                return 'X'
            if num == self.BOARD_PLAYER_O:
                return 'O'
            return '_'

        i = 0
        for _ in range(3):
            for _ in range(3):
                print(convert(s[i]), end=' ')
                i += 1
            print()

if __name__ == '__main__':
    solve = solveTicTacToe()
    
    s = [solve.BOARD_EMPTY for _ in range(9)]
    print('|------- WELCOME TO TIC TAC TOE -----------|')
    print('You are X while the Computer is O')

    while solve.terminal(s) is None:
        play = solve.player(s)
        
        if play == solve.BOARD_PLAYER_X:
            print('\n\nIt is your turn', end='\n\n')
            x = int(input('Enter the x-coordinate [0-2]: '))
            y = int(input('Enter the y-coordinate [0-2]: '))
            index = 3 * x + y
    
            if not s[index] == solve.BOARD_EMPTY: 
                print('That coordinate is already taken. Please try again.')
                continue
    
            s = solve.GetResult(s, (1, index))
            solve.print_board(s)
        else:
            print('\n\nThe is computer is playing its turn')
            action = solve.minimax(s)
            s = solve.GetResult(s, action[0])
            solve.print_board(s)

    winner = solve.utility(s, 1)[0]
    if winner == solve.BOARD_PLAYER_X:
        print("You have won!")
    elif winner == solve.BOARD_PLAYER_O:
        print("You have lost!")
    else:
        print("It's a tie.")
            
            
''''''
