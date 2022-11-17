import argparse
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import cm
import numpy as np
from os import path


# Show the solution graphically by using a list of corners inside the margins w_plate and h_plate

def plot_solution(w_plate, h_plate, n, circuits, solution, colors = None, save_fig_path=None):

    corners = solution['corners']
    rotations = solution['rotation']

    # get n colors if they are not passed as parameter
    if colors is None:
        colors = cm.jet(np.linspace(0, 1, n))

    fig, ax = plt.subplots(facecolor='w', edgecolor='k')

    for i in range(n):
        # dimensions of the circuit
        x = circuits[i][0]
        y = circuits[i][1]

        # check rotation
        if rotations[i]:
            x, y = y, x

        r = Rectangle(corners[i],x,y,facecolor=colors[i],edgecolor='black', linewidth=1.5, label=f'circuit {i+1}')
        ax.add_patch(r)

    ax.set_xlim(0, w_plate)
    ax.set_ylim(0, h_plate)
    ax.set_xticks(np.arange(w_plate))
    ax.set_yticks(np.arange(h_plate))
    plt.xlabel("w")
    plt.ylabel("h")
    plt.grid(color='black',linewidth=0.5)


    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    if save_fig_path is not None:
        plt.savefig(f"{save_fig_path}/{w_plate}x{h_plate}-sol.png", dpi=300, bbox_inches='tight')

    plt.show()


if __name__ == "__main__":

    # Construct the argument parser
    parser = argparse.ArgumentParser()

    # Add the arguments to the parser
    parser.add_argument("-f", "--filename", required=True, type=str)
    args = parser.parse_args()

    if not path.isfile(args.filename):
        print("\nSpecified file does not exist, please insert an existing solution file.\n")
    else:
        with open(args.filename, "r") as file:  # Use file to refer to the file object

            # Read the first line which contains the width and the minimal height of the silicon plate
            first_line = file.readline().strip().split(" ")

            width = int(first_line[0])
            height = int(first_line[1])

            # Read the second line which contains the number of necessary circuits
            n_circuits = int(file.readline().strip())

            # Read all the remaining lines which contains the horizontal and vertical dimension of the i-th circuit
            # and its bottom left corner coordinate
            remaining_lines = file.readlines()

            # To remove empty lines
            remaining_lines = [line.strip() for line in remaining_lines if line.strip()]

            # To remove lines like === or ----
            remaining_lines = [line for line in remaining_lines if ("=" not in line) and ('-' not in line)]

            circuits = []
            solution = {'corners': [], 'rotation': []}

            for i in range(n_circuits):
                line = remaining_lines[i]
                line = line.split()
                circuits.append((int(line[0]), int(line[1])))
                solution['corners'].append((int(line[2]), int(line[3])))
                solution['rotation'].append(True if "rotated" in line else False)

        plot_solution(width, height, n_circuits, circuits, solution)
