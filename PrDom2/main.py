import numpy as np
import matplotlib.pyplot as plt

RANGE = 3


def f(x, y):
    return 3 * (x - 1) ** 2 - 2 * (x - 1) * y + 3 * y ** 2


def gradient(x, y):
    grad = np.array([6 * (x - 1) - 2 * y, -2 * (x - 1) + 6 * y])
    return grad


def gradient_descent(gradient, w0):
    w = w0
    w_hist = [w0]
    k = 1
    while True:
        w = w - 0.1 * gradient(w[0], w[1])
        w_hist.append(w)
        if f(*w) < 1e-4 or k > 1000:
            break
        k += 1
    return w_hist, k


x = np.linspace(-RANGE, RANGE, 1000)
y = np.linspace(-RANGE, RANGE, 1000)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.view_init(30, 45)
plt.savefig('function.png')
plt.show()
k_hist = []
for i in range(100):
    w_hist, k = gradient_descent(gradient, np.array([
        np.random.uniform(-RANGE, RANGE),
        np.random.uniform(-RANGE, RANGE)
    ]))

    k_hist.append(k)

    for i in range(len(w_hist)):
        plt.plot(w_hist[i][0], w_hist[i][1], 'r.')
        if i < len(w_hist) - 1:
            plt.arrow(w_hist[i][0], w_hist[i][1], w_hist[i + 1][0] -
                      w_hist[i][0], w_hist[i + 1][1] - w_hist[i][1],
                      color='k', width=0.01)

cp = plt.contour(X, Y, Z, 15)
plt.clabel(cp, inline=True, fontsize=10)
plt.xlabel('x')
plt.ylabel('y')

plt.plot(1, 0, 'b*', markersize=15)
plt.plot([], [], 'r.', label='Gradient descent')
plt.plot([], [], 'b*', label='Minimum')
plt.legend()

print("Average number of iterations: ", np.mean(k_hist))
plt.savefig('plot.png')
plt.show()
