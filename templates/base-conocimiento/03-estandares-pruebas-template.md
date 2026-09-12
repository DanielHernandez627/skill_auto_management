# Estándares de Pruebas y Estrategia de Testing

| Campo | Detalles |
|---|---|
| **Proyecto** | [Nombre del Sistema] |
| **Fecha de Revisión** | YYYY-MM-DD |
| **Líder Técnico** | [TechLeadArchitect] |

---

## 1. Coverage Gates Requeridos

| Capa / Ecosistema | Framework / Runner | Cobertura Mínima |
|---|---|---|
| **.NET (C#)** | xUnit / NUnit (Coverlet) | **80%** |
| **Java (Spring / Jakarta)** | JUnit 5 (JaCoCo) | **80%** |
| **Frontend / TS / Node** | Jasmine / Jest / Vitest | **85%** |
| **Python** | Pytest / Unittest | **80%** |
| **Go** | go test (-cover) | **80%** |
| **Rust** | cargo test | **80%** |

---

## 2. Comandos de Ejecución No Interactivos

### .NET (C#)
```bash
dotnet test --no-restore --verbosity normal /p:CollectCoverage=true /p:CoverletOutputFormat=opencover
```

### Java (Maven / Gradle)
```bash
# Maven
mvn clean test -DinteractiveMode=false
# Gradle
./gradlew test --no-daemon --console=plain
```

### Frontend (Angular / React / Vue / Jest)
```bash
# Headless y sin prompts
export NG_CLI_ANALYTICS=false
npm test -- --watch=false --browsers=ChromeHeadless --code-coverage
```

### Python
```bash
# Runner principal con cobertura:
pytest --maxfail=1 --disable-warnings -q --cov=src --cov-report=term-missing

# Fallback estándar nativo (sin dependencias externas):
python -m unittest discover -s tests -v
# En Linux / macOS:
python3 -m unittest discover -s tests -v
```

### Go
```bash
go test -v -coverprofile=coverage.out ./...
```

### Rust
```bash
cargo test -- --nocapture
```

---

## 3. Tipología de Pruebas y Ubicación de Suites

1. **Pruebas Unitarias**: Aislamiento estricto con mocks de dependencias externas.
2. **Pruebas de Integración**: Pruebas de controladores/endpoints con servidor en memoria y base de datos efímera.
3. **Casos Críticos Obligatorios**: Escenarios de autenticación, transacciones monetarias o streaming multimedia (ej. HTTP 206).

---

## 4. Estándar de Diseño: Patrón AAA y Data Builders

### A. Patrón AAA (Arrange - Act - Assert)
Toda prueba automatizada debe estructurarse estrictamente bajo el patrón AAA mediante **separación visual limpia** (líneas en blanco), **sin comentarios explicativos redundantes** (`// Arrange`, `// Act`, `// Assert`):

- **Arrange**: Inicialización de mocks, configuración de dependencias y preparación de datos de prueba.
- **Act**: Invocación de la acción bajo prueba (idealmente una única línea o llamada al método/endpoint).
- **Assert**: Comprobación exhaustiva del resultado esperado, cambios de estado o verificación de invocaciones.

### B. Patrón Data Builder (Test Data Builder)
Para entidades de dominio, modelos o DTOs con 3 o más propiedades o relaciones anidadas, se adopta el patrón **Data Builder**:

- **Valores por Defecto Válidos**: El builder inicializa un objeto completamente válido por defecto.
- **Personalización Exclusiva**: Cada prueba solo sobrescribe los campos directamente relacionados con el escenario evaluado (ej. `.withStatus(Status.Pending)` o `.asVip()`).
- **Resiliencia**: Los cambios en constructores de entidades no rompen las suites de prueba existentes.

---

## 5. Configuración de Cobertura y Exclusiones
*Definir exclusiones para entrypoints de ejecución o interfaces que distorsionen la métrica de cobertura de la lógica de negocio:*
- **.NET**: `[ExcludeFromCodeCoverage]` o filtro en `.runsettings`.
- **Java**: Exclusiones de `*Application.class` y configuraciones en JaCoCo.
- **TypeScript**: `coveragePathIgnorePatterns` en Jest/Vitest.
- **Python**: `omit` en `setup.cfg` o `pyproject.toml` para `main.py`, `app.py`, etc.

