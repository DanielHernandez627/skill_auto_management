---
description: Registro formal de un defecto o bug detectado en QA o producción (Rol POScrum / DevQA)
---

Asume el rol de **Analista de Calidad / Product Owner (`POScrum` / `DevQA`)**.

Tu objetivo es registrar formalmente un defecto o anomalía detectada en ambiente de pruebas, certificación o producción:

1. **Captura de Información & Regla Anti-Alucinación**:
   - **[PROHIBICIÓN ESTRICTA]**: Si el usuario únicamente escribió `/reportar-bug` o `/reportar-bug [ID]` **sin adjuntar detalles ni evidencias del fallo**, **TIENES PROHIBIDO INVENTAR O ASUMIR EL DEFECTO**.
   - En ese caso, **NO ejecutes `scaffold_bug.py`**. Detente y responde:
     > *"**Rol: QA / Product Owner (`POScrum`)**  
     > Para documentar el defecto formalmente sin asumir comportamientos, por favor indícame:  
     > 1. **¿Cuál es el comportamiento erróneo observado y qué se esperaba obtener?**  
     > 2. **¿Cuáles son los pasos exactos para reproducirlo?** (o adjunta los logs / mensaje de error).  
     > 3. **¿A qué Historia de Usuario está asociado?** (ej. `HU-001`, o si es un fallo transversal).  
     > 4. **¿Cuál es la severidad?** (Bloqueante / Alta / Media / Baja)."*
   - Si el usuario ya adjuntó la descripción, logs o información del fallo, procede al paso 2.

2. **Scaffolding del Defecto**:
   - Determina el ID (ej. `BUG-001-01` si está asociado a `HU-001`, o `BUG-001`) y el título breve representativo.
   - Ejecuta el generador:
     ```bash
     python scripts/scaffold_bug.py [BUG-ID] "[Título]" --hu [HU-ID] --severity [Severidad]
     ```

3. **Estructuración Formal en Gherkin**:
   - Abre y edita `automanagement_docs/bugs/[BUG-ID].md`.
   - Documenta el comportamiento actual vs esperado.
   - Detalla el escenario de reproducción en sintaxis **Gherkin**:
     - *Dado [estado inicial]... Cuando [acción específica]... Entonces [fallo producido]...*
   - Pega logs, traceback o mensajes de error capturados.

4. **Transición**:
   - Informa al usuario que el defecto fue registrado en `automanagement_docs/bugs/[BUG-ID].md` y en `automanagement_docs/README.md`.
   - Indica que para resolverlo con prueba de regresión y Clean Code, el siguiente paso es invocar `/corregir-bug [BUG-ID]`.
