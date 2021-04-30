import boto3
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

from keras.models import load_model

import datetime
import matplotlib.pyplot as plt
import tensorflow as tf

# Connect to Boto3
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2')

# Your Bucket goes here
bucket_name = 'bitcoin-prediction'

# Your S3 Path goes here
filename = 'sagemaker/bitcoin_2018-3-1_2021-4-28.csv'

# s3.Bucket(bucket_name).download_file(Filename='bitcoin_2016-3-15_2021-4-25.csv', Key=filename)
print('Download Complete')

df = pd.read_csv('bitcoin_2018-3-1_2021-4-28.csv')

df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by='Date', inplace=True)
df1 = df.reset_index()['Close']

scaler = MinMaxScaler(feature_range=(0, 1))
df1 = scaler.fit_transform(np.array(df1).reshape(-1, 1))

# splitting dataset into train and test split
training_size = int(len(df1) * 0.7)
test_size = len(df1) - training_size
train_data, test_data = df1[0:training_size, :], df1[training_size:len(df1), :1]


# convert an array of values into a dataset matrix
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)


# reshape into X=t,t+1,t+2,t+3 and Y=t+4
time_step = 100

X_train, y_train = create_dataset(train_data, time_step)
X_test, y_test = create_dataset(test_data, time_step)

# reshape input to be [samples, time steps, features] which is required for LSTM
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(100, 1)))
model.add(LSTM(50, return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')

model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=64, verbose=1)

# save model
model.save('lstm_model.h5')

# Lets Do the prediction
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)

model = load_model('lstm_model.h5')

x_input = test_data[len(test_data) - time_step:].reshape(1, -1)

temp_input = list(x_input)
temp_input = temp_input[0].tolist()

lst_output = []
n_steps = time_step
i = 0
while i < 30:

    if (len(temp_input) > 100):
        # print(temp_input)
        x_input = np.array(temp_input[1:])
        # print("{} day input {}".format(i,x_input))
        x_input = x_input.reshape(1, -1)
        x_input = x_input.reshape((1, n_steps, 1))
        # print(x_input)
        yhat = model.predict(x_input, verbose=0)
        print("{} day output {}".format(i, yhat))
        temp_input.extend(yhat[0].tolist())
        temp_input = temp_input[1:]
        # print(temp_input)
        lst_output.extend(yhat.tolist())
        i = i + 1
    else:
        x_input = x_input.reshape((1, n_steps, 1))
        yhat = model.predict(x_input, verbose=0)
        # print(yhat[0])
        temp_input.extend(yhat[0].tolist())
        # print(len(temp_input))
        lst_output.extend(yhat.tolist())
        i = i + 1

numdays = 30
base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
print(date_list)

dt_list = list()
for t in date_list:
    dt = t.strftime('%d-%m-%Y')
    dt_list.append(dt)
print(dt_list)

# date_zip = zip(dt_list, lst_output)
# print(list(date_zip))

df = pd.DataFrame(list(zip(dt_list, scaler.inverse_transform(lst_output))), columns=['Date', 'Pred'])
print(df)

df.to_csv('30_pred.csv', encoding='utf-8', index=False)
