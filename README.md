<p align="center">
  <img src="assets/logo_horizontal.svg" alt="WINE³ai — World Wine Maps & Terroir Intelligence" width="480">
</p>

# WINE³ai — Global Wine Regions & Terroir Intelligence 🍷

**English** | [Versión en Español](README_ES.md)

## Project Overview

**WINE³ai** (formerly *World Wine Wide*) is an open geospatial and viticultural intelligence project with a clear, ambitious mission: **to create authoritative, interactive maps and climate intelligence for every wine region on Earth**.

From the slopes of Bordeaux and Burgundy to the valleys of Napa and Rioja, from the terraces of Priorat to the volcanic soils of the Canary Islands, **WINE³ai** provides a rigorous, visual reference for winemakers, sommeliers, students, and enthusiasts.

## The Result

This project produces **interactive web maps** and terroir analytics that show the precise boundaries of wine appellations, world climate zones, and grape varietal distribution:

👉 **Official Interactive Web Map:** [https://jreyes13.github.io/wine3ai/](https://jreyes13.github.io/wine3ai/)  
👉 **Grape Varieties Global Explorer:** [https://jreyes13.github.io/wine3ai/grapes.html](https://jreyes13.github.io/wine3ai/grapes.html)  
👉 **Atlas.co Project:** [WINE³ai Map on Atlas](https://app.atlas.co/shared/iRfhgtNFAbVm6zHZL3bN?loc=-3.8121%2C41.8957%2C6.2431z&public=true)

## The Challenge: Sourcing Global Data

Every country manages its own geographic data. There is no single, global source for administrative boundaries. The core principle of **World Wine Wide** is to identify and process the most **authoritative official public sources** for both regulatory viticultural decrees and geographic demarcations:

### A. Authoritative Sources for Completed Nations (21 Countries)

| Country | Official Cartographic Agency / Portal | Base Administrative Level | Native Coordinate System (CRS) | Regulatory Wine Authority |
| :--- | :--- | :--- | :--- | :--- |
| 🇦🇲 **Armenia** | Cadastre Committee / Natural Earth | Marzer (Provinces) | ArmRef02 / WGS84 | VWFA / Min. of Economy |
| 🇦🇹 **Austria** | BEV (Bundesamt für Eich- und Vermessungswesen) | Gemeinden / Bezirke | MGI / Austria Lambert (EPSG:31287) | BML / eAmbrosia |
| 🇧🇬 **Bulgaria** | AGKK / Natural Earth | Oblasti / Obshtini | BGS2005 (EPSG:7801) | EAVW (Bulgarian Wine Agency) |
| 🇭🇷 **Croatia** | DGU (Državna geodetska uprava) | Županije / Gradovi | HTRS96/TM (EPSG:3765) | Min. Poljoprivrede / eAmbrosia |
| 🇨🇾 **Cyprus** | Dept. of Lands and Surveys / Natural Earth | Eparchies / Communities | CGRS93 (EPSG:6312) | Department of Agriculture |
| 🇨🇿 **Czech Republic** | ČÚZK (State Administration of Land Surveying) | Okresy / Kraje | S-JTSK (EPSG:5514) | ÚKZÚZ |
| 🇫🇷 **France** | IGN France (BD CARTO® / Géoportail) | Communes / Cantons | RGF93 / Lambert-93 (EPSG:2154) | INAO (*Cahiers des charges*) |
| 🇬🇪 **Georgia** | NAPR (National Agency of Public Registry) | Municipalities / Rayons | WGS84 / UTM 38N (EPSG:32638) | National Wine Agency / Sakpatenti |
| 🇩🇪 **Germany** | BKG (Bundesamt für Kartographie und Geodäsie) | Gemeinden / Kreise | ETRS89 / UTM 32N (EPSG:25832) | BLE / *Weinverordnung* |
| 🇬🇷 **Greece** | Hellenic Statistical Authority (ELSTAT) | Prefectures / Municipalities | GGRS87 (EPSG:2100) | YPAAT (Min. of Agriculture) |
| 🇭🇺 **Hungary** | Lechner Tudásközpont / FÖMI | Counties / Settlements | EOV / HD72 (EPSG:23700) | HNT / NÉBIH |
| 🇮🇹 **Italy** | ISTAT (Istituto Nazionale di Statistica) | Comuni | Roma40 / Gauss-Boaga (EPSG:3003) | MASAF (*Disciplinari*) |
| 🇱🇧 **Lebanon** | Directorate of Geographic Affairs (DAG) | Governorates / Districts | Deir ez Zor / Levant (EPSG:22770) | Union Vinicole du Liban (UVL) |
| 🇲🇩 **Moldova** | ARFC (Cadastre Agency) / Natural Earth | Raioane | Moldref 99 (EPSG:4026) | ONVV |
| 🇵🇹 **Portugal** | DGT (Direção-Geral do Território - CAOP) | Concelhos / Freguesias | ETRS89 / PT-TM06 (EPSG:3763) | IVV (*Cadernos de especificações*) |
| 🇷🇴 **Romania** | ANCPI / Eurostat | Județe / Comuni | Dealul Piscului 1970 (EPSG:31700) | ONVPV |
| 🇸🇰 **Slovakia** | ÚGKK SR (Geodesy Authority) / Eurostat | Kraje / Okresy | S-JTSK (EPSG:5514) | Min. Pôdohospodárstva |
| 🇸🇮 **Slovenia** | GURS (Surveying and Mapping Authority) | Občine / Upravne enote | D96/TM (EPSG:3794) | MKGP / eAmbrosia |
| 🇪🇸 **Spain** | IGN España (INSPIRE) | Municipios (`recintos_municipales`) | ETRS89 (EPSG:4258) / REGCAN95 | MAPA / Consejos Reguladores |
| 🇨🇭 **Switzerland** | swisstopo (Federal Office of Topography) | Cantons / Communes | CH1903+ / LV95 (EPSG:2056) | OFAG / BLW |
| 🇹🇷 **Turkey** | Harita Genel Müdürlüğü (HGM) / Natural Earth | İller (Provinces) / İlçeler | TUREF (EPSG:5254) / WGS84 | Tarım ve Orman Bak. / TÜRKPATENT |

### B. Roadmap Sources for Upcoming New World Expansion

| Country | Primary Cartographic Agency | Base Geographic Unit | Coordinate Reference System | Viticultural Authority |
| :--- | :--- | :--- | :--- | :--- |
| 🇺🇸 **USA** | US Census Bureau (TIGER/Line) | Counties / TTB Boundaries | NAD83 (EPSG:4269) | TTB (Alcohol and Tobacco Tax Bureau) |
| 🇦🇷 **Argentina** | IGN Argentina | Departamentos | POSGAR 2007 (EPSG:5343) | INV (Instituto Nacional de Vitivinicultura) |
| 🇨🇱 **Chile** | IDE Chile / IGM | Comunas / Provincias | SIRGAS-Chile (EPSG:5360) | SAG (Servicio Agrícola y Ganadero) |
| 🇦🇺 **Australia** | Geoscience Australia | GIs / Local Government Areas | GDA2020 (EPSG:7844) | Wine Australia |
| 🇳🇿 **New Zealand** | LINZ (Land Information New Zealand) | GIs / Territorial Authorities | NZGD2000 (EPSG:2193) | New Zealand Winegrowers |
| 🇿🇦 **South Africa** | NGI (National Geo-spatial Information) | Municipalities / WOs | Hartebeesthoek94 (EPSG:2048) | SAWIS (Wine Industry Information) |

> **Cartographic Standard:** All vector layers are reprojected and exported to **WGS84 (EPSG:4326)** for unified global GIS analysis and web performance.

## The Generic Workflow (5 Steps)

This methodology is designed to be **country-agnostic**. It can be applied to any wine region in the world.

### Step 1: Obtain the Official List of Administrative Units

Every wine region is defined by a set of administrative boundaries (municipalities, communes, counties, etc.). This list is the key to filtering the geographic data.

- **Source:** The wine's **Regulatory Council** (Consejo Regulador, Appellation d'Origine, etc.) usually publishes the official list of towns or villages that are part of the appellation.
- **Format:** This can be a PDF, a webpage, or a CSV file. The goal is to create a simple list of names that will be used as a filter.

### Step 2: Find and Download Official Geographic Data

Search for the national mapping agency of the country and download the administrative boundary data for the relevant region or for the entire country.

- **Search terms:** "administrative boundaries [country]", "municipalities shapefile [country]", "[country] GIS data", "INSPIRE [country]".
- **Data format:** The data may come as a Shapefile (`.shp`), GeoPackage (`.gpkg`), CSV with WKT, or other formats. All are usable.
- **Coordinate system:** Note the native coordinate system (e.g., ETRS89, NAD83, GDA2020). It will be preserved during processing.

### Step 3: Process the Data with QGIS (Open Source)

**QGIS** is the recommended tool for this step. It is free, open-source, and runs on all major operating systems.

1. **Import the raw data.**
   - Use `Layer > Add Layer > Add Vector Layer` (for Shapefiles/GeoPackages) or `Add Delimited Text Layer` (for CSV files with WKT).
   - If using a CSV with WKT, ensure you select **"Well Known Text (WKT)"** as the geometry definition.

2. **Filter by the list of administrative units.**
   - This is the core of the process. You need to match the names from **Step 1** with the names or unique identifiers in the geographic data.
   - In QGIS, open the attribute table of the layer and use the **"Select by Expression"** tool.
   - Use an expression like this to select all the features you need:
     ```sql
     "name_column" IN ('Name1', 'Name2', 'Name3', ...)
     ```
     *Or, if using official ID codes:*
     ```sql
     "id_column" IN ('ID1', 'ID2', 'ID3', ...)
     ```

3. **Export the filtered layer.**
   - Right-click on the layer → `Export > Save Selected Features As...`
   - Choose the **GeoPackage (GPKG)** format. It is an open, efficient, and highly recommended format for GIS data.
   - Save the file, e.g., `wine_region.gpkg`. This file now contains **only** the administrative units that make up the wine region.

### Step 4: Convert for Web Use (KML or GeoJSON)

Web mapping platforms like Google Maps do not support GeoPackage directly. They require **KML** or **GeoJSON**.

1. Use an online conversion tool like **[mygeodata.cloud](https://mygeodata.cloud/)** (free for small files).
2. **Input:** The GeoPackage file (`.gpkg`) from QGIS.
3. **Output:** Choose **KML** (for Google Maps) or **GeoJSON** (more flexible for developers).
4. **Coordinate System:** Ensure the output is **WGS84 (EPSG:4326)** , the standard for web maps. Most converters handle this automatically.
5. Download the converted file, e.g., `wine_region.kml`.

### Step 5: Publish on Google My Maps

1. Go to **[Google My Maps](https://www.google.com/maps/d/)**.
2. Click on **"Create a new map"**.
3. Click `Add layer > Import` and upload your KML file.
4. Customize the appearance (colors, borders, opacity) to match the wine region's style.
5. Add a title and description to the map.
6. Click **"Share"** to make the map public and obtain a shareable link.

## A Working Example: Ribera del Duero (Spain)

To validate this workflow, it was first applied to the **Ribera del Duero D.O.** in Spain. This region serves as the pilot example for the global project.

- **Region:** Ribera del Duero (Castilla y León, Spain)
- **Number of administrative units:** 77 municipalities
- **Data Source:** IGN Spain (via INSPIRE) - `recintos_municipales_inspire_peninbal_etrs89.csv`
- **Result:** [World Wine Wide Map](https://www.google.com/maps/d/u/0/edit?mid=1CJHfZIoR3TKiEuWkXqIKF3ItGwuLS5s&usp=sharing)

This example proves that the methodology works with real-world, official data.

For comprehensive technical specifications, official cartographic agencies across all 21 countries, Coordinate Reference Systems (CRS), SQL queries, and the grape analysis pipeline, see the full [Methodology Guide](docs/METHODOLOGY.md) (or [Versión en Español](docs/METODOLOGIA.md)).

## Multi-Country Coverage Status 🌍

The **World Wine Wide** project has completed full, authoritative census coverage across **21 sovereign wine nations**, encompassing **763 official wine regions**, **791 QGIS vector layers**, and **670 official legal specification documents (PDFs)**:

| Country | Status | Appellations / Regions | Key Official Classifications | Primary Cartographic Agency | National Registry |
| :--- | :---: | :---: | :--- | :--- | :---: |
| 🇦🇲 **Armenia** | 100% | 5 | PDO (Vayots Dzor, Aragatsotn, Armavir, etc.) | Natural Earth / VWFA | [Registry](docs/ARMENIA/REGISTRO_REGIONS.md) |
| 🇦🇹 **Austria** | 100% | 18 | DAC (Wachau, Kremstal, Kamptal, etc.) | BEV / eAmbrosia | [Registry](docs/AUSTRIA/REGISTRO_DACS.md) |
| 🇧🇬 **Bulgaria** | 100% | 5 | PGI (Danubian Plain, Thracian Lowland, etc.) | Natural Earth / EAVW | [Registry](docs/BULGARIA/REGISTRO_REGIONS.md) |
| 🇭🇷 **Croatia** | 100% | 4 (16 ZOI) | ZOI (Dalmacija, Istra, Slavonija, Bregovita) | Natural Earth / eAmbrosia | [Registry](docs/CROATIA/REGISTRO_ZOI.md) |
| 🇨🇾 **Cyprus** | 100% | 5 | PDO (Commandaria, Krasochoria, etc.) | Natural Earth / eAmbrosia | [Registry](docs/CYPRUS/REGISTRO_PDOS.md) |
| 🇨🇿 **Czech Republic** | 100% | 6 | CHOP / VOC (Znojemská, Mikulovská, etc.) | Natural Earth / ÚKZÚZ | [Registry](docs/CZECH_REPUBLIC/REGISTRO_PODOBLASTI.md) |
| 🇫🇷 **France** | 100% | 325 | AOC (Bordeaux, Bourgogne, Rhône, Loire, etc.) | IGN France / INAO | [Registry](docs/FRANCE/REGISTRO_AOCS.md) |
| 🇬🇪 **Georgia** | 100% | 29 | PDO (Mukuzani, Kindzmarauli, Tsinandali, etc.) | Natural Earth / Sakpatenti | [Registry](docs/GEORGIA/REGISTRO_PDOS.md) |
| 🇩🇪 **Germany** | 100% | 13 | g.U. Anbaugebiete (Mosel, Rheingau, Pfalz, etc.) | BKG / BLE | [Registry](docs/GERMANY/REGISTRO_ANBAUGEBIETE.md) |
| 🇬🇷 **Greece** | 100% | 33 | POP (Naoussa, Nemea, Santorini, etc.) | Natural Earth / YPAAT | [Registry](docs/GREECE/REGISTRO_POPS.md) |
| 🇭🇺 **Hungary** | 100% | 22 | OEM Borvidékek (Tokaj, Villány, Eger, etc.) | Natural Earth / HNT | [Registry](docs/HUNGARY/REGISTRO_OEMS.md) |
| 🇮🇹 **Italy** | 100% | 121 | DOCG & DOC (Barolo, Chianti, Brunello, etc.) | ISTAT / MASAF | [Registry](docs/ITALY/REGISTRO_DOCS.md) |
| 🇱🇧 **Lebanon** | 100% | 4 | GI (Bekaa Valley, Mount Lebanon, Batroun, etc.) | Natural Earth / UVL | [Registry](docs/LEBANON/REGISTRO_TERROIRS.md) |
| 🇲🇩 **Moldova** | 100% | 4 | IGP (Valul lui Traian, Ștefan Vodă, Codru, Divin) | Natural Earth / ONVV | [Registry](docs/MOLDOVA/REGISTRO_IGP.md) |
| 🇵🇹 **Portugal** | 100% | 31 | DOC / DOP (Douro, Dão, Alentejo, Vinho Verde) | DGT / IVV | [Registry](docs/PORTUGAL/REGISTRO_DOCS.md) |
| 🇷🇴 **Romania** | 100% | 8 (37 DOC) | DOC (Dealurile Moldovei, Munteniei, etc.) | Natural Earth / ONVPV | [Registry](docs/ROMANIA/REGISTRO_REGIUNI.md) |
| 🇸🇰 **Slovakia** | 100% | 6 | CHOP (Malokarpatská, Tokaj, Južnoslovenská, etc.) | Natural Earth / eAmbrosia | [Registry](docs/SLOVAKIA/REGISTRO_OBLASTI.md) |
| 🇸🇮 **Slovenia** | 100% | 9 | ZGP (Goriška Brda, Vipavska dolina, Kras, etc.) | Natural Earth / eAmbrosia | [Registry](docs/SLOVENIA/REGISTRO_ZGP.md) |
| 🇪🇸 **Spain** | 100% | 101 | DOCa, DO, VP, VC (Rioja, Ribera, Priorat, etc.) | IGN Spain / MAPA | [Registry](docs/SPAIN/REGISTRO_DOS.md) |
| 🇨🇭 **Switzerland** | 100% | 6 | AOC / DOC (Valais, Vaud, Genève, Ticino, etc.) | Natural Earth / OFAG | [Registry](docs/SWITZERLAND/REGISTRO_REGIONS.md) |
| 🇹🇷 **Turkey** | 100% | 9 | Bölge / GI (Trakya, Urla, Denizli, Kapadokya, etc.) | Natural Earth / TÜRKPATENT | [Registry](docs/TURKEY/REGISTRO_REGIONS.md) |

👉 **For the complete regional descriptions, territorial notes, and wine profiles of each country, see the full [Multi-Country Coverage Report](docs/COVERAGE.md) (or [Versión en Español](docs/COBERTURA.md)).**

**Key metrics:**
* **763 official wine regions** interactive in the web applications with commune-level search, basemap switcher, multi-country and regional filters, and official PDF specification viewers.
* **791 vector layers** systematically arranged in the primary QGIS project (`QGIS/wine_world_wine.qgz`) partitioned into twenty-two national groups: `SPAIN`, `FRANCE`, `PORTUGAL`, `ITALY`, `GERMANY`, `AUSTRIA`, `GREECE`, `HUNGARY`, `GEORGIA`, `CZECH_REPUBLIC`, `SWITZERLAND`, `SLOVENIA`, `CROATIA`, `SLOVAKIA`, `ROMANIA`, `BULGARIA`, `MOLDOVA`, `ARMENIA`, `CYPRUS`, `LEBANON`, `TURKEY`, and `Google`.
* **670 official legal specification documents (PDFs)** archived locally in [`DOWNs/DOCs/`](DOWNs/DOCs/).
* **Dedicated SQL filter libraries** available under `QGIS/<COUNTRY>/SQLs/`.

---

## Building the Global Collection 🚀

With the **Old World wine heritage fully mapped across 21 countries**, the next phase of the **World Wine Wide** project expands into the New World:
* **North America:** United States (California AVAs — Napa Valley, Sonoma, Paso Robles, Santa Barbara; Oregon — Willamette Valley; Washington — Columbia Valley).
* **South America:** Argentina (Mendoza — Uco Valley, Luján de Cuyo; Salta — Cafayate) and Chile (Maipo, Colchagua, Casablanca).
* **Oceania:** Australia (Barossa Valley, McLaren Vale, Margaret River, Yarra Valley) and New Zealand (Marlborough, Central Otago).
* **South Africa:** Western Cape (Stellenbosch, Swartland, Walker Bay).

See our [Global Expansion Guide](docs/GLOBAL_EXPANSION.md) (or [Versión en Español](docs/EXPANSION_GLOBAL.md)) for the detailed architectural plan and contribution guidelines.

---

## License and Attribution

This project is for educational and informational purposes. All data used is from official public sources. Please respect the individual licenses of the data providers.

When using or sharing these maps, attribution to the original data source (e.g., "Administrative boundaries © IGN Spain") is appreciated.

## Contributing

Contributions are welcome! If you have access to official geographic data for a wine region, or if you have a list of administrative units for an appellation, please open an issue or submit a pull request. Together, we can build the definitive map of the world's wine.

**Cheers! 🍷**
