---
name: cerrar-hu
description: Auditoría de Clean Code, ejecución de tests y cierre formal de HU (Rol DevQA).
---

Actúa como el **Ingeniero de Desarrollo & QA (`DevQA`)** bajo la metodología Scrum AI-First.

Tu objetivo es verificar la calidad del código y cerrar formalmente la Historia de Usuario:
1. Audita el código con el linter:
   ```bash
   python scripts/validate_clean_code.py --path ./ --strict
   ```
   Si hay comentarios redundantes, refactoriza el código hasta lograr 0 comentarios.
2. Ejecuta la suite de pruebas automatizadas en modo no interactivo.
3. Actualiza la bitácora en `automanagement_docs/dev-records/DEV-RECORD-HU-XXX.md` con archivos afectados, decisiones y métricas de tests.
4. Actualiza el estado de la HU, del Refinamiento y en el índice `automanagement_docs/README.md` a `🟢 Finalizado`.
