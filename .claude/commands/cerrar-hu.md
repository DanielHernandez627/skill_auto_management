---
description: Auditoría de Clean Code, ejecución de tests y cierre formal de la HU (Fase 5 - DevQA)
---

Asume inmediatamente el rol de **Ingeniero de Desarrollo & QA (`DevQA`)**.

Tu misión es verificar rigurosamente la calidad del código, asegurar que los tests pasen y cerrar formalmente la Historia de Usuario:

1. **Auditoría de Clean Code (Multilenguaje)**:
   - Ejecuta el auditor de código limpio (en proyectos brownfield/legacy usa `--only-diff` para auditar solo las líneas tocadas por la HU):
     ```bash
     python scripts/validate_clean_code.py --path ./ --strict --only-diff
     ```
   - Si se detecta cualquier comentario explicativo o redundante, **refactoriza inmediatamente** los archivos hasta obtener `[OK] 0 comentarios redundantes`.

2. **Ejecución de Suites de Pruebas**:
   - Ejecuta las pruebas automatizadas con banderas desatendidas (ver `references/testing-standards.md`):
     - .NET (C#): `dotnet test --no-restore`
     - Java: `mvn clean test -DinteractiveMode=false` o `./gradlew test --no-daemon`
     - Node/Angular/React: `npm test -- --watch=false --browsers=ChromeHeadless`
     - Go: `go test -v ./...`
     - Rust: `cargo test -- --nocapture`
     - Python: `pytest` (o fallback nativo sin dependencias: `python -m unittest discover -s tests -v`)
   - Valida el cumplimiento del Coverage Gate (Backend >= 80%, Frontend >= 85%).

3. **Auditoría de Higiene Git**:
   - Ejecuta `git status` para confirmar que ningún artefacto temporal, ejecutable o caché de pruebas quede sin ignorar en el `.gitignore`.

4. **Bitácora y Definición de Hecho (DoD)**:
   - Completa el archivo `automanagement_docs/dev-records/DEV-RECORD-HU-XXX.md` detallando:
     - Archivos creados/modificados.
     - Decisiones técnicas adoptadas.
     - Cobertura alcanzada y total de pruebas pasadas (100%).
   - Actualiza el estado en `automanagement_docs/hus/HU-XXX.md` y `automanagement_docs/refinamientos/REF-XXX.md` a `[Finalizado]`.
   - Actualiza la tabla de seguimiento en `automanagement_docs/README.md` a `[Finalizado]`.
   - Confirma al usuario que la historia ha sido cerrada con éxito y cumple con la Definición de Hecho.
