# Global Expansion Guide & Next Viticultural Frontiers 🌍

**English** | [Versión en Español](EXPANSION_GLOBAL.md)

This document establishes the modular, technical, and collaborative architecture for scaling **WINE³ai** (*World Wide Wine*) globally, documenting the milestone already achieved across the **Old World** and providing a clear roadmap for integrating the wine regions of the **New World**.

---

## 1. Current Collection Status & Architecture

The project has achieved 100% complete official census coverage across **21 sovereign wine nations** throughout Europe, the Mediterranean basin, Anatolia, and the Caucasus:

| Regional Axis | Covered Countries (100% Official Census) | Demarcated Regions |
| :--- | :--- | :---: |
| **Western & Iberian Europe** | 🇪🇸 Spain, 🇵🇹 Portugal, 🇫🇷 France, 🇮🇹 Italy | 578 DOs / AOCs / DOCGs |
| **Central Europe & Alpine-Adriatic** | 🇩🇪 Germany, 🇦🇹 Austria, 🇨🇭 Switzerland, 🇸🇮 Slovenia, 🇭🇷 Croatia, 🇨🇿 Czech Republic, 🇸🇰 Slovakia | 72 g.U. / DAC / ZGP / CHOP |
| **Black Sea & Eastern Central Europe** | 🇭🇺 Hungary, 🇷🇴 Romania, 🇧🇬 Bulgaria, 🇲🇩 Moldova | 39 Borvidékek / DOC / PGI / IGP |
| **Archaeological Caucasus, Anatolia & Levant** | 🇬🇪 Georgia, 🇬🇷 Greece, 🇦🇲 Armenia, 🇨🇾 Cyprus, 🇱🇧 Lebanon, 🇹🇷 Turkey | 74 PDOs / POPs / GIs / Terroirs |
| **Total Consolidated Metric** | **21 Sovereign Nations** | **763 Official Regions** |

### Standardized Directory Hierarchy
The repository organizes all assets within a clean, country-by-country modular structure:

```
wine3ai/
├── index.html                   # Primary interactive wine map viewer (MapLibre GL JS)
├── grapes.html                  # Grape Varieties Global Explorer (circular charts & blend typology)
├── README.md                    # Main project documentation in English (summary table & links)
├── README_ES.md                 # Main project documentation in Spanish
├── data/                        # Production-ready datasets
│   ├── spain_wine_regions.geojson # 754 wine regions with vector boundaries, grapes, and metadata
│   ├── grape_varieties.json     # Knowledgebase of 675 normalized grape varieties
│   └── *.js                     # JS wrappers for local offline (file:// without CORS) use
├── docs/                        # Technical guides, methodology, and national registries
│   ├── COVERAGE.md              # Exhaustive coverage report in English
│   ├── COBERTURA.md             # Exhaustive coverage report in Spanish
│   ├── METHODOLOGY.md           # Technical methodology in English
│   ├── METODOLOGIA.md           # Technical methodology in Spanish
│   ├── GLOBAL_EXPANSION.md      # Scaling guide in English
│   ├── EXPANSION_GLOBAL.md      # Scaling guide in Spanish
│   ├── SPAIN/ ... SWITZERLAND/  # 20 national directories with full appellation registries
├── DOWNs/                       # Primary raw data archive
│   ├── DOCs/<COUNTRY>/          # 661 official legal specification PDFs organized by country
│   └── natural_earth_vector/    # High-resolution base administrative vector datasets
├── QGIS/                        # GIS vector layers (.gpkg) and master project (.qgz)
│   ├── wine_world_wine.qgz      # Master QGIS project (782 layers across 21 national groups)
│   ├── <COUNTRY>/               # GeoPackage layers organized by country
│   └── <COUNTRY>/SQLs/          # Versioned SQL filter scripts for administrative boundaries
└── web/                         # Synchronized mirror for GitHub Pages static web deployment
```

---

## 2. The Next Frontier: New World Viticulture 🍷

