import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import datetime
from cycler import cycler
import itertools
import time
import math
import warnings
warnings.filterwarnings("ignore")
import glob
from preprocess import *
import random
import pickle
from sklearn import svm
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score

def generate_training_labels(W, days, house, df, columns, string_type, plot=False):

    prev_value = {}

    num_one_labels = 0

    SECONDS_IN_DAY = 86400

    df_apps = df[house][columns]
    df_apps = df_apps[:days * SECONDS_IN_DAY]

    df[house]["mains"] = df[house]["1_mains"] + df[house]["2_mains"]
    columns = ['mains']

    windows = {}
    window_list = {}
    window_start = {}
    prev_diff = {}
    prev_diff[string_type] = 0
    prev_diff['rest'] = 0
    plot_list = {}
    plot_list['rest'] = {}
    plot_list[string_type] = {}
    for col in columns:
        window_list[col] = []
        prev_value[col] = df[house][:1][col].values[0]
        window_start[col] = df[house][:1][col].index.strftime("%Y-%m-%d %H:%M:%S")[0]
        windows[col] = {}
        prev_diff[col] = 0
    df_mains = df[house][columns]
    df_mains = df_mains[:days * SECONDS_IN_DAY]

    row_one = True

    for (mains, apps) in zip(df_mains.iterrows(), df_apps.iterrows()):
        index = mains[0]
        main_row = mains[1]
        app_row = apps[1]
        if row_one:
            row_one = False
            prev_app_row = app_row
        for ind, value in main_row.items():

            diff = value - prev_value[ind]
            str_window_start = str(window_start[ind])
            str_index = str(index)
            date_window_start = datetime.datetime.strptime(str_window_start, '%Y-%m-%d %H:%M:%S')
            date_index = datetime.datetime.strptime(str_index, '%Y-%m-%d %H:%M:%S')

            if abs(diff) > W:

                max_val = W - 1
                label = 0

                for item, prev_item in zip(app_row.iteritems(), prev_app_row.iteritems()):
                    appliance = item[0]
                    val = abs(item[1] - prev_item[1])
                    if val > max_val:
                        max_val = val
                        if string_type in appliance:
                            label = 1
                        else:
                            label = 0

                x = random.randint(0,70)

                window_list_val = window_list[ind]

                if plot:
                    if label == 1:
                        prev_diff[string_type] = abs(diff)
                        prev_diff[string_type] = 0
                        #plot_list[string_type][date_window_start] = abs(diff)
                        plot_list[string_type][date_index] = diff #abs(diff)
                        #plot_list['rest'][date_window_start] = 0
                        plot_list['rest'][date_index] = 0
                    else:
                        prev_diff[string_type] = 0
                        prev_diff['rest'] = abs(diff)
                        #plot_list[string_type][date_window_start] = 0
                        plot_list[string_type][date_index] = 0
                        #plot_list['rest'][date_window_start] = abs(diff)
                        plot_list['rest'][date_index] = diff #abs(diff)

                if x == 25 or label == 1:

                    windows[ind][str_window_start] = {'end': str_index}
                    windows[ind][str_window_start]["diff"] = prev_diff[ind]
                    time_diff = date_index - date_window_start
                    diff_seconds = time_diff.total_seconds()
                    windows[ind][str_window_start]["duration"] = diff_seconds
                    hour = int(str_window_start.split(" ")[1].split(":")[0])
                    if hour < 9 or hour > 17:
                        night_day = 0
                    else:
                        night_day = 1

                    level = abs(diff) / value
                    windows[ind][str_window_start]["hour"] = night_day
                    windows[ind][str_window_start]["level"] = level
                    windows[ind][str_window_start]['label'] = label
                    windows[ind][str_window_start]["max"] = max(window_list_val)
                    windows[ind][str_window_start]["min"] = min(window_list_val)
                    windows[ind][str_window_start]["avg"] = sum(window_list_val) / len(window_list_val)
                    num_one_labels += label

                prev_diff[ind] = diff
                window_start[ind] = index
                window_list[ind] = []

            else:
                #plot_list[string_type][date_window_start] = 0 #prev_diff[string_type]
                plot_list[string_type][date_index] = prev_diff[string_type]
                #plot_list['rest'][date_window_start] = 0 #prev_diff['rest']
                plot_list['rest'][date_index] = prev_diff['rest']

            prev_value[ind] = value
            window_list[ind].append(value)

        prev_app_row = app_row


    if plot:
        new_df = pd.DataFrame(data=plot_list)

        df_mains.plot(); plt.legend(loc='best')
        plt.title("Main Energy Usage")

        new_df.plot(); plt.legend(loc='best')
        plt.ylim(-250, 250)
        plt.title("Energy Window Classifications")



    return windows, num_one_labels

def get_windows(W, days, house, df, columns, is_main=False, plot=False) :

    w_diffs = {}
    diff_v = {}
    prev_value = {}
    num_lights = 0

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

                if 'light' in ind:
                    num_lights += 1

                w_diffs[ind].append((diff, index))
                str_window_start = str(window_start[ind])
                str_index = str(index)
                window_list_val = window_list[ind]
                windows[ind][str_window_start] = {str_index: window_list_val}

                if len(window_list[ind]) > 0:
                    # windows[ind][str_window_start]["max"] = max(window_list_val)
                    # windows[ind][str_window_start]["min"] = min(window_list_val)
                    # windows[ind][str_window_start]["avg"] = sum(window_list_val) / len(window_list_val)
                    windows[ind][str_window_start]["diff"] = prev_diff[ind]
                    prev_diff[ind] = diff

                    window_start[ind] = index
                    window_list[ind] = []
                    diff_v[ind].append(value)

            else:
                diff_v[ind].append(prev_value[ind])

            prev_value[ind] = value
            window_list[ind].append(value)

    if plot:
        new_df = pd.DataFrame(data=diff_v)
        plt.figure(); new_df.plot(); plt.legend(loc='best')
        plt.figure(); df.plot(); plt.legend(loc='best')
        plt.ylim(-250, 250)

    return windows, num_lights

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
                # windows[str_window_start]["max"] = max(window_list)
                # windows[str_window_start]["min"] = min(window_list)
                # windows[str_window_start]["avg"] = sum(window_list) / len(window_list)
                windows[str_window_start]["max"]
                windows[str_window_start]["diff"] = value - prev_value

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

def create_feature_vector(windows,timestamps=None) :

    X = []
    Y = []

    for type, dics in windows.items():

        for k, lower_dic in dics.items():
            diff_val = abs(lower_dic['diff'])
            label = lower_dic['label']

            if not diff_val == 0:
                Y.append(label)
                X.append([abs(lower_dic['diff']), lower_dic['hour'], lower_dic['level']]) #, lower_dic['max'], lower_dic['min'], lower_dic['avg']]) lower_dic['duration'],

    return X, Y



def create_svm(feature_vector):
    pass


def main():

    #H1
    # 10: 0.55 , 20: 0.60 , 30: 0.59
    #H2
    # 20: 0.12 , 30: 0.14
    W = 35
    Noise = 15
    days = 1
    house = 1

    start = time.time()

    df = get_preproccess_data()

    #x = datetime.datetime.strptime('2011-04-18 13:22:09', '%Y-%m-%d %H:%M:%S')

    #main_windows = get_main_windows(W, days )
    #main_windows, light_dict = get_windows(W+Noise, days, house, df, ['mains'], is_main=True)

    columns = [col for col in df[house].columns if 'main' not in col]
    main_windows, num_lights = generate_training_labels(W, days, house, df, columns, 'light', plot=True)

    house = 2
    days = 1

    columns = [col for col in df[house].columns if 'main' not in col]
    test_main_windows, num_lights_test = generate_training_labels(W, days, house, df, columns, 'light')

    # columns = [col for col in df[house].columns if 'main' not in col]
    # appliance_windows, num_lights = get_windows(W, days, house, df, columns)

    # main_length = 0
    # appliance_length = 0
    #
    # for value in main_windows.values():
    #     main_length += len(value)
    #
    # for value in appliance_windows.values():
    #     appliance_length += len(value)

    X, Y = create_feature_vector(main_windows)

    clf = svm.SVC()
    clf.fit(X, Y)

    X_Test, Y_true = create_feature_vector(test_main_windows)

    Y_pred = clf.predict(X_Test)

    recall = recall_score(Y_true,  Y_pred)
    precision = precision_score(Y_true, Y_pred)
    accuracy = accuracy_score(Y_true, Y_pred)

    print(f"Recall: {recall}")
    print(f"Precision: {precision}")
    print(f"Accuracy: {accuracy}")

    # filename = 'finalized_model.sav'
    # pickle.dump(clf, open(filename, 'wb'))

    end = time.time()
    print("Time: ", end - start)

    plt.show()

    print("Done")

#H1
# Recall: 0.75
# Precision: 0.5454545454545454
# Accuracy: 0.6111111111111112
# Time:  189.97088646888733

    #TODO
    #We need to cherry pick 7 days of data from houses 1-4 that we like and are good

if __name__ == "__main__" :
    main()