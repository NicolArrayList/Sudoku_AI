from models.solver import *
from models.sudokuGenerator import SudokuGenerator


def text_to_sudoku():
    f = open("examples/hard_sudoku_example.txt", "r")

    tab = []

    for i in range(0, 9):
        line = f.readline()
        for j in range(0, 9):
            tab.append(line[j])

    return tab


def main():
    while True:
        print("---------------------- MENU ----------------------")
        print("1 - Résoudre le sudoku contenu dans le fichier txt")
        print("2 - Résoudre un sudoku généré aléatoirement")
        print("0 - Quitter")
        user_input = input("Entrez le numéro correspondant à votre choix : ")

        if user_input:
            user_input = int(user_input)
            if user_input == 1:
                print("\nSudoku de départ (fichier txt) : ")
                sudoku = Sudoku(text_to_sudoku())
                print(sudoku)

                solved_sudokou = solve(sudoku)
                print("Sudoku résolu :")
                print(solved_sudokou)
            elif user_input == 2:
                sudoku = SudokuGenerator().generate_sudoku()
                print("\nSudoku de départ (généré aléatoirement: ")
                print(sudoku)

                solved_sudoku = solve(sudoku)
                print("Sudoku résolu : ")
                print(solved_sudoku)
            elif user_input == 0:
                exit()
            else:
                print("\nErreur d'entrée\n")
        else:
            print("\nVeuillez entrer une valeur\n")


if __name__ == '__main__':
    main()
