from clause import *
import itertools

"""
For the color grid problem, the only code you have to do is in this file.

You should replace

# your code here

by a code generating a list of clauses modeling the grid color problem
for the input file.

You should build clauses using the Clause class defined in clause.py

Read the comment on top of clause.py to see how this works.
"""


def get_expression(size, points=None):
    expression = []
    if points is not None:
        for point in points:
            c = Clause(size)
            c.add_positive(point[0], point[1], point[2])
            expression.append(c)
    for i in range(0,size):
        for j in range(0,size):
            caution = []
            caution.extend(get_line(i, j, size))
            caution.extend(get_column(i, j, size))
            caution.extend(get_diags(i, j, size))
            d = Clause(size)
            for color in range(0, size):
                for x, y in itertools.product(range(0, size), range(0, size)):
                    c = Clause(size)
                    if(x, y) == (i, j):
                        d.add_positive(x, y, color)
                        expression.append(d)
                    elif (x, y) in caution:
                        c.add_negative(i, j, color)
                        c.add_negative(x, y, color)
                        expression.append(c)
    return expression




def get_column(i, j, size):
    column = []
    for x in range(0, size):
        if x != i:
            column.append((x, j))
    return column

def get_line(i, j, size):
    line = []
    for y in range(0, size):
        if y != j:
            line.append((i, y))
    return line

def get_diags(i, j, size):
    diags = []
    for d in range(size):
        if d != 0:
            if i-d >= 0 and j-d >= 0:
                diags.append((i-d, j-d))
            if i-d >= 0 and j+d < size:
                diags.append((i-d, j+d))
            if i+d < size and j-d >= 0:
                diags.append((i+d, j-d))
            if i+d < size and j+d < size:
                diags.append((i+d, j+d))
    return diags

if __name__ == '__main__':
    expression = get_expression(2)
    for clause in expression:
        print(clause)
