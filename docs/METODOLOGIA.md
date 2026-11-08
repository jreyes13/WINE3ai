# Metodología de Mapeo Cartográfico y Análisis Vitivinícola 🗺️

[English Version](METHODOLOGY.md) | **Versión en Español**

Este documento detalla el flujo de trabajo técnico, cartográfico y analítico estandarizado utilizado en **WINE³ai** (*World Wide Wine*) para transformar pliegos normativos oficiales en capas SIG georreferenciadas, bases de datos vectoriales optimizadas y visualizaciones analíticas web interactivas.

---

## 1. Fundamentos Cartográficos y Fuentes Oficiales

La premisa fundacional del proyecto es la utilización exclusiva de **fuentes gubernamentales e institucionales oficiales**, descartando polígonos aproximados dibujados a mano alzada.

### A. Marco Normativo Vitivinícola Oficial
* **Unión Europea:** Base de datos oficial **eAmbrosia** (Directorio de Denominaciones de Origen Protegidas e Indicaciones Geográficas de la Comisión Europea).
* **Organismos Nacionales Competentes:**
  * 🇪🇸 **España:** Ministerio de Agricultura, Pesca y Alimentación (MAPA) y boletines oficiales autonómicos.
  * 🇫🇷 **Francia:** Institut National de l'Origine et de la Qualité (INAO) — *Cahiers des charges*.
  * 🇮🇹 **Italia:** Ministero dell'Agricoltura, della Sovranità Alimentare e delle Foreste (MASAF) — *Disciplinari di produzione*.
  * 🇵🇹 **Portugal:** Instituto da Vinha e do Vinho (IVV) — *Cadernos de especificações*.
  * 🇩🇪 **Alemania:** Bundesanstalt für Landwirtschaft und Ernährung (BLE) — *Weinverordnung (WeinV)*.
  * 🇦🇹 **Austria:** Bundesministerium für Land- und Forstwirtschaft (BML) — *Österreichisches Weingesetz*.
  * 🇬🇷 **Grecia:** Ministerio de Desarrollo Rural y Alimentación (YPAAT).
  * 🇭🇺 **Hungría:** Nemzeti Élelmiszerlánc-biztonsági Hivatal (NÉBIH) y Hegyközségek Nemzeti Tanácsa (HNT).
  * 🇬🇪 **Georgia:** Agencia Nacional del Vino de Georgia (NWA) y Sakpatenti.
  * 🇨🇿 **República Checa:** Ústřední kontrolní a zkušební ústav zemědělský (ÚKZÚZ).
  * 🇨🇭 **Suiza:** Office Fédéral de l'Agriculture (OFAG / BLW) y Swiss Wine Promotion.
  * 🇸🇮 **Eslovenia:** Ministerio de Agricultura, Silvicultura y Alimentación (MKGP).
  * 🇭🇷 **Croacia:** Ministerio de Agricultura — *Zakon o vinu*.
  * 🇸🇰 **Eslovaquia:** Ministerio de Agricultura y Desarrollo Rural — *Zákon č. 313/2009 Z. z.*
  * 🇷🇴 **Rumanía:** Oficiul Național al Viei și Produselor Vitivinicole (ONVPV).
  * 🇧🇬 **Bulgaria:** Agencia Ejecutiva de la Viña y el Vino (EAVW).
  * 🇲🇩 **Moldavia:** Oficina Nacional de la Viña y el Vino (ONVV).
  * 🇦🇲 **Armenia:** Fundación de la Viña y el Vino de Armenia (VWFA) y Ministerio de Economía.
  * 🇨🇾 **Chipre:** Departamento de Agricultura.
  * 🇱🇧 **Líbano:** Union Vinicole du Liban (UVL) — *Loi no 216/2000*.
  * 🇹🇷 **Turquía:** Ministerio de Agricultura y Silvicultura (*Tarım ve Orman Bakanlığı* - TADB) y el Instituto Turco de Patentes y Marcas (*TÜRKPATENT*).

### B. Cartografía Administrativa Base y Sistemas de Referencia (CRS)
| Ámbito Geográfico / País | Organismo Cartográfico Oficial | Nivel de Entidad Base | Sistema de Coordenadas Nativo | CRS de Publicación Web |
| :--- | :--- | :--- | :--- | :--- |
| **Alemania** | BKG (Bundesamt für Kartographie und Geodäsie) | Gemeinden / Kreise | ETRS89 / UTM 32N (EPSG:25832) | WGS84 (EPSG:4326) |
| **Armenia** | Cadastre Committee / Natural Earth | Marzer (Provincias) | ArmRef02 (EPSG:5636) / WGS84 | WGS84 (EPSG:4326) |
| **Austria** | BEV (Bundesamt für Eich- und Vermessungswesen) | Gemeinden / Bezirke | MGI / Austria Lambert (EPSG:31287) | WGS84 (EPSG:4326) |
| **Bulgaria** | AGKK / Natural Earth | Oblasti / Obshtini | BGS2005 (EPSG:7801) | WGS84 (EPSG:4326) |
| **Chipre** | Dept. of Lands and Surveys / Natural Earth | Eparquías / Comunidades | CGRS93 (EPSG:6312) | WGS84 (EPSG:4326) |
| **Croacia** | DGU (Državna geodetska uprava) | Županije / Gradovi | HTRS96/TM (EPSG:3765) | WGS84 (EPSG:4326) |
| **Eslovaquia** | ÚGKK SR / Eurostat | Kraje / Okresy | S-JTSK (EPSG:5514) | WGS84 (EPSG:4326) |
| **Eslovenia** | GURS (Autoridad Cartográfica y Geodésica) | Občine / Upravne enote | D96/TM (EPSG:3794) | WGS84 (EPSG:4326) |
| **España (Península / Baleares)** | IGN España (INSPIRE) | Municipios (`recintos_municipales`) | ETRS89 (EPSG:4258) | WGS84 (EPSG:4326) |
| **España (Canarias)** | IGN España | Municipios | REGCAN95 (EPSG:4081) | WGS84 (EPSG:4326) |
| **Francia** | IGN France (BD CARTO® / Géoportail) | Communes / Cantons | RGF93 / Lambert-93 (EPSG:2154) | WGS84 (EPSG:4326) |
| **Georgia** | NAPR / Sakpatenti | Municipios / Rayones | WGS84 / UTM 38N (EPSG:32638) | WGS84 (EPSG:4326) |
| **Grecia** | ELSTAT / YPAAT | Prefecturas / Municipios | GGRS87 (EPSG:2100) | WGS84 (EPSG:4326) |
| **Hungría** | Lechner Tudásközpont / FÖMI | Condados / Asentamientos | EOV / HD72 (EPSG:23700) | WGS84 (EPSG:4326) |
| **Italia** | ISTAT (Istituto Nazionale di Statistica) | Comuni | Roma40 / Gauss-Boaga (EPSG:3003) | WGS84 (EPSG:4326) |
| **Líbano** | Dirección de Asuntos Geográficos (DAG) | Gobernaciones / Distritos | Deir ez Zor / Levant (EPSG:22770) | WGS84 (EPSG:4326) |
| **Moldavia** | ARFC / Natural Earth | Raioane | Moldref 99 (EPSG:4026) | WGS84 (EPSG:4326) |
| **Portugal** | DGT (Direção-Geral do Território - CAOP) | Concelhos / Freguesias | ETRS89 / PT-TM06 (EPSG:3763) | WGS84 (EPSG:4326) |
| **República Checa** | ČÚZK | Okresy / Kraje | S-JTSK (EPSG:5514) | WGS84 (EPSG:4326) |
| **Rumanía** | ANCPI / Eurostat | Județe / Comuni | Dealul Piscului 1970 (EPSG:31700) | WGS84 (EPSG:4326) |
| **Suiza** | swisstopo | Cantones / Comunas | CH1903+ / LV95 (EPSG:2056) | WGS84 (EPSG:4326) |
| **Turquía** | Harita Genel Müdürlüğü (HGM) / Natural Earth | İller (Provincias) / İlçeler | TUREF (EPSG:5254) / WGS84 | WGS84 (EPSG:4326) |

---

## 2. El Flujo de Trabajo Técnico en 5 Pasos

```
[1. Pliego Oficial PDF] ──> [2. Extracción y Normalización] ──> [3. Filtrado SQL en QGIS]
                                                                        │
[5. Publicación Web]    <── [4. Exportación GeoJSON / GPKG] <───────────┘
```

### Paso 1: Extracción de la Delimitación Geográfica
Cada pliego de condiciones dedica una sección específica a la demarcación territorial:
* En los pliegos españoles: **Apartado 4 ("Delimitación de la zona geográfica")**.
* En los *Cahiers des charges* franceses: **Chapitre I, Section III ("Aire géographique")**.
* En los *Disciplinari* italianos: **Articolo 3 ("Zona di produzione delle uve")**.
* En los *Cadernos de especificações* portugueses: **Capítulo III ("Área geográfica delimitada")**.
* Se extrae la lista rigurosa de términos municipales, comunas o entidades menores habilitadas para la producción de uva y elaboración de vino.

### Paso 2: Normalización y Resolución de Nombres
Se aplican reglas de coincidencia contra los nomenclátores oficiales para evitar pérdidas de geometría:
1. **Nombres Bilingües Oficiales:** Se contempla la coexistencia de denominaciones dobles (ej. Álava: `Ayala/Aiara`, `Laguardia/Guardia`; Suiza: cantones bilingües de Valais y Friburgo; Trentino-Alto Adige: nombres duales italiano/alemán como `Bolzano/Bozen`).
2. **Entidades Menores y Pedanías:** Cuando el pliego cita aldeas o caseríos no constituidos en municipio propio, se asigna cartográficamente el municipio matriz oficial.
3. **Fusiones y Reorganizaciones Municipales:** Se utilizan las tablas de correspondencia histórica de comunas (ej. comunas nuevas en Francia o fusiones en Portugal tras la reforma de 2013).

### Paso 3: Construcción y Versionado de Expresiones SQL
Para cada región vitivinícola, se genera una consulta SQL validada que permite reproducir instantáneamente la selección en QGIS:
```sql
-- Ejemplo: Selección por atributo normalizado
"NAMEUNIT" IN (
  'Municipio 1',
  'Municipio 2',
  'Municipio 3'
)
```
Todas las consultas se archivan en `QGIS/<PAIS>/SQLs/` garantizando reproducibilidad y versionado continuo.

### Paso 4: Empaquetado Vectorial (GeoPackage y GeoJSON)
Las entidades seleccionadas se exportan asegurando la integridad topológica:
* **En QGIS Desktop:** *Exportar > Guardar objetos seleccionados como...* seleccionando formato GeoPackage (`.gpkg`) con reproyección a **EPSG:4326 (WGS84)**.
* **Vía línea de comandos (`ogr2ogr`):**
  ```bash
  ogr2ogr -f GeoJSON -t_srs EPSG:4326 salida.geojson entrada.shp \
    -where "NAMEUNIT IN ('Muni1', 'Muni2')"
  ```
* Se calculan los centroides geométricos de cada región (`centroid: [lng, lat]`) para facilitar el posicionamiento dinámico de la cámara y marcadores analíticos.

### Paso 5: Despliegue en Aplicaciones Web Interactivas
Los datos vectoriales se despliegan en el ecosistema digital del proyecto:
1. **Visor de Mapas de Regiones ([`index.html`](../index.html)):**
   * Motor cartográfico basado en **MapLibre GL JS** sobre teselas vectoriales CartoDB (Voyager, Positron, Dark Matter) y satélite ESRI.
   * Filtros dinámicos en cascada por país, clasificación (DOCa, DO, AOC, DOCG, etc.) y subregión.
   * Buscador de municipios interactivo con apertura de *chips* e hipervínculos a los pliegos oficiales.
   * Panel lateral colapsable con redimensionamiento fluido del lienzo (`map.resize()`).
2. **Plataforma Atlas.co:** Publicación colaborativa en la nube con simbología estandarizada y tooltips enriquecidos.

---

## 3. Pipeline de Análisis de Variedades de Uva (`grapes.html`)

El proyecto incorpora un analizador especializado en variedades de uva alimentado por un pipeline automatizado en Python ([`scratch/build_grape_database.py`](../scratch/build_grape_database.py)):

```
[GeoJSON 763 Regiones] ──> [Normalización & Sinónimos] ──> [Cálculo de Cuotas & Estilos]
                                                                     │
[Visualización grapes.html] <── [Datasets JSON / JS] <───────────────┘
```

1. **Extracción y Tokenización:** El script recorre los campos `grapes_red` y `grapes_white` de las 763 regiones vitivinícolas, separando menciones y limpiando notas contextuales.
2. **Diccionario Universal de Sinónimos:** Vincula las denominaciones vernáculas a su identidad canónica:
   * *Tempranillo:* Tinta del País, Tinto Fino, Cencibel, Ull de Llebre, Aragonez, Tinta Roriz, Tinto de Toro.
   * *Pinot Noir:* Spätburgunder, Pinot Nero, Blauburgunder, Modri Pinot, Rulandské modré.
   * *Garnacha / Grenache:* Garnacha Tinta, Grenache Noir, Cannonau, Alicante, Lledoner Pelut.
   * *Sangiovese:* Brunello, Morellino, Prugnolo Gentile, Nielluccio.
   * *Nebbiolo:* Spanna, Chiavennasca, Picotendro.
   * *Blaufränkisch:* Kékfrankos, Lemberger, Frankovka, Modra Frankinja.
   * *Grüner Veltliner:* Veltlínské zelené, Zelený veltlín.
   * *Chasselas:* Fendant, Gutedel.
   * *Welschriesling / Graševina:* Olaszrizling, Ryzlink vlašský, Laški rizling.
3. **Cálculo de Porcentajes Reglamentarios y Enfoque de Mezcla:**
   * Detecta si la variedad cuenta con una exigencia porcentual en el pliego (ej. *Ribera del Duero min 75% Tempranillo; Barolo 100% Nebbiolo; Brunello 100% Sangiovese; Naoussa 100% Xinomavro; Wachau 100% DAC*).
   * Clasifica la aptitud de elaboración: **Monovarietal (Varietal)** vs. **Mezcla (Coupage/Assemblage)**.
4. **Categorización de Estilos de Vino:**
   * **Vino Tranquilo (*Still*):** Tintos, blancos y rosados convencionales.
   * **Vino Espumoso (*Sparkling*):** Método tradicional y charmat (Champagne, Cava, Franciacorta, Prosecco, Crémant, Pezsgő, Sekt).
   * **Generoso y Dulce (*Fortified & Dessert*):** Vinos fortificados, asoleados y botritizados (Oporto, Jerez/Sherry, Madeira, Tokaji Aszú, Sauternes, Commandaria, Samos, Ruster Ausbruch).
5. **Generación de Datasets Ligeros:**
   * `data/grape_varieties.json` (2.5 MB) y `data/grape_varieties.js` (1.7 MB), sincronizados automáticamente con el directorio `web/`.
6. **Visualización Gráfica en SVG:**
   * Gráfico circular interactivo (*Donut Chart*) con distribución porcentual por país y filtro cruzado en un solo clic hacia la tabla y el mapa.

---

## 4. Filosofía Bilingüe y Accesibilidad

Todas las herramientas web (`index.html`, `grapes.html`) y documentos del repositorio se estructuran bajo un modelo bilingüe simétrico:
* **Idioma por Defecto:** Inglés (`en`), facilitando el acceso a la comunidad global de investigadores, estudiantes y sumilleres.
* **Conmutación Instantánea:** Selector de idioma en tiempo real (`ES` / `EN`) que traduce etiquetas, descripciones sensoriales, leyendas de gráficos y cabeceras sin recargar la página.
