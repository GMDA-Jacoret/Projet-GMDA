import numpy as np
from scipy import sqrt, exp, log
from scipy.stats import ortho_group
from random import choice, uniform, random, randint

from randomRotation import randomRotation
from diameter import brute_force_diameter, diam_approx
from createTestData import createtestdata3, createtestdata2


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


def create(data, RM, i=0, cell_size=1):
    """Returns a kd-tree of the data
    """
    print('appel')
    n = data.shape[0]
    d = data.shape[1]
    if n <= 10:
        return KdTree(data=data)
    else:
        # Projection vector
        v = RM[:, i]
        # Projected data
        p = data.dot(v)
        # Median of data projected on this vector
        m = np.median(p)
        if False:
            diam = diam_approx(data)
            eps = 3 * diam / sqrt(d)
            delta = uniform(-eps, eps)
            split = m + delta
        else:
            b = random() / 2 + 0.25  # entre 1/4 et 3/4
            split = np.percentile(p, b * 100)
        # Right and left trees
        Sright = data[p <= split]
        Sleft = data[p > split]
        Tright = create(Sright, RM, i % (d+1))
        Tleft = create(Sleft, RM, i % (d+1))
        kdtree = KdTree(data, Tright, Tleft, i, split)
    return kdtree


n, d = 100, 20
# data = createtestdata3(n, d, 10)
data = createtestdata2(n, d)
# RM = ortho_group.rvs(dim=data.shape[1])
RM = randomRotation(data.shape[1])
t = create(data, RM, cell_size=5)
# Doubling dimension
dd = log(n)
# Pick a random cell
depth = randint(0, t.depth())
t1 = t.random_subtree(depth)
C = t1.get_data()
d1 = brute_force_diameter(C)

# Pick another cell at least c2*d*log(d) deeper (here random)
depth2 = randint(depth, t.depth())
Cprime = t1.random_subtree(depth2).get_data()
d2 = brute_force_diameter(Cprime)
print("D2/D1 = %f" % (d2/d1))

print("Arbre de profondeur %i créé" % t.depth())

print(str(t.get_random_cell(0,3).shape))
