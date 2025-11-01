import numpy as np
from utils.eao_improvements import reflect_bounds, adaptive_update_on_success, gaussian_local_perturbation

# jDE state: store per-population per-individual F and CR values so they persist across iterations
_JDE_STATE = {}

# Optional runtime-configurable jDE params
try:
    from utils.jde_config import JDE_PARAMS
except Exception:
    JDE_PARAMS = {}


def iterarEAO_DE_Hybrid(
    maxIter,
    iter,
    dim,
    population,
    fitness,
    best,
    lb0,
    ub0,
    EvaluateCatalysis=None,
):
    """Iteración híbrida EAO-DE.

    Parámetros adicionales:
    - EvaluateCatalysis: callable opcional que recibe un vector candidato y devuelve
      un fitness escalar. Si se omite, se usa la función Sphere (suma de cuadrados)
      como fallback para mantener compatibilidad con llamadas actuales.
    """
    new_population = np.copy(population)
    AF = np.sqrt((iter + 1) / maxIter)

    # jDE parameters (can be overridden via utils.jde_config.JDE_PARAMS)
    tau_F = JDE_PARAMS.get("tau_F", 0.1)
    tau_CR = JDE_PARAMS.get("tau_CR", 0.1)
    F_low, F_up = (
        JDE_PARAMS.get("F_low", 0.1),
        JDE_PARAMS.get("F_up", 0.9),
    )

    pop_id = id(population)
    EnzymeCount = population.shape[0]
    # initialize jDE state for this population if needed
    if pop_id not in _JDE_STATE or _JDE_STATE[pop_id]["F"].shape[0] != EnzymeCount:
        # initial F in [0.4,0.9], CR in [0.1,0.9]
        _JDE_STATE[pop_id] = {
            "F": 0.4 + 0.5 * np.random.rand(EnzymeCount),
            "CR": 0.1 + 0.8 * np.random.rand(EnzymeCount),
        }

    F_array = _JDE_STATE[pop_id]["F"]
    CR_array = _JDE_STATE[pop_id]["CR"]

    for i in range(population.shape[0]):
        q = np.random.rand(dim)
        candidate1 = (best - population[i, :]) + q * np.sin(AF * population[i, :])

        # jDE: propose trial F and CR for this individual
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

        # construct mutant using Fi_trial (current-to-best plus differential)
        r1, r2 = np.random.choice([idx for idx in range(EnzymeCount) if idx != i], 2, replace=False)
        mutant_vector = (
            population[i, :]
            + Fi_trial * (best - population[i, :])
            + Fi_trial * (population[r1, :] - population[r2, :])
        )

        # binomial crossover between current and mutant using CR_trial
        cross = np.random.rand(dim) < CR_trial
        # ensure at least one dimension is taken from mutant
        if not np.any(cross):
            cross[np.random.randint(dim)] = True
        candidate2 = population[i, :].copy()
        candidate2[cross] = mutant_vector[cross]

        # Decisión interna basada en la función objetivo real si está disponible.
        if EvaluateCatalysis is not None:
            try:
                fit1 = float(EvaluateCatalysis(candidate1))
                fit2 = float(EvaluateCatalysis(candidate2))
            except Exception:
                # Fallback seguro a Sphere si la evaluación falla por cualquier motivo
                fit1 = np.sum(candidate1**2)
                fit2 = np.sum(candidate2**2)
        else:
            fit1 = np.sum(candidate1**2)
            fit2 = np.sum(candidate2**2)

        # Choose the better candidate
        if fit1 < fit2:
            chosen = candidate1
            chosen_fit = fit1
        else:
            chosen = candidate2
            chosen_fit = fit2

        # Elitist replacement: only replace if chosen is better than current
        current_fit = float(fitness[i]) if fitness is not None else np.sum(population[i, :] ** 2)
        if chosen_fit < current_fit:
            bounded = reflect_bounds(chosen, lb0, ub0)
            new_population[i, :] = bounded
            # accept jDE parameters and nudge history toward the successful trial
            adaptive_update_on_success(F_array, CR_array, i, Fi_trial, CR_trial, alpha=0.1)
        else:
            new_population[i, :] = population[i, :].copy()

    # --- CORRECCIÓN: calcular fitness usando la función objetivo si está disponible ---
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
