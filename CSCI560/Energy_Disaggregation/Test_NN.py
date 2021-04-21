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
import pickle


def read_label():
    label = {}
    for i in range(1, 7):
        hi = 'low_freq/house_{}/labels.dat'.format(i)
        label[i] = {}
        with open(hi) as f:
            for line in f:
                splitted_line = line.split(' ')
                label[i][int(splitted_line[0])] = splitted_line[1].strip() + '_' + splitted_line[0]
    return label


labels = read_label()
for i in range(1, 3):
    print('House {}: '.format(i), labels[i], '\n')


def read_merge_data(house):
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

X_train = []
Y_train = []
# X_val = []
# Y_val = []
X_test = []
Y_test = []

for i in range(1, 2):
    f = f'./pkl_files/house_{i}.pkl'
    with open(f, 'rb') as pickle_file:
        data = pickle.load(pickle_file)
    #data["mains"] = data["1_mains"] + data["2_mains"]
    mains = data[['1_mains', '2_mains']].values
    #mains = data["mains"].values
    app = data['20_washer_dryer'].values
    num_vals = len(mains)
    train_len = int(num_vals * 0.7)
#     val_len = train_len + int(num_vals * 0.2)
    X_train.extend(mains[:train_len])
#     X_val.extend(mains[train_len:val_len])
    X_test.extend(mains[train_len:])
    Y_train.extend(app[:train_len])
#     Y_val.extend(app[train_len:val_len])
    Y_test.extend(app[train_len:])

X_train = np.asarray(X_train)
# X_val = np.asarray(X_val)
X_test = np.asarray(X_test)
Y_train = np.asarray(Y_train)
# Y_val = np.asarray(Y_val)
Y_test = np.asarray(Y_test)

print(X_train.shape, Y_train.shape, X_test.shape, Y_test.shape)

fc_model_1 = build_fc_model()

adam = Adam(lr = 1e-5)
fc_model_1.compile(loss='mean_squared_error', optimizer=adam)
start = time.time()
checkpointer = ModelCheckpoint(filepath="./fc_light_h1_2.hdf5", verbose=0, save_best_only=True)
hist_fc_1 = fc_model_1.fit( X_train, Y_train,
                    batch_size=512, verbose=1, epochs=10,
                    validation_split=0.33, callbacks=[checkpointer])
print('Finish trainning. Time: ', time.time() - start)

fc_model_1 = load_model('fc_light_h1_2.hdf5')
pred_fc_1 = fc_model_1.predict(X_test).reshape(-1)
mse_loss_fc_1 = mse_loss(pred_fc_1, Y_test)
mae_loss_fc_1 = mae_loss(pred_fc_1, Y_test)
print('Mean square error on test set: ', mse_loss_fc_1)
print('Mean absolute error on the test set: ', mae_loss_fc_1)

train_loss = hist_fc_1.history['loss']
val_loss = hist_fc_1.history['val_loss']

# plot_each_app(df1_test, dates[1][17:], pred_fc_1, Y_test,
#               'FC model: real and predict Refrigerator on 6 test day of house 1', look_back = 50)