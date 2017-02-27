# -*- coding : utf8 -*-

import numpy as np
import unittest


def randomRotation(n_dim):
    """Generates a random rotation matrix

    Input : dimension of the data
    Output : a random rotation matrix of that dimension
    """

    # Generate Normally distributed vectors
    randVects = np.random.normal(0, 1, (n_dim, n_dim))
    # Normalize them to unit sphere
    norms = np.linalg.norm(randVects, axis=0)
    normVects = np.divide(randVects, norms)

    # Gram-Schmidt using the QR decomposition
    # rotationMatrix = np.linalg.qr(normVects)[0]

    # Custom Gram-Schmidt
    gsBasis = []
    for v in normVects.T:
        u = v - np.sum(np.dot(v, e) * e for e in gsBasis)
        gsBasis.append(u / np.linalg.norm(u))
    rotationMatrix = np.array(gsBasis).T

    return rotationMatrix


# --- Tests ---

class TestRandomRotation(unittest.TestCase):
    """Tests the randomRotation function"""
    def test_RM_1(self):
        a = randomRotation(3)
        np.linalg.det(a)
        np.linalg.norm(a, axis=0)
        errors = sum(sum(a.dot(a.T) - np.identity(3) > 1e-10))
        self.assertEqual(errors, 0)

    def test_RM_2(self):
        b = randomRotation(22)
        np.linalg.det(b)
        np.linalg.norm(b, axis=0)
        errors = sum(sum(b.dot(b.T) - np.identity(22) > 1e-10))
        self.assertEqual(errors, 0)


if __name__ == '__main__':
    unittest.main()
