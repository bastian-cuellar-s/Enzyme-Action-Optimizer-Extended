import numpy as np

def iterar_MFO(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    t = iter + 1
    T = maxIter
    a = -1 + t * ((-1) / T)
    b = 1
    sorted_indices = np.argsort(fitness)
    flames = population[sorted_indices]
    for i in range(population.shape[0]):
        P_i = population[i, :]
        F_i = flames[i, :]
        D = np.abs(F_i - P_i)
        l = 2 * np.random.rand(dim) - 1
        new_pos = D * np.exp(b * l) * np.cos(2 * np.pi * l) + F_i
        new_population[i, :] = np.clip(new_pos, lb0, ub0)
    new_fitness = np.array([np.sum(new_population[i, :]**2) for i in range(population.shape[0])])
    return new_population, new_fitness
