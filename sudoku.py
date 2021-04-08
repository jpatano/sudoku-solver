import csv
import random
from pprint import pprint
import copy


boards = 'sample_sudoku_board_inputs.csv'


class SudokuSolver:
    def __init__(self, board_string=None):
        """if not board string is provided, a random game will be chosen from csv"""
        self.board_string = board_string
        self.solved = False
        self.formatted_list = self._format_list(self.board_string)
        self.board = None
        # self.recursion_counter = 0

    def _select_random_game(self):
        """select a random game from given csv file"""
        try:
            with open(boards) as raw_boards:
                csv_reader = csv.reader(raw_boards)
                games = []
                for row in csv_reader:
                    games.append(row)
                return random.choice(games)[0]
        except:
            return False

    def _format_list(self, board_string=None):
        """format the raw string into a list"""
        formatted_list = []
        # if no board string is specified choose a random one from a csv file
        if not board_string:
            raw_board = self._select_random_game()
            if not raw_board:
                return "No csv provided or file could not be read"
        else:
            raw_board = self.board_string
        # split the string up into chunks of 9 by slicing the list every 9th element
        for i in range(len(raw_board)):
            if i % 9 == 0 and i > 0:
                formatted_list.append(list(raw_board[i-9:i]))
        formatted_list.append(list(raw_board[i-8:i + 1]))
        return formatted_list

    def _identify_numbers(self, x, y):
        """identify the possible numbers that can fill a given location"""
        # index will by [x, y]
        x, y = int(x), int(y)
        # bad_nums will store unique values of everything that our number can NOT be
        bad_nums = set()
        # check row for numbers
        for num in self.formatted_list[y]:
            if num != '0':
                bad_nums.add(num)
                # check column for numbers
        for row in self.formatted_list:
            if row[x] != '0':
                bad_nums.add(row[x])
        # check square for numbers
        # (x // 3) * 3 allows us to select the square containing the row of this index
        # (y // 3) * 3 allows us to select the column containing the row of this index
        row_square = (x // 3) * 3
        col_square = (y // 3) * 3
        # iterate through each square and check for "bad nums"
        for row in range(col_square, col_square + 3):
            for num in range(row_square, row_square + 3):
                # if the number at the selected index is not "0" add it to bad_nums
                if self.formatted_list[row][num] != '0':
                    bad_nums.add(self.formatted_list[row][num])
        # return the stringified index for every number that is not in bad_nums
        return [str(i) for i in range(1, 10) if str(i) not in bad_nums]

    def _format_board(self):
        """function for formating and displaying the board to the user"""
        master_string = ''
        for i, row in enumerate(self.formatted_list):
            # set a string pf "-" for the top border, and bottom of each square
            # Using % 3 splits the sections up into rows of 3
            if i % 3 == 0:
                master_string += f"{'-' * 22}\n"
            row_string = ''
            for j, num in enumerate(row):
                if j % 3 == 0 and j > 0:
                    # add a vertical line after ever 3rd character
                    row_string += ' |'
                row_string += f' {num}'
            master_string += f'{row_string}\n'
        master_string += f"{'-' * 22}\n"
        return master_string

        #------------------End of Private Methods----------------------#

    def solve(self):
        """solves the sudoku using recursion"""
        # self.recursion_counter += 1  <----- fun to see the recursion count
        for row, row_val in enumerate(self.formatted_list):
            for col, col_val in enumerate(row_val):
                # if the value of the current index (column in row) is 0 solve it
                if col_val == '0':
                    choices = self._identify_numbers(col, row)
                    # for each possible choice that was identified, try to fill in current index with possible choice
                    for num in choices:
                        # set the corresponding value to each number
                        self.formatted_list[row][col] = num
                        if row == 8 and col == 8:
                            # if you reach the end, set the solved flag to True.  This prevents
                            # the program from continuing and un-solving itself
                            self.solved = True
                        # if not at the end, recurse into the next iteration
                        self.solve()
                        # if self.solved == true return the formated solved board, else replace the index with '0
                        if self.solved == True:
                            self.board = self._format_board()
                            return
                        else:
                            self.formatted_list[row][col] = '0'
                    return
                # if the index is not a '0' and it is the final index, set self.solved to True
                else:
                    if row == 8 and col == 8:
                        self.solved = True
                        self.board = self._format_board()
                        return


new_game = SudokuSolver(
    '500400060009000800640020000000001008208000501700500000000090084003000600060003002')
print(new_game.board)
print(new_game.solve())
print(new_game.board)

# <------------check out all the recursion amounts per board----------------->

# games = []
# with open(boards) as raw_boards:
#     csv_reader = csv.reader(raw_boards)
#     for row in csv_reader:
#         games.append(row)

# for i, game in enumerate(games):

#     loop_instance = SudokuSolver(game[0])
#     loop_instance.solve()
#     print(i, ' ', game)
#     print('recursion count: ', loop_instance.recursion_counter)
