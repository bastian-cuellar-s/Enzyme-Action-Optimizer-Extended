#!/usr/bin/env python3
"""
Aggregate per-run result CSVs in `results/data/` into a consolidated summary and produce plots.

Creates:
 - results/summary_by_function.csv
 - results/summary_wilcoxon.csv
 - results/plots/boxplot_F{n}.png
 - results/plots/agg_convergence_F{n}.png  (when per-iteration data available)

This script is defensive: it tolerates mixed filename patterns produced by the experiment scripts.
"""
import os
import re
import json
from collections import defaultdict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


DATA_DIR = os.path.join('results', 'data')
PLOTS_DIR = os.path.join('results', 'plots')
os.makedirs(PLOTS_DIR, exist_ok=True)


def find_result_files():
    files = []
    if not os.path.isdir(DATA_DIR):
        print(f"No data directory found at {DATA_DIR}")
        return files
    for fn in os.listdir(DATA_DIR):
        if fn.lower().endswith('.csv') and fn.startswith('result_'):
            files.append(os.path.join(DATA_DIR, fn))
    return files


RE = re.compile(r"result_([^_]+)_F(\d+)(?:_run(\d+))?\.csv", re.IGNORECASE)


def parse_filename(fn):
    base = os.path.basename(fn)
    m = RE.match(base)
    if not m:
        return None, None, None
    variant, func, run = m.group(1), int(m.group(2)), m.group(3)
    run = int(run) if run is not None else None
    return variant, func, run


def extract_last_value(csv_path):
    # Robust fallback: parse file lines and extract the last numeric token per line.
    # Many of the produced CSVs contain extra comma-separated data in some rows
    # (e.g. substrate vectors), so pandas.read_csv can fail due to inconsistent
    # field counts. We'll attempt line-based parsing first.
    try:
        with open(csv_path, 'r', encoding='utf-8', errors='replace') as fh:
            lines = [ln.strip() for ln in fh if ln.strip()]
    except Exception as e:
        print(f"Failed to open {csv_path}: {e}")
        return None, None

    vals = []
    float_re = re.compile(r'[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?')
    for i, ln in enumerate(lines):
        # skip header-like lines that contain letters
        if i == 0 and re.search('[A-Za-z]', ln):
            continue
        parts = ln.split(',')
        last = parts[-1].strip()
        try:
            v = float(last)
            vals.append(v)
            continue
        except Exception:
            # try to find a float anywhere in the line
            m = float_re.search(ln)
            if m:
                try:
                    vals.append(float(m.group(0)))
                    continue
                except Exception:
                    pass
            # otherwise skip this line
            continue

    if vals:
        ser = pd.Series(vals)
        df = pd.DataFrame({'best': ser})
        return float(ser.iloc[-1]), df

    # Last resort: try pandas with permissive options
    try:
        df = pd.read_csv(csv_path, engine='python', on_bad_lines='skip')
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols and df.shape[0] > 0:
            last_col = num_cols[-1]
            return float(df.iloc[-1][last_col]), df
    except Exception:
        pass

    return None, None


