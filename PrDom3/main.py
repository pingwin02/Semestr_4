import numpy as np
import matplotlib.pyplot as plt

RANGE = 10


def f(x, y):
    return 4 * x ** 2 + 2 * y ** 2 - 4 * x * y


def gradient(x, y):
    return np.array([8 * x - 4 * y, 4 * y - 4 * x])


def gradient_descent(gradient, w0):
    w = w0
    w_hist = [w0]
    k = 1
    while True:
        w = w - 0.1 * gradient(w[0], w[1])
        w_hist.append(w)
        if f(*w) < 1e-4 or k > 10000:
            break
        k += 1
    return w_hist, k


def simulated_annealing(f, w0, Tmax, n):
    w = w0
    k = 1
    f_value = f(*w)
    w_hist = [w]
    T = Tmax
    while True:
        delta_w = np.random.normal(0, T, len(w))
        w_prime = w + delta_w
        f_prime = f(*w_prime)
        delta_f = f_prime - f_value
        if delta_f < 0 or np.random.rand() < 1 / (1 + np.exp(delta_f / T)):
            w, f_value = w_prime, f_prime
            w_hist.append(w)
        T *= n
        if f(*w) < 1e-4 or k > 10000:
            break
        k += 1
    return w_hist, k


def random_search(f, w0, sigma):
    w = w0
    k = 1
    f_value = f(*w)
    w_hist = [w]
    while True:
        delta_w = np.random.normal(0, sigma, len(w))
        w_prime = w + delta_w
        f_prime = f(*w_prime)
        delta_f = f_prime - f_value
        if delta_f < 0:
            w = w_prime
            f_value = f_prime
            w_hist.append(w)
        if f(*w) < 1e-4 or k > 10000:
            break
        k += 1
    return w_hist, k


x = np.linspace(-RANGE, RANGE, 100)
y = np.linspace(-RANGE, RANGE, 100)

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

k1_hist = []
k2_hist = []
k3_hist = []

w_0 = np.array(np.array([
    np.random.uniform(-RANGE, RANGE),
    np.random.uniform(-RANGE, RANGE)]))

w_hist, k1 = simulated_annealing(f, w_0, 10, 0.99)
w_hist2, k2 = gradient_descent(gradient, w_0)
w_hist3, k3 = random_search(f, w_0, 0.1)

k1_hist.append(k1)
k2_hist.append(k2)
k3_hist.append(k3)

for i in range(len(w_hist) - 1):
    plt.plot([w_hist[i][0], w_hist[i + 1][0]],
             [w_hist[i][1], w_hist[i + 1][1]], 'k-')
for i in range(len(w_hist2) - 1):
    plt.plot([w_hist2[i][0], w_hist2[i + 1][0]],
             [w_hist2[i][1], w_hist2[i + 1][1]], 'g-')
for i in range(len(w_hist3) - 1):
    plt.plot([w_hist3[i][0], w_hist3[i + 1][0]],
             [w_hist3[i][1], w_hist3[i + 1][1]], 'r-')


print('Simulated annealing: ', np.mean(k1_hist))
print('Gradient descent: ', np.mean(k2_hist))
print('Random search: ', np.mean(k3_hist))

cp = plt.contour(X, Y, Z, 25)
plt.xlabel('x')
plt.ylabel('y')

plt.plot(0, 0, 'y*', markersize=15)

plt.plot([], [], 'k-', label='Simulated annealing')
plt.plot([], [], 'g-', label='Gradient descent')
plt.plot([], [], 'r-', label='Random search')
plt.plot([], [], 'y*', label='Minimum')
plt.legend()

plt.savefig('plot.png')
plt.show()
