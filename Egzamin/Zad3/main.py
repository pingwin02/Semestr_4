import numpy as np
import matplotlib.pyplot as plt

RANGE = 3.1
ACCURACY = 1e-4
ITERATIONS = 5
ITERATIONS2 = 1000 # dla losowych metod
STARTING_POINT = np.array([-2, 3])

def f(x, y):
    return 3 * (x - 1) ** 2 - 2 * (x - 1) * y + 3 * y ** 2

def gradient(x, y):
    return np.array([6 * (x - 1) - 2 * y, -2 * (x - 1) + 6 * y])

def gradient_descent(gradient, w0):
    w = w0
    w_hist = [w]
    k = 1
    while True:
        w = w - 0.1 * gradient(w[0], w[1])
        w_hist.append(w)
        if f(*w) < ACCURACY or k > ITERATIONS:
            break
        k += 1
    return w_hist

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
        if delta_f < 0 and np.random.rand() < 1 / (1 + np.exp(delta_f / T)):
            w, f_value = w_prime, f_prime
            w_hist.append(w)
        T *= n
        if f(*w) < ACCURACY or k > ITERATIONS2:
            break
        k += 1 
    return w_hist

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
        if f(*w) < ACCURACY or k > ITERATIONS2:
            break
        k += 1
    return w_hist

if __name__ == '__main__':

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
    plt.title('Funkcja f(x, y)')
    plt.savefig('function.png')
    plt.show()

    w_hist = gradient_descent(gradient, STARTING_POINT)
    w_hist2 = simulated_annealing(f, STARTING_POINT, 10, 0.95)
    w_hist3 = random_search(f, STARTING_POINT, 0.1)

    for i in range(len(w_hist) - 1):
        plt.plot([w_hist[i][0], w_hist[i + 1][0]], [w_hist[i][1], w_hist[i + 1][1]], 'k--')
        plt.plot(w_hist[i + 1][0], w_hist[i + 1][1], 'ro')
        plt.text(w_hist[i + 1][0], w_hist[i + 1][1], f'({w_hist[i + 1][0]:.5f}, {w_hist[i + 1][1]:.5f})')

    for i in range(len(w_hist2) - 1):
        plt.plot([w_hist2[i][0], w_hist2[i + 1][0]], [w_hist2[i][1], w_hist2[i + 1][1]], 'g--')
        # plt.plot(w_hist2[i + 1][0], w_hist2[i + 1][1], 'ro')
        # plt.text(w_hist2[i + 1][0], w_hist2[i + 1][1], f'({w_hist2[i + 1][0]:.2f}, {w_hist2[i + 1][1]:.2f})')

    for i in range(len(w_hist3) - 1):
        plt.plot([w_hist3[i][0], w_hist3[i + 1][0]], [w_hist3[i][1], w_hist3[i + 1][1]], 'r--')
        # plt.plot(w_hist3[i + 1][0], w_hist3[i + 1][1], 'ro')
        # plt.text(w_hist3[i + 1][0], w_hist3[i + 1][1], f'({w_hist3[i + 1][0]:.2f}, {w_hist3[i + 1][1]:.2f})')

    print('Gradient descent:')
    print(np.array(w_hist))
    print('Simulated annealing:')
    print(np.array(w_hist2))
    print('Random search:')
    print(np.array(w_hist3))

    plt.contour(X, Y, Z, 30)
    plt.xlabel('x')
    plt.ylabel('y')

    plt.plot(1, 0, 'y*', markersize=15)
    plt.plot([], [], 'k--', label='Gradient descent')
    plt.plot([], [], 'g--', label='Simulated annealing')
    plt.plot([], [], 'r--', label='Random search')
    plt.plot([], [], 'y*', label='Minimum')
    plt.legend()

    plt.savefig('plot.png')

    plt.xlim(0.95, 1.05)
    plt.ylim(-0.05, 0.05)
    
    plt.savefig('plot_zoomed.png')
    plt.show()
