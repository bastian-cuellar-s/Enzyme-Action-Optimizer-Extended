# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 18:20:58 2025

@author: aliro
"""

import numpy as np
from metaheuristics.eao import EAO
from get_f import Get_F
import shutil, os

def main():
    # Limpiar carpeta de resultados al inicio
    import shutil, os

    resultados_path = 'resultados'
    datos_path = os.path.join(resultados_path, 'datos')
    graficos_path = os.path.join(resultados_path, 'graficos')
    # Eliminar y recrear carpetas
    for folder in [resultados_path, datos_path, graficos_path]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)
    # Selección de variante y función objetivo
    from eao_variants import get_variant_func, VARIANT_FUNCTIONS
    EnzymeCount = int(input("Cantidad de enzimas (EnzymeCount): ") or "50")
    MaxIter = int(input("Iteraciones máximas (MaxIter): ") or "500")
    # Listar funciones disponibles automáticamente
    from get_f import Get_F
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
    print("Funciones disponibles:")
    for detail in func_details:
        print(detail)
    f_name = input("Nombre de la función objetivo (por ejemplo, F23 o 'all'): ") or "F23"
    # Normalizar nombre de función (mayúsculas)
    if f_name.lower() not in ['all', 'todas']:
        if f_name[0].lower() == 'f' and f_name[1:].isdigit():
            f_name = f_name[0].upper() + f_name[1:]
    print("Variantes disponibles:")
    print("(Puedes copiar y pegar el nombre exacto)")
    for v in VARIANT_FUNCTIONS:
        print(f"- {v}")
    print("- todas (o 'all')")
    variant = input("Selecciona variante (o 'todas'/'all' para probar todas): ") or list(VARIANT_FUNCTIONS.keys())[0]

    import matplotlib.pyplot as plt

    # Obtener lista de funciones
    from get_f import Get_F
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
            print(f"ERROR: Variante '{variant}' no existe. Opciones válidas: {list(VARIANT_FUNCTIONS.keys())} o 'todas'/'all'")
            return
        variants_to_run = [variant]

    # Ejecutar todas las combinaciones
    all_best_results = []
    for func in funcs_to_run:
        print(f"\n{'='*20} EJECUTANDO FUNCIÓN: {func} {'='*20}")
        try:
            lb, ub, dim, fobj = Get_F(func)
            lb = np.array(lb, dtype=float)
            ub = np.array(ub, dtype=float)
        except Exception as e:
            print(f"ERROR: La función objetivo '{func}' no existe o no se pudo cargar. Detalle: {e}")
            continue
        plt.figure(figsize=(10, 6))
        func_best_val = None
        func_best_variant = None
        func_best_substrate = None
        for v in variants_to_run:
            print(f"--- Probando variante: {v} ---")
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
            plt.savefig(f'{graficos_path}/convergencia_{v}_{func}.png', dpi=300)
            datos_file = f'{datos_path}/resultado_{v}_{func}.csv'
            with open(datos_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Iteracion", "MejorValor"])
                for idx, val in enumerate(conv_curve):
                    writer.writerow([idx+1, val])
                writer.writerow([])
                writer.writerow(["MejorValorFinal", OptimalCatalysis])
                writer.writerow(["MejorSubstratoFinal"] + list(BestSubstrate))
            if func_best_val is None or OptimalCatalysis < func_best_val:
                func_best_val = OptimalCatalysis
                func_best_variant = v
                func_best_substrate = BestSubstrate
        if func_best_val is not None and func_best_variant is not None:
            print(f"--- MEJOR RESULTADO PARA {func} ---")
            print(f"Variante: {func_best_variant}")
            print(f"Mejor valor: {func_best_val}")
            print(f"Mejor substrato: {func_best_substrate}")
            plt.xlabel('Iteración')
            plt.ylabel('Mejor valor encontrado')
            plt.title(f'Curva de Convergencia Comparativa ({func})')
            plt.legend()
            plt.grid(True)
            comparative_plot_path = f'{graficos_path}/convergencia_comparativa_{func}.png'
            plt.savefig(comparative_plot_path, dpi=300)
            plt.close()
            print(f"Gráfico comparativo para '{func}' guardado en: {comparative_plot_path}")
            all_best_results.append({
                "funcion": func,
                "variante": func_best_variant,
                "valor": func_best_val,
                "substrato": func_best_substrate
            })
    print(f"\n\n{'='*25} RESUMEN DE MEJORES RESULTADOS {'='*25}")
    print(f"{'Función':<10} | {'Mejor Variante':<20} | {'Mejor Valor':<25}")
    print(f"{'-'*10} | {'-'*20} | {'-'*25}")
    if not all_best_results:
        print("No se obtuvo ningún resultado. Verifica que la función objetivo y las variantes sean correctas y que no haya errores en la ejecución.")
    else:
        for result in all_best_results:
            valor_str = '{:.10e}'.format(result['valor'])
            print(f"{result['funcion']:<10} | {result['variante']:<20} | {valor_str:<25}")
    graficos_path = os.path.join(resultados_path, 'graficos')
    import importlib.util
    import sys
    def import_from_path(module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    # Importar metricas desde la raíz
    metricas_mod = import_from_path('metricas', os.path.join(os.getcwd(), 'metricas.py'))
    graficos_mod = import_from_path('graficos', os.path.join(os.getcwd(), 'graficos.py'))
    calcular_metricas = metricas_mod.calcular_metricas
    prueba_wilcoxon = metricas_mod.prueba_wilcoxon
    curva_convergencia = graficos_mod.curva_convergencia
    boxplot_comparativo = graficos_mod.boxplot_comparativo
    # Guardar métricas y boxplot de los mejores resultados
    valores = [result['valor'] for result in all_best_results]
    metricas = calcular_metricas(valores)
    # Guardar métricas en la carpeta resultados
    with open(os.path.join(resultados_path, 'resumen_metricas.txt'), 'w') as f:
        for k, v in metricas.items():
            f.write(f"{k}: {v}\n")
    # Boxplot comparativo de variantes
    variantes = [result['variante'] for result in all_best_results]
    boxplot_comparativo([np.array([result['valor']]) for result in all_best_results], variantes, os.path.join(graficos_path, 'boxplot_mejores.png'))
    # Curva de convergencia comparativa (si hay datos)
    # (Ejemplo: usar las curvas de convergencia de las variantes de la última función)
    # Puedes adaptar esto para guardar todas las curvas si lo deseas
    print("="*75)

if __name__ == "__main__":
    main()
