import os
import glob
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Ensure repo root is on path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.plots import comparative_boxplot


def main(func_name="F1"):
    DATA_DIR = os.path.join(ROOT, "results", "data")
    OUT_DIR = os.path.join(ROOT, "results", "plots")
    os.makedirs(OUT_DIR, exist_ok=True)

    files = glob.glob(os.path.join(DATA_DIR, f"result_*_{func_name}_run*.csv"))
    if not files:
        print("No CSV files found for function", func_name)
        return

    by_variant = {}
    for f in files:
        name = os.path.basename(f)
        parts = name.split("_")
        # result_{variant}_{func}_run{n}.csv
        if len(parts) < 4:
            continue
        variant = parts[1]
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        if "BestValue" in df.columns:
            last = df["BestValue"].values[-1]
        else:
            # fallback: last numeric in file
            last = df.values[-1, -1]
        by_variant.setdefault(variant, []).append(float(last))

    variants = sorted(by_variant.keys())
    arrays = [np.array(by_variant[v]) for v in variants]
    boxpath = os.path.join(OUT_DIR, f"boxplot_{func_name}.png")
    comparative_boxplot(arrays, variants, boxpath)
    print("Saved boxplot to", boxpath)

    # Aggregated convergence curves (mean across runs)
    plt.figure(figsize=(10, 6))
    for v in variants:
        conv_files = sorted(glob.glob(os.path.join(DATA_DIR, f"result_{v}_{func_name}_run*.csv")))
        curves = []
        for cf in conv_files:
            try:
                df = pd.read_csv(cf)
            except Exception:
                continue
            if "BestValue" in df.columns:
                curves.append(df["BestValue"].values)
        if not curves:
            continue
        arr = np.vstack(curves)
        mean_curve = np.mean(arr, axis=0)
        plt.plot(mean_curve, label=v)

    plt.legend()
    plt.xlabel("Iteration")
    plt.ylabel("Mean Best Value")
    plt.title(f"Aggregated Convergence {func_name}")
    plt.grid(True)
    aggpath = os.path.join(OUT_DIR, f"agg_convergence_{func_name}.png")
    plt.savefig(aggpath, dpi=300)
    plt.close()
    print("Saved aggregated convergence to", aggpath)


if __name__ == "__main__":
    main()
