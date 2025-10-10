import numpy as np


def iterar_GTO(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    t = iter + 1
    T = maxIter
    N = population.shape[0]
    P = 0.03
    F = np.cos(2 * np.random.rand()) + 1
    C = F * (1 - t / T)
    for i in range(N):
        P_i = population[i, :]
        r = np.random.rand()
        if r < P:
            rand_pos = lb0 + np.random.rand(dim) * (ub0 - lb0)
            new_pos = rand_pos
        else:
            r2 = np.random.rand()
            if r2 >= 0.5:
                A = 2 * np.random.rand(dim) - 1
                new_pos = best - (best * C) + P_i * A
            else:
                rand_idx = np.random.randint(0, N)
                P_r = population[rand_idx, :]
                new_pos = P_i - C * (C * P_r - P_i)
        new_population[i, :] = np.clip(new_pos, lb0, ub0)
    new_fitness = np.array(
        [np.sum(new_population[i, :] ** 2) for i in range(new_population.shape[0])]
    )
    return new_population, new_fitness
