% VLSI Design - CP rotation model

include "globals.mzn";
include "diffn.mzn";
include "cumulative.mzn";

% Input variables

int: width; % plate width
int: n; % number of circuits
set of int: CIRCUITS = 1..n;

% array of circuits widths
array[CIRCUITS] of int: x_dim;
% array of circuits heights
array[CIRCUITS] of int: y_dim;

% Boolean array to model rotation of the circuits
array[CIRCUITS] of var bool: rotation;

% Actual horizontal dimension of circuits
array[CIRCUITS] of var int: x_dim_rot = [if rotation[i] then y_dim[i] else x_dim[i] endif | i in CIRCUITS];

% Actual vertical dimension of the circuits
array[CIRCUITS] of var int: y_dim_rot = [if rotation[i] then x_dim[i] else y_dim[i] endif | i in CIRCUITS];

% Output variables

% Horizontal coordinate of circuits
array[CIRCUITS] of var 0..width-1: x;
% Vertical coordinate of circuits
array[CIRCUITS] of var 0..sum(y_dim)-1: y;

% Plate bounds
int: lowb = max(y_dim ++ x_dim);
int: upb = sum([max(y_dim[i], x_dim[i]) | i in CIRCUITS]);

% Height of plate that ranges from lower to upper bound, to minimize
var lowb..upb: height;
height = max([y[i] + y_dim_rot[i] | i in CIRCUITS]);

% Domain reduction
constraint forall(i in CIRCUITS) (x[i] <= width - x_dim_rot[i])::domain;
constraint forall(i in CIRCUITS) (y[i] <= height - y_dim_rot[i])::domain;

% Constraints

% max width
constraint max([x[i] + x_dim_rot[i] | i in CIRCUITS]) <= width;
% max height
constraint max([y[i] + y_dim_rot[i] | i in CIRCUITS]) <= upb;

% A circuit cannot be rotated if its height is greater than plate width
constraint forall(i in CIRCUITS)(y_dim[i] > width -> rotation[i]==false);

% Global constraints

% Cumulative constraint: circuits as activities with duration and resources
constraint cumulative(y, y_dim_rot, x_dim_rot, width);
constraint cumulative(x, x_dim_rot, y_dim_rot, height);

% Non-overlapping circuits
constraint diffn(x, y, x_dim_rot, y_dim_rot);

% Symmetry breaking constraints

% Circuits which have dimensions that are the same should not be rotated
constraint symmetry_breaking_constraint(
  forall (i in CIRCUITS) (x_dim[i] = y_dim[i] -> rotation[i] = 0)
);

% Ordered circuits wrt their area
array[CIRCUITS] of int: area = [-x_dim[i] * y_dim[i] | i in CIRCUITS];
array[CIRCUITS] of int : ord_circ = sort_by(CIRCUITS, area);

% Largest rectangle is placed on the lower left wrt the second largest
constraint symmetry_breaking_constraint(
    x[ord_circ[1]] == 0 /\ y[ord_circ[1]] == 0
);

% Search

% Variables to control search heuristics and restart strategies
int: search_heur = 1;
int: restart_strat = 3;

% Search type
ann: search_ann =
  if search_heur == 1
    then int_search([height], input_order, indomain_min)
  elseif search_heur == 2
    then int_search([height], first_fail, indomain_min)
  else int_search([height], dom_w_deg, indomain_min)
  endif;

% Restart type
ann: restart_ann =
  if restart_strat == 1
    then restart_constant(750)
  elseif restart_strat == 2
    then restart_linear(20)
  elseif restart_strat == 3
    then restart_geometric(1.5, 500)
  else restart_luby(250)
  endif;

% Solve CP problem
solve :: search_ann
      :: restart_ann
      minimize height;

output ["\(width) \(height)\n\(n)\n"]
       ++ ["\(x_dim[i]) \(y_dim[i]) \(x[i]) \(y[i])"
       ++ if fix(rotation[i]) then " rotated" else "" endif
       ++ "\n"
      | i in 1..n];
