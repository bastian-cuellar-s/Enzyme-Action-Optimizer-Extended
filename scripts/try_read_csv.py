import pandas as pd

f = 'results/data/result_de_F1.csv'
print('Trying default')
try:
    df = pd.read_csv(f)
    print('cols', df.columns.tolist())
    print(df.head(3))
except Exception as e:
    print('default failed', e)

print('\nTrying sep=","')
try:
    df = pd.read_csv(f, sep=',')
    print('cols', df.columns.tolist())
    print(df.head(3))
except Exception as e:
    print('sep comma failed', e)

print('\nTrying engine=python')
try:
    df = pd.read_csv(f, engine='python')
    print('cols', df.columns.tolist())
    print(df.head(3))
except Exception as e:
    print('engine python failed', e)

print('\nTrying sep=\';\'')
try:
    df = pd.read_csv(f, sep=';')
    print('cols', df.columns.tolist())
    print(df.head(3))
except Exception as e:
    print('sep ; failed', e)
