# Notas de cierre del release 1.0.1

La versión 1.0.1 corrige la orden de pytest del release inicial: la suite se
ejecuta desde `causal_benchmark_zoo/` para evitar que el directorio contenedor
oculte el paquete Python instalado. El tag `v1.0.0` conserva el historial
original; use `v1.0.1` para la edición corregida.

Fecha de preparación: 2026-10-15. El alcance está definido en [`RELEASE_SCOPE.md`](./RELEASE_SCOPE.md) y las huellas de archivos en [`RELEASE_MANIFEST.json`](./RELEASE_MANIFEST.json).

## Controles ejecutados

Los siguientes comandos se ejecutaron en un entorno virtual nuevo (`/tmp/causal_benchmark_release_env`) con Python 3.13.13, instalando `requirements-dev.txt` y `causal_benchmark_zoo` en editable:

```text
python scripts/validate_release.py       -> 43 escenarios; 0 errores; 16 advertencias
(cd causal_benchmark_zoo && python -m pytest -q tests) -> 30 passed
python -m causal_benchmark_zoo.fetch validate-all -> 4 manifests válidos
python -m causal_benchmark_zoo.fetch list -> 4 benchmarks registrados
```

También se cargó `lalonde_nsw` desde Parquet y se inspeccionó `bnlearn_asia` con el CLI. La primera instalación limpia reveló que faltaba `pyarrow`; se añadió a `requirements.txt` y a `causal_benchmark_zoo/pyproject.toml`, y la segunda ejecución quedó en 30/30 tests.

El validador de los escenarios ejecutó todos los 43 directorios: 33 pasan sin advertencia, 10 tienen advertencias documentadas y ninguno tiene error. Las advertencias no son fallos de integridad:

- siete archivos `data.csv` legacy contienen truth junto con la tabla histórica; para evaluar use los archivos `observed_*` o `data_public.csv`;
- tres escenarios Twins son controles negativos no estimables y por diseño tienen tratamiento/outcome constantes;
- las mismas tres variantes Twins repiten esa señal en sus columnas constantes.

La ejecución genera los reportes comprometidos bajo `causal_benchmark_synthetic/results/validation/`; el validador transversal escribe en un directorio temporal y no modifica el árbol de trabajo.

## Límites conocidos

`csuite_lingauss` permanece `pending/manual` porque su descarga pública respondió HTTP 403; no se simula ni se incorpora un archivo inventado. La compatibilidad de Python 3.10 se declara en los manifests y CI, pero la ejecución local documentada en este cierre fue Python 3.13.13. Las integraciones opcionales no forman parte de la ruta base ni de la suite obligatoria.
