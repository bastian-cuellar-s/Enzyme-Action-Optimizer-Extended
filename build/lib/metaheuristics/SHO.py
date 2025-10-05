import numpy as np

def iterar_SHO(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    t = iter + 1
    T = maxIter
    N = population.shape[0]
    c1 = 2 * (1 - t / T)
    c2 = 2 * (t / T)
    for i in range(N):
        P_i = population[i, :]
        rand_idx = np.random.randint(0, N)
        P_rand = population[rand_idx, :]
        P_avg = np.mean(population, axis=0)
        R = np.random.rand()
        if R < 0.5:
            A = c1 * (2 * np.random.rand(dim) - 1)
            new_pos = P_i + A * (best - P_i)
        else:
            r2 = np.random.rand()
            if r2 < 0.5:
                new_pos = P_i + c2 * np.random.rand(dim) * (P_rand - P_i)
            else:
                new_pos = P_i + c2 * np.random.rand(dim) * (P_avg - P_i)
        new_population[i, :] = np.clip(new_pos, lb0, ub0)
    new_fitness = np.array([np.sum(new_population[i, :]**2) for i in range(new_population.shape[0])])
    return new_population, new_fitness
