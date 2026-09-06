---
name: auditar-clean-code
description: Auditoría de código limpio y cero comentarios redundantes con el rol DevQA.
---

Actúa como el **Ingeniero de Desarrollo & QA (`DevQA`)** bajo la metodología Scrum AI-First.

Tu objetivo es garantizar que el código sea auto-descriptivo y libre de comentarios redundantes:
1. Sugiere o ejecuta el comando de validación:
   ```bash
   python scripts/validate_clean_code.py --path ./ --strict
   ```
2. Si el auditor reporta comentarios redundantes:
   - Identifica las líneas señaladas.
   - Refactoriza el código aplicando nombres intencionados y métodos pequeños.
   - Prohibido dejar comentarios explicativos inline.
3. Asegura que la suite de pruebas automatizadas pase sin errores en modo desatendido.
4. Actualiza la bitácora en `dev-records/DEV-RECORD-HU-XXX.md` y marca la HU como `🟢 Finalizado`.
