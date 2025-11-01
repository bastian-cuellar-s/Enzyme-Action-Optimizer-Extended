import pandas as pd

df = pd.read_csv('results/summary_by_function.csv')
pivot = df.pivot_table(index='function', columns='variant', values='mean')
functions = sorted(pivot.index.tolist())
eaodehybrid_worse = []
eaodehybrid_better = []
equal = []
for f in functions:
    a = pivot.loc[f].get('eaodehybrid')
    b = pivot.loc[f].get('eao')
    if pd.isna(a) or pd.isna(b):
        continue
    if a > b:
        eaodehybrid_worse.append((f, float(a), float(b)))
    elif a < b:
        eaodehybrid_better.append((f, float(a), float(b)))
    else:
        equal.append((f, float(a), float(b)))

print('eaodehybrid worse than eao for functions:')
for item in eaodehybrid_worse:
    print(item)
print('\neaodehybrid better than eao for functions:')
for item in eaodehybrid_better:
    print(item)
print('\nequal:')
for item in equal:
    print(item)
