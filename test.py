# Où l'on mesure le diamètre de feuilles.


from testFunctions import createTD1, createTD2, testTree
from kdtree import create
from scipy import log
import numpy as np
import pandas as pd
import logging
logging.basicConfig(filename='log_filename.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# --- Variables à itérer ---

D = [2, 5, 10, 20, 50, 100]
# N = np.multiply(D, 100)
Jit = [0.01, 0.1, 1, 3, 10]


# Data1 = np.empty(len(D), dtype=object)
# Data2 = np.empty(len(D), dtype=object)
# for i in range(0, len(D)):
#     # Data1[i] = createTD1(N[i], D[i])
#     Data2[i] = createTD2(N[i], D[i], np.floor(D[i]/2))


# Results = np.empty((len(D), len(Jit)), dtype=object)
results = pd.DataFrame(columns=['test_id', 'n', 'd', 'picked_depth',
                                'halving_depth', 'ratio'])


compt = 1

for test_id in [1, 2]:
    for d in D:

        n = 100 * d
        if test_id == 1:
            data = createTD1(n, d)
        elif test_id == 2:
            data = createTD2(n, d, np.floor(d/2))

        print("\nDataset de dimensions (%i,%i)" % (data.shape[0], data.shape[1]))
        print("*  *  *  *  *  *  *  *  *  *  *  *  *  *  "
              "*  *  *  *  *  *  *  *  *  *  * ")

        for j, jit in enumerate(Jit):
            # print("\njit coeff : %.2f" % jit)
            # Results[i, j] = testTree(data, cell_size=10, max_depth=10, jit=jit)
            testresults = testTree(data, cell_size=10, max_depth=10, jit=jit)
            test_info = np.append(test_id, data.shape)
            results.loc[compt] = np.append(test_info, testresults)
            compt += 1


# Doubling dimension

results.loc[results.test_id == 1,
            'dd'] = log(results.loc[results.test_id == 1, 'n'])

results.loc[results.test_id == 2,
            'dd'] = np.floor(d/2)*log(results.loc[results.test_id == 2, 'n'])

logging.info('\n'.join([''.join(['{:40}'.format("Start=" + str(item[0]) +
             " Reached_at=" + str(item[1]) +
             " Ratio=" + str('%.2f' % item[2])) for item in row]) for row in Results]))

# Constantes
results['c0'] = results.dd * log(results.dd) / results.n
results['c2'] = results.halving_depth / results.dd*log(results.dd)

# Export
results.to_csv('results.csv')
