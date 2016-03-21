/* 
	Capacitated VRP
	Muhammad Rafdi
	11/02/2016

  Minimise : sum of all selected paths * its respective costs

  subject to:
    1) no of vehicles entering one point must be equal to no of vehicles leaving one point
    2) no of vehicles leaving the depot must be equal to no of vehicles entering the depot
    3) Capacity constraint
*/

/* how do you define the variables */

/* Variables */
param n, integer, >= 3;

set Nodes := 1..n;

set Edges, within Nodes cross Nodes;

param cost{(i,j) in Edges};

var x{(i,j) in Edges}, binary;

minimize: optimal_distance: sum{(i,j) in E} cost[i,j] * x[i,j];

/* Constraints */

s.t. leave{i in V}: sum{(i,j) in E} x[i,j] = 1;

s.t. enter{j in V}: sum{(i,j) in E} x[i,j] = 1;

/* vehicle constraints here.. */

s.t. 

/* Subtour constraints here */

var y{(i,j) in E}, >= 0;
/* y[i,j] is the number of cars, which the salesman has after leaving
   node i and before entering node j; in terms of the network analysis,
   y[i,j] is a flow through arc (i,j) */

s.t. cap{(i,j) in E}: y[i,j] <= (n-1) * x[i,j];
/* if arc (i,j) does not belong to the salesman's tour, its capacity
   must be zero; it is obvious that on leaving a node, it is sufficient
   to have not more than n-1 cars */

s.t. node{i in V}:
/* node[i] is a conservation constraint for node i */

      sum{(j,i) in E} y[j,i]
      /* summary flow into node i through all ingoing arcs */

      + (if i = 1 then n)
      /* plus n cars which the salesman has at starting node */

      = /* must be equal to */

      sum{(i,j) in E} y[i,j]
      /* summary flow from node i through all outgoing arcs */

      + 1;
      /* plus one car which the salesman sells at node i */


solve;

printf "The sum of optimal tours is...\n";

data;

/* VRP dataset, the depot is 1, the optimal solution is 29, given 3 different routes */

param n := 9;

param vehicles

param : E : cost :=
  1  2  2
  1  3  10
  1  4  2
  1  5  3
  1  6  3
  1  7  4
  1  8  10
  1  9  4
  2  1  2
  2  3  2
  2  4  10
  2  5  10
  2  6  10
  2  7  10
  2  8  10
  2  9  10
  3  1  10
  3  2  2
  3  4  2
  3  5  10
  3  6  10
  3  7  10
  3  8  10
  3  9  10
  4  1  2
  4  2  10
  4  3  2
  4  5  10
  4  6  10
  4  7  10
  4  8  10
  4  9  10
  5  1  3
  5  2  10
  5  3  10
  5  4  10
  5  6  3
  5  7  10
  5  8  10
  5  9  10
  6  1  3
  6  2  10
  6  3  10
  6  4  10
  6  5  3
  6  7  10
  6  8  10
  6  9  10
  7  1  4
  7  2  10
  7  3  10
  7  4  10
  7  5  10
  7  6  10
  7  8  4
  7  9  10
  8  1  10
  8  2  10
  8  3  10
  8  4  10
  8  5  10
  8  6  10
  8  7  4
  8  9  4
  9  1  4
  9  2  10
  9  3  10
  9  4  10
  9  5  10
  9  6  10
  9  7  10
  9  8  4
;

end;
