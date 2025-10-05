import numpy as np

def iterarEAO_DE_Hybrid(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    AF = np.sqrt((iter + 1) / maxIter)
    F = 0.5
    
    for i in range(population.shape[0]):
        q = np.random.rand(dim)
        candidate1 = (best - population[i, :]) + q * np.sin(AF * population[i, :])

        r1, r2 = np.random.choice([idx for idx in range(population.shape[0]) if idx != i], 2, replace=False)
        mutant_vector = population[i, :] + F * (best - population[i, :]) + F * (population[r1, :] - population[r2, :])
        candidate2 = mutant_vector

        # Decisión interna basada en fitness temporal
        fit1 = np.sum(candidate1**2)
        fit2 = np.sum(candidate2**2)

        if fit1 < fit2:
            new_population[i, :] = np.clip(candidate1, lb0, ub0)
        else:
            new_population[i, :] = np.clip(candidate2, lb0, ub0)
    
    # --- CORRECCIÓN ---
    new_fitness = np.sum(new_population**2, axis=1)
    return new_population, new_fitness
