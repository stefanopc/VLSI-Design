import os
import re

# Open each instance in a .txt file and read the data
def read_instance(f):
    file = open(f, "r")
    width = int(file.readline())
    n_circuits  = int(file.readline())
    x_sizes = []
    y_sizes = []
    for i in range(n_circuits):
        circ_dim = file.readline()
        circ_dim_split = circ_dim.strip().split(" ")
        x_sizes.append(int(circ_dim_split[0]))
        y_sizes.append(int(circ_dim_split[1]))
    return width, n_circuits, x_sizes, y_sizes

# Write the data of each instance into a .dzn file
def write_instance(width, n_circuits, x_sizes, y_sizes, out_path="./file.dzn"):
    file = open(out_path, mode="w")
    file.write(f"width = {width};\n")
    file.write(f"n = {n_circuits};\n")
    file.write(f"x_sizes = {x_sizes};\n")
    file.write(f"y_sizes = {y_sizes};")
    file.close()


if __name__ == "__main__":
    # Input and output directories
    in_path = "../instances/"
    out_path = "../CP/in/"
    files = os.listdir(in_path)

    list_instances = []
    for f in files:
        obj = re.search("^ins-[0-9]+.txt", f)
        if obj is not None:
            width, n_circuits, x_sizes, y_sizes = read_instance(in_path + f)
            f2 = f.replace(".txt", ".dzn")
            write_instance(width, n_circuits, x_sizes, y_sizes, out_path + f2)