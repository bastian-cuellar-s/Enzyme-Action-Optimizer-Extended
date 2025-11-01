"""
Aggregate per-run results under results/expand_smoke_all into a CSV and a human-readable summary.
Writes:
 - results/expand_smoke_all_summary.csv
 - results/expand_smoke_all/experiments_summary.txt

Usage: python scripts/aggregate_expand_smoke_all.py
"""
import os
import numpy as np

ROOT = os.path.join('results', 'expand_smoke_all')
OUT_CSV = os.path.join('results', 'expand_smoke_all_summary.csv')
OUT_SUMMARY = os.path.join('results', 'expand_smoke_all', 'experiments_summary.txt')

if not os.path.isdir(ROOT):
    raise SystemExit(f"No directory {ROOT}")

rows = []
functions = sorted([d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d))])
for func in functions:
    data_dir = os.path.join(ROOT, func, 'data')
    if not os.path.isdir(data_dir):
        continue
    files = [f for f in os.listdir(data_dir) if f.startswith('result_') and f.endswith('.csv')]
    per_variant = {}
    for fn in files:
        parts = fn.split('_')
        # expect result_<variant>_<func>_runN.csv
        if len(parts) < 4:
            continue
        variant = parts[1]
        path = os.path.join(data_dir, fn)
        final_val = None
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                lines = [ln.strip() for ln in fh if ln.strip()]
            # find BestFinalValue line
            for ln in reversed(lines):
                if ln.startswith('BestFinalValue'):
                    if ',' in ln:
                        final_val = float(ln.split(',', 1)[1])
                    else:
                        try:
                            final_val = float(ln.split()[-1])
                        except Exception:
                            final_val = None
                    break
            if final_val is None:
                # fallback: last numeric in Iteration,BestValue
                for ln in reversed(lines):
                    if ',' in ln and ln.split(',')[0].strip().isdigit():
                        try:
                            final_val = float(ln.split(',')[1])
                        except Exception:
                            final_val = None
                        break
        except Exception as e:
            print('ERROR reading', path, e)
            continue
        if final_val is None:
            continue
        per_variant.setdefault(variant, []).append(final_val)
    for variant, vals in per_variant.items():
        cnt = len(vals)
        m = float(np.mean(vals)) if cnt > 0 else float('nan')
        med = float(np.median(vals)) if cnt > 0 else float('nan')
        sd = float(np.std(vals, ddof=1)) if cnt > 1 else 0.0
        rows.append((func, variant, cnt, m, med, sd))

# write CSV
os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
with open(OUT_CSV, 'w', encoding='utf-8') as fh:
    fh.write('Function,Variant,Count,Mean,Median,Std\n')
    for r in sorted(rows):
        fh.write(f"{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]}\n")

# write textual summary with winner per function (lowest mean)
by_func = {}
for func, variant, cnt, m, med, sd in rows:
    by_func.setdefault(func, []).append((variant, cnt, m, med, sd))

os.makedirs(os.path.dirname(OUT_SUMMARY), exist_ok=True)
with open(OUT_SUMMARY, 'w', encoding='utf-8') as fh:
    for func in sorted(by_func.keys()):
        fh.write(f'Function {func}\n')
        rows_f = sorted(by_func[func], key=lambda x: x[2])
        for v in rows_f:
            fh.write(f'  {v[0]}: count={v[1]} mean={v[2]:.6g} median={v[3]:.6g} std={v[4]:.6g}\n')
        winner = rows_f[0]
        fh.write(f'  >> Winner by mean: {winner[0]} (mean={winner[2]:.6g})\n\n')

print('Wrote', OUT_CSV, 'and', OUT_SUMMARY)
