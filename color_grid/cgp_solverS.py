from clause import *
from itertools import chain

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
    if points is not None :
        for p in points:
            c = Clause(size)
            c.add_positive(p[0], p[1], p[2])
            expression.append(c)

    cells = list(coord(size))
    for p in cells:
        color = Clause(size)
        for k in range(size):
            color.add_positive(p[0], p[1], k)
            expression.append(color)
            for i in range(size):
                if i != p[0] :
                    c = Clause(size)
                    c.add_negative(p[0], p[1], k)
                    c.add_negative(i, p[1], k)
                    expression.append(c)
            for j in range(size):
                if j != p[1]:
                    c = Clause(size)
                    c.add_negative(p[0], p[1], k)
                    c.add_negative(p[0], j, k)
                    expression.append(c)
            for (x, y) in diagonals((p[0], p[1]), size):
                if (x, y) != (p[0], p[1]):
                    c = Clause(size)
                    c.add_negative(p[0], p[1], k)
                    c.add_negative(x, y, k)
                    expression.append(c)
    return expression

def coord(size):
    for i in range(size):
        for j in range(size):
            yield [i, j]

# copied from https://codereview.stackexchange.com/questions/146935/find-diagonal-positions-for-bishop-movement
def diagonals(coord, size):
    x, y = coord
    return list(chain(
        [(x, y)],
        zip(range(x - 1, -1, -1), range(y - 1, -1, -1)),
        zip(range(x + 1, size, 1), range(y + 1, size, 1)),
        zip(range(x + 1, size, 1), range(y - 1, -1, -1)),
        zip(range(x - 1, -1, -1), range(y + 1, size, 1)),
    ))

if __name__ == '__main__':
    expression = get_expression(2)
    for clause in expression:
        print(clause)
