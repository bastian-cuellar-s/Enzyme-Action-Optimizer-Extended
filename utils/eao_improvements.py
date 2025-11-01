import numpy as np


def reflect_bounds(vec, lb, ub):
    """Reflective boundary handling: reflects values that go out of bounds back into [lb, ub].

    Works element-wise and returns a clipped/reflected copy.
    """
    vec = np.array(vec, copy=True, dtype=float)
    lb = np.array(lb, dtype=float)
    ub = np.array(ub, dtype=float)

    # Ensure vec is shaped like lb/ub for elementwise ops
    if vec.ndim == 0:
        # if lb/ub are arrays, create a vector matching their shape
        if lb.ndim == 0:
            vec = np.full((), float(vec))
        else:
            vec = np.full(lb.shape, float(vec))
    # If lb/ub are scalars but vec is vector, expand lb/ub to vec.shape
    if lb.ndim == 0 and vec.ndim > 0:
        lb = np.full(vec.shape, float(lb))
    if ub.ndim == 0 and vec.ndim > 0:
        ub = np.full(vec.shape, float(ub))
    if vec.shape != lb.shape:
        # try flatten/reshape if sizes match
        if vec.size == lb.size:
            vec = vec.flatten().reshape(lb.shape)
        else:
            # fallback: make a copy shaped like lb
            vec = np.broadcast_to(vec, lb.shape).copy()

    for i in range(vec.shape[0]):
        if vec[i] < lb[i]:
            vec[i] = lb[i] + (lb[i] - vec[i])
            if vec[i] > ub[i]:
                vec[i] = lb[i]
        elif vec[i] > ub[i]:
            vec[i] = ub[i] - (vec[i] - ub[i])
            if vec[i] < lb[i]:
                vec[i] = ub[i]
    return vec


def adaptive_update_on_success(F_array, CR_array, idx, F_trial, CR_trial, alpha=0.1):
    """Move individual parameters a bit towards the successful trial values.

    This is a lightweight success-history mechanism: on success we set
    F = (1-alpha)*F + alpha*F_trial, CR similar.
    """
    F_array[idx] = (1 - alpha) * F_array[idx] + alpha * F_trial
    CR_array[idx] = (1 - alpha) * CR_array[idx] + alpha * CR_trial


def gaussian_local_perturbation(population, best, lb, ub, sigma=0.01, prob=0.02):
    """Apply small Gaussian perturbation to a subset of individuals with given probability.

    Perturbation is scaled by the domain range (ub-lb) so it's dimension-aware.
    """
    pop = population.copy()
    D = pop.shape[1]
    rng = np.random.RandomState()
    range_scale = (np.array(ub) - np.array(lb))
    for i in range(pop.shape[0]):
        if rng.rand() < prob:
            noise = rng.normal(0, sigma, D) * range_scale
            pop[i, :] = pop[i, :] + noise
            # ensure bounds via reflection
            pop[i, :] = reflect_bounds(pop[i, :], lb, ub)
    return pop
