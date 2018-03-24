## TIC-TAC-TOE with RL ##

NUM_GAMES = 1000
'''
Opponents: [RandomPlayer, BetterAI, RLAgent, HumanPlayer]
'''
OPPONENT_INDEX = 3  # 0-3

import random
import json
try:
    import matplotlib.pyplot as plt
    has_pyplot = True
except ImportError: has_pyplot = False

class TTTGame():
    
    def __init__(self, playerX, playerO, load_x_state = False):
        self.second_mark = "O"
        if playerX != RLAgent: load_x_state = False
        self.playerX = playerX(self, "X", load_x_state)
        self.playerO = playerO(self, "O")
        self.winners = []
    
    def new_game(self):
        self.board = self.make_empty_board()
        self.playerX.board = self.board
        self.playerO.board = self.board
        self.second_mark = self.get_other_mark(self.second_mark)
        self.new_turn(self.board, self.second_mark)
    
    def put_in_board(self, board, mark, square_num):
        board_row = (square_num - 1) // 3
        board_col = (square_num - 1) % 3
        if [board_row, board_col] in get_free_squares(board):
            board[board_row][board_col] = mark
        else:
            return False
    
    def new_turn(self, board, last_mark):
        mark = self.get_other_mark(last_mark)
        prompt = "Enter your move ("+mark+"):"
        if mark == "O":
            move = self.playerO.move(self.board)
        if mark == "X":
            move = self.playerX.move(self.board)
        i, j = move
        board[i][j] = mark
        if self.is_win(board, mark):
            # self.print_board_and_legend(board)
            if mark == "X":
                self.winners.append("X")
                self.playerX.get_reward(1)
                self.playerO.get_reward(-1)
            else:
                self.winners.append("O")
                self.playerO.get_reward(1)
                self.playerX.get_reward(-1)
            return
        if self.get_free_squares(board) == []:
            self.winners.append(" ")
            self.playerO.get_reward(-0)
            self.playerX.get_reward(-0)
            # self.print_board_and_legend(board)
            return
        self.new_turn(board, mark)
            
    def is_win(self, board, mark):
        for ind in range(3):
            if self.is_row_all_marks(board, ind, mark):
                return True
            if self.is_col_all_marks(board, ind, mark):
                return True
        if self.is_diags_all_marks(board, mark):
            return True
        return False
    
    def is_row_all_marks(self, board, row_i, mark):
        for col in range(3):
            if board[row_i][col] != mark:
                return False
        return True
    
    def is_col_all_marks(self, board, col_i, mark):
        for row in range(3):
            if board[row][col_i] != mark:
                return False
        return True
    
    def is_diags_all_marks(self, board, mark):
        if board[1][1] != mark:
            return False
        if board[0][0] == mark and board[2][2] == mark:
            return True
        if board[2][0] == mark and board[0][2] == mark:
            return True
        return False
    
    
    def get_free_squares(self, board):
        empty_squares=[]
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    empty_squares.append([i,j])
        return empty_squares
        
    def get_other_mark(self, mark):
        if mark == "X":
            return "O"
        else:
            return "X"
        
    def make_empty_board(self):
        board = []
        for i in range(3):
            board.append([" "]*3)
        return board

class TicTacToePlayer():
    def __init__(self, game, mark, load = False):
        self.mark = mark
        self.game = game
        
    def move(self, board):
        pass
    def get_reward(self, reward):
        pass

class RandomPlayer(TicTacToePlayer):    # Makes a random choice from available moves.
    
    def __init__(self, game, mark, load = False):
        TicTacToePlayer.__init__(self, game, mark)
    
    def move(self, board):
        mvs = self.game.get_free_squares(board)
        
        a=mvs[int(len(mvs)*random.random())]
        return a
        
