# Cartographic Mapping Methodology & Viticultural Analysis 🗺️

**English** | [Versión en Español](METODOLOGIA.md)

This document details the standardized technical, cartographic, and analytical workflow utilized across **WINE³ai** (*World Wide Wine*) to transform official regulatory specifications (*cahiers des charges*, product specifications, ministerial decrees) into georeferenced GIS layers, optimized vector databases, and interactive web visual analytics.

---

## 1. Cartographic Foundations & Official Sources

The foundational principle of the project is the exclusive use of **official governmental and institutional sources**, discarding freehand or approximate polygons.

### A. Official Viticultural Regulatory Framework
* **European Union:** Official **eAmbrosia** database (Register of Protected Designations of Origin and Protected Geographical Indications of the European Commission).
* **National Competent Authorities:**
  * 🇪🇸 **Spain:** Ministerio de Agricultura, Pesca y Alimentación (MAPA) and regional official gazettes.
  * 🇫🇷 **France:** Institut National de l'Origine et de la Qualité (INAO) — *Cahiers des charges*.
  * 🇮🇹 **Italy:** Ministero dell'Agricoltura, della Sovranità Alimentare e delle Foreste (MASAF) — *Disciplinari di produzione*.
  * 🇵🇹 **Portugal:** Instituto da Vinha e do Vinho (IVV) — *Cadernos de especificações*.
  * 🇩🇪 **Germany:** Bundesanstalt für Landwirtschaft und Ernährung (BLE) — *Weinverordnung (WeinV)*.
  * 🇦🇹 **Austria:** Bundesministerium für Land- und Forstwirtschaft (BML) — *Österreichisches Weingesetz*.
  * 🇬🇷 **Greece:** Ministry of Rural Development and Food (YPAAT).
  * 🇭🇺 **Hungary:** Nemzeti Élelmiszerlánc-biztonsági Hivatal (NÉBIH) & Hegyközségek Nemzeti Tanácsa (HNT).
  * 🇬🇪 **Georgia:** National Wine Agency of Georgia (NWA) & Sakpatenti.
  * 🇨🇿 **Czech Republic:** Ústřední kontrolní a zkušební ústav zemědělský (ÚKZÚZ).
  * 🇨🇭 **Switzerland:** Federal Office for Agriculture (OFAG / BLW) & Swiss Wine Promotion.
  * 🇸🇮 **Slovenia:** Ministry of Agriculture, Forestry and Food (MKGP).
  * 🇭🇷 **Croatia:** Ministry of Agriculture — *Zakon o vinu*.
  * 🇸🇰 **Slovakia:** Ministry of Agriculture and Rural Development — *Zákon č. 313/2009 Z. z.*
  * 🇷🇴 **Romania:** Oficiul Național al Viei și Produselor Vitivinicole (ONVPV).
  * 🇧🇬 **Bulgaria:** Executive Agency on Vine and Wine (EAVW).
  * 🇲🇩 **Moldova:** National Office for Vine and Wine (ONVV).
  * 🇦🇲 **Armenia:** Vine and Wine Foundation of Armenia (VWFA) & Ministry of Economy.
  * 🇨🇾 **Cyprus:** Department of Agriculture.
  * 🇱🇧 **Lebanon:** Union Vinicole du Liban (UVL) — *Loi no 216/2000*.
  * 🇹🇷 **Turkey:** Ministry of Agriculture and Forestry (*Tarım ve Orman Bakanlığı* - TADB) & Turkish Patent and Trademark Office (*TÜRKPATENT*).

