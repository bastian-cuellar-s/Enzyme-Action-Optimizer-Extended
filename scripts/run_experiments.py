import os
import numpy as np
from utils.eao_variants import get_variant_func
from problems.continuous.get_f import Get_F
from utils.metrics import calculate_metrics, wilcoxon_test
from multiprocessing import Pool
import multiprocessing
from functools import partial


def _run_single_worker(args):
    """Worker for a single run. args is a tuple:
    (variant_name, run_idx, func_name, EnzymeCount, MaxIter, datos_path)
    """
    v, run_idx, func_name, EnzymeCount, MaxIter, datos_path = args
    import numpy as _np
    from problems.continuous.get_f import Get_F as _Get_F
    from utils.eao_variants import get_variant_func as _get_variant_func

    lb, ub, dim, fobj = _Get_F(func_name)
    lb = _np.array(lb, dtype=float)
    ub = _np.array(ub, dtype=float)

    # seed
    seed = run_idx
    _np.random.seed(seed)
    population = lb + (ub - lb) * _np.random.rand(EnzymeCount, dim)
    fitness = _np.array([fobj(population[i, :]) for i in range(EnzymeCount)])
    best_idx = _np.argmin(fitness)
    best = population[best_idx, :].copy()

    if v == "eao":
        from metaheuristics.eao import EAO as _EAO

        OptimalCatalysis, BestSubstrate, conv_curve = _EAO(
            EnzymeCount, MaxIter, lb, ub, dim, fobj
        )
    else:
        conv_curve = _np.zeros(MaxIter)
        variant_func_local = _get_variant_func(v)
        for it in range(MaxIter):
            try:
                res = variant_func_local(
                    MaxIter, it, dim, population, fitness, best, lb, ub, fobj
                )
            except TypeError:
                res = variant_func_local(MaxIter, it, dim, population, fitness, best, lb, ub)

            if isinstance(res, tuple) and len(res) >= 2:
                population, fitness = res[0], res[1]
            else:
                raise RuntimeError(f"Unexpected return from variant {v}")

            best_idx = _np.argmin(fitness)
            best = population[best_idx, :].copy()
            conv_curve[it] = fitness[best_idx]

        OptimalCatalysis = float(fitness[best_idx])
        BestSubstrate = best

    # Save per-run CSV
    out_csv = os.path.join(datos_path, f"result_{v}_{func_name}_run{run_idx+1}.csv")
    with open(out_csv, "w") as f:
        f.write("Iteration,BestValue\n")
        for i, val in enumerate(conv_curve):
            f.write(f"{i+1},{val}\n")
        f.write("\nBestFinalValue,%s\n" % OptimalCatalysis)

    return v, OptimalCatalysis


def run_experiments(
    func_name="F1",
    variants=None,
    reps=10,
    EnzymeCount=30,
    MaxIter=200,
    n_jobs=1,
    output_dir: str = None,
):
    if variants is None:
        variants = [
            "eaodehybrid",
            "eaoecdynamic",
            "eaolfexploration",
            "eaolfperturbation",
            "eaoprobabilistic",
            "eao",
        ]

    resultados_path = os.path.join("results")
    if output_dir:
        resultados_path = os.path.join(resultados_path, output_dir)
    datos_path = os.path.join(resultados_path, "data")
    plots_path = os.path.join(resultados_path, "plots")
    os.makedirs(datos_path, exist_ok=True)
    os.makedirs(plots_path, exist_ok=True)

    # Load function
    lb, ub, dim, fobj = Get_F(func_name)
    lb = np.array(lb, dtype=float)
    ub = np.array(ub, dtype=float)

    all_results = {v: [] for v in variants}

    # Worker moved to module-level helper to be picklable by multiprocessing
    def _make_args(v, run_idx):
        return (v, run_idx, func_name, EnzymeCount, MaxIter, datos_path)

    # Use multiprocessing to parallelize runs per variant
    for v in variants:
        print(f"Running variant {v} ({reps} reps) with n_jobs={n_jobs}")
        runs = list(range(reps))
        if n_jobs == 1:
            # run sequentially to avoid multiprocessing overhead
            results = []
            for r in runs:
                results.append(_run_single_worker(_make_args(v, r)))
        else:
            # limit processes to available cpus
            procs = min(n_jobs, multiprocessing.cpu_count())
            with Pool(processes=procs) as pool:
                args_iter = [_make_args(v, r) for r in runs]
                results = pool.map(_run_single_worker, args_iter)

        for _, val in results:
            all_results[v].append(val)

    # Compute metrics and wilcoxon comparing eaodehybrid vs others
    summary_path = os.path.join(resultados_path, "experiments_summary.txt")
    with open(summary_path, "w") as out:
        for v, vals in all_results.items():
            metrics = calculate_metrics(vals)
            out.write(f"Variant: {v} --> {metrics}\n")

        baseline = "eaodehybrid"
        if baseline in all_results:
            for v, vals in all_results.items():
                if v == baseline:
                    continue
                try:
                    stat, p = wilcoxon_test(all_results[baseline], vals)
                except Exception as e:
                    stat, p = (None, None)
                out.write(f"Wilcoxon {baseline} vs {v}: stat={stat}, p={p}\n")

    print(f"Experiments finished. Summary written to {summary_path}")


if __name__ == "__main__":
    run_experiments()
