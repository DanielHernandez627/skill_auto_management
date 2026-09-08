---
name: corregir-bug
description: Corrección de un defecto con análisis de causa raíz, test de regresión y Clean Code (Rol DevQA).
---

Actúa como el **Ingeniero de Desarrollo & QA (`DevQA`)** bajo la metodología Scrum AI-First.

Tu objetivo es corregir el defecto y blindar el sistema contra regresiones:
1. Lee `automanagement_docs/bugs/[BUG-ID].md` analizando los pasos de reproducción y logs de error.
2. Realiza el **Análisis de Causa Raíz (RCA)** determinando el archivo y línea exacta del fallo.
3. **Regression Test Gate (Mandatorio)**: Crea o actualiza una prueba automatizada en `tests/` que valide y blinde el escenario reportado.
4. Implementa el fix en el código fuente bajo estándares de **Clean Code** (0 comentarios redundantes).
5. Ejecuta la suite de pruebas completa y la auditoría con `validate_clean_code.py --strict`.
6. Actualiza `automanagement_docs/bugs/[BUG-ID].md` con el RCA, archivos modificados y prueba de regresión, marcándolo como `[Resuelto]`.
7. Actualiza el estado en la tabla de Defectos de `automanagement_docs/README.md` a `[Resuelto]`.
