import numpy as np
from random import sample, randint
from modules.randomRotation import randomRotation
from modules.kdtree import KdTree, create
from modules.diameter import brute_force_diameter
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
    logging.info(">>> DS of dim (%i,%i) and jit coeff %.2f"
                 % (data.shape[0], data.shape[1], jit))

    RM = randomRotation(data.shape[1])
    t = create(data, RM, cell_size=cs, max_depth=md, jitter=jit, )
    total_depth = t.depth()
    logging.info("    Tree of size %i has grown." % total_depth)

    # Pick a random node in first half of the tree that is not a leaf and
    # with non-zero diameter
    depth1 = randint(0, np.floor(total_depth / 2))
    t1 = KdTree()
    d1 = 0
    while (d1==0 or t1.is_leaf()):
        logging.info("    *")
        t1 = t.random_subtree(depth1)
        C = t1.get_data()
        d1 = brute_force_diameter(C)
        depth1 = randint(0, np.floor(total_depth / 2))

    logging.info("    Diameter at depth %i : %f " % (depth1, d1))

    # Find a depth with a cell that halves the diameter by randomly going down the tree
    additional_depth = 1
    depth2 = t1.depth()
    logging.info("    Depth of chosen subtree %i" % depth2)

    ratio = 1
    while (additional_depth <= depth2):
        try:
            t2 = t1.random_subtree(additional_depth)
        except ValueError:
            logging.info("==> Failed!")
            return [depth1, None, None]
        Cprime = t2.get_data()
        d2 = brute_force_diameter(Cprime)
        ratio = d2 / d1
        logging.info("    Ratio %i nodes deeper : %f"
                     % (additional_depth, ratio))


        if (ratio <= .5):
            # Explore obtained depth
            bingo = t1.diams_miner(additional_depth, .5*d1)
            if bingo:
                logging.info("==> it's a BINGO!")
                return [depth1, additional_depth]

        additional_depth += 1

    logging.info("==> Reached max depth")
    # Save result
    return [depth1, None]