### B. Base Administrative Cartography & Coordinate Reference Systems (CRS)
| Geographic Scope | Official Cartographic Agency | Base Administrative Entity | Native Coordinate Reference System | Web Publishing CRS |
| :--- | :--- | :--- | :--- | :--- |
| **Armenia** | Cadastre Committee / Natural Earth | Marzer (Provinces) | ArmRef02 (EPSG:5636) / WGS84 | WGS84 (EPSG:4326) |
| **Austria** | BEV (Bundesamt für Eich- und Vermessungswesen) | Gemeinden / Bezirke | MGI / Austria Lambert (EPSG:31287) | WGS84 (EPSG:4326) |
| **Bulgaria** | AGKK / Natural Earth | Oblasti / Obshtini | BGS2005 (EPSG:7801) | WGS84 (EPSG:4326) |
| **Croatia** | DGU (Državna geodetska uprava) | Županije / Gradovi | HTRS96/TM (EPSG:3765) | WGS84 (EPSG:4326) |
| **Cyprus** | Dept. of Lands and Surveys / Natural Earth | Eparchies / Communities | CGRS93 (EPSG:6312) | WGS84 (EPSG:4326) |
| **Czech Republic** | ČÚZK | Okresy / Kraje | S-JTSK (EPSG:5514) | WGS84 (EPSG:4326) |
| **France** | IGN France (BD CARTO® / Géoportail) | Communes / Cantons | RGF93 / Lambert-93 (EPSG:2154) | WGS84 (EPSG:4326) |
| **Georgia** | NAPR / Sakpatenti | Municipalities / Rayons | WGS84 / UTM 38N (EPSG:32638) | WGS84 (EPSG:4326) |
| **Germany** | BKG (Bundesamt für Kartographie und Geodäsie) | Gemeinden / Kreise | ETRS89 / UTM 32N (EPSG:25832) | WGS84 (EPSG:4326) |
| **Greece** | ELSTAT / YPAAT | Prefectures / Municipalities | GGRS87 (EPSG:2100) | WGS84 (EPSG:4326) |
| **Hungary** | Lechner Tudásközpont / FÖMI | Counties / Settlements | EOV / HD72 (EPSG:23700) | WGS84 (EPSG:4326) |
| **Italy** | ISTAT (Istituto Nazionale di Statistica) | Comuni | Roma40 / Gauss-Boaga (EPSG:3003) | WGS84 (EPSG:4326) |
| **Lebanon** | Directorate of Geographic Affairs (DAG) | Governorates / Districts | Deir ez Zor / Levant (EPSG:22770) | WGS84 (EPSG:4326) |
| **Moldova** | ARFC / Natural Earth | Raioane | Moldref 99 (EPSG:4026) | WGS84 (EPSG:4326) |
| **Portugal** | DGT (Direção-Geral do Território - CAOP) | Concelhos / Freguesias | ETRS89 / PT-TM06 (EPSG:3763) | WGS84 (EPSG:4326) |
| **Romania** | ANCPI / Eurostat | Județe / Comuni | Dealul Piscului 1970 (EPSG:31700) | WGS84 (EPSG:4326) |
| **Slovakia** | ÚGKK SR / Eurostat | Kraje / Okresy | S-JTSK (EPSG:5514) | WGS84 (EPSG:4326) |
| **Slovenia** | GURS (Surveying and Mapping Authority) | Občine / Upravne enote | D96/TM (EPSG:3794) | WGS84 (EPSG:4326) |
| **Spain (Peninsula / Balearics)** | IGN España (INSPIRE) | Municipios (`recintos_municipales`) | ETRS89 (EPSG:4258) | WGS84 (EPSG:4326) |
| **Spain (Canary Islands)** | IGN España | Municipios | REGCAN95 (EPSG:4081) | WGS84 (EPSG:4326) |
| **Switzerland** | swisstopo | Cantons / Communes | CH1903+ / LV95 (EPSG:2056) | WGS84 (EPSG:4326) |
| **Turkey** | Harita Genel Müdürlüğü (HGM) / Natural Earth | İller (Provinces) / İlçeler | TUREF (EPSG:5254) / WGS84 | WGS84 (EPSG:4326) |

---

## 2. The 5-Step Technical Workflow

```
[1. Official Decree PDF] ──> [2. Extraction & Resolution] ──> [3. SQL Query in QGIS]
                                                                        │
[5. Web Deployment]      <── [4. Vector Export GeoJSON/GPKG] <──────────┘
```

### Step 1: Extraction of Geographic Delimitations
Every regulatory specification contains a dedicated territorial demarcation clause:
* Spanish specifications: **Section 4 ("Delimitación de la zona geográfica")**.
* French *Cahiers des charges*: **Chapitre I, Section III ("Aire géographique")**.
* Italian *Disciplinari*: **Articolo 3 ("Zona di produzione delle uve")**.
* Portuguese *Cadernos de especificações*: **Capítulo III ("Área geográfica delimitada")**.
* The exhaustive, authoritative list of municipalities, communes, or parishes permitted to cultivate grapes and produce wine is extracted.

### Step 2: Name Normalization & Disambiguation
Matching algorithms and name standardization rules are executed against national gazetteers to ensure zero geometry omission:
1. **Official Bilingual Names:** Handles co-official toponyms (e.g. Álava: `Ayala/Aiara`, `Laguardia/Guardia`; Switzerland: bilingual Valais and Fribourg communes; Trentino-Alto Adige: dual Italian/German names like `Bolzano/Bozen`).
2. **Sub-municipal Settlements & Hamlets:** Where legal decrees specify hamlets (*pedanías*, *hameaux*, *frazioni*), the containing official municipal polygon is matched.
3. **Municipal Mergers & Reforms:** Historical correspondence tables reconcile recent administrative mergers (e.g. *communes nouvelles* in France; Portuguese *freguesia* amalgamations of 2013).

### Step 3: Construction & Version Control of SQL Queries
For every wine region, an authenticated SQL expression is generated and archived to enable instantaneous, idempotent selection in QGIS:
```sql
-- Example: Normalized attribute selection
"NAMEUNIT" IN (
  'Municipality 1',
  'Municipality 2',
  'Municipality 3'
)
```
All queries are committed under `QGIS/<COUNTRY>/SQLs/` to ensure full reproducibility and continuous version control.

### Step 4: Vector Packaging (GeoPackage and GeoJSON)
Selected spatial entities are exported while enforcing topological integrity:
* **In QGIS Desktop:** *Export > Save Selected Features As...* using GeoPackage (`.gpkg`) format reprojected to **EPSG:4326 (WGS84)**.
* **Via command line (`ogr2ogr`):**
  ```bash
  ogr2ogr -f GeoJSON -t_srs EPSG:4326 output.geojson input.shp \
    -where "NAMEUNIT IN ('Muni1', 'Muni2')"
  ```
* Geometric centroids (`centroid: [lng, lat]`) are computed for every appellation to facilitate dynamic map panning and analytics markers.

### Step 5: Deployment to Interactive Web Applications
Vector features are integrated into the project's digital web ecosystem:
1. **Interactive Map Viewer ([`index.html`](../index.html)):**
   * Powered by **MapLibre GL JS** over CartoDB vector basemaps (Voyager, Positron, Dark Matter) and ESRI World Imagery.
   * Dynamic cascading filters by country, wine classification (DOCa, DO, AOC, DOCG, etc.), and subregion.
   * Interactive municipality search with tag *chips* and direct hyperlinks to official regulatory PDFs.
   * Collapsible sidebar with fluid canvas resizing (`map.resize()`).
2. **Atlas.co Collaborative Platform:** Cloud GIS deployment with uniform cartographic styling and enriched hover cards.

---

## 3. Grape Variety Analytical Pipeline (`grapes.html`)

The repository features a specialized grape variety analytics engine driven by an automated Python parsing pipeline ([`scratch/build_grape_database.py`](../scratch/build_grape_database.py)):

```
[763 GeoJSON Regions] ──> [Normalization & Synonyms] ──> [Quota & Style Calculations]
                                                                   │
[grapes.html Dashboard] <── [JSON / JS Datasets] <─────────────────┘
```

1. **Extraction & Tokenization:** The script parses the `grapes_red` and `grapes_white` fields across all 763 wine regions, tokenizing individual grape mentions and scrubbing regulatory metadata.
2. **Universal Synonym Dictionary:** Maps vernacular regional names to their canonical botanical identities:
   * *Tempranillo:* Tinta del País, Tinto Fino, Cencibel, Ull de Llebre, Aragonez, Tinta Roriz, Tinto de Toro.
   * *Pinot Noir:* Spätburgunder, Pinot Nero, Blauburgunder, Modri Pinot, Rulandské modré.
   * *Garnacha / Grenache:* Garnacha Tinta, Grenache Noir, Cannonau, Alicante, Lledoner Pelut.
   * *Sangiovese:* Brunello, Morellino, Prugnolo Gentile, Nielluccio.
   * *Nebbiolo:* Spanna, Chiavennasca, Picotendro.
   * *Blaufränkisch:* Kékfrankos, Lemberger, Frankovka, Modra Frankinja.
   * *Grüner Veltliner:* Veltlínské zelené, Zelený veltlín.
   * *Chasselas:* Fendant, Gutedel.
   * *Welschriesling / Graševina:* Olaszrizling, Ryzlink vlašský, Laški rizling.
3. **Regulatory Percentage & Blending Focus Engine:**
   * Detects mandatory quota requirements specified in regulations (e.g. *Ribera del Duero min 75% Tempranillo; Barolo 100% Nebbiolo; Brunello 100% Sangiovese; Naoussa 100% Xinomavro; Wachau 100% DAC*).
   * Classifies winemaking orientation: **Single-Varietal (Varietal)** vs. **Blend (Coupage / Assemblage)**.
4. **Wine Style Categorization:**
   * **Still Wine:** Conventional red, white, and rosé wines.
   * **Sparkling Wine:** Traditional and charmat method wines (Champagne, Cava, Franciacorta, Prosecco, Crémant, Pezsgő, Sekt).
   * **Fortified & Dessert Wine:** Fortified, dried-grape, and botrytized wines (Port, Sherry/Jerez, Madeira, Tokaji Aszú, Sauternes, Commandaria, Samos, Ruster Ausbruch).
5. **Lightweight Dataset Serialization:**
   * Generates optimized `data/grape_varieties.json` (2.5 MB) and `data/grape_varieties.js` (1.7 MB), mirrored directly to the `web/` directory.
6. **SVG Visual Analytics:**
   * Interactive Donut Chart displaying national acreage/appellation distribution with one-click cross-filtering to tabular and geospatial views.

---

## 4. Bilingual Design Philosophy & Accessibility

Both web applications (`index.html`, `grapes.html`) and the complete repository documentation follow a symmetrical bilingual standard:
* **Default Language:** English (`en`), providing immediate accessibility for the global research, academic, and sommelier community.
* **Instant Language Toggle:** Real-time language switcher (`ES` / `EN`) dynamically translating interface controls, analytical labels, chart legends, and data headers without page reload.
