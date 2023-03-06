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

# calculate closed-form solution
x_train = np.c_[np.ones(len(x_train)), x_train]
theta_best = np.linalg.inv(x_train.T.dot(x_train)).dot(x_train.T).dot(y_train)
print("Theta regression:", theta_best)

# calculate error
RSS = 0
for i in range(len(x_test)):
    RSS += (theta_best[1] * x_test[i] + theta_best[0] - y_test[i]) ** 2
MSE = RSS / len(x_test)
print('MSE:', MSE)

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()

# get the columns
y_train = train_data['MPG'].to_numpy()
x_train = train_data['Weight'].to_numpy()

y_test = test_data['MPG'].to_numpy()
x_test = test_data['Weight'].to_numpy()

# standarization
X_avg = np.average(x_train)
X_war = np.std(x_train)
x_train = (x_train - X_avg) / X_war
x_train = np.c_[np.ones(len(x_train)), x_train]

Y_avg = np.average(y_train)
Y_war = np.std(y_train)
y_train = (y_train - Y_avg) / Y_war

X_avg = np.average(x_test)
X_war = np.std(x_test)
x_test = (x_test - X_avg) / X_war

Y_avg = np.average(y_test)
Y_war = np.std(y_test)
y_test = (y_test - Y_avg) / Y_war

# calculate theta using Batch Gradient Descent
y_train = y_train.reshape(len(y_train), 1)
theta_best = np.random.rand(2, 1)
learning_rate = 0.01
iterations = 100

for i in range(iterations):
    gradient = 2 / len(x_train) * x_train.T.dot(x_train.dot(theta_best) - y_train)
    theta_best = theta_best - learning_rate * gradient

print("Theta gradient:", theta_best)

#  calculate error
RSS = 0
for i in range(len(x_test)):
    RSS += (theta_best[1] * x_test[i] + theta_best[0] - y_test[i]) ** 2
MSE = RSS / len(x_test)
print('MSE:', MSE)

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()
