# 🤖 Skill Auto Management: Metodología AI-First Multi-Asistente

Repositorio centralizado que implementa una metodología ágil (Scrum AI-First) y herramientas de automatización en Python para la gestión de **Historias de Usuario (HUs)**, diseño técnico por contratos, pruebas automatizadas y estándares estrictos de **Clean Code** sin comentarios redundantes.

Diseñado bajo la filosofía **Single Source of Truth**, es compatible de forma nativa e inmediata con:
- **Google Antigravity** (vía `SKILL.md`).
- **Anthropic Claude Code / Claude Desktop** (vía `CLAUDE.md`).
- **GitHub Copilot** (vía `.github/copilot-instructions.md`).

---

## 📁 Estructura del Repositorio

```text
skill_auto_management/
├── .gitignore                          # Exclusiones para Python, C#/.NET, Java, Node e IDEs
├── README.md                           # Documentación principal del repositorio
├── SKILL.md                            # Entrada nativa para Antigravity (YAML frontmatter)
├── CLAUDE.md                           # Directivas operativas para Claude Code / Claude CLI
├── .github/
│   └── copilot-instructions.md         # Instrucciones de workspace para GitHub Copilot
├── templates/                          # 📋 Plantillas estandarizadas en Markdown
│   ├── base-conocimiento/              # Plantillas para Onboarding Técnico (Fase 0)
│   │   ├── 01-analisis-arquitectura-template.md
│   │   ├── 02-estandares-desarrollo-template.md
│   │   ├── 03-estandares-pruebas-template.md
│   │   └── 04-dominio-negocio-template.md
│   ├── hu-template.md                  # Plantilla de HU (metadatos, DoD y Gherkin)
│   ├── refinamiento-template.md        # Plantilla de refinamiento con diagramas Mermaid y contratos
│   └── dev-record-template.md          # Plantilla para bitácora individual de cambios por HU
├── references/                         # 📚 Guías metodológicas y estándares
│   ├── ai-first-scrum-workflow.md      # Flujo de trabajo en Fase 0 + 5 fases y roles
│   ├── clean-code-rules.md             # Guía de código auto-descriptivo (C#, Java, TS, Python)
│   └── testing-standards.md            # Coverage gates (80%-85%) y comandos no interactivos
└── scripts/                            # ⚡ Scripts de automatización en Python (CLI)
    ├── __init__.py
    ├── onboard_project.py              # Onboarding técnico de proyectos existentes (Fase 0)
    ├── scaffold_hu.py                  # Generador interactivo de HU + Refinamiento + Bitácora
    └── validate_clean_code.py          # Auditor de código limpio multilenguaje (C#, Java, TS, etc.)
```

---

## 🌐 Compatibilidad Multilenguaje

La metodología y los scripts de validación están preparados para proyectos en cualquier stack:
- **C# / .NET** (`.cs`)
- **Java / Spring Boot** (`.java`)
- **TypeScript / JavaScript** (`.ts`, `.tsx`, `.js`, `.jsx`)
- **Python** (`.py`)
- **Go** (`.go`), **Rust** (`.rs`), **C/C++** (`.c`, `.cpp`), **Kotlin** (`.kt`), **Swift** (`.swift`), etc.

---

## 🛠 Herramientas de Automatización en Python

Los scripts utilizan exclusivamente la **biblioteca estándar de Python** (sin dependencias externas obligatorias).

### 1. Asistente de Onboarding Técnico (`onboard_project.py`)
Diseñado para el rol de **Líder Técnico (`TechLeadArchitect`)** al aterrizar en un proyecto existente (Brownfield, productivo o sin documentar). Escanea el repositorio, detecta automáticamente el stack y genera la carpeta `base-conocimiento/`:

```bash
# Escanear el directorio actual e inicializar base-conocimiento/
python scripts/onboard_project.py --path ./ --name "MiSistema"

# Ver diagnóstico sin crear archivos
python scripts/onboard_project.py --path ./ --dry-run
```

### 2. Generador de Artefactos para HUs (`scaffold_hu.py`)
Crea en un solo paso la tríada de documentos requerida (`hus/HU-XXX.md`, `refinamientos/REF-XXX.md` y `dev-records/DEV-RECORD-HU-XXX.md`) con IDs, fechas y enlaces enlazados:

```bash
# Uso básico
python scripts/scaffold_hu.py HU-001 "Autenticación de Usuarios con JWT"

# Especificar carpeta de destino (ej. en un subproyecto)
python scripts/scaffold_hu.py HU-001 "Autenticación" --target-dir ../mi-proyecto
```

### 3. Auditor de Clean Code (`validate_clean_code.py`)
Analiza los archivos fuente para garantizar la ausencia de comentarios explicativos redundantes antes de cerrar una HU:

```bash
# Escanear el directorio actual
python scripts/validate_clean_code.py

# Escanear una carpeta específica
python scripts/validate_clean_code.py --path ./src

# Filtrar únicamente archivos C# (.cs) o TypeScript (.ts)
python scripts/validate_clean_code.py --path ./src --ext .cs .ts

# Modo estricto para pipelines de integración continua (CI)
python scripts/validate_clean_code.py --path ./src --strict
```

*Nota: El validador ignora automáticamente carpetas de compilación y dependencias como `bin/`, `obj/`, `node_modules/`, `target/`, `dist/`, `.venv/`, etc.*

---

## ⚡ Slash Commands y Atajos Rápidos por Asistente

Para una experiencia óptima de desarrollo (DX), el repositorio incluye atajos nativos en cada plataforma:

| Acción Deseada | Rol Scrum | Antigravity | Claude Code (`.claude/commands/`) | GitHub Copilot (`.github/prompts/`) |
|---|---|---|---|---|
| **1. Onboarding Técnico (Fase 0)** | `TechLeadArchitect` | `/onboarding` | `/onboarding` | `/onboarding` |
| **2. Nueva Historia de Usuario (Fase 1)** | `POScrum` | `/nueva-hu` | `/nueva-hu` | `/nueva-hu` |
| **3. Refinamiento y Contratos (Fase 2)** | `TechLeadArchitect` | `/refinar-hu` | `/refinar-hu` | `/refinar-hu` |
| **4. Desarrollo Clean Code (Fase 4)** | `DevQA` | `/desarrollar-hu` | `/desarrollar-hu` | `/desarrollar-hu` |
| **5. Cierre, Tests y Bitácora (Fase 5)** | `DevQA` | `/cerrar-hu` | `/cerrar-hu` | `/cerrar-hu` |

---

## 🔄 Integración con Asistentes de IA

### 🤖 Google Antigravity
Copia o enlaza este repositorio dentro del proyecto en `.agents/skills/skill_auto_management/` o úsalo directamente como workspace. Antigravity detectará `SKILL.md` y activará el flujo de Fase 0 a Fase 5 cuando invoques los comandos o menciones los roles.

### 🧠 Anthropic Claude (Claude Code / Desktop)
Claude Code detecta automáticamente `CLAUDE.md` y los comandos en `.claude/commands/`. Solo escribe `/onboarding`, `/nueva-hu` o `/auditar-clean-code` en la consola.

### 🐙 GitHub Copilot
VS Code y GitHub Copilot consumen `.github/copilot-instructions.md` y los prompts reusables en `.github/prompts/`. Puedes invocar los roles directamente en la ventana de Copilot Chat.

