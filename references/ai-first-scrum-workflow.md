# 🔄 Ciclo de Vida de Desarrollo AI-First (Scrum + Asistentes IA)

Este documento describe el flujo de trabajo estandarizado de **5 Fases** para la gestión e implementación de Historias de Usuario optimizado para interacción con Agentes de Inteligencia Artificial (Antigravity, Claude Code, GitHub Copilot).

---

## 👥 1. Roles y Responsabilidades

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🏛️ ROL 1: Líder Técnico / Arquitecto (TechLeadArchitect)                    │
│ - Inicialización y mantenimiento de la base de conocimiento del proyecto.    │
│ - Diseño técnico, diagramas de arquitectura en Mermaid y contratos de API.   │
│ - Entregable principal: `refinamientos/REF-XXX.md`.                         │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📋 ROL 2: Product Owner / Scrum Master (POScrum)                            │
│ - Redacción formal de la Historia de Usuario según el estándar.             │
│ - Criterios de Aceptación estructurados en formato Gherkin (Given-When-Then).│
│ - Entregable principal: `hus/HU-XXX.md`.                                    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 💻 ROL 3: Ingeniero de Desarrollo & QA (DevQA)                              │
│ - Implementación de código bajo principios de Clean Code estricto.           │
│ - Creación y ejecución de pruebas automatizadas (Coverage Gates).            │
│ - Entregable principal: Código fuente + `dev-records/DEV-RECORD-HU-XXX.md`. │
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
   - El script detecta lenguajes (.NET C#, Java, TS, Python), frameworks (Spring, Angular, React, EF Core), herramientas de build y genera la carpeta `base-conocimiento/`.
2. **Generación de la Base de Conocimiento**:
   - `01-analisis-arquitectura.md`: El Líder Técnico documenta componentes, mapa de directorios y elabora diagramas **Mermaid**.
   - `02-estandares-desarrollo.md`: Convenciones de nombrado, Clean Code y patrones vigentes en el proyecto.
   - `03-estandares-pruebas.md`: Suites existentes, comandos desatendidos y *Coverage Gates*.
   - `04-dominio-negocio.md`: Modelo conceptual, entidades principales y reglas de negocio deducidas.
3. **Establecimiento de la Línea Base**:
   - El código existente queda catalogado formalmente. A partir de este momento, el Product Owner puede redactar la primera Historia de Usuario con contexto pleno y sin ambigüedad.

---

### 🟡 Fase 1: Identificación y Redacción de la HU
1. Crear el archivo `hus/HU-XXX.md` a partir de `templates/hu-template.md` (o usando `python scripts/scaffold_hu.py HU-XXX "Título"`).
2. Redactar la descripción orientada al valor de negocio (*Como... Quiero... Para que...*).
3. Detallar escenarios de aceptación en formato Gherkin:
   - Casos felices (happy path).
   - Casos borde, excepciones y códigos de error esperados.
4. Estado inicial: `🟡 En Refinamiento`.

### 🔬 Fase 2: Refinamiento Técnico y Contratos
1. Crear el archivo `refinamientos/REF-XXX.md`.
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
3. Completar la bitácora individual en `dev-records/DEV-RECORD-HU-XXX.md`.
4. Marcar la HU y el Refinamiento como `🟢 Finalizado`.
