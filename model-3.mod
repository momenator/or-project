/* 
	VRP with subtour elimination
	Muhammad Rafdi
	02/02/2016
*/

/* Number of nodes */
param n, integer, >=3;

/* Set of vertices */
set V := 1..n;

/* Set of edges */
set E, within V cross V;

/* Artificial Set of vertices for subtour formulation */
set S, within V cross V;

/* Set of costs */
param cost{(i,j) in E};

/* Path variable x, x=1 if there is a path from i to j in the optimal tour, 0 otherwise */
var x{(i,j) in E}, binary;

/* Objective function */
minimize tour_distance: sum{(i,j) in E} cost[i, j] * x[i,j];

/* Salesman leaves and enters a node exactly once */
s.t. leave{i in V}: sum{(i, j) in E} x[i,j] = 1;
s.t. enter{j in V}: sum{(i, j) in E} x[i,j] = 1;

/* Vehicle constraints */
s.t. leaveDepot{i in V}: sum{(i,j) in E} x[i, 1] = 3;
s.t. enterDepot{j in V}: sum{(i,j) in E} x[1, j] = 3;

/* subtour formulation */
/* Network flow analysis, flow[i,j] is the flow through arc i to j*/
var flow{(i,j) in E}, >= 0;

/* flow from i to j should be <= n-1 */
s.t. capacity{(i,j) in E}: flow[i,j] <= (n-1) * x[i,j];

/* network flow constraint to eliminate subtours */
s.t. node{i in V}: sum{(j,i) in E} flow[j,i] + (if i = 1 then n) = sum{(i,j) in E} flow[i,j] + 1;


solve;

printf "Optimal tour has length %d\n", sum{(i,j) in E} cost[i,j] * x[i,j];

data;

/* VRP dataset, the depot is 1, the optimal solution is  */

param n := 9;

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
