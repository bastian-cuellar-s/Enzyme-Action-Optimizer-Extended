import numpy as np


def iterar_WSO(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    t = iter + 1
    T = maxIter
    N = population.shape[0]
    S_t = 2 - t * ((2) / T)
    H_t = 1 - t * ((1) / T)
    b = 1  # Parámetro de espiral
    for i in range(N):
        P_i = population[i, :]
        r = np.random.rand()
        if r < 0.5:
            R_aud = 2 * np.random.rand() * H_t
            rv = np.random.uniform(-1, 1)
            D_best = np.abs(best - P_i)
            new_pos = best - D_best * np.exp(b * rv) * np.cos(2 * np.pi * rv) * R_aud
        else:
            P_rand = population[np.random.randint(0, N), :]
            R_smell = 2 * np.random.rand() * S_t
            new_pos = P_i + R_smell * (P_rand - P_i)
        new_population[i, :] = np.clip(new_pos, lb0, ub0)
    new_fitness = np.array(
        [np.sum(new_population[i, :] ** 2) for i in range(new_population.shape[0])]
    )
    return new_population, new_fitness
