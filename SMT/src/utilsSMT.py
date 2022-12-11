from z3 import *

# Open each instance text file and read the data
def read_instance(instance):
    with open(instance, 'r') as input_file:
        lines = input_file.read().splitlines()
        width = lines[0]
        n_circuits = lines[1]
        # vectors of x and y dimensions
        x_dim = []
        y_dim = []
        # for all circuits, store the horizontal and vertical dimensions
        for i in range(int(n_circuits)):
            line = lines[i + 2].split(' ')
            x_dim.append(int(line[0]))
            y_dim.append(int(line[1]))

        return int(width), int(n_circuits), x_dim, y_dim

# Z3 utilities

# Find maximum of a vector in Z3
def maxVal(vector):
    maximum = vector[0]
    for value in vector[1:]:
        maximum = If(value > maximum, value, maximum)
    return maximum 

# Cumulative constraint in Z3 as in MiniZinc
def cumulative(start, duration, resources, total):
    cumulative = []
    for u in resources:
        cumulative.append(
            sum([If(And(start[i] <= u, u < start[i] + duration[i]), resources[i], 0)
                 for i in range(len(start))]) <= total
        )
    return cumulative