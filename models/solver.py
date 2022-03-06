from Sudoku import Sudoku


def ac3(sudoku):
    # Get the list of all the constraints
    queue = list(sudoku.binary_constraints)

    while queue:
        # Remove the first element of the queue
        x, y = queue.pop(0)

        if remove_inconsistent_values(sudoku, x, y):
            #TODO: Vérifier l'effet de ce if
            if len(sudoku.possibilities[x]) == 0:
                return False

            # Check all the neighbors of the cell and then add them to the queue
            for i in sudoku.neighboring_cells[x]:
                #TODO: vérifier ce if
                if i != x:
                    queue.append([i, x])

    return True


def remove_inconsistent_values(sudoku, x, y):
    removed = False

    #TODO: Changer nom fonction constraint
    for i in sudoku.possibilities[x]:
        if not any([sudoku.constraint(i, j) for j in sudoku.possibilities[y]]):
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
        #TODO: changer nom fonction en isConsistent()
        # If the value is consistent with the assignment we add it
        if sudoku.consistent(assignment, var, value):
            sudoku.assign(var, value, assignment)
            result = backtracking(assignment, sudoku)

            if result:
                return result

            sudoku.unassign(var, assignment)

    return False


# Allow to pick the unassigned variable/square that has the fewest usable values remaining
def select_unassigned_variable(assignment, sudoku):
    unassigned_values = [value for value in sudoku.squares if value not in assignment]

    # Returns the key whose number of possibilities is the lowest
    return min(unassigned_values, key=lambda key: len(sudoku.possibilities[key]))


#TODO: changer description fonction
# Sort the values in order to get those that rules out the fewest possibilities for
# the neighbor squares first
def order_possibilities_values(sudoku, var):
    if len(sudoku.possibilities[var]) == 1:
        return sudoku.possibilities[var]

    #TODO: Changer nom fonction conflicts
    return sorted(sudoku.possibilities[var], key=lambda value: sudoku.conflicts(sudoku, var, value))
