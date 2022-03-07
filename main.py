from models.sudoku import Sudoku
from models.solver import *


def text_to_grid():
    f = open("examples/tranquille_sudoku_example.txt", "r")

    tab = []

    for i in range(0, 9):
        line = f.readline()
        for j in range(0, 9):
            tab.append(line[j])

    return tab


def main():
    sudoku = Sudoku(text_to_grid())
    # TODO: Ajouter la création et la gestion du sudoku
    # ...

    if ac3(sudoku):
        if sudoku.is_solved():
            print(sudoku)
        else:
            assignment = {}

            for x in sudoku.squares:
                if len(sudoku.possibilities[x]) == 1:
                    assignment[x] = sudoku.possibilities[x][0]

            assignment = backtracking(assignment, sudoku)

            for possibility in sudoku.possibilities:
                # TODO: vérifier conformité de ce if
                if len(possibility) > 1:
                    sudoku.possibilities[possibility] = assignment[possibility]

            if assignment:
                # TODO: afficher le sudoku à cette étape
                print(sudoku)
            else:
                print("There is no solution")


if __name__ == '__main__':
    main()
