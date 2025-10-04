import numpy as np

def iterar_MVO(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    # Convertir límites a arrays de tamaño dim si son escalares o arrays de tamaño 1
    lb0 = np.array(lb0)
    ub0 = np.array(ub0)
    if lb0.size == 1:
        lb0 = np.full(dim, lb0.item())
    if ub0.size == 1:
        ub0 = np.full(dim, ub0.item())
    new_population = np.copy(population)
    t = iter + 1
    T = maxIter
    max_fit = np.max(fitness)
    min_fit = np.min(fitness)
    if (max_fit - min_fit) == 0:
        norm_fitness = np.zeros_like(fitness)
    else:
        norm_fitness = (fitness - min_fit) / (max_fit - min_fit)
    WEP = 0.2 + t * (0.8 / T)
    TDR = 1 - t**(1/6) / T**(1/6)
    for i in range(population.shape[0]):
        P_i = population[i, :]
        r1, r2 = np.random.rand(2)
        if r1 < WEP:
            j = np.random.randint(0, dim)
            if r2 < 0.5:
                new_population[i, j] = best[j] + TDR * (ub0[j] - lb0[j]) * np.random.rand()
            else:
                new_population[i, j] = best[j] - TDR * (ub0[j] - lb0[j]) * np.random.rand()
        else:
            probs = norm_fitness / np.sum(norm_fitness)
            k = np.random.choice(population.shape[0], p=probs)
            u_k = population[k, :]
            new_pos = u_k + TDR * np.random.normal(0, 1, dim)
        new_population[i, :] = np.clip(new_population[i, :], lb0, ub0)
    new_fitness = np.array([np.sum(new_population[i, :]**2) for i in range(population.shape[0])])
    return new_population, new_fitness
