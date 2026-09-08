# Estándares y Convenciones de Desarrollo del Proyecto

| Campo | Detalles |
|---|---|
| **Proyecto** | [Nombre del Sistema] |
| **Fecha de Revisión** | YYYY-MM-DD |
| **Líder Técnico** | [TechLeadArchitect] |

---

## 1. Política de Clean Code y Código Auto-Descriptivo
- **Nomenclatura Intencionada**: Clases, métodos y variables deben expresar su función exacta sin ambigüedad.
- **Cero Comentarios Redundantes**: Prohibido comentar código para describir lo evidente. El código se explica por sí mismo.
- **Funciones Pequeñas y de Responsabilidad Única**: Limitar funciones a una sola tarea clara.

---

## 2. Convenciones de Nomenclatura por Lenguaje

### Backend ([C# / Java / Python / Go])
- **Clases / Interfaces**: `PascalCase` (Ej. `EpisodeRepository`, `IUserService`).
- **Métodos**: `PascalCase` en C# (`GetByIdAsync`), `camelCase` en Java/TS (`getById`), `snake_case` en Python (`get_by_id`).
- **Variables locales**: `camelCase` o `snake_case`.

### Frontend ([TypeScript / Angular / React])
- **Componentes**: `PascalCase` para clases (`PlayerComponent`), `kebab-case` para nombres de archivos (`player.component.ts`).
- **Constantes**: `UPPER_SNAKE_CASE`.

---

## 3. Manejo de Excepciones y Respuestas de Error
- **Errores de Negocio**: Lanzar excepciones de dominio controladas (`EntityNotFoundException`, `BusinessRuleViolationException`).
- **Respuestas HTTP**: Utilizar esquemas estándar de error (ej. RFC 7807 `ProblemDetails` o estructura JSON común con código y mensaje).

---

## 4. Directrices de Persistencia y ORM
- **Entidades Limpias**: Declarar modelos sin lógica de infraestructura acoplada.
- **Colecciones Ordenadas**: Declarar explícitamente ordenamiento por columnas ordinales (ej. `.OrderBy(x => x.Order)` o `@OrderBy("order ASC")`).
- **Validación DDL**: Todo campo obligatorio en la base de datos debe reflejarse como no anulable en el código y viceversa.
