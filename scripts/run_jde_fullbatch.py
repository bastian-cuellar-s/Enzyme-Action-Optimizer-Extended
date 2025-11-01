"""Run jDE hyper experiments (A: best-config high-rep; B: random search) across multiple functions.

Usage examples (PowerShell):

# default run (functions 1,4,5,6,12,14,15,18)
python scripts/run_jde_fullbatch.py

# custom functions and parallelism
python scripts/run_jde_fullbatch.py --functions 1 2 3 --reps-best 30 --configs-per-func 5 --reps-rand 10 --n-jobs 6

The script saves per-config outputs under results/<outdir>/ and aggregates after each run.
"""
import argparse
import time
import os
import numpy as np
import utils.jde_config as jde_conf
from scripts.run_experiments import run_experiments
import scripts.aggregate_results as agg

DEFAULT_FUNCTIONS = [1, 4, 5, 6, 12, 14, 15, 18]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--functions', nargs='+', type=int, default=DEFAULT_FUNCTIONS,
                   help='List of function numbers to run (e.g. 1 4 5)')
    p.add_argument('--reps-best', type=int, default=30, help='Reps for best-config runs')
    p.add_argument('--configs-per-func', type=int, default=5, help='Number of random configs per function')
    p.add_argument('--reps-rand', type=int, default=10, help='Reps for random search configs')
    p.add_argument('--enzymecount', type=int, default=30)
    p.add_argument('--maxiter', type=int, default=200)
    p.add_argument('--n-jobs', type=int, default=6)
    p.add_argument('--seed', type=int, default=12345)
    p.add_argument('--out-prefix', type=str, default='jde', help='Prefix for result folders')
    p.add_argument('--only-rand', action='store_true', help='Run only Part B (random search) and skip Part A (best-config)')
    return p.parse_args()


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def aggregate_folder(outdir):
    data_dir = os.path.join('results', outdir, 'data')
    plots_dir = os.path.join('results', outdir, 'plots')
    agg.DATA_DIR = data_dir
    agg.PLOTS_DIR = plots_dir
    ensure_dir(plots_dir)
    try:
        agg.aggregate()
    except Exception as e:
        print(f"Aggregation failed for {outdir}: {e}")


def main():
    args = parse_args()
    rng = np.random.RandomState(args.seed)

    functions = args.functions
    best_cfg = {'tau_F': 0.2, 'tau_CR': 0.1, 'F_low': 0.1, 'F_up': 0.9}

    completed = []
    start_all = time.time()

    # Part A: best-config high-rep
    if not args.only_rand:
        for f in functions:
            jde_conf.JDE_PARAMS.update(best_cfg)
            outdir = f"{args.out_prefix}_bestcfg_F{f}"
            print(f"\n--- Running best config for F{f} -> {outdir} (reps={args.reps_best}) ---")
            t0 = time.time()
            run_experiments(func_name=f'F{f}', variants=['eaodehybrid', 'eao'], reps=args.reps_best,
                            EnzymeCount=args.enzymecount, MaxIter=args.maxiter, n_jobs=args.n_jobs, output_dir=outdir)
            dt = time.time() - t0
            print(f"Completed F{f} in {dt:.1f}s")
            aggregate_folder(outdir)
            completed.append(('best', f, outdir, dt))
    else:
        print("Skipping Part A (best-config) because --only-rand was specified.")

    # Part B: random search per function
    for f in functions:
        for cfg_idx in range(args.configs_per_func):
            tau_F = float(rng.uniform(0.01, 0.3))
            tau_CR = float(rng.uniform(0.01, 0.3))
            F_low = float(rng.uniform(0.05, 0.3))
            F_up = float(rng.uniform(0.7, 0.95))
            if F_low >= F_up:
                F_low, F_up = 0.1, 0.9
            jde_conf.JDE_PARAMS.update({'tau_F': tau_F, 'tau_CR': tau_CR, 'F_low': F_low, 'F_up': F_up})
            outdir = f"{args.out_prefix}_randsearch_F{f}_cfg{cfg_idx+1}"
            print(f"\n--- Running random cfg {cfg_idx+1}/{args.configs_per_func} for F{f} -> {outdir} (reps={args.reps_rand}) ---")
            t0 = time.time()
            run_experiments(func_name=f'F{f}', variants=['eaodehybrid', 'eao'], reps=args.reps_rand,
                            EnzymeCount=args.enzymecount, MaxIter=args.maxiter, n_jobs=args.n_jobs, output_dir=outdir)
            dt = time.time() - t0
            print(f"Completed rand cfg {cfg_idx+1} for F{f} in {dt:.1f}s")
            aggregate_folder(outdir)
            completed.append(('rand', f, outdir, dt))

    total = time.time() - start_all
    print('All experiments done in', total)
    ensure_dir('results')
    with open('results/jde_full_run_summary.txt', 'w') as fh:
        fh.write('type,func,outdir,seconds\n')
        for c in completed:
            fh.write(f"{c[0]},{c[1]},{c[2]},{c[3]:.1f}\n")
    print('Summary written to results/jde_full_run_summary.txt')


if __name__ == '__main__':
    main()
