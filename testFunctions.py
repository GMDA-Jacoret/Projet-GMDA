import numpy as np
from random import sample, randint
from randomRotation import randomRotation
from kdtree import KdTree, create
from diameter import brute_force_diameter
import logging
logging.basicConfig(filename='test_log.txt', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def createTD1(n, d):
    """Creates a data set for which each point belongs to
    one of the [-1,1] segment along the axises

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
        raise ValueError("Number of non-zero coordinates must be inferior to"
                         " the number of coordinates")

    test2 = np.zeros((n, d))
    for i in range(test2.shape[0]):
        n_nonzero = randint(0, k)
        nonzeros = sample(range(d), n_nonzero)
        test2[i, nonzeros] = np.random.rand(n_nonzero)
    return test2


def testTree(data, cs, md, jit):
    """Tests the results of the theorem on a given point set by picking a
    random cell and randomly travel down the tree to find the cell that halves
    the diameter of the initially picked cell.
    """
    logging.info("> Dataset de dimensions (%i,%i) et jit coeff %.2f"
                 % (data.shape[0], data.shape[1], jit))
    logging.info("La graine est plantée.")
    RM = randomRotation(data.shape[1])
    t = create(data, RM, cell_size=cs, max_depth=md, jitter=jit, )
    total_depth = t.depth()
    logging.info("\nUn arbre de profondeur %i a poussé" % total_depth)

    # Pick a random cell in first half of the tree
    depth1 = randint(0, np.floor(total_depth / 2))
    d1 = 0
    t1 = KdTree()
    while (d1 == 0 or t1.is_leaf()):
        t1 = t.random_subtree(depth1)
        C = t1.get_data()
        d1 = brute_force_diameter(C)
    logging.info("Diamètre à la profondeur %i : %f " % (depth1, d1))

    # Find the cell that halves the diameter by randomly going down the tree
    additional_depth = 1
    depth1 = t1.depth()
    ratio = 1
    while ((ratio > .5) and (additional_depth <= depth1)):
        try:
            t2 = t1.random_subtree(additional_depth)
        except ValueError:
            logging.error("oooh noooooooooon.")
            return [depth1, None, None]
        Cprime = t2.get_data()
        d2 = brute_force_diameter(Cprime)
        ratio = d2 / d1
        logging.info("Ratio %i noeuds plus loin : %f"
                     % (additional_depth, ratio))
        additional_depth += 1

    # Save result
    logging.info(" ==>  c'est un BINGO !")
    return [depth1, additional_depth, ratio]
