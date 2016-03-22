/* 
	TSP problem with MTZ subtour elimination
	Muhammad Rafdi
	01/02/2016
*/

/* Number of nodes */
param n, integer, >=3;

/* Set of vertices */
set V := 1..n;

/* Set of edges */
set E, within V cross V;

/* Set of costs */
param cost{(i,j) in E};

/* Path variable x, x=1 if there is a path from i to j in the optimal tour, 0 otherwise */
var x{(i,j) in E}, binary;

/* Artificial variable u, for subtour elimination */
var u {i in V}, >=1;

/* Objective function */
minimize tour_distance: sum{(i,j) in E} cost[i, j] * x[i,j];

/* Salesman leaves and enters a node exactly once */
s.t. leave{i in V}: sum{(i, j) in E} x[i,j] = 1;
s.t. enter{j in V}: sum{(i, j) in E} x[i,j] = 1;

/* MTZ subtour formulation */
s.t. subtour_constraint_1: u[1] = 1;
s.t. subtour_constraint_2{(i,j) in E}: 2 <= u[i] <= n;
s.t. subtour_constraint_3{(i, j) in E}: u[i] - u[j] + 1 <= (n - 1) * (1 - x[i,j]);

solve;

printf "Optimal tour has length %d\n", sum{(i,j) in E} cost[i,j] * x[i,j];

data;

/* Sample data set, optimal solution is 17 */

param n := 4;

param : E : cost :=
	1  2  4
	1  3  5
	1  4  7
	2  1  4
	2  3  6
	2  4  5
	3  1  5
	3  2  6
	3  4  3
	4  1  7
	4  2  5
	4  3  3
;

end;


/* These data correspond to the symmetric instance ulysses16 from:

   Reinelt, G.: TSPLIB - A travelling salesman problem library.
   ORSA-Journal of the Computing 3 (1991) 376-84;
   http://elib.zib.de/pub/Packages/mp-testdata/tsp/tsplib */

/* The optimal solution is 6859 */

/*
param n := 16;

param : E : cost :=
    1  2   509
    1  3   501
    1  4   312
    1  5  1019
    1  6   736
    1  7   656
    1  8    60
    1  9  1039
    1 10   726
    1 11  2314
    1 12   479
    1 13   448
    1 14   479
    1 15   619
    1 16   150
    2  1   509
    2  3   126
    2  4   474
    2  5  1526
    2  6  1226
    2  7  1133
    2  8   532
    2  9  1449
    2 10  1122
    2 11  2789
    2 12   958
    2 13   941
    2 14   978
    2 15  1127
    2 16   542
    3  1   501
    3  2   126
    3  4   541
    3  5  1516
    3  6  1184
    3  7  1084
    3  8   536
    3  9  1371
    3 10  1045
    3 11  2728
    3 12   913
    3 13   904
    3 14   946
    3 15  1115
    3 16   499
    4  1   312
    4  2   474
    4  3   541
    4  5  1157
    4  6   980
    4  7   919
    4  8   271
    4  9  1333
    4 10  1029
    4 11  2553
    4 12   751
    4 13   704
    4 14   720
    4 15   783
    4 16   455
    5  1  1019
    5  2  1526
    5  3  1516
    5  4  1157
    5  6   478
    5  7   583
    5  8   996
    5  9   858
    5 10   855
    5 11  1504
    5 12   677
    5 13   651
    5 14   600
    5 15   401
    5 16  1033
    6  1   736
    6  2  1226
    6  3  1184
    6  4   980
    6  5   478
    6  7   115
    6  8   740
    6  9   470
    6 10   379
    6 11  1581
    6 12   271
    6 13   289
    6 14   261
    6 15   308
    6 16   687
    7  1   656
    7  2  1133
    7  3  1084
    7  4   919
    7  5   583
    7  6   115
    7  8   667
    7  9   455
    7 10   288
    7 11  1661
    7 12   177
    7 13   216
    7 14   207
    7 15   343
    7 16   592
    8  1    60
    8  2   532
    8  3   536
    8  4   271
    8  5   996
    8  6   740
    8  7   667
    8  9  1066
    8 10   759
    8 11  2320
    8 12   493
    8 13   454
    8 14   479
    8 15   598
    8 16   206
    9  1  1039
    9  2  1449
    9  3  1371
    9  4  1333
    9  5   858
    9  6   470
    9  7   455
    9  8  1066
    9 10   328
    9 11  1387
    9 12   591
    9 13   650
    9 14   656
    9 15   776
    9 16   933
   10  1   726
   10  2  1122
   10  3  1045
   10  4  1029
   10  5   855
   10  6   379
   10  7   288
   10  8   759
   10  9   328
   10 11  1697
   10 12   333
   10 13   400
   10 14   427
   10 15   622
   10 16   610
   11  1  2314
   11  2  2789
   11  3  2728
   11  4  2553
   11  5  1504
   11  6  1581
   11  7  1661
   11  8  2320
   11  9  1387
   11 10  1697
   11 12  1838
   11 13  1868
   11 14  1841
   11 15  1789
   11 16  2248
   12  1   479
   12  2   958
   12  3   913
   12  4   751
   12  5   677
   12  6   271
   12  7   177
   12  8   493
   12  9   591
   12 10   333
   12 11  1838
   12 13    68
   12 14   105
   12 15   336
   12 16   417
   13  1   448
   13  2   941
   13  3   904
   13  4   704
   13  5   651
   13  6   289
   13  7   216
   13  8   454
   13  9   650
   13 10   400
   13 11  1868
   13 12    68
   13 14    52
   13 15   287
   13 16   406
   14  1   479
   14  2   978
   14  3   946
   14  4   720
   14  5   600
   14  6   261
   14  7   207
   14  8   479
   14  9   656
   14 10   427
   14 11  1841
   14 12   105
   14 13    52
   14 15   237
   14 16   449
   15  1   619
   15  2  1127
   15  3  1115
   15  4   783
   15  5   401
   15  6   308
   15  7   343
   15  8   598
   15  9   776
   15 10   622
   15 11  1789
   15 12   336
   15 13   287
   15 14   237
   15 16   636
   16  1   150
   16  2   542
   16  3   499
   16  4   455
   16  5  1033
   16  6   687
   16  7   592
   16  8   206
   16  9   933
   16 10   610
   16 11  2248
   16 12   417
   16 13   406
   16 14   449
   16 15   636
;
*/
end;

