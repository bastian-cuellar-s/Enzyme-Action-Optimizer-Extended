import numpy as np
from scipy.special import gamma
from utils import helpers
levy_flight = helpers.levy_flight

def iterar_HLOA(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    t = iter + 1
    T = maxIter
    a = 2 * (1 - t / T)
    b = 2 * (t / T)
    for i in range(population.shape[0]):
        P_i = population[i, :]
        R1 = np.random.rand()
        if R1 < 0.5:
            r = np.random.rand(dim)
            A = a * r - a
            C = 2 * r
            D = np.abs(C * best - P_i)
            new_pos = best - A * D
        else:
            P_rand = population[np.random.randint(0, population.shape[0]), :]
            r_vec = np.random.rand(dim)
            beta_levy = 1.5
            LF = levy_flight(beta_levy, dim)
            P_escape = (P_rand + P_i) / 2
            new_pos = P_escape + b * LF * r_vec * (best - P_i)
        new_population[i, :] = np.clip(new_pos, lb0, ub0)
    new_fitness = np.array([np.sum(new_population[i, :]**2) for i in range(new_population.shape[0])])
    return new_population, new_fitness
