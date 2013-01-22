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
        The maze must have one start, one end, be rectangular, enclosed by
        '#', consist of only ' 's and '#'s and have no blank lines.'''
        
        new_line = []
        self.the_maze = []
        for line in open(file_name):
            for character in line.strip('\n'):
                if character not in [' ','#','1','2']:
                    raise MazeInputError('''Illegal character, '%s', in maze.'''
                                         % (character))
                new_line.append(character)
            self.the_maze.append(new_line)
            new_line = []
        self.start = self.find_start()
        self.check_rectangular()
        self.file_name = file_name
    
    def check_rectangular(self):
        '''Raise a MazeException if the maze is not rectangular or isn't 
        enclosed in #'s.'''
        
        sides = self.the_maze[0]+self.the_maze[-1]
        total_rows = len(self.the_maze)
        len_of_row = len(self.the_maze[0])
        for i in range(len(self.the_maze)):
            try:
                sides.append(self.the_maze[i][0])
            except Exception:
                raise MazeInputError('Extra blank line on the input file.')
            if len(self.the_maze[i]) != len_of_row:
                raise MazeInputError('The input maze is not rectangular.')
            sides.append(self.the_maze[i][-1])
        for item in sides:
            if item != '#':
                raise MazeInputError('The input maze is not fully exclosed in'
                                    ' a rectangle of #s')
            
    def find_start(self):
        '''Raise MazeException if the maze has too many or not enough 
        start or end positions, else return the start coordinates.'''
        
        row_count = -1
        col_count = 0
        start = []
        end = []
        for row in self.the_maze:
            row_count += 1
            for col in row:
                if col == '1':
                    start.append((row_count, col_count))
                elif col == '2':
                    end.append((row_count, col_count))
                col_count +=1
            col_count = 0
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
        current_line = ''
        for line in self.the_maze:
            for character in line:
                current_line += character
            print current_line
            current_line = ''
            
    def solve(self):
        '''Solves the maze and marks the path taken, returns true if the 
                maze is solvable and False if not'''
        
        if self.try_to_solve(self.start[1],self.start[0]):
            return True
        else:
            raise MazeUnsolvable('There is no solution to this maze.')
        
    def mark_it(self,c,r,mark):
        '''Place the input mark on the current spot (row, column).'''
        
        if not self.the_maze[r][c]  == '1':
            self.the_maze[r][c] = mark
        
    def try_to_solve(self,c,r):
        '''Return True if maze can be solved from position (row, column),
        else return False.'''
        
        current_square = self.the_maze[r][c]
        if current_square != '2':
            d = {'x': False, '#': False, ' ': True, '2': True, '.': False, 
                 '1': False}
            #The dictionary is used to assign True or False depending on if
            #the position in question is traversable.
            
            up = d[self.the_maze[r - 1][c]]
            down = d[self.the_maze[r + 1][c]]
            right = d[self.the_maze[r][c + 1]]
            left = d[self.the_maze[r][c - 1]]
            #Checks to see what is in the adjacent squares and is assigned 
            #a value of True if it's a ' ' or a '2' and False if it's
            #anything else.   
            
            self.mark_it(c,r,'.')
            #Marks the current spot as traversed.
            
            if up and self.try_to_solve(c,r - 1):
                return True     
            if down and self.try_to_solve(c,r + 1):
                return True
            if left and self.try_to_solve(c - 1,r):
                return True
            if right and self.try_to_solve(c + 1,r):
                return True
            #Tries all the possible directions one at a time until it reaches
            #the end of the maze.
            
            self.mark_it(c,r,'x')
            return False
            #This indicates it has tried all the traversable spots adjacent
            #to it and it will now mark the spot 'x', having not led to the
            #end of the maze.
        
        else:
            return True
        #The current square is the exit.
