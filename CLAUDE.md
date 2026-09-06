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
   - **En proyectos existentes sin HUs**: Iniciar como `TechLeadArchitect` ejecutando `python scripts/onboard_project.py` para construir la `base-conocimiento/` antes de escribir código.
   - **Para cada nueva funcionalidad**: Generar la tríada de documentos:
     - `hus/HU-XXX.md` (Criterios de aceptación en formato Gherkin).
     - `refinamientos/REF-XXX.md` (Diagramas Mermaid y contratos API).
     - `dev-records/DEV-RECORD-HU-XXX.md` (Bitácora de cambios y cobertura de tests).

3. **Pruebas y Cobertura (Coverage Gates)**:
   - Backend $\ge 80\%$ | Frontend $\ge 85\%$.
   - Siempre invocar comandos de build y testing con flags desatendidos / no interactivos (ver `references/testing-standards.md`).

---

## 🛠 Comandos de Utilidad en Python

- **Onboarding de un proyecto existente (Fase 0: TechLeadArchitect)**:
  ```bash
  python scripts/onboard_project.py --path ./ --name "NombreDelProyecto"
  ```

- **Crear una nueva HU con su refinamiento y bitácora**:
  ```bash
  python scripts/scaffold_hu.py HU-XXX "Título de la Historia"
  ```

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
