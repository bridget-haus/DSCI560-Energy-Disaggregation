from sklearn.datasets import load_boston
from keras.models import Sequential
from keras.layers import Dense, Conv1D, Flatten, MaxPooling1D
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from preprocess import *
import numpy as np
import tensorflow as tf

house_data = read_pre_proc('train', num_houses=1, first=True)

df = house_data[1]

df["mains"] = df["1_mains"] + df["2_mains"]
columns = ['mains']

x = []
y = []

for row in df.iterrows():
    sub_y = []
    for ind, value in row[1].items():
        if 'light' in ind:
            sub_y.append(value)
        elif ind == 'mains':
            x.append([value])
    y.append(sub_y)

x = np.array(x)
y = np.array(y)

print(x.shape)
print(y.shape)

train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.15)

# define parameters
verbose, epochs, batch_size = 0, 70, 16
n_timesteps = train_x.shape[1]
n_features = 1 #train_x.shape[2]
n_outputs = 3

#n_timesteps, n_features, n_outputs = train_x.shape[1], train_x.shape[2], train_y.shape[1]

train_data = tf.data.Dataset.from_tensor_slices((train_x, train_y))

# define model
model = Sequential()
model.add(Conv1D(filters=32, kernel_size=3, activation='relu', input_shape=(n_timesteps,n_features)))
model.add(Conv1D(filters=32, kernel_size=3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Conv1D(filters=16, kernel_size=3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dense(n_outputs))
model.compile(loss='mse', optimizer='adam')
# fit network
model.fit(train_data, epochs=epochs, batch_size=batch_size, verbose=verbose)

ypred = model.predict(test_x)
print(model.evaluate(train_x, train_y))
print("MSE: %.4f" % mean_squared_error(test_y, ypred))

x_ax = range(len(ypred))
plt.scatter(x_ax, test_y, s=5, color="blue", label="original")
plt.plot(x_ax, ypred, lw=0.8, color="red", label="predicted")
plt.legend()
plt.show()

# import pandas
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.wrappers.scikit_learn import KerasClassifier
# from keras.utils import np_utils
# from sklearn.model_selection import cross_val_score
# from sklearn.model_selection import KFold
# from sklearn.preprocessing import LabelEncoder
# from sklearn.pipeline import Pipeline
#
# # load dataset
# dataframe = pandas.read_csv("iris.csv", header=None)
# dataset = dataframe.values
# X = dataset[:, 0:4].astype(float)
# Y = dataset[:, 4]
# # encode class values as integers
# encoder = LabelEncoder()
# encoder.fit(Y)
# encoded_Y = encoder.transform(Y)
# # convert integers to dummy variables (i.e. one hot encoded)
# dummy_y = np_utils.to_categorical(encoded_Y)
#
#
# # define baseline model
# def baseline_model():
#     # create model
#     model = Sequential()
#     model.add(Dense(8, input_dim=4, activation='relu'))
#     model.add(Dense(3, activation='softmax'))
#     # Compile model
#     model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#     return model
#
#
# estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5, verbose=0)
# kfold = KFold(n_splits=10, shuffle=True)
# results = cross_val_score(estimator, X, dummy_y, cv=kfold)
# print("Baseline: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))