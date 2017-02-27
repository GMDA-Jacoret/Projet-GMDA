# Random oriented kd-trees and adaptation to intrinsic dimension

## Introduction

The goal of this project is to study the efficiency of \textit{kd-trees} as data structures. In particular we aim at providing evidence that randomly rotating the data before storing it allows for such structures to adapt to its intrinsic dimension.

## How to run

The file `test.py` runs tests on several test datasets generated thanks to functions in `testFunctions.py`. You may vary the dimension of the datasets, the width of the jittered split, and run several iterations to observe the effect of random jittered split.

Functions required to create the k-d tree from a given data set are in `kdtree.py`.
Various functions required in the algorithm are in `diameter.py`and `randomRotation.py`


## Output

Results are outputted into `results.csv`. It contains several fields : `test_id, n, d, jit_coef, picked_depth, halving_depth, dd, c0, c2`
- `test_id` : kind of dataset which has been generated
- `n`, d : shape of the dataset
- `jit_coef` : coefficient of the jittered split width
- `picked_depth` : depth of the cell randomly picked among the tree
- `halving_depth` : additionnal depth for which all cells have a diameter at least 2 times smaller than picked cell's diameter
- `dd` : doubling dimension of the dataset
- `c0` : `dd*log(dd)/d`, value that we try to prove is bounded
- `c2` : `dd*log(dd)/halving_depth`, idem

Log of the test algorithm is stored in `test_log.txt`

Output is analysed in `analysis.py`.



