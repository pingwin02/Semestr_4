import numpy as np
import matplotlib.pyplot as plt


def gradient(x, y):
    grad = np.array([6 * x - 2 * y - 2, -2 * x + 6 * y - 4])
    return grad


def gradient_descent(gradient, w0, num_iter):
    w = w0
    w_hist = [w0]
    for i in range(num_iter):
        w = w - 0.1 * gradient(w[0], w[1])
        w_hist.append(w)
    return w_hist


x = np.linspace(-100, 100, 1000)
y = np.linspace(-100, 100, 1000)

X, Y = np.meshgrid(x, y)
Z = 3 * X ** 2 - 2 * X * Y + 3 * Y ** 2 - 2 * X - 4 * Y

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.view_init(30, 45)
plt.savefig('function.png')
plt.show()

w_hist = gradient_descent(gradient, np.array([
    200 * np.random.rand() - 100,
    200 * np.random.rand() - 100,
]), 25)

cp = plt.contour(X, Y, Z, 15)
plt.clabel(cp, inline=True, fontsize=10)
plt.xlabel('x')
plt.ylabel('y')

for i in range(len(w_hist)):
    plt.plot(w_hist[i][0], w_hist[i][1], 'k.')
    if i < len(w_hist) - 1:
        plt.arrow(w_hist[i][0], w_hist[i][1], w_hist[i + 1][0] -
                  w_hist[i][0], w_hist[i + 1][1] - w_hist[i][1],
                  color='r', width=0.01)

plt.savefig('plot.png')
plt.show()
