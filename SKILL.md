---
name: agile-hu-workflow
description: Metodología AI-First para onboarding técnico de proyectos existentes (Fase 0), especificación, refinamiento, desarrollo, QA, gestión de bugs, consulta/chat de HUs y métricas de calidad de Historias de Usuario con Clean Code y documentación centralizada en automanagement_docs/. Activa esta skill obligatoriamente cuando el usuario ejecute /onboarding, /nueva-hu, /refinar-hu, /desarrollar-hu, /cerrar-hu, /reportar-bug, /corregir-bug, /kpis, /chat-hu, o mencione roles como Líder Técnico (TechLeadArchitect), Product Owner (POScrum) o DevQA.
---

# Metodología AI-First para Historias de Usuario

Esta skill guía a los Agentes de IA en el ciclo de vida de desarrollo de software ágil bajo política **AI-First**, garantizando código auto-descriptivo sin comentarios redundantes, pruebas automatizadas y documentación sincronizada en `automanagement_docs/`.

---

## Cuándo Activar esta Skill

Activa esta skill cuando el usuario solicite:
- Onboarding de un proyecto existente (Brownfield / legacy / productivo) o inicialización de arquitectura.
- Iniciar, refinar o implementar una Historia de Usuario (HU).
- Reportar o corregir un defecto o bug con pruebas de regresión automáticas.
- Consultar, auditar o conversar sobre una Historia de Usuario existente (`/chat-hu`).
- Consultar el tablero de métricas y KPIs locales (`/kpis`).
- Crear especificaciones técnicas, contratos REST o diagramas Mermaid.
- Refactorizar o auditar código bajo Clean Code estricto (0 comentarios inline/bloques explicativos).
- Diseñar y ejecutar suites de pruebas automatizadas con Coverage Gates (Backend >= 80%, Frontend >= 85%).

---

## Slash Commands y Roles

| Comando | Rol Activado | Fase / Ámbito | Acción Ejecutada |
|---|---|---|---|
| `/onboarding` o `/lider-tecnico` | `TechLeadArchitect` | Fase 0 | Escaneo del stack con `onboard_project.py` y generación de `automanagement_docs/base-conocimiento/`. |
| `/nueva-hu` o `/po-scrum` | `POScrum` | Fase 1 | Captura requerimientos con **Regla Anti-Alucinación estricta**. |
| `/refinar-hu` | `TechLeadArchitect` | Fase 2 | Modela flujo Mermaid, define DTOs/contratos y valida persistencia en `automanagement_docs/refinamientos/REF-XXX.md`. |
| `/desarrollar-hu` | `DevQA` | Fase 4 | Implementa código bajo Clean Code estricto (**cero comentarios explicativos**). |
| `/cerrar-hu` o `/auditar-clean-code` | `DevQA` | Fase 5 | Audita comentarios con `validate_clean_code.py`, ejecuta tests desatendidos, genera bitácora y marca `[Finalizado]`. |
| `/reportar-bug` | `POScrum` / `DevQA` | Calidad QA | Registra formalmente un defecto con **Regla Anti-Alucinación** en `automanagement_docs/bugs/`. |
| `/corregir-bug` | `DevQA` | Calidad QA | Diagnostica RCA, crea prueba de regresión obligatoria, corrige con Clean Code y marca `[Resuelto]`. |
| `/kpis` o `/metricas` | Todos | Monitoreo | Ejecuta `show_metrics.py` y muestra el dashboard en 0.02s con **cero consumo de tokens IA**. |
| `/chat-hu` | Especialista 360° | Auditoría | Consulta, audita y explica una HU leyendo quirúrgicamente su tríada documental en `automanagement_docs/`. |

---

## Protocolo Operativo

