# A simple matrix
# This matrix is a list of lists
# Column and row numbers start with 1
 
class Matrix(object):
    def __init__(self, rows, cols):
        self.cols = cols
        self.rows = rows
        # initialize matrix and fill with zeroes
        self.matrix = []
        for i in range(rows):
            ea_row = []
            for j in range(cols):
                ea_row.append(0)
            self.matrix.append(ea_row)

    def row_count(self):
        return self.rows;

    def col_count(self):
        return self.cols;
    
    def get_row(self, row):
        return self.matrix[row];    
 
    def set_item(self, row, col, v):
        self.matrix[row][col] = v
 
    def get_item(self, row, col):
        return self.matrix[row][col]
 
    def __repr__(self):
        outStr = ""
        for i in range(self.rows):
            outStr += 'Row %s = %s\n' % (i, self.matrix[i])
        return outStr
 
    def __iter__(self):
        for row in range(self.rows):
            for col in range(self.cols):
                yield (self.matrix, row, col)
