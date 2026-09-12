# GitHub Copilot Instructions - Scrum AI-First & Clean Code

Este repositorio define los estándares y herramientas de desarrollo para el trabajo asistido por IA. Al interactuar con el código de este proyecto o proyectos asociados, debes seguir estrictamente estas directrices:

---

## 1. Reglas de Código (Clean Code Multilenguaje Mandatorio)
- **Cero comentarios inline/explicativos**: Escribe código en C# (.cs), Java (.java), TypeScript (.ts), Go (.go), Rust (.rs), PHP (.php), Python (.py) u otros lenguajes que se auto-explique mediante nombres claros de variables, métodos e interfaces.
- **No generes comentarios que describan lo evidente** (ej. evitar `// llama al servicio`, `// constructor`, `// valida si es nulo`).
- Divide métodos extensos en funciones pequeñas y cohesivas con nombres expresivos en vez de agregar comentarios.
- Puedes consultar ejemplos en `references/clean-code-rules.md`.

---

## 2. Metodología: Onboarding (Fase 0) e Historias de Usuario (HUs)
- **Proyectos sin HUs o existentes**: Si el proyecto tiene código productivo o preexistente sin documentar, asume el rol de Líder Técnico y sugiere o ejecuta:
  ```bash
  python scripts/onboard_project.py --path <ruta_al_proyecto> --name "NombreDelSistema"
  ```
  *(Acepta `--path` o `--target-dir` y detecta automáticamente subdirectorios con `.git` o descriptores de stack).*
- **Nuevas Funcionalidades**: Todo desarrollo parte de una Historia de Usuario especificada en `automanagement_docs/hus/HU-XXX.md`, su respectivo análisis en `automanagement_docs/refinamientos/REF-XXX.md` y el registro en `automanagement_docs/README.md`.
- Puedes crear automáticamente la estructura de una nueva HU ejecutando:
  ```bash
  python scripts/scaffold_hu.py HU-XXX "Título Descriptivo"
  ```
- Los criterios de aceptación deben formularse y respetarse en formato Gherkin (*Dado/Cuando/Entonces*).
- Antes de dar por cerrada una tarea, audita el código fuente con:
  ```bash
  # Proyecto completo:
  python scripts/validate_clean_code.py --path <ruta_al_codigo> --strict
  # Proyectos legacy / brownfield:
  python scripts/validate_clean_code.py --path <ruta_al_codigo> --strict --only-diff
  ```

---

## 3. Pruebas y Comandos No Interactivos
- Redacta pruebas que cubran los escenarios felices y casos de borde.
- Cumple con los umbrales mínimos de cobertura: Backend $\ge 80\%$, Frontend $\ge 85\%$.
- En tus sugerencias de comandos de terminal, usa siempre parámetros no interactivos (`--no-watch`, `--no-restore`, `--no-daemon`).

---

## 4. Prompts Reusables en VS Code (`.github/prompts/`)
Puedes invocar directamente estos roles en el chat de Copilot:
- `/onboarding`: Activa `onboarding.prompt.md` (Líder Técnico - Fase 0).
- `/nueva-hu`: Activa `nueva-hu.prompt.md` (Product Owner - Fase 1, acepta Azure/Jira).
- `/refinar-hu`: Activa `refinar-hu.prompt.md` (Líder Técnico - Fase 2, contratos y Mermaid).
- `/desarrollar-hu`: Activa `desarrollar-hu.prompt.md` (DevQA - Fase 4, codificación Clean Code).
- `/cerrar-hu`: Activa `cerrar-hu.prompt.md` (DevQA - Fase 5, validación y bitácora).
- `/auditar-clean-code`: Activa `auditar-clean-code.prompt.md` (DevQA - linter de comentarios).

