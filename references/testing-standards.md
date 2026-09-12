# Estándares y Estrategia de Testing Automatizado (Multilenguaje)

Este documento establece las metas de cobertura (*Coverage Gates*), estándares de diseño de pruebas y pautas de ejecución sin bloqueos para entornos de desarrollo asistidos por Inteligencia Artificial en cualquier ecosistema tecnológico (.NET C#, Java Spring, TypeScript/Node/Angular/React, Go, Rust, PHP, Python).

---

## 1. Umbrales Mínimos de Cobertura (Coverage Gates)

| Capa / Ecosistema | Runner / Framework | Cobertura Mínima | Tipos de Prueba Requeridos |
|---|---|---|---|
| **Backend .NET (C#)** | xUnit / NUnit + Coverlet | **80%** | Pruebas unitarias de dominio, servicios, handlers CQRS y tests de integración con WebApplicationFactory. |
| **Backend Java (Spring Boot)** | JUnit 5 + Mockito + JaCoCo | **80%** | Casos de uso CQRS, slices con `@WebMvcTest`, controladores y servicios de dominio. |
| **Frontend (Angular / React / Vue / TS)** | Jasmine / Jest / Vitest | **85%** | Componentes UI, pipes, guards, stores y servicios HTTP con HttpTestingController. |
| **Backend / CLI / Microservicios (Python)** | Pytest / Unittest | **80%** | Lógica de negocio, parsers, validadores y endpoints FastAPI/Flask/Django. |
| **Microservicios (Go)** | go test (-cover) | **80%** | Handlers HTTP, servicios de dominio y repositorios con interfaces mockeadas. |
| **Sistemas / CLI (Rust)** | cargo test | **80%** | Módulos de lógica central, serialización y validaciones de tipos. |

---

## 2. Ejecución No Interactiva (Evitar Bloqueos de Terminal)

Para que los agentes de IA (Antigravity, Claude, Copilot) puedan ejecutar suites de pruebas y builds de forma desatendida, es mandatorio utilizar banderas que supriman prompts interactivos o peticiones de analíticas:

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

### Frontend (Angular CLI / NPM / Jest)
```bash
# Desactivar telemetría y ejecutar headless
export NG_CLI_ANALYTICS=false
npm test -- --watch=false --browsers=ChromeHeadless --code-coverage
```

### Python
```bash
# Runner principal con reporte de cobertura en terminal:
pytest --maxfail=1 --disable-warnings -q --cov=src --cov-report=term-missing

# Fallback estándar nativo (sin requerir dependencias externas instaladas):
python -m unittest discover -s tests -v
# En Linux / macOS:
python3 -m unittest discover -s tests/unit -v
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

## 3. Estructura y Diseño de Pruebas: Patrón AAA y Data Builders

### A. Patrón AAA (Arrange - Act - Assert)
Todo test automatizado debe reflejar de forma auto-descriptiva las 3 fases esenciales, separadas exclusivamente por líneas en blanco y **sin comentarios explicativos** (`// Arrange`, `// Act`, `// Assert`):

```csharp
// C# (.NET) - Estructura AAA auto-descriptiva
[Fact]
public async Task ProcessInvoice_WhenCustomerIsVip_AppliesTwentyPercentDiscount()
{
    var customer = new CustomerDataBuilder().AsVip().Build();
    var invoice = new InvoiceDataBuilder().WithCustomer(customer).WithSubtotal(1000m).Build();
    var sut = new InvoiceProcessor();

    var result = await sut.ProcessAsync(invoice);

    result.Total.Should().Be(800m);
    result.DiscountApplied.Should().Be(200m);
}
```

```typescript
// TypeScript / Jest - Estructura AAA auto-descriptiva
test('debe aplicar descuento VIP cuando el cliente cumple la condicion', async () => {
  const customer = aCustomerBuilder().asVip().build();
  const invoice = anInvoiceBuilder().withCustomer(customer).withSubtotal(1000).build();
  const processor = new InvoiceProcessor();

  const result = await processor.process(invoice);

  expect(result.total).toBe(800);
  expect(result.discountApplied).toBe(200);
});
```

```python
# Python / Unittest o Pytest - Estructura AAA auto-descriptiva
def test_process_invoice_when_customer_is_vip_applies_discount(self):
    customer = CustomerDataBuilder().as_vip().build()
    invoice = InvoiceDataBuilder().with_customer(customer).with_subtotal(1000).build()
    processor = InvoiceProcessor()

    result = processor.process(invoice)

    self.assertEqual(result.total, 800)
    self.assertEqual(result.discount_applied, 200)
```

---

### B. Patrón Data Builder (Test Data Builder)
El patrón **Data Builder** es el estándar obligatorio para construir fixtures y entidades de prueba complejas:

1. **Cuándo Aplica**:
   - Entidades de dominio, modelos o DTOs con 3 o más propiedades.
   - Objetos con relaciones anidadas (ej. Factura $\rightarrow$ Cliente $\rightarrow$ Dirección).
   - Escenarios donde solo 1 o 2 campos son relevantes para la aserción del test.
2. **Ventajas Clave**:
   - **Valores Válidos por Defecto**: El builder encapsula la creación de un objeto válido, evitando tests repetitivos.
   - **Legibilidad y Expresividad**: Métodos fluidos como `.withRole(Role.Admin)`, `.withActiveSubscription()`, `.asVip()`.
   - **Resiliencia ante Cambios**: Modificar constructores o añadir nuevas propiedades en las entidades no rompe los tests existentes; solo se actualiza el Builder central.

---

## 4. Buenas Prácticas de Testing AI-First

1. **Aislamiento de Dependencias Externas**:
   - Bases de datos reales: Usar contenedores efímeros (Testcontainers), bases en memoria (H2 / SQLite / In-Memory EF Core) o repositorios mockeados para tests unitarios.
   - APIs externas: Simular siempre las respuestas HTTP con contratos JSON prefijados.
2. **Nomenclatura Expresiva de Tests**:
   - Nombrar las pruebas bajo la convención: `MetodoProbado_Escenario_ResultadoEsperado` o enunciados claros en BDD:
     - `ResolveSkipTimestamps_WhenEpisodeHasNoMarks_ReturnsSeasonDefaultMarks()`
3. **Registro Obligatorio en Bitácora**:
   - Toda suite de tests ejecutada con éxito debe reflejarse en `dev-records/DEV-RECORD-HU-XXX.md` indicando porcentaje de cobertura y número de pruebas ejecutadas.

---

## 5. Configuración de Cobertura y Exclusión de Entrypoints Multilenguaje

Para evitar que archivos de inicialización, lanzadores de interfaz gráfica o servidores embebidos distorsionen negativamente la métrica de cobertura de la lógica de negocio, se deben configurar exclusiones estándar según el ecosistema:

- **.NET (C#)**:
  - Decorar clases de arranque con `[ExcludeFromCodeCoverage]` o definir en el archivo `.runsettings`:
    ```xml
    <CodeCoverage>
      <ModulePaths>
        <Exclude><ModulePath>.*Program.*</ModulePath></Exclude>
      </ModulePaths>
    </CodeCoverage>
    ```
- **Java (JaCoCo / Maven / Gradle)**:
  - Excluir clases de configuración y arranque en la configuración del plugin JaCoCo:
    ```xml
    <excludes>
      <exclude>**/*Application.class</exclude>
      <exclude>**/config/**</exclude>
    </excludes>
    ```
- **Frontend / TypeScript (Jest / Vitest)**:
  - Configurar en `jest.config.js` o `vite.config.ts`:
    ```javascript
    coveragePathIgnorePatterns: ["main.ts", "environments/", ".*\\.module\\.ts$"]
    ```
- **Python (Pytest / Coverage)**:
  - Configurar en `setup.cfg` o `pyproject.toml`:
    ```ini
    [coverage:run]
    omit =
        */main.py
        */app.py
        */wsgi.py
    ```
