import numpy as np
import importlib
otros = importlib.import_module('otros')
get_best_agents = otros.get_best_agents

def iterar_GWO(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    t = iter + 1
    T = maxIter
    N = population.shape[0]
    a = 2 - t * (2 / T)
    alpha, beta, delta = get_best_agents(population, fitness)
    for i in range(N):
        P_i = population[i, :]
        r1, r2 = np.random.rand(2)
        A1 = 2 * a * r1 - a
        C1 = 2 * r2
        D_alpha = np.abs(C1 * alpha - P_i)
        P1 = alpha - A1 * D_alpha
        r1, r2 = np.random.rand(2)
        A2 = 2 * a * r1 - a
        C2 = 2 * r2
        D_beta = np.abs(C2 * beta - P_i)
        P2 = beta - A2 * D_beta
        r1, r2 = np.random.rand(2)
        A3 = 2 * a * r1 - a
        C3 = 2 * r2
        D_delta = np.abs(C3 * delta - P_i)
        P3 = delta - A3 * D_delta
        new_pos = (P1 + P2 + P3) / 3
        new_population[i, :] = np.clip(new_pos, lb0, ub0)
    new_fitness = np.array([np.sum(new_population[i, :]**2) for i in range(population.shape[0])])
    return new_population, new_fitness
