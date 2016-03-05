import sys
sys.setrecursionlimit(4000)


class MazeInputError(Exception):
    '''Exception class for inproperly formed maze related Exceptions.'''
    pass


class  MazeUnsolvable(Exception):
    '''Exception class for unsolvable maze related Exceptions.'''
    pass


class Maze():
    '''Object class for solving mazes.'''

    def __init__(self,file_name):
        '''Initialize a new maze from the file, file_name, and check
        the maze for errors.
        The maze must have a single starting and ending point as well as
        be perfectly rectangular and enclosed by '#'s.
        It may only contain the '1', '2', '#' and ' ' charcters.'''

        self.the_maze = []
        for line in open(file_name):
            new_line = list(line.strip('\n'))  # e.g. split "# #" into ["#", " ", "#"]
            for character in new_line:
                if character not in [' ','#','1','2']:
                    raise MazeInputError('''Illegal character, '%s', in maze.''' % (character))
            self.the_maze.append(new_line)

        self.start = self.find_start()
        self.check_rectangular()

    def check_rectangular(self):
        '''Raise a MazeException if the maze is not rectangular or isn't
        enclosed in #'s.'''
        # This will loop over all the rows in the maze and get their lengths, e.g. [9, 9, 9, 9].
        # Then reduce will loop over that list looking at each value and the one beside it and
        # return -1 if any of them are different.
        # Reduce works by taking a list of items [a, b, c, d, e] and takes a function that takes
        # two values i.e. to add up a list you'd have:
        # result = reduce(lambda total_so_far, item: item + total_so_far, list_of_numbers)
        # if list_of_numbers was [1 ,3 ,4, 9], it would be like:
        # call 1: (1, 3)
        # call 2: (4, 4)
        # call 3: (8, 9)
        # result would be 17
        # In this case, it looks at each number and says, if you are equal then return the same number to
        # be compared against the next one, otherwise return -1.
        if -1 == reduce(lambda val, other_val: val if val == other_val else -1, [len(row) for row in self.the_maze]):
            raise MazeInputError('The input maze is not rectangular.')

        # We take all the characters of the left side of the maze, the right side, the top row and the bottom row
        # and then we filter the list for non `#` characters and if there are any, the maze is malformed.
        # Filter returns a list of items that result in the lambda function being True and (bool([]) == False)
        boundaries = (
            [row[0] for row in self.the_maze] +
            [row[-1] for row in self.the_maze] +
            [col[-1] for col in self.the_maze[0]] +
            [col[-1] for col in self.the_maze[-1]]
        )
        if filter(lambda side: side != "#", boundaries):
            raise MazeInputError('The input maze is not fully exclosed in a rectangle of #s')

    def find_start(self):
        '''Raise MazeException if the maze has too many or not enough
        start or end positions, else return the start coordinates.'''

        start = []
        end = []

        for row_index, row in enumerate(self.the_maze):
            for col_index, col in enumerate(row):
                if col == '1':
                    start.append((row_index, col_index))
                elif col == '2':
                    end.append((row_index, col_index))

        if len(start) == 0:
            raise MazeInputError('There is no start.')
        elif len(start) > 1:
            raise MazeInputError('There are too many start sites.')
        if len(end) == 0:
            raise MazeInputError('There is no end.')
        elif len(end) > 1:
            raise MazeInputError('There are too many end sites.')
        return start[0]

    def print_out(self):
        '''Print maze to screen.'''
        # for each row, convert each of the items to a string and join them togeather for
        # one long string and print that.
        for row in self.the_maze:
            print "".join(str(character) for character in row)

    def solve(self):
        '''
        Solves the maze and marks the path taken, returns True if the maze is solvable
        and raises an exception if not
        '''
        # Check if the maze can be solved from the start spot.
        if not self.is_part_of_route_to_the_exit(column=self.start[1], row=self.start[0]):
            raise MazeUnsolvable('There is no solution to this maze.')
        return True

    def mark_it(self, column, row, mark):
        '''Place the input mark on the current spot (row, column).'''
        if not self.the_maze[row][column] not in ['1', 's']:
            self.the_maze[row][column] = mark
        else:
            # We mark it as an 's' to acknowledge we've seen the start position before
            # and we want to keep it on the map.
            self.the_maze[row][column] = 's'

    def is_part_of_route_to_the_exit(self, column, row):
        '''
        Return True if maze can be solved from position (row, column),
        else return False.
        '''

        current_square = self.the_maze[row][column]
        if current_square == '2':
            return True  #The current square is the exit.
        elif current_square in ['x', '#', '.', 's']
            return False

        # we know at this point he current square is '1', the start position,
        # or ' ' and we can explore.

        #Marks the current spot as traversed.
        self.mark_it(column=column, row=row, mark='.')

        # Try going in each direction and if we can reach the end from any
        # adjacent position then we can solve the maze from our current position.
        if self.is_part_of_route_to_the_exit(column, row - 1):
            return True
        if self.is_part_of_route_to_the_exit(column, row + 1):
            return True
        if self.is_part_of_route_to_the_exit(column - 1, row):
            return True
        if self.is_part_of_route_to_the_exit(column + 1, row):
            return True

        # We tried all adjacent paths and didn't find the exit from here so we should
        # mark the spot as not part of the solution.
        self.mark_it(column=column, row=row, mark='x')
        return False
