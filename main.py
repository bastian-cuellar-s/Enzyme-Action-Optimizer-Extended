# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 18:20:58 2025

@author: aliro
"""

import numpy as np
from metaheuristics.eao import EAO
from utils.get_f import Get_F
import shutil, os

def main():
    # Limpiar carpeta de resultados al inicio
    import shutil, os

    resultados_path = 'results'
    datos_path = os.path.join(resultados_path, 'data')
    graficos_path = os.path.join(resultados_path, 'plots')
    # Eliminar y recrear carpetas
    for folder in [resultados_path, datos_path, graficos_path]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)
    # Variant and objective function selection
    from utils.eao_variants import get_variant_func, VARIANT_FUNCTIONS
    EnzymeCount = int(input("Number of enzymes (EnzymeCount): ") or "50")
    MaxIter = int(input("Max iterations (MaxIter): ") or "500")
    # Listar funciones disponibles automáticamente
    from utils.get_f import Get_F
    available_funcs = []
    func_details = []
    for i in range(1, 24):
        try:
            lb, ub, dim, _ = Get_F(f"F{i}")
            lb, ub, dim, _ = Get_F(f"F{i}") # No se necesita fobj aquí
            available_funcs.append(f"F{i}")
            func_details.append(f"{f'F{i}':<4} | lb: {lb} | ub: {ub} | dim: {dim}")
        except:
            pass
    print("Available functions:")
    for detail in func_details:
        print(detail)
    f_name = input("Objective function name (e.g. F23 or 'all'): ") or "F23"
    # Normalizar nombre de función (mayúsculas)
    if f_name.lower() not in ['all', 'todas']:
        if f_name[0].lower() == 'f' and f_name[1:].isdigit():
            f_name = f_name[0].upper() + f_name[1:]
    print("Available variants:")
    print("(You can copy/paste the exact name)")
    for v in VARIANT_FUNCTIONS:
        print(f"- {v}")
    print("- all")
    variant = input("Select variant (or 'all' to run all): ") or list(VARIANT_FUNCTIONS.keys())[0]

    import matplotlib.pyplot as plt

    # Obtener lista de funciones
    # Get_F imported from utils at top
    available_funcs = []
    for i in range(1, 24):
        try:
            lb, ub, dim, fobj = Get_F(f"F{i}")
            available_funcs.append(f"F{i}")
        except:
            pass

    # Determinar funciones y variantes a ejecutar
    if f_name.lower() in ['all', 'todas']:
        funcs_to_run = available_funcs
    else:
        funcs_to_run = [f_name]

    if variant.lower() in ['all', 'todas']:
        variants_to_run = list(VARIANT_FUNCTIONS.keys())
    else:
        if variant not in VARIANT_FUNCTIONS:
            print(f"ERROR: Variant '{variant}' does not exist. Valid options: {list(VARIANT_FUNCTIONS.keys())} or 'all'")
            return
        variants_to_run = [variant]

    # Ejecutar todas las combinaciones
    all_best_results = []
    for func in funcs_to_run:
        print(f"\n{'='*20} RUNNING FUNCTION: {func} {'='*20}")
        try:
            lb, ub, dim, fobj = Get_F(func)
            lb = np.array(lb, dtype=float)
            ub = np.array(ub, dtype=float)
        except Exception as e:
            print(f"ERROR: Objective function '{func}' cannot be loaded. Details: {e}")
            continue
        plt.figure(figsize=(10, 6))
        func_best_val = None
        func_best_variant = None
        func_best_substrate = None
        for v in variants_to_run:
            print(f"--- Testing variant: {v} ---")
            population = lb + (ub - lb) * np.random.rand(EnzymeCount, dim)
            fitness = np.array([fobj(population[i, :]) for i in range(EnzymeCount)])
            best_idx = np.argmin(fitness)
            best = population[best_idx, :].copy()
            variant_func = get_variant_func(v)
            import csv
            if v == 'eao':
                # Ejecutar EAO solo una vez, obtener curva de convergencia real
                from metaheuristics.eao import EAO
                OptimalCatalysis, BestSubstrate, conv_curve = EAO(EnzymeCount, MaxIter, lb, ub, dim, fobj)
                # Actualizar población y fitness para compatibilidad
                population = lb + (ub - lb) * np.random.rand(EnzymeCount, dim)
                fitness = np.array([fobj(population[i, :]) for i in range(EnzymeCount)])
                best_idx = np.argmin(fitness)
                best = population[best_idx, :].copy()
            elif v == 'pso':
                # Inicializar velocity y pbest
                velocity = np.zeros_like(population)
                pbest = np.copy(population)
                pbest_fitness = np.copy(fitness)
                conv_curve = np.zeros(MaxIter)
                for iter in range(MaxIter):
                    population, fitness, velocity = variant_func(MaxIter, iter, dim, population, fitness, best, lb, ub, velocity, pbest)
                    # Actualizar pbest
                    improved = fitness < pbest_fitness
                    pbest[improved, :] = population[improved, :]
                    pbest_fitness[improved] = fitness[improved]
                    best_idx = np.argmin(fitness)
                    best = population[best_idx, :].copy()
                    conv_curve[iter] = fitness[best_idx]
                OptimalCatalysis = fitness[best_idx]
                BestSubstrate = best
            else:
                conv_curve = np.zeros(MaxIter)
                for iter in range(MaxIter):
                    population, fitness = variant_func(MaxIter, iter, dim, population, fitness, best, lb, ub)
                    best_idx = np.argmin(fitness)
                    best = population[best_idx, :].copy()
                    conv_curve[iter] = fitness[best_idx]
                OptimalCatalysis = fitness[best_idx]
                BestSubstrate = best
            plt.plot(conv_curve, label=f'{v}')
            plt.savefig(f'{graficos_path}/convergence_{v}_{func}.png', dpi=300)
            datos_file = f'{datos_path}/result_{v}_{func}.csv'
            with open(datos_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Iteration", "BestValue"])
                for idx, val in enumerate(conv_curve):
                    writer.writerow([idx+1, val])
                writer.writerow([])
                writer.writerow(["BestFinalValue", OptimalCatalysis])
                writer.writerow(["BestFinalSubstrate"] + list(BestSubstrate))
            if func_best_val is None or OptimalCatalysis < func_best_val:
                func_best_val = OptimalCatalysis
                func_best_variant = v
                func_best_substrate = BestSubstrate
        if func_best_val is not None and func_best_variant is not None:
            print(f"--- BEST RESULT FOR {func} ---")
            print(f"Variant: {func_best_variant}")
            print(f"Best value: {func_best_val}")
            print(f"Best substrate: {func_best_substrate}")
            plt.xlabel('Iteration')
            plt.ylabel('Best value found')
            plt.title(f'Comparative Convergence Curve ({func})')
            plt.legend()
            plt.grid(True)
            comparative_plot_path = f'{graficos_path}/convergence_comparison_{func}.png'
            plt.savefig(comparative_plot_path, dpi=300)
            plt.close()
            print(f"Comparative plot for '{func}' saved to: {comparative_plot_path}")
            all_best_results.append({
                "function": func,
                "variant": func_best_variant,
                "value": func_best_val,
                "substrate": func_best_substrate
            })
    print(f"\n\n{'='*25} SUMMARY OF BEST RESULTS {'='*25}")
    print(f"{'Function':<10} | {'Best Variant':<20} | {'Best Value':<25}")
    print(f"{'-'*10} | {'-'*20} | {'-'*25}")
    if not all_best_results:
        print("No results obtained. Check that the objective function and variants are correct and that there are no runtime errors.")
    else:
        for result in all_best_results:
            valor_str = '{:.10e}'.format(result['value'])
            print(f"{result['function']:<10} | {result['variant']:<20} | {valor_str:<25}")
    graficos_path = os.path.join(resultados_path, 'plots')
    # Importar utilidades desde el paquete utils
    from utils.metrics import calculate_metrics, wilcoxon_test
    from utils.plots import convergence_curve, comparative_boxplot
    # Save metrics and boxplot for the best results
    values = [result['value'] for result in all_best_results]
    metrics = calculate_metrics(values)
    # Save metrics in results folder
    with open(os.path.join(resultados_path, 'summary_metrics.txt'), 'w') as f:
        for k, v in metrics.items():
            f.write(f"{k}: {v}\n")
    # Boxplot comparativo de variantes
    variants = [result['variant'] for result in all_best_results]
    comparative_boxplot([np.array([result['value']]) for result in all_best_results], variants, os.path.join(graficos_path, 'boxplot_best.png'))
    # Curva de convergencia comparativa (si hay datos)
    # (Ejemplo: usar las curvas de convergencia de las variantes de la última función)
    # Puedes adaptar esto para guardar todas las curvas si lo deseas
    print("="*75)

if __name__ == "__main__":
    main()
