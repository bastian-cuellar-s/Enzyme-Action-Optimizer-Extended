
import importlib
import numpy as np

# Diccionario que mapea nombres de variantes a sus funciones de iteración
VARIANT_FUNCTIONS = {
    'eao': ('metaheuristics.eao', 'EAO'),
    'de': ('metaheuristics.DE', 'iterar_DE'),
    'eaodehybrid': ('metaheuristics.EAODEHybrid', 'iterarEAO_DE_Hybrid'),
    'eaoecdynamic': ('metaheuristics.EAOECDynamic', 'iterarEAO_EC_Dynamic'),
    'eaolfexploration': ('metaheuristics.EAOLFExploration', 'iterarEAO_LF_Exploration'),
    'eaolfperturbation': ('metaheuristics.EAOLFPerturbation', 'iterarEAO_LF_Perturbation'),
    'eaoprobabilistic': ('metaheuristics.EAOProbabilistic', 'iterarEAO_Probabilistic'),
    'fda': ('metaheuristics.FDA', 'iterar_FDA'),
    'gmo': ('metaheuristics.GMO', 'iterar_GMO'),
    'gto': ('metaheuristics.GTO', 'iterar_GTO'),
    'gwo': ('metaheuristics.GWO', 'iterar_GWO'),
    'hgso': ('metaheuristics.HGSO', 'iterar_HGSO'),
    'hloa': ('metaheuristics.HLOA', 'iterar_HLOA'),
    'mfo': ('metaheuristics.MFO', 'iterar_MFO'),
    'mvo': ('metaheuristics.MVO', 'iterar_MVO'),
    'pso': ('metaheuristics.PSO', 'iterar_PSO'),
    'sca': ('metaheuristics.SCA', 'iterar_SCA'),
    'sho': ('metaheuristics.SHO', 'iterar_SHO'),
    'woa': ('metaheuristics.WOA', 'iterar_WOA'),
    'wso': ('metaheuristics.WSO', 'iterar_WSO'),
}

def _eao_wrapper(MaxIter, iter, dim, population, fitness, best, lb, ub):
    # Adaptar los argumentos al formato de EAO
    from metaheuristics.eao import EAO
    # population: matriz inicial, fitness: vector inicial, best: mejor solución inicial
    # lb, ub: límites
    # dim: dimensión
    # MaxIter: número de iteraciones
    # iter: ignorado (EAO ejecuta todo de una vez)
    # Definir una función de evaluación temporal (usando la población actual)
    def fobj(x):
        # Se asume que la función objetivo está definida en el contexto de main.py
        # Aquí solo se usa para compatibilidad
        return np.sum(x**2)
    EnzymeCount = population.shape[0]
    OptimalCatalysis, BestSubstrate, conv_curve = EAO(EnzymeCount, MaxIter, lb, ub, dim, fobj)
    # Simular la interfaz: devolver la población y fitness final
    # (No se usa en la convergencia real, pero permite compatibilidad)
    new_population = population.copy()
    new_fitness = np.array([fobj(new_population[i, :]) for i in range(EnzymeCount)])
    return new_population, new_fitness

def get_variant_func(variant_name):
    if variant_name not in VARIANT_FUNCTIONS:
        raise ValueError(f"Variante '{variant_name}' no soportada.")
    if variant_name == 'eao':
        return _eao_wrapper
    module_name, func_name = VARIANT_FUNCTIONS[variant_name]
    module = importlib.import_module(f"{module_name}")
    return getattr(module, func_name)
