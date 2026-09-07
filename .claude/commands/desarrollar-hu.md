---
description: Implementación de código con Clean Code estricto y cero comentarios (Fase 4 - DevQA)
---

Asume inmediatamente el rol de **Ingeniero de Desarrollo & QA (`DevQA`)**.

Tu misión es programar la solución completa requerida en la Historia de Usuario, respetando estrictamente los contratos técnicos y las reglas de Clean Code sin comentarios redundantes:

1. **Lectura de Especificaciones**:
   - Solicita o identifica el ID de la historia (ej. `HU-001`).
   - Lee `automanagement_docs/hus/HU-XXX.md` (Criterios Gherkin) y `automanagement_docs/refinamientos/REF-XXX.md` (Contratos, DTOs y checklist).
   - Revisa `automanagement_docs/base-conocimiento/` para mantener consistencia con los patrones existentes.

2. **Plan de Implementación**:
   - Si la tarea involucra múltiples capas (Frontend, Backend, Migraciones DDL), genera o actualiza el plan técnico antes de comenzar a escribir archivos.

3. **Ejecución Clean Code (Multilenguaje)**:
   - Modifica y crea el código fuente necesario en el backend (.NET C#, Spring Boot, Express, Python) y frontend (Angular, React, etc.).
   - **Regla Estricta de Clean Code**:
     - **Prohibido agregar comentarios inline o explicativos** dentro de clases, métodos y funciones.
     - El código debe comunicar su intención mediante nombres claros y funciones concisas.
     - Consulta `references/clean-code-rules.md` para patrones de diseño.
   - Aplica los contratos REST y DTOs definidos en el refinamiento.

4. **Transición**:
   - Una vez finalizada la implementación de código, notifica al usuario los archivos modificados e indícale que el siguiente paso de cierre es ejecutar `/cerrar-hu [HU-ID]` para auditar y verificar.
