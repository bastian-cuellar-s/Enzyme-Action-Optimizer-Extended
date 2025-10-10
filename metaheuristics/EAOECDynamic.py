import numpy as np


def iterarEAO_EC_Dynamic(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)

    EC_inicial = 0.4
    tasa_decaimiento_EC = 0.995
    ec_actual = EC_inicial * (tasa_decaimiento_EC**iter)
    AF = np.sqrt((iter + 1) / maxIter)

    for i in range(population.shape[0]):
        p, q_idx = np.random.choice(
            [idx for idx in range(population.shape[0]) if idx != i], 2, replace=False
        )
        S1, S2 = population[p, :], population[q_idx, :]

        scA1 = ec_actual + (1 - ec_actual) * np.random.rand(dim)
        exA = (ec_actual + (1 - ec_actual) * np.random.rand(dim)) * AF
        candidateA = (
            population[i, :] + scA1 * (S1 - S2) + exA * (best - population[i, :])
        )

        scB1 = ec_actual + (1 - ec_actual) * np.random.rand()
        exB = (ec_actual + (1 - ec_actual) * np.random.rand()) * AF
        candidateB = (
            population[i, :] + scB1 * (S1 - S2) + exB * (best - population[i, :])
        )

        # Decisión interna basada en fitness temporal
        fitA = np.sum(candidateA**2)
        fitB = np.sum(candidateB**2)

        Upd = candidateA if fitA < fitB else candidateB
        new_population[i, :] = np.clip(Upd, lb0, ub0)

    # --- CORRECCIÓN ---
    new_fitness = np.sum(new_population**2, axis=1)
    return new_population, new_fitness
