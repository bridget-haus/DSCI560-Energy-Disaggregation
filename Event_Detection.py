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
import pickle
from sklearn import svm
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score

def get_windows(W, days, house, df, columns, is_main=False, plot=False) :

    w_diffs = {}
    diff_v = {}
    prev_value = {}
    light_dict = {}

    SECONDS_IN_DAY = 86400

    if is_main:
        df[house]["mains"] = df[house]["1_mains"] + df[house]["2_mains"]
        columns = ['mains']

    window_list = {}
    windows = {}
    window_start = {}
    prev_diff = {}
    for col in columns:
        w_diffs[col] = []
        diff_v[col] = []
        window_list[col] = []
        prev_value[col] = df[house][:1][col].values[0]
        window_start[col] = df[house][:1][col].index.strftime("%Y-%m-%d %H:%M:%S")[0]
        windows[col] = {}
        prev_diff[col] = 0
    df = df[house][columns]
    df = df[:days*SECONDS_IN_DAY]

    for index, row in df.iterrows():
        for ind, value in row.items():
            diff = value - prev_value[ind]
            if abs(diff) > W:
                w_diffs[ind].append((diff, index))
                str_window_start = str(window_start[ind])
                str_index = str(index)
                window_list_val = window_list[ind]
                windows[ind][str_window_start] = {str_index: window_list_val}

                if len(window_list[ind]) > 0 :
                    windows[ind][str_window_start]["max"] = max(window_list_val)
                    windows[ind][str_window_start]["min"] = min(window_list_val)
                    windows[ind][str_window_start]["avg"] = sum(window_list_val) / len(window_list_val)
                    windows[ind][str_window_start]["diff"] = prev_diff[ind]
                    prev_diff[ind] = diff

                    if 'light' in ind:
                        light_dict[index] = 'light'

                    window_start[ind] = index
                    window_list[ind] = []
                    diff_v[ind].append(value)
                    prev_value[ind] = value


            else:
                diff_v[ind].append(prev_value[ind])

            window_list[ind].append(value)

    if plot:
        new_df = pd.DataFrame(data=diff_v)
        plt.figure(); new_df.plot(); plt.legend(loc='best')
        plt.figure(); df.plot(); plt.legend(loc='best')

    return windows

def get_main_windows(W, days):

    df = get_preproccess_data()
    df = df[1]
    df["mains"] = df["1_mains"] + df["2_mains"]
    df = df['mains']
    w_diffs = []
    diff_v = []
    prev_value = df[:1].values[0]

    #df = df[:604800]
    df = df[:86400*days]

    windows = {}
    window_start = df[:1].index.strftime("%Y-%m-%d %H:%M:%S")[0]
    window_list = []

    for index, row in df.items():
        value = row
        diff = abs(prev_value - value)

        if diff > W:
            w_diffs.append((diff, index))
            str_window_start = str(window_start)
            str_index = str(index)
            windows[str_window_start] = {str_index: window_list}
            if len(window_list) > 0:
                windows[str_window_start]["max"] = max(window_list)
                windows[str_window_start]["min"] = min(window_list)
                windows[str_window_start]["avg"] = sum(window_list) / len(window_list)
                windows[str_window_start]["diff"] =  value - prev_value

            window_start = index
            window_list = []
            diff_v.append(value)
            prev_value = value
        else:
            diff_v.append(prev_value)

        window_list.append(row)

    # new_df = pd.DataFrame(data=diff_v)
    # plt.figure(); new_df.plot(); plt.legend(loc='best')
    # plt.figure(); df.plot(); plt.legend(loc='best')

    print("Test")
    return windows

def create_feature_vector(windows) :

    X = []
    Y = []
    y_val = 0

    for type, dics in windows.items():
        if 'light' in type:
            key = 'lights'
            y_val = 0
        else:
            key = 'rest'
            y_val = 1

        for lower_dic in dics.values():
            diff_val = abs(lower_dic['diff'])
            if not diff_val == 0:
                X.append([abs(lower_dic['diff'])])
                Y.append(y_val)

    return X, Y



def create_svm(feature_vector):
    pass


#H1
# 10: 0.55 , 20: 0.60 , 30: 0.59
#H2
# 20: 0.12 , 30: 0.14
W = 20
Noise = 10
days = 1
house = 1

start = time.time()

df = get_preproccess_data()

#main_windows = get_main_windows(W, days )
main_windows = get_windows(W+Noise, days, house, df, ['mains'], is_main=True)

columns = [col for col in df[house].columns if 'main' not in col]
appliance_windows = get_windows(W, days, house, df, columns)

main_length = 0
appliance_length = 0

for value in main_windows.values():
    main_length += len(value)

for value in appliance_windows.values():
    appliance_length += len(value)

X, Y = create_feature_vector(appliance_windows)

clf = svm.SVC()
clf.fit(X, Y)

X_Test, Y_true = create_feature_vector(main_windows)

Y_pred = clf.predict(X_Test)

recall = recall_score(Y_true,  Y_pred)
precision = precision_score(Y_true, Y_pred)

# filename = 'finalized_model.sav'
# pickle.dump(clf, open(filename, 'wb'))

end = time.time()
percent_diff = appliance_length / main_length
print("Time: ", end - start)

print(appliance_length)
print(main_length)

print("muck")

#TODO
#We need to cherry pick 7 days of data from houses 1-4 that we like and are good
