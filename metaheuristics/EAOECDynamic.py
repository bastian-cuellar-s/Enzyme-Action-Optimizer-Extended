import numpy as np
from utils.eao_improvements import reflect_bounds, adaptive_update_on_success, gaussian_local_perturbation

# jDE state storage (per-population)
_JDE_STATE = {}

try:
    from utils.jde_config import JDE_PARAMS
except Exception:
    JDE_PARAMS = {}


def iterarEAO_EC_Dynamic(
    maxIter, iter, dim, population, fitness, best, lb0, ub0, EvaluateCatalysis=None
):
    new_population = np.copy(population)

    EC_inicial = 0.4
    tasa_decaimiento_EC = 0.995
    ec_actual = EC_inicial * (tasa_decaimiento_EC ** iter)
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
    if pop_id not in _JDE_STATE or _JDE_STATE[pop_id]["F"].shape[0] != EnzymeCount:
        _JDE_STATE[pop_id] = {
            "F": 0.4 + 0.5 * np.random.rand(EnzymeCount),
            "CR": 0.1 + 0.8 * np.random.rand(EnzymeCount),
        }

    F_array = _JDE_STATE[pop_id]["F"]
    CR_array = _JDE_STATE[pop_id]["CR"]

    for i in range(population.shape[0]):
        # select partners
        p, q_idx = np.random.choice(
            [idx for idx in range(population.shape[0]) if idx != i], 2, replace=False
        )
        S1, S2 = population[p, :], population[q_idx, :]

        # propose per-individual jDE parameters
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

        scA1 = ec_actual + (1 - ec_actual) * np.random.rand(dim)
        exA = (ec_actual + (1 - ec_actual) * np.random.rand(dim)) * AF
        candidateA = (
            population[i, :] + scA1 * (S1 - S2) + exA * (best - population[i, :])
        )

        scB1 = ec_actual + (1 - ec_actual) * np.random.rand()
        exB = (ec_actual + (1 - ec_actual) * np.random.rand()) * AF
        # combine DE-style perturbation scaled by Fi_trial
        mutant = population[i, :] + Fi_trial * (best - population[i, :]) + Fi_trial * (S1 - S2)
        # crossover between A/B and mutant using CR_trial
        cross = np.random.rand(dim) < CR_trial
        if not np.any(cross):
            cross[np.random.randint(dim)] = True
        candidateB = population[i, :].copy()
        candidateB[cross] = mutant[cross]

        # Decisión interna basada en la función objetivo real si está disponible.
        if EvaluateCatalysis is not None:
            try:
                fitA = float(EvaluateCatalysis(candidateA))
                fitB = float(EvaluateCatalysis(candidateB))
            except Exception:
                fitA = np.sum(candidateA**2)
                fitB = np.sum(candidateB**2)
        else:
            fitA = np.sum(candidateA**2)
            fitB = np.sum(candidateB**2)

        Upd = candidateA if fitA < fitB else candidateB

        # Elitist replacement and jDE parameter acceptance
        current_fit = float(fitness[i]) if fitness is not None else np.sum(population[i, :] ** 2)
        upd_fit = fitA if (Upd is candidateA) else fitB
        if upd_fit < current_fit:
            bounded = reflect_bounds(Upd, lb0, ub0)
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
