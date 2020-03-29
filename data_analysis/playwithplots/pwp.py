#!/usr/bin/env python3
#
# References:
#   - https://realpython.com/python-matplotlib-guide/
#

import os
import sys
from io import BytesIO
import tarfile
from urllib.request import urlopen

import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
from plotutils import mplu_realcircle, mplu_text, mplu_realsquare, mplu_arrow, mplu_line

# - - - - - - - - - - - - - - - - - - - - - - - - - -
def linspace_1_to_10():
    # just to start... one liner graph

    # https://realpython.com/python-matplotlib-guide/
    # Calling plt.plot() is just a convenient way to get
    # the current Axes of the current Figure and then call
    # its plot() method (stateful interface always “implicitly
    # tracks” the plot that it wants to reference.
    #
    # pyplot is home to a batch of functions that are really
    # just wrappers around matplotlib’s object-oriented interface.
    # For example, with plt.title(), there are corresponding
    # setter and getter methods within the OO approach,
    # ax.set_title() and ax.get_title(). (Use of getters and
    # setters tends to be more popular in languages such as
    # Java but is a key feature of matplotlib’s OO approach.)

    # Stateful "Matlab-like" interface:
    plt.plot(np.linspace(1, 10, num=10))

# - - - - - - - - - - - - - - - - - - - - - - - - - -
def quadratic_more_structured():

    # the data
    x = np.linspace(-10, 10, num=40)
    x2 = list(map(lambda x: x*x, x))

    # in this example, we work O.O.

    # get top level Figure object
    # A Figure object is the outermost container for a matplotlib
    # graphic, which can contain multiple Axes objects.
    fig, ax = plt.subplots()
    # ax is a single AxesSubplot object
    # to get the current axes the gca() function can be used.
    #ax = fig.gca()
    # One source of confusion is the name: an Axes actually
    # translates into what we think of as an individual plot
    # or graph (rather than the plural of “axis” as we might expect).

    # --- plot data ---------------------------
    ax.plot(x, x2)
    # -----------------------------------------

    # set title
    ax.set_title('Quadratic function')

    # set x axis label
    ax.set_xlabel('$x$')

    # set y axis label
    ax.set_ylabel('$x^2$')

    # set the legend. Please note that this call shall
    # be placed after the call to ax.plot()
    ax.legend(["y = x^2"])


# - - - - - - - - - - - - - - - - - - - - - - - - - -
def two_subplots():
    x = np.random.randint(low=1, high=11, size=50)
    y = x + np.random.randint(1, 5, size=x.size)
    data = np.column_stack((x, y))

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8,4))

    ax1.scatter(x=x, y=y, marker='x', c='r', edgecolor='b')
    ax1.set_title('Scatter $x$ versus $y$')
    ax1.set_xlabel('$x$')
    ax1.set_ylabel('$y$')

    ax2.hist(data, bins=np.arange(data.min(), data.max()), label=('x','y'))
    ax2.legend()
    ax2.set_title('Frequencies of $x$ and $y$')
    ax2.yaxis.tick_right()

# - - - - - - - - - - - - - - - - - - - - - - - - - -
def three_subplots_advanced():
    # prepare data
    url = 'http://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.tgz'
    b = BytesIO(urlopen(url).read())
    fpath = 'CaliforniaHousing/cal_housing.data'
    with tarfile.open(mode='r', fileobj=b) as archive:
        housing = np.loadtxt(archive.extractfile(fpath), delimiter=',')
    y = housing[:, -1]
    pop, age = housing[:, [4, 7]].T

    # prepare the plot
    gridsize = (3, 2)
    fig = plt.figure(figsize=(12, 8))
    ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=2)
    ax2 = plt.subplot2grid(gridsize, (2, 0))
    ax3 = plt.subplot2grid(gridsize, (2, 1))

    ax1.set_title('Home value as a function of home age & area population',
                  fontsize=14)
    sctr = ax1.scatter(x=age, y=pop, c=y, cmap="RdYlGn")
    plt.colorbar(sctr, ax=ax1, format='$%d')
    ax1.set_yscale('log')
    ax2.hist(age, bins='auto')
    ax3.hist(pop, bins='auto', log=True)

    add_titlebox(ax2, 'Histogram: home age')
    add_titlebox(ax3, 'Histogram: area population (log scl.)')

# - - - - - - - - - - - - - - - - - - - - - - - - - -
def plot_with_decorations():

    # same data and plot of the "quadratic" case
    x = np.linspace(-10, 10, num=40)
    x2 = list(map(lambda x: x*x, x))
    fig, ax = plt.subplots()
    ax.plot(x, x2)

    mplu_realcircle(ax, 0, 40, 2.5)
    mplu_text(ax, 0, 40, "Hello MPL")
    mplu_realsquare(ax, -0.55, 77, 0.9)
    mplu_arrow(ax, -7, 75, -2.5, 50, color='darkgreen', scale=10)
    mplu_line(ax, -10, 80, 0, 80, width=3)
    mplu_line(ax, 0, 80, 10, 80, width=3)


# - - - - - - - - - - - - - - - - - - - - - - - - - -
def add_titlebox(ax, text):
    ax.text(.55, .8, text,
            horizontalalignment='center',
            transform=ax.transAxes,
            bbox=dict(facecolor='white', alpha=0.6),
            fontsize=12.5)
    return ax

# ---------------------------------------------------
def main():
    sns.set_style('darkgrid')
    #linspace_1_to_10()
    #quadratic_more_structured()
    #two_subplots()
    #three_subplots_advanced()
    plot_with_decorations()

    plt.show()



if __name__ == '__main__':
    main()

