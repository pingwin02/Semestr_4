from matplotlib import pyplot as plt
import pandas as pd


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

    plt.xlabel('numer dnia')
    plt.ylabel('Wartość')
    plt.title('MACD i SIGNAL', fontweight='bold')
    plt.legend()
    plt.savefig('macdsignal.png')

    plt.figure(figsize=(10, 5))
    plt.subplots_adjust(hspace=0.3)

    plt.subplot(2, 1, 1)

    plt.plot(range(460, 580), data[460:580], color='red', label='Cena akcji')

    plt.ylabel('Cena akcji (PLN)')
    plt.title('Cena akcji CD Projekt Red', fontweight='bold')
    plt.grid(color='gray', linestyle='--')

    plt.subplot(2, 1, 2)

    plt.plot(range(460, 580), macd[460:580], color='blue', label='MACD')
    plt.plot(range(460, 580), signal[460:580], color='red', label='SIGNAL')

    plt.scatter(460, -10, color='red', label='Kupno')
    plt.scatter(460, -10, color='green', label='Sprzedaż')

    for i in range(460, 580):
        if macd[i] > signal[i] and macd[i - 1] < signal[i - 1]:
            plt.scatter(i, macd[i], color='red')

        elif macd[i] < signal[i] and macd[i - 1] > signal[i - 1]:
            plt.scatter(i, macd[i], color='green')

    plt.grid(color='gray', linestyle='--')
    plt.xlabel('numer dnia')
    plt.ylabel('Wartość')
    plt.title('MACD i SIGNAL', fontweight='bold')
    plt.legend()
    plt.savefig('macdsignal_zoom.png')

    return macd, signal


def plotWilliams(data, period=10):
    williams = []

    for i in range(period, len(data)):
        _max = data[i - period: i + 1].max()
        _min = data[i - period: i + 1].min()

        williams.append((data[i] - _max) / (_max - _min) * 100)

    plt.figure(figsize=(10, 5))
    plt.plot(range(period, len(data)), williams, color='orange', label='Williams')
    plt.grid(color='gray', linestyle='--')

    plt.axhline(y=-80, color='green', linestyle='--', label='Sprzedaż')
    plt.axhline(y=-20, color='red', linestyle='--', label='Kupno')

    plt.xlabel('numer dnia')
    plt.ylabel('Wartość')
    plt.title('Wskaźnik %R Williamsa', fontweight='bold')
    plt.legend()
    plt.savefig('williams.png')

    williams = [0.0] * period + williams

    return williams


def endSimulation(cash, actions, data, cash_history):
    print(f'Zysk: {cash - 1000} PLN. Pozostało akcji: {actions} sztuk.')
    print(f'Sprzedaję resztę akcji za {actions * data[len(data) - 1]} PLN.')
    cash += actions * data[len(data) - 1]
    cash_history.append(cash)
    print(f'Zysk całkowity: {cash - 1000} PLN.')

    plt.figure(figsize=(10, 5))
    plt.plot(range(33, len(data)), cash_history, color='blue')
    plt.grid(color='gray', linestyle='--')
    plt.axhline(y=1000, color='red', linestyle='--')
    plt.xlabel('numer dnia')
    plt.ylabel('Ilość pieniędzy (PLN)')


def simulateSimple(dataset, macd, signal):
    cash = 1000
    actions = 0
    cash_history = [cash]

    data = dataset['Close']

    print(f'Początkowa ilość pieniędzy: {cash} PLN')

    for i in range(35, len(data)):
        if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1] and cash > data[i]:
            _actions = int(cash / data[i])
            cash -= _actions * data[i]
            print(f"Dzień {i}: ", end=' ')
            print(f'Kupiłem {_actions} akcje za {_actions * data[i]} PLN.')
            actions += _actions
        elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1] and actions > 0:
            print(f"Dzień {i}: ", end=' ')
            print(f'Sprzedałem {actions} akcje za {actions * data[i]} PLN.')
            cash += actions * data[i]
            actions = 0
        cash_history.append(cash)

    endSimulation(cash, actions, data, cash_history)
    plt.title('Gotówka - symulacja prosta', fontweight='bold')
    plt.savefig('simulation_simple.png')


def simulateAdvanced(dataset, macd, signal, williams):
    cash = 1000
    actions = 0
    cash_history = [cash]

    data = dataset['Close']

    print(f'Początkowa ilość pieniędzy: {cash} PLN')

    for i in range(35, len(data)):
        if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1] and williams[i] > -20 and cash > data[i]:
            _actions = int(cash / data[i])
            cash -= _actions * data[i]
            print(f"Dzień {i}: ", end=' ')
            print(f'Kupiłem {_actions} akcje za {_actions * data[i]} PLN.')
            actions += _actions
        elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1] and williams[i] < -80 and actions > 0:
            print(f"Dzień {i}: ", end=' ')
            print(f'Sprzedałem {actions} akcje za {actions * data[i]} PLN.')
            cash += actions * data[i]
            actions = 0
        cash_history.append(cash)

    endSimulation(cash, actions, data, cash_history)
    plt.title('Gotówka - symulacja złożona', fontweight='bold')
    plt.savefig('simulation_advanced.png')
