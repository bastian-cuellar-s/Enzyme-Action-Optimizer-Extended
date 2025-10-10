import numpy as np


def iterar_SCA(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    t = iter + 1
    T = maxIter
    a = 2
    r1 = a - t * (a / T)
    for i in range(population.shape[0]):
        P_i = population[i, :]
        r2 = 2 * np.pi * np.random.rand(dim)
        r3 = 2 * np.random.rand(dim)
        r4 = np.random.rand(dim)
        if np.mean(r4) < 0.5:
            new_pos = P_i + r1 * np.sin(r2) * np.abs(r3 * best - P_i)
        else:
            new_pos = P_i + r1 * np.cos(r2) * np.abs(r3 * best - P_i)
        new_population[i, :] = np.clip(new_pos, lb0, ub0)
    new_fitness = np.array(
        [np.sum(new_population[i, :] ** 2) for i in range(population.shape[0])]
    )
    return new_population, new_fitness
