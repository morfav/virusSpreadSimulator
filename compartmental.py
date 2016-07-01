# SIR model: S(usceptible), I(nfected), R(ecovered)

import numpy as np
import matplotlib.pyplot as plt

infection_duration = 9
infection_duration_std = 2
initial_infections = 1


def simulate(N, beta, gamma):
    # susceptible
    Ns = N - initial_infections
    # infected
    Ni = initial_infections
    # recovered
    Nr = 0
    t = 0

    compartments = [[Ns, Ni, Nr]]

    # Generate recovery times for initially infected
    # np.random.normal(mean, std, number of variables to draw)
    days_to_recovery = np.random.normal(infection_duration, infection_duration_std, initial_infections)

    for recovery_period in days_to_recovery:
        recovery_period = max(int(round(recovery_period)), 0)
        # Extend compartments list forward in time if it covers a period shorter than recovery time
        while len(compartments) - 1 < t + recovery_period:
            compartments.append([0, 0, 0])
        # After recovery, -1 infected and +1 recovered
        compartments[t + recovery_period][1] -= 1
        compartments[t + recovery_period][2] += 1

    # While there is a possibility for someone to become infected
    while t < len(compartments) - 1:
        # start next period
        t += 1
        infection_rate = (beta * Ns * Ni) / N
        # recovery_rate = (gamma * Ni)

        # !!
        if infection_rate != 0:
            new_infections = int(min(round(np.random.exponential(infection_rate)), Ns))
            # print("new", new_infections, "Ns", Ns, "\n")

            # np.random.normal(mean, std, number of variables to draw)
            days_to_recovery = np.random.normal(infection_duration, infection_duration_std, new_infections)

            # Number of susceptibles in current period = susceptibles from prior period minus newly infected
            Ns -= new_infections
            Ni += new_infections

            for recovery_period in days_to_recovery:
                recovery_period = max(int(round(recovery_period)), 0)

                while len(compartments) - 1 < t + recovery_period:
                    compartments.append([0, 0, 0])
                compartments[t + recovery_period][1] -= 1
                compartments[t + recovery_period][2] += 1

        compartments[t][0] += Ns
        compartments[t][1] += Ni
        compartments[t][2] += Nr

        Ns = compartments[t][0]
        Ni = compartments[t][1]
        Nr = compartments[t][2]

    return compartments


def run_SIR():

    starting_population = [50*(10**3), 250*(10**3), 50*(10**4), 1*(10**6), 2*(10**6)]
    betas = [0.25, 0.5, 1.5, 3]

    counter = 1

    plt.figure(1)
    for current_population in starting_population:
        for beta in betas:
            plt.subplot(len(starting_population), len(betas), counter)
            plt.title("Population: {}; beta: {}".format(current_population, beta))
            compartments = simulate(current_population, beta, 1)
            susc, inf, rec = plt.plot(compartments)
            plt.ylabel("Infections")
            plt.xlabel("t")
            counter += 1

    plt.figlegend((susc, inf, rec), ("Susceptible", "Infected", "Recovered"), "upper left")
    plt.show()


run_SIR()




# Agent-based modeling
# R: epinet package
