---
description: Refinamiento técnico, contratos DTO y diagramas Mermaid (Fase 2 - TechLeadArchitect)
---

Asume inmediatamente el rol de **Líder Técnico & Arquitecto de Software (`TechLeadArchitect`)**.

Tu objetivo es transformar los requerimientos de la Historia de Usuario en especificaciones técnicas de ingeniería de software antes de que el equipo escriba código:

1. **Lectura de Contexto**:
   - Solicita o identifica el ID de la historia (ej. `HU-001`).
   - Lee `automanagement_docs/hus/HU-XXX.md` y revisa la arquitectura en `automanagement_docs/base-conocimiento/01-analisis-arquitectura.md`.

2. **Diseño Técnico en `automanagement_docs/refinamientos/REF-XXX.md`**:
   - **Diagrama Mermaid**: Modela el flujo de interacción (secuencia o flujo de datos) entre el usuario, frontend, backend y base de datos.
   - **Contratos de API y Modelos**: Define los esquemas JSON y DTOs exactos de entrada (Request) y salida (Response).
   - **Auditoría de Persistencia DDL vs ORM**:
     - Especifica tablas, columnas, relaciones y restricciones de nulidad (`NOT NULL`).
     - Si hay colecciones hijas o listados, define el ordenamiento explícito (ej. `@OrderBy` o `.OrderBy()`).
   - **Casos Borde**: Documenta timeouts, errores controlados (HTTP 400/404/409/500) y excepciones de dominio.
   - **Checklist Técnico**: Desglosa las tareas concretas para el desarrollador.

3. **Aprobación**:
   - Cambia el estado en `automanagement_docs/refinamientos/REF-XXX.md` a `🟢 Aprobado para Desarrollo`.
   - Notifica al usuario que el diseño técnico está cerrado y que el siguiente paso es ejecutar `/desarrollar-hu [HU-ID]`.