```mermaid
graph TD
    F0[Fase 0: Onboarding en automanagement_docs/base-conocimiento/] --> F1[Fase 1: Redaccion HU en automanagement_docs/hus/]
    F1 --> F2[Fase 2: Refinamiento en automanagement_docs/refinamientos/]
    F2 --> F3[Fase 3: Plan de Implementacion / Planning Mode]
    F3 --> F4[Fase 4: Ejecucion Clean Code sin comentarios]
    F4 --> F5[Fase 5: Cierre, Tests, validate_clean_code.py y Bitacora]
```

### Fase 0: Onboarding Técnico & Descubrimiento (Rol: TechLeadArchitect)
- **Ejecución del Escaneo**:
  ```bash
  python scripts/onboard_project.py --path <ruta_proporcionada_por_usuario> --name "NombreDelSistema"
  ```
- **Regla de Oro de Ruta y No Duplicación**:
  - Usa `--path` con la ruta raíz indicada por el usuario (o `./`). Nunca apuntes a subcarpetas internas de código.
  - `automanagement_docs/` reside exclusivamente en la raíz del espacio de trabajo. Prohibido duplicar, sincronizar o crear uniones simbólicas.
- Documentar en `automanagement_docs/base-conocimiento/`:
  - `01-analisis-arquitectura.md` (Diagramas Mermaid y mapa de capas).
  - `02-estandares-desarrollo.md` (Convenciones y Clean Code).
  - `03-estandares-pruebas.md` (Coverage gates y comandos headless).
  - `04-dominio-negocio.md` (Entidades y reglas del negocio).
- Genera `automanagement_docs/README.md` con la tabla de seguimiento. Audita higiene de Git (`.gitignore`).

### Fase 1: Identificación y Redacción de la HU (Rol: POScrum)

> [!CAUTION]
> **[REGLA ANTI-ALUCINACIÓN ESTRICTA]**:
> Si el usuario ejecuta `/nueva-hu` o `/nueva-hu [ID]` **sin adjuntar una descripción o requerimiento**, el agente **TIENE PROHIBIDO INVENTAR O ASUMIR** la historia.
> Detenerse inmediatamente y solicitar:
> 1. Objetivo de la funcionalidad (o tarea de Azure DevOps / Jira).
> 2. Rol o actor principal (*Como...*).
> 3. Criterios de aceptación o reglas de negocio clave.

- **Flujo**:
  1. Con la información confirmada, ejecutar:
     ```bash
     python scripts/scaffold_hu.py HU-XXX "Título de la Historia"
     ```
  2. Editar `automanagement_docs/hus/HU-XXX.md` estructurando criterios de aceptación en formato **Gherkin** (*Dado / Cuando / Entonces*).
  3. Asignar estado `[En Refinamiento]`. Invitar a continuar con `/refinar-hu HU-XXX`.

### Fase 2: Refinamiento Técnico & Contratos (Rol: TechLeadArchitect)
- Crear `automanagement_docs/refinamientos/REF-XXX.md` adaptado a la arquitectura real (Desktop GUI, Web API, CLI, Microservicio):
  - **Diagrama Mermaid**: Modela el flujo real de interacción.
  - **Modelos y Contratos**: Clases/DTOs en el lenguaje nativo del proyecto.
  - **Integridad de Plantillas**: Si consume plantillas binarias (`.docx`/`.xlsx`/`.pdf`), vistas (`.html`/`.mjml`) o planas (`.txt`/`.csv`), auditar marcadores y variables existentes. Prohibido asumir cambios en la estructura de plantillas sin aprobación.
  - **Casos Borde y Validaciones**: Manejo controlado de excepciones.
  - **Checklist Técnico**: Tareas ordenadas para desarrollo.
- Actualizar estado a `[Aprobado para Desarrollo]` en `HU-XXX.md` y `automanagement_docs/README.md`.

### Fase 3: Plan de Implementación (Planning Mode)
- Generar `implementation_plan.md` si la HU involucra múltiples capas o cambios en persistencia. Solicitar aprobación antes de modificar código.

