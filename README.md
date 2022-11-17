# VLSI Design

Project work for the Combinatorial Decision Making and Optimization course.

## Introduction

VLSI (Very Large Scale Integration) refers to the trend of integrating circuits into silicon chips. The modern trend of shrinking transistor sizes, allowing engineers to fit more and more transistors into the same area of silicon, has pushed the integration of more and more functions of cellphone circuitry into a single silicon die (i.e. plate). This enabled the modern cellphone to mature into a powerful tool that shrank from the size of a large brick-sized unit to a device small enough to comfortably carry in a pocket or purse, with a video camera, touchscreen, and other advanced features.

The combinatorial optimization problem will be modeled and solved with Constraint Programming (CP) and Satisfiability Modulo Theories (SMT).

## Requirements

It is required to have installed the latest versions of Python and MiniZinc IDE, as well as the following libraries:
- minizinc
- z3-solver
- matplotlib
- numpy
- natsort

## Instructions:

To run the CP (SMT) model, go into the relative directory CP/src (SMT/src) and execute the python solver file with the command 'python3 solve.py'. This requires that all the instances are in the .dzn format; to convert the instances from .txt to .dzn, run the python script `convert_to_dzn.py` in the `util` folder.

To visualize the solutions, it is necessary to move into the `util` folder and run the python script `plot_solution.py` with the following command:
"python3 plot_solution.py -f <output file_path>"
