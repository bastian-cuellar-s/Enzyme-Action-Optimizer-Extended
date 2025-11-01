import importlib
mods=['metaheuristics.EAODEHybrid','metaheuristics.EAOECDynamic','metaheuristics.EAOLFExploration','metaheuristics.EAOLFPerturbation','metaheuristics.EAOProbabilistic']
for m in mods:
    try:
        importlib.import_module(m)
        print(m+' OK')
    except Exception as e:
        print(m+' ERROR', e)
