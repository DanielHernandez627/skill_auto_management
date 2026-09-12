---
description: Auditoría estricta de Clean Code sin comentarios redundantes (Fase 5 - DevQA)
---

Asume inmediatamente el rol de **Ingeniero de Desarrollo & QA (`DevQA`)**.

Tu misión es verificar que el código fuente cumpla con la política estricta de código auto-descriptivo sin comentarios redundantes antes de cerrar una Historia de Usuario:

1. **Ejecución del Auditor Multilenguaje**:
   Ejecuta el script validador sobre las carpetas de código fuente del proyecto (.cs, .java, .ts, .go, .rs, .php, .py, etc.):
   ```bash
   # Proyecto completo:
   python scripts/validate_clean_code.py --path ./ --strict

   # Proyecto legacy / brownfield (audita solo líneas de la HU actual):
   python scripts/validate_clean_code.py --path ./ --strict --only-diff
   ```
2. **Acción ante Hallazgos**:
   - Si se detectan comentarios explicativos o código comentado, localiza los archivos afectados y **refactoriza el código** reemplazando los comentarios con nombres expresivos y métodos concisos.
   - Reejecuta el script hasta obtener `[OK] 0 comentarios redundantes`.
3. **Cierre de Bitácora**:
   - Actualiza la bitácora en `automanagement_docs/dev-records/DEV-RECORD-HU-XXX.md` indicando 0 comentarios encontrados y los resultados de las pruebas unitarias/integración.
   - Cambia el estado de la HU y del Refinamiento a `[Finalizado]`.
