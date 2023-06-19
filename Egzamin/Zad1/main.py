import matplotlib.pyplot as plt
import numpy as np

def tn(x):
    return np.piecewise(x, [x <= 10, (10 < x) & (x < 30), x >= 30], [1, lambda x: (30 - x) / 20, 0])

def tw(x):
    return np.piecewise(x, [x <= 10, (10 < x) & (x < 30), x >= 30], [0, lambda x: (x - 10) / 20, 1])

def wn(x):
    return np.piecewise(x, [x <= 40, (40 < x) & (x < 100), x >= 100], [1, lambda x: (100 - x) / 60, 0])

def ww(x):
    return np.piecewise(x, [x <= 40, (40 < x) & (x < 100), x >= 100], [0, lambda x: (x - 40) / 60, 1])

def mn(x):
    return np.piecewise(x, [x <= 30, (30 < x) & (x < 70), x >= 70], [1, lambda x: 1 - (x - 30) / 40, 0])

def ms(x):
    return np.piecewise(x, [x <= 20, (20 < x) & (x <= 50), (50 < x) & (x < 80), x >= 80],
                        [0, lambda x: (x - 20) / 30, lambda x: 1 - (x - 50) / 30, 0])

def mw(x):
    return np.piecewise(x, [x <= 30, (30 < x) & (x < 70), x >= 70], [0, lambda x: (x - 30) / 40, 1])

def plot_functions():
    x = np.linspace(10, 30, 100)

    plt.figure(figsize=(5, 5))
    plt.plot(x, tn(x), label='tn(x)')
    plt.plot(x, tw(x), label='tw(x)')
    plt.xlabel('temperatura (°C)')
    plt.ylabel('przynależność')
    plt.legend()
    plt.grid(True)
    plt.savefig('tn_tw.png')
    plt.show()

    x = np.linspace(0, 100, 1000)
    plt.figure(figsize=(5, 5))
    plt.plot(x, wn(x), label='wn(x)')
    plt.plot(x, ww(x), label='ww(x)')
    plt.xlabel('wilgotność (%)')
    plt.ylabel('przynależność')
    plt.legend()
    plt.grid(True)
    plt.savefig('wn_ww.png')
    plt.show()

    plt.figure(figsize=(5, 5))
    plt.plot(x, mn(x), label='mn(x)')
    plt.plot(x, ms(x), label='ms(x)')
    plt.plot(x, mw(x), label='mw(x)')
    plt.xlabel('moc klimatyzatora (%)')
    plt.ylabel('przynależność')
    plt.legend()
    plt.grid(True)
    plt.savefig('mn_ms_mw.png')
    plt.show()

def s_1(x):
    return np.piecewise(x, [x <= 60, (60 < x) & (x < 70), x >= 70], [0.25, lambda x: 1 - (x - 30) / 40, 0])

def s_2(x):
    return np.piecewise(x, [x <= 20, (20 < x) & (x <= 37.4), (37.4 < x) & (x < 62.6), (62.6 < x) & (x < 80), x >= 80],
                        [0, lambda x: (x - 20) / 30, 0.58, lambda x: 1 - (x - 50) / 30, 0])

def s_3(x):
    return np.piecewise(x, [x <= 30, (30 < x) & (x < 46.8), x >= 46.8], [0, lambda x: (x - 30) / 40, 0.42])


def plot_rules():
    x = np.linspace(0, 100, 1000)
    
    plt.plot(x, s_1(x), label='$s_1(x)$')
    plt.plot(x, s_2(x), label='$s_2(x)$')
    plt.plot(x, s_3(x), label='$s_3(x)$')
    
    plt.xlabel('x')
    plt.ylabel('s(x)')
    plt.title('Reguły')
    plt.legend()
    plt.grid(True)
    plt.savefig('rules.png')
    plt.show()

def s(x):
    return np.piecewise(x, [x <= 27.5, (27.5 < x) & (x <= 37.4), (37.4 < x) & (x < 62.6), (62.6 < x) & (x < 67.4), x >= 67.4],
                        [0.25, lambda x: (x - 20) / 30, 0.58, lambda x: 1 - (x - 50) / 30, 0.42])

def calculate_center_of_mass(x, y):
    x = np.sum(x * y) / np.sum(y)
    y = 0.5 * np.sum(y ** 2) / np.sum(y)
    return x, y

def plot_composition():
    x = np.linspace(0, 100, 1000)

    center_of_mass = calculate_center_of_mass(x, s(x))
    
    plt.plot(x, s(x), label='$s(x)$')
    plt.fill_between(x, s(x), 0, alpha=0.5)

    plt.scatter(center_of_mass[0], center_of_mass[1], marker='o', color='red', label='środek ciężkości')

    plt.xlabel('x')
    plt.ylabel('s(x)')
    plt.title('Funkcja przynależności wyniku s(x)')
    plt.legend()
    plt.grid(True)
    plt.savefig('composition.png')
    plt.show()

    print('Środek ciężkości: ', center_of_mass)

if __name__ == '__main__':
    plot_functions()
    plot_rules()
    plot_composition()
