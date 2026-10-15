# Contribuir al benchmark zoo

Las contribuciones deben mantener la separación entre datos observables y verdad de evaluación. Para añadir un benchmark:

1. cree un directorio bajo `benchmarks/<id>/` con un `manifest.yaml` válido;
2. documente la fuente, licencia, tarea, población, estimando y limitaciones;
3. incluya hashes SHA-256 de los artefactos disponibles y marque como `manual` o `pending` lo que no pueda distribuirse;
4. añada o actualice un test y ejecute `python -m pytest -q tests` y `python -m causal_benchmark_zoo.fetch validate-all`;
5. no incluya credenciales, datos personales, caches, artefactos de `build/` ni descargas que el manifest no describa.

Los cambios grandes de esquema requieren una nota de migración y una actualización del contrato correspondiente. Las licencias de fuentes externas no se sustituyen por la licencia MIT de este repositorio.
