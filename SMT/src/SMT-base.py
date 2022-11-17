import numpy as np
import time
from natsort import natsorted
from glob import glob
from utilsSMT import *

#
def solve_instance(input_file, output_dir):
    instance_name = input_file.split('/')[-1]
    instance_name = instance_name[:len(instance_name) - 4]
    out_file = os.path.join(output_dir, instance_name + '-out.txt')

    width, n_circuits, x_sizes, y_sizes = read_instance(input_file)

    # Coordinates of the circuits
    x = IntVector('x', n_circuits)
    y = IntVector('y', n_circuits)

    # Maximum plate height to minimize
    height = max_z3([y[i] + y_sizes[i] for i in range(n_circuits)])

    # Set the optimizer with objective function to minimize
    opt = Optimize()
    opt.minimize(height)

    # Setting domain and no-overlap constraints
    dom_x = []
    dom_y = []
    no_overlap = []

    for i in range(n_circuits):
        dom_x.append(x[i] >= 0)
        dom_x.append(x[i] + x_sizes[i] <= width)
        dom_y.append(y[i] >= 0)
        dom_y.append(y[i] + y_sizes[i] <= height)

        for j in range(i+1, n_circuits):
            no_overlap.append(
                Or(x[i]+x_sizes[i] <= x[j],
                   x[j]+x_sizes[j] <= x[i],
                   y[i]+y_sizes[i] <= y[j],
                   y[j]+y_sizes[j] <= y[i]))

    opt.add(dom_x + dom_y + no_overlap)

    # Cumulative constraints
    cumulative_x = cumulative_z3(x, x_sizes, y_sizes, sum(y_sizes))
    cumulative_y = cumulative_z3(y, y_sizes, x_sizes, width)
    opt.add(cumulative_x + cumulative_y)

    # Boundaries constraints
    max_width = [max_z3([x[i] + x_sizes[i] for i in range(n_circuits)]) <= width]
    max_height = [max_z3([y[i] + y_sizes[i] for i in range(n_circuits)]) <= sum(y_sizes)]
    opt.add(max_width + max_height)

    # Symmetry breaking constraints
    areas_index = np.argsort([x_sizes[i] * y_sizes[i] for i in range(n_circuits)])
    biggest_circuit = areas_index[-1]
    # Impose that the biggest is positioned at the bottom left (at coordinates (0,0))
    sym_biggest_bottom_left = And(x[biggest_circuit] == 0, y[biggest_circuit] == 0)
    opt.add(sym_biggest_bottom_left)

    # Maximum time of execution is 300 seconds = 5 minutes
    opt.set("timeout", 300000)
    # Array of solutions for x and y
    x_sol = []
    y_sol = []

    # Solve
    print(f'{out_file}:', end='\t', flush=True)
    start_time = time.time()

    # when opt.check() returns sat Z3 can provide a model that assigns values to the free constants and functions in the assertions
    if opt.check() == sat:
        model = opt.model()
        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')
        # Getting values of variables
        for i in range(n_circuits):
            x_sol.append(model.evaluate(x[i]).as_string())
            y_sol.append(model.evaluate(y[i]).as_string())
        height_sol = model.evaluate(height).as_string()

        # Storing the result
        output_solution(width, n_circuits, x_sizes, y_sizes, x_sol, y_sol, height_sol, out_file, elapsed_time)
    
    else:  # produces unsat
        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')
        print("Solution not found")

def main():
    in_dir = "../../instances"
    out_dir = "../out/base"
    for in_file in natsorted(glob((os.path.join(in_dir, '*.txt')))):
        solve_instance(in_file, out_dir)
    

if __name__ == '__main__':
    main()