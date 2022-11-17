from z3 import *

# Open each instance text file and read the data
def read_instance(instance):
    with open(instance, 'r') as input_file:
        lines = input_file.read().splitlines()
        width = lines[0]
        n_circuits = lines[1]
        # vectors of x and y sizes
        x_sizes = []
        y_sizes = []
        # for all circuits, store in the x_sizes and y_sizes arrays the horizontal and vertical sizes of the circuits
        for i in range(int(n_circuits)):
            line = lines[i + 2].split(' ')
            x_sizes.append(int(line[0]))
            y_sizes.append(int(line[1]))

        return int(width), int(n_circuits), x_sizes, y_sizes

# For each instance write the solution into an output file
def output_solution(width, n_circuits, x_sizes, y_sizes, x_sol, y_sol, height, solution, time):
    with open(solution, 'w+') as output_file:
        output_file.write('{} {}\n'.format(width, height))
        output_file.write('{}\n'.format(n_circuits))

        for i in range(n_circuits):
            output_file.write('{} {} {} {}\n'.format(x_sizes[i], y_sizes[i], x_sol[i], y_sol[i]))

        output_file.write("----------\n")
        output_file.write('{}'.format(time))


def output_solution_rot(width, n_circuits, x_size, y_size, x_sol, y_sol, rot_sol, height, solution, time):

    with open(solution, 'w+') as out_file:
        out_file.write('{} {}\n'.format(width, height))
        out_file.write('{}\n'.format(n_circuits))

        for i in range(n_circuits):
            rotation = "rotated" if rot_sol[i] else ""
            out_file.write('{} {} {} {} {}\n'.format(x_size[i], y_size[i], x_sol[i], y_sol[i], rotation))

        out_file.write("----------\n")
        out_file.write('{}'.format(time))

# Z3 utilities

# Find maximum of a vector in Z3
def max_z3(vector):
    maximum = vector[0]
    for value in vector[1:]:
        maximum = If(value > maximum, value, maximum)
    return maximum 

# Cumulative constraint in Z3
def cumulative_z3(start, duration, resources, total):
    cumulative = []
    for u in resources:
        cumulative.append(
            sum([If(And(start[i] <= u, u < start[i] + duration[i]), resources[i], 0)
                 for i in range(len(start))]) <= total
        )
    return cumulative