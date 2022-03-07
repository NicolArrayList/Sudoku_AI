import copy
from models.sudoku import Sudoku
from models.solver import *


class SudokuGenerator:
    def __init__(self):
        self.sudoku = Sudoku(["0"] * 81)

    def create_solved_sudoku(self):
        self.sudoku = solve(self.sudoku)

    def check_multiple_solution(self, sudoku):
        for possibilities in sudoku.possibilities.values():
            if len(possibilities) > 1:
                return True
        return False

    def remove_values(self):
        """
        We remove at least 5 values and at most 17 because
        all sudokus with more than 17 empty squares have necessarily more than
        1 solution
        """
        number_of_removed = random.randint(12, 17)


        solving_test = copy.deepcopy(self.sudoku)
        # Update solving_test grid values
        for index, val in enumerate(self.sudoku.possibilities.values()):
            solving_test.grid[index] = val[0]

        while number_of_removed > 0:
            # Choose a random square to remove and regenerate possibilities
            removed_number = random.randint(0, 80)
            solving_test.grid[removed_number] = "0"
            solving_test.generate_possibilities()

            # Try to solve solving_test and see the result
            solved = solve(copy.deepcopy(solving_test))

            # Update grid values in solved to display
            for index, val in enumerate(solved.possibilities.values()):
                solved.grid[index] = val

            if self.check_multiple_solution(solved):
                return self.sudoku
            else:
                self.sudoku = solving_test

            number_of_removed -= 1

    def generate_sudoku(self):
        self.create_solved_sudoku()
        self.remove_values()
        return self.sudoku
