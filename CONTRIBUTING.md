# Contribuciones

Este repositorio acepta correcciones de documentación, validadores y escenarios reproducibles. Antes de abrir un cambio:

1. cree un entorno virtual y ejecute `python scripts/validate_release.py`;
2. mantenga separados los archivos observacionales y los artefactos de truth;
3. documente la fuente, licencia, semilla, población, estimando y límites de cualquier dato nuevo;
4. ejecute `python -m pip install -r requirements-dev.txt`, `python -m pip install -e causal_benchmark_zoo` y `(cd causal_benchmark_zoo && python -m pytest -q tests)`;
5. no incluya credenciales, datos personales, caches, resultados locales o directorios de build.

Los cambios de contrato deben actualizar `BENCHMARK_SCHEMA.md`, los índices y los tests en el mismo cambio. Los datos externos conservan sus licencias originales; la licencia MIT del código no las reemplaza.
