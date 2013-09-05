#!/usr/bin/env python

"""Module for setting up plotting routines"""

import pylab as pl
import data_evac


def plot_all_data():
    """Plot the data and decorate the output."""
    plot_evac_data()
    decorate_plot1()


def plot_evac_data():
    """Plot the measured data."""
    pl.plot(data_evac.exit_distance,
            data_evac.flow,
            'bs', ms=10, mew=0, label='Exp. Data')


def plot_model1(m):
    """
    Plot each realization from Model 1.
    """
    x = pl.arange(0.01, 700, 1)
    for theta_t in m.theta.trace():
        flow = theta_t[0] * x**theta_t[1] * x**theta_t[2]
        pl.plot(x, flow,
                color='gray', alpha=.75, zorder=-1)

    theta = m.theta.stats()['mean']
    flow = theta[0] * x**theta[1] * x**theta[2]
    pl.plot(x, flow,
            color='purple', linewidth=5,
            label='Model 1')
    decorate_plot1()


def plot_model2(m):
    """
    Plot each realization from Model 2.
    """
    x = pl.arange(0.01, 700, 1)
    for theta_t in m.theta.trace():
        flow = theta_t[0] * x**theta_t[1] * x**theta_t[2]
        pl.plot(x, flow,
                color='gray', alpha=.75, zorder=-1)

    theta = m.theta.stats()['mean']
    flow = theta[0] * x**theta[1] * x**theta[2]
    pl.plot(x, flow,
            color='purple', linewidth=5,
            label='Model 2')
    decorate_plot2()


def plot_model3(m):
    """
    Plot each realization from Model 3.
    """
    x = pl.arange(0.01, 700, 1)
    for theta_t in m.theta.trace():
        flow = theta_t[0] * x**theta_t[1] * x**theta_t[2] * x**theta_t[3]
        pl.plot(x, flow,
                color='gray', alpha=.75, zorder=-1)

    theta = m.theta.stats()['mean']
    flow = theta[0] * x**theta[1] * x**theta[2] * x**theta[3]
    pl.plot(x, flow,
            color='purple', linewidth=5,
            label='Model 3')
    decorate_plot3()


def decorate_plot1():
    """Decorate the plot with labels."""
    pl.axis([0, 700, 0.1, 0.9])
    pl.legend(numpoints=1, prop=dict(size=20), fancybox=True)
    pl.xticks(fontsize=20)
    pl.xlabel('theta[0] * occupants^theta[1] * exit_distance^theta[2]', fontsize=24)
    pl.yticks(fontsize=20)
    pl.ylabel('Flow (people/s)', fontsize=24)


def decorate_plot2():
    """Decorate the plot with labels."""
    pl.axis([0, 700, 0.1, 0.9])
    pl.legend(numpoints=1, prop=dict(size=20), fancybox=True)
    pl.xticks(fontsize=20)
    pl.xlabel('theta[0] * occupants^theta[1] * effective_width^theta[2]', fontsize=24)
    pl.yticks(fontsize=20)
    pl.ylabel('Flow (people/s)', fontsize=24)


def decorate_plot3():
    """Decorate the plot with labels."""
    pl.axis([0, 700, 0.1, 0.9])
    pl.legend(numpoints=1, prop=dict(size=20), fancybox=True)
    pl.xticks(fontsize=20)
    pl.xlabel('theta[0] * occupants^theta[1] * exit_distance^theta[2] * effective_width^theta[3]', fontsize=24)
    pl.yticks(fontsize=20)
    pl.ylabel('Flow (people/s)', fontsize=24)

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
