# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 18:20:58 2025

@author: aliro
"""

import numpy as np
import os
import shutil
from problems.SCP.problem import SCP


def main():
    # Limpiar carpeta de resultados al inicio

    resultados_path = "results"
    datos_path = os.path.join(resultados_path, "data")
    graficos_path = os.path.join(resultados_path, "plots")
    # Eliminar y recrear carpetas
    for folder in [resultados_path, datos_path, graficos_path]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)
    # Variant and objective function selection
    from utils.eao_variants import get_variant_func, VARIANT_FUNCTIONS

    # Validación para EnzymeCount
    default_enzyme_count = 50
    while True:
        prompt = f"Number of enzymes (EnzymeCount) [default: {default_enzyme_count}]: "
        user_input = input(prompt)

        if user_input == "":
            EnzymeCount = default_enzyme_count
            print(f"  -> Using default value: {EnzymeCount}")
            break
        elif user_input.isdigit():
            EnzymeCount = int(user_input)
            break
        else:
            print("\nERROR: Invalid input. Please enter a whole number (e.g., 50).\n")

    # Validación para MaxIter
    default_max_iter = 500
    while True:
        prompt = f"Max iterations (MaxIter) [default: {default_max_iter}]: "
        user_input = input(prompt)

        if user_input == "":
            MaxIter = default_max_iter
            print(f"  -> Using default value: {MaxIter}")
            break
        elif user_input.isdigit():
            MaxIter = int(user_input)
            break
        else:
            print("\nERROR: Invalid input. Please enter a whole number (e.g., 500).\n")

    # Selección del tipo de problema
    problem_type = None
    while not problem_type:
        print("\nSelect the problem to solve:")
        print("1. Continuous functions")
        print("2. Set Cover Problem (SCP)")
        choice = input("Enter your choice (1 or 2): ") or "1"

        if choice == "1":
            problem_type = "continuous"
        elif choice == "2":
            problem_type = "scp"
        else:
            print(f"\nERROR: Invalid choice '{choice}'. Please enter 1 or 2.")

    f_name = None
    if problem_type == "continuous":
        # Listar funciones continuas disponibles
        from problems.continuous.get_f import Get_F

        available_funcs = []
        func_details = []
        for i in range(1, 24):
            try:
                lb, ub, dim, _ = Get_F(f"F{i}")
                available_funcs.append(f"F{i}")
                func_details.append(f"{f'F{i}':<4} | lb: {lb} | ub: {ub} | dim: {dim}")
            except Exception:
                pass

        while not f_name:
            print("\nAvailable continuous functions:")
            for detail in func_details:
                print(detail)
            f_name_input = (
                input("Objective function name (e.g. F23 or 'all'): ") or "F23"
            )

            f_name_check = f_name_input.lower()
            if f_name_check == "all" or f_name_check.upper() in available_funcs:
                f_name = f_name_input
            else:
                print(
                    f"\nERROR: Invalid function '{f_name_input}'. "
                    "Please select from the list or type 'all'."
                )

    elif problem_type == "scp":
        instance_path = os.path.join("problems", "SCP", "Instances")
        available_instances = [
            f.split(".")[0] for f in os.listdir(instance_path) if f.endswith(".txt")
        ]

        while not f_name:
            print("\nAvailable SCP instances (some examples):")
            for inst in sorted(available_instances)[:10]:
                print(f"- {inst}")
            if len(available_instances) > 10:
                print("- ... and many more.")

            f_name_input = input("SCP instance name (e.g., scp41): ") or "scp41"

            if f_name_input in available_instances:
                f_name = f_name_input
            else:
                print(
                    f"\nERROR: Invalid SCP instance '{f_name_input}'. "
                    "Please select a valid instance."
                )

    # Normalizar nombre de función (mayúsculas)
    if f_name.lower() not in ["all", "todas"]:
        if f_name.startswith("f") and f_name[1:].isdigit():
            f_name = f_name.upper()

    # Selección de la variante
    variant = None
    while not variant:
        print("\nAvailable variants:")
        print("(You can copy/paste the exact name)")
        for v in VARIANT_FUNCTIONS:
            print(f"- {v}")
        print("- all")
        variant_input = (
            input("Select variant (or 'all' to run all): ")
            or list(VARIANT_FUNCTIONS.keys())[0]
        )

        if (
            variant_input.lower() in ["all", "todas"]
            or variant_input in VARIANT_FUNCTIONS
        ):
            variant = variant_input
        else:
            print(
                f"\nERROR: Invalid variant '{variant_input}'. "
                "Please select from the list or type 'all'."
            )

    import matplotlib.pyplot as plt

    # Obtener lista de funciones
    # Get_F imported from utils at top
    available_funcs = []
    for i in range(1, 24):
        try:
            lb, ub, dim, fobj = Get_F(f"F{i}")
            available_funcs.append(f"F{i}")
        except Exception:
            pass

    # Determinar funciones y variantes a ejecutar
    if f_name.lower() in ["all", "todas"]:
        funcs_to_run = available_funcs
    else:
        funcs_to_run = [f_name]

    if variant.lower() in ["all", "todas"]:
        variants_to_run = list(VARIANT_FUNCTIONS.keys())
    else:
        variants_to_run = [variant]

    # Ejecutar todas las combinaciones
    all_best_results = []
    for func in funcs_to_run:
        print(f"\n{'='*20} RUNNING FUNCTION: {func} {'='*20}")

        if problem_type == "continuous":
            try:
                lb, ub, dim, fobj = Get_F(func)
                lb = np.array(lb, dtype=float)
                ub = np.array(ub, dtype=float)
            except Exception:
                print(
                    f"ERROR: Objective function '{func}' cannot be loaded."
                )
                continue
        elif problem_type == "scp":
            try:
                instance = SCP(func)  # func es el nombre de la instancia, ej. 'scp41'
                dim = instance.getColumns()
                lb = np.zeros(dim)
                ub = np.ones(dim)

                # Wrapper para la función objetivo de SCP
                def fobj_wrapper(solution_continuous):
                    # 1. Binarizar la solución
                    solution_binary = (solution_continuous > 0.5).astype(int)

                    # 2. Verificar factibilidad y reparar si es necesario
                    is_feasible = instance.factibilityTest(solution_binary)[0]
                    if not is_feasible:
                        solution_binary = instance.repair(
                            solution_binary, "simple"
                        )  # o 'complex'

                    # 3. Calcular fitness con la solución binaria y factible
                    return instance.fitness(solution_binary)

                fobj = fobj_wrapper

            except Exception:
                print(f"ERROR: SCP instance '{func}' cannot be loaded.")
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

            if v == "eao":
                # Ejecutar EAO solo una vez, obtener curva de convergencia real
                from metaheuristics.eao import EAO

                OptimalCatalysis, BestSubstrate, conv_curve = EAO(
                    EnzymeCount, MaxIter, lb, ub, dim, fobj
                )
                # Actualizar población y fitness para compatibilidad
                population = lb + (ub - lb) * np.random.rand(EnzymeCount, dim)
                fitness = np.array([fobj(population[i, :]) for i in range(EnzymeCount)])
                best_idx = np.argmin(fitness)
                best = population[best_idx, :].copy()
            elif v == "pso":
                # Inicializar velocity y pbest
                velocity = np.zeros_like(population)
                pbest = np.copy(population)
                pbest_fitness = np.copy(fitness)
                conv_curve = np.zeros(MaxIter)
                for iter in range(MaxIter):
                    population, fitness, velocity = variant_func(
                        MaxIter,
                        iter,
                        dim,
                        population,
                        fitness,
                        best,
                        lb,
                        ub,
                        velocity,
                        pbest,
                    )
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
                    population, fitness = variant_func(
                        MaxIter, iter, dim, population, fitness, best, lb, ub
                    )
                    best_idx = np.argmin(fitness)
                    best = population[best_idx, :].copy()
                    conv_curve[iter] = fitness[best_idx]
                OptimalCatalysis = fitness[best_idx]
                BestSubstrate = best
            plt.plot(conv_curve, label=f"{v}")
            plt.savefig(f"{graficos_path}/convergence_{v}_{func}.png", dpi=300)
            datos_file = f"{datos_path}/result_{v}_{func}.csv"
            with open(datos_file, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Iteration", "BestValue"])
                for idx, val in enumerate(conv_curve):
                    writer.writerow([idx + 1, val])
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
            plt.xlabel("Iteration")
            plt.ylabel("Best value found")
            plt.title(f"Comparative Convergence Curve ({func})")
            plt.legend()
            plt.grid(True)
            comparative_plot_path = f"{graficos_path}/convergence_comparison_{func}.png"
            plt.savefig(comparative_plot_path, dpi=300)
            plt.close()
            print(f"Comparative plot for '{func}' saved to: {comparative_plot_path}")
            all_best_results.append(
                {
                    "function": func,
                    "variant": func_best_variant,
                    "value": func_best_val,
                    "substrate": func_best_substrate,
                }
            )
    print(f"\n\n{'='*25} SUMMARY OF BEST RESULTS {'='*25}")
    print(f"{'{Function}':<10} | {'{Best Variant}':<20} | {'{Best Value}':<25}")
    print(f"{'-'*10} | {'-'*20} | {'-'*25}")
    if not all_best_results:
        print(
            "No results obtained. Check that the objective function and "
            "variants are correct and that there are no runtime errors."
        )
    else:
        for result in all_best_results:
            valor_str = "{:.10e}".format(result["value"])
            print(
                f"{result['function']:<10} | "
                f"{result['variant']:<20} | "
                f"{valor_str:<25}"
            )
    graficos_path = os.path.join(resultados_path, "plots")
    # Importar utilidades desde el paquete utils
    from utils.metrics import calculate_metrics
    from utils.plots import comparative_boxplot

    # Save metrics and boxplot for the best results
    values = [result["value"] for result in all_best_results]
    metrics = calculate_metrics(values)
    # Save metrics in results folder
    with open(os.path.join(resultados_path, "summary_metrics.txt"), "w") as f:
        for k, v in metrics.items():
            f.write(f"{k}: {v}\n")
    # Boxplot comparativo de variantes
    variants = [result["variant"] for result in all_best_results]
    comparative_boxplot(
        [np.array([result["value"]]) for result in all_best_results],
        variants,
        os.path.join(graficos_path, "boxplot_best.png"),
    )
    # Curva de convergencia comparativa (si hay datos)
    # (Ejemplo: usar las curvas de convergencia de las variantes de la última función)
    # Puedes adaptar esto para guardar todas las curvas si lo deseas
    print("=" * 75)


if __name__ == "__main__":
    main()
