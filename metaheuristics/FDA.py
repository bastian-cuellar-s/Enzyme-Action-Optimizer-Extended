import numpy as np


def iterar_FDA(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    t = iter + 1
    T = maxIter
    N = population.shape[0]
    w = 0.9 - 0.5 * (t / T)
    c = 0.5 + 0.5 * (t / T)
    for i in range(N):
        P_i = population[i, :]
        r_indices = np.random.choice(
            [idx for idx in range(N) if idx != i], 3, replace=False
        )
        P_r1, P_r2, P_r3 = population[r_indices, :]
        FD = P_i + c * (best - P_i) + np.random.rand() * (P_r1 - P_r2)
        FV = w * (P_r3 - P_i)
        new_pos = P_i + FD + FV
        new_population[i, :] = np.clip(new_pos, lb0, ub0)
    new_fitness = np.array(
        [np.sum(new_population[i, :] ** 2) for i in range(new_population.shape[0])]
    )
    return new_population, new_fitness
