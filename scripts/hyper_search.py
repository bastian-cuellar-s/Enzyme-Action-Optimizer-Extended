import os
import sys

# Ensure repo root on path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.run_experiments import run_experiments


def run_grid(enzyme_counts=(20, 50), max_iters=(200, 500), reps=30, func_name="F1", n_jobs=None):
    RESULTS_DIR = os.path.join(ROOT, "results")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    summary_lines = []
    for EnzymeCount in enzyme_counts:
        for MaxIter in max_iters:
            print(f"Running grid EnzymeCount={EnzymeCount}, MaxIter={MaxIter}, reps={reps}")
            # Choose number of jobs: default to cpu_count-1 if not provided
            if n_jobs is None:
                nj = max(1, os.cpu_count() - 1)
            else:
                nj = n_jobs
            # Call run_experiments for this config but only with variants 'eaodehybrid' and 'eao'
            run_experiments(
                func_name,
                variants=["eaodehybrid", "eao"],
                reps=reps,
                EnzymeCount=EnzymeCount,
                MaxIter=MaxIter,
                n_jobs=nj,
            )
            summary_lines.append(f"Completed EnzymeCount={EnzymeCount}, MaxIter={MaxIter}")

    # Save a tiny summary file
    with open(os.path.join(RESULTS_DIR, "hyper_search_summary.txt"), "w") as f:
        for l in summary_lines:
            f.write(l + "\n")
    print("Grid search finished. Summary saved to results/hyper_search_summary.txt")


if __name__ == "__main__":
    run_grid()
