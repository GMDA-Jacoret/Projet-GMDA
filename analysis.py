import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
pylab.ion()

# Import data
raw = pd.read_csv("results.csv", index_col = 0)

# Preprocessing ----------------------------------------------------------------
# Group by doubling dimension and jitter
res = raw.groupby(['d', 'jit_coef'], as_index=False).mean()

# Compute and ad c1
# Retrieve number of iterations over a given couple of doubling depth and jitter split
n_iter = raw.fillna(1).groupby(['d', 'jit_coef'], as_index=False).count()['halving_depth'][0]

# Get success rate and compute c1
success_rate = raw[['d', 'jit_coef', 'halving_depth']].groupby(['d', 'jit_coef'], as_index=False).count()/n_iter
res['succ_rate'] = success_rate['halving_depth']
res['c1'] = np.log(res['m'] / (1 - res['succ_rate'])) / res['n']

# Data of type I
res_t1 = res.loc[res['test_id'] == 1]
# Data of type II
res_t2 = res.loc[res['test_id'] == 2]

# Graphical analysis -----------------------------------------------------------
# Halving depth
fig_hd, axes = plt.subplots(nrows=1, ncols=2)
for k, res in enumerate([res_t1, res_t2]):
    # halving depths
    hd_data = np.zeros((len(res['d'].unique()), len(res['jit_coef'].unique())))
    for i, e in enumerate(res['d'].unique()):
        for j, v in enumerate(res['jit_coef'].unique()):
            hd_data[i,j] = res['halving_depth'].loc[((res['jit_coef'] == v)\
                        & (res['d'] == e))]
    hd_index = res['d'].unique()
    hd_columns = res['jit_coef'].unique()
    hd_df = pd.DataFrame(hd_data, index = hd_index, columns = hd_columns)

    # plot
    hd = hd_df.plot(marker = '.', ax=axes[k],figsize=(10, 4))
    hd.set_title('Dataset of type %i' %(k+1), fontsize = 10)
    hd.set_xlabel('Doubling dimension')
    hd.set_ylabel('Halving depth')
    hd.legend(['Jit coef : 0', 'Jit coef : 1', 'Jit coef : 3'], loc = 'best', fontsize = 9)

# c0
fig_c0, axes = plt.subplots(nrows=1, ncols=2)
for k, res in enumerate([res_t1, res_t2]):

    c0_data = np.zeros((len(res['d'].unique()), 1))
    for i, e in enumerate(res['d'].unique()):
            c0_data[i,0] = res['c0'].loc[((res['jit_coef'] == 0)\
                        & (res['d'] == e))]
    c0_index = res['d'].unique()
    c0_df = pd.DataFrame(c0_data, index = c0_index)
    # plot
    c0 = c0_df.plot(marker = '.', ax=axes[k],figsize=(10, 4))
    c0.set_title('Dataset of type %i' %(k+1), fontsize = 10)
    c0.set_xlabel('Doubling dimension')
    c0.set_ylabel('c0')
    c0.legend(['Jit coef : 0', 'Jit coef : 1', 'Jit coef : 3'], loc = 'best', fontsize = 9)

# c1
fig_c1, axes = plt.subplots(nrows=1, ncols=2)
for k, res in enumerate([res_t1, res_t2]):
    c1_data = np.zeros((len(res['d'].unique()), 1))
    for i, e in enumerate(res['d'].unique()):
            c1_data[i,0] = res['c1'].loc[((res['jit_coef'] == 0)\
                        & (res['d'] == e))]
    c1_index = res['d'].unique()
    c1_df = pd.DataFrame(c1_data, index = c1_index)
    # plot
    c1 = c1_df.plot(marker = '.', ax=axes[k],figsize=(10, 4))
    c1.set_title('Dataset of type %i' %(k+1), fontsize = 10)
    c1.set_xlabel('Doubling dimension')
    c1.set_ylabel('c1')
    c1.legend(['Jit coef : 0', 'Jit coef : 1', 'Jit coef : 3'], loc = 'best', fontsize = 9)

# c2
fig_c2, axes = plt.subplots(nrows=1, ncols=2)
for k, res in enumerate([res_t1, res_t2]):
    c2_data = np.zeros((len(res['d'].unique()), len(res['jit_coef'].unique())))
    for i, e in enumerate(res['d'].unique()):
        for j, v in enumerate(res['jit_coef'].unique()):
            c2_data[i,j] = res['c2'].loc[((res['jit_coef'] == v)\
                        & (res['d'] == e))].mean(skipna = True)
    c2_index = res['d'].unique()
    c2_columns = res['jit_coef'].unique()
    c2_df = pd.DataFrame(c2_data, index = c2_index, columns = c2_columns)
    # plot
    c2 = c2_df.plot(marker = '.', ax=axes[k],figsize=(10, 4))
    c2.set_title('Dataset of type %i' %(k+1), fontsize = 10)
    c2.set_xlabel('Doubling dimension')
    c2.set_ylabel('c2')
    c2.legend(['Jit coef : 0', 'Jit coef : 1', 'Jit coef : 3'], loc = 'best', fontsize = 9)
