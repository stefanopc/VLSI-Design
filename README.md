# VLSI Design

Combinatorial Decision Making and Optimization project work

## Introduction

VLSI (Very Large Scale Integration) refers to the trend of integrating circuits into silicon chips. The modern trend of shrinking transistor sizes, allowing engineers to fit more and more transistors into the same area of silicon, has pushed the integration of more and more functions of cellphone circuitry into a single silicon die (i.e. plate). This enabled the modern cellphone to mature into a powerful tool that shrank from the size of a large brick-sized unit to a device small enough to comfortably carry in a pocket or purse, with a video camera, touchscreen, and other advanced features.

Given a fixed-width plate and a list of rectangular circuits, the problem consists in deciding how to place the circuits on the plate in order to minimize the length of the final device. 

The combinatorial optimization problem will be modeled and solved using two approaches: Constraint Programming (CP) using Minizinc and Satisfiability Modulo Theories (SMT) using Z3Py.

## Requirements

It is required to have installed the latest versions of Python and MiniZinc IDE, as well as the following libraries:
- minizinc
- z3-solver
- matplotlib
- numpy

## Instructions:

To run the CP (or SMT) model, go into the relative directory CP/src (or SMT/src) and execute the python solver file with the command 'python3 solveCP.py'. This requires that all the instances are in the .dzn format; to convert the instances from .txt to .dzn, run the python script `convert_to_dzn.py` in the `util` folder.

To visualize the solutions, it is necessary to move into the `util` directory and run the python script `plot_solution.py` with the following command: "python3 plot_solution.py -f <output file ins-x-out.txt >".