class HumanPlayer(TicTacToePlayer):     # Your turn!
    
    def __init__(self, game, mark, load = False):
        TicTacToePlayer.__init__(self, game, mark)
    
    def move(self, board):
        self.print_board_and_legend(board)
        move = 0
        while move not in self.game.get_free_squares(board):
            mv = int(input("Select a square [0-8]   "))
            move = [mv//3, mv%3]
        return move
        
    def print_board_and_legend(self, board):
        for i in range(3):
            line1 = " " +  board[i][0] + " | " + board[i][1] + " | " +  board[i][2]
            line2 = " " + str(i*3)   + " | " + str(i*3+1)  + " | " + str(i*3+2)
            print(line1+ " "*6 +line2)
            if i < 2:
                print("---+---+---" + " "*5 + "---+---+---")
    
    def get_reward(self, reward):
        if reward == 1:
            print("YOU WIN!!")
        elif reward == -1:
            print("YOU LOSE!! :(")
        else:
            print("DRAW")
        self.print_board_and_legend(self.game.board)

class BetterAI(TicTacToePlayer):        # WILL NEVER LOSE. The perfect TTT player.
    
    def __init__(self, game, mark, load = False):
        TicTacToePlayer.__init__(self, game, mark)
    
    def move(self, board):
        mark = self.mark
        other_mark = self.game.get_other_mark(mark)
        free_squares = self.game.get_free_squares(board)
        for x in range(len(free_squares)):
            a=free_squares[x]
            i=a[0]
            j=a[1]
            board[i][j]=mark
            if self.game.is_win(board, mark) == True:
                board[i][j] = " "
                return a
            else:
                board[i][j] = " "
        for x in range(len(free_squares)):
            a=free_squares[x]
            i=a[0]
            j=a[1]
            board[i][j]=other_mark
            if self.game.is_win(board, other_mark) == True:
                board[i][j] = " "
                return a
            else:
                board[i][j] = " "
        if len(free_squares)==8 or (len(free_squares)==6 \
            and [1, 1] not in free_squares):
                if ([0,1] not in free_squares or [1,0] not\
                    in free_squares) and [0, 0] in free_squares:
                        return [0,0]
                elif ([2,1] not in free_squares or [1,2] not\
                    in free_squares) and [2, 2] in free_squares:
                        return[2,2]
        if [1, 1] in free_squares:
            return [1,1]
        else:
            if board[0][0] == other_mark and\
                board[2][2] == other_mark and len(free_squares)==6:
                    return [0,1]
            elif board[0][2] == other_mark and\
                board[2][0] == other_mark and len(free_squares)==6:
                    return [0,1]
            elif [1,1] not in free_squares and\
                (len(free_squares) > 5 and len(free_squares) < 9):
                    if [0,0] in free_squares:
                        return [0,0]
                    elif [2,0] in free_squares:
                        return [2,0]
                    elif [0,2] in free_squares:
                        return [0,2]
                    elif [2,2] in free_squares:
                        return [2,2]
        return free_squares[random.randint(0,len(free_squares)-1)]
    
class RLAgent(TicTacToePlayer):
    
    valueTable = {}
    alpha = 0.5
    back = 1
    eps = 1
    eps_slope = 1e-5
    min_eps = 0.000
    prev_states = []
    
    def __init__(self, game, mark, load = False):
        TicTacToePlayer.__init__(self, game, mark)
        # if mark == "O":
        #     self.min_eps = 0.1
        #     self.eps_slope = 1e-3
        if load:
            self.read_state()
        
    def check_model(self, move):
        '''Return the board after a given move is made. Assume move is legal.'''
        #deep copy the board.
        brd = [[],[],[]]
        for i in range(3):
            for j in range(3):
                brd[i].append(self.board[i][j])
        #get new board with move
        i, j = move
        brd[i][j] = self.mark
        return brd
    
    def update_table(self, prev_states, reward):
        add = reward
        for s in prev_states:
            try:
                self.valueTable[s] += self.alpha*(add-self.valueTable[s])
            except KeyError:
                self.valueTable[s] = add
            add = self.back * add
        # Normalize
        '''
        max = 0
        for val in self.valueTable.values():
            if abs(val) > max:
                max = abs(val)
        if max > 0:
            for s, val in self.valueTable.items():
                self.valueTable[s] = val/max
        '''
    
    def get_reward(self, reward):
        self.update_table(self.prev_states, reward)
        self.prev_states = []
    
    def take_turn(self, board):
        moves = self.game.get_free_squares(board)
        if random.random() < self.eps:
            move = moves[random.randint(0, len(moves)-1)]
            next_brd = self.check_model(move)
        else:
            max = None
            move = 0
            next_brd = 0
            for mv in moves:
                brd = self.check_model(mv)
                try:
                    val = self.valueTable[self.get_state(brd)]
                except KeyError:
                    self.valueTable[self.get_state(brd)] = val = 0
                if max != None:
                    if val <= max:
                        continue
                max = val
                move = mv
                next_brd = brd
        self.eps -= self.eps_slope
        if self.eps < self.min_eps: self.eps = self.min_eps
        self.prev_states.insert(0,self.get_state(next_brd))
        return move
    
    def move(self, board):
        return self.take_turn(board)
    
    def get_state(self, board):
        state = ""
        for i in range(3):
            for j in range(3):
                mrk = board[i][j]
                if mrk == self.mark:
                    state = state + "+"
                elif mrk == self.game.get_other_mark(self.mark):
                    state = state + "-"
                else: state = state + " "
        return state
    
    def save_state(self):
        with open('RLstate.txt', 'w') as f:
            f.write(json.dumps([self.valueTable, [self.eps, self.min_eps]]))
    
    def read_state(self):
        with open('RLstate.txt', 'r') as f:
            [self.valueTable, [self.eps, self.min_eps]] = json.loads(f.readline())
        

def sort_by_val(dict):
    '''Return list of pairs: state, val, sorted by val'''
    lis = []
    for k, v in dict.items():
        inserted = False
        for i in range(len(lis)):
            if v > lis[i][1]:
                lis.insert(i, [k, v])
                inserted = True
                break
        if not inserted:
            lis.append([k,v])
    return lis

def count(list, value):
    val = 0 
    for v in list:
        if v == value:
            val += 1
    return val

def train():
    again = "Y"
    trials = 0
    while again == "Y":
        trials += 1
        num_games = NUM_GAMES
        games_played = 0
        xwins = 0
        owins = 0
        draws = 0
        points = []
        losses = []
        draw = []
        while games_played < num_games:
            ttt.new_game()
            games_played += 1
            dt = 1000
            winner = ttt.winners[-dt:]
            xwins = count(winner, "X")
            owins = count(winner, "O")
            draws = count(winner, " ")
            points.append(xwins/min(games_played,dt))
            draw.append(draws/min(games_played,dt))
            losses.append(owins/min(games_played,dt))
            if games_played % 1000 == 0:
                print("%d games played of %d" %(games_played, num_games))
        if has_pyplot:
            lis = range(1, games_played+1)
            plt.plot(lis, points, lis, losses, lis, draw)
            plt.legend(["Wins", "Losses", "Draws"], loc = 0)
            plt.title("Trial "+str(trials))
            plt.ylabel("Ratio of wins in last "+str(dt))
            plt.ylim([0,1])
            plt.xlabel("Episodes")
            plt.show()
        ttt.playerX.save_state()
        again = input("Train again? Y/N  ")
    # print(sort_by_val(ttt.playerX.valueTable))
    again = input("Would you like to test? Y/N   ")
    if again == "Y":
        ttt.playerX.eps = 0.00
        ttt.playerX.min_eps = 0.0
        ttt.playerO = HumanPlayer(ttt, "O")
        while again == "Y":
            if again == "R":
                ttt.playerO = RandomPlayer(ttt, "O")
            elif again == "H":
                ttt.playerO = HumanPlayer(ttt, "O")
            ttt.new_game()
            again = input("Play again? Y/N   ")
    again = input("Train more? Y/N   ")
    if again == "Y":
        ttt.playerX.read_state()
        ttt.playerO = opponents[OPPONENT_INDEX](ttt, "O")
        train()
        return

if __name__ == "__main__":
    
    opponents = [RandomPlayer, BetterAI, RLAgent, HumanPlayer]
    opp = ["0: Random", "1: Perfect", "2: Learning", "3: Human"]
    for obj in opp:
        print(obj)
    ans = input("Pick an opponent by index from the options above. [0-3]    ")
    try:
        ans = int(ans)
        if ans >= 0 and ans <= 3:
            OPPONENT_INDEX = ans
    except Exception: pass
    ans = input("How many games would you like to play?    ")
    try:
        NUM_GAMES = int(ans)
    except Exception: pass
    loadx = input("Load state? Y/N   ")
    loadx = (loadx == "Y")
    playerX = RLAgent
    playerO = opponents[OPPONENT_INDEX]
    ttt = TTTGame(playerX, playerO, loadx)
    train()