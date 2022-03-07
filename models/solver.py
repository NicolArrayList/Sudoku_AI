from models.sudoku import *


def ac3(sudoku):
    # Get the list of all the constraints
    queue = list(sudoku.binary_constraints)

    while queue:
        # Remove the first element of the queue
        x, y = queue.pop(0)

        if remove_inconsistent_values(sudoku, x, y):
            if len(sudoku.possibilities[x]) == 0:
                return False

            # Check all the neighbors of the cell and then add them to the queue
            for i in sudoku.neighboring_cells[x]:
                if i != x:
                    queue.append([i, x])

    return True


def remove_inconsistent_values(sudoku, x, y):
    removed = False

    for i in sudoku.possibilities[x]:
        if not any([i != j for j in sudoku.possibilities[y]]):
            sudoku.possibilities[x].remove(i)
            removed = True

    return removed


def backtracking(assignment, sudoku):
    # Check if the assignment is complete
    if len(assignment) == len(sudoku.squares):
        return assignment

    # Get all the unassigned variables
    var = select_unassigned_variable(assignment, sudoku)

    for value in order_possibilities_values(sudoku, var):
        # If the value is consistent with the assignment we add it
        if sudoku.is_consistent(assignment, var, value):
            assignment[var] = str(value)
            result = backtracking(assignment, sudoku)

            if result:
                return result

            del assignment[var]

    return False


# Allow to pick the unassigned variable/square that has the fewest usable values remaining
def select_unassigned_variable(assignment, sudoku):
    unassigned_values = [value for value in sudoku.squares if value not in assignment]

    # Returns the key whose number of possibilities is the lowest
    return min(unassigned_values, key=lambda key: len(sudoku.possibilities[key]))


# Sort the values in order to get those that rules out the fewest possibilities for
# the neighbor squares first
def order_possibilities_values(sudoku, var):
    if len(sudoku.possibilities[var]) == 1:
        return sudoku.possibilities[var]

    return sorted(sudoku.possibilities[var], key=lambda value: sudoku.number_of_conflicts(var, value))


"""
This function updates the grid used to display the sudoku
"""
def update_grid(sudoku):
    for index, val in enumerate(sudoku.possibilities.values()):
        sudoku.grid[index] = val[0]


def solve(sudoku):
    if not ac3(sudoku):
        print("There is no solution to this specific sudoku...")
        return False
    else:
        # If the ac3 is enough to solve the sudoku, we display it
        if sudoku.is_solved():
            update_grid(sudoku)
            return sudoku
        else:
            assignment = {}

            # We assign all the correct possibilities
            for x in sudoku.squares:
                if len(sudoku.possibilities[x]) == 1:
                    assignment[x] = sudoku.possibilities[x][0]

            assignment = backtracking(assignment, sudoku)

            if not assignment:
                print("An unexpected error occurred sorry...")

            for possibility in sudoku.possibilities:
                if len(possibility) > 1:
                    sudoku.possibilities[possibility] = assignment[possibility]

    update_grid(sudoku)
    return sudoku
