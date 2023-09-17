import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from settings import FONT_SIZE, LINE_COLOR, MAX_TRIES, NUMBER_OF_PUZZLES, SQUARE_COLOR, X_COLOR
from utils import determine_hints, get_solution


class Nonogram:
    """
    A class representing a nonogram puzzle.

    This class provides the functionality to play the nonogram puzzle. It includes methods for drawing the game grid,
    handling click events, restarting the game, checking the game state, and loading new puzzles.

    Attributes:
        solution (List[List[int]]):     The solution grid for the Nonogram puzzle.
        n_columns (int):                The number of columns in the Nonogram grid.
        n_rows (int):                   The number of rows in the Nonogram grid.
        grid (List[List[str]]):         The current state of the Nonogram grid.
        column_hints (List[List[int]]): The hints for each column in the Nonogram grid.
        row_hints (List[List[int]]):    The hints for each row in the Nonogram grid.
        root_window (tk.Tk):            The root window of the Nonogram game.
        tries_left (int):               The number of tries left in the game.
        tries_left_frame (tk.Frame):    The frame for the lives counter.
        tries_label (tk.Label):         The label for displaying the number of tries left.
        game_frame (tk.Frame):          The frame for the Nonogram grid.
        fig (Figure):                   The figure for the Nonogram grid.
        subplot (matplotlib.axes.Axes): The subplot for the Nonogram grid.
        canvas (FigureCanvasTkAgg):     The canvas for displaying the Nonogram grid.

    Methods:
        draw():                     Draws the Nonogram grid based on the current state of the game.
        on_click(event):            Handles the click event on the Nonogram grid.
        restart_game():             Restarts the game by resetting the grid, tries left, determining hints, and redrawing the grid.
        check_state():              Checks if the current state of the grid matches the solution.
        load_puzzle(puzzle_number): Loads a new puzzle from the puzzles folder based on the given puzzle number.

    """
    def __init__(self):
        # Initialize variables needed for game logic
        self.solution = get_solution()
        self.n_columns = len(self.solution[0])
        self.n_rows = len(self.solution)
        self.grid = [["0" for _ in range(self.n_columns)] for _ in range(self.n_rows)]
        self.column_hints, self.row_hints = determine_hints(self.solution)

        # Initialize root window
        self.root_window = tk.Tk()
        self.root_window.title("Nonogram")

        # Create a frame for the lives counter
        self.tries_left = MAX_TRIES
        self.tries_left_frame = tk.Frame(self.root_window)
        self.tries_left_frame.pack(side="top", pady=10)
        self.tries_label = tk.Label(self.tries_left_frame, text="Tries left: " + str(self.tries_left))
        self.tries_label.pack(side="left")

        # Create a frame for the nonogram grid and draw it
        self.game_frame = tk.Frame(self.root_window)
        self.game_frame.pack(side="top")
        self.fig = Figure()
        self.subplot = self.fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.game_frame)
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.canvas.get_tk_widget().pack(side="right")
        self.draw()

        # Create a frame for buttons that allow you to choose different puzzles
        self.button_frame = tk.Frame(self.root_window)
        self.button_frame.pack(side="bottom", padx=5)

        for i in range(1, NUMBER_OF_PUZZLES + 1):
            button = tk.Button(self.button_frame, text=f"Puzzle {i}", command=lambda n=i: self.load_puzzle(n))
            button.pack(side="left", pady=5)

        tk.mainloop()

    def draw(self) -> None:
        """
        Draws the nonogram grid based on the current state of the game.

        This function clears the subplot, sets the axis properties, fills in the grid cells,
        draws the grid lines, and displays the hints.

        Returns:
            None
        """
        self.subplot.clear()
        self.subplot.axis("equal")
        self.subplot.axis("off")
        self.subplot.set_aspect("equal", adjustable="box")

        # Fill in the grid based on existing data
        for i in range(self.n_rows):
            for j in range(self.n_columns):
                if self.grid[i][j] == "1":
                    self.subplot.fill([j, j, j + 1, j + 1], [i, i + 1, i + 1, i], SQUARE_COLOR)
                elif self.grid[i][j] == "x":
                    self.subplot.plot([j, j + 1], [i, i + 1], X_COLOR)
                    self.subplot.plot([j, j + 1], [i + 1, i], X_COLOR)

        # Draw the grid
        for i in range(0, self.n_rows + 1):
            self.subplot.axhline(i, color=LINE_COLOR, linewidth=1)
        for i in range(self.n_rows, 0, -5):
            self.subplot.axhline(i, color=LINE_COLOR, linewidth=2)
        for i in range(self.n_columns + 1):
            self.subplot.axvline(i, color=LINE_COLOR, linewidth=1)
            if i % 5 == 0:
                self.subplot.axvline(i, color=LINE_COLOR, linewidth=2)

        # Determine size for hint fields, and move the plot limits so the hints are visible
        max_hints_column = max(len(line) for line in self.column_hints)
        max_hints_row = max(len(line) for line in self.row_hints)

        self.subplot.set_xlim(-max_hints_row, self.n_columns)
        self.subplot.set_ylim(0, self.n_rows + max_hints_column)

        # Write in the column hints
        for column_number, column_hint in enumerate(self.column_hints):
            for hint_number, hint in enumerate(reversed(column_hint)):
                self.subplot.text(0.35 + column_number, self.n_rows + 0.25 + hint_number, hint, fontsize=FONT_SIZE)

        # Write in the row hints
        for row_number, row_hint in enumerate(reversed(self.row_hints)):
            for hint_number, hint in enumerate(reversed(row_hint)):
                self.subplot.text(-0.8 - hint_number, 0.25 + row_number, hint, fontsize=FONT_SIZE)

        self.canvas.draw()

    def on_click(self, event) -> None:
        """
        Handles the click event on the nonogram grid.

        This function determines the button clicked (LMB or RMB), updating the grid based on it,
        and checking the state of the game.

        Args:
            event (matplotlib.backend_bases.MouseEvent): The click event.
        """
        button = event.button
        x, y = int(event.xdata), int(event.ydata)
        if button == 1:  # Left click
            if self.grid[y][x] == "0":
                if self.solution[self.n_rows - y - 1][x] == 1:  # Only mark a cell if it is empty and correct
                    self.grid[y][x] = "1"
                else:                                           # If it is empty and wrong, mark it and remove a try
                    self.grid[y][x] = "x"
                    self.tries_left -= 1
                    self.tries_label.config(text="Tries left: " + str(self.tries_left))
                    if self.tries_left == 0:                    # If it is the last try, game over
                        tk.messagebox.showinfo("Game over", "You are out of tries, the game will now restart.")
                        self.restart_game()
                        return
                    tk.messagebox.showinfo("Mistake", "You made a mistake!")
        elif button == 3:  # Right click
            if self.grid[y][x] == "0":  # Toggle "x"
                self.grid[y][x] = "x"
            elif self.grid[y][x] == "x":
                self.grid[y][x] = "0"
        self.draw()
        if self.check_state():
            tk.messagebox.showinfo("You won!", "Good job! You completed the nonogram! How about another one?")

    def restart_game(self) -> None:
        """
        Restarts the game by resetting the grid, tries left, determining hints and redrawing the grid.
        """
        self.grid = [["0" for _ in range(self.n_columns)] for _ in range(self.n_rows)]
        self.tries_left = MAX_TRIES
        self.tries_label.config(text="Tries left: " + str(self.tries_left))
        self.column_hints, self.row_hints = determine_hints(self.solution)
        self.draw()

    def check_state(self) -> bool:
        """
        Checks if the current state of the grid matches the solution.

        Returns:
            bool: True if the grid matches the solution, False otherwise.
        """
        for i in range(self.n_rows):
            for j in range(self.n_columns):
                if self.solution[self.n_rows - i - 1][j] == 1:
                    if self.grid[i][j] != "1":
                        return False
        return True

    def load_puzzle(self, puzzle_number) -> None:
        """
        Loads a new puzzle from the puzzles folder based on the given puzzle number.
        Make sure the name of the saved puzzle file is in the format "puzzle_<puzzle_number>".

        Args:
            puzzle_number (int): The number of the puzzle to load.

        Raises:
            FileNotFoundError: If the puzzle file is not found.
        """
        try:
            self.solution = get_solution(puzzle_number)
            self.n_columns = len(self.solution[0])
            self.n_rows = len(self.solution)
            self.restart_game()
        except FileNotFoundError:
            tk.messagebox.showerror("Error", "Puzzle file not found.")
