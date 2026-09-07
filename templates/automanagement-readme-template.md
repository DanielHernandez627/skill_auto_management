# 📚 Documentación del Proyecto: [Nombre del Proyecto]

Bienvenido a la carpeta centralizada de documentación de **[Nombre del Proyecto]**. Este espacio está estructurado bajo una **política AI-First** y metodologías ágiles (Scrum), optimizado para ser consumido tanto por desarrolladores como por Agentes de Inteligencia Artificial (Antigravity, Claude, Copilot).

---

## 📁 Estructura Centralizada (`automanagement_docs/`)

```text
automanagement_docs/
├── README.md                      # Índice general y tabla de estado de HUs
├── base-conocimiento/             # 🧠 Base de conocimiento global (Fase 0: Onboarding)
│   ├── 01-analisis-arquitectura.md# Arquitectura, capas y diagramas Mermaid
│   ├── 02-estandares-desarrollo.md# Convenciones de nombrado y Clean Code
│   ├── 03-estandares-pruebas.md   # Estrategia de testing y Coverage Gates
│   └── 04-dominio-negocio.md      # Modelo conceptual y reglas de negocio
├── hus/                           # 📋 Historias de Usuario aisladas (Fase 1)
├── refinamientos/                 # 🔬 Refinamientos técnicos y contratos DTO (Fase 2)
└── dev-records/                   # 📝 Bitácoras individuales de desarrollo y QA (Fase 5)
```

---

## 🚀 Índice de Historias de Usuario (HUs)

| ID | Título | Estado | Refinamiento | Registro Dev / QA |
|---|---|---|---|---|
| *(Las nuevas HUs creadas con `/nueva-hu` se registrarán en esta sección)* | | | | |

---

## 🤖 Directrices AI-First del Proyecto
1. **Código Auto-Descriptivo**: Cero comentarios explicativos o redundantes en el código fuente.
2. **Modularidad**: Cada HU, refinamiento y bitácora reside en su propio archivo Markdown aislado.
3. **Coverage Gates**: Mínimo 80% de cobertura en Backend y 85% en Frontend antes del cierre.
