import numpy as np
import time
from natsort import natsorted
from glob import glob
from utilsSMT import *


# Takes the input file, solves the instances and outputs the solution
def solve_instance(input_file, output_dir):
    instance_name = input_file.split('/')[-1]
    instance_name = instance_name[:len(instance_name) - 4]
    out_file = os.path.join(output_dir, instance_name + '-out.txt')

    # Get values from input instance file
    width, n_circuits, x_dim, y_dim = read_instance(input_file)

    # Vector of circuits' x and y coordinates
    x = IntVector('x', n_circuits)
    y = IntVector('y', n_circuits)

    # Objective variable: maximum plate height to minimize
    height = maxVal([y[i] + y_dim[i] for i in range(n_circuits)])

    # Set the optimizer with objective function
    opt = Optimize()
    opt.minimize(height)

    # Set domain and no-overlap constraints
    dom_x = []
    dom_y = []
    no_overlap = []
    for i in range(n_circuits):
        dom_x.append(x[i] >= 0)
        dom_x.append(x[i] + x_dim[i] <= width)
        dom_y.append(y[i] >= 0)
        dom_y.append(y[i] + y_dim[i] <= height)
        for j in range(i+1, n_circuits):
            no_overlap.append(
                Or(x[i]+x_dim[i] <= x[j],
                   x[j]+x_dim[j] <= x[i],
                   y[i]+y_dim[i] <= y[j],
                   y[j]+y_dim[j] <= y[i]))

    opt.add(dom_x + dom_y + no_overlap)

    # Cumulative constraints
    cumulative_x = cumulative(x, x_dim, y_dim, sum(y_dim))
    cumulative_y = cumulative(y, y_dim, x_dim, width)
    opt.add(cumulative_x + cumulative_y)

    # Boundaries constraints
    max_width = [maxVal([x[i] + x_dim[i] for i in range(n_circuits)]) <= width]
    max_height = [maxVal([y[i] + y_dim[i] for i in range(n_circuits)]) <= sum(y_dim)]
    opt.add(max_width + max_height)


    # Symmetry breaking constraints

    areas_index = np.argsort([x_dim[i] * y_dim[i] for i in range(n_circuits)])
    biggest_circuit = areas_index[-1]

    # Impose that the biggest circuit is placed at the bottom left (at coordinates (0,0))
    sym_biggest_bottom_left = And(x[biggest_circuit] == 0,
                                  y[biggest_circuit] == 0)
    opt.add(sym_biggest_bottom_left)

    # Maximum time of execution is 300 seconds, otherwise the solving process is aborted
    opt.set("timeout", 300000)

    # Array of solutions for x and y
    x_sol = []
    y_sol = []

    # Solve
    print(f'{out_file}:', end='\t', flush=True)
    start_time = time.time()

    # Checks whether there is a satisfying assignment for the formulas
    if opt.check() == sat:
        model = opt.model()
        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')
        # Store solutions to output
        for i in range(n_circuits):
            x_sol.append(model.evaluate(x[i]).as_string())
            y_sol.append(model.evaluate(y[i]).as_string())
        height_sol = model.evaluate(height).as_string()

        # Outputs solution values
        output_solution(width, n_circuits, x_dim, y_dim, x_sol, y_sol, height_sol, out_file, elapsed_time)
    
    else:  # unsat
        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')
        print("Solution not found")

# For each instance write the solution into an output file
def output_solution(width, n_circuits, x_dim, y_dim, x_sol, y_sol, height, solution, time):
    with open(solution, 'w+') as output_file:
        output_file.write('{} {}\n'.format(width, height))
        output_file.write('{}\n'.format(n_circuits))

        for i in range(n_circuits):
            output_file.write('{} {} {} {}\n'.format(x_dim[i], y_dim[i], x_sol[i], y_sol[i]))

        output_file.write("----------\n")
        output_file.write('{}'.format(time))

def main():
    # Input instances and output directories
    in_dir = "../../instances"
    out_dir = "../out/base"
    for in_file in natsorted(glob((os.path.join(in_dir, '*.txt')))):
        solve_instance(in_file, out_dir)

if __name__ == '__main__':
    main()