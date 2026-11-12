# Guía Operativa para Claude (Claude Code / Claude Desktop)

Este repositorio contiene la metodología, plantillas y herramientas de automatización para la gestión de Historias de Usuario (Scrum AI-First) y desarrollo con Clean Code.

---

### 1. Directrices Principales de Desarrollo

1. **Clean Code Estricto (Multilenguaje)**:
   - Todo código escrito (.NET C#, Java Spring, TypeScript/Node/Angular/React, Go, Rust, PHP, Python, etc.) debe ser **100% auto-descriptivo**.
   - **Prohibido agregar comentarios redundantes o explicativos** dentro de clases y funciones.
   - **Cero Números Mágicos ni Strings Mágicos (`No Magic Numbers / Magic Strings`)**: Todo literal numérico, umbral, tasa, código de estado o configuración debe declararse en constantes con nombre semántico (`UPPER_SNAKE_CASE`, `const`, `readonly`) o `Enum`.
   - Si una lógica parece compleja, refactoriza en métodos auxiliares con nombres expresivos en lugar de comentarla.
   - Consulta `references/clean-code-rules.md`.

2. **Flujo de Trabajo (Greenfield `/iniciarproyecto`, Fase 0 Onboarding + HUs)**:
   - **En proyectos nuevos o pruebas técnicas (`/iniciarproyecto`)**: **PROHIBIDO escribir el código de toda la solución de golpe** aunque el usuario adjunte un PDF o enunciado completo de requerimientos. Primero se debe: (a) preguntar y confirmar los estándares de código y pruebas (Cero Números Mágicos, 0 comentarios, Patrón AAA y Data Builder), (b) extraer y proponer el desglose del documento/PDF en un **Backlog de Historias de Usuario separadas (`HU-001`, `HU-002`, ...)**, y (c) crear primero `automanagement_docs/base-conocimiento/` y `automanagement_docs/README.md` para implementar las HUs **una por una**.
   - **En proyectos existentes sin HUs**: Iniciar como `TechLeadArchitect` ejecutando `python scripts/onboard_project.py` para construir la carpeta central `automanagement_docs/` con su índice `README.md` y `base-conocimiento/` antes de escribir código.
   - **Para cada nueva funcionalidad**: Generar los documentos enlazados dentro de `automanagement_docs/`:
     - `automanagement_docs/hus/HU-XXX.md` (Criterios de aceptación en formato Gherkin).
     - `automanagement_docs/refinamientos/REF-XXX.md` (Diagramas Mermaid y contratos API en el lenguaje nativo).
     - `automanagement_docs/dev-records/DEV-RECORD-HU-XXX.md` (Bitácora de cambios y cobertura de tests).
     - `automanagement_docs/README.md` (Tabla central de seguimiento sincronizada).

3. **Pruebas, Patrón AAA, Data Builders y Cobertura (Coverage Gates)**:
   - Backend >= 80% | Frontend >= 85%.
   - **Patrón AAA (`Arrange - Act - Assert`) y `Data Builder` Obligatorios**: Desde el primer test generado, estructurar todas las pruebas en 3 bloques visuales limpios (`Arrange`, `Act`, `Assert` separados por líneas en blanco, sin comentarios) y emplear **Data Builders** para instanciar entidades o DTOs de prueba ($\ge 3$ propiedades o reutilizados en varios tests).
   - Siempre invocar comandos de build y testing con flags desatendidos / no interactivos (ver `references/testing-standards.md`).

4. **Integridad de Plantillas Preexistentes**:
   - Si el proyecto consume o genera archivos desde plantillas (documentos Word/Excel/PDF, correos HTML, archivos planos TXT/CSV), auditar sus variables reales y mapear estrictamente a ellas sin asumir cambios de esquema ni alterar archivos binarios sin autorización.

5. **Higiene de Git Multilenguaje (.gitignore)**:
   - Auditar en Fase 0 y Fase 5 que el `.gitignore` del proyecto excluya carpetas de compilación (`bin/`, `obj/`, `target/`), dependencias (`node_modules/`, `.venv/`, `vendor/`), cachés de pruebas (`.pytest_cache`, `.coverage`, `TestResults/`) y artefactos temporales generados en runtime.

---

## 2. Slash Commands Nativos en Claude Code (`.claude/commands/`)

Claude Code reconoce automáticamente los siguientes atajos en el chat:
- `/iniciarproyecto`: Asume el rol `CTO / TechAdvisor` para crear proyectos desde cero (greenfield), calibrando el perfil (técnico/no técnico), chequeando el entorno y generando la base de conocimiento.
- `/onboarding`: Asume el rol `TechLeadArchitect` y ejecuta `onboard_project.py` para levantar `automanagement_docs/base-conocimiento/`.
- `/nueva-hu`: Asume el rol `POScrum`, permite pegar información de Azure DevOps/Jira, ejecuta `scaffold_hu.py` y redacta los escenarios Gherkin en `automanagement_docs/hus/`.
- `/refinar-hu`: Asume el rol `TechLeadArchitect`, modela flujo Mermaid y define contratos DTO en `automanagement_docs/refinamientos/REF-XXX.md`.
- `/desarrollar-hu`: Asume el rol `DevQA` y programa la funcionalidad en Backend/Frontend con Clean Code estricto (0 comentarios inline).
- `/cerrar-hu`: Asume el rol `DevQA`, ejecuta `validate_clean_code.py` (con `--only-diff` en proyectos legacy), corre pruebas, actualiza bitácora en `automanagement_docs/dev-records/` y marca `[Finalizado]`.
- `/reportar-bug`: Registra un defecto formal en `automanagement_docs/bugs/` con regla anti-alucinación estricta.
- `/corregir-bug`: Asume el rol `DevQA`, realiza RCA, crea prueba de regresión obligatoria y cierra el bug en `[Resuelto]`.
- `/kpis` (o `/metricas`): Ejecuta `show_metrics.py` y presenta el dashboard en local sin consumo de tokens de IA.
- `/chat-hu`: Asume el rol de Especialista 360° para consultar, auditar y explicar cualquier HU leyendo su tríada documental en `automanagement_docs/`.
- `/auditar-clean-code`: Alias directo para validar ausencia de comentarios con `validate_clean_code.py`.

---

## 3. Comandos de Utilidad CLI

Todos los scripts admiten indistintamente `--path` o `--target-dir` (`-p` / `-t`):

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
  # Proyecto completo:
  python scripts/validate_clean_code.py --path ./src --strict

  # Proyecto legacy / brownfield (audita solo líneas modificadas en la HU):
  python scripts/validate_clean_code.py --path ./src --strict --only-diff

  # Escanear extensiones específicas (ej. solo C# o TypeScript):
  python scripts/validate_clean_code.py --path ./src --ext .cs .ts
  ```

---

## 4. Estructura de Referencias

- `templates/`: Plantillas oficiales Markdown (`hu-template.md`, `refinamiento-template.md`, `dev-record-template.md`).
- `references/`: Guías profundas (`ai-first-scrum-workflow.md`, `clean-code-rules.md`, `testing-standards.md`).
- `scripts/`: Herramientas de automatización en Python.
