import numpy as np

def iterar_WOA(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    t = iter + 1
    T = maxIter
    N = population.shape[0]
    a = 2 - t * (2 / T)
    for i in range(N):
        P_i = population[i, :]
        r1, r2, p = np.random.rand(3)
        A = 2 * a * r1 - a
        C = 2 * r2
        l = np.random.uniform(-1, 1)
        if p < 0.5:
            if np.abs(A) < 1:
                D = np.abs(C * best - P_i)
                new_pos = best - A * D
            else:
                rand_idx = np.random.randint(0, N)
                P_rand = population[rand_idx, :]
                D = np.abs(C * P_rand - P_i)
                new_pos = P_rand - A * D
        else:
            D_prime = np.abs(best - P_i)
            new_pos = D_prime * np.exp(l) * np.cos(2 * np.pi * l) + best
        new_population[i, :] = np.clip(new_pos, lb0, ub0)
    new_fitness = np.array([np.sum(new_population[i, :]**2) for i in range(population.shape[0])])
    return new_population, new_fitness
