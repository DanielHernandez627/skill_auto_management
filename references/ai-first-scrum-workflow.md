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
   - **Regla Estricta de Aislamiento**: La documentación debe vivir **únicamente en la raíz del espacio de trabajo**. Queda **estrictamente prohibido duplicar o copiar (`Copy-Item`, `cp -r`)** la carpeta `automanagement_docs/` dentro de directorios de código fuente (repositorios Git internos o subproyectos).
2. **Generación de la Base de Conocimiento (`automanagement_docs/base-conocimiento/`)**:
   - `01-analisis-arquitectura.md`: El Líder Técnico documenta componentes, mapa de directorios y elabora diagramas **Mermaid**.
   - `02-estandares-desarrollo.md`: Convenciones de nombrado, Clean Code y patrones vigentes en el proyecto.
   - `03-estandares-pruebas.md`: Suites existentes, comandos desatendidos y *Coverage Gates*.
   - `04-dominio-negocio.md`: Modelo conceptual, entidades principales y reglas de negocio deducidas.
3. **Auditoría de Higiene de Git (.gitignore Multilenguaje)**:
   - Verificar que el archivo `.gitignore` del proyecto ignore las carpetas de compilación (`bin/`, `obj/`, `target/`, `dist/`), paquetes/dependencias (`node_modules/`, `.venv/`), cachés de pruebas (`.pytest_cache`, `.coverage`, `TestResults/`) y artefactos temporales generados en runtime.
4. **Establecimiento de la Línea Base**:
   - El código existente queda catalogado formalmente en `automanagement_docs/`. A partir de este momento, el Product Owner puede redactar la primera Historia de Usuario con contexto pleno y sin ambigüedad.

---

### 🟡 Fase 1: Identificación y Redacción de la HU (Rol: POScrum)
1. **Captura de Requerimientos & Regla Anti-Alucinación**:
   - **Prohibido inventar funcionalidades**: Si el usuario invoca `/nueva-hu` o `/nueva-hu [ID]` sin descripción o contexto, el PO no debe inventar la historia. Debe detenerse y realizar preguntas directas sobre el enfoque, actor principal y criterios esperados (o solicitar el texto copiado de Azure DevOps / Jira).
2. **Generación con Scaffolding**:
   - Con la información confirmada, ejecutar `python scripts/scaffold_hu.py HU-XXX "Título Confirmado"` para inicializar la Historia de Usuario (`automanagement_docs/hus/HU-XXX.md`) y registrarla en el índice `automanagement_docs/README.md`. *Nota: El refinamiento y la bitácora dev se generarán bajo demanda en sus respectivas fases.*
3. **Estructura Formal y Gherkin**:
   - Redactar la descripción orientada al valor de negocio (*Como... Quiero... Para que...*).
   - Detallar escenarios de aceptación en formato **Gherkin**:
     - Casos felices (*Dado... Cuando... Entonces...*).
     - Casos borde, validaciones y códigos de error esperados.
4. **Estado Inicial**: Marcar como `🟡 En Refinamiento`.

### 🔬 Fase 2: Refinamiento Técnico y Diseño de Arquitectura (Rol: TechLeadArchitect)
1. **Generación bajo demanda del Refinamiento**:
   - Crear `automanagement_docs/refinamientos/REF-XXX.md` adaptado a la arquitectura real del proyecto (Desktop GUI, Web REST API, Microservicios o CLI). Si no existía previamente, crearlo y actualizar los enlaces en `HU-XXX.md` y `automanagement_docs/README.md`.
2. **Modelado y Arquitectura Específica por Paradigma**:
   - **Aplicaciones de Escritorio (Desktop GUI - Tkinter, WPF, Qt, Electron)**: Modelar componentes de UI (ventanas, paneles, widgets), ciclo de eventos, binding reactivo y servicios locales de sistema de archivos o base de datos local.
   - **Aplicaciones Web / API REST**: Definir contratos de interfaz, DTOs (Request / Response) y endpoints HTTP.
   - **CLI / Librerías / Procesamiento por Lotes**: Definir comandos, argumentos, contratos de entrada/salida y manejo de flujos.
   - Modelar el flujo de datos y secuencia de interacción mediante diagramas **Mermaid**.
