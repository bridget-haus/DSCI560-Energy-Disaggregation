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
import math
import pickle5 as pickle


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


def rmse_loss(y_predict, y):

    return math.sqrt(np.mean(np.square(y_predict - y)))


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


def train_test_split(appliance_dict, test_house):

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
        elif house == test_house:
            test_mains = data[['1_mains', '2_mains']].values
            test_app = data[app].values
            X_test.extend(test_mains)
            Y_test.extend(test_app)

    f = f'./pkl_files/house_{test_house}.pkl'
    with open(f, 'rb') as pickle_file:
        data = pickle.load(pickle_file)
    date_indexes = data.index.values
    dates = [str(time)[:10] for time in date_indexes]
    dates = sorted(list(set(dates)))

    X_train = np.asarray(X_train)
    X_test = np.asarray(X_test)
    Y_train = np.asarray(Y_train)
    Y_test = np.asarray(Y_test)

    print(X_train.shape, Y_train.shape, X_test.shape, Y_test.shape)

    return X_train, X_test, Y_train, Y_test, data, dates, date_indexes


def train_model(nn_model, X_train, X_test, Y_train, Y_test, epochs, batch_size, appliance, house):

    adam = Adam(lr=1e-5)
    nn_model.compile(loss='mean_squared_error', optimizer=adam)
    start = time.time()
    checkpointer = ModelCheckpoint(filepath=f'./nn_house_{house}_{appliance}.hdf5', verbose=0, save_best_only=True)
    hist_nn = nn_model.fit(X_train, Y_train,
                               batch_size=batch_size, verbose=1, epochs=epochs,
                               validation_split=0.33, callbacks=[checkpointer])
    print('Finish training time: ', time.time() - start)

    nn_model = load_model(f'nn_house_{house}_{appliance}.hdf5')
    prediciton = nn_model.predict(X_test).reshape(-1)
    RMSE = rmse_loss(prediciton, Y_test)
    MAE = mae_loss(prediciton, Y_test)

    train_loss = hist_nn.history['loss']
    val_loss = hist_nn.history['val_loss']

    return prediciton, RMSE, MAE


def pckl_results(date_indexes, prediction, appliance, house):

    results_dict = {'timestamp': list(date_indexes), 'prediction': list(prediction)}
    results_df = pd.DataFrame(data=results_dict)

    with open(f'pkl_results/nn_predict_house_{house}_{appliance}.pkl', 'wb') as f:
        pickle.dump(results_df, f)


def main():

    appliance = 'washer_dryer'
    epochs = 10
    batch_size = 512
    test_house = 6

    appliance_dict = choose_appliance(appliance)
    X_train, X_test, Y_train, Y_test, data, dates, date_indexes = train_test_split(appliance_dict, test_house)
    nn_model = build_fc_model()
    prediction, RMSE, MAE = train_model(nn_model, X_train, X_test, Y_train, Y_test, epochs, batch_size, appliance, test_house)
    pckl_results(date_indexes, prediction, appliance, test_house)

    print(f'RMSE on test set: {RMSE}')
    print(f'MAE on the test set: {MAE}')
    print(dates)

    plot_each_app(data, dates, prediction, Y_test,
                  f'True Value vs Predicted Value {appliance}', look_back=50)


if __name__ == "__main__":
    main()