from typing import List, Tuple

def determine_hints(solution: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
    """
    Determines the hints for each row and column in the Nonogram grid based on the solution.

    Args:
        solution (List[List[int]]): The solution grid for the Nonogram puzzle.

    Returns:
        Tuple[List[List[int]], List[List[int]]]: A tuple containing the column hints and row hints respectively.
    """

    row_hints = []
    column_hints = []
    # Determine column hints
    for col in range(len(solution[0])):
        col_hint = []
        count = 0
        for row in range(len(solution)):
            if solution[row][col] == 1:
                count += 1
            elif count > 0:
                col_hint.append(count)
                count = 0
        if count > 0:
            col_hint.append(count)
        column_hints.append(col_hint)

    # Determine row hints
    for row in solution:
        row_hint = []
        count = 0
        for square in row:
            if square == 1:
                count += 1
            elif count > 0:
                row_hint.append(count)
                count = 0
        if count > 0:
            row_hint.append(count)
        row_hints.append(row_hint)
    return (column_hints, row_hints)
    
def get_solution(puzzle_number=1) -> List[List[int]]:
    """
    Retrieves the solution grid for the Nonogram puzzle from a file.
    Make sure the name of the saved puzzle file is in the format "puzzle_<puzzle_number>".

    Args:
        puzzle_number (int): The number of the puzzle to parse. Defaults to 1.

    Returns:
        List[List[int]]: The solution grid for the Nonogram puzzle.
    """
    solution = []
    with open("puzzles/puzzle_" + str(puzzle_number) + ".txt", "r", encoding="utf-8") as file:
        for line in file:
            row = [int(x.strip()) for x in line.split(" ")]
            solution.append(row)
    return solution
