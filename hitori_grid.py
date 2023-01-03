class HitoriGrid:
    """
    Class to represent an assignment of values to the 64 variables defining a Hitori game. 

    Attribute _cells stores a matrix with 64 entries, one for each variable in the puzzle. 
    Each entry of the matrix stores the domain of a variable.
    Backtracking search will reduce the the domain of the variables as they proceed with search and inference.
    """
    def __init__(self):
        self._cells = []
        self._width = 8

    def copy(self):
        """
        Returns a copy of the grid. 
        """
        copy_grid = HitoriGrid()
        copy_grid._cells = [row.copy() for row in self._cells]
        return copy_grid

    def get_cells(self):
        """
        Returns the matrix with the domains of all variables in the puzzle.
        """
        return self._cells

    def get_width(self):
        """
        Returns the width of the grid.
        """
        return self._width

    def read_file(self, string_puzzle):
        """
        Reads a Hitori puzzle from string and initializes the matrix _cells. 

        This is a valid input string:

        3735516256237284175725623411682342751376382465148241357575862737

        This is translated into the following Hitori grid:

        - - - - - - - - - - - - - - - - - 
        | 3 | 7 | 3 | 5 | 5 | 1 | 6 | 2 | 
        - - - - - - - - - - - - - - - - - 
        | 5 | 6 | 2 | 3 | 7 | 2 | 8 | 4 | 
        - - - - - - - - - - - - - - - - - 
        | 1 | 7 | 5 | 7 | 2 | 5 | 6 | 2 | 
        - - - - - - - - - - - - - - - - - 
        | 3 | 4 | 1 | 1 | 6 | 8 | 2 | 3 | 
        - - - - - - - - - - - - - - - - - 
        | 4 | 2 | 7 | 5 | 1 | 3 | 7 | 6 | 
        - - - - - - - - - - - - - - - - - 
        | 3 | 8 | 2 | 4 | 6 | 5 | 1 | 4 | 
        - - - - - - - - - - - - - - - - - 
        | 8 | 2 | 4 | 1 | 3 | 5 | 7 | 5 | 
        - - - - - - - - - - - - - - - - - 
        | 7 | 5 | 8 | 6 | 2 | 7 | 3 | 7 | 
        - - - - - - - - - - - - - - - - -  

        """
        i = 0
        row = []
        for p in string_puzzle:
            row.append(p+'X')

            i += 1

            if i % self._width == 0:
                self._cells.append(row)
                row = []
        

    def print(self):
        """
        Prints the grid on the screen.
        """
        string = '- ' * (2*self._width + 1)
        print(string)

        for row in self._cells:

            print('|', end=" ")

            for col in row:

                if len(col) == 1:
                    print(col, end=" ")
                else:
                    print(col[0], end=" ")

                print('|', end=" ")

            print()
            print(string)

    def print_domains(self):
        """
        Print the domain of each variable for a given grid of the puzzle.
        """
        for row in self._cells:
            print(row)

    def single_variable(self):
        """
        Returns True if all the variables have been assigned a single value and False otherwise. 
        """
        solved = True
        for row in self._cells:
            for col in row:
                if len(col) != 1:
                    solved = False
        
        return solved

    def white_cells(self):
        """
        Returns total no of cells that are not eliminated in the current grid
        """
        counter = 0
        for row in self.get_cells():
            for col in row:
                if col != 'X' and len(col) == 1:
                    counter = counter + 1
        return counter

    def partition(self, row, col):
        """
        Returns True if there is a partition of eliminated cells present in the given grid
        """
        open = [(row, col)]
        closed = [(row, col)]
        
        while len(open) != 0:
            element = open.pop(0)
            x = self.available_moves(element[0], element[1])
            for neighbor in x:
                if neighbor not in closed:
                    open.append(neighbor)
                    closed.append(neighbor)

        if len(closed) != self.white_cells():
            return True
        else:
            return False
        

    def available_moves(self, row, col):
        """
        Returns the neigboring available moves (horizontal or vertical non-eliminated cells)
        """
        if self._cells[row][col]:
            if row == 0:
                if col == 0:
                    return self.remove_eliminated_cells([(row+1, col), (row, col+1)])
                elif col == self.get_width() - 1:
                    return self.remove_eliminated_cells([(row, col-1), (row+1, col)])
                else:
                    return self.remove_eliminated_cells([(row, col-1), (row+1, col), (row, col+1)])

            elif row == self.get_width() - 1:
                if col == 0:
                    return self.remove_eliminated_cells([(row-1, col), (row, col+1)])
                elif col == self.get_width() - 1:
                    return self.remove_eliminated_cells([(row, col-1), (row-1, col)])
                else:
                    return self.remove_eliminated_cells([(row, col-1), (row-1, col), (row, col+1)])
            
            else:
                if col == 0:
                    return self.remove_eliminated_cells([(row-1, col), (row, col+1), (row+1, col)])
                elif col == self.get_width() - 1:
                    return self.remove_eliminated_cells([(row-1, col), (row, col-1), (row+1, col)])
                else:
                    return self.remove_eliminated_cells([(row-1, col), (row, col-1), (row+1, col), (row, col+1)])


    def remove_eliminated_cells(self, cells):
        """
        Returns all elements from given list that are not 'X' (eliminated)
        """
        a = []
        for element in cells:
            if self._cells[element[0]][element[1]] != 'X':
                a.append(element)
        return a
       

    def is_value_consistent(self, value, row, column):
        """
        Checks if the current value is consistent
        """
        if value.isnumeric():
            for i in range(self.get_width()):
                if i == column: continue
                if self.get_cells()[row][i] == value:
                    return False
        
            for i in range(self.get_width()):
                if i == row: continue
                if self.get_cells()[i][column] == value:
                    return False

        elif row == 0:
            if column == 0:
                if self._cells[row+1][column] == 'X' or self._cells[row][column+1] == 'X':
                    return False
            elif column == self.get_width()-1:
                if self._cells[row+1][column] == 'X' or self._cells[row][column-1] == 'X':
                    return False
            else:
                if self._cells[row+1][column] == 'X' or self._cells[row][column+1] == 'X' or self._cells[row][column-1] == 'X':
                    return False

        elif row == self.get_width()-1:
            if column == 0:
                if self._cells[row-1][column] == 'X' or self._cells[row][column+1] == 'X':
                    return False
            elif column == self.get_width()-1:
                if self._cells[row-1][column] == 'X' or self._cells[row][column-1] == 'X':
                    return False
            else:
                if self._cells[row-1][column] == 'X' or self._cells[row][column+1] == 'X' or self._cells[row][column-1] == 'X':
                    return False

        elif column == 0:
            if self._cells[row][column+1] == 'X' or self._cells[row-1][column] == 'X' or self._cells[row+1][column] == 'X':
                    return False

        elif column == self.get_width()-1:
            if self._cells[row][column-1] == 'X' or self._cells[row-1][column] == 'X' or self._cells[row+1][column] == 'X':
                    return False

        else:
            if self._cells[row-1][column] == 'X' or  self._cells[row][column-1] == 'X' or self._cells[row+1][column] == 'X' or self._cells[row][column+1] == 'X':
                return False
        
        return True

