# KD-Tree(S,V,i).
# If |S| = 1, return S.
# 1. Let 2∆ be the diameter of S.
# 2. Let m be the median of S along v and δ be uniform random in  −6∆, 6∆ . i √n √n
# 3.S− ={x∈S : ⟨x,vi⟩≤m+δ};S+ =S\S−.
# 4.T− =KD-Tree(S−,V,i modn+1);T+ =KD-Tree(S+,V,i modn+1). 5. Return [T −, T +].

# import pandas as pd
from random import choice, uniform
import numpy as np
from scipy import sqrt, log
from scipy.stats import ortho_group
from randomRotation import randomRotation
# from sklearn.preprocessing import scale

from diameter import brute_force_diameter, diam_approx
from createTestData import createtestdata3, createtestdata2


class KdTree:
    """Classe définissant un arbre caractérisé par :
    - son diamètre
    - un sous arbre droit
    - un sous arbre gauche
    """
    def __init__(self, projection, split):
        self.projection = projection
        self.split = split
        self.children = np.empty(2)

    def add_right_child(self, obj):
        self.children.append(obj)

    def add_left_child(self, obj):
        self.children.append(obj)


def kdtreeClass(data, RM, i):
    """Returns a kd-tree of the data
    """
    print('appel')
    n = data.shape[0]
    d = data.shape[1]
    if n <= 10:
        return data
    else:
        # Projection vector
        v = RM[:, i]
        # Projected data
        p = data.dot(v)
        # Median of data projected on this vector
        m = np.median(p)
        if False:
            diam = brute_force_diameter(data)
            eps = 3 * diam / sqrt(d)
        else:
            diam = diam_approx(data)
            eps = choice([-1, 1]) * diam / sqrt(d)
        delta = uniform(-eps, eps)
        split = m + delta
        kdtree = KdTree(v, split)
        # Right and left trees
        Sminus = data[p <= split]
        Splus = data[p > split]
        Tminus = kdtree(Sminus, RM, i % (d + 1))
        Tplus = kdtree(Splus, RM, i % (d + 1))
        kdtree.add_right_child(Tminus)
        kdtree.add_left_child(Tplus)
    return kdtree


def kdtree(data, RM, i):
    """Returns a kd-tree of the data
    """
    print('appel')
    n = data.shape[0]
    d = data.shape[1]
    if n <= 10:
        return data
    else:
        # Projection vector
        v = RM[:, i]
        # Projected data
        p = data.dot(v)
        # Median of data projected on this vector
        m = np.median(p)
        if False:
            diam = brute_force_diameter(data)
            eps = 3 * diam / sqrt(d)
        else:
            diam = diam_approx(data)
            eps = choice([-1, 1]) * diam / sqrt(d)
        delta = uniform(-eps, eps)
        split = m + delta
        # Right and left trees
        Sminus = data[p <= split]
        Splus = data[p > split]
        Tminus = kdtree(Sminus, RM, i % (d + 1))
        Tplus = kdtree(Splus, RM, i % (d + 1))
    return [Tminus, Tplus]


n, d = 100, 20
# Generate test data
data = createtestdata3(n, d, 10) # Doubling dimension O(d log(n))
data = createtestdata2(n, d) # Doubling dimension log n
# Doubling dimension
dd = log(n)
diam = diam_approx(data)
RM = ortho_group.rvs(dim=data.shape[1])
RM = randomRotation(data.shape[1])
tree = kdtree(data, RM, 0)
