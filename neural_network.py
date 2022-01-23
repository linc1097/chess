from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
# load the dataset
dataset = loadtxt('board_data.txt', delimiter=', ')
# split into input (X) and output (y) variables
X = dataset[:,0:768]
y = dataset[:,768]
# define the keras model
model = Sequential()
model.add(Dense(100, input_dim=768, activation='relu'))
model.add(Dense(30, activation='relu'))
model.add(Dense(1, activation='linear'))
# compile the keras model
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])
# fit the keras model on the dataset
model.fit(X, y, epochs=1, batch_size=100)
# evaluate the keras model
_, accuracy = model.evaluate(X, y)
print(accuracy)