# 🧪 Estándares y Estrategia de Testing Automatizado

Este documento establece las metas de cobertura (*Coverage Gates*), estándares de diseño de pruebas y pautas de ejecución sin bloqueos para entornos de desarrollo asistidos por Inteligencia Artificial.

---

## 🎯 1. Umbrales Mínimos de Cobertura (Coverage Gates)

| Capa / Ecosistema | Runner / Framework | Cobertura Mínima | Tipos de Prueba Requeridos |
|---|---|---|---|
| **Backend .NET (C#)** | xUnit / NUnit + Coverlet | **80%** | Pruebas unitarias de dominio, servicios, handlers CQRS y tests de integración con WebApplicationFactory. |
| **Backend Java (Spring Boot)** | JUnit 5 + Mockito + JaCoCo | **80%** | Casos de uso CQRS, slices con `@WebMvcTest`, controladores y servicios de dominio. |
| **Frontend (Angular / React / Vue)** | Jasmine / Jest / Vitest | **85%** | Componentes UI, pipes, guards, stores y servicios HTTP con HttpTestingController. |
| **Microservicios / CLI (Python)** | Pytest + pytest-cov | **85%** | Lógica de negocio, parsers, validadores y endpoints FastAPI/Flask. |

---

## ⚡ 2. Ejecución No Interactiva (Evitar Bloqueos de Terminal)

Para que los agentes de IA (Antigravity, Claude, Copilot) puedan ejecutar suites de pruebas y builds de forma desatendida, es mandatorio utilizar banderas que supriman prompts interactivos o peticiones de analíticas:

### 🟦 .NET (C#)
```bash
dotnet test --no-restore --verbosity normal /p:CollectCoverage=true /p:CoverletOutputFormat=opencover
```

### ☕ Java (Maven / Gradle)
```bash
# Maven
mvn clean test -DinteractiveMode=false

# Gradle
./gradlew test --no-daemon --console=plain
```

### 🅰️ Frontend (Angular CLI / NPM)
```bash
# Desactivar telemetría y ejecutar headless
export NG_CLI_ANALYTICS=false
npm test -- --watch=false --browsers=ChromeHeadless --code-coverage
```

### 🐍 Python
```bash
pytest --maxfail=1 --disable-warnings -q --cov=src --cov-report=term-missing
```

---

## 📋 3. Buenas Prácticas de Testing AI-First

1. **Aislamiento de Dependencias Externas**:
   - Bases de datos reales: Usar contenedores efímeros (Testcontainers), bases en memoria (H2 / SQLite / In-Memory EF Core) o repositorios mockeados para tests unitarios.
   - APIs externas: Simular siempre las respuestas HTTP con contratos JSON prefijados.
2. **Nomenclatura Expresiva de Tests**:
   - Nombrar las pruebas bajo la convención: `MetodoProbado_Escenario_ResultadoEsperado` o enunciados claros en BDD:
     - `ResolveSkipTimestamps_WhenEpisodeHasNoMarks_ReturnsSeasonDefaultMarks()`
3. **Registro Obligatorio en Bitácora**:
   - Toda suite de tests ejecutada con éxito debe reflejarse en `dev-records/DEV-RECORD-HU-XXX.md` indicando porcentaje de cobertura y número de pruebas ejecutadas.

---

## 🛡️ 4. Configuración de Cobertura y Exclusión de Entrypoints Multilenguaje

Para evitar que archivos de inicialización, lanzadores de interfaz gráfica o servidores embebidos distorsionen negativamente la métrica de cobertura de la lógica de negocio, se deben configurar exclusiones estándar según el ecosistema:

- **🟦 .NET (C#)**:
  - Decorar clases de arranque con `[ExcludeFromCodeCoverage]` o definir en el archivo `.runsettings`:
    ```xml
    <CodeCoverage>
      <ModulePaths>
        <Exclude><ModulePath>.*Program.*</ModulePath></Exclude>
      </ModulePaths>
    </CodeCoverage>
    ```
- **☕ Java (JaCoCo / Maven / Gradle)**:
  - Excluir clases de configuración y arranque en la configuración del plugin JaCoCo:
    ```xml
    <excludes>
      <exclude>**/*Application.class</exclude>
      <exclude>**/config/**</exclude>
    </excludes>
    ```
- **🅰️ Frontend / TypeScript (Jest / Vitest)**:
  - Configurar en `jest.config.js` o `vite.config.ts`:
    ```javascript
    coveragePathIgnorePatterns: ["main.ts", "environments/", ".*\\.module\\.ts$"]
    ```
- **🐍 Python (Pytest / Coverage)**:
  - Configurar en `setup.cfg` o `pyproject.toml`:
    ```ini
    [coverage:run]
    omit =
        */main.py
        */app.py
        */wsgi.py
    ```