With the Old World foundational heritage mapped in full, the project's strategic roadmap focuses on the renowned terroirs of the Americas, Oceania, and South Africa:

### 🇺🇸 United States
* **Regulatory Authority:** **Alcohol and Tobacco Tax and Trade Bureau (TTB)** — *American Viticultural Areas (AVAs)* established under Title 27 of the Code of Federal Regulations (27 CFR Part 9).
* **Cartographic Baseline:** **US Census Bureau (TIGER/Line)** at County/Place level and TTB AVA vector boundaries.
* **Priority Terroirs:**
  * **California:** Napa Valley (and its 16 sub-AVAs: Oakville, Rutherford, Stags Leap District, Howell Mountain, Mount Veeder, Los Carneros), Sonoma County (Russian River Valley, Alexander Valley, Sonoma Coast, Dry Creek Valley), Paso Robles, Santa Barbara County (Sta. Rita Hills, Santa Maria Valley).
  * **Oregon:** Willamette Valley (Dundee Hills, Ribbon Ridge, Eola-Amity Hills, Yamhill-Carlton).
  * **Washington:** Columbia Valley, Walla Walla Valley, Red Mountain, Yakima Valley.

### 🇦🇷 Argentina
* **Regulatory Authority:** **Instituto Nacional de Vitivinicultura (INV)** — *Indicaciones Geográficas (IG)* and *Denominaciones de Origen Controlada (DOC)* (Law 25.163).
* **Cartographic Baseline:** **Instituto Geográfico Nacional de Argentina (IGN)** at Departamento and Distrito levels.
* **Priority Terroirs:**
  * **Mendoza:** Uco Valley (Gualtallary, Paraje Altamira, San Pablo, Los Chacayes, Vista Flores), Luján de Cuyo (Las Compuertas, Vistalba, Agrelo, Perdriel), Maipú (Barrancas).
  * **Salta & Calchaquí Valleys:** Cafayate, Molinos, Cachi (extreme high-altitude vineyards up to 3,111 m).
  * **San Juan:** Pedernal Valley, Calingasta Valley.
  * **Patagonia:** Río Negro (Alto Valle) and Neuquén (San Patricio del Chañar).

### 🇨🇱 Chile
* **Regulatory Authority:** **Servicio Agrícola y Ganadero (SAG)** — *Denominaciones de Origen (DO)* governed by Decree 464 on Viticultural Zoning and its complementary classifications (*Costa, Entre Cordilleras, Andes*).
* **Cartographic Baseline:** **Instituto Geográfico Militar (IGM Chile)** communal/provincial administrative boundaries.
* **Priority Terroirs:**
  * **Central Valley:** Maipo Valley (Alto Maipo, Pirque, Puente Alto), Colchagua Valley (Apalta, Los Lingues), Cachapoal Valley (Peumo), Curicó Valley, Maule Valley.
  * **Coastal Valleys:** Casablanca Valley, Leyda Valley, San Antonio Valley, Limarí Valley.
  * **Southern & Dry-Farmed Valleys:** Itata Valley (heritage ancestral País and Cinsault), Bío-Bío Valley.

### 🇦🇺 Australia
* **Regulatory Authority:** **Wine Australia** — *Geographical Indications (GI)* under the *Wine Australia Act 2013*.
* **Cartographic Baseline:** **Geoscience Australia** and the official *Register of Protected GIs*.
* **Priority Terroirs:**
  * **South Australia:** Barossa Valley, Eden Valley, McLaren Vale, Clare Valley, Coonawarra, Adelaide Hills.
  * **Western Australia:** Margaret River, Great Southern.
  * **Victoria:** Yarra Valley, Mornington Peninsula, Heathcote, Rutherglen.
  * **New South Wales:** Hunter Valley.

