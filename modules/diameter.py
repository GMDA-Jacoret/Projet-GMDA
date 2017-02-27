# -*- coding : utf8 -*-

import numpy as np
from random import choice


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


def diam_approx(data):
    """Rough approximation of diameter

    Input : scaled numpy array
    Output : diameter (float)
    """
    x = choice(data)
    diam = 0
    for y in data:
        if np.linalg.norm(x-y) > diam:
            diam = np.linalg.norm(x-y)
    return diam
