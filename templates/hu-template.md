# 📋 Historia de Usuario: [HU-XXX] - [Título Corto de la Historia]

| Campo | Detalles |
|---|---|
| **ID Historia** | HU-XXX |
| **Fase / Módulo** | [Nombre del Módulo o Fase] |
| **Estado** | 🔴 Pendiente / 🟡 En Refinamiento / 🔵 En Desarrollo / 🟢 Finalizado |
| **Prioridad** | Alta / Media / Baja |
| **Refinamiento Técnico**| [`REF-XXX.md`](../refinamientos/REF-XXX.md) |
| **Bitácora Dev/QA** | [`DEV-RECORD-HU-XXX.md`](../dev-records/DEV-RECORD-HU-XXX.md) |
| **Archivos Relacionados** | *(Se completará durante el desarrollo)* |

---

## 🎯 Descripción
**Como** [tipo de usuario / rol / sistema],  
**Quiero** [funcionalidad u objetivo técnico/negocio a realizar],  
**Para que** [beneficio o valor de negocio obtenido].

---

## ✅ Criterios de Aceptación (Gherkin)

- [ ] **Escenario 1:** [Descripción del comportamiento esperado principal]
  - **Dado** [contexto o estado inicial del sistema]
  - **Cuando** [acción ejecutada por el usuario o evento disparado]
  - **Entonces** [resultado o comportamiento esperado verificable]

- [ ] **Escenario 2:** [Manejo de errores, validaciones o casos borde]
  - **Dado** [condición de error, datos inválidos o límite del sistema]
  - **Cuando** [se intenta realizar la acción]
  - **Entonces** [respuesta de error controlada, código HTTP o notificación en UI]

---

## 🛠 Requisitos Técnicos e Integración
- **Lenguaje / Framework:** [.NET C#, Java Spring Boot, TypeScript/Angular, Python, etc.]
- **Entradas:** [Payloads JSON, parámetros REST/gRPC, eventos o UI inputs]
- **Salidas:** [Respuestas REST, mutaciones en base de datos, mensajes en colas]
- **Dependencias:** [Otras HUs, librerías o servicios de infraestructura requeridos]

---

## 🧪 Plan de Verificación y Pruebas
- [ ] Compilación y build sin advertencias bloqueantes (flags no interactivos).
- [ ] Pruebas unitarias que cubran los escenarios Gherkin.
- [ ] Validación de cobertura mínima (Coverage Gate: Backend $\ge 80\%$, Frontend $\ge 85\%$).
- [ ] Auditoría de código limpio: Cero comentarios explicativos redundantes.
