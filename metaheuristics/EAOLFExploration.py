import numpy as np
from scipy.special import gamma
from utils.eao_improvements import (
    reflect_bounds,
    adaptive_update_on_success,
    gaussian_local_perturbation,
    inject_global_best,
    restart_worst,
)
import os
import json

# jDE state storage (per-population)
_JDE_STATE = {}

try:
    from utils.jde_config import JDE_PARAMS
except Exception:
    JDE_PARAMS = {}


def levy_flight(beta, D):
    sigma_u = (
        gamma(1 + beta)
        * np.sin(np.pi * beta / 2)
        / (gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))
    ) ** (1 / beta)
    sigma_v = 1
    u = np.random.normal(0, sigma_u, D)
    v = np.random.normal(0, sigma_v, D)
    step = u / (np.abs(v) ** (1 / beta))
    return step


def iterarEAO_LF_Exploration(
    maxIter, iter, dim, population, fitness, best, lb0, ub0, EvaluateCatalysis=None
):
    new_population = np.copy(population)
    AF = np.sqrt((iter + 1) / maxIter)

    # jDE parameters (overridable from utils.jde_config.JDE_PARAMS)
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
        # adaptive levy state
        _JDE_STATE[pop_id]["alpha_levy_ind"] = np.full(EnzymeCount, JDE_PARAMS.get('alpha_levy_init', 0.01))
        _JDE_STATE[pop_id]["levy_prob_ind"] = np.full(EnzymeCount, JDE_PARAMS.get('levy_fraction', 0.2))

    F_array = _JDE_STATE[pop_id]["F"]
    CR_array = _JDE_STATE[pop_id]["CR"]

    # adaptive levy helper parameters
    alpha_ind = _JDE_STATE[pop_id]["alpha_levy_ind"]
    levy_prob_ind = _JDE_STATE[pop_id]["levy_prob_ind"]
    levy_fraction = JDE_PARAMS.get('levy_fraction', 0.2)
    alpha_min = JDE_PARAMS.get('alpha_levy_min', 0.001)
    alpha_max = JDE_PARAMS.get('alpha_levy_max', 0.5)
    alpha_rate = JDE_PARAMS.get('alpha_adapt_rate', 0.1)
    clamp_frac = JDE_PARAMS.get('levy_clamp_fraction', 0.2)
    apply_mode = JDE_PARAMS.get('levy_apply_mode', 'random')

    for i in range(population.shape[0]):
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

        # decide whether to apply Levy to this individual
        if apply_mode == 'random':
            do_levy = np.random.rand() < levy_fraction
        else:
            do_levy = np.random.rand() < levy_prob_ind[i]

        # phase gating: optionally restrict Levy to early/late iterations via AF
        levy_apply_phase = JDE_PARAMS.get('levy_apply_phase', 'early')
        levy_phase_threshold = JDE_PARAMS.get('levy_phase_threshold', 0.6)
        try:
            if levy_apply_phase == 'early' and AF >= levy_phase_threshold:
                do_levy = False
            elif levy_apply_phase == 'late' and AF <= levy_phase_threshold:
                do_levy = False
        except Exception:
            pass

        q = np.random.rand(dim)
        # scale the exploration/exploitation components by Fi_trial
        candidate1 = (best - population[i, :]) + q * np.sin(AF * population[i, :]) * Fi_trial

        if do_levy:
            alpha_i = float(alpha_ind[i])
            beta_levy = 1.5
            levy_step = levy_flight(beta_levy, dim)
            max_step = clamp_frac * np.linalg.norm(ub0 - lb0)
            step_norm = np.linalg.norm(levy_step)
            if step_norm > 0:
                levy_step = levy_step * (min(step_norm, max_step) / step_norm)
            candidate2 = population[i, :] + (alpha_i * levy_step) * Fi_trial
        else:
            candidate2 = population[i, :].copy()

        # crossover between candidate1 and candidate2 guided by CR_trial
        cross = np.random.rand(dim) < CR_trial
        if not np.any(cross):
            cross[np.random.randint(dim)] = True
        candidate = candidate1.copy()
        candidate[cross] = candidate2[cross]

        # Decisión interna basada en la función objetivo real si está disponible.
        if EvaluateCatalysis is not None:
            try:
                cand_fit = float(EvaluateCatalysis(candidate))
            except Exception:
                cand_fit = np.sum(candidate**2)
        else:
            cand_fit = np.sum(candidate**2)

        # Elitist replacement and jDE parameter acceptance
        current_fit = float(fitness[i]) if fitness is not None else np.sum(population[i, :] ** 2)
        if cand_fit < current_fit:
            bounded = reflect_bounds(candidate, lb0, ub0)
            new_population[i, :] = bounded
            # lightweight success-history: nudge individual's params toward successful trial
            adaptive_update_on_success(F_array, CR_array, i, Fi_trial, CR_trial, alpha=0.05)
            try:
                if do_levy:
                    alpha_ind[i] = min(alpha_max, alpha_ind[i] * (1.0 + alpha_rate))
            except Exception:
                pass
        else:
            new_population[i, :] = population[i, :].copy()
            try:
                if do_levy:
                    alpha_ind[i] = max(alpha_min, alpha_ind[i] * (1.0 - alpha_rate))
            except Exception:
                pass

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
        # reduced perturbation probability for LF variant to avoid overly large jumps
        new_population = gaussian_local_perturbation(new_population, best, lb0, ub0, sigma=0.01, prob=0.01)

    # injection and restart hooks
    inject_every = JDE_PARAMS.get('inject_every', 50)
    inject_prob = JDE_PARAMS.get('inject_prob', 0.02)
    restart_every = JDE_PARAMS.get('restart_every', 100)
    restart_frac = JDE_PARAMS.get('restart_frac', 0.05)
    if (iter % inject_every) == 0:
        new_population = inject_global_best(new_population, best, lb0, ub0, prob=inject_prob, noise_scale=0.001)
    if (iter % restart_every) == 0:
        new_population, _ = restart_worst(new_population, new_fitness, lb0, ub0, frac=restart_frac)

        # write diagnostics for this iteration (summary of adaptive Levy state)
        try:
            logs_dir = os.path.join('results', 'logs', 'lf_diagnostics')
            os.makedirs(logs_dir, exist_ok=True)
            pid = os.getpid()
            fname = os.path.join(logs_dir, f'eaolfexploration_pid{pid}.jsonl')
            entry = {
                'iter': int(iter),
                'mean_alpha': float(np.mean(alpha_ind)),
                'min_alpha': float(np.min(alpha_ind)),
                'max_alpha': float(np.max(alpha_ind)),
                'mean_levy_prob': float(np.mean(levy_prob_ind)),
            }
            with open(fname, 'a', encoding='utf-8') as fh:
                fh.write(json.dumps(entry) + '\n')
        except Exception:
            pass

    return new_population, new_fitness
