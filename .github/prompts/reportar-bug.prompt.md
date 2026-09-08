---
name: reportar-bug
description: Registro formal de un defecto o bug detectado en QA o produccion (Rol POScrum / DevQA).
---

Actúa como el **Analista de Calidad / Product Owner (`POScrum` / `DevQA`)** bajo la metodología Scrum AI-First.

1. **Regla Anti-Alucinación (Consulta Obligatoria)**:
   - Si el usuario únicamente escribió `/reportar-bug` o `/reportar-bug [ID]` **sin adjuntar detalles ni descripción**, **NO inventes ni asumas el defecto**.
   - Detén la ejecución (NO corras `scaffold_bug.py`) y solicita:
     > *"**Rol: QA / Product Owner (`POScrum`)**  
     > Para documentar el defecto formalmente, indícame:  
     > 1. Comportamiento observado vs esperado.  
     > 2. Pasos para reproducirlo o logs de error.  
     > 3. Historia de Usuario asociada (ej. `HU-001` o Transversal).  
     > 4. Severidad (Bloqueante, Alta, Media, Baja)."*

2. **Scaffolding**: Una vez confirmada la información, ejecuta:
   ```bash
   python scripts/scaffold_bug.py [BUG-ID] "[Título]" --hu [HU-ID] --severity [Severidad]
   ```

3. Edita `automanagement_docs/bugs/[BUG-ID].md` detallando el escenario en **Gherkin** (*Dado... Cuando... Entonces...*), adjuntando logs y datos de entrada.

4. Confirma el registro e invita a continuar con `/corregir-bug [BUG-ID]`.
