import numpy as np

def iterar_GMO(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    N = population.shape[0]
    weights = 1 / (fitness + np.finfo(float).eps)
    weights = weights / np.sum(weights)
    for i in range(N):
        P_i = population[i, :]
        r_indices = np.random.choice([idx for idx in range(N) if idx != i], 3, replace=False)
        P_r1, P_r2, P_r3 = population[r_indices, :]
        W_i = weights[i]
        r = np.random.rand()
        new_pos = P_i + W_i * r * (best - P_i) + (1 - W_i) * (P_r1 - P_r2) * r * (P_r3 - P_i)
        new_population[i, :] = np.clip(new_pos, lb0, ub0)
    new_fitness = np.array([np.sum(new_population[i, :]**2) for i in range(new_population.shape[0])])
    return new_population, new_fitness
