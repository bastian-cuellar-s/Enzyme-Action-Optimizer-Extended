import numpy as np
from scipy.special import gamma # Necesario para Vuelo de Lévy (HLOA, SHO, MFO)


## SCA function moved to metaheuristics/SCA.py


## MFO function moved to metaheuristics/MFO.py


## GWO function moved to metaheuristics/GWO.py


## DE function moved to metaheuristics/DE.py




# Función para obtener los tres mejores agentes (soluciones) según el fitness
def get_best_agents(population, fitness):
	idx_sorted = np.argsort(fitness)
	alpha = population[idx_sorted[0], :]
	beta = population[idx_sorted[1], :]
	delta = population[idx_sorted[2], :]
	return alpha, beta, delta

# Función de vuelo de Lévy (usada en HLOA, SHO, MFO, etc.)
def levy_flight(beta, D):
	sigma_u = (gamma(1 + beta) * np.sin(np.pi * beta / 2) /
			   (gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)))**(1 / beta)
	sigma_v = 1
	u = np.random.normal(0, sigma_u, D)
	v = np.random.normal(0, sigma_v, D)
	step = u / (np.abs(v)**(1 / beta))
	return step