import numpy as np

def iterar_HGSO(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    t = iter + 1
    T = maxIter
    N = population.shape[0]
    K = 100
    alpha = 0.1
    T_r = 298.15
    T_t = np.exp(-t / T) * (T_r - 200) + 200
    for i in range(N):
        P_i = population[i, :]
        r = np.random.rand(dim)
        H_i = alpha * np.exp(- (T_r - T_t) / T_t)
        S_i = K * H_i
        r_vec = np.random.rand(dim)
        new_pos = P_i + r_vec * S_i * (best - P_i) + np.random.normal(0, 1, dim) * H_i
        new_population[i, :] = np.clip(new_pos, lb0, ub0)
    new_fitness = np.array([np.sum(new_population[i, :]**2) for i in range(new_population.shape[0])])
    return new_population, new_fitness