def aggregate():
    files = find_result_files()
    groups = defaultdict(list)  # key: (func, variant) -> list of file paths

    for f in files:
        variant, func, run = parse_filename(f)
        if variant is None:
            # skip unknown patterns
            continue
        groups[(func, variant)].append(f)

    # collect per-run values and optionally per-iteration series
    per_fn_variant_values = defaultdict(list)
    per_fn_variant_series = defaultdict(list)  # for convergence curves

    for (func, variant), fpaths in groups.items():
        for p in sorted(fpaths):
            val, df = extract_last_value(p)
            if val is None:
                continue
            per_fn_variant_values[(func, variant)].append(val)
            # if df contains an 'iter' or index-like and a 'best' column, keep series
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            series_col = None
            if 'best' in num_cols:
                series_col = 'best'
            elif 'fitness' in num_cols:
                series_col = 'fitness'
            elif len(num_cols) >= 2:
                # assume second numeric column is the objective trace (common patterns)
                series_col = num_cols[-1]

            if series_col is not None and df.shape[0] > 1:
                # store as (run_indexed_series)
                s = pd.Series(df[series_col].values)
                per_fn_variant_series[(func, variant)].append(s)

    # Build summary table
    rows = []
    by_function = defaultdict(dict)
    for (func, variant), vals in per_fn_variant_values.items():
        arr = np.array(vals)
        row = {
            'function': int(func),
            'variant': variant,
            'n_runs': int(len(arr)),
            'mean': float(np.mean(arr)),
            'std': float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
            'median': float(np.median(arr)),
            'best': float(np.min(arr)),
            'worst': float(np.max(arr)),
        }
        rows.append(row)
        by_function[int(func)][variant] = arr

    if not rows:
        print("No result rows collected. Make sure `results/data` contains CSVs named like result_<variant>_F<NUMBER>[_runN].csv")
        return
    summary_df = pd.DataFrame(rows)
    summary_df = summary_df.sort_values(['function', 'mean'])
    # write summary next to the DATA_DIR parent (so per-output-dir aggregation is possible)
    base_dir = os.path.dirname(DATA_DIR)
    out_csv = os.path.join(base_dir, 'summary_by_function.csv')
    summary_df.to_csv(out_csv, index=False)
    print(f"Wrote summary to {out_csv}")

    # Wilcoxon / Mann-Whitney comparisons vs 'eao'
    wil_rows = []
    for func, variants in sorted(by_function.items()):
        if 'eaodehybrid' in variants and 'eao' in variants:
            x = variants['eaodehybrid']
            y = variants['eao']
            test_used = 'wilcoxon'
            try:
                if len(x) == len(y) and len(x) > 0:
                    stat, p = stats.wilcoxon(x, y)
                else:
                    # unpaired: Mann-Whitney U
                    stat, p = stats.mannwhitneyu(x, y, alternative='two-sided')
                    test_used = 'mannwhitney'
            except Exception as e:
                stat, p = np.nan, np.nan
                test_used = f'error:{e}'
            better = 'eaodehybrid' if np.nanmean(x) < np.nanmean(y) else 'eao'
            wil_rows.append({'function': int(func), 'test': test_used, 'stat': float(stat) if not np.isnan(stat) else None, 'p_value': float(p) if not np.isnan(p) else None, 'better': better})

    wil_df = pd.DataFrame(wil_rows)
    wil_out = os.path.join(base_dir, 'summary_wilcoxon.csv')
    if not wil_df.empty:
        wil_df.to_csv(wil_out, index=False)
        print(f"Wrote wilcoxon/mannwhitney summary to {wil_out}")
    else:
        print("No paired eaodehybrid vs eao results found for Wilcoxon/Mann-Whitney tests.")

    # Produce boxplots per function
    for func in sorted({k[0] for k in per_fn_variant_values.keys()}):
        data_rows = []
        for (f, variant), vals in per_fn_variant_values.items():
            if f != func:
                continue
            for v in vals:
                data_rows.append({'variant': variant, 'value': v})
        if not data_rows:
            continue
        df_box = pd.DataFrame(data_rows)
        plt.figure(figsize=(8, 5))
        sns.boxplot(x='variant', y='value', data=df_box)
        plt.title(f'Function F{func} — final values by variant')
        plt.xticks(rotation=45)
        plt.tight_layout()
        out_fig = os.path.join(PLOTS_DIR, f'boxplot_F{func}.png')
        plt.savefig(out_fig)
        plt.close()
        print(f"Saved boxplot for F{func} -> {out_fig}")

        # aggregated convergence plot if series are available
        # compute mean curve per variant
        curves = {}
        for (f, variant), series_list in per_fn_variant_series.items():
            if f != func or not series_list:
                continue
            # align by index: pad shorter series with nan and take mean across runs
            maxlen = max(len(s) for s in series_list)
            arr = np.vstack([np.pad(s.values, (0, maxlen - len(s)), constant_values=np.nan) for s in series_list])
            mean_curve = np.nanmean(arr, axis=0)
            curves[variant] = mean_curve

        if curves:
            plt.figure(figsize=(8, 5))
            for variant, curve in curves.items():
                plt.plot(curve, label=variant)
            plt.xlabel('Iteration')
            plt.ylabel('Mean best-so-far')
            plt.title(f'F{func} — aggregated convergence')
            plt.legend()
            plt.tight_layout()
            outc = os.path.join(PLOTS_DIR, f'agg_convergence_F{func}.png')
            plt.savefig(outc)
            plt.close()
            print(f"Saved aggregated convergence for F{func} -> {outc}")

    # also write a small JSON summary
    meta = {
        'n_functions': int(summary_df['function'].nunique()) if not summary_df.empty else 0,
        'n_rows': int(len(summary_df)),
    }
    with open(os.path.join('results', 'summary_meta.json'), 'w') as fh:
        json.dump(meta, fh, indent=2)
    print('Aggregation complete.')


if __name__ == '__main__':
    aggregate()
