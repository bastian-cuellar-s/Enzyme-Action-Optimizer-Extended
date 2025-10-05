import numpy as np
from scipy.stats import wilcoxon

def calculate_metrics(results):
    results = np.array(results)
    mean = np.mean(results)
    std = np.std(results)
    best = np.min(results)
    worst = np.max(results)
    return {
        'mean': mean,
        'std': std,
        'best': best,
        'worst': worst
    }

def wilcoxon_test(list1, list2):
    stat, p = wilcoxon(list1, list2)
    return stat, p

if __name__ == "__main__":
    results1 = np.random.rand(30)
    results2 = np.random.rand(30)
    print("Metrics list 1:", calculate_metrics(results1))
    print("Metrics list 2:", calculate_metrics(results2))
    stat, p = wilcoxon_test(results1, results2)
    print(f"Wilcoxon: stat={stat}, p={p}")