### Fase 4: Ejecución Clean Code Multilenguaje (Rol: DevQA)
- Implementar en el stack correspondiente (.NET C#, Java Spring, TypeScript, Python, etc.).
- **Regla Estricta Clean Code**: Cero comentarios explicativos redundantes. Código 100% auto-descriptivo.
- **Fidelidad a Plantillas**: Mapear estrictamente los datos a las plantillas preexistentes.

### Fase 5: Cierre, Verificación y Bitácora (Rol: DevQA)
- Ejecutar tests con flags desatendidos (`dotnet test --no-restore`, `mvn test`, `pytest`, `npm test -- --watch=false`).
- Superar Coverage Gates: Backend >= 80%, Frontend >= 85%.
- Auditar Clean Code: `python scripts/validate_clean_code.py --path ./src --strict`
- Verificar higiene Git (`git status`).
- Completar bitácora en `automanagement_docs/dev-records/DEV-RECORD-HU-XXX.md`.
- Actualizar HU, Refinamiento y `README.md` a `[Finalizado]`.

---

## Gestión de Defectos y Métricas de Calidad

### Reporte de Defectos (`/reportar-bug`)
- **Regla Anti-Alucinación**: Solicitar comportamiento observado vs. esperado, pasos/logs, HU asociada y severidad (`[Bloqueante]`, `[Alta]`, `[Media]`, `[Baja]`).
- Ejecutar: `python scripts/scaffold_bug.py BUG-XXX-01 "Título del Defecto" --hu HU-XXX --severity Alta`

### Corrección de Defectos (`/corregir-bug`)
- Realizar análisis RCA (archivo y línea exacta).
- **Regression Test Gate Obligatorio**: Crear prueba automatizada en `tests/` que reproduzca el fallo antes de darlo por corregido.
- Corregir con Clean Code, verificar suite completa y marcar `[Resuelto]`.

### Tablero de Métricas Locales (`/kpis`)
- Ejecuta `python scripts/show_metrics.py` en 0.02s con **0 tokens de IA** y 100% de privacidad local.

### Consulta y Chat de Historias de Usuario (`/chat-hu [HU-ID]`)
- **Soporte Flexible de IDs**: Admite formatos estándar (`HU-001`), Azure DevOps (`607340`, `US-607340`) o Jira (`PROJ-123`).
- **Carga Quirúrgica de Contexto**: Lee exclusivamente `automanagement_docs/hus/HU-XXX.md`, `refinamientos/REF-XXX.md`, `dev-records/DEV-RECORD-HU-XXX.md` y bugs asociados.
- **Inspección de Código Puntual**: Si el usuario proporciona una ruta o solicita auditar código puntual, inspecciona ese archivo específico para contrastarlo contra los requerimientos y el refinamiento de la HU.
- **Respuesta Multirrol Especializada**:
  - Responde como `POScrum` para alcance, negocio o criterios Gherkin.
  - Responde como `TechLeadArchitect` para contratos, DTOs, diagramas Mermaid o persistencia.
  - Responde como `DevQA` para archivos modificados, suites de prueba y métricas de cobertura.
- **Trazabilidad y Cero Alucinaciones**: Cita siempre el documento fuente (`[REF-XXX.md]`, `[HU-XXX.md]`) y archivo/línea de código si fue inspeccionado. Si algo no fue contemplado, lo declara abiertamente sin inventar.

---

## Recursos y Plantillas Vinculadas

- Plantilla HU: [`templates/hu-template.md`](templates/hu-template.md)
- Plantilla Bug: [`templates/bug-template.md`](templates/bug-template.md)
- Plantilla Refinamiento: [`templates/refinamiento-template.md`](templates/refinamiento-template.md)
- Plantilla Bitácora: [`templates/dev-record-template.md`](templates/dev-record-template.md)
- Reglas Clean Code: [`references/clean-code-rules.md`](references/clean-code-rules.md)
- Flujo y Roles Scrum: [`references/ai-first-scrum-workflow.md`](references/ai-first-scrum-workflow.md)
- Estándares Testing: [`references/testing-standards.md`](references/testing-standards.md)
