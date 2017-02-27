import numpy as np
from scipy import sqrt
from random import choice, uniform
from modules.diameter import brute_force_diameter, diam_approx
import logging
logging.basicConfig(filename='test_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class KdTree:
    """Class defining a tree characterized by :

    - data (if it(s a leaf))
    - a right subtree (None if leaf)
    - a left subtree (idem)
    - a projection on which the data will be split
    - a value of the split on this projection
    """

    def __init__(self, data=None, left=None, right=None, i=None, split=None):
        self.data = data  # np array
        self.right = right  # tree or list
        self.left = left  # tree or list
        self.i = i
        self.split = split

    def has_right_child(self):
        return not(self.right is None)

    def has_left_child(self):
        return not(self.left is None)

    def is_leaf(self):
        """Returns True if both left and right children are None"""
        return not(self.has_left_child() | self.has_right_child())

    def get_data(self):
        """Recursively returns the data associated with a tree"""
        if self.is_leaf():
            return self.data
        else:
            return np.append(self.right.get_data(),
                             self.left.get_data(), axis=0)

    def depth(self):
        """Returns the maximum depth of the tree"""
        if self.is_leaf():
            return 0
        else:
            return max(self.right.depth(), self.left.depth()) + 1

    def random_subtree(self, depth):
        """Get a random subtree at a given depth"""
        if depth == 0:
            return self
        else:
            if choice([True, False]):
                try:
                    return self.right.random_subtree(depth - 1)
                except:
                    try:
                        return self.left.random_subtree(depth - 1)
                    except:
                        raise ValueError('No node at this depth')
            else:
                try:
                    return self.left.random_subtree(depth - 1)
                except:
                    try:
                        return self.right.random_subtree(depth - 1)
                    except:
                        raise ValueError('No node at this depth')

    def diams_miner(self, depth, threshold):
        """Returns True if all cells at a given depth have a diameter
        inferior to threshold"""
        if depth == 0:
            d = brute_force_diameter(self.data)
            logging.info("        mined ratio = %f" % (.5 * d / threshold))
            if d > threshold:
                logging.info("        failure")
                return False
            else:
                logging.info("        goood")
                return True
        elif self.is_leaf():
            return True
        else:
            return (self.right.diams_miner(depth - 1, threshold) and
                    self.left.diams_miner(depth - 1, threshold))


def create(data, RM, i=0, cell_size=10, max_depth=50, jitter=0.1, depth=0):
    """Returns a kd-tree of the data

    input : data : np-array of dimension (n,d)
            RM : rotation matrix of dimension (d,d)
            cell_size : minimal number of point in a cell required to divide it
            max_depth : maximal depth of constructed tree
    """
    logging.debug('.')
    m = data.shape[0]
    n = data.shape[1]
    if ((m <= cell_size) or (depth == max_depth)):
        return KdTree(data=data)
    else:
        # Projection vector
        v = RM[:, i]
        # Projected data
        p = data.dot(v)
        # Median of data projected on this vector
        med = np.median(p)
        # Jittered split
        diam = diam_approx(data)
        eps = jitter * diam / sqrt(n)
        delta = uniform(-eps, eps)
        split = med + delta
        # Right and left sub-treess
        Sright = data[p <= split]
        Sleft = data[p > split]
        Tright = create(Sright, RM, (i + 1) % n, depth=depth + 1)
        Tleft = create(Sleft, RM, (i + 1) % n, depth=depth + 1)
        kdtree = KdTree(data, Tright, Tleft, i, split)
    return kdtree
