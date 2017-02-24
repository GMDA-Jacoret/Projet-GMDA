import numpy as np
from random import sample, randint

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
