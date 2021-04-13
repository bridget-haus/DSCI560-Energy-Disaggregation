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

def generate_training_labels(W, full_df, string_type, skew, plot=False):

    prev_value = {}

    num_one_labels = 0
    num_houses = len(full_df)

    all_windows = {}

    for i in range(1, num_houses + 1):

        df = full_df[i]

        columns = [col for col in df.columns if 'main' not in col] #[col for col in df.columns if string_type in col]
        df_apps = df[columns]

        df["mains"] = df["1_mains"] + df["2_mains"]
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
            prev_value[col] = df[:1][col].values[0]
            window_start[col] = df[:1][col].index.strftime("%Y-%m-%d %H:%M:%S")[0]
            windows[col] = {}
            prev_diff[col] = 0
        df_mains = df[columns]

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

                # for item, prev_item in zip(app_row.iteritems(), prev_app_row.iteritems()):
                #     appliance = item[0]
                #     val = abs(item[1] - prev_item[1])
                #     if val > W:
                #         max_val = val
                #         if string_type in appliance:
                #             label = 1
                #         else:
                #             label = 0

                if abs(diff) > W:

                    max_val = W - 1
                    label = 0

                    row_diffs = app_row - prev_app_row
                    row_diffs = row_diffs.abs()
                    row_diff_sum = row_diffs.sum()
                    high_val = max(abs(diff), row_diff_sum)

                    for item, prev_item in zip(app_row.iteritems(), prev_app_row.iteritems()):
                        appliance = item[0]
                        val = abs(item[1] - prev_item[1])
                        if val > max_val:
                            max_val = val
                            if string_type in appliance and abs(val / high_val) > 0.3:
                                label = 1
                            else:
                                label = 0

                    x = random.randint(0,skew)

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

                    if x == 1 or label == 1:

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

        all_windows[i] = windows


        if plot:
            new_df = pd.DataFrame(data=plot_list)

            df_mains.plot(); plt.legend(loc='best')
            plt.title("Main Energy Usage")

            new_df.plot(); plt.legend(loc='best')
            plt.ylim(-250, 250)
            plt.title("Energy Window Classifications")



    return all_windows

def generate_training_labels_cnn(W, full_df, string_type, skew, plot=False):

    prev_value = {}

    num_one_labels = 0
    num_houses = len(full_df)

    all_windows = {}

    for i in range(1, num_houses + 1):

        df = full_df[i]

        columns = [col for col in df.columns if 'main' not in col] #[col for col in df.columns if string_type in col]
        df_apps = df[columns]

        df["mains"] = df["1_mains"] + df["2_mains"]
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
            prev_value[col] = df[:1][col].values[0]
            window_start[col] = df[:1][col].index.strftime("%Y-%m-%d %H:%M:%S")[0]
            windows[col] = {}
            prev_diff[col] = 0
        df_mains = df[columns]

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

                # for item, prev_item in zip(app_row.iteritems(), prev_app_row.iteritems()):
                #     appliance = item[0]
                #     val = abs(item[1] - prev_item[1])
                #     if val > W:
                #         max_val = val
                #         if string_type in appliance:
                #             label = 1
                #         else:
                #             label = 0

                if abs(diff) > W:

                    max_val = W - 1
                    label = 0

                    row_diffs = app_row - prev_app_row
                    row_diffs = row_diffs.abs()
                    row_diff_sum = row_diffs.sum()
                    high_val = max(abs(diff), row_diff_sum)

                    for item, prev_item in zip(app_row.iteritems(), prev_app_row.iteritems()):
                        appliance = item[0]
                        val = abs(item[1] - prev_item[1])
                        if val > max_val:
                            max_val = val
                            if string_type in appliance and abs(val / high_val) > 0.3:
                                label = 1
                            else:
                                label = 0

                    x = random.randint(0, skew)

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

                    if x == 1 or label == 1:

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

        all_windows[i] = windows


        if plot:
            new_df = pd.DataFrame(data=plot_list)

            df_mains.plot(); plt.legend(loc='best')
            plt.title("Main Energy Usage")

            new_df.plot(); plt.legend(loc='best')
            plt.ylim(-250, 250)
            plt.title("Energy Window Classifications")



    return all_windows

def create_feature_vector(windows,timestamps=None) :

    X = []
    Y = []

    num_houses = len(windows)

    for house_dict in windows.values():
        for type, dics in house_dict.items():

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
    W = 15
    Noise = 15

    start = time.time()

    #df = get_preproccess_data()

    df_train = read_pre_proc('train')
    df_test = read_pre_proc('test')

    # main_windows = generate_training_labels(W, df_train, 'wash', 25) #, plot=True)
    #
    # f = open(f"windows_${W}.pkl", "wb")
    # pickle.dump(main_windows, f)
    # f.close()

    with open(f'pkl_files/windows.pkl', 'rb') as handle:
        main_windows = pickle.load(handle)

    # test_main_windows = generate_training_labels(W, df_test, 'wash', 25)
    #
    # f = open(f"test_windows_${W}.pkl", "wb")
    # pickle.dump(test_main_windows, f)
    # f.close()

    with open(f'test_windows_${W}.pkl', 'rb') as handle:
        test_main_windows = pickle.load(handle)

    X, Y = create_feature_vector(main_windows)

    clf = svm.SVC()
    clf.fit(X, Y)

    X_Test, Y_true = create_feature_vector(main_windows)

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