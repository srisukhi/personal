from dateutil import parser as dtparser
import matplotlib.pyplot as plt
import pandas as pd
import sys


def datm(str):
    return dtparser.parse(str)


def plot(series, title='No title', one_graph=True):
    if isinstance(series, list) and one_graph is False:
        names = [elem.name for elem in series]
        print("Plotting these series:", names)
        for elem in series:
            plt.plot(elem)
        plt.legend(names)
    elif isinstance(series, pd.core.frame.DataFrame):
        plt.plot(series)
        plt.legend(list(series))
    else:
        plt.plot(series)
    if series.min().min().min() >= 0:
        plt.ylim(bottom=0)
    plt.title(title)
    plt.show()


def analyze(water):
    water['rollmean12'] = water['Usage'].rolling(12).mean()
    water['Usage'] = water['Usage'].astype('float')
    plt.plot(water['Usage'])
    plt.plot(water['rollmean12'])
    plt.ylim(bottom=0)
    plt.xlabel('Date')
    plt.ylabel('Usage (Gallons)')
    plt.title('Monthly water usage')
    plt.show()

    annual = water['Usage'].groupby(water.index.year).sum()
    plt.bar(annual.index, annual)
    plt.xlabel('Date')
    plt.ylabel('Usage (Gallons)')
    plt.title('Annual water usage')
    plt.show()

    water['rollmean6'] = water['Usage'].rolling(6).mean()
    last12 = water.loc[datm('2020-07-01'):]
    plt.bar(last12.index, last12['rollmean6'], width=20)
    plt.xlabel('Date')
    plt.ylabel('Usage (Gallons)')
    plt.title('12-month water usage')
    plt.show()

    last18 = water.loc[datm('2020-01-01'):]
    plt.bar(last18.index, last18['Usage'], width=20)
    plt.xlabel('Date')
    plt.ylabel('Usage (Gallons)')
    plt.title('18-month water usage')
    plt.show()

def main(wfile):
    cmrd = 'Current_Meter_Read_Date'
    pmrd ='Previous_Meter_Read_Date'
    water = pd.read_csv(wfile, parse_dates=[cmrd, pmrd])
    water['Date'] = water[pmrd] + (water[cmrd] - water[pmrd]) / 2
    water.set_index('Date', inplace=True)
    water.sort_index(inplace=True)
    water['Usage'] = water['Usage'] * 748.052
    analyze(water)


if __name__ == "__main__":
    main(sys.argv[1])
