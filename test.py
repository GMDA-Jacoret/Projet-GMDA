# Où l'on mesure le diamètre de feuilles.


from randomRotation import randomRotation
from diameter import brute_force_diameter, diam_approx
from createTestData import createTD1, createTD2
from kdtree import *
import numpy as np


D = [2, 5, 10, 20, 50]
N = np.multiply(D,100)

Data1 = np.empty(len(D), dtype = object)
Data2 = np.empty(len(D), dtype = object)
for i in range(0,len(D)):
    Data1[i] = createTD1(N[i], D[i])
    #Data2[i] = createTD2(N[i], D[i], np.floor(D[i]/2))

Jit = [0.0001, 0.001, 0.01, 0.1, 1, 10]

Results = np.empty((len(D), len(Jit)))

for i, data in enumerate(Data1):
    print("\nDataset de dimensions (%i,%i)"%(data.shape[0], data.shape[1]))
    print("===============================")
    for j, jit in enumerate(Jit):
        print("\njit coeff : %f, la graine est plantée." %jit)
        RM = randomRotation(data.shape[1])
        t = create(data, RM, cell_size=5, jit = 2)
        print("\nUn arbre de profondeur %i a poussé" % t.depth())
        # Pick a random cellin first half of the tree
        depth = randint(0, np.floor(t.depth()/2))
        t1 = t.random_subtree(depth)
        C = t1.get_data()
        d1 = brute_force_diameter(C)
        print("Diamètre à la profondeur %i : %f "%(depth,d1))
        if d1 == 0:
            print("échec")
        else:
            # Pick another cell at least c2*d*log(d) deeper (here random)
            depth2 = randint(1, t.depth()-depth)
            Cprime = t1.random_subtree(depth2).get_data()
            d2 = brute_force_diameter(Cprime)
            print("Diamètre %i noeuds plus loin : %f "%(depth2,d2))
            print("D2/D1 = %f..." % (d2/d1), end="")
            if d2/d1 >0.5:
                print("  oh non")
            else:
                print("  c'est un BINGO !")
            Results[i,j] = d2/d1

Results
