# 🔄 Ciclo de Vida de Desarrollo AI-First (Scrum + Asistentes IA)

Este documento describe el flujo de trabajo estandarizado de **5 Fases** para la gestión e implementación de Historias de Usuario optimizado para interacción con Agentes de Inteligencia Artificial (Antigravity, Claude Code, GitHub Copilot).

---

## 👥 1. Roles y Responsabilidades

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🏛️ ROL 1: Líder Técnico / Arquitecto (TechLeadArchitect)                    │
│ - Inicialización y mantenimiento de la base de conocimiento del proyecto.    │
│ - Diseño técnico, diagramas de arquitectura en Mermaid y contratos de API.   │
│ - Entregable principal: `automanagement_docs/refinamientos/REF-XXX.md`.      │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📋 ROL 2: Product Owner / Scrum Master (POScrum)                            │
│ - Redacción formal de la Historia de Usuario según el estándar.             │
│ - Criterios de Aceptación estructurados en formato Gherkin (Given-When-Then).│
│ - Entregable principal: `automanagement_docs/hus/HU-XXX.md`.                 │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 💻 ROL 3: Ingeniero de Desarrollo & QA (DevQA)                              │
│ - Implementación de código bajo principios de Clean Code estricto.           │
│ - Creación y ejecución de pruebas automatizadas (Coverage Gates).            │
│ - Entregable principal: Código + `automanagement_docs/dev-records/`.        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔁 2. El Ciclo de Vida: Fase 0 + 5 Fases de Desarrollo

### 🏛️ Fase 0: Onboarding Técnico & Descubrimiento de Arquitectura (TechLeadArchitect)
*Aplica al iniciar un proyecto existente (Brownfield / legacy / productivo) o al arrancar un nuevo repositorio.*

1. **Escaneo del Repositorio y Detección de Stack**:
   - Ejecutar la herramienta de onboarding:
     ```bash
     python scripts/onboard_project.py --path <ruta_al_proyecto> --name "NombreDelProyecto"
     ```
   - El script detecta lenguajes (.NET C#, Java, TS, Python), frameworks (Spring, Angular, React, EF Core), herramientas de build y genera la carpeta central `automanagement_docs/` con su índice `README.md` y `base-conocimiento/`.
2. **Generación de la Base de Conocimiento (`automanagement_docs/base-conocimiento/`)**:
   - `01-analisis-arquitectura.md`: El Líder Técnico documenta componentes, mapa de directorios y elabora diagramas **Mermaid**.
   - `02-estandares-desarrollo.md`: Convenciones de nombrado, Clean Code y patrones vigentes en el proyecto.
   - `03-estandares-pruebas.md`: Suites existentes, comandos desatendidos y *Coverage Gates*.
   - `04-dominio-negocio.md`: Modelo conceptual, entidades principales y reglas de negocio deducidas.
3. **Establecimiento de la Línea Base**:
   - El código existente queda catalogado formalmente en `automanagement_docs/`. A partir de este momento, el Product Owner puede redactar la primera Historia de Usuario con contexto pleno y sin ambigüedad.

---

### 🟡 Fase 1: Identificación y Redacción de la HU (Rol: POScrum)
1. **Captura de Requerimientos & Regla Anti-Alucinación**:
   - **Prohibido inventar funcionalidades**: Si el usuario invoca `/nueva-hu` o `/nueva-hu [ID]` sin descripción o contexto, el PO no debe inventar la historia. Debe detenerse y realizar preguntas directas sobre el enfoque, actor principal y criterios esperados (o solicitar el texto copiado de Azure DevOps / Jira).
2. **Generación con Scaffolding**:
   - Con la información confirmada, ejecutar `python scripts/scaffold_hu.py HU-XXX "Título Confirmado"` para generar los 3 documentos enlazados.
3. **Estructura Formal y Gherkin**:
   - Redactar la descripción orientada al valor de negocio (*Como... Quiero... Para que...*).
   - Detallar escenarios de aceptación en formato **Gherkin**:
     - Casos felices (*Dado... Cuando... Entonces...*).
     - Casos borde, validaciones y códigos de error esperados.
4. **Estado Inicial**: Marcar como `🟡 En Refinamiento`.

### 🔬 Fase 2: Refinamiento Técnico y Contratos
1. Completar el archivo `automanagement_docs/refinamientos/REF-XXX.md`.
2. Modelar el flujo de datos y secuencia de interacción mediante diagramas **Mermaid**.
3. Definir contratos de interfaz y DTOs (Request / Response) antes de escribir código.
4. **Auditoría de Persistencia DDL vs ORM**:
   - Validar restricciones de nulidad (`NOT NULL`), tipos de datos y llaves foráneas.
   - Establecer ordenamiento explícito para listas y colecciones hijas (ej. `@OrderBy` en Java/JPA o `.OrderBy()` en C#/.NET).
5. Actualizar estado a `🟢 Aprobado para Desarrollo`.

### 📐 Fase 3: Plan de Implementación (Planning Mode)
1. Para cambios que involucren múltiples capas, bases de datos o modificaciones arquitectónicas, generar un plan de implementación explícito (`implementation_plan.md`).
2. Desglosar componentes modificados y creados.
3. Presentar el plan para validación y aprobación humana antes de modificar código fuente.

### 💻 Fase 4: Ejecución Clean Code Multilenguaje
1. Escribir código que exprese claramente su propósito mediante nombres precisos y funciones pequeñas de responsabilidad única.
2. **Cero comentarios redundantes o explicativos** dentro del cuerpo de clases y métodos (C#, Java, TypeScript, Python, etc.).
3. Desacoplar UI en capas independientes (HTML/SCSS/TS o Razor/CSS/C#).
4. No utilizar cuadros de diálogo nativos bloqueantes (`alert()`, `confirm()`); emplear servicios de componentes de notificación o modales accesibles.

### 🧪 Fase 5: Cierre, Verificación y Bitácora
1. Ejecutar las suites de pruebas automatizadas usando banderas no interactivas:
   - .NET / C#: `dotnet test --no-restore --verbosity normal`
   - Java / Spring: `mvn test` o `./gradlew test --no-daemon`
   - Frontend / Node: `npm test -- --watch=false --browsers=ChromeHeadless`
   - Python: `pytest --maxfail=1 -v`
2. Ejecutar la auditoría de código limpio:
   ```bash
   python scripts/validate_clean_code.py --path ./src
   ```
3. Completar la bitácora individual en `automanagement_docs/dev-records/DEV-RECORD-HU-XXX.md`.
4. Marcar la HU, el Refinamiento y la tabla en `automanagement_docs/README.md` como `🟢 Finalizado`.
