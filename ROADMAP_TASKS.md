# WINE³ai — Roadmap y Banco de Tareas para LM Studio

**Fecha de Creación:** 2026-11-19  
**Objetivo:** Guía de desarrollo de nuevas funcionalidades (App de Ficha de Cata SAT/CMS) y catálogo estructurado de tareas de inferencia local para ejecutar en momentos muertos u overnight mediante **LM Studio** (`qwen/qwen3.5-9b`).

---

## 📌 PARTE 1: La Ficha de Cata Digital (Web & Mobile PWA)

Diseño de una herramienta interactiva (accesible desde el móvil y el navegador) para registrar notas de cata profesionales siguiendo los dos grandes estándares mundiales:

### 1.1. Modo WSET SAT (Systematic Approach to Tasting — Nivel 3 / Diploma)
* **Fase Visual:** Claridad (límpido/turbio), Intensidad (pálido/medio/profundo), Color (púrpura, rubí, granate, leonado para tintos; limón, dorado, ámbar para blancos; rosa, salmón, naranja para rosados).
* **Fase Olfativa:** Condición (limpio/defectuoso: TCA, reducción, oxidación), Intensidad (baja/media-/media/media+/pronunciada), Descriptores de aromas agrupados:
  * *Primarios:* Fruta, flores, hierbas, especias, terruño.
  * *Secundarios:* Fermentación, lías, FML (mantequilla), roble (vainilla, humo, cedro).
  * *Terciarios:* Evolución en botella (cuero, sotobosque, compota, frutos secos, tabaco).
  * *Desarrollo:* Joven / En desarrollo / En su punto / Pasado.
* **Fase Gustativa:**
  * Dulzor (seco, casi seco, medio seco, medio dulce, dulce, muy dulce).
  * Acidez (baja/media-/media/media+/alta).
  * Tanino (nivel y naturaleza: maduro, sedoso, verde, astringente).
  * Alcohol (bajo, medio, alto) y Cuerpo (ligero, medio-, medio, medio+, pleno).
  * Mousse (delicado, cremoso, agresivo para espumosos).
  * Intensidad de sabor y Final / Persistencia (segundos/longitud).
* **Conclusiones y Nivel de Calidad (Criterio BLIC):**
  * **B**alance (Equilibrio)
  * **L**ength (Longitud/Persistencia)
  * **I**ntensity (Intensidad)
  * **C**omplexity (Complejidad)
  * Veredicto: Defectuoso / Pobre / Aceptable / Bueno / Muy Bueno / Sobresaliente.
  * Potencial de guarda: Beber ya (no apto para guarda) / Apto para beber pero puede mejorar / En su momento óptimo / Demasiado viejo.

### 1.2. Modo CMS (Court of Master Sommeliers — Deductive Tasting Grid)
* **Visual:** Clarity, Brightness, Color, Concentration, Rim Variation, Gas Evidence, Sediment, Staining of tears/viscosity.
* **Nariz:** Clean/Faulted, Intensity, Age Assessment, Fruit Characteristics (Tart, ripe, overripe, jammy, dried), Non-Fruit Characteristics (Floral, herbal, vegetal, spice, earth, mineral), Oak Treatment (French/American, new vs neutral, toast level).
* **Boca:** Sweetness, Fruit/Non-fruit, Structure (Acidity, Tannin, Alcohol, Body, Texture, Finish).
* **Conclusión Inicial (Initial Deduction):**
  * Old World vs New World.
  * Climate (Cool, Moderate, Warm).
  * Grape Variety (or Blend).
  * Estimated Age / Vintage Range.
* **Conclusión Final (Final Deduction):**
  * Grape Variety.
  * Country, Region, Sub-appellation / Cru.
  * Quality Level / Producer classification.
  * Vintage.

### 1.3. Funcionalidad Estrella: "Comparador contra el Canon (AI Evaluator)"
* Al terminar la cata, el usuario pulsa **"Comparar con el Canon"**.
* El motor compara las notas introducidas por el usuario contra el perfil canónico generado por LM Studio para ese vino/denominación y le da *feedback pedagógico* (ej. *"Has marcado tanino medio, pero un Barolo clásico tiene tanino alto y secante debido al hollejo de la Nebbiolo; buen ojo en las notas de alquitrán y violeta"*).

---

## 🤖 PARTE 2: Banco de Tareas para LM Studio (Momentos Muertos)

Este catálogo de tareas está listo para ser generado por bloques utilizando `scripts/overnight_worker.py` o scripts dedicados, consumiendo **0 tokens externos**.

---

### 📦 BLOQUE A: Perfiles Canónicos de Cata (Benchmark Tasting Profiles)
> **Propósito:** Base de datos de notas de cata canónicas (WSET SAT + CMS Grid) de los 50 vinos más representativos del mundo para alimentar la app de cata y las comparativas.

#### Tareas a Generar:
1. `Barolo DOCG (Nebbiolo, Piamonte, añada madura tradicional)`
2. `Chablis 1er Cru (Chardonnay, suelo kimmeridgiense, sin roble nuevo)`
3. `Rioja Gran Reserva (Tempranillo + Graciano, roble americano, crianza oxidativa prolongada)`
4. `Napa Valley Cabernet Sauvignon (Clima cálido, roble francés nuevo, madurez fenólica plena)`
5. `Sancerre / Pouilly-Fumé (Sauvignon Blanc, suelo de sílex y caillottes, acidez alta)`
6. `Mosel Riesling Spätlese (Suelo de pizarra azul, baja graduación, acidez punzante y azúcar residual)`
7. `Bordeaux Pauillac Cru Classé (Cabernet Sauvignon dominante, grava garonense, cedro y cassis)`
8. `Bourgogne Côte de Nuits Gevrey-Chambertin (Pinot Noir, caliza bajociana, fruta roja y sotobosque)`
9. `Brunello di Montalcino DOCG (Sangiovese Grosso, crianza en boti de roble eslavonio)`
10. `Hermitage Rouge (Syrah septentrional, granito descompuesto, rotundona, mora y cuero)`
11. `Vintage Port (Douro, blend autóctono, alcohol fortificado 20%, tanino masivo, fruta negra)`
12. `Champagne Blanc de Blancs Extra Brut (Chardonnay de la Côte des Blancs, creta, autólisis prolongada)`
13. `Jerez Manzanilla Pasada (Palomino Fino, suelo de albariza, velo de flor prolongado, salinidad extrema)`
14. `Hunter Valley Semillon (Bajo alcohol 11%, acidez extrema, notas de cera y tostado sin madera)`
15. `Mendoza Malbec de Altura (Gualtallary / Paraje Altamira, suelo aluvial con carbonato de calcio, violetas)`

---

### 📦 BLOQUE B: Simulador de Cartas de Vinos Erróneas (*Wine List Quizzes*)
> **Propósito:** Generar 30 casos prácticos estilo examen CMS (*Certified & Advanced*) donde una carta de restaurante ficticia contiene 6-10 errores enológicos que el estudiante debe cazar.

#### Tipos de Errores a Programar en los Prompts:
* **Añadas inexistentes o desastrosas:** (ej. *Châteauneuf-du-Pape 2002* donde las inundaciones destruyeron la cosecha).
* **Productores en denominaciones erróneas:** (ej. *Domaine Leflaive en Côte de Nuits* o *Vega Sicilia en Rías Baixas*).
* **Variedades no autorizadas en el pliego de condiciones:** (ej. *Chianti Classico con 100% Merlot* o *Sancerre con Chardonnay*).
* **Clasificaciones y Crus desfasados:** (ej. *Château Cheval Blanc como Premier Grand Cru Classé B*).
* **Errores ortográficos y de toponimia enológica:** (ej. *Meursault "Genevrieres"* en lugar de *Genevrières*, *Pouilly-Fuissé* listado en el Valle del Loira en vez del Mâconnais).

---

### 📦 BLOQUE C: Baterías de Preguntas de Examen de Sumillería (*Mock Exams*)
> **Propósito:** Generar 150 preguntas de opción múltiple estructuradas por estándar con justificación razonada.

#### Secciones a Cubrir:
1. **Estándar WSET Nivel 3 (50 Preguntas):**
   - Factores naturales que influyen en el estilo (latitud, altitud, corrientes marinas, pendientes).
   - Técnicas de vinificación y crianza (maceración en frío, FML, microoxigenación, velo de flor).
   - Estilos fortificados (Oporto, Jerez, Madeira) y espumosos (Champagne, Cava, Prosecco, Cap Classique).
2. **Estándar CMS Certified & Advanced (50 Preguntas):**
   - Geografía vitícola precisa (comunas de Burdeos, Crus de Barolo, Subzonas del Mosela).
   - Legislación vitivinícola internacional (Prädikatswein en Alemania/Austria, DOCG en Italia, AVAs en EE.UU.).
   - Servicio de sala, temperaturas de servicio, protocolo de decantación con vela y maridajes complejos.
3. **Estándar ASI Global (50 Preguntas):**
   - Concurso internacional de sumillería: cervezas del mundo, sakes (Junmai, Daiginjo), destilados y aguas minerales.
   - Viticultura sostenible, biodinámica (preparados 500 y 501, certificación Demeter) y agroecología.

---

### 📦 BLOQUE D: Guía Fonética y Ampelográfica
> **Propósito:** Base de datos fonética para que la web o la app pueda pronunciar correctamente términos difíciles mediante la *Web Speech API*.

#### Lista de Términos Críticos para Inferencia:
* **Francia:** *Châteauneuf-du-Pape*, *Meursault Charmes*, *Savennières Coulée de Serrant*, *Gevrey-Chambertin*, *Haut-Médoc*, *Gewürztraminer Sélection de Grains Nobles*.
* **Alemania & Austria:** *Trockenbeerenauslese*, *Wehlener Sonnenuhr*, *Schloss Johannisberg*, *Grüner Veltliner Smaragd*, *Blaufränkisch*.
* **Italia:** *Aglianico del Vulture*, *Valpolicella Ripasso*, *Taurasi*, *Cannonau di Sardegna*, *Schiava*, *Nerello Mascalese*.
* **Hungría & Grecia:** *Tokaji Aszú 6 Puttonyos*, *Hárslevelű*, *Furmint*, *Assyrtiko*, *Xinomavro*, *Agiorgitiko*.

---

## 🚀 Cómo Lanzar Estas Tareas en LM Studio

Todos estos lotes se pueden ir despachando usando el cliente `scripts/lm_studio.py` o añadiendo las listas a `scripts/overnight_worker.py`.

Ejemplo de script para correr un bloque específico:
```bash
# Lanzar el worker nocturno hasta la hora deseada
python3 scripts/overnight_worker.py --end 07:00
```
