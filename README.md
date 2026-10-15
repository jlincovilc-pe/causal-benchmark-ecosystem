# Causal Benchmark Ecosystem

[![CI](https://github.com/jlincovilc-pe/causal-benchmark-ecosystem/actions/workflows/ci.yml/badge.svg)](https://github.com/jlincovilc-pe/causal-benchmark-ecosystem/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

Repositorio reproducible para comparar métodos de descubrimiento causal e inferencia de efectos. Incluye los datos, el contrato de cada escenario y un paquete Python pequeño para cargar, validar y evaluar benchmarks.

## Qué contiene

| Componente | Contenido | Entrada principal |
|---|---|---|
| [`causal_benchmark_synthetic/`](./causal_benchmark_synthetic/) | 43 escenarios versionados: 7 basados en estructuras de literatura y 36 controlados | [`release_index/dataset_index.csv`](./causal_benchmark_synthetic/release_index/dataset_index.csv) |
| [`causal_benchmark_zoo/`](./causal_benchmark_zoo/) | Registro, loaders, validación de manifests y métricas de grafos | [`README.md`](./causal_benchmark_zoo/README.md) |
| [`scripts/validate_release.py`](./scripts/validate_release.py) | Comprobación de coherencia del release completo | `python scripts/validate_release.py` |

La colección incluye 27 tareas de descubrimiento, 7 de estimación de efectos, 5 de enlaces temporales y 4 escenarios sin objetivo puntuable. El inventario y sus números son la fuente de verdad; esta descripción no se actualiza a mano cuando cambia el catálogo.

### Qué significa `real/`

El nombre `datasets/real/` identifica escenarios cuya **estructura, nombres o referencia de efecto** provienen de publicaciones. Los valores numéricos distribuidos en este repositorio son generados por SEM y están documentados en cada `metadata.json`. No se distribuyen historias clínicas, datos de personas ni credenciales. No use esos escenarios para afirmar validez externa sobre una población real.

Los archivos observacionales (`observed_*.csv`, `observed.csv` o `data_public.csv`) son las entradas de un estimador. Los archivos `truth_*`, `y0`, `y1`, `tau`, los grafos y los `scorecard.json` son información de evaluación y solo deben usarse cuando el protocolo lo permita. El contrato completo está en [`BENCHMARK_SCHEMA.md`](./causal_benchmark_synthetic/BENCHMARK_SCHEMA.md).

## Inicio rápido

Requiere Python 3.10 o posterior. La ruta base no necesita nube ni servicios externos.

```bash
git clone https://github.com/jlincovilc-pe/causal-benchmark-ecosystem.git
cd causal-benchmark-ecosystem
python -m venv .venv
source .venv/bin/activate                 # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/validate_release.py
```

Para ejecutar las pruebas del paquete:

```bash
python -m pip install -r requirements-dev.txt
python -m pip install -e causal_benchmark_zoo
python -m pytest -q causal_benchmark_zoo/tests
```

Para probar el CLI del zoo:

```bash
python -m causal_benchmark_zoo.fetch list
python -m causal_benchmark_zoo.fetch validate-all
python -m causal_benchmark_zoo.fetch inspect bnlearn_asia
```

Para validar únicamente los escenarios sintéticos (la salida se escribe en un directorio temporal):

```bash
python causal_benchmark_synthetic/scripts/00_validate_benchmark.py \
  --root causal_benchmark_synthetic \
  --output /tmp/causal-benchmark-validation
```

Si la instalación falla, revise `python --version`, active el entorno virtual y vuelva a ejecutar el diagnóstico. No copie el entorno del autor ni dependa de archivos fuera de este repositorio. Los paquetes opcionales para algoritmos de descubrimiento e integraciones DoWhy/EconML están enumerados en [`requirements-optional.txt`](./requirements-optional.txt); no son necesarios para validar el release.

## Uso en el curso

El curso `Sistema de Inteligencia Causal` consume una selección pequeña de este catálogo. El repositorio de benchmarks conserva los 43 escenarios para prácticas y proyectos; no todos deben entregarse a un estudiante en cada cohorte. Una distribución docente puede seleccionar solo los CSV observacionales y mantener los artefactos de truth en el repositorio de evaluación.

La separación entre entrada y evaluación es deliberada:

1. el estudiante recibe la entrada observacional y el contrato del escenario;
2. el estimador produce su resultado y registra población, estimando e incertidumbre;
3. el corrector compara contra `truth_*`, grafos o scorecards según el tipo de tarea.

Un grafo de descubrimiento no es un estimando ATE/CATE, y una equivalencia de archivos no hace intercambiables las garantías científicas. Consulte [`docs/METRICS_GUIDE.md`](./causal_benchmark_synthetic/docs/METRICS_GUIDE.md) y [`causal_benchmark_zoo/docs/ground_truth_taxonomy.md`](./causal_benchmark_zoo/docs/ground_truth_taxonomy.md).

## Reproducibilidad y alcance del release

- [`RELEASE_MANIFEST.json`](./RELEASE_MANIFEST.json) contiene la versión, el entorno de validación y un SHA-256 de cada archivo incluido (se excluye a sí mismo).
- [`RELEASE_SCOPE.md`](./RELEASE_SCOPE.md) define qué se versiona y qué se genera localmente.
- Los directorios `build/`, `.pytest_cache/`, `__pycache__/`, `*.egg-info/` y `.benchmarks/` son artefactos locales y no forman parte del release.
- Los informes de validación y scorecards comprometidos son evidencia de una ejecución; la validación reproducible vuelve a ejecutarse con los scripts.
- No se usa Git LFS: el archivo más grande del release está por debajo del límite de blob de GitHub.

Para regenerar datos sintéticos, revisar semillas y comprender qué es observable, use [`causal_benchmark_synthetic/scripts/`](./causal_benchmark_synthetic/scripts/) y la documentación de cada escenario. Generar datos no sustituye la revisión del contrato ni convierte un escenario en dato real.

## Proveniencia, licencias y citación

El código propio se distribuye bajo MIT. Algunos artefactos se basan en bnlearn, NBER/Dehejia-Wahba y publicaciones de Sachs, Hill, LaLonde, Twins y otras fuentes; sus condiciones y referencias se mantienen en los manifests y metadatos. Lea [`causal_benchmark_zoo/LIMITATIONS.md`](./causal_benchmark_zoo/LIMITATIONS.md) antes de redistribuir un subconjunto.

Cite [`CITATION.cff`](./CITATION.cff) y las fuentes originales indicadas por el escenario. Las incidencias y contribuciones se gestionan conforme a [`CONTRIBUTING.md`](./CONTRIBUTING.md).

## Estado conocido

`csuite_lingauss` está registrado pero requiere descarga manual porque la fuente pública devolvió HTTP 403 durante la preparación del release. Los demás benchmarks registrados tienen manifest y artefactos locales verificables. Esta limitación no afecta a los 43 escenarios del componente sintético.

## Estructura

```text
causal_benchmark_synthetic/   # datos, metadatos, truth, índices y scorecards
causal_benchmark_zoo/          # paquete Python, manifests, schemas, ejemplos y tests
scripts/                       # validación transversal del release
.github/workflows/ci.yml       # instalación y controles automáticos
```

Para añadir un escenario, siga [`causal_benchmark_zoo/docs/adding_a_dataset.md`](./causal_benchmark_zoo/docs/adding_a_dataset.md) y actualice el índice, el manifest, la licencia y la evidencia de validación en el mismo cambio.
