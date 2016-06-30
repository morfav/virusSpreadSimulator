# SIR model: S(usceptible), I(nfected), R(ecovered)

import numpy as np


def exponential_var(lambd):
    return -np.log(np.random.random())/lambd


def poisson_distribution(lambd, t):
    cumulative = 0.0
    events = 0

    exp_var = exponential_var(lambd)
    while cumulative + exp_var < t:
        cumulative += exp_var
        events += 1
        exp_var = exponential_var(lambd)
    return events


def simulate(N, beta, gamma):
    Ns = [N - 1]
    Ni = [1]
    Nr = 0
    t = 0

    while (Nr < N):
        infection_rate = (beta * Ns[-1] * Ni[-1]) / N
        recovery_rate = (gamma * Ni)
        new_infections = poisson_distribution(infection_rate, 1)
        # np.random.normal(mean, std)
        new_recoveries = np.random.normal(9, 2)

        Ns.append(Ns[-1] - new_infections)
        Ni.append(Ni[-1] + new_infections)

        t += 1
        Nr = N - Ns[-1] - Ni[-1]

# Agent-based modeling
# R: epinet package