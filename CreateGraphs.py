import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
import pandas
import numpy as np
from datetime import datetime


data = pandas.read_csv('enron.csv')
data = data.drop(['to', 'from'], axis=1)
data = np.array(data)
names = ['day', 'month', 'year', 'hour']


def plot_against_hour():
    plt.figure(figsize=(20, 20))
    X = data[:, 0:3]
    T = data[:, 3]
    Xnames = names[0:3]
    Tname = names[3]
    for c in range(X.shape[1]):
        plt.subplot(3, 3, c + 1)
        plt.plot(X[:, c], T, 'o', alpha=0.5)
        plt.ylabel(Tname)
        plt.xlabel(Xnames[c])
    plt.show()


def plot_against_year():
    plt.figure(figsize=(20, 20))
    X = np.column_stack((data[:, 0:2], data[:, 3]))
    T = data[:, 2]
    Xnames = np.hstack((names[0:2], names[3]))
    Tname = names[2]
    for c in range(X.shape[1]):
        plt.subplot(3, 3, c + 1)
        plt.plot(X[:, c], T, 'o', alpha=0.5)
        plt.ylabel(Tname)
        plt.xlabel(Xnames[c])
    plt.show()


def plot_against_month():
    plt.figure(figsize=(20, 20))
    X = np.column_stack((data[:, 0], data[:, 2:]))
    T = data[:, 1]
    Xnames = np.hstack((names[0], names[2:]))
    Tname = names[1]
    for c in range(X.shape[1]):
        plt.subplot(3, 3, c + 1)
        plt.plot(X[:, c], T, 'o', alpha=0.5)
        plt.ylabel(Tname)
        plt.xlabel(Xnames[c])
    plt.show()


def plot_against_day():
    plt.figure(figsize=(20, 20))
    X = data[:, 1:]
    T = data[:, 0]
    Xnames = names[1:]
    Tname = names[0]
    for c in range(X.shape[1]):
        plt.subplot(3, 3, c + 1)
        plt.plot(X[:, c], T, 'o', alpha=0.5)
        plt.ylabel(Tname)
        plt.xlabel(Xnames[c])
    plt.show()


def plot_hour_against_date():
    plt.figure(figsize=(20, 20))
    Xtemp = data[:, 0:3]
    list_of_datetimes = []
    T = data[:, 3]
    Tname = names[3]
    for x in Xtemp:
        xString = np.array2string(x, precision=1, suppress_small=True)
        xString = " ".join(xString.split()).replace("[", "").replace("]", "").lstrip()
        list_of_datetimes.append(datetime.strptime(xString, "%d %m %Y"))

    X = list_of_datetimes

    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter("%d/%m/%Y")
    plt.gca().xaxis.set_major_formatter(myFmt)

    plt.plot(X, T, 'o', alpha=0.5)
    plt.ylabel(Tname)
    plt.xlabel("Date: d/m/y")
    plt.show()


if __name__ == '__main__':
    # plot_against_hour()
    # plot_against_year()
    # plot_against_month()
    # plot_against_day()
    plot_hour_against_date()
