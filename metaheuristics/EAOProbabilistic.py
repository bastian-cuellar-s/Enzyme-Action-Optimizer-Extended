import numpy as np
from utils.eao_improvements import reflect_bounds, adaptive_update_on_success, gaussian_local_perturbation

# jDE state storage (per-population)
_JDE_STATE = {}

try:
    from utils.jde_config import JDE_PARAMS
except Exception:
    JDE_PARAMS = {}


def iterarEAO_Probabilistic(
    maxIter, iter, dim, population, fitness, best, lb0, ub0, EvaluateCatalysis=None
):
    new_population = np.copy(population)
    # exploration probability that decreases over time (start higher -> decay)
    prob_exploracion = 0.5 * (1 - (iter / maxIter)) + 0.25
    AF = np.sqrt((iter + 1) / maxIter)

    # jDE parameters (override via utils.jde_config.JDE_PARAMS)
    tau_F = JDE_PARAMS.get("tau_F", 0.1)
    tau_CR = JDE_PARAMS.get("tau_CR", 0.1)
    F_low, F_up = (
        JDE_PARAMS.get("F_low", 0.1),
        JDE_PARAMS.get("F_up", 0.9),
    )

    pop_id = id(population)
    EnzymeCount = population.shape[0]
    # initialize jDE state per-population
    if pop_id not in globals().get("_JDE_STATE", {}):
        globals()['_JDE_STATE'] = {}
    if pop_id not in _JDE_STATE or _JDE_STATE[pop_id]["F"].shape[0] != EnzymeCount:
        _JDE_STATE[pop_id] = {
            "F": 0.4 + 0.5 * np.random.rand(EnzymeCount),
            "CR": 0.1 + 0.8 * np.random.rand(EnzymeCount),
        }

    F_array = _JDE_STATE[pop_id]["F"]
    CR_array = _JDE_STATE[pop_id]["CR"]

    for i in range(population.shape[0]):
        # per-individual jDE proposals
        Fi = F_array[i]
        CRi = CR_array[i]
        if np.random.rand() < tau_F:
            Fi_trial = F_low + np.random.rand() * (F_up - F_low)
        else:
            Fi_trial = Fi
        if np.random.rand() < tau_CR:
            CR_trial = np.random.rand()
        else:
            CR_trial = CRi

        if np.random.rand() < prob_exploracion:
            # Exploración
            p, q_idx = np.random.choice(
                [idx for idx in range(population.shape[0]) if idx != i],
                2,
                replace=False,
            )
            S1, S2 = population[p, :], population[q_idx, :]
            EC = 0.1
            scA1 = EC + (1 - EC) * np.random.rand(dim)
            exA = (EC + (1 - EC) * np.random.rand(dim)) * AF
            candidate = (
                population[i, :] + scA1 * (S1 - S2) + exA * (best - population[i, :])
            )
        else:
            # Explotación
            q = np.random.rand(dim)
            candidate = (best - population[i, :]) + q * np.sin(AF * population[i, :])

        # Evaluate candidate and apply elitist replacement
        if EvaluateCatalysis is not None:
            try:
                cand_fit = float(EvaluateCatalysis(candidate))
            except Exception:
                cand_fit = np.sum(candidate ** 2)
        else:
            cand_fit = np.sum(candidate ** 2)

        current_fit = float(fitness[i]) if fitness is not None else np.sum(population[i, :] ** 2)
        if cand_fit < current_fit:
            bounded = reflect_bounds(candidate, lb0, ub0)
            new_population[i, :] = bounded
            adaptive_update_on_success(F_array, CR_array, i, Fi_trial, CR_trial, alpha=0.1)
        else:
            new_population[i, :] = population[i, :].copy()

    # Calcular fitness usando la función objetivo si está disponible
    if EvaluateCatalysis is not None:
        try:
            new_fitness = np.array([float(EvaluateCatalysis(x)) for x in new_population])
        except Exception:
            new_fitness = np.sum(new_population**2, axis=1)
    else:
        new_fitness = np.sum(new_population**2, axis=1)

    # occasional small local perturbation to maintain diversity
    if (iter % 50) == 0:
        new_population = gaussian_local_perturbation(new_population, best, lb0, ub0, sigma=0.01, prob=0.02)

    return new_population, new_fitness
