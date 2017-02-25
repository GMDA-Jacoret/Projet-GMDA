import numpy as np
from scipy import sqrt, exp, log
from scipy.stats import ortho_group
from random import choice, uniform, random, randint
from diameter import brute_force_diameter, diam_approx
import logging
logging.basicConfig(filename='log_filename.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class KdTree:
    """Classe définissant un arbre caractérisé par :

    - des données (si c'est une feuille)
    - un sous arbre droit (None si c'est une feuille)
    - un sous arbre gauche (idem)
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
        return not(self.has_left_child() | self.has_right_child())

    def get_data(self):
        if self.is_leaf():
            return self.data
        else:
            return np.append(self.right.get_data(), self.left.get_data(), axis=0)

    def depth(self):
        """Returns the maximum depth of the tree"""
        if self.is_leaf():
            return 0
        else:
            return max(self.right.depth(), self.left.depth()) + 1

    def random_subtree(self, depth):
        """Get a random subtree at a given depth"""
        if self.is_leaf():
            return self
        else:
            if depth == 0:
                return self
            else:
                if choice([True, False]):
                    if self.has_right_child():
                        return self.right.random_subtree(depth - 1)
                    else:
                        return self
                else:
                    if self.has_left_child():
                        return self.left.random_subtree(depth - 1)
                    else:
                        return self

    def get_brute_force_diameter(self):
        return brute_force_diameter(self.get_data())


def create(data, RM, i=0, cell_size=10, max_depth=15, jit=0.1, depth=0):
    """Returns a kd-tree of the data
    """
    logging.debug('.', end="")
    n = data.shape[0]
    d = data.shape[1]
    if ((n <= cell_size) or (depth == max_depth)):
        return KdTree(data=data)
    else:
        # Projection vector
        v = RM[:, i]
        # Projected data
        p = data.dot(v)
        # Median of data projected on this vector
        m = np.median(p)
        if True:
            diam = diam_approx(data)
            eps = jit * diam / sqrt(d)
            delta = uniform(-eps, eps)
            split = m + delta
        else:
            b = random() / 2 + 0.25  # entre 1/4 et 3/4
            split = np.percentile(p, b * 100)
        # Right and left trees
        Sright = data[p <= split]
        Sleft = data[p > split]
        Tright = create(Sright, RM, (i+1)%d, depth = depth+1)
        Tleft = create(Sleft, RM, (i+1)%d, depth = depth+1)
        kdtree = KdTree(data, Tright, Tleft, i, split)
    return kdtree
