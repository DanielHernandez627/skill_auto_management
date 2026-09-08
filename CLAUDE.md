# Guía Operativa para Claude (Claude Code / Claude Desktop)

Este repositorio contiene la metodología, plantillas y herramientas de automatización para la gestión de Historias de Usuario (Scrum AI-First) y desarrollo con Clean Code.

---

## 🎯 Directrices Principales de Desarrollo

1. **Clean Code Estricto (Multilenguaje)**:
   - Todo código escrito (C#, Java, TypeScript, Python, etc.) debe ser **100% auto-descriptivo**.
   - **Prohibido agregar comentarios redundantes o explicativos** dentro de clases y funciones.
   - Si una lógica parece compleja, refactoriza en métodos auxiliares con nombres expresivos en lugar de comentarla.
   - Consulta `references/clean-code-rules.md`.

2. **Flujo de Trabajo (Fase 0 Onboarding + HUs)**:
   - **En proyectos existentes sin HUs**: Iniciar como `TechLeadArchitect` ejecutando `python scripts/onboard_project.py` para construir la carpeta central `automanagement_docs/` con su índice `README.md` y `base-conocimiento/` antes de escribir código.
   - **Para cada nueva funcionalidad**: Generar los documentos enlazados dentro de `automanagement_docs/`:
     - `automanagement_docs/hus/HU-XXX.md` (Criterios de aceptación en formato Gherkin).
     - `automanagement_docs/refinamientos/REF-XXX.md` (Diagramas Mermaid y contratos API).
     - `automanagement_docs/dev-records/DEV-RECORD-HU-XXX.md` (Bitácora de cambios y cobertura de tests).
     - `automanagement_docs/README.md` (Tabla central de seguimiento sincronizada).

3. **Pruebas y Cobertura (Coverage Gates)**:
   - Backend $\ge 80\%$ | Frontend $\ge 85\%$.
   - Siempre invocar comandos de build y testing con flags desatendidos / no interactivos (ver `references/testing-standards.md`).

4. **Integridad de Plantillas Preexistentes**:
   - Si el proyecto consume o genera archivos desde plantillas (documentos Word/Excel/PDF, correos HTML, archivos planos TXT/CSV), auditar sus variables reales y mapear estrictamente a ellas sin asumir cambios de esquema ni alterar archivos binarios sin autorización.

5. **Higiene de Git Multilenguaje (.gitignore)**:
   - Auditar en Fase 0 y Fase 5 que el `.gitignore` del proyecto excluya carpetas de compilación (`bin/`, `obj/`, `target/`), dependencias (`node_modules/`, `.venv/`), cachés de pruebas (`.pytest_cache`, `.coverage`, `TestResults/`) y artefactos temporales generados en runtime.

---

## ⚡ Slash Commands Nativos en Claude Code (`.claude/commands/`)

Claude Code reconoce automáticamente los siguientes atajos en el chat:
- `/onboarding`: Asume el rol `TechLeadArchitect` y ejecuta `onboard_project.py` para levantar `automanagement_docs/base-conocimiento/`.
- `/nueva-hu`: Asume el rol `POScrum`, permite pegar información de Azure DevOps/Jira, ejecuta `scaffold_hu.py` y redacta los escenarios Gherkin en `automanagement_docs/hus/`.
- `/refinar-hu`: Asume el rol `TechLeadArchitect`, modela flujo Mermaid y define contratos DTO en `automanagement_docs/refinamientos/REF-XXX.md`.
- `/desarrollar-hu`: Asume el rol `DevQA` y programa la funcionalidad en Backend/Frontend con Clean Code estricto (0 comentarios inline).
- `/cerrar-hu`: Asume el rol `DevQA`, ejecuta `validate_clean_code.py`, corre pruebas, actualiza bitácora en `automanagement_docs/dev-records/` y marca `[Finalizado]`.
- `/reportar-bug`: Registra un defecto formal en `automanagement_docs/bugs/` con regla anti-alucinación estricta.
- `/corregir-bug`: Asume el rol `DevQA`, realiza RCA, crea prueba de regresión obligatoria y cierra el bug en `[Resuelto]`.
- `/kpis` (o `/metricas`): Ejecuta `show_metrics.py` y presenta el dashboard en local sin consumo de tokens de IA.
- `/auditar-clean-code`: Alias directo para validar ausencia de comentarios con `validate_clean_code.py`.

---

## 🛠 Comandos de Utilidad en Python

- **Onboarding de un proyecto existente (Fase 0: TechLeadArchitect)**:
  ```bash
  python scripts/onboard_project.py --path ./ --name "NombreDelProyecto"
  ```

- **Crear una nueva HU y registrarla en el índice**:
  ```bash
  python scripts/scaffold_hu.py HU-XXX "Título de la Historia"
  ```
  *(Nota: Genera automanagement_docs/hus/HU-XXX.md y actualiza automanagement_docs/README.md; el refinamiento y bitácora se generan en sus respectivas fases)*

- **Auditar ausencia de comentarios en código (Clean Code)**:
  ```bash
  # Escanear todo el proyecto o directorio específico
  python scripts/validate_clean_code.py --path ./src

  # Escanear extensiones específicas (ej. solo C# o TypeScript)
  python scripts/validate_clean_code.py --path ./src --ext .cs .ts

  # Validar con código de salida estricto (para integración continua)
  python scripts/validate_clean_code.py --path ./src --strict
  ```

---

## 📁 Estructura de Referencias

- `templates/`: Plantillas oficiales Markdown (`hu-template.md`, `refinamiento-template.md`, `dev-record-template.md`).
- `references/`: Guías profundas (`ai-first-scrum-workflow.md`, `clean-code-rules.md`, `testing-standards.md`).
- `scripts/`: Herramientas de automatización en Python.
