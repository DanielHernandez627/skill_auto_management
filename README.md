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
Diseñado para el rol de **Líder Técnico (`TechLeadArchitect`)** al aterrizar en un proyecto existente (Brownfield, productivo o sin documentar). Escanea el repositorio, detecta automáticamente el stack, genera la carpeta centralizada `automanagement_docs/` con su índice `README.md` y `base-conocimiento/`, y audita la higiene de `.gitignore` para el stack detectado:

```bash
# Escanear el directorio actual e inicializar automanagement_docs/
python scripts/onboard_project.py --path ./ --name "MiSistema"

# Ver diagnóstico sin crear archivos
python scripts/onboard_project.py --path ./ --dry-run
```

### 2. Generador de Artefactos para HUs (`scaffold_hu.py`)
Inicializa la Historia de Usuario (`automanagement_docs/hus/HU-XXX.md`) y actualiza el índice general `automanagement_docs/README.md` (el refinamiento técnico y la bitácora dev se generan bajo demanda al ejecutar `/refinar-hu` y `/cerrar-hu` respectivamente):

```bash
# Uso básico (genera HU en automanagement_docs/hus/)
python scripts/scaffold_hu.py HU-001 "Autenticación de Usuarios con JWT"

# Especificar carpeta raíz del proyecto (ej. en un subproyecto)
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
| **6. Reportar Defecto / Bug** | `POScrum` / `DevQA` | `/reportar-bug` | `/reportar-bug` | `/reportar-bug` |
| **7. Corregir Defecto y Blindaje** | `DevQA` | `/corregir-bug` | `/corregir-bug` | `/corregir-bug` |
| **8. Métricas y KPIs Locales** | Todos | `/kpis` o `/metricas` | `/kpis` | `/kpis` |

---

## 🚀 Instalación Rápida Paso a Paso (Multi-Asistente)

El instalador `install.py` configura automáticamente el entorno según el asistente que utilices (**Google Antigravity**, **Anthropic Claude Code** o **GitHub Copilot**):

### 🌟 1. Instalación Global (Google Antigravity + Claude Code)
Configura ambos asistentes de forma global en tu máquina con **un único comando**:

#### 🪟 En Windows
```bash
python install.py
```
*(O doble clic en `install.bat`)*

#### 🐧 En Linux Mint / Ubuntu / macOS
```bash
python3 install.py
```
*(O `./install.sh`)*

> [!TIP]
> **¿Qué hace la instalación global?**
> - **Google Antigravity:** Instala la skill en `%USERPROFILE%\.gemini\config\skills\agile-hu-workflow\` (o `~/.gemini/config/skills/` en Linux), habilitando los comandos en cualquier conversación (Chat o IDE).
> - **Claude Code (CLI):** Copia los comandos a `%USERPROFILE%\.claude\commands\` (o `~/.claude/commands/` en Linux) y el `CLAUDE.md`, habilitando `/onboarding`, `/nueva-hu`, etc. en cualquier terminal.

---

### 🐙 2. Configurar un Proyecto para GitHub Copilot (o Workspace Local)
Dado que **GitHub Copilot** opera a nivel de proyecto (en VS Code o JetBrains), requiere sus archivos dentro del repositorio de trabajo. Ejecuta:

```bash
# En Windows o Linux
python install.py --workspace /ruta/a/tu-proyecto
```

> [!NOTE]
> **¿Qué configura en el proyecto?**
> - **GitHub Copilot:** Copia `.github/copilot-instructions.md` y `.github/prompts/*.prompt.md` para activar los slash commands en Copilot Chat.
> - **Claude Code:** Copia `.claude/commands/` y `CLAUDE.md` localmente en el proyecto.
> - **Antigravity Local:** Copia la skill en `.agents/skills/agile-hu-workflow/`.
> - **Scripts y Plantillas:** Copia `scripts/` y `templates/` para que los asistentes ejecuten la auditoría y scaffolding desde la raíz del repositorio.

---

### 🖐️ 3. Instalación Manual (Sin scripts de Python)

- **Para Google Antigravity (Global):**
  - **Windows (PowerShell):**
    ```powershell
    $dest = "$env:USERPROFILE\.gemini\config\skills\agile-hu-workflow"; New-Item -ItemType Directory -Force -Path $dest; Copy-Item -Path ".\*" -Destination $dest -Recurse -Force
    ```
  - **Linux / macOS (Bash):**
    ```bash
    mkdir -p ~/.gemini/config/skills/agile-hu-workflow && cp -r ./* ~/.gemini/config/skills/agile-hu-workflow/
    ```

- **Para Claude Code (Global):**
  - **Windows (PowerShell):**
    ```powershell
    $dest = "$env:USERPROFILE\.claude\commands"; New-Item -ItemType Directory -Force -Path $dest; Copy-Item -Path ".\.claude\commands\*" -Destination $dest -Force
    ```
  - **Linux / macOS (Bash):**
    ```bash
    mkdir -p ~/.claude/commands && cp -r ./.claude/commands/* ~/.claude/commands/
    ```

- **Para GitHub Copilot (En tu proyecto):**
  - Copia la carpeta `.github/` de este repositorio dentro de la raíz de tu proyecto.

---

### ✅ Verificación de Instalación
- **En Antigravity (Chat o IDE):** Escribe `/onboarding` o `/nueva-hu HU-001`.
- **En Claude Code CLI:** Abre la consola en cualquier carpeta y escribe `/onboarding`.
- **En GitHub Copilot (VS Code):** Abre Copilot Chat y escribe `/onboarding` o `/nueva-hu`.

