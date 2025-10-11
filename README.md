# Enzyme Action Optimizer — Enzyme-Action-Optimizer-Extended

Authors / Autores:

- BASTIAN STEFANO CUELLAR SALINAS
- CAMILA ROXANA MUÑOZ CUYUL
- MILENKA ORIANA ZUVIC PINOCHET

---

English (EN)
=============

A concise, clear README for running the project.

## Overview

Python implementation of the Enzyme Action Optimizer (EAO) framework and several metaheuristics. Modular, easy to run and extend.

## Requirements

- Python 3.8+
- Install dependencies:

```powershell
pip install -r requirements.txt
```

### Virtual environment (PowerShell)

It's recommended to use a virtual environment to avoid polluting the system Python.

Create and install dependencies (from project root):

```powershell
# create venv in .venv and install requirements
.\scripts\setup_venv.ps1
```

Manual steps (equivalent):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

To run the project inside the activated environment:

```powershell
python main.py
```

## Quick start

Run the interactive main script:

```powershell
python main.py
```

The CLI will prompt for:
- Population size (number of enzymes)
- Maximum iterations
- Problem type (continuous or SCP/USCP)
- Objective function or instance
- Variant (algorithm) to run

## Outputs

- `results/data/` — CSVs with convergence/history per run
- `results/plots/` — PNGs with convergence curves and boxplots
- `results/summary_metrics.txt` — aggregated metrics per variant

## Project layout

- `main.py` — interactive runner
- `problems/` — problem definitions and instances
- `metaheuristics/` — algorithm implementations
- `utils/` — helpers, metrics and plotting utilities
- `results/` — generated outputs

## Contributing

1. Add a new file under `metaheuristics/` implementing the variant.
2. Ensure the exported function matches the signature expected by `utils/eao_variants.get_variant_func()`.
3. Register the variant in `utils/eao_variants.py` so it appears in `main.py`.

---

Español (ES)
===========

README conciso y claro para ejecutar el proyecto.

## Resumen

Implementación en Python del marco Enzyme Action Optimizer (EAO) y varias metaheurísticas. Modular y fácil de ejecutar.

## Requisitos

- Python 3.8+
- Instalar dependencias:

```powershell
pip install -r requirements.txt
```

### Entorno virtual (PowerShell)

Se recomienda usar un entorno virtual para evitar ensuciar la instalación global de Python.

Crear e instalar dependencias (desde la raíz del proyecto):

```powershell
# crea .venv e instala dependencias
.\scripts\setup_venv.ps1
```

Pasos manuales (equivalente):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Para ejecutar el proyecto dentro del entorno activado:

```powershell
python main.py
```

## Inicio rápido

Ejecuta el script interactivo:

```powershell
python main.py
```

El CLI pedirá:
- Tamaño de población (número de enzimas)
- Número máximo de iteraciones
- Tipo de problema (continuo o SCP/USCP)
- Función objetivo o instancia
- Variante (algoritmo) a ejecutar

## Salidas

- `results/data/` — CSVs con historia de convergencia por ejecución
- `results/plots/` — PNGs con curvas de convergencia y boxplots
- `results/summary_metrics.txt` — métricas agregadas por variante

## Estructura del proyecto

- `main.py` — ejecutor interactivo
- `problems/` — definiciones e instancias
- `metaheuristics/` — implementaciones de algoritmos
- `utils/` — utilidades, métricas y gráficos
- `results/` — salidas generadas

## Contribuir

1. Añade un archivo en `metaheuristics/` con la variante.
2. Asegúrate de que la función exportada tenga la firma esperada por `utils/eao_variants.get_variant_func()`.
3. Registra la variante en `utils/eao_variants.py` para que aparezca en `main.py`.


