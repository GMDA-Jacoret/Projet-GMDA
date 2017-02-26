import numpy as np
from scipy import sqrt, exp, log
from scipy.stats import ortho_group
from random import choice, uniform, random, randint
from diameter import brute_force_diameter, diam_approx
import logging
logging.basicConfig(filename='test_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
                        raise ValueError('Pas de noeud à cette profondeur')
            else:
                try:
                    return self.left.random_subtree(depth - 1)
                except:
                    try:
                        return self.right.random_subtree(depth - 1)
                    except:
                        raise ValueError('Pas de noeud à cette profondeur')

    def get_brute_force_diameter(self):
        return brute_force_diameter(self.get_data())

    def diams_explorer(self, depth):
        if depth == 0:
            return self
        else:
            try:
                return self.left.diams_explorer(depth - 1)
            except:
                try:
                    return self.right.random_subtree(depth - 1)
                except:
                    raise ValueError('Pas de noeud à cette profondeur')

    def diams_miner(self, depth, threshold):
        if depth == 0:
            d = brute_force_diameter(self.data)
            logging.info("        mined ratio = %f" % (.5*d/threshold))
            if d > threshold:
                logging.info("        failure")
                return False
            else:
                logging.info("        goood")
                return True
        elif self.is_leaf():
            return True
        else:
            return (self.right.diams_miner(depth - 1, threshold) and self.left.diams_miner(depth - 1, threshold))

def create(data, RM, i=0, cell_size=10, max_depth=15, jitter=0.1, depth=0):
    """Returns a kd-tree of the data
    """
    logging.debug('.')
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
            eps = jitter * diam / sqrt(d)
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
