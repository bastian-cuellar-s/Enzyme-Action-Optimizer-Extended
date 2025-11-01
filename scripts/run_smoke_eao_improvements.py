# small runner to execute a smoke test for the improved EAO variants
from scripts.run_experiments import run_experiments

if __name__ == '__main__':
    run_experiments(func_name='F1',
                    variants=['eaodehybrid','eao','eaolfexploration','eaolfperturbation','eaoprobabilistic','eaoecdynamic'],
                    reps=5,
                    EnzymeCount=30,
                    MaxIter=100,
                    n_jobs=2,
                    output_dir='smoke_eao_improvements')
