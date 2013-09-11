#!/usr/bin/env python

"""Module for setting up plotting routines"""

import pylab as pl
import numpy as np
import data_evac


def plot_all_data(x, y, xlabel, ylabel):
    """Plot the data and decorate the output."""
    plot_evac_data(x, y, xlabel, ylabel)
    decorate_plot(x, y, xlabel, ylabel)


def plot_evac_data(x, y, xlabel, ylabel):
    """Plot the measured data."""
    pl.plot(x, y, 'bs', ms=10, mew=0, label='Exp. Data')


def plot_model(m, x, y, xlabel, ylabel):
    """
    Plot each realization.
    """
    x1 = pl.linspace(0, np.max(x)*1.1, 1000)
    for theta_t in m.theta.trace():
        y1 = theta_t * x1
        pl.plot(x1, y1,
                color='gray', alpha=.75, zorder=-1)

    theta = m.theta.stats()['mean']
    y1 = theta * x1
    pl.plot(x1, y1,
            color='purple', linewidth=5,
            label='Model 1')
    decorate_plot(x, y, xlabel, ylabel)


def decorate_plot(x, y, xlabel, ylabel):
    """Decorate the plot with labels."""
    pl.axis([0, np.max(x)*1.1, 0, np.max(y)*1.1])
    pl.legend(numpoints=1, prop=dict(size=20), fancybox=True, loc='lower right')
    pl.xticks(fontsize=20)
    pl.xlabel(xlabel, fontsize=24)
    pl.yticks(fontsize=20)
    pl.ylabel(ylabel, fontsize=24)


# def plot_joint_density(X, Y, bounds=None):
#     """
#     Plot joint density of X and Y.

#     Used in example 4 to explore model convergence.
#     """
#     if bounds:
#         X_min, X_max, Y_min, Y_max = bounds
#     else:
#         X_min = X.min()
#         X_max = X.max()
#         Y_min = Y.min()
#         Y_max = Y.max()

#     pl.plot(X, Y,
#             linestyle='none', marker='o',
#             color='green', mec='green',
#             alpha=.75, zorder=-99)

#     import scipy.stats
#     gkde = scipy.stats.gaussian_kde([X, Y])
#     x, y = pl.mgrid[X_min:X_max:(X_max-X_min)/25.,
#                     Y_min:Y_max:(Y_max-Y_min)/25.]
#     z = pl.array(gkde.evaluate([x.flatten(), y.flatten()])).reshape(x.shape)
#     pl.contour(x, y, z, linewidths=2)

#     pl.axis([X_min, X_max, Y_min, Y_max])


def plot_predicted_data(y_pred):
    """
    Plot predicted data side-by-side in subplots.

    Used in example 5 to explore model convergence.
    """
    pl.subplot(3,1,1)
    plot_evac_data()
    decorate_plot()
    pl.xlabel('')
    pl.ylabel('')

    pl.subplot(3,1,2)
    plot_predicted_sample(data_evac.exit_distance, y_pred)
    decorate_plot()
    pl.xlabel('')

    pl.subplot(3,1,3)
    plot_predicted_sample(data_evac.exit_distance, y_pred)
    decorate_plot()
    pl.ylabel('')

    pl.subplots_adjust(hspace=0.)


def plot_predicted_sample(x, y_pred):
    """Used by the plot_predicted_data function."""
    t = pl.rand() * len(y_pred.trace())
    y_t = y_pred.trace()[t]
    pl.plot(x, y_t, 'g^', ms=12, mew=0, label='Prediction')
