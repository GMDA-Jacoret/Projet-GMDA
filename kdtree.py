# KD-Tree(S,V,i).
# If |S| = 1, return S.
# 1. Let 2∆ be the diameter of S.
# 2. Let m be the median of S along v and δ be uniform random in  −6∆, 6∆ . i √n √n
# 3.S− ={x∈S : ⟨x,vi⟩≤m+δ};S+ =S\S−.
# 4.T− =KD-Tree(S−,V,i modn+1);T+ =KD-Tree(S+,V,i modn+1). 5. Return [T −, T +].

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


import pandas as pd
from random import random, choice, uniform
import numpy as np
from scipy import sqrt
from scipy.stats import ortho_group
from sklearn.preprocessing import scale

from diameter import *
from createtestdata3 import createtestdata3

def kdtree(data, RM, i):
    """Returns a kd-tree of the data
    """
    print('appel')
    n = data.shape[0]
    d = data.shape[1]
    if n <= 10:
        return data
    else :
        # Projection vector
        v = RM[:,i]
        # Projected data
        p = data.dot(v)
        # Median of data projected on this vector
        m = np.median(p)
        if False:
            diam = brute_force_diameter(data)
            eps = 3*diam/sqrt(d)
        else:
            diam = diam_approx(data)
            eps = choice([-1,1]) * diam / sqrt(d)
        delta = uniform(-eps,eps)
        split = m + delta
        kdtree = KdTree(v, split)
        # Right and left trees
        Sminus = data[p <= split]
        Splus = data[p > split]
        Tminus = kdtree(Sminus, RM, i % (d+1))
        Tplus = kdtree(Splus, RM, i % (d+1))
        kdtree.add_right_child(Tminus)
        kdtree.add_left_child(Tplus)
    return kdtree

data = createtestdata3(100, 20, 10)
diam_approx(data)
RM = ortho_group.rvs(dim=data.shape[1])

tree = kdtree(data, RM, 0)
