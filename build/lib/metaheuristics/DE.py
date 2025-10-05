import numpy as np

def iterar_DE(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    N = population.shape[0]
    F = 0.8
    CR = 0.9
    for i in range(N):
        P_i = population[i, :]
        r_indices = np.random.choice([idx for idx in range(N) if idx != i], 3, replace=False)
        P_r1, P_r2, P_r3 = population[r_indices, :]
        mutant_vector = P_r1 + F * (P_r2 - P_r3)
        trial_vector = np.copy(P_i)
        j_rand = np.random.randint(0, dim)
        for j in range(dim):
            if np.random.rand() < CR or j == j_rand:
                trial_vector[j] = mutant_vector[j]
        trial_fitness = np.sum(trial_vector**2)
        if trial_fitness < fitness[i]:
            new_population[i, :] = np.clip(trial_vector, lb0, ub0)
        else:
            new_population[i, :] = P_i
    new_fitness = np.array([np.sum(new_population[i, :]**2) for i in range(N)])
    return new_population, new_fitness
