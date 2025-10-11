# Enzyme Action Optimizer — Enzyme-Action-Optimizer-Extended

<!-- CI and coverage badges removed per maintainer request -->

Authors / Autores:

- BASTIAN STEFANO CUELLAR SALINAS
- CAMILA ROXANA MUÑOZ CUYUL
- MILENKA ORIANA ZUVIC PINOCHET

---

English (EN)
==============

This repository contains a Python implementation of the Enzyme Action Optimizer (EAO) framework and several metaheuristics and utilities to compare their performance on benchmark functions. The aim is to provide a modular, easy-to-run, and extensible project.

## Installation

### From Source
Requires Python 3.8+. Install dependencies using the bundled requirements file:

```powershell
pip install -r requirements.txt
```

### From a GitHub Release
You can also install the package from a `.whl` file provided in a GitHub Release.

1.  Go to the [Releases page](https://github.com/bastian-cuellar-s/Enzyme-Action-Optimizer-Extended/releases) on GitHub.
2.  Download the `release_artifacts.zip` file from the latest release.
3.  Unzip the file. It contains a `.whl` file and a `.tar.gz` source distribution.
4.  Install the wheel file using `pip`:

```powershell
pip install path/to/enzyme_action_optimizer_extended-*.whl
```

## Quick Usage

Run the main script and follow the interactive menus:

```powershell
python main.py
```

The script will guide you through the following selections with validation:

1.  **Number of enzymes (population size)**: e.g., 50
2.  **Maximum number of iterations**: e.g., 500
3.  **Problem Type**: Choose between continuous functions or Set-Cover Problems (SCP).
4.  **Objective Function / Instance**: Select a specific benchmark function (e.g., `F1`, `F23`) or an SCP instance (e.g., `scp41`). The script will show a list of available options.
5.  **Variant**: Select the algorithm to run (e.g., `eao`, `pso`) or `all` to run all of them.

## Outputs

- `results/data/` — CSVs with convergence history per run.
- `results/plots/` — PNGs with convergence curves and comparative boxplots.
- `results/summary_metrics.txt` — summary with mean/std/best/worst per variant.

## Repository Layout

- `main.py` — main script to run experiments (interactive CLI).
- `problems/` — Problem definitions.
  - `problems/continuous/` — CEC/classical benchmark functions.
  - `problems/SCP/` — Set-Cover Problem instances and loader.
  - `problems/USCP/` — Unicost Set-Cover Problem instances and loader.
- `metaheuristics/` — modular algorithm implementations (PSO, GWO, MVO, DE, EAO, ...).
- `utils/` — core utilities (`metrics.py`, `plots.py`, `helpers.py`, `eao_variants.py`).
- `results/` — output folder created by `main.py` for data and plots.

## Contributing / Adding a new variant

1. Add a new file under `metaheuristics/` implementing the variant.
2. Ensure the exported function matches the signature expected by `utils/eao_variants.get_variant_func()` (check that file). Iterative algorithms should provide a per-iteration callable or be adapted accordingly.
3. Register the variant in `utils/eao_variants.py` so it appears in the `main.py` menu.

---

Español (ES)
============

Este repositorio contiene una implementación en Python del marco "Enzyme Action Optimizer" (EAO) y varias metaheurísticas y utilidades para comparar su desempeño en funciones de referencia. La meta es ofrecer un proyecto modular, fácil de ejecutar y de extender.

## Instalación

### Desde el código fuente
Requiere Python 3.8+. Instala las dependencias usando el archivo de requisitos:

```powershell
pip install -r requirements.txt
```

### Desde una Release de GitHub
También puedes instalar el paquete desde un archivo `.whl` disponible en las Releases de GitHub.

1.  Ve a la [página de Releases](https://github.com/bastian-cuellar-s/Enzyme-Action-Optimizer-Extended/releases).
2.  Descarga el archivo `release_artifacts.zip` de la última release.
3.  Descomprime el archivo. Contiene un fichero `.whl` y una distribución de código fuente `.tar.gz`.
4.  Instala el archivo wheel usando `pip`:

```powershell
pip install ruta/al/archivo/enzyme_action_optimizer_extended-*.whl
```

## Uso Rápido

Ejecuta el script principal y sigue los menús interactivos:

```powershell
python main.py
```

El script te guiará a través de las siguientes selecciones (con validación de entrada):

1.  **Número de enzimas (tamaño de población)**: ej: 50
2.  **Número máximo de iteraciones**: ej: 500
3.  **Tipo de Problema**: Elige entre funciones continuas o Problemas de Cobertura de Conjuntos (SCP).
4.  **Función Objetivo / Instancia**: Selecciona una función de benchmark específica (ej: `F1`, `F23`) o una instancia de SCP (ej: `scp41`). El script mostrará una lista de opciones disponibles.
5.  **Variante**: Selecciona el algoritmo a ejecutar (ej: `eao`, `pso`) o `all` para ejecutarlos todos.

## Salidas

- `results/data/` — CSVs con la historia de convergencia por cada ejecución.
- `results/plots/` — PNGs con curvas de convergencia y boxplots comparativos.
- `results/summary_metrics.txt` — Resumen con media/std/mejor/peor por cada variante.

## Estructura del Repositorio

- `main.py` — script principal para ejecutar experimentos (CLI interactivo).
- `problems/` — Definiciones de los problemas.
  - `problems/continuous/` — Funciones de benchmark clásicas/CEC.
  - `problems/SCP/` — Instancias y cargador para Set-Cover Problem.
  - `problems/USCP/` — Instancias y cargador para Unicost Set-Cover Problem.
- `metaheuristics/` — Implementaciones modulares de los algoritmos (PSO, GWO, MVO, DE, EAO, ...).
- `utils/` — Utilidades centrales (`metrics.py`, `plots.py`, `helpers.py`, `eao_variants.py`).
- `results/` — Carpeta de salida creada por `main.py` para datos y gráficos.

## Contribuir / Añadir una nueva variante

1. Crea un archivo nuevo en `metaheuristics/` con la implementación de la variante.
2. Asegura que la función exportada tenga la firma esperada por `utils/eao_variants.get_variant_func()` (revisa ese archivo). Los algoritmos iterativos deben proporcionar una función que se pueda llamar en cada iteración.
3. Registra la variante en `utils/eao_variants.py` para que aparezca en el menú de `main.py`.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Developer setup

The repository has been simplified per maintainer request: CI workflows and automated pre-commit hooks were removed from the active tree. If you still want local developer tooling, install Black and Flake8 locally and run them manually.

Backups of removed CI/workflow and test artifacts are available under `docs/removed_for_no_ci/` (for example `ci.yml.backup`, `release.yml.backup`, `requirements-dev.txt.backup`, and `.pre-commit-config.yaml.backup`).

## History rewrite (important)

On 2025-10-10 the repository history for `main` was rewritten and the branch on the remote was replaced to remove large LFS-tracked files. If you have a local clone, reset to the new `main` with:

```powershell
git fetch origin
git reset --hard origin/main
```

If you had uncommitted or unpushed work, back it up before running the commands above.

## Note about large files / Git LFS

This repository tracks some large assets (for example the `problems/` dataset directory) with Git LFS. If you plan to clone or contribute, please ensure `git-lfs` is installed and enabled in your environment. See `docs/MIGRATION_TO_LFS.md` for details and migration notes.

## Notes about the rewrite and how to resync (short)

The repository history was rewritten on 2025-10-10 to remove CI/test artifacts and large files from earlier commits. This operation replaced the remote main branch and is destructive for existing clones. If you already had a local clone, follow these steps to resynchronize safely:

1. Backup any local changes you care about (stash/branch or copy files).
2. Fetch the updated refs:

`powershell
git fetch origin
`

3. Hard-reset your local main to match the remote:

`powershell
git checkout main
git reset --hard origin/main
git clean -fdx
`

4. If you had local branches based on the old history, rebase them onto the new main or re-create them from scratch.

If you want me to preserve any of the pre-rewrite backup bundles or branches in a separate archive branch instead of deleting them, say so now and I will restore them to rchive/pre-rewrite-backups.

