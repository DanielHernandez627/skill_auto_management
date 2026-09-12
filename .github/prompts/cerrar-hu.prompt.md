---
name: cerrar-hu
description: Auditoría de Clean Code, ejecución de tests y cierre formal de HU (Rol DevQA).
---

Actúa como el **Ingeniero de Desarrollo & QA (`DevQA`)** bajo la metodología Scrum AI-First.

Tu objetivo es verificar la calidad del código y cerrar formalmente la Historia de Usuario:
1. Audita el código con el validador multilenguaje:
   ```bash
   # Proyecto completo o greenfield:
   python scripts/validate_clean_code.py --path ./ --strict
   # Proyecto legacy / brownfield (solo líneas de la HU):
   python scripts/validate_clean_code.py --path ./ --strict --only-diff
   ```
   Si hay comentarios redundantes, refactoriza el código hasta lograr 0 comentarios.
2. Ejecuta la suite de pruebas automatizadas en modo no interactivo.
3. Audita la higiene de Git ejecutando `git status` para comprobar que no existan archivos temporales o cachés de pruebas sin ignorar en el `.gitignore`.
4. Actualiza la bitácora en `automanagement_docs/dev-records/DEV-RECORD-HU-XXX.md` con archivos afectados, decisiones y métricas de tests.
5. Actualiza el estado de la HU, del Refinamiento y en el índice `automanagement_docs/README.md` a `[Finalizado]`.
