from models.Sudoku import Sudoku
from models.solver import *

def main():

    sudoku = Sudoku()
    #TODO: Ajouter la création et la gestion du sudoku
    # ...

    if ac3(sudoku):
        if sudoku.solved():
            #TODO: afficher le sudoku résolu

        else:
            assignment = {}

            for x in sudoku.squares:
                if len(sudoku.possibilities[x] == 1):
                    assignment[x] = sudoku.possibilities[x][0]

            assignment = backtracking(assignment, sudoku)

            for possibility in sudoku.possibilities:
                #TODO: vérifier conformité de ce if
                if len(possibility) > 1:
                    sudoku.possibilities[possibility] = assignment[possibility]

            if assignment:
                #TODO: afficher le sudoku à cette étape
            else:
                print("There is no solution")



if __name__ == '__main__':
    main()