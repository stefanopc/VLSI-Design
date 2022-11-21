import argparse
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import cm
import numpy as np
from os import path


# Plot the solution of each instance by means of rectangles using a list of corners in the plate margins w and h
def plot_solution(w, h, n_circuits, circ_dim, solution, colors = None):
    corners = solution['corners']
    rotations = solution['rotation']
    # Color for plotting
    if colors is None:
        colors = cm.jet(np.linspace(0, 1, n_circuits))
    fig, ax = plt.subplots(facecolor='w', edgecolor='k')

    for i in range(n_circuits):
        # circuits dimensions x,y
        x = circ_dim[i][0]
        y = circ_dim[i][1]
        # if rotation swap the dimensions
        if rotations[i]:
            x, y = y, x

        # create a rectangle given the corners and circuit dimensions
        r = Rectangle(corners[i], x, y, facecolor=colors[i], edgecolor='black', linewidth=1.5, label=f'circuit {i+1}')
        ax.add_patch(r)

    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.set_xticks(np.arange(w))
    ax.set_yticks(np.arange(h))
    plt.xlabel("w")
    plt.ylabel("h")
    plt.grid(color='black',linewidth=0.5)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()


if __name__ == "__main__":
    # Construct the argument parser
    parser = argparse.ArgumentParser()
    # Add the arguments to the parser
    parser.add_argument("-f", "--filename", required=True, type=str)
    args = parser.parse_args()

    if not path.isfile(args.filename):
        print("\nInsert an existing solution file.\n")
    else:
        with open(args.filename, "r") as file:
            # Read the first line which contains width and height of the plate
            first_line = file.readline().strip().split(" ")
            width = int(first_line[0])
            height = int(first_line[1])
            # Read the second line which contains the number of circuits
            n_circuits = int(file.readline().strip())
            # Read all the remaining lines which contains the horizontal and vertical dimension of the i-th circuit
            # and its bottom left corner coordinate
            remaining_lines = file.readlines()
            # To remove empty lines
            remaining_lines = [line.strip() for line in remaining_lines if line.strip()]
            # To remove lines with dashed signs
            remaining_lines = [line for line in remaining_lines if ("=" not in line) and ('-' not in line)]
            # circuits x,y dimensions
            circuits = []
            # solution contains a list of corners and specifies if the circuit is rotated
            solution = {'corners': [], 'rotation': []}

            for i in range(n_circuits):
                line = remaining_lines[i]
                line = line.split()
                # circuits dimensions
                circuits.append((int(line[0]), int(line[1])))
                # append the circuits corners of the solution and possible rotation
                solution['corners'].append((int(line[2]), int(line[3])))
                solution['rotation'].append(True if "rotated" in line else False)

        plot_solution(width, height, n_circuits, circuits, solution)
