# KD-Tree(S,V,i).
# If |S| = 1, return S.
# 1. Let 2∆ be the diameter of S.
# 2. Let m be the median of S along v and δ be uniform random in  −6∆, 6∆ . i √n √n
# 3.S− ={x∈S : ⟨x,vi⟩≤m+δ};S+ =S\S−.
# 4.T− =KD-Tree(S−,V,i modn+1);T+ =KD-Tree(S+,V,i modn+1). 5. Return [T −, T +].

# class KdTree:
#     """Classe définissant un arbre caractérisé par :
#     - son diamètre
#     - un sous arbre droit
#     - un sous arbre gauche
#     """
#     def __init__(self, data):
#         self.data = data
#         self.diam = diameter(data)
#
#
#     def get_diameter(self):
#         diameter()

import pandas as pd
import random
import numpy as np
import scipy
from scipy.stats import ortho_group
from sklearn.preprocessing import scale

from diameter import brute_force_diameter
from createtestdata3 import createtestdata3
compt = 1

def kdtree(data, RM, i):
    """Returns a kd-tree of the data
    """
    print('%i appel' % compt)
    n = data.shape[0]
    d = data.shape[0]
    if n == 1:
        return data
    else :
        diam = brute_force_diameter(data)
        eps = 3*diam/scipy.sqrt(n)
        delta = random.uniform(-eps,eps)
        # Rotate the data
        M = data.dot(RM)
        # Projection vector
        v = RM[:,i]
        # Median of data projected on this vector
        m = np.median(M[:,i])
        # Right and left trees
        Sminus = data[M[:,i] <= m+delta]
        Splus = data[M[:,i] > m+delta]
        Tminus = kdtree(Sminus, RM, i % (d+1))
        Tplus = kdtree(Splus, RM, i % (d+1))
    return [Tminus, Tplus]

data = createtestdata3(100, 20, 10)
RM = ortho_group.rvs(dim=data.shape[1])

kdtree(data, RM, 0)
