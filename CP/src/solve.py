import os
from glob import glob
from natsort import natsorted
import subprocess
from time import time


# Given the model

def solve_instance(model, in_file, out_dir):
    # Run the chosen model
    command = f'minizinc --solver Gecode -t 300000 {model} {in_file}'

    instance_name = in_file.split('/')[-1] if os.name == 'nt' else in_file.split('/')[-1]
    instance_name = instance_name[:len(instance_name) - 4]
    out_file = os.path.join(out_dir, instance_name + '-out.txt')
    with open(out_file, 'w') as f:
        print(f'{out_file}:', end='\n', flush=True)
        start_time = time()
        subprocess.run(command.split())
        elapsed_time = time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')
        if (elapsed_time * 1000) < 300000:
            subprocess.run(command.split(), stdout=f)
            f.write('{}'.format(round(elapsed_time,4)))


def main():
    in_dir = "../in"
    model = "CP-model-base.mzn" # base or rotation model
    out_dir = "../out/baseMOD"
    for in_file in natsorted(glob((os.path.join(in_dir, '*.dzn')))):
        solve_instance(model, in_file, out_dir)


if __name__ == '__main__':
    main()