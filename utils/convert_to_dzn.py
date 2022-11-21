import os
import re

# Open each instance in a .txt file and read the data
def read_instance(f):
    file = open(f, "r")
    # extract plate width
    width = int(file.readline())
    # extract number of circuits
    n_circuits = int(file.readline())
    x_dim = []
    y_dim = []
    # extract x and y circuits dimensions
    for i in range(n_circuits):
        circ_dim = file.readline()
        circ_dim_split = circ_dim.strip().split(" ")
        x_dim.append(int(circ_dim_split[0]))
        y_dim.append(int(circ_dim_split[1]))
    return width, n_circuits, x_dim, y_dim

# Write the data of each instance into a .dzn file
def write_instance(width, n_circuits, x_dim, y_dim, out_path=None):
    file = open(out_path, mode="w")
    file.write(f"width = {width};\n")
    file.write(f"n = {n_circuits};\n")
    file.write(f"x_dim = {x_dim};\n")
    file.write(f"y_dim = {y_dim};")
    file.close()


if __name__ == "__main__":
    # Input and output directories
    in_path = "../instances/"
    out_path = "../CP/in/"
    files = os.listdir(in_path)

    list_instances = []
    for f_in in files:
        obj = re.search("^ins-[0-9]+.txt", f_in)
        if obj is not None:
            width, n_circuits, x_dim, y_dim = read_instance(in_path + f_in)
            f_out = f_in.replace(".txt", ".dzn")
            write_instance(width, n_circuits, x_dim, y_dim, out_path + f_out)