# Documentación Técnica: Scripts de WINE³ai

**Versión:** 1.0.3  
**Directorio:** `/scripts/`  
**Proyecto:** WINE³ai (Sistema de Inteligencia Artificial Local para Enología)  
**Estado:** Estable / Producción  

---

## 1. Introducción

El directorio `scripts/` contiene la infraestructura de orquestación local para el procesamiento de datos enológicos y la inferencia de modelos de lenguaje (LLM). Todos los componentes están diseñados para operar **offline**, garantizando la privacidad de las recetas, análisis sensoriales y metadatos vitivinícolas sin dependencia de APIs externas.

---

## 2. `lm_studio.py`
**Conector Cliente Local con LM Studio**

Este script actúa como interfaz de aplicación (API Client) hacia una instancia local de LM Studio. Su función principal es encapsular la comunicación HTTP para gestionar inferencias de texto, asegurando que el procesamiento de tokens se realice estrictamente en hardware local (GPU/CPU), eliminando cualquier latencia o costo asociado a servicios en la nube.

### 2.1. Funcionalidades Clave
*   **Cero Consumo en la Nube:** Todas las peticiones se enrutan a `http://localhost:1234/v1`.
*   **Gestión de Tokens Granular:** Permite desglosar el consumo de tokens en tres categorías críticas para modelos de razonamiento:
    1.  **Prompt:** Tokens de entrada (instrucción + contexto).
    2.  **Gen:** Tokens generados por el modelo (respuesta directa).
    3.  **Reasoning:** Tokens dedicados a la cadena de pensamiento (Chain-of-Thought) interna del modelo.
*   **Control de Temperatura y Top-P:** Configuración dinámica para ajustar la creatividad vs. precisión en descripciones de cata o análisis de suelo.

### 2.2. Firma de la Función Principal (`query_lm`)

```python
def query_lm(prompt, system_prompt=None, model="qwen/qwen3.5-9b", max_tokens=5000, temperature=0.2, return_usage=False):
    """
    Envía una petición al endpoint local http://localhost:1234/v1/chat/completions.
    
    Retorna:
      - Si return_usage=False: str (contenido de la respuesta)
      - Si return_usage=True: tuple (content, token_stats_dict)
    """
```

| Parámetro | Tipo | Descripción | Valor por Defecto |
| :--- | :--- | :--- | :--- |
| `prompt` | str | Instrucción del usuario para la tarea enológica. | *(Requerido)* |
| `system_prompt` | str | Rol enológico / de sumiller asignado al modelo. | `None` |
| `model` | str | ID del modelo cargado en LM Studio. | `"qwen/qwen3.5-9b"` |
| `max_tokens` | int | Límite de tokens (evita truncamiento en modelos con CoT). | `5000` |
| `temperature` | float | Control de aleatoriedad (bajo para fidelidad técnica). | `0.2` |
| `return_usage` | bool | Devuelve el desglose detallado de tokens de LM Studio. | `False` |

### 2.3. Ejemplo de Uso desde Terminal o Python

```bash
# Invocación directa desde terminal
python3 scripts/lm_studio.py "Analiza la estructura tánica y mineral de la variedad Mencía en el Bierzo."
```

```python
# Uso programático con desglose de tokens
from scripts.lm_studio import query_lm

contenido, usage = query_lm(
    prompt="Genera ficha técnica para Tempranillo",
    system_prompt="Eres un Master Sommelier.",
    return_usage=True
)
print(f"Tokens invertidos: {usage['total_tokens']} (Razonamiento: {usage['reasoning_tokens']})")
```

---

## 3. `overnight_worker.py`
**Generador Autónomo Local de Contenido Enológico**

Script diseñado para ejecutarse en segundo plano (cron jobs) durante periodos inactivos del sistema. Genera contenido estructurado para la base de conocimiento WINE³ai, incluyendo fichas de producto, tarjetas de estudio y perfiles varietales.

### 3.1. Catálogo de Datos
El worker procesa automáticamente un catálogo interno de **370 fichas** enológicas, cubriendo:
*   **WINEp3dIA:** Base de datos interna de productos.
*   **Flashcards WSET3:** Material de estudio para el Diploma de Sommelier (Nivel 3).
*   **CMS (Certified Master Sommelier):** Datos avanzados de cata y gestión.
*   **ASI (Análisis Sensorial Integrado):** Perfiles de uva y terroir.

### 3.2. Argumentos CLI y Comportamiento

| Argumento | Formato | Descripción | Valor por Defecto |
| :--- | :--- | :--- | :--- |
| `--start` | `HH:MM` | Hora de inicio programada (ej. `22:30`). Si ya pasó, asume mañana. | Ahora mismo |
| `--end` | `HH:MM` | Hora de corte/finalización (ej. `06:45`). Si cruza medianoche, se programa para mañana. | Ahora + 3 horas |
| `--hours` | float/int | Duración en horas de la sesión (ej. `5` u `8.5`). | `3` horas |
| `--now` | flag | Fuerza el arranque inmediato sin esperas. | `False` |

### 3.3. Comportamiento por Defecto
Al ejecutarse sin argumentos:
1. Inicia inmediatamente.
2. Opera durante un bloque predeterminado de **3 horas**.
3. Visualiza el progreso ficha a ficha con desglose de tokens de LM Studio y tiempo en segundos.
4. Al terminar o alcanzar la hora límite, auto-compila la producción y genera `OVERNIGHT_REPORT.md`.

### 3.4. Ejemplos de Invocación

```bash
# 1. Modo rápido por defecto (arranca ya, corre 3 horas)
python3 scripts/overnight_worker.py

# 2. Modo noche completa hasta la mañana
python3 scripts/overnight_worker.py --end 06:45

# 3. Sesión con duración fija (ej. 8 horas)
python3 scripts/overnight_worker.py --hours 8

# 4. Programado para arrancar tarde y parar antes del desayuno
python3 scripts/overnight_worker.py --start 23:00 --end 06:45
```

---

## 4. `compile_generated_data.py`
**Compilador Seguro de Checkpoints JSON**

Este script es responsable de la etapa final del pipeline: consolidar los datos generados en formato JSON (almacenados temporalmente en `data/generated/`) hacia los archivos de producción de WINE³ai. Utiliza el motor **JavaScriptCore (`jsc`)** para garantizar integridad y seguridad durante la escritura de archivos masivos.

### 4.1. Mecanismo de Seguridad
Para evitar colisiones de archivos (race conditions) y sobrescrituras accidentales, el compilador implementa un mecanismo de bloqueo basado en `jsc`:
*   **Atomic Writes:** Los datos se escriben en un archivo temporal antes de renombrarlo al destino final.
*   **Checksum Validation:** Verificación de integridad del hash SHA-256 tras la compilación.
*   **Locking:** Bloqueo exclusivo sobre el directorio de salida durante el proceso.

### 4.2. Flujo de Trabajo y Destinos de Producción
1. Escanea `data/generated/` para leer los checkpoints JSON generados por el worker.
2. Carga los archivos JavaScript existentes mediante el motor nativo `jsc` de macOS (`/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc`) para interpretar de forma segura los objetos globales `WINEPEDIA_ARTICLES` y `STUDY_CARDS`.
3. Realiza un merge incremental por identificador único (`id` o nombre de uva), evitando duplicados.
4. Escribe sincrónicamente los activos tanto en el backend como en la aplicación web:
   - `data/winepedia_articles.js` y `web/data/winepedia_articles.js`
   - `data/study_cards.js` y `web/data/study_cards.js`
   - `data/grape_varieties.json` y `web/data/grape_varieties.json`

### 4.3. Ejemplo de Uso

```bash
# Compilación manual (también se ejecuta automáticamente al finalizar overnight_worker)
python3 scripts/compile_generated_data.py
```

---

## 5. Buenas Prácticas de Ejecución Nocturna

Para maximizar la eficiencia del sistema WINE³ai durante las ventanas de mantenimiento nocturno, se recomienda seguir los siguientes protocolos:

1.  **Orquestación:** Utilice `cron` o un scheduler similar para invocar `overnight_worker.py` entre las 02:00 y 05:00 AM, cuando la carga del sistema es mínima.
2.  **Monitoreo de Tokens:** Verifique el log de salida de `lm_studio.py`. Si el consumo de tokens supera el umbral de memoria RAM disponible, reduzca `--max-gen-tokens` en la siguiente ejecución.
3.  **Integridad de Datos:** Ejecute `compile_generated_data.py` inmediatamente después de que `overnight_worker.py` finalice con éxito (código de salida 0). Nunca fuerce una compilación si el directorio `data/generated/` está vacío.
4.  **Persistencia:** Asegúrese de que el servicio LM Studio esté persistente y en modo "Server" antes de iniciar cualquier script de inferencia.

---

**Nota Legal:** Todos los scripts operan exclusivamente bajo licencia local. No se establecen conexiones salientes a servidores externos salvo la API local de LM Studio.