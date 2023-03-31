import pandas as pd
from functions import *

if __name__ == '__main__':
    url = 'https://query1.finance.yahoo.com/v7/finance/download/CDR.WA?period1=1547596800&period2=1669852800&interval=1d&events=history&includeAdjustedClose=true'
    raw_dataset = pd.read_csv(url, index_col='Date', parse_dates=True)

    dataset = raw_dataset.dropna()

    print(dataset.shape)
    print(dataset.head())
    print(dataset.tail())
    print(dataset.describe().T)

    dataset['Close'].plot(legend=False, figsize=(10, 5), color='red')

    plt.annotate('Premiera gry Cyberpunk 2077', xy=('2020-12-04', int(dataset['Close'].loc['2020-12-04'])),
                 xytext=('2021-03-01', 410),
                 arrowprops=dict(arrowstyle="->"), color='blue')

    plt.xticks(pd.date_range(start='2019-01-16', end='2023-01-01', freq='3MS', inclusive="both"), rotation=45)

    plt.xlabel('Data')
    plt.ylabel('Cena akcji (PLN)')
    plt.title('Cena akcji CD Projekt Red od 2019-01-16 do 2022-11-30', fontweight='bold')
    plt.grid(color='gray', linestyle='--')

    plt.savefig('wykres.png')

    macd, signal = plotSIGNALMACD(dataset['Close'])

    simulateSimple(dataset, macd, signal)

    williams = plotWilliams(dataset['Close'])

    print()

    simulateAdvanced(dataset, macd, signal, williams)

    plt.show()
