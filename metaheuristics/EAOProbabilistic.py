import numpy as np


def iterarEAO_Probabilistic(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    prob_exploracion = 0.5
    AF = np.sqrt((iter + 1) / maxIter)

    for i in range(population.shape[0]):
        if np.random.rand() < prob_exploracion:
            # Exploración
            p, q_idx = np.random.choice(
                [idx for idx in range(population.shape[0]) if idx != i],
                2,
                replace=False,
            )
            S1, S2 = population[p, :], population[q_idx, :]
            EC = 0.1
            scA1 = EC + (1 - EC) * np.random.rand(dim)
            exA = (EC + (1 - EC) * np.random.rand(dim)) * AF
            new_pos = (
                population[i, :] + scA1 * (S1 - S2) + exA * (best - population[i, :])
            )
        else:
            # Explotación
            q = np.random.rand(dim)
            new_pos = (best - population[i, :]) + q * np.sin(AF * population[i, :])

        new_population[i, :] = np.clip(new_pos, lb0, ub0)

    # --- CORRECCIÓN ---
    new_fitness = np.sum(new_population**2, axis=1)
    return new_population, new_fitness
