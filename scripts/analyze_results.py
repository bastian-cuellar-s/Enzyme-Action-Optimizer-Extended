import os
import sys
import glob
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon


def analyze(func_name="F8"):
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DATA_DIR = os.path.join(ROOT, "results", "data")
    pattern = os.path.join(DATA_DIR, f"result_*_{func_name}_run*.csv")
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No result files found for {func_name} (pattern: {pattern})")
        return 1

    by_variant = {}
    for f in files:
        name = os.path.basename(f)
        parts = name.split("_")
        if len(parts) < 4:
            continue
        variant = parts[1]
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        txt = open(f).read()
        if "BestFinalValue" in txt:
            last_line = None
            for line in txt.strip().splitlines()[::-1]:
                if line.startswith("BestFinalValue"):
                    last_line = line
                    break
            if last_line:
                try:
                    val = float(last_line.split(",")[1])
                except Exception:
                    val = float(last_line.split(":")[-1])
            else:
                # fallback
                if "BestValue" in df.columns:
                    val = float(df["BestValue"].values[-1])
                else:
                    val = float(df.values[-1, -1])
        else:
            if "BestValue" in df.columns:
                val = float(df["BestValue"].values[-1])
            else:
                val = float(df.values[-1, -1])
        by_variant.setdefault(variant, []).append(val)

    print(f"Results summary for {func_name}:")
    for k in sorted(by_variant.keys()):
        arr = np.array(by_variant[k])
        print(f"- {k}: n={len(arr)}, mean={arr.mean():.6e}, std={arr.std():.6e}, min={arr.min():.6e}, max={arr.max():.6e}")

    if "eaodehybrid" in by_variant and "eao" in by_variant:
        a = np.array(by_variant["eaodehybrid"])
        b = np.array(by_variant["eao"])
        m = min(len(a), len(b))
        a_tr = a[:m]
        b_tr = b[:m]
        try:
            stat, p = wilcoxon(a_tr, b_tr)
        except Exception:
            stat, p = None, None
        print(f"\nComparison eaodehybrid vs eao (first {m} runs each):")
        print(f"  eaodehybrid mean,std = {a_tr.mean():.6e}, {a_tr.std():.6e}")
        print(f"  eao         mean,std = {b_tr.mean():.6e}, {b_tr.std():.6e}")
        print(f"  Wilcoxon: stat={stat}, p={p}")
    else:
        print("Not enough data to compare eaodehybrid vs eao for this function.")


if __name__ == "__main__":
    func = sys.argv[1] if len(sys.argv) > 1 else "F8"
    sys.exit(analyze(func))
