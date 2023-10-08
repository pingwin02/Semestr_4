import numpy as np
import matplotlib.pyplot as plt

# Zadanie 1
x = np.array([-1.21, 0.1, 0.4, 0.82])
d = np.array([2.3, 3.4, 5.1, 6.3])
A = np.zeros((4, 2))
for i in range(4):
    A[i, :] = [x[i] ** 2, x[i]]
w = np.linalg.inv(A.T.dot(A)).dot(A.T).dot(d)
print(w)

emp = 0
for i in range(4):
    emp += (w[0] * x[i] ** 2 + w[1] * x[i] - d[i]) ** 2
emp /= 4
print(emp)

plt.scatter(x, d, color='black', label='dane')

x = np.linspace(-1.5, 1, 100)
y = w[0] * x ** 2 + w[1] * x
plt.plot(x, y, '-r', label='y = 5.3x^2 + 4.72x')
plt.grid()
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.savefig('plot.png')
plt.show()

# Zadanie 2
x1 = np.array([0.2, -0.3, -0.5, -0.1, -1.0, -0.3, 0.1])
x2 = np.array([0.3, 0.4, 3.3, 4.8, 3.2, 7.2, 3.4])
d = np.array([0.8, 0.2, -0.3, 1.2, 1.6, 0.5, -0.2])
A = np.zeros((7, 6))
for i in range(7):
    A[i, :] = [x1[i], x2[i], x1[i] * x2[i],
               x1[i] / x2[i], x1[i] ** 2, x2[i] ** 2]
w = np.linalg.inv(A.T.dot(A)).dot(A.T).dot(d)
print(w)

emp = 0
for i in range(7):
    emp += (w[0] * x1[i] + w[1] * x2[i] + w[2] * x1[i] * x2[i] +
            w[3] * x1[i] / x2[i] + w[4] * x1[i] ** 2 +
            w[5] * x2[i] ** 2 - d[i]) ** 2
print(emp)

# Zadanie 3
x1 = np.array([0.2, -0.3, -0.5, -0.1, -1.0, -0.3, 0.1])
x2 = np.array([0.3, 0.4, 3.3, 4.8, 3.2, 7.2, 3.4])
d = np.array([0.8, 0.2, -0.3, 1.2, 1.6, 0.5, -0.2])
A = np.zeros((7, 4))
for i in range(7):
    A[i, :] = [x1[i], x2[i], x1[i] * x2[i], x1[i] / x2[i]]
w = np.linalg.inv(A.T.dot(A)).dot(A.T).dot(d)
print(w)

emp = 0
for i in range(7):
    emp += (w[0] * x1[i] + w[1] * x2[i] + w[2] * x1[i] * x2[i] +
            w[3] * x1[i] / x2[i] - d[i]) ** 2
print(emp)
