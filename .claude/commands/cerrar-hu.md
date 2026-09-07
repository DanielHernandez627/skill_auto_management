---
description: Auditoría de Clean Code, ejecución de tests y cierre formal de la HU (Fase 5 - DevQA)
---

Asume inmediatamente el rol de **Ingeniero de Desarrollo & QA (`DevQA`)**.

Tu misión es verificar rigurosamente la calidad del código, asegurar que los tests pasen y cerrar formalmente la Historia de Usuario:

1. **Auditoría de Clean Code**:
   - Ejecuta el auditor de código limpio:
     ```bash
     python scripts/validate_clean_code.py --path ./ --strict
     ```
   - Si se detecta cualquier comentario explicativo o redundante, **refactoriza inmediatamente** los archivos hasta obtener `[OK] 0 comentarios redundantes`.

2. **Ejecución de Suites de Pruebas**:
   - Ejecuta las pruebas automatizadas con banderas desatendidas (ver `references/testing-standards.md`):
     - .NET: `dotnet test --no-restore`
     - Node/Angular: `npm test -- --watch=false --browsers=ChromeHeadless`
     - Java: `mvn test`
     - Python: `pytest`
   - Valida el cumplimiento del Coverage Gate (Backend $\ge 80\%$, Frontend $\ge 85\%$).

3. **Bitácora y Definición de Hecho (DoD)**:
   - Completa el archivo `automanagement_docs/dev-records/DEV-RECORD-HU-XXX.md` detallando:
     - Archivos creados/modificados.
     - Decisiones técnicas adoptadas.
     - Cobertura alcanzada y total de pruebas pasadas (100%).
   - Actualiza el estado en `automanagement_docs/hus/HU-XXX.md` y `automanagement_docs/refinamientos/REF-XXX.md` a `🟢 Finalizado`.
   - Actualiza la tabla de seguimiento en `automanagement_docs/README.md` a `🟢 Finalizado`.
   - Confirma al usuario que la historia ha sido cerrada con éxito y cumple con la Definición de Hecho.
