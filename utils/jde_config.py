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
