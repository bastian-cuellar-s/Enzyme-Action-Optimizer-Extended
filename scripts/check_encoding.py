fn = 'results/data/result_de_F1.csv'
bs = open(fn, 'rb').read(200)
print('raw bytes start:', bs[:60])
for enc in ['utf-8', 'utf-8-sig', 'utf-16', 'utf-16-le', 'utf-16-be', 'latin1']:
    try:
        s = bs.decode(enc)
        print('decoding with', enc, '->', repr(s.splitlines()[0]))
    except Exception as e:
        print('decoding', enc, 'failed:', e)
