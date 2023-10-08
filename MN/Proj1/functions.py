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

    return macd, signal


def plotWilliams(data, period=10):
    williams = []

    for i in range(period, len(data)):
        _max = data[i - period: i + 1].max()
        _min = data[i - period: i + 1].min()

        williams.append((data[i] - _max) / (_max - _min) * 100)

    plt.figure(figsize=(10, 5))
    plt.plot(range(period, len(data)), williams, color='gray', label='%R Williamsa')
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
    print(f'Zysk końcowy: {cash - 1000} PLN.')

    plt.figure(figsize=(10, 5))
    plt.plot(range(33, len(data)), cash_history, color='blue')
    plt.grid(color='gray', linestyle='--')
    plt.axhline(y=1000, color='red', linestyle='--')
    plt.xlabel('numer dnia')
    plt.ylabel('Ilość pieniędzy (PLN)')


def plotFragment(ax1, ax2, data, macd, signal, pkt_kupna, pkt_sprzedazy, start, stop, williams=None, ax3=None):
    ax1.plot(range(start, stop), data[start:stop], color='orange', label='Cena akcji')
    ax1.set_title('Cena akcji CD Projekt Red', fontweight='bold')
    ax1.set_ylabel('Cena akcji (PLN)')
    ax1.set_xticks(range(start, stop + 1, 10))
    ax1.grid(color='gray', linestyle='--')
    ax1.legend((pkt_kupna, pkt_sprzedazy), ('Punkt kupna', 'Punkt sprzedaży'))

    ax2.plot(range(start, stop), macd[start:stop], color='blue', label='MACD')
    ax2.plot(range(start, stop), signal[start:stop], color='orange', label='SIGNAL')
    ax2.set_title('MACD i SIGNAL', fontweight='bold')
    ax2.set_ylabel('Wartość')
    ax2.set_xticks(range(start, stop + 1, 10))
    ax2.grid(color='gray', linestyle='--')
    ax2.legend()

    if williams and ax3 is not None:
        ax3.plot(range(start, stop), williams[start:stop], color='gray', label='%R Williamsa')
        ax3.set_title('%R Williamsa', fontweight='bold')
        ax3.set_xlabel('numer dnia')
        ax3.set_ylabel('Wartość')
        ax3.set_xticks(range(start, stop + 1, 10))
        ax3.grid(color='gray', linestyle='--')
        ax3.set_xlabel('numer dnia')
        ax3.axhline(y=-80, color='green', linestyle='--', label='Sprzedaż')
        ax3.axhline(y=-20, color='red', linestyle='--', label='Kupno')
        ax3.legend()
    else:
        ax2.set_xlabel('numer dnia')


def simulateSimple(dataset, macd, signal):
    cash = 1000
    actions = 0
    cash_history = [cash]

    data = dataset['Close']

    print(f'Początkowa ilość pieniędzy: {cash} PLN')

    start, stop = 460, 580

    plt.figure(figsize=(10, 5))
    plt.subplots_adjust(hspace=0.5)
    ax1 = plt.subplot(2, 1, 1)
    ax2 = plt.subplot(2, 1, 2)

    for i in range(35, len(data)):
        if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1] and cash > data[i]:
            _actions = int(cash / data[i])
            cash -= _actions * data[i]
            actions += _actions
            print(f"Dzień {i}: ", end=' ')
            print(f'Kupiłem {_actions} akcje za {_actions * data[i]} PLN.', end=' ')
            print(f'Stan: {cash} PLN, {actions} akcji.')
            if stop > i > start:
                pkt_kupna = ax1.scatter(i, data[i], color='red')
                ax2.scatter(i, macd[i], color='red')
        elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1] and actions > 0:
            print(f"Dzień {i}: ", end=' ')
            print(f'Sprzedałem {actions} akcje za {actions * data[i]} PLN.', end=' ')
            cash += actions * data[i]
            actions = 0
            print(f'Stan: {cash} PLN, {actions} akcji.')
            if stop > i > start:
                pkt_sprzedazy = ax1.scatter(i, data[i], color='green')
                ax2.scatter(i, macd[i], color='green')

        cash_history.append(cash)

    plotFragment(ax1, ax2, data, macd, signal, pkt_kupna, pkt_sprzedazy, start, stop)
    plt.savefig('zoom_simple.png')

    endSimulation(cash, actions, data, cash_history)
    plt.title('Gotówka - symulacja prosta', fontweight='bold')
    plt.savefig('simulation_simple.png')


def simulateAdvanced(dataset, macd, signal, williams):
    cash = 1000
    actions = 0
    cash_history = [cash]

    data = dataset['Close']

    print(f'Początkowa ilość pieniędzy: {cash} PLN')

    start, stop = 460, 580

    plt.figure(figsize=(10, 8))
    plt.subplots_adjust(hspace=0.5)
    ax1 = plt.subplot(3, 1, 1)
    ax2 = plt.subplot(3, 1, 2)
    ax3 = plt.subplot(3, 1, 3)

    for i in range(35, len(data)):
        if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1] and williams[i] > -20 and cash > data[i]:
            _actions = int(cash / data[i])
            cash -= _actions * data[i]
            actions += _actions
            print(f"Dzień {i}: ", end=' ')
            print(f'Kupiłem {_actions} akcje za {_actions * data[i]} PLN.', end=' ')
            print(f'Stan: {cash} PLN, {actions} akcji.')
            if stop > i > start:
                pkt_kupna = ax1.scatter(i, data[i], color='red')
                ax2.scatter(i, macd[i], color='red')
                ax3.scatter(i, williams[i], color='red')
        elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1] and williams[i] < -80 and actions > 0:
            print(f"Dzień {i}: ", end=' ')
            print(f'Sprzedałem {actions} akcje za {actions * data[i]} PLN.', end=' ')
            cash += actions * data[i]
            actions = 0
            print(f'Stan: {cash} PLN, {actions} akcji.')
            if stop > i > start:
                pkt_sprzedazy = ax1.scatter(i, data[i], color='green')
                ax2.scatter(i, macd[i], color='green')
                ax3.scatter(i, williams[i], color='green')
        cash_history.append(cash)

    plotFragment(ax1, ax2, data, macd, signal, pkt_kupna, pkt_sprzedazy, start, stop, williams, ax3)

    plt.savefig('zoom_advanced.png')

    endSimulation(cash, actions, data, cash_history)
    plt.title('Gotówka - symulacja złożona', fontweight='bold')
    plt.savefig('simulation_advanced.png')
