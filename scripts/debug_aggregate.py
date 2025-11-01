import sys
sys.path.append('.')
from scripts import aggregate_results as agg

files = agg.find_result_files()
print('FOUND files:', len(files))
for i, f in enumerate(files[:30]):
    print('---')
    print(i, f)
    variant, func, run = agg.parse_filename(f)
    print(' parsed:', variant, func, run)
    val, df = agg.extract_last_value(f)
    print(' extracted val:', val)
    if df is None:
        print(' df is None')
    else:
        print(' df.shape:', df.shape)
        print(' columns:', df.columns.tolist())
        print(' head:')
        print(df.head(3).to_string())

print('\nGrouping sample:')
from collections import defaultdict
groups = defaultdict(int)
for f in files:
    variant, func, run = agg.parse_filename(f)
    if variant is None:
        groups['__unknown__'] += 1
    else:
        groups[(func, variant)] += 1

keys = list(groups.items())[:20]
for k, v in keys:
    print(k, v)

print('Total groups:', len(groups))
