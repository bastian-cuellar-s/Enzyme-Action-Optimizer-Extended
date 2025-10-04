import numpy as np

def iterar_PSO(maxIter, iter, dim, population, fitness, best, lb0, ub0, velocity, pbest):
    new_population = np.copy(population)
    new_velocity = np.copy(velocity)
    N = population.shape[0]
    w = 0.729
    c1 = 1.4944
    c2 = 1.4944
    for i in range(N):
        r1, r2 = np.random.rand(2, dim)
        cognitive = c1 * r1 * (pbest[i, :] - population[i, :])
        social = c2 * r2 * (best - population[i, :])
        new_velocity[i, :] = w * velocity[i, :] + cognitive + social
        new_pos = population[i, :] + new_velocity[i, :]
        new_population[i, :] = np.clip(new_pos, lb0, ub0)
    new_fitness = np.array([np.sum(new_population[i, :]**2) for i in range(N)])
    return new_population, new_fitness, new_velocity
