# central jDE config used by metaheuristics variants
# Update JDE_PARAMS at runtime before running experiments to change behavior

JDE_PARAMS = {
    # probability to re-sample F for an individual in each generation
    "tau_F": 0.1,
    # probability to re-sample CR for an individual in each generation
    "tau_CR": 0.1,
    # allowed range for F when re-sampling
    "F_low": 0.1,
    "F_up": 0.9,
}

# Additional experiment/variant controls
JDE_PARAMS.setdefault('inject_every', 50)
JDE_PARAMS.setdefault('inject_prob', 0.02)
JDE_PARAMS.setdefault('restart_every', 100)
JDE_PARAMS.setdefault('restart_frac', 0.05)

# Levy-flight and LF-perturbation tuning hooks (used by EAOLF variants)
# alpha_levy: scale of Levy perturbation (default 0.01)
# AF_mult: multiplicative factor applied to AF = sqrt((iter+1)/maxIter)
JDE_PARAMS.setdefault('alpha_levy', 0.01)
JDE_PARAMS.setdefault('AF_mult', 1.0)
# Adaptive Levy-flight defaults
JDE_PARAMS.setdefault('levy_fraction', 0.05)  # fraction of population to apply Levy per iter (conservative)
JDE_PARAMS.setdefault('alpha_levy_init', 0.005)
JDE_PARAMS.setdefault('alpha_levy_min', 0.0005)
JDE_PARAMS.setdefault('alpha_levy_max', 0.2)
JDE_PARAMS.setdefault('alpha_adapt_rate', 0.05)  # multiplicative adapt rate on success/failure (smoother)
JDE_PARAMS.setdefault('levy_clamp_fraction', 0.08)  # clamp Levy step to this fraction of (ub-lb)
JDE_PARAMS.setdefault('levy_apply_mode', 'random')  # 'random' or 'per_individual_prob'
# Levy application phase: 'early' applies Levy when AF < threshold, 'late' for AF > threshold, 'always' to ignore
JDE_PARAMS.setdefault('levy_apply_phase', 'early')
JDE_PARAMS.setdefault('levy_phase_threshold', 0.6)
