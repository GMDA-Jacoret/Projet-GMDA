import numpy as np
from random import sample, randint


def createtestdata3(n, d, k):
    """Creates a data set for which each point has at most k nonzeros coordinates

    n : number of points
    d : number of coordinates
    k : maximum number of nonzero coordinates (must be < d)
    """

    if k > d:
        raise ValueError("Number of non-zero coordinates must be inferior to the"
                         "number of coordinates")

    test3 = np.zeros((n, d))

    for i in range(test3.shape[0]):
        n_nonzero = randint(0, k)
        nonzeros = sample(range(d), n_nonzero)
        test3[i, nonzeros] = np.random.rand(n_nonzero)

    return test3


test3 = createtestdata3(100, 20, 10)


def createtestdata2(n, d):
    """Creates a data set for which each point belongs to one of the [-1,1] segment along the axises

    n : number of points
    d : number of coordinates
    """

    test2 = np.zeros((n, d))
    for i in range(test2.shape[0]):
        axis = randint(0, d - 1)
        test2[i, axis] = 2 * np.random.rand() - 1
    return test2


test2 = createtestdata2(100, 5)
