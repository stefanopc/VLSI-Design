% VLSI Design - CP base model

include "globals.mzn"; 
include "diffn.mzn";
include "cumulative.mzn";

% Input variables

int: width; % plate width
int: n; % number of circuits
set of int: CIRCUITS = 1..n;

% array of circuits widths
array[CIRCUITS] of int: x_sizes;
% array of circuits heights
array[CIRCUITS] of int: y_sizes;

% Other variables

% Plate bounds
int: lowb = max(y_sizes); % lower bound (max circuit height)
int: upb = sum(y_sizes); % upper bound (sum of circuits heights)

% Output variables

% Horizontal coordinate of circuits
array[CIRCUITS] of var 0..width-1: x;
% Vertical coordinate of circuits
array[CIRCUITS] of var 0..sum(y_sizes)-1: y;

% Height of plate that ranges from lower to upper bound, to minimize
var lowb..upb: height;
height = max([y[i] + y_sizes[i] | i in CIRCUITS]);

% Domain reduction
constraint forall(i in CIRCUITS) (x[i] <= width - x_sizes[i])::domain;
constraint forall(i in CIRCUITS) (y[i] <= height - y_sizes[i])::domain;

% Constraints

% max width
constraint max([x[i] + x_sizes[i] | i in CIRCUITS]) <= width;

% max height
constraint max([y[i] + y_sizes[i] | i in CIRCUITS]) <= upb;

% Global constraints

% Cumulative constraint: circuits as activities with d=height and r=width
constraint cumulative(y, y_sizes, x_sizes, width);
constraint cumulative(x, x_sizes, y_sizes, height);

% Non-overlapping circuits
constraint diffn(x, y, x_sizes, y_sizes);

% Symmetry breaking constraints

% Ordered circuits wrt their area
array[CIRCUITS] of int: area = [-x_sizes[i] * y_sizes[i] | i in CIRCUITS];
array[CIRCUITS] of int : ord_circ = sort_by(CIRCUITS, area);

% Largest rectangle is placed on the lower left wrt the second largest
constraint symmetry_breaking_constraint(
    let {
        int: c1 = ord_circ[1], int: c2 = ord_circ[2]
    } in lex_lesseq([y[c1],x[c1]], [y[c2],x[c2]])
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
       ++ ["\(x_sizes[i]) \(y_sizes[i]) \(x[i]) \(y[i])"
       ++ "\n"
      | i in 1..n];