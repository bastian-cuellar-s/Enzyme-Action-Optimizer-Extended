import numpy as np
from scipy.special import gamma

def get_best_agents(population, fitness):
    idx_sorted = np.argsort(fitness)
    alpha = population[idx_sorted[0], :]
    beta = population[idx_sorted[1], :]
    delta = population[idx_sorted[2], :]
    return alpha, beta, delta

def levy_flight(beta, D):
    sigma_u = (gamma(1 + beta) * np.sin(np.pi * beta / 2) /
               (gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)))**(1 / beta)
    sigma_v = 1
    u = np.random.normal(0, sigma_u, D)
    v = np.random.normal(0, sigma_v, D)
    step = u / (np.abs(v)**(1 / beta))
    return step
