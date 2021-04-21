import tensorflow as tf
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
from keras.optimizers import Adam
import numpy as np
import pandas as pd
import time
import warnings
warnings.filterwarnings("ignore")
import glob
import matplotlib.pyplot as plt
import pickle5 as pickle


def read_label():

    label = {}
    for i in range(1, 7):
        house = f'low_freq/house_{i}/labels.dat'
        label[i] = {}
        with open(house) as f:
            for line in f:
                split_line = line.split(' ')
                label[i][int(split_line[0])] = split_line[1].strip() + '_' + split_line[0]
    return label


def read_merge_data(house, labels):

    path = 'low_freq/house_{}/'.format(house)
    file = path + 'channel_1.dat'
    df = pd.read_table(file, sep=' ', names=['unix_time', labels[house][1]],
                       dtype={'unix_time': 'int64', labels[house][1]: 'float64'})

    num_apps = len(glob.glob(path + 'channel*'))
    for i in range(2, num_apps + 1):
        file = path + 'channel_{}.dat'.format(i)
        data = pd.read_table(file, sep=' ', names=['unix_time', labels[house][i]],
                             dtype={'unix_time': 'int64', labels[house][i]: 'float64'})
        df = pd.merge(df, data, how='inner', on='unix_time')
    df['timestamp'] = df['unix_time'].astype("datetime64[s]")
    df = df.set_index(df['timestamp'].values)
    df.drop(['unix_time', 'timestamp'], axis=1, inplace=True)

    return df


def preprocess(labels):

    df = {}
    for i in range(1, 7):
        df[i] = read_merge_data(i, labels)

    dates = {}
    for i in range(1, 7):
        dates[i] = [str(time)[:10] for time in df[i].index.values]
        dates[i] = sorted(list(set(dates[i])))
        print('House {0} data contain {1} days from {2} to {3}.'.format(i, len(dates[i]), dates[i][0], dates[i][-1]))
        print(dates[i], '\n')

    return df, dates


def plot_each_app(df, dates, predict, y_test, title, look_back=0):

    num_date = len(dates)
    fig, axes = plt.subplots(num_date, 1, figsize=(24, num_date * 5))
    plt.suptitle(title, fontsize='25')
    fig.tight_layout()
    fig.subplots_adjust(top=0.95)
    for i in range(num_date):
        if i == 0: l = 0
        ind = df.loc[dates[i]].index[look_back:]
        axes.flat[i].plot(ind, y_test[l:l + len(ind)], color='blue', alpha=0.6, label='True value')
        axes.flat[i].plot(ind, predict[l:l + len(ind)], color='red', alpha=0.6, label='Predicted value')
        axes.flat[i].legend()
        l = len(ind)
    plt.show()


def mse_loss(y_predict, y):

    return np.mean(np.square(y_predict - y))


def mae_loss(y_predict, y):

    return np.mean(np.abs(y_predict - y))


def build_fc_model():

    fc_model = Sequential()
    fc_model.add(tf.keras.layers.Dense(2, activation='relu'))
    fc_model.add(tf.keras.layers.Dense(256, activation='relu'))
    fc_model.add(tf.keras.layers.Dense(512))
    fc_model.add(tf.keras.layers.Dense(1024))
    fc_model.add(tf.keras.layers.Dense(1))
    fc_model.build((214816, 2))
    fc_model.summary()

    return fc_model


def choose_appliance(appliance):

    appliance_dict = {}
    for i in range(1, 7):
        f = f'./pkl_files/house_{i}.pkl'
        with open(f, 'rb') as pickle_file:
            data = pickle.load(pickle_file)
            for col in data.columns:
                if appliance in col:
                    appliance_dict[i] = col

    return appliance_dict


def train_test_split(appliance_dict):

    X_train = []
    Y_train = []
    X_test = []
    Y_test = []

    for house, app in appliance_dict.items():
        f = f'./pkl_files/house_{house}.pkl'
        with open(f, 'rb') as pickle_file:
            data = pickle.load(pickle_file)
        if house == 1 or house == 2 or house == 3 or house == 4:
            train_mains = data[['1_mains', '2_mains']].values
            train_app = data[app].values
            X_train.extend(train_mains)
            Y_train.extend(train_app)
        elif house == 5 or house == 6:
            test_mains = data[['1_mains', '2_mains']].values
            test_app = data[app].values
            X_test.extend(test_mains)
            Y_test.extend(test_app)

    X_train = np.asarray(X_train)
    X_test = np.asarray(X_test)
    Y_train = np.asarray(Y_train)
    Y_test = np.asarray(Y_test)

    print(X_train.shape, Y_train.shape, X_test.shape, Y_test.shape)

    return X_train, X_test, Y_train, Y_test


def train_model(fc_model_1, X_train, X_test, Y_train, Y_test, epochs, batch_size):

    adam = Adam(lr=1e-5)
    fc_model_1.compile(loss='mean_squared_error', optimizer=adam)
    start = time.time()
    checkpointer = ModelCheckpoint(filepath="./fc_light_h1_2.hdf5", verbose=0, save_best_only=True)
    hist_fc_1 = fc_model_1.fit(X_train, Y_train,
                               batch_size=batch_size, verbose=1, epochs=epochs,
                               validation_split=0.33, callbacks=[checkpointer])
    print('Finish trainning. Time: ', time.time() - start)

    fc_model_1 = load_model('fc_light_h1_2.hdf5')
    pred_fc_1 = fc_model_1.predict(X_test).reshape(-1)
    mse_loss_fc_1 = mse_loss(pred_fc_1, Y_test)
    mae_loss_fc_1 = mae_loss(pred_fc_1, Y_test)

    train_loss = hist_fc_1.history['loss']
    val_loss = hist_fc_1.history['val_loss']

    return pred_fc_1, mse_loss_fc_1, mae_loss_fc_1


def main():

    appliance = 'kitchen_outlets'
    epochs = 1
    batch_size = 512

    appliance_dict = choose_appliance(appliance)
    X_train, X_test, Y_train, Y_test = train_test_split(appliance_dict)
    fc_model_1 = build_fc_model()
    pred_fc_1, mse_loss_fc_1, mae_loss_fc_1 = train_model(fc_model_1, X_train, X_test, Y_train, Y_test, epochs, batch_size)

    print(f'MSE on test set: {mse_loss_fc_1}')
    print(f'MAE on the test set: {mae_loss_fc_1}')


if __name__ == "__main__":
    main()