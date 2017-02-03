# -*- coding : utf8 -*-

import pandas as pd
import scipy as sp
import numpy as np

from sklearn.preprocessing import scale

data = pd.read_csv('data.csv')
data = data.as_matrix()
data = scale(data)

def brute_force_diameter(data):
    """Computes the exact diameter using brute force computation

    Input : scaled numpy array
    Output : diameter (float)
    """
    diam = 0
    for line in data:
        for other_line in data:
            dist = np.linalg.norm(line-other_line)
            if dist > diam:
                diam = dist
    return diam

# Wall time 1min53s
