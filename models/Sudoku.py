import itertools
import random

rows = "123456789"
cols = "ABCDEFGHI"


def assign(square, number, assignment):
    assignment[square] = number


def unassign(square, assignment):
    del assignment[square]


class Sudoku:

    def __init__(self, grid):

        if grid is None:
            self.generate_random_grid()
        else:
            self.grid = grid

        self.squares = list()
        self.generate_squares()

        self.possibilities = dict()
        self.generate_possibilities()

        self.binary_constraints = list()
        self.generate_sudoku_constraints_as_binary()

        self.neighboring_cells = dict()
        self.generate_neighboring_square_for_all()

    def generate_squares(self):
        for col in cols:
            for row in rows:
                # add a new square to our square list based on the col and row
                self.squares.append(col + row)

    def generate_possibilities(self):
        for i, square in enumerate(self.squares):
            # if the passed list as a value of 0 for this square then it can be anything between 1 and 9
            if self.grid[i] == "0":
                self.possibilities[square] = list(range(1, 10))
            # else it can only be the passed value
            else:
                self.possibilities[square] = [self.grid[i]]

    def generate_sudoku_constraints_as_binary(self):
        # We will use the list to add
        # - row constraints
        # - column constraints
        # - subSodokuSquare constraints
        not_so_binary_constraints = list()

        # Here we take care of all rows
        for row in rows:
            # This list represents the current row with square coordinates
            # Example for the first row : ['A1', 'B1', 'C1', 'D1', ..., 'I1']
            row_constraints = list()
            for col in cols:
                row_constraints.append(col + row)
            not_so_binary_constraints.append(row_constraints)

        # Here we take care of all columns
        for col in cols:
            # This list represents the current col with square coordinates
            # Example for the first column : ['A1', 'A2', 'A3', 'A4', ..., 'A9']
            col_constraints = list()
            for row in rows:
                col_constraints.append(col + row)
            not_so_binary_constraints.append(col_constraints)

        # Here we take care of sub square of the sodoku's grid
        cols_sub_square = list()
        rows_sub_square = list()

        for i in range(0, 9, 3):
            cols_sub_square.append(cols[i:i + 3])
            rows_sub_square.append(rows[i:i + 3])

        for row in rows_sub_square:
            for col in cols_sub_square:
                sub_square_constraints = list()
                for i in row:
                    for j in col:
                        sub_square_constraints.append(i + j)
                not_so_binary_constraints.append(sub_square_constraints)

        # Now we can make those constraints binary
        # Example : ['A1', 'A2'] or ['A1', 'B1']
        # For that we use a permutation library

        for constraints in not_so_binary_constraints:
            for tuple_of_constraint in itertools.permutations(constraints, 2):
                if list(tuple_of_constraint) not in self.binary_constraints:
                    self.binary_constraints.append(list(tuple_of_constraint))

    """
    This method generates the neighboring square for every square
    """
    def generate_neighboring_square_for_all(self):
        # for each square
        for square in self.squares:
            self.neighboring_cells[square] = list()
            # We go through constraints
            for c in self.binary_constraints:
                # if there is a constraint with our current square
                if square == c[0]:
                    # The other square is a neighbour !
                    self.neighboring_cells[square].append(c[1])

    """
    This method indicates whether a square or cell is consistent. 
    That means the passed square can't have any related square with the same value
    """
    def is_consistent(self, assignment, passed_square, passed_number):
        # Going through the assignment list
        for square, number in assignment.items():
            # if one assignment as the same value then the solution is not consistent
            if (number == passed_number) and (square in self.neighboring_cells[passed_square]):
                return False
        return True

    def __str__(self):

        output = ""
        count = 1

        # for each cell, print its value
        for cell in self.squares:

            # trick to get the right print in case of an AC3-finished sudoku
            value = str(self.possibilities[cell])
            if type(self.possibilities[cell]) == list:
                value = str(self.possibilities[cell][0])

            output += "[" + value + "]"

            # if we reach the end of the line,
            # make a new line on display
            if count >= 9:
                count = 0
                output += "\n"

            count += 1

        return output


