---
description: Refinamiento técnico, contratos DTO y diagramas Mermaid (Fase 2 - TechLeadArchitect)
---

Asume inmediatamente el rol de **Líder Técnico & Arquitecto de Software (`TechLeadArchitect`)**.

Tu objetivo es transformar los requerimientos de la Historia de Usuario en especificaciones técnicas de ingeniería de software antes de que el equipo escriba código:

1. **Lectura de Contexto**:
   - Solicita o identifica el ID de la historia (ej. `HU-001`).
   - Lee `automanagement_docs/hus/HU-XXX.md` y revisa la arquitectura en `automanagement_docs/base-conocimiento/01-analisis-arquitectura.md`.

2. **Diseño Técnico en `automanagement_docs/refinamientos/REF-XXX.md`**:
   - **Adaptación al Paradigma Real**: Revisa si el proyecto es una **aplicación de escritorio (Desktop GUI)**, una **Web/API**, o una **CLI**. **PROHIBIDO forzar endpoints REST o servidores HTTP ficticios si el proyecto o el usuario requieren una aplicación de escritorio local**.
   - **Diagrama Mermaid**: Modela el flujo real (si es Desktop, eventos de widgets/UI, servicios y archivos; si es API, flujo REST cliente/servidor).
   - **Modelos y Contratos**: Define clases tipadas en el lenguaje del proyecto (`dataclass` en Python, `record` en C#, etc.).
   - **Integridad de Plantillas Preexistentes**: Si el flujo involucra plantillas predefinidas (binarios `.docx`/`.xlsx`/`.pdf`, correos `.html`/`.mjml`, archivos `.txt`/`.csv`), audita sus variables y estructura exacta. **Prohibido asumir cambios estructurales en plantillas existentes** sin autorización explícita; la capa adaptadora debe amoldarse a los campos de la plantilla actual.
   - **Persistencia**: Especifica la manipulación segura de archivos locales (JSON, plantillas) o esquemas de base de datos según corresponda.
   - **Casos Borde**: Documenta validaciones de entrada, colisiones de archivo y errores controlados.
   - **Checklist Técnico**: Desglosa las tareas concretas para el desarrollador.

3. **Aprobación y Enlaces**:
   - Establece el estado en `automanagement_docs/refinamientos/REF-XXX.md` como `[Aprobado para Desarrollo]`.
   - Actualiza el enlace en `automanagement_docs/hus/HU-XXX.md` a `[`REF-XXX.md`](../refinamientos/REF-XXX.md)` y cambia su estado a `[Aprobado para Desarrollo]`.
   - Actualiza la tabla central en `automanagement_docs/README.md` enlazando el nuevo refinamiento.
   - Presenta al usuario un resumen conciso y el enlace a `REF-XXX.md`, indicando que el siguiente paso es ejecutar `/desarrollar-hu [HU-ID]`.
