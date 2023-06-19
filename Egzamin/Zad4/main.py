import keras.optimizers
import matplotlib.pyplot as plt
import numpy as np
from keras import Sequential, layers, backend as K


def wygeneruj_trapez():
    _x = np.linspace(0, 8, 100)
    _y1 = -0.67 * _x + 4
    _y2 = 0.5 * _x
    _y3 = 0.5 * _x + 3
    _y4 = -1.5 * _x + 14
    plt.plot(_x, _y1, label='$-0.67*x_1 - x_2 + 4 = 0$', color='green')
    plt.plot(_x, _y2, label='$0.5*x_1 - x_2 = 0$', color='blue')
    plt.plot(_x, _y3, label='$0.5*x_1 - x_2 + 3 = 0$', color='red')
    plt.plot(_x, _y4, label='$-1.5*x_1 - x_2 + 14 = 0$', color='purple')

    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.ylim(0, 8)
    plt.xlim(0, 8)

    plt.legend(loc='upper left')



# Funkcja aktywacji step
def step(x):
    return K.cast(K.greater(x, 0), K.floatx())


def testuj_model_teor():
    weights1 = np.array([
        [2 / 3, -1 / 2, 1 / 2, -3 / 2],
        [1, 1, -1, -1]])

    biases1 = np.array([-4, 0, 3, 14])

    weights2 = np.array([[1, 1, 1, 1]]).T

    biases2 = np.array([-3])

    # Definicja modelu sieci neuronowej
    model = Sequential([
        layers.Dense(4, activation=step, input_shape=(
            2,), weights=[weights1, biases1]),
        layers.Dense(1, activation=step, weights=[weights2, biases2])
    ])

    # Wygenerowanie 1000 punktow z przedzialu [0, 8]
    points = np.random.uniform(low=0, high=8, size=(1000, 2))
    predictions = model.predict(points)

    # Wygenerowanie wykresu z punktami
    plt.scatter(points[:, 0], points[:, 1], c=predictions.flatten())
    wygeneruj_trapez()
    plt.savefig('punkty_teor.png')

    plt.show()


# Funkcja, ktora sprawdza, czy punkt nalezy do obszaru trapezu
def is_in_trapezoid(x1, x2):
    condition1 = (2 / 3 * x1 + x2 - 4 >= 0)
    condition2 = (x2 - 0.5 * x1 >= 0)
    condition3 = (x2 - 0.5 * x1 - 3 <= 0)
    condition4 = (1.5 * x1 + x2 - 14 <= 0)
    return condition1 and condition2 and condition3 and condition4


def testuj_model():
    # Definicja modelu sieci neuronowej
    model = Sequential([
        layers.Dense(4, activation='sigmoid', input_shape=(2,)),
        layers.Dense(1, activation='sigmoid')
    ])

    # Kompilacja modelu
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.01),
                  loss='mse', metrics=['accuracy'])

    # Wygenerowanie 1000 punktow z przedzialu [0, 8]
    points = np.random.uniform(low=0, high=8, size=(1000, 2))

    # Wygenerowanie etykiet dla punktow
    labels = np.array([is_in_trapezoid(x1, x2) for x1, x2 in points])

    # Trenowanie modelu
    model.fit(points, labels, epochs=200, batch_size=32)

    # Wypisz wagi i biasy
    print(*model.layers[0].get_weights())
    print(*model.layers[1].get_weights())

    # Predykcja dla punktow testowych

    test_points = np.random.uniform(low=0, high=8, size=(1000, 2))

    predictions = model.predict(test_points)

    # Wygenerowanie wykresu z punktami
    plt.scatter(test_points[:, 0], test_points[:, 1], c=predictions.flatten())
    wygeneruj_trapez()
    plt.savefig('punkty.png')

    plt.show()


if __name__ == "__main__":
    wygeneruj_trapez()
    plt.savefig('trapez.png')
    plt.show()

    testuj_model_teor()

    testuj_model()
