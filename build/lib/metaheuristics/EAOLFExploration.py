import numpy as np
from scipy.special import gamma

def levy_flight(beta, D):
    sigma_u = (gamma(1 + beta) * np.sin(np.pi * beta / 2) /
               (gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)))**(1 / beta)
    sigma_v = 1
    u = np.random.normal(0, sigma_u, D)
    v = np.random.normal(0, sigma_v, D)
    step = u / (np.abs(v)**(1 / beta))
    return step

def iterarEAO_LF_Exploration(maxIter, iter, dim, population, fitness, best, lb0, ub0):
    new_population = np.copy(population)
    AF = np.sqrt((iter + 1) / maxIter)

    for i in range(population.shape[0]):
        q = np.random.rand(dim)
        candidate1 = (best - population[i, :]) + q * np.sin(AF * population[i, :])

        alpha = 0.01 * (ub0 - lb0)
        beta_levy = 1.5
        levy_step = levy_flight(beta_levy, dim)
        candidate2 = population[i, :] + alpha * levy_step

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
