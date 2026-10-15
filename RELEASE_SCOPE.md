# Alcance del release

Este repositorio contiene dos componentes distribuidos juntos:

- `causal_benchmark_synthetic/`: 43 escenarios, sus CSV, metadatos, grafos/truth cuando están declarados, índices, scorecards y reportes de validación.
- `causal_benchmark_zoo/`: código Python, manifests, schemas, benchmarks procesados, tests, ejemplos y documentación.

Se excluyen del control de versiones y de `RELEASE_MANIFEST.json` los artefactos reproducibles `build/`, `dist/`, `*.egg-info/`, `.pytest_cache/`, `__pycache__/`, `.ipynb_checkpoints/`, `.benchmarks/` y las salidas locales de `results/discovery/`, `results/inference/` y `results/full_pipeline/`. Los scorecards y reportes comprometidos bajo `results/scorecards/` y `results/validation/` sí forman parte de la evidencia del release.

La distribución pública de un curso puede ser un subconjunto: entregue los archivos `observed_*` y el contrato del escenario al estudiante y conserve `truth_*`, grafos de referencia y scorecards en el paquete de evaluación. El repositorio completo de benchmarks sí incluye esos artefactos porque su propósito es reproducir la evaluación.

No se han encontrado credenciales ni datos personales en la inspección del release. Las fuentes externas conservan las condiciones indicadas en sus manifests y documentos de limitaciones.
