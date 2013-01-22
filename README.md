Maze_Solver
===========

Python ascii maze solver.

This file takes in a correctly formed rectangular enclosed maze input file using # for walls, 1 for start and 2 for end. If the maze is not solvable the program will call a MazeUnsolvable exception and if the maze is either non-rectangular or not enclosed by #s, it will call a MazeInputError exception. The solve function will attempt to solve the maze object and if it is not solvable, it will call a MazeUnsolvable exception.

An example of a well formed maze:
#######
#1    #
#     #
### ###
#   ###
#     #
##### #
#2    #
#######

An example of a well formed maze without a solution:
#######
#1    #
#     #
### ###
#   ###
#     #
#######
#2    #
#######

This program was written in python by myself and Nick Frosst
