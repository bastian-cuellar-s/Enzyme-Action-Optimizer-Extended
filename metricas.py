import numpy as np
from scipy.stats import wilcoxon

def calcular_metricas(resultados):
    resultados = np.array(resultados)
    media = np.mean(resultados)
    std = np.std(resultados)
    mejor = np.min(resultados)
    peor = np.max(resultados)
    return {
        'media': media,
        'std': std,
        'mejor': mejor,
        'peor': peor
    }

def prueba_wilcoxon(lista1, lista2):
    stat, p = wilcoxon(lista1, lista2)
    return stat, p

if __name__ == "__main__":
    # Ejemplo de uso
    resultados1 = np.random.rand(30)
    resultados2 = np.random.rand(30)
    print("Métricas lista 1:", calcular_metricas(resultados1))
    print("Métricas lista 2:", calcular_metricas(resultados2))
    stat, p = prueba_wilcoxon(resultados1, resultados2)
    print(f"Wilcoxon: stat={stat}, p={p}")
