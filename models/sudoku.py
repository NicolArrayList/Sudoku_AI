import itertools
import random

rows = "123456789"
cols = "ABCDEFGHI"


def assign(square, number, assignment):
    assignment[square] = str(number)


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

        self.beurre()

    def generate_squares(self):
        """
        This method generates coordinates for our sudoku's.
        It's fantastic to make constraint in a human-readable way !
        :return: None
        """
        for col in cols:
            for row in rows:
                # add a new square to our square list based on the col and row
                self.squares.append(col + row)

    def generate_possibilities(self):
        """
        This method generates possibilities according to grid
        :return: None
        """
        for i, square in enumerate(self.squares):
            # if the passed list as a value of 0 for this square then it can be anything between 1 and 9
            if self.grid[i] == "0":
                self.possibilities[square] = list(range(1, 10))
            # else it can only be the passed value
            else:
                self.possibilities[square] = [self.grid[i]]

    def generate_sudoku_constraints_as_binary(self):
        """
        This huge method generates constraints and makes them binary
        :return: None
        """
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
                        sub_square_constraints.append(j + i)
                not_so_binary_constraints.append(sub_square_constraints)

        # Now we can make those constraints binary
        # Example : ['A1', 'A2'] or ['A1', 'B1']
        # For that we use a permutation library

        for constraints in not_so_binary_constraints:
            for tuple_of_constraint in itertools.permutations(constraints, 2):
                if list(tuple_of_constraint) not in self.binary_constraints:
                    self.binary_constraints.append(list(tuple_of_constraint))

    def generate_neighboring_square_for_all(self):
        """
        This method generates the neighboring square for every square
        :return: None
        """
        # for each square
        for square in self.squares:
            self.neighboring_cells[square] = list()
            # We go through constraints
            for c in self.binary_constraints:
                # if there is a constraint with our current square
                if square == c[0]:
                    # The other square is a neighbour !
                    self.neighboring_cells[square].append(c[1])

    def number_of_conflicts(self, square, value):
        """
        Calculate the number of conflict in the grid
        :return: int = the number of conflicts in the current grid
        """
        count = 0
        for related_c in self.neighboring_cells[square]:
            if len(self.possibilities[related_c]) > 1 and value in self.possibilities[related_c]:
                count += 1
        return count

    def is_consistent(self, assignment, passed_square, passed_number):
        """
        This method indicates whether a square or cell is consistent.
        That means the passed square can't have any related square with the same value
        :return: bool
        """
        # Going through the assignment list
        passed_number = str(passed_number)
        for square, number in assignment.items():
            # if one assignment as the same value then the solution is not consistent
            if (number == passed_number) and (square in self.neighboring_cells[passed_square]):
                return False
        return True

    def is_solved(self):
        """
        is_solved checks if the current sudoku as only one possibility for each square
        :return: bool
        """
        for v in self.squares:
            if len(self.possibilities[v]) > 1:
                return False
        return True

    # Redefine str method to show the grid
    def __str__(self):
        output = ""
        count = 1

        # for each cell, print its value
        for square in self.squares:

            value = str(self.possibilities[square])

            output += value + ' '

            # New horizontal subSquare line
            if count % 27 == 0 and count != 81:
                output += "\n---------------------\n"
            # New line
            elif count % 9 == 0:
                output += "\n"
            # New vertical subSquare line
            elif count % 3 == 0:
                output += "| "
            count += 1

        return output

    def beurre(self):
        pass
