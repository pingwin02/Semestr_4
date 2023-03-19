import pandas as pd
from matplotlib import pyplot as plt


def calcEMA(data, current, period):
    data = data[current: current - period: -1]
    numerator = 0
    denominator = 0
    alfa = 2 / (period + 1)
    for i in range(period):
        numerator += (1 - alfa) ** i * data[i]
        denominator += (1 - alfa) ** i

    return numerator / denominator


def plotSIGNALMACD(data):
    macd = []
    signal = []

    for i in range(26, len(data)):
        macd.append(calcEMA(data, i, 12) - calcEMA(data, i, 26))

    for i in range(9, len(macd)):
        signal.append(calcEMA(macd, i, 9))

    plt.figure(figsize=(10, 5))
    plt.plot(range(26, len(data)), macd, color='blue', label='MACD')
    plt.plot(range(35, len(data)), signal, color='red', label='SIGNAL')
    plt.grid(color='gray', linestyle='--')

    macd = [0.0] * 26 + macd
    signal = [0.0] * 35 + signal

    plt.scatter(0, 0, color='red', label='Kupno')
    plt.scatter(0, 0, color='green', label='Sprzedaż')

    for i in range(35, len(data)):
        if macd[i] > signal[i] and macd[i - 1] < signal[i - 1]:
            plt.scatter(i, macd[i], color='red')

        elif macd[i] < signal[i] and macd[i - 1] > signal[i - 1]:
            plt.scatter(i, macd[i], color='green')

    plt.xlabel('nr próbki')
    plt.ylabel('Wartość')
    plt.title('MACD i SIGNAL', fontweight='bold')
    plt.legend()
    plt.savefig('macdsignal.png')

    return macd, signal


def simulateSimple(dataset, macd, signal):
    cash = 1000

    data = dataset['Close']

    print(f'Początkowa ilość pieniędzy: {cash} PLN')

    for i in range(35, len(data)):
        if macd[i] > signal[i] and macd[i - 1] < signal[i - 1]:
            cash -= data[i]
            print("Dzień: ", dataset.index[i], end=' ')
            print(f'Kupiłem akcje za {data[i]} PLN')
        elif macd[i] < signal[i] and macd[i - 1] > signal[i - 1]:
            cash += data[i]
            print("Dzień: ", dataset.index[i], end=' ')
            print(f'Sprzedałem akcje za {data[i]} PLN')

    print(f'Zysk: {cash - 1000} PLN')
