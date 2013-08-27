#!/usr/bin/env python

"""
This script demonstrates the stabilization of a Markov chain.
You can change the initial probability vector to any value,
(it should sum to 1), yet the chain converges to the same P(x).

"""

import matplotlib
matplotlib.use("Agg")

import numpy as np
from pylab import *

initial = np.array([0.2, 0.7, 0.1])
results = initial

T = np.array([[0.5, 0.5, 0], [0, 0, 1], [0.9, 0.1, 0]])

for i in range(1,50):
    results = np.row_stack([results, np.dot(initial, np.linalg.matrix_power(T, i))])

np.set_printoptions(precision=3)

print results

figure()
plot(results[:,0], 'k-', lw=2, label='$s_1(t)$')
plot(results[:,1], 'r-', lw=2, label='$s_2(t)$')
plot(results[:,2], 'g-', lw=2, label='$s_3(t)$')
xlim([0, 20])
xlabel('Time Step', fontsize=20)
ylabel('Probability', fontsize=20)
legend(loc='upper right')
xticks(fontsize=14)
yticks(fontsize=14)
grid(True)
savefig('MC_Trace.pdf')
