# 🧪 Estándares de Pruebas y Estrategia de Testing

| Campo | Detalles |
|---|---|
| **Proyecto** | [Nombre del Sistema] |
| **Fecha de Revisión** | YYYY-MM-DD |
| **Líder Técnico** | [TechLeadArchitect] |

---

## 🎯 1. Coverage Gates Requeridos

| Capa | Framework / Runner | Cobertura Mínima |
|---|---|---|
| **Backend** | [xUnit / JUnit 5 / Pytest] | **80%** |
| **Frontend** | [Jasmine / Jest / Vitest] | **85%** |

---

## ⚡ 2. Comandos de Ejecución No Interactivos

### Backend
```bash
# Comando de ejecución sin interacción ni bloqueos
[Ej. dotnet test --no-restore --verbosity normal]
```

### Frontend
```bash
# Comando de ejecución desatendida en modo Headless
[Ej. npm test -- --watch=false --browsers=ChromeHeadless --code-coverage]
```

---

## 🔬 3. Tipología de Pruebas y Ubicación de Suites

1. **Pruebas Unitarias**: Aislamiento estricto con mocks de dependencias externas.
2. **Pruebas de Integración**: Pruebas de controladores/endpoints con servidor en memoria y base de datos efímera.
3. **Casos Críticos Obligatorios**: Escenarios de autenticación, transacciones monetarias o streaming multimedia (ej. HTTP 206).
