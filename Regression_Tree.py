import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
import math
import warnings
warnings.filterwarnings("ignore")
import glob
from preprocess import *

df = get_preproccess_data()

for i in range(1,2):
    print('House {} data has shape: '.format(i), df[i].shape)

dates = {}
for i in range(1,2):
    dates[i] = [str(time)[:10] for time in df[i].index.values]
    dates[i] = sorted(list(set(dates[i])))
    print('House {0} data contain {1} days from {2} to {3}.'.format(i,len(dates[i]),dates[i][0], dates[i][-1]))
    print(dates[i], '\n')

def plot_df(df, title):
    apps = df.columns.values
    num_apps = len(apps)
    fig, axes = plt.subplots((num_apps+1)//2,2, figsize=(24, num_apps*2) )
    for i, key in enumerate(apps):
        axes.flat[i].plot(df[key], alpha = 0.6)
        axes.flat[i].set_title(key, fontsize = '15')
    plt.suptitle(title, fontsize = '30')
    fig.tight_layout()
    fig.subplots_adjust(top=0.95)
    plt.show(block=False)
    fig = plt.gcf()
    fig.set_size_inches(16.5, 10.5)
    plt.pause(3)
    plt.close()

# for i in range(1,2):
#     plot_df(df[i].loc[:dates[i][1]], 'First 2 day data of house {}'.format(i))

train = df[1].loc[:dates[1][2]]
test = df[1].loc[dates[1][2]:dates[1][3]]
X_train1 = train[['1_mains','2_mains']].values
y_train1 = train['9_lighting'].values

x_test1 = test[['1_mains','2_mains']].values

def mse_loss(y_predict, y):
    return np.mean(np.square(y_predict - y))
def mae_loss(y_predict, y):
    return np.mean(np.abs(y_predict - y))

from sklearn import svm
regr = svm.SVR()

print("Fitting data to svm regrsssion")
regr.fit(X_train1, y_train1)

print("Predicting values for house")
y_pred = regr.predict(x_test1)
y = test['9_lighting'].values

mse = mse_loss(y_pred, y)
mae = mae_loss(y_pred, y)
print('Mean square error on test set: ', mse)
print('Mean absolute error on the test set: ', mae)
