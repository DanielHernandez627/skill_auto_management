# Reporte de Defecto / Bug: [BUG-ID] — [Título del Defecto]

| Campo | Detalles |
|---|---|
| **ID Defecto** | [BUG-ID] |
| **Historia Asociada** | [`[HU-ID]`](../hus/[HU-ID].md) |
| **Severidad** | [Bloqueante] / [Alta] / [Media] / [Baja] |
| **Estado** | [Reportado] |
| **Fecha de Reporte** | YYYY-MM-DD |
| **Fecha de Resolución** | Pendiente (`/corregir-bug`) |
| **Reportado por** | [QA Tester / Product Owner / Dev] |
| **Asignado a (DevQA)** | [Rol DevQA] |

---

## 1. Descripción del Comportamiento Anómalo

### Comportamiento Observado (Actual)
[Describe detalladamente qué ocurre actualmente al ejecutar la acción que falla.]

### Comportamiento Esperado
[Describe qué debería ocurrir según los criterios de aceptación o reglas de negocio.]

---

## 2. Pasos para Reproducir (Formato Gherkin)

```gherkin
Escenario: Reproducción del fallo [BUG-ID]
  Dado [estado inicial del sistema, configuración o datos de prueba]
  Cuando [el usuario realiza la acción específica con los parámetros exactos]
  Entonces [se produce el comportamiento anómalo en lugar del resultado esperado]
```

---

## 3. Evidencias, Datos de Entrada y Logs

```text
[Pega aquí el traceback de error, código de estado HTTP inesperado,
captura de consola o payload JSON utilizado]
```

---

## 4. Análisis de Causa Raíz (RCA — Completado por DevQA)

*Se completa durante la ejecución de `/corregir-bug`:*
- **Módulo / Componente afectado:** [ej. Capa de Servicios, Repositorio, Controlador, Frontend]
- **Archivo(s) origen del fallo:** [Ruta del archivo]
- **Causa raíz técnica:** [Explicación técnica concisa de por qué ocurrió la falla]

---

## 5. Solución Técnica Implementada

- [ ] Código refactorizado cumpliendo Clean Code estricto (0 comentarios explicativos).
- [ ] Rutas y contratos de persistencia validados.
- **Archivos modificados:**
  - `[MODIFY] ruta/al/archivo`

---

## 6. Prueba de Regresión Automatizada (Regression Test Gate)

> [!IMPORTANT]
> **Mandatorio en Scrum AI-First**: Todo defecto corregido debe contar obligatoriamente con una prueba automatizada que garantice que la anomalía nunca vuelva a presentarse.

- **Archivo de prueba:** `tests/test_[modulo].py`
- **Nombre de la prueba:** `test_[metodo]_[escenario_fallo]_[resultado_esperado]`
- **Resultado de ejecución:**
  ```text
  [Comando ejecutado y confirmación de que la prueba pasa exitosamente]
  ```

---

## 7. Verificación y Re-certificación

- [ ] Suite de pruebas completa ejecutada con éxito (100% de tests aprobados).
- [ ] Auditoría `validate_clean_code.py --strict` superada (0 infracciones).
- [ ] Estado actualizado a [Resuelto] en este documento y en `automanagement_docs/README.md`.
