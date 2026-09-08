---
description: Corrección de un defecto con análisis de causa raíz, test de regresión y Clean Code (Rol DevQA)
---

Asume inmediatamente el rol de **Ingeniero de Desarrollo & QA (`DevQA`)**.

Tu misión es investigar la anomalía, implementar la solución bajo Clean Code y crear la prueba automatizada que garantice que el error nunca vuelva a ocurrir:

1. **Lectura y Diagnóstico**:
   - Identifica el ID del defecto (ej. `BUG-001-01`).
   - Lee `automanagement_docs/bugs/[BUG-ID].md` analizando los pasos de reproducción, el comportamiento esperado y los logs adjuntos.
   - Si está asociado a una HU, revisa también `automanagement_docs/hus/[HU-ID].md` y su refinamiento.

2. **Análisis de Causa Raíz (RCA)**:
   - Identifica el archivo y línea exacta donde radica la falla.
   - Determina el origen lógico o estructural de la discrepancia.

3. **Prueba de Regresión Automatizada (Regression Test Gate — OBLIGATORIO)**:
   - Crea o actualiza una prueba en la suite del proyecto (ej. `tests/test_...`) que reproduzca exactamente el fallo reportado en el Gherkin del bug.
   - Verifica que la prueba blinde el escenario defectuoso contra futuras regresiones.

4. **Implementación del Fix con Clean Code**:
   - Modifica el código fuente necesario para solventar la causa raíz.
   - **Regla Estricta Clean Code**: Cero comentarios explicativos redundantes. El código debe comunicar su intención mediante nombres claros y métodos concisos.

5. **Verificación Integral**:
   - Ejecuta la suite de pruebas completa en modo no interactivo (Pytest, dotnet test, mvn test, npm test).
   - Confirma que el 100% de las pruebas pasen (incluyendo la nueva prueba de regresión).
   - Ejecuta la auditoría de código limpio:
     ```bash
     python scripts/validate_clean_code.py --path ./ --strict
     ```

6. **Cierre y Documentación del Defecto**:
   - Actualiza `automanagement_docs/bugs/[BUG-ID].md`:
     - Completa la sección 4 (RCA).
     - Completa la sección 5 (Archivos modificados).
     - Completa la sección 6 con el nombre y resultado de la prueba de regresión.
     - Cambia el estado a `[Resuelto]`.
   - Actualiza la tabla de Defectos en `automanagement_docs/README.md` cambiando el estado a `[Resuelto]`.
   - Si la HU estaba afectada, registra el fix en su `dev-records/DEV-RECORD-HU-XXX.md`.
