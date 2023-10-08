import numpy as np
import matplotlib.pyplot as plt

from data import get_data, inspect_data, split_data

data = get_data()
# inspect_data(data)

train_data, test_data = split_data(data)

# Simple Linear Regression
# predict MPG (y, dependent variable) using Weight (x, independent variable) using closed-form solution
# y = theta_0 + theta_1 * x - we want to find theta_0 and theta_1 parameters that minimize the prediction error

# We can calculate the error using MSE metric:
# MSE = SUM (from i=1 to n) (actual_output - predicted_output) ** 2

# get the columns
y_train = train_data['MPG'].to_numpy()
x_train = train_data['Weight'].to_numpy()

y_test = test_data['MPG'].to_numpy()
x_test = test_data['Weight'].to_numpy()

x_train_copy = x_train
y_train_copy = y_train


# standarization
def standarize(n, train):
    return (n - np.average(train)) / np.std(train)


x_train = standarize(x_train, x_train)
x_train = np.c_[np.ones(len(x_train)), x_train]

y_train = standarize(y_train, y_train)
x_test = standarize(x_test, x_train_copy)
y_test = standarize(y_test, y_train_copy)

# calculate closed-form solution
theta_best = np.linalg.inv(x_train.T.dot(x_train)).dot(x_train.T).dot(y_train)
print("Theta regression:", theta_best)


def MSE(theta, x, y):
    _sum = 0
    for _i in range(len(x)):
        _sum += ((theta[1] * x[_i] + theta[0] - y[_i]) ** 2) / len(x)
    return _sum


def plot(theta, _x, _y):
    x = np.linspace(min(_x), max(_x), 100)
    y = float(theta[0]) + float(theta[1]) * x
    plt.plot(x, y)
    plt.scatter(_x, _y)
    plt.xlabel('Weight')
    plt.ylabel('MPG')
    plt.show()


# calculate error
print('MSE:', MSE(theta_best, x_test, y_test))

# plot the regression line
plot(theta_best, x_test, y_test)

# calculate theta using Batch Gradient Descent
y_train = y_train.reshape(len(y_train), 1)
theta_best = np.random.rand(2, 1)
learning_rate = 0.01
iterations = 1000

for i in range(iterations):
    gradient = 2 / len(x_train) * x_train.T.dot(x_train.dot(theta_best) - y_train)
    theta_best = theta_best - learning_rate * gradient

print("Theta gradient:", theta_best.T)

#  calculate error
print('MSE:', MSE(theta_best, x_test, y_test))

# plot the regression line
plot(theta_best, x_test, y_test)
