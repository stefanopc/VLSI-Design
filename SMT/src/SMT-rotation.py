import numpy as np
import time
from natsort import natsorted
from glob import glob
from utilsSMT import *

def solve_instance(in_file, out_dir):
    instance_name = in_file.split('/')[-1]
    instance_name = instance_name[:len(instance_name) - 4]
    out_file = os.path.join(out_dir, instance_name + '-out.txt')

    width, n_circuits, x_sizes, y_sizes = read_instance(in_file)

    # Coordinates of the circuits
    x = IntVector('x', n_circuits)
    y = IntVector('y', n_circuits)

    ''''# coordinates of the points
    x = [Int("p_x_%s" % str(i + 1)) for i in range(n_circuits)]
    y = [Int("p_y_%s" % str(i + 1)) for i in range(n_circuits)]'''

    # rotation array
    rotation = BoolVector('rot', n_circuits)
    # actual dimensions of circuits considering rotation
    x_sizes_rot = [If(And(x_sizes[i] != y_sizes[i], rotation[i]), y_sizes[i], x_sizes[i]) for i in range(n_circuits)]
    y_sizes_rot = [If(And(x_sizes[i] != y_sizes[i], rotation[i]), x_sizes[i], y_sizes[i]) for i in range(n_circuits)]

    # Maximum plate height to minimize
    height = max_z3([y[i] + y_sizes[i] for i in range(n_circuits)])

    # Setting the optimizer
    opt = Optimize()
    opt.minimize(height)

    # Setting domain and no overlap constraints
    domain_x = []
    domain_y = []
    no_overlap = []

    for i in range(n_circuits):
        domain_x.append(x[i] >= 0)
        domain_x.append(x[i] + x_sizes_rot[i] <= width) # ROT
        domain_y.append(y[i]>=0)
        domain_y.append(y[i] + y_sizes_rot[i] <= height) # ROT

        for j in range(i+1, n_circuits):
            no_overlap.append(Or(x[i]+x_sizes_rot[i] <= x[j],
                                 x[j]+x_sizes_rot[j] <= x[i],
                                 y[i]+y_sizes_rot[i] <= y[j],
                                 y[j]+y_sizes_rot[j] <= y[i]))


        # If a circuit is squared it is forced not to be rotated
        opt.add(If(x_sizes[i]==y_sizes[i],
                   And(x_sizes[i]==x_sizes_rot[i],
                       y_sizes[i]==y_sizes_rot[i]),
                   Or(And(x_sizes[i]==x_sizes_rot[i],
                          y_sizes[i]==y_sizes_rot[i]),
                      And(x_sizes_rot[i]==y_sizes[i],
                          y_sizes_rot[i]==x_sizes[i]))))

    opt.add(domain_x + domain_y + no_overlap)

    # Cumulative constraints
    cumulative_y = cumulative_z3(y, y_sizes_rot, x_sizes_rot, width) # ROT
    cumulative_x = cumulative_z3(x, x_sizes_rot, y_sizes_rot, sum(y_sizes_rot)) # ROT

    opt.add(cumulative_x + cumulative_y)

    # Boundaries constraints
    max_width = [max_z3([x[i] + x_sizes_rot[i] for i in range(n_circuits)]) <= width] # ROT
    max_height = [max_z3([y[i] + y_sizes_rot[i] for i in range(n_circuits)]) <= sum(y_sizes_rot)] # ROT

    opt.add(max_width + max_height)

    # Symmetry breaking constraints
    areas_index = np.argsort([x_sizes[i] * y_sizes[i] for i in range(n_circuits)])
    biggest_circuit = areas_index[-1]
    # Impose that the biggest is positioned at the bottom left (at coordinates (0,0))
    sym_biggest_bottom_left = And(x[biggest_circuit] == 0,
                                  y[biggest_circuit] == 0)
    opt.add(sym_biggest_bottom_left)


    # Maximum time of execution
    opt.set("timeout", 300000)

    # solutions
    x_sol = []
    y_sol = []
    rot_sol = []

    # Solve

    print(f'{out_file}:', end='\t', flush=True)
    start_time = time.time()

    if opt.check() == sat:
        model = opt.model()
        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')
        # Getting values of variables
        for i in range(n_circuits):
            x_sol.append(model.evaluate(x[i]).as_string())
            y_sol.append(model.evaluate(y[i]).as_string())
            # check whether there was rotation or not
            rot_value = model[rotation[i]]
            if rot_value is None:
                rot_sol.append(False)
            else:
                rot_sol.append(rot_value)
        height_sol = model.evaluate(height).as_string()

        # Storing the result
        output_solution_rot(width, n_circuits, x_sizes, y_sizes, x_sol, y_sol, rot_sol, height_sol, out_file, elapsed_time)
    else:
        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')
        print("Solution not found")

def main():
    in_dir = "../../instances"
    out_dir = "../out/rotation"
    for in_file in natsorted(glob((os.path.join(in_dir, '*.txt')))):
        solve_instance(in_file, out_dir)

if __name__ == '__main__':
    main()