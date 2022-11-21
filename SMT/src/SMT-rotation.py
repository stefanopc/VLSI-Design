import numpy as np
import time
from natsort import natsorted
from glob import glob
from utilsSMT import *

# Takes the input file, solves the instances and outputs the solution
def solve_instance(in_file, out_dir):
    instance_name = in_file.split('/')[-1]
    instance_name = instance_name[:len(instance_name) - 4]
    out_file = os.path.join(out_dir, instance_name + '-out.txt')

    # Get values from input instance file
    width, n_circuits, x_dim, y_dim = read_instance(in_file)

    # Vector of the circuits x and y coordinates
    x = IntVector('x', n_circuits)
    y = IntVector('y', n_circuits)

    # rotation array
    rotation = BoolVector('rot', n_circuits)
    # actual dimensions of circuits considering rotation
    x_dim_rot = [If(And(x_dim[i] != y_dim[i], rotation[i]), y_dim[i], x_dim[i]) for i in range(n_circuits)]
    y_dim_rot = [If(And(x_dim[i] != y_dim[i], rotation[i]), x_dim[i], y_dim[i]) for i in range(n_circuits)]

    # Objective variable: maximum plate height to minimize
    height = max_z3([y[i] + y_dim[i] for i in range(n_circuits)])

    # Set the optimizer with objective function
    opt = Optimize()
    opt.minimize(height)

    # Set domain and no overlap constraints
    domain_x = []
    domain_y = []
    no_overlap = []
    for i in range(n_circuits):
        domain_x.append(x[i] >= 0)
        domain_x.append(x[i] + x_dim_rot[i] <= width)
        domain_y.append(y[i]>=0)
        domain_y.append(y[i] + y_dim_rot[i] <= height)
        for j in range(i+1, n_circuits):
            no_overlap.append(Or(x[i]+x_dim_rot[i] <= x[j],
                                 x[j]+x_dim_rot[j] <= x[i],
                                 y[i]+y_dim_rot[i] <= y[j],
                                 y[j]+y_dim_rot[j] <= y[i]))

        # If a circuit is squared it is forced not to be rotated
        opt.add(If(x_dim[i]==y_dim[i],
                   And(x_dim[i]==x_dim_rot[i],
                       y_dim[i]==y_dim_rot[i]),
                   Or(And(x_dim[i]==x_dim_rot[i],
                          y_dim[i]==y_dim_rot[i]),
                      And(x_dim_rot[i]==y_dim[i],
                          y_dim_rot[i]==x_dim[i]))))

    opt.add(domain_x + domain_y + no_overlap)

    # Cumulative constraints
    cumulative_y = cumulative_z3(y, y_dim_rot, x_dim_rot, width)
    cumulative_x = cumulative_z3(x, x_dim_rot, y_dim_rot, sum(y_dim_rot))
    opt.add(cumulative_x + cumulative_y)

    # Boundaries constraints
    max_width = [max_z3([x[i] + x_dim_rot[i] for i in range(n_circuits)]) <= width]
    max_height = [max_z3([y[i] + y_dim_rot[i] for i in range(n_circuits)]) <= sum(y_dim_rot)]
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

    # Arrays of solutions for x,y and rotation
    x_sol = []
    y_sol = []
    rot_sol = []

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
            # Checks circuit rotation
            rot_value = model[rotation[i]]
            if rot_value is None:
                rot_sol.append(False)
            else:
                rot_sol.append(rot_value)
        height_sol = model.evaluate(height).as_string()

        # Outputs solution values
        output_solution(width, n_circuits, x_dim, y_dim, x_sol, y_sol, rot_sol, height_sol, out_file, elapsed_time)
    else:  # unsat
        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')
        print("Solution not found")

# For each instance write the solution into an output file (also with rotation)
def output_solution(width, n_circuits, x_dim, y_dim, x_sol, y_sol, rot_sol, height, solution, time):

    with open(solution, 'w+') as out_file:
        out_file.write('{} {}\n'.format(width, height))
        out_file.write('{}\n'.format(n_circuits))

        for i in range(n_circuits):
            rotation = "rotated" if rot_sol[i] else ""
            out_file.write('{} {} {} {} {}\n'.format(x_dim[i], y_dim[i], x_sol[i], y_sol[i], rotation))

        out_file.write("----------\n")
        out_file.write('{}'.format(time))

def main():
    # Input instances and output directories
    in_dir = "../../instancesMOD"
    out_dir = "../out/rotation2"
    for in_file in natsorted(glob((os.path.join(in_dir, '*.txt')))):
        solve_instance(in_file, out_dir)

if __name__ == '__main__':
    main()