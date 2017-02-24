import numpy as np
from random import sample, randint
from randomRotation import randomRotation
from kdtree import *
from diameter import brute_force_diameter, diam_approx


def createTD1(n, d):
    """Creates a data set for which each point belongs to one of the [-1,1] segment along the axises

    n : number of points
    d : number of coordinates
    """
    test1 = np.zeros((n, d))
    for i in range(test1.shape[0]):
        axis = randint(0, d - 1)
        test1[i, axis] = 2 * np.random.rand() - 1
    return test1

def createTD2(n, d, k):
    """Creates a data set for which each point has at most k nonzeros coordinates

    n : number of points
    d : number of coordinates
    k : maximum number of nonzero coordinates (must be < d)
    """
    if k > d:
        raise ValueError("Number of non-zero coordinates must be inferior to the"
                         "number of coordinates")

    test2 = np.zeros((n, d))
    for i in range(test2.shape[0]):
        n_nonzero = randint(0, k)
        nonzeros = sample(range(d), n_nonzero)
        test2[i, nonzeros] = np.random.rand(n_nonzero)
    return test2

def testTree(data, cell_size, max_depth, jit):
    print("La graine est plantée.")
    RM = randomRotation(data.shape[1])
    t = create(data, RM, cell_size=cell_size, max_depth=max_depth, jit = jit, )
    total_depth = t.depth()
    print("\nUn arbre de profondeur %i a poussé" % total_depth)

    # Pick a random cell in first half of the tree
    depth1 = randint(0, np.floor(total_depth/2))
    d1=0
    while d1 == 0:
        t1 = t.random_subtree(depth1)
        C = t1.get_data()
        d1 = brute_force_diameter(C)
    print("Diamètre à la profondeur %i : %f "%(depth1,d1))

    # Find the cell that halves the diameter by randomly going down the tree
    depth2 = 1
    ratio = 1
    t2 = t1.random_subtree(1)
    while ((ratio >.5) and (total_depth-depth2 >= 0)):
        Cprime = t2.get_data()
        d2 = brute_force_diameter(Cprime)
        ratio = d2/d1
        print("Ratio %i noeuds plus loin : %f "%(depth2,ratio), end="")
        if ratio <= 0.5:
            print(" ==>  c'est un BINGO !")
        else:
            print("")
        depth2 += 1
        t2 = t2.random_subtree(1)

    # Save result
    return [depth1, depth2, ratio]
