from clause import *

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
    for i in range(0,size):
        for j in range(0,size):
            clause1 = Clause(size)
            for c in range(size):
                clause2_4 = Clause(size)
                clause3_7 = Clause(size)
                clause5_8 = Clause(size) 
                clause6_9 = Clause(size)
                clause1.add_positive(i,j,c)
                clause2_4.add_positive(i,j,c)
                clause3_7.add_positive(i,j,c)
                if (j+1<size):
                    clause5_8.add_negative(i,j+1,c)
                if (i+1<size):
                    clause6_9.add_negative(i+1,j,c)
                for other in range(size):
                    if (other!=c):
                        if (j+1<size):
                            clause2_4.add_negative(i,j+1,other)
                            clause5_8.add_negative(i,j+1,other)
                        if (i+1<size):
                            clause3_7.add_negative(i+1,j,other) 
                            clause6_9.add_negative(i+1,j,other)  
                if (j+1<size):
                    expression.append(clause2_4)
                    expression.append(clause5_8)
                if (i+1<size):
                    expression.append(clause3_7)
                    expression.append(clause6_9)
            expression.append(clause1)  
    return expression #TODO: pas correct -> index bizarres, jsp pk et il faut rajouter la contrainte sur la diagonale, voir la photo dans le git pour les numéros de clauses


if __name__ == '__main__':
    expression = get_expression(2)
    for clause in expression:
        print(clause)
