# Estándares de Código Auto-Descriptivo (Clean Code Multilenguaje)

La regla fundamental de este repositorio y de los proyectos gestionados bajo esta metodología es:

> **El código debe autoexplicarse a través de su diseño, estructura y nomenclatura en cualquier lenguaje (.NET C#, Java, TypeScript/JavaScript, Go, Rust, PHP, Python, etc.). Si un fragmento requiere un comentario explicativo para ser entendido, debe ser refactorizado.**

---

## 1. Reglas Generales de Comentarios y Constantes Semánticas

1. **Cero comentarios explicativos**: No documentar lo que una línea o bloque de código ya hace de manera evidente.
2. **Cero código comentado**: No dejar bloques de código inactivos o deprecados comentados. Utilizar el historial de Git para revisiones históricas.
3. **Cero Números Mágicos ni Strings Mágicos (`No Magic Numbers / Magic Strings`)**:
   - **Prohibido** utilizar literales numéricos (`60`, `0.19`, `86400`, `403`, `3`) o cadenas literales de negocio sueltas directamente en condicionales, cálculos o constructores.
   - Todo valor de negocio, umbral, factor de conversión, límite de reintentos o código de estado debe extraerse en **constantes con nombre semántico** (`UPPER_SNAKE_CASE`, `const`, `static readonly`) o **enumeraciones tipadas (`Enum`)**.
4. **Comentarios válidos únicamente en**:
   - Limitaciones externas impuestas por librerías de terceros o bugs del runtime (con enlace al issue).
   - Regulaciones legales o licencias de cabecera de archivo (si son estrictamente requeridas).

---

## 2. Comparativas por Lenguaje: Código Redundante vs Auto-Descriptivo

### C# (.NET / `.cs`)

#### ❌ Incorrecto (Comentarios redundantes)
```csharp
public class EpisodeService 
{
    // Obtiene los timestamps del episodio
    public async Task<List<TimeSpan>> GetTimestamps(int id) 
    {
        // Si no tiene marcas propias, busca en la temporada
        var episode = await _repository.FindByIdAsync(id);
        if (episode.SkipMarks == null || episode.SkipMarks.Count == 0) 
        {
            // Retorna las marcas de la temporada padre
            return episode.Season.DefaultSkipMarks;
        }
        return episode.SkipMarks;
    }
}
```

#### ✅ Correcto (Auto-descriptivo, conciso y expresivo)
```csharp
public class EpisodeService 
{
    public async Task<IReadOnlyList<TimeSpan>> ResolveSkipTimestampsAsync(int episodeId) 
    {
        var episode = await _repository.FindByIdAsync(episodeId);
        
        if (episode.HasCustomSkipMarks) 
        {
            return episode.SkipMarks;
        }

        return episode.Season.DefaultSkipMarks;
    }
}
```

---

### Java (Spring Boot / `.java`)

#### ❌ Incorrecto
```java
// Convierte el tiempo recibido en segundos
public int toSec(String t) {
    String[] parts = t.split(":"); // divide por dos puntos
    int m = Integer.parseInt(parts[0]); // minutos
    int s = Integer.parseInt(parts[1]); // segundos
    return (m * 60) + s; // formula de conversion
}
```

#### ✅ Correcto (Auto-descriptivo, sin números mágicos ni comentarios)
```java
private static final String TIME_SEPARATOR = ":";
private static final int SECONDS_PER_MINUTE = 60;

public int convertFormattedTimeToSeconds(String timeFormat) {
    String[] timeSegments = timeFormat.split(TIME_SEPARATOR);
    int minutes = Integer.parseInt(timeSegments[0]);
    int seconds = Integer.parseInt(timeSegments[1]);
    
    int totalMinutesInSeconds = minutes * SECONDS_PER_MINUTE;
    return totalMinutesInSeconds + seconds;
}
```

---

### TypeScript / JavaScript (`.ts`, `.js`)

#### ❌ Incorrecto
```typescript
// Valida si el usuario puede saltar intro
function canSkip(pos: number, start: number, end: number): boolean {
  // Comprueba si esta dentro del rango
  if (pos >= start && pos <= end) {
    return true;
  }
  return false;
}
```

#### ✅ Correcto
```typescript
function isPlaybackWithinIntroWindow(currentPosition: number, introStart: number, introEnd: number): boolean {
  return currentPosition >= introStart && currentPosition <= introEnd;
}
```

---

### Python (`.py`)

#### ❌ Incorrecto
```python
# Filtra archivos mp4 y los ordena
def get_files(path):
    f = os.listdir(path) # lista carpeta
    res = [x for x in f if x.endswith('.mp4')] # solo mp4
    res.sort() # ordenar alfabeticamente
    return res
```

#### ✅ Correcto
```python
def list_sorted_video_files(directory_path: Path) -> list[Path]:
    video_files = [file for file in directory_path.iterdir() if file.suffix.lower() == ".mp4"]
    return sorted(video_files, key=lambda file: file.name)
```

---

## 3. Verificación Automatizada Multilenguaje

Antes de dar por finalizada cualquier Historia de Usuario, se debe ejecutar la herramienta de auditoría:

```bash
# Proyecto completo (greenfield / nueva aplicación):
python scripts/validate_clean_code.py --path <ruta_al_proyecto> --strict

# Proyecto heredado / brownfield (audita únicamente líneas agregadas/modificadas de la HU):
python scripts/validate_clean_code.py --path <ruta_al_proyecto> --strict --only-diff
```

Si el script detecta comentarios en línea o bloques redundantes en el alcance evaluado, la tarea no se considera completada hasta haberlos eliminado o justificado.
