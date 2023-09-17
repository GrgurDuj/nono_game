# Nonogram

This project was done as a part of a technical assessment. It comes with 3 pre-loaded nonogram (Picross) puzzles of dimensions 10x10, 15x15 ([Source](https://nonogramskatana.wordpress.com/)) and 13x12 ([Source](https://apps.apple.com/be/app/picture-cross/id977150768)).

## How to play

The user can play the 3 different puzzles by pressing the corresponding puzzle buttons. The point of the puzzle is to fill in the grid with squares using hints that are on the side of the grid. By default the user can make 3 mistakes before they have to start over. The user can help themselves by placing Xs on places they know a square doesn't go. Press LMB to place a square and RMB to place an X.  

## Customizing
The settings.py file has some variables that can change how the game looks and plays.  
Firstly, the user can add custom puzzles. To add more puzzles:  
- create a solution by converting it from an image to a grid of numbers with a whitespace delimeter, for example:
```
0 1 0 0 0
1 1 1 0 0
0 1 0 1 0
0 0 1 1 1
0 0 0 1 0
```
- save the solution into the puzzles folder with the name "puzzle_\<next number in order>.txt"
- in settings.py, adjust the NUMBER_OF_PUZZLES value to however many puzzles are in the "puzzles" folder

Additionally, in settings.py the user can change the font size for the numbers, element colors, line widths and max tries.

## Getting Started

### Dependencies

- matplotlib


### Installing

- either unzip everything into one folder or clone the git repository

### Executing program

- after installing the dependencies run the program wtih
```
python main.py
```

## Authors

Grgur Dujmovic | Email: [grgur.duj@gmail.com](grgur.duj@gmail.com) | [Git](https://github.com/GrgurDuj)