### 🇿🇦 South Africa
* **Regulatory Authority:** **South African Wine Industry Information and Systems (SAWIS)** — *Wine of Origin (WO)* scheme established under the *Liquor Products Act 60 of 1989*.
* **Cartographic Baseline:** **Municipal Demarcation Board (MDB)** and SAWIS District/Ward cartography.
* **Priority Terroirs:**
  * **Coastal Region:** Stellenbosch, Paarl, Swartland, Franschhoek, Constantia, Durbanville.
  * **Cape South Coast:** Walker Bay (Hemel-en-Aarde), Elgin.
  * **Breede River Valley:** Robertson.

### 🇳🇿 New Zealand
* **Regulatory Authority:** **New Zealand Winegrowers** and the *Intellectual Property Office of New Zealand (IPONZ)* — *Geographical Indications (Registration) Act 2016*.
* **Cartographic Baseline:** **Land Information New Zealand (LINZ)**.
* **Priority Terroirs:**
  * **South Island:** Marlborough (Wairau Valley, Awatere Valley), Central Otago (Bannockburn, Gibbston, Wanaka), Nelson, Waipara Valley.
  * **North Island:** Hawke's Bay (Gimblett Gravels, Bridge Pa), Martinborough / Wairarapa.

---

## 3. Standard Protocol for Integrating a New Nation or Appellation

To maintain strict cartographic rigor and interoperability within the **World Wine Wide** ecosystem, every addition adheres to this standardized 5-step workflow:

```
[1. Official Legal PDF] ──> [2. National Cartography] ──> [3. QGIS SQL Filtering]
                                                                  │
[5. Web Deployment] <── [4. GeoJSON / GPKG Export] <──────────────┘
```

1. **Obtain Official Specification:** Retrieve the governing regulatory statute defining the boundary and archive it as a PDF under `DOWNs/DOCs/<COUNTRY>/`.
2. **Acquire Base Administrative Boundaries:** Download official municipal/county geometries from the national mapping agency.
3. **Build SQL Selection Filter:** Develop the precise attribute selection expression in QGIS and version it under `QGIS/<COUNTRY>/SQLs/`.
4. **Export Vector Geometries:** Save the layer in GeoPackage format (`QGIS/<COUNTRY>/...`) with coordinates reprojected to standard **WGS84 (EPSG:4326)**.
5. **Web & Grape Analytics Integration:**
   * Append the new feature with full attributes (category, red varieties, white varieties, color, specifications link) into `data/spain_wine_regions.geojson`.
   * Run `scratch/build_grape_database.py` to automatically update the grape varieties knowledgebase and circular charts in `grapes.html`.
   * Document the appellation in `docs/<COUNTRY>/REGISTRO_...md` and update coverage matrices in `README.md`, `README_ES.md`, `COVERAGE.md`, and `COBERTURA.md`.

---

## 4. Contribution Template for New Appellations

When submitting a pull request or issue to propose or add a new wine region, use this standard Markdown template:

```markdown
### [Appellation / Wine Region Name]

- **Country & Macro-region:** [e.g. Argentina / Mendoza / Uco Valley]
- **Official Quality Classification:** [AVA / IG / DOC / DO / WO / GI]
- **Governing Regulatory Body:** [e.g. INV / TTB / SAG / Wine Australia]
- **Official Legal Specification:** [Link or PDF filename archived in DOWNs/DOCs/<COUNTRY>/]
- **Base Cartographic Agency:** [Official national mapping agency & dataset release year]
- **Filter Field Attribute:** [e.g. `NAME`, `FIPS`, `INSEE_COM`, etc.]
- **SQL Selection Query:**
  ```sql
  "NAME_UNIT" IN ('Unit 1', 'Unit 2', 'Unit 3')
  ```
- **Resulting GeoPackage File:** `QGIS/<COUNTRY>/<REGION>/<Appellation_Name>.gpkg`
- **Authorized Grape Varieties:**
  - Red: [e.g. Malbec (min 85%), Cabernet Franc, Merlot]
  - White: [e.g. Chardonnay, Torrontés, Sauvignon Blanc]
- **Production Styles:** [Still / Sparkling / Fortified]
- **Blend Typology:** [Monovarietal / Blend]
```

---

*Together, we are building the definitive, open geospatial reference for the world's wine terroirs!* 🍷
