# Où l'on mesure le diamètre de feuilles.

from testFunctions import createTD1, createTD2, testTree
from kdtree import create
from scipy import log
import numpy as np
import pandas as pd
import logging
logging.basicConfig(filename='test_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Variables à itérer ---
D = [2, 5, 10]#, 20, 50, 100]
Jit = [0.01, 0.1, 1, 3]#, 10]

# Results = np.empty((len(D), len(Jit)), dtype=object)
results = pd.DataFrame(columns=['test_id', 'n', 'd', 'jit_coef',  'picked_depth',
                                'halving_depth', 'ratio'])

compt = 1
for test_id in [1, 2]:
    for d in D:
        n = 100 * d
        if test_id == 1:
            data = createTD1(n, d)
        elif test_id == 2:
            data = createTD2(n, d, np.floor(d/2))

        for j, jit in enumerate(Jit):
            print("Dataset de type %i, dimensions (%i,%i) et jit coeff %.2f... " % (test_id, data.shape[0], data.shape[1], jit), end="")
            testresults = testTree(data, cs=10, md=10, jit=jit)
            test_info = np.append(np.append(test_id, data.shape),jit)
            results.loc[compt] = np.append(test_info, testresults)
            compt += 1
            print("done.\n")

# Doubling dimension
results.loc[results.test_id == 1,
            'dd'] = log(results.loc[results.test_id == 1, 'n'])

results.loc[results.test_id == 2,
            'dd'] = np.floor(d/2)*log(results.loc[results.test_id == 2, 'n'])

# Constantes
results['c0'] = results.dd * log(results.dd) / results.n
results['c2'] = results.halving_depth / results.dd*log(results.dd)

# Export
results[['test_id', 'n', 'd', 'picked_depth', 'halving_depth']] = results[['test_id', 'n', 'd', 'picked_depth', 'halving_depth']].astype(int)
results.to_csv('results.csv')