3. **Auditoría de Persistencia / Modelo de Datos**:
   - Validar restricciones de nulidad (`NOT NULL`), tipos de datos y llaves foráneas o esquemas de archivos.
   - Establecer ordenamiento explícito para listas y colecciones hijas (ej. `@OrderBy` en Java/JPA o `.OrderBy()` en C#/.NET).
4. **Respeto e Integridad a Plantillas Preexistentes**:
   - Si la HU interactúa con plantillas predefinidas en el repositorio (documentos binarios `.docx`/`.xlsx`/`.pdf`, correos `.html`/`.mjml`, archivos planos `.txt`/`.csv` o templates Jinja/Razor/Thymeleaf), **auditar los marcadores y variables existentes**.
   - **Queda estrictamente prohibido asumir cambios de estructura en plantillas predefinidas** sin autorización explícita del usuario; el adaptador debe amoldarse al esquema esperado por la plantilla actual.
5. Actualizar estado en la HU a `[Aprobado para Desarrollo]`.

### Fase 3: Plan de Implementación (Planning Mode)
1. Para cambios que involucren múltiples capas, bases de datos o modificaciones arquitectónicas, generar un plan de implementación explícito (`implementation_plan.md`).
2. Desglosar componentes modificados y creados.
3. Presentar el plan para validación y aprobación humana antes de modificar código fuente.

### Fase 4: Ejecución Clean Code Multilenguaje
1. Escribir código que exprese claramente su propósito mediante nombres precisos y funciones pequeñas de responsabilidad única.
2. **Cero comentarios redundantes o explicativos** dentro del cuerpo de clases y métodos (C#, Java, TypeScript, Python, etc.).
3. Desacoplar UI en capas independientes (HTML/SCSS/TS o Razor/CSS/C#).
4. No utilizar cuadros de diálogo nativos bloqueantes (`alert()`, `confirm()`); emplear servicios de componentes de notificación o modales accesibles.
5. **Mapeo Fiel a Plantillas**: Al generar archivos a partir de plantillas existentes, asegurar que los diccionarios o contextos de renderizado utilicen con exactitud las variables esperadas por la plantilla.

### Fase 5: Cierre, Verificación y Bitácora
1. Ejecutar las suites de pruebas automatizadas usando banderas no interactivas:
   - .NET / C#: `dotnet test --no-restore --verbosity normal`
   - Java / Spring: `mvn test` o `./gradlew test --no-daemon`
   - Frontend / Node: `npm test -- --watch=false --browsers=ChromeHeadless`
   - Python: `pytest --maxfail=1 -v`
2. Ejecutar la auditoría de código limpio:
   ```bash
   python scripts/validate_clean_code.py --path ./src
   ```
3. **Auditoría de Higiene Git**:
   - Ejecutar `git status` para comprobar que no existan archivos temporales, binarios generados en ejecución o cachés de testing (`.pytest_cache`, `.coverage`, etc.) sin ignorar en el `.gitignore`.
4. Completar la bitácora individual en `automanagement_docs/dev-records/DEV-RECORD-HU-XXX.md`.
5. Marcar la HU, el Refinamiento y la tabla en `automanagement_docs/README.md` como `[Finalizado]`.

---

## 3. Sub-flujo de Certificación QA, Defectos e Incidentes

Aplica cuando durante la certificación en ambientes de prueba (QA/Staging) o tras el paso a producción se detecta una anomalía o discrepancia:

### Reportar un Defecto (`/reportar-bug [ID]`)
1. **Regla Estricta Anti-Alucinación**:
   - Si no se adjuntan detalles del fallo, el agente **NO debe inventar el bug**. Solicita obligatoriamente: comportamiento observado vs esperado, pasos para reproducir / logs, HU asociada y severidad.
2. **Generación de Ficha (`automanagement_docs/bugs/BUG-XXX.md`)**:
   - Ejecuta `python scripts/scaffold_bug.py BUG-XXX-01 "Título" --hu HU-XXX --severity Alta`.
   - Modela el escenario de fallo en sintaxis **Gherkin**.
   - Registra el defecto en `automanagement_docs/README.md` en la *Tabla de Defectos y Bugs*.

### Corrección y Blindaje (`/corregir-bug [ID_BUG]`)
1. **Diagnóstico RCA**: Identificar la causa raíz técnica en el código fuente.
2. **Regression Test Gate (Mandatorio)**:
   - Escribir una prueba automatizada en `tests/` que reproduzca el fallo antes del fix para blindar contra regresiones futuras.
3. **Fix Clean Code**: Modificar el código fuente con 0 comentarios redundantes.
4. **Verificación**: Correr suite de pruebas completa y auditoría de `validate_clean_code.py`.
5. **Cierre**: Actualizar la ficha del bug con RCA, archivos modificados y prueba de regresión a `[Resuelto]`.

---

## 4. Tablero de Métricas y KPIs Locales (`/kpis`)

- Al escribir `/kpis` (o `/metricas`), el asistente ejecuta de forma desatendida:
  ```bash
  python scripts/show_metrics.py
  ```
- **Cero Consumo de Tokens de IA**: El cálculo matemático, conteo de HUs, porcentaje de cobertura y estado de bugs se calcula en local mediante Python en 0.02 segundos sin gastar tokens de la ventana de contexto del LLM.
- **Privacidad Total (Zero Data Leakage)**: Los datos viven exclusivamente en el disco local (`automanagement_docs/`), sin telemetría externa.
