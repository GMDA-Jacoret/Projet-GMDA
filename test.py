# Où l'on mesure le diamètre de feuilles.


from randomRotation import randomRotation
from diameter import brute_force_diameter, diam_approx
from testFunctions import *
from kdtree import *
import numpy as np


D = [2, 5, 10]
N = np.multiply(D,100)

Data1 = np.empty(len(D), dtype = object)
Data2 = np.empty(len(D), dtype = object)
for i in range(0,len(D)):
    Data1[i] = createTD1(N[i], D[i])
    #Data2[i] = createTD2(N[i], D[i], np.floor(D[i]/2))

Jit = [0.01, 0.1, 1, 3, 10]

Results = np.empty((len(D), len(Jit)), dtype = object)

for i, data in enumerate(Data1):
    print("\nDataset de dimensions (%i,%i)"%(data.shape[0], data.shape[1]))
    print("*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  * ")
    for j, jit in enumerate(Jit):
        print("\njit coeff : %.2f" %jit)
        Results[i,j] = testTree(data, cell_size=10, max_depth=10, jit=jit)

Results
