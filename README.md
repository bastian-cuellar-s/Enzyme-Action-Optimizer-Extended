# Enzyme Action Optimizer — Enzyme-Action-Optimizer-Extended

![CI](https://github.com/bastian-cuellar-s/Enzyme-Action-Optimizer-Extended/actions/workflows/ci.yml/badge.svg)
![Coverage](https://codecov.io/gh/bastian-cuellar-s/Enzyme-Action-Optimizer-Extended/branch/main/graph/badge.svg)


Este repositorio contiene una implementación en Python del marco "Enzyme Action Optimizer" (EAO) y varias metaheurísticas y utilidades relacionadas para comparar su desempeño sobre un conjunto de funciones de referencia (CEC2022). El objetivo es ofrecer un proyecto modular, fácil de ejecutar y de extender.

## Resumen del algoritmo

Enzyme Action Optimizer (EAO) es un algoritmo metaheurístico bio-inspirado que modela comportamientos adaptativos semejantes a la acción de enzimas sobre sustratos. En esta implementación EAO se incluye como una variante especial que se ejecuta en un solo run y devuelve una curva de convergencia (historia del mejor valor por iteración). Además el repositorio contiene otras metaheurísticas clásicas (PSO, GWO, MVO, DE, etc.) para comparación.

Puntos clave:
- EAO se ejecuta como un proceso independiente (no itera de forma 'step-by-step' en la interfaz principal) y por eso en el runner hay un adaptador que convierte su salida a una curva de convergencia.
- PSO y algunos métodos requieren estado (velocidades, pbest), el runner ya incluye casos especiales para mantener ese estado entre iteraciones.

## Requisitos

- Python 3.8+
 
Makefile targets
---------------

You can use the provided `Makefile` for common tasks (on Unix):

```bash
make setup   # create venv
make install # install runtime deps
make test    # run pytest if tests exist
make lint    # run flake8
make format  # run black
```

CI note
-------

The GitHub Actions workflow runs `flake8` and `black --check` but currently treats their results as warnings (they do not fail the CI job). This keeps the pipeline permissive while still reporting style issues. If you later want strict enforcement, we can change the workflow to fail on style errors.
# Enzyme Action Optimizer — Enzyme-Action-Optimizer-Extended

Authors / Autores:

- BASTIAN STEFANO CUELLAR SALINAS
- CAMILA ROXANA MUÑOZ CUYUL
- MILENKA ORIANA ZUVIC PINOCHET

---

English (EN)
==============

This repository contains a Python implementation of the Enzyme Action Optimizer (EAO) framework and several metaheuristics and utilities to compare their performance on benchmark functions (CEC2022). The aim is to provide a modular, easy-to-run, and extensible project.

Algorithm summary
-----------------

Enzyme Action Optimizer (EAO) is a bio-inspired metaheuristic algorithm that models adaptive behaviors similar to enzyme actions on substrates. In this implementation, EAO is included as a special variant that runs as a single process and returns a convergence curve (best value per iteration). The repository also includes classical metaheuristics (PSO, GWO, MVO, DE, etc.) for comparison.

Key points:

- EAO runs as a single experiment (not step-by-step), so the runner adapts the output into a per-iteration convergence curve.
- PSO and some algorithms require persistent state (velocities, personal bests); the main runner handles these cases specially.

Requirements
------------

- Python 3.8+
- Install dependencies using the bundled requirements file:

```powershell
pip install -r requirements.txt
```

Repository layout (short)
------------------------

- `main.py` — main script to run experiments (interactive CLI).
- `metaheuristics/` — modular algorithm implementations (PSO, GWO, MVO, DE, EAO, ...).
- `utils/` — core utilities (`get_f.py`, `metrics.py`, `plots.py`, `helpers.py`, `eao_variants.py`).
- `results/` — output folder created by `main.py` for data and plots.
- `tools/` — optional migration and quick-test scripts (can be removed if not needed).

Quick usage
-----------

Run the main script and follow the menu:

```powershell
python main.py
```

You will be asked for:

- Number of enzymes (population size)
- Maximum number of iterations
- Benchmark function (e.g. `F1`, `F2`, ...)
- Variant to run (algorithm name or `all`)

Outputs
-------

- `results/data/` — CSVs with convergence history per run.
- `results/plots/` — PNGs with convergence curves and comparative boxplots.
- `results/summary_metrics.txt` — summary with mean/std/best/worst per variant.

Notes and known issues
----------------------

- Population-size requirements: some algorithms (e.g., DE) assume a minimum population when sampling without replacement. Avoid very small population sizes during quick tests (e.g., < 4). If you see the error "Cannot take a larger sample than population when 'replace=False'", increase the number of agents.
- The `utils` package exposes English module names only (`metrics`, `plots`, `helpers`, `get_f`, `eao_variants`).

Tools
-----

- `tools/migrate_results.py` — migrate an old Spanish `resultados/` folder to the new English `results/` layout (rename files, headers, and subfolders).
- `tools/run_quick.py` — run `main.main()` with canned inputs for quick testing.
- `tools/temp_smoke.py` — small smoke-test runner.

If you don't need these helpers, it's safe to remove the `tools/` folder.

Release / Packaging helpers
---------------------------

There are three helper scripts to build distributable artifacts (sdist + wheel):

- PowerShell (Windows): `scripts/build_release.ps1`
- Bash (Linux/macOS): `scripts/build_release.sh`
- Cross-platform Python: `scripts/build_release.py` (recommended if you want a single command)

Usage examples:

PowerShell (Windows):
```powershell
& 'scripts\build_release.ps1'
```

Linux / macOS:
```bash
chmod +x scripts/build_release.sh
./scripts/build_release.sh
```

Cross-platform (any OS with Python):
```bash
python scripts/build_release.py
```

All scripts will produce the distributions inside `dist/` and will also create
`dist/release_artifacts.zip` when `zip` is available. The zip can be uploaded to a
GitHub Release or used for manual distribution.

CI note: the repository includes a GitHub Actions workflow `.github/workflows/release.yml`
that triggers on Release creation. I also expanded the workflow to support manual
dispatch and tag pushes so builds can be triggered either via the web UI or by
pushing a tag (see `.github/workflows/release.yml`).

Publishing to PyPI
------------------

If you want to publish the package to PyPI, follow these steps locally and/or via CI.

1. Bump the version in `pyproject.toml` or the relevant place (if you track the version there).
2. Create a tag and push it (this repo's release workflow also supports tag pushes):

```bash
git tag v0.1.0
git push origin v0.1.0
```

3. Build artifacts (locally or in CI):

PowerShell:
```powershell
& 'scripts\build_release.ps1'
```

Linux/macOS:
```bash
./scripts/build_release.sh
```

Cross-platform (Python):
```bash
python scripts/build_release.py
```

4. Upload to PyPI using `twine` (recommended). Install twine and upload:

```bash
python -m pip install --upgrade twine
# Use an API token stored in the environment (recommended). On CI set the secret PYPI_API_TOKEN.
python -m twine upload dist/* -u __token__ -p "$PYPI_API_TOKEN"
```

CI notes for publishing
----------------------
- Add a repository secret named `PYPI_API_TOKEN` with a PyPI token (create it on https://pypi.org/manage/account/#api-tokens).
- Add/enable a GitHub Actions job that runs on `push` of tags (or on `release`) which:
	- builds sdist and wheel (`python -m build`)
	- runs tests
	- uploads with `twine` using the secret above

Example minimal GitHub Actions step (inside a job):

```yaml
- name: Publish to PyPI
	if: startsWith(github.ref, 'refs/tags/')
	env:
		PYPI_API_TOKEN: ${{ secrets.PYPI_API_TOKEN }}
	run: |
		python -m pip install --upgrade build twine
		python -m build --sdist --wheel
		python -m twine upload dist/* -u __token__ -p "$PYPI_API_TOKEN"
```

Security note: prefer PyPI API tokens (scoped) and store them as repository secrets; avoid storing credentials in plaintext.


Environment setup (recommended)
-------------------------------

There is a PowerShell helper to create a virtual environment and install pinned dependencies:

```powershell
.\setup_env.ps1
```

This script creates a `venv/`, activates it (if run interactively), upgrades pip and installs:
- `requirements.txt` (runtime dependencies pinned)
- `requirements-dev.txt` (pytest, black, flake8)


Contributing / Adding a new variant
----------------------------------

1. Add a new file under `metaheuristics/` implementing the variant.
2. Ensure the exported function matches the signature expected by `utils/eao_variants.get_variant_func()` (check that file). Iterative algorithms should provide a per-iteration callable or be adapted accordingly.
3. Register the variant in `utils/eao_variants.py` so it appears in the `main.py` menu.

Quick examples
--------------

Run one function with all variants (interactive):

```powershell
python main.py
# example responses: 10 (population), 50 (iter), F1, all
```

Run the quick, non-interactive test (if `tools/run_quick.py` is present):

```powershell
python .\tools\run_quick.py
```

Interacting with GitHub Actions and Releases using GitHub CLI
-----------------------------------------------------------

You can use the GitHub CLI (`gh`) to interact with workflow runs and releases directly from the command line.

### 1. Installation

Install `gh` on Windows using `winget` or `scoop`:

```powershell
# Using winget
winget install --id GitHub.cli

# Using scoop
scoop install gh
```

For other systems, refer to the [official installation guide](https://github.com/cli/cli#installation).

### 2. Authentication

Log in to your GitHub account. You can use a browser-based login (recommended) or a personal access token (PAT).

```powershell
# Follow the prompts to authenticate in your browser
gh auth login
```

### 3. List and View Workflow Runs

You can list recent runs for the `release.yml` workflow and find the one corresponding to a specific tag, like `v0.1.1`.

```powershell
# List the last 10 runs for the release workflow
gh run list --workflow release.yml --limit 10
```

From the list, copy the **RUN ID** of the run triggered by the `v0.1.1` tag.

To see details, view logs, or open the run in a browser:

```powershell
# View details of a specific run (replace <RUN_ID>)
gh run view <RUN_ID>

# View the run in your web browser
gh run view <RUN_ID> --web

# View the logs for all jobs in the run
gh run view <RUN_ID> --log
```

### 4. Download Artifacts

You can download artifacts directly from a workflow run. The `release.yml` workflow produces an artifact named `release_artifacts.zip`.

```powershell
# Download the artifact from the run (replace <RUN_ID>)
# The artifact will be downloaded to the current directory
gh run download <RUN_ID> -n release_artifacts.zip
```

### 5. View and Download from a Release

Alternatively, you can interact with the GitHub Release created by the workflow.

```powershell
# View the details of the v0.1.1 release
gh release view v0.1.1

# List the assets attached to the release
gh release view v0.1.1 --json assets

# Download the release_artifacts.zip from the release
gh release download v0.1.1 --pattern "release_artifacts.zip"
```

License
-------

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

Contact
-------

For questions or suggestions, please open an issue in the repository.

---

Español (ES)
============

Este repositorio contiene una implementación en Python del marco "Enzyme Action Optimizer" (EAO) y varias metaheurísticas y utilidades para comparar su desempeño en funciones de referencia (CEC2022). La meta es ofrecer un proyecto modular, fácil de ejecutar y de extender.

Resumen del algoritmo
---------------------

Enzyme Action Optimizer (EAO) es un algoritmo metaheurístico bio-inspirado que modela comportamientos adaptativos semejantes a la acción de enzimas sobre sustratos. En esta implementación, EAO se incluye como una variante especial que se ejecuta en un único run y devuelve una curva de convergencia (mejor valor por iteración). El repositorio también incluye metaheurísticas clásicas (PSO, GWO, MVO, DE, etc.) para comparación.

Puntos clave:

- EAO se ejecuta como un experimento completo (no paso-a-paso), por lo que el runner adapta su salida a una curva de convergencia por iteración.
- PSO y algunos métodos requieren estado persistente (velocidades, pbest); el runner principal maneja estos casos de forma especial.

Requisitos
----------

- Python 3.8+
- Dependencias (instalar con el fichero requirements.txt):

```powershell
pip install -r requirements.txt
```

Estructura del repositorio (resumen)
-----------------------------------

- `main.py` — script principal para ejecutar experimentos (CLI interactivo).
- `metaheuristics/` — implementaciones modulares de algoritmos.
- `utils/` — utilidades centrales (`get_f.py`, `metrics.py`, `plots.py`, `helpers.py`, `eao_variants.py`).
- `results/` — carpeta de salida creada por `main.py`.
- `tools/` — scripts opcionales para migración y pruebas rápidas.

Uso (básico)
------------

Ejecuta el script principal y responde el menú:

```powershell
python main.py
```

Entradas solicitadas:

- Número de enzimas (tamaño de población)
- Número máximo de iteraciones
- Función de benchmark (ej.: `F1`, `F2`, ...)
- Variante a ejecutar (nombre del algoritmo o `all`)

Salidas
------

- `results/data/` — CSVs con historia de convergencia por ejecución.
- `results/plots/` — PNGs con curvas y boxplots comparativos.
- `results/summary_metrics.txt` — resumen con media/std/mejor/peor por variante.

Notas y problemas conocidos
--------------------------

- Requisitos de tamaño de población: algunos algoritmos (p. ej. DE) asumen una población mínima al muestrear sin reemplazo. Evita tamaños muy pequeños en pruebas rápidas (p. ej. < 4). Si ves el error "Cannot take a larger sample than population when 'replace=False'", aumenta el número de agentes.
- El paquete `utils` expone módulos en inglés (`metrics`, `plots`, `helpers`, `get_f`, `eao_variants`).

Herramientas
-----------

- `tools/migrate_results.py` — migrar una carpeta antigua `resultados/` a `results/`.
- `tools/run_quick.py` — ejecutar `main.main()` con entradas predefinidas.
- `tools/temp_smoke.py` — runner de smoke tests.

Contribuir / Añadir variantes
----------------------------

1. Crea un archivo nuevo en `metaheuristics/` con la variante.
2. Asegura que la función exportada tenga la firma esperada por `utils/eao_variants.get_variant_func()`.
3. Registra la variante en `utils/eao_variants.py`.

Ejemplos rápidos
---------------

Ejecutar una función con todas las variantes (interactivo):

```powershell
python main.py
# respuestas ejemplo: 10 (población), 50 (iter), F1, all
```

Ejecutar prueba rápida no interactiva:

```powershell
python .\tools\run_quick.py
```

Interactuar con GitHub Actions y Releases usando GitHub CLI
-----------------------------------------------------------

Puedes usar la GitHub CLI (`gh`) para interactuar con las ejecuciones de workflows y las releases directamente desde la línea de comandos.

### 1. Instalación

Instala `gh` en Windows usando `winget` o `scoop`:

```powershell
# Usando winget
winget install --id GitHub.cli

# Usando scoop
scoop install gh
```

Para otros sistemas, consulta la [guía de instalación oficial](https://github.com/cli/cli#installation).

### 2. Autenticación

Inicia sesión en tu cuenta de GitHub. Puedes usar el inicio de sesión basado en navegador (recomendado) o un token de acceso personal (PAT).

```powershell
# Sigue las instrucciones para autenticarte en tu navegador
gh auth login
```

### 3. Listar y Ver Ejecuciones de Workflow

Puedes listar las ejecuciones recientes del workflow `release.yml` y encontrar la que corresponde a una etiqueta específica, como `v0.1.1`.

```powershell
# Listar las últimas 10 ejecuciones del workflow de release
gh run list --workflow release.yml --limit 10
```

De la lista, copia el **RUN ID** de la ejecución disparada por la etiqueta `v0.1.1`.

Para ver detalles, logs, o abrir la ejecución en el navegador:

```powershell
# Ver detalles de una ejecución específica (reemplaza <RUN_ID>)
gh run view <RUN_ID>

# Ver la ejecución en tu navegador web
gh run view <RUN_ID> --web

# Ver los logs de todos los jobs en la ejecución
gh run view <RUN_ID> --log
```

### 4. Descargar Artefactos

Puedes descargar artefactos directamente desde una ejecución de workflow. El workflow `release.yml` produce un artefacto llamado `release_artifacts.zip`.

```powershell
# Descargar el artefacto de la ejecución (reemplaza <RUN_ID>)
# El artefacto se descargará en el directorio actual
gh run download <RUN_ID> -n release_artifacts.zip
```

### 5. Ver y Descargar desde una Release

Alternativamente, puedes interactuar con la Release de GitHub creada por el workflow.

```powershell
# Ver los detalles de la release v0.1.1
gh release view v0.1.1

# Listar los assets adjuntos a la release
gh release view v0.1.1 --json assets

# Descargar el release_artifacts.zip desde la release
gh release download v0.1.1 --pattern "release_artifacts.zip"
```

Licencia
-------------------

Este proyecto está licenciado bajo la Licencia Pública General de GNU v3.0. Consulta el archivo [LICENSE](LICENSE) para más detalles.

Contacto
-------------------

Para preguntas o sugerencias, por favor abre un issue en el repositorio.

---
