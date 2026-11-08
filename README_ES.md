<p align="center">
  <img src="assets/logo_horizontal.svg" alt="WINE³ai — Mapas Vitivinícolas Mundiales e Inteligencia Territorial" width="480">
</p>

# WINE³ai — World Wide Wine: Mapas Vitivinícolas Mundiales e Inteligencia Territorial 🍷

[English Version](README.md) | **Versión en Español**

## Visión General del Proyecto

**WINE³ai** (*World Wide Wine*) es un proyecto geoespacial abierto y colaborativo con un objetivo claro y ambicioso: **crear mapas precisos, fidedignos e interactivos de todas las regiones vitivinícolas del mundo, integrando capas climáticas y análisis varietal**.

Desde las colinas de Burdeos y Borgoña hasta los valles de Napa y Rioja, pasando por las terrazas del Priorat o las llanuras de Mendoza, el proyecto busca ofrecer una referencia visual rigurosa para entusiastas, estudiantes, sumilleres y profesionales del vino.

Para lograrlo, combinamos **fuentes oficiales indiscutibles**:
1. Los **Pliegos de Condiciones oficiales** aprobados por los Consejos Reguladores, Ministerios de Agricultura y la Unión Europea (*eAmbrosia*).
2. La **cartografía de delimitaciones territoriales oficiales** de los institutos geográficos nacionales (en España, el **IGN** bajo directiva europea **INSPIRE**).

---

## 🗺️ Visualización Interactiva

El resultado del proyecto son **mapas web interactivos** que muestran con total precisión los límites de cada denominación de origen, zonas climáticas mundiales y variedades de uva:

👉 **Aplicación Web Interactiva Oficial:** [https://jreyes13.github.io/wine3ai/](https://jreyes13.github.io/wine3ai/)  
👉 **Explorador Global de Variedades de Uva:** [https://jreyes13.github.io/wine3ai/grapes.html](https://jreyes13.github.io/wine3ai/grapes.html)  
👉 **Explorar el proyecto en Atlas:** [WINE³ai Map en Atlas.co](https://app.atlas.co/projects/iRfhgtNFAbVm6zHZL3bN?loc=-2.7334%2C39.9785%2C6.0441z)

---

## 🌐 El Reto: Obtención de Datos Cartográficos Globales (*Sourcing Global Data*)

Cada país gestiona su propia cartografía oficial de forma soberana. No existe una fuente única mundial para las delimitaciones administrativas y vitivinícolas. El principio fundacional de **World Wide Wine** es identificar y procesar exclusivamente las **fuentes oficiales gubernamentales e institucionales más autorizadas**:

### A. Fuentes Oficiales de los 51 Países Consolidados

| País | Organismo Cartográfico Oficial / Portal | Nivel de Entidad Base | Sistema de Coordenadas Nativo (CRS) | Autoridad Vitivinícola Reguladora |
| :--- | :--- | :--- | :--- | :--- |
| 🇩🇪 **Alemania** | BKG (Bundesamt für Kartographie und Geodäsie) | Gemeinden / Kreise | ETRS89 / UTM 32N (EPSG:25832) | BLE / *Weinverordnung* |
| 🇦🇷 **Argentina** | IGN Argentina | Departamentos / Distritos | POSGAR 2007 (EPSG:5343) | INV (Instituto Nacional de Vitivinicultura) |
| 🇦🇲 **Armenia** | Cadastre Committee / Natural Earth | Marzer (Provincias) | ArmRef02 / WGS84 | VWFA / Min. de Economía |
| 🇦🇺 **Australia** | Geoscience Australia / Natural Earth | GIs / Zonas de Gobierno Local | GDA2020 (EPSG:7844) | Wine Australia |
| 🇦🇹 **Austria** | BEV (Bundesamt für Eich- und Vermessungswesen) | Gemeinden / Bezirke | MGI / Austria Lambert (EPSG:31287) | BML / eAmbrosia |
| 🇦🇿 **Azerbaiyán** | Comité Estatal de Asuntos de la Propiedad / Natural Earth | Rayones / Municipios | WGS84 / UTM 38N (EPSG:32638) | Min. de Agricultura / Asociación del Vino de Azerbaiyán |
| 🇧🇪 **Bélgica** | NGI Bélgica (IGN) | Communes / Gewesten | Belgian Lambert 2008 (EPSG:3812) | FOD Economie / eAmbrosia |
| 🇧🇴 **Bolivia** | IGM Bolivia / Natural Earth | Provincias / Municipios | WGS84 / UTM 20S (EPSG:32720) | MDRyT / Cenavit |
| 🇧🇦 **Bosnia y Herzegovina** | FGU / RGU / Eurostat | Opštine / Gradovi | MGI 1901 / Balcanes (EPSG:31276) | Agencia de Seguridad Alimentaria / eAmbrosia |
| 🇧🇷 **Brasil** | IBGE (Instituto Brasileiro de Geografia e Estatística) | Municípios / Distritos | SIRGAS 2000 (EPSG:4674) | MAPA / Embrapa Uva e Vinho |
| 🇧🇬 **Bulgaria** | AGKK / Natural Earth | Oblasti / Obshtini | BGS2005 (EPSG:7801) | EAVW (Agencia Búlgara de la Viña y el Vino) |
| 🇨🇦 **Canadá** | Statistics Canada / Natural Earth | CSD (Census Subdivisions) / Regions | NAD83 / StatCan Lambert (EPSG:3347) | VQA Ontario / BC VQA |
| 🇨🇱 **Chile** | IDE Chile / IGM | Comunas / Provincias | SIRGAS-Chile (EPSG:5360) | SAG (Servicio Agrícola y Ganadero) |
| 🇨🇳 **China** | National Geomatics Center of China (NGCC) | Prefecturas / Condados | CGCS2000 (EPSG:4490) | SAMR / Oficinas Vitivinícolas Provinciales |
| 🇨🇾 **Chipre** | Dept. of Lands and Surveys / Natural Earth | Eparquías / Comunidades | CGRS93 (EPSG:6312) | Departamento de Agricultura |
| 🇭🇷 **Croacia** | DGU (Državna geodetska uprava) | Županije / Gradovi | HTRS96/TM (EPSG:3765) | Min. Poljoprivrede / eAmbrosia |
| 🇸🇰 **Eslovaquia** | ÚGKK SR / Eurostat | Kraje / Okresy | S-JTSK (EPSG:5514) | Min. Pôdohospodárstva |
| 🇸🇮 **Eslovenia** | GURS (Autoridad Cartográfica y Geodésica) | Občine / Upravne enote | D96/TM (EPSG:3794) | MKGP / eAmbrosia |
| 🇪🇸 **España** | IGN España (INSPIRE) | Municipios (`recintos_municipales`) | ETRS89 (EPSG:4258) / REGCAN95 | MAPA / Consejos Reguladores |
| 🇺🇸 **Estados Unidos** | US Census Bureau (TIGER/Line) | Condados / Límites TTB AVA | NAD83 / WGS84 | TTB (Alcohol and Tobacco Tax and Trade Bureau) |
| 🇫🇷 **Francia** | IGN France (BD CARTO® / Géoportail) | Communes / Cantons | RGF93 / Lambert-93 (EPSG:2154) | INAO (*Cahiers des charges*) |
| 🇬🇪 **Georgia** | NAPR (Agencia Nacional del Registro Público) | Municipios / Rayones | WGS84 / UTM 38N (EPSG:32638) | Agencia Nacional del Vino / Sakpatenti |
| 🇬🇷 **Grecia** | ELSTAT (Autoridad Estadística Helénica) | Prefecturas / Municipios | GGRS87 (EPSG:2100) | YPAAT (Min. de Desarrollo Rural) |
| 🇭🇺 **Hungría** | Lechner Tudásközpont / FÖMI | Condados / Asentamientos | EOV / HD72 (EPSG:23700) | HNT / NÉBIH |
| 🇮🇳 **India** | Survey of India / Natural Earth | Talukas / Distritos | WGS84 / UTM 43N (EPSG:32643) | Intellectual Property India / GI Registry |
| 🇮🇱 **Israel** | Survey of Israel (MAPI) | Distritos / Regiones Naturales | Israel TM Grid (EPSG:2039) | Consejo Regulador del Vino de Israel |
| 🇮🇹 **Italia** | ISTAT (Istituto Nazionale di Statistica) | Comuni | Roma40 / Gauss-Boaga (EPSG:3003) | MASAF (*Disciplinari*) |
| 🇯🇵 **Japón** | Geospatial Information Authority of Japan (GSI) | Prefecturas / Municipios | JGD2011 (EPSG:6668) | National Tax Agency (NTA) / GI Japan |
| 🇱🇧 **Líbano** | Dirección de Asuntos Geográficos (DAG) | Gobernaciones / Distritos | Deir ez Zor / Levant (EPSG:22770) | Union Vinicole du Liban (UVL) |
| 🇱🇺 **Luxemburgo** | ACT (Administration du Cadastre et de la Topographie) | Communes / Cantones | LUREF (EPSG:2169) | Min. de l'Agriculture / IVV |
| 🇲🇰 **Macedonia del Norte** | AREC (Catastro de Bienes Inmuebles) | Opštini (Municipios) | MGI 1901 / Balcanes (EPSG:31277) | Ministerio de Agricultura |
| 🇲🇹 **Malta** | Planning Authority Malta / Natural Earth | Consejos Locales / Islas | ED50 / Malta UTM 33N (EPSG:23033) | Unidad de Viticultura y Enología (MAFA) |
| 🇲🇦 **Marruecos** | ANCFCC (Cadastre et Cartographie) | Provincias / Círculos | Merchich / Nord Maroc (EPSG:26191) | ONSSA (Min. de l'Agriculture) |
| 🇲🇽 **México** | INEGI (Instituto Nacional de Estadística y Geografía) | Municipios | Marco Geoestadístico / ITRF2008 (EPSG:6372) | CMV / SADER |
| 🇲🇩 **Moldavia** | ARFC (Agencia de Catastro) / Natural Earth | Raioane | Moldref 99 (EPSG:4026) | ONVV |
| 🇲🇪 **Montenegro** | Uprava za nekretnine / Eurostat | Opštine (Municipios) | MGI 1901 / Balcanes (EPSG:31276) | Ministerio de Agricultura y Desarrollo Rural |
| 🇳🇿 **Nueva Zelanda** | LINZ (Land Information New Zealand) / Natural Earth | GIs / Distritos Territoriales | NZGD2000 (EPSG:2193) | New Zealand Winegrowers |
| 🇳🇱 **Países Bajos** | Kadaster (PDOK) | Gemeenten / Provincias | Amersfoort / RD New (EPSG:28992) | RVO / eAmbrosia |
| 🇵🇪 **Perú** | IGN Perú / INEI | Provincias / Distritos | WGS84 / UTM 18S (EPSG:32718) | INDECOPI / Min. de la Producción |
| 🇵🇱 **Polonia** | GUGiK (Oficina Central de Geodesia y Cartografía) | Gminy / Powiaty | PL-1992 (EPSG:2180) | KOWR / Min. Rolnictwa |
| 🇵🇹 **Portugal** | DGT (Direção-Geral do Território - CAOP) | Concelhos / Freguesias | ETRS89 / PT-TM06 (EPSG:3763) | IVV (*Cadernos de especificações*) |
| 🇬🇧 **Reino Unido** | Ordnance Survey (OS Boundary-Line™) | Counties / Unitary Authorities | British National Grid (EPSG:27700) | DEFRA / Food Standards Agency |
| 🇨🇿 **República Checa** | ČÚZK (Administración Estatal de Agrimensura) | Okresy / Kraje | S-JTSK (EPSG:5514) | ÚKZÚZ |
| 🇷🇴 **Rumanía** | ANCPI / Eurostat | Județe / Comuni | Dealul Piscului 1970 (EPSG:31700) | ONVPV |
| 🇷🇸 **Serbia** | RGZ (Autoridad Geodésica de la República) | Opštine / Gradovi | MGI 1901 / Balcanes (EPSG:31277) | Min. Poljoprivrede, Šumarstva i Vodoprivrede |
| 🇿🇦 **Sudáfrica** | NGI (National Geo-spatial Information) / Natural Earth | Municipios / WOs | Hartebeesthoek94 (EPSG:2048) | SAWIS (Wine Industry Information) |
| 🇨🇭 **Suiza** | swisstopo (Oficina Federal de Topografía) | Cantones / Comunas | CH1903+ / LV95 (EPSG:2056) | OFAG / BLW |
| 🇹🇳 **Túnez** | OTC (Office de la Topographie et du Cadastre) | Gobernaciones / Delegaciones | Carthage / UTM 32N (EPSG:22332) | DGPA / Min. de l'Agriculture |
| 🇹🇷 **Turquía** | Harita Genel Müdürlüğü (HGM) / Natural Earth | İller (Provincias) / İlçeler | TUREF (EPSG:5254) / WGS84 | Tarım ve Orman Bak. / TÜRKPATENT |
| 🇺🇦 **Ucrania** | StateGeoCadastre / Natural Earth | Rayones / Hromadas | UCS-2000 (EPSG:5563) | Min. de Política Agraria y Alimentación |
| 🇺🇾 **Uruguay** | SGM Uruguay / IDE Uy | Departamentos / Secciones | BROU 1928 / UTM 21S (EPSG:5382) | INAVI (Instituto Nacional de Vitivinicultura) |

> **Estándar Cartográfico:** Todas las capas vectoriales se exportan y publican reproyectadas al sistema universal **WGS84 (EPSG:4326)** para garantizar interoperabilidad SIG y rendimiento web.

---

## 🚀 Metodología en 5 Pasos

El flujo de trabajo es reproducible y aplicable a cualquier país:

1. **Obtención del Pliego de Condiciones Oficial:** Recuperar el documento normativo vigente que delimita la zona de producción.
2. **Descarga de Datos Cartográficos Oficiales:** Descargar los recintos municipales oficiales de la agencia geográfica nacional.
3. **Normalización y Filtrado en QGIS:** Cotejar los términos municipales con el nomenclátor oficial (`NAMEUNIT`) y aplicar expresiones SQL de selección:
   ```sql
   "NAMEUNIT" IN ('Municipio1', 'Municipio2', ...)
   ```
4. **Generación de Capas Abiertas (GeoPackage / GeoJSON):** Exportar los objetos seleccionados preservando el sistema de referencia espacial (ETRS89 / WGS84).
5. **Publicación y Estilo en Atlas.co:** Subir las capas vectoriales, asignar paletas cromáticas armónicas y configurar leyendas y tooltips interactivos.

Para ver los detalles técnicos y particularidades cartográficas (pedanías, nombres bilingües, etc.), consulta la [Guía Metodológica Completa](docs/METODOLOGIA.md).

---

## 📊 Estado Actual: Cobertura Multipaís

El proyecto **WINE³ai** cuenta con una cobertura censal oficial completada al 100% en **51 naciones vitivinícolas soberanas**, que integran **867 regiones vitivinícolas oficiales**, **900+ capas vectoriales SIG** y **760+ pliegos oficiales de condiciones (PDFs)**:

| País | Estado | Denominaciones / Regiones | Figuras Oficiales Clave | Organismo Cartográfico Base | Registro Nacional |
| :--- | :---: | :---: | :--- | :--- | :---: |
| 🇩🇪 **Alemania** | 100% | 13 | g.U. Anbaugebiete (Mosel, Rheingau, Pfalz, etc.) | BKG / BLE | [Registro](docs/GERMANY/REGISTRO_ANBAUGEBIETE.md) |
| 🇦🇷 **Argentina** | 100% | 7 | IG / DOC (Valle de Uco, Luján de Cuyo, Maipú, Cafayate, etc.) | IGN Argentina / INV | [Registro](docs/COBERTURA.md) |
| 🇦🇲 **Armenia** | 100% | 5 | PDO (Vayots Dzor, Aragatsotn, Armavir, etc.) | Natural Earth / VWFA | [Registro](docs/ARMENIA/REGISTRO_REGIONS.md) |
| 🇦🇺 **Australia** | 100% | 8 | GI (Barossa Valley, McLaren Vale, Margaret River, Yarra Valley, Coonawarra, etc.) | Geoscience Australia / Wine Australia | [Registro](docs/COBERTURA.md) |
| 🇦🇹 **Austria** | 100% | 18 | DAC (Wachau, Kremstal, Kamptal, etc.) | BEV / eAmbrosia | [Registro](docs/AUSTRIA/REGISTRO_DACS.md) |
| 🇦🇿 **Azerbaiyán** | 100% | 1 | Qorunan Coğrafi Göstərici / GI (Ganja & Goygol) | Natural Earth / Min. de Agricultura | [Registro](docs/COBERTURA.md) |
| 🇧🇪 **Bélgica** | 100% | 2 | DOP (Côtes de Sambre et Meuse, Hagelandse Wijn) | NGI Bélgica / eAmbrosia | [Registro](docs/COBERTURA.md) |
| 🇧🇴 **Bolivia** | 100% | 2 | G.I. (Valle Central de Tarija, Valle de Cinti) | IGM Bolivia / MDRyT / Cenavit | [Registro](docs/COBERTURA.md) |
| 🇧🇦 **Bosnia y Herzegovina** | 100% | 1 | ZOI (Hercegovina) | FGU / eAmbrosia | [Registro](docs/COBERTURA.md) |
| 🇧🇷 **Brasil** | 100% | 3 | D.O. / I.P. (Vale dos Vinhedos, Campanha Gaúcha, Pinto Bandeira) | IBGE / Embrapa / MAPA | [Registro](docs/COBERTURA.md) |
| 🇧🇬 **Bulgaria** | 100% | 5 | PGI (Llanura Danubiana, Tracia, etc.) | Natural Earth / EAVW | [Registro](docs/BULGARIA/REGISTRO_REGIONS.md) |
| 🇨🇦 **Canadá** | 100% | 3 | VQA (Niagara Peninsula, Okanagan Valley, Prince Edward County) | StatCan / VQA Ontario / BC VQA | [Registro](docs/COBERTURA.md) |
| 🇨🇱 **Chile** | 100% | 8 | D.O. (Valle del Maipo, Colchagua, Casablanca, Leyda, Peumo, etc.) | IDE Chile / SAG | [Registro](docs/COBERTURA.md) |
| 🇨🇳 **China** | 100% | 4 | National GI (Ningxia, Shandong Yantai, Xinjiang, Yunnan Shangri-La) | NGCC / SAMR | [Registro](docs/COBERTURA.md) |
| 🇨🇾 **Chipre** | 100% | 5 | PDO (Commandaria, Krasochoria, etc.) | Natural Earth / eAmbrosia | [Registro](docs/CYPRUS/REGISTRO_PDOS.md) |
| 🇭🇷 **Croacia** | 100% | 4 (16 ZOI) | ZOI (Dalmacija, Istra, Slavonija, Bregovita) | Natural Earth / eAmbrosia | [Registro](docs/CROATIA/REGISTRO_ZOI.md) |
| 🇸🇰 **Eslovaquia** | 100% | 6 | CHOP (Malokarpatská, Tokaj, etc.) | Natural Earth / eAmbrosia | [Registro](docs/SLOVAKIA/REGISTRO_OBLASTI.md) |
| 🇸🇮 **Eslovenia** | 100% | 9 | ZGP (Goriška Brda, Vipavska dolina, Kras, etc.) | Natural Earth / eAmbrosia | [Registro](docs/SLOVENIA/REGISTRO_ZGP.md) |
| 🇪🇸 **España** | 100% | 101 | DOCa, DO, VP, VC (Rioja, Ribera, Priorat, etc.) | IGN España / MAPA | [Registro](docs/SPAIN/REGISTRO_DOS.md) |
| 🇺🇸 **Estados Unidos** | 100% | 15 | AVA (Napa Valley, Sonoma County, Paso Robles, Willamette, Columbia Valley, etc.) | US Census Bureau / TTB | [Registro](docs/COBERTURA.md) |
| 🇫🇷 **Francia** | 100% | 325 | AOC (Burdeos, Borgoña, Ródano, Loira, etc.) | IGN France / INAO | [Registro](docs/FRANCE/REGISTRO_AOCS.md) |
| 🇬🇪 **Georgia** | 100% | 29 | PDO (Mukuzani, Kindzmarauli, Tsinandali, etc.) | Natural Earth / Sakpatenti | [Registro](docs/GEORGIA/REGISTRO_PDOS.md) |
| 🇬🇷 **Grecia** | 100% | 33 | POP (Naoussa, Nemea, Santorini, etc.) | Natural Earth / YPAAT | [Registro](docs/GREECE/REGISTRO_POPS.md) |
| 🇭🇺 **Hungría** | 100% | 22 | OEM Borvidékek (Tokaj, Villány, Eger, etc.) | Natural Earth / HNT | [Registro](docs/HUNGARY/REGISTRO_OEMS.md) |
| 🇮🇳 **India** | 100% | 1 | GI (Nashik Valley Wine) | Survey of India / GI Registry | [Registro](docs/COBERTURA.md) |
| 🇮🇱 **Israel** | 100% | 2 | Región Vitivinícola (Judean Hills, Upper Galilee & Golan) | Survey of Israel / Wine Board | [Registro](docs/COBERTURA.md) |
| 🇮🇹 **Italia** | 100% | 121 | DOCG y DOC (Barolo, Chianti, Brunello, etc.) | ISTAT / MASAF | [Registro](docs/ITALY/REGISTRO_DOCS.md) |
| 🇯🇵 **Japón** | 100% | 2 | GI (Yamanashi, Nagano) | GSI / NTA GI Japan | [Registro](docs/COBERTURA.md) |
| 🇱🇧 **Líbano** | 100% | 4 | GI (Valle de la Becá, Monte Líbano, etc.) | Natural Earth / UVL | [Registro](docs/LEBANON/REGISTRO_TERROIRS.md) |
| 🇱🇺 **Luxemburgo** | 100% | 1 | AOP (Moselle Luxembourgeoise) | ACT / IVV | [Registro](docs/COBERTURA.md) |
| 🇲🇰 **Macedonia del Norte** | 100% | 3 | PDO / ZOI (Tikveš, Pčinja-Osogovo, Pelagonija) | AREC / Min. de Agricultura | [Registro](docs/COBERTURA.md) |
| 🇲🇹 **Malta** | 100% | 1 | DOK (DOK Malta & DOK Gozo) | PA Malta / eAmbrosia | [Registro](docs/COBERTURA.md) |
| 🇲🇦 **Marruecos** | 100% | 2 | AOG (Guerrouane, Beni M'Tir) | ANCFCC / ONSSA | [Registro](docs/COBERTURA.md) |
| 🇲🇽 **México** | 100% | 3 | Región Vitivinícola (Valle de Guadalupe, Valle de Parras, Querétaro) | INEGI / CMV / SADER | [Registro](docs/COBERTURA.md) |
| 🇲🇩 **Moldavia** | 100% | 4 | IGP (Valul lui Traian, Ștefan Vodă, Codru, Divin) | Natural Earth / ONVV | [Registro](docs/MOLDOVA/REGISTRO_IGP.md) |
| 🇲🇪 **Montenegro** | 100% | 2 | ZOI / GI (Skadarsko jezero, Crnogorsko primorje) | Uprava za nekretnine / Min. Agr. | [Registro](docs/COBERTURA.md) |
| 🇳🇿 **Nueva Zelanda** | 100% | 4 | GI (Marlborough, Central Otago, Hawke's Bay, Martinborough) | LINZ / NZ Winegrowers | [Registro](docs/COBERTURA.md) |
| 🇳🇱 **Países Bajos** | 100% | 2 | BOB / DOP (Mergelland / Zuid-Limburg, Achterhoek - Winterswijk) | Kadaster / eAmbrosia | [Registro](docs/COBERTURA.md) |
| 🇵🇪 **Perú** | 100% | 2 | D.O. (Valle de Ica, Valle de Moquegua) | IGN Perú / INDECOPI | [Registro](docs/COBERTURA.md) |
| 🇵🇱 **Polonia** | 100% | 2 | Región Vitivinícola (Zielona Góra, Małopolska & Podkarpacie) | GUGiK / KOWR | [Registro](docs/COBERTURA.md) |
| 🇵🇹 **Portugal** | 100% | 31 | DOC / DOP (Douro, Dão, Alentejo, Vinho Verde) | DGT / IVV | [Registro](docs/PORTUGAL/REGISTRO_DOCS.md) |
| 🇬🇧 **Reino Unido** | 100% | 3 | PDO (Sussex, English Wine, Welsh Wine) | OS / DEFRA | [Registro](docs/COBERTURA.md) |
| 🇨🇿 **República Checa** | 100% | 6 | CHOP / VOC (Znojemská, Mikulovská, etc.) | Natural Earth / ÚKZÚZ | [Registro](docs/CZECH_REPUBLIC/REGISTRO_PODOBLASTI.md) |
| 🇷🇴 **Rumanía** | 100% | 8 (37 DOC) | DOC (Dealurile Moldovei, Munteniei, etc.) | Natural Earth / ONVPV | [Registro](docs/ROMANIA/REGISTRO_REGIUNI.md) |
| 🇷🇸 **Serbia** | 100% | 5 | KPK / PDO (Fruška Gora, Šumadija, Župa, etc.) | RGZ / Min. Poljoprivrede | [Registro](docs/COBERTURA.md) |
| 🇿🇦 **Sudáfrica** | 100% | 7 | WO (Stellenbosch, Swartland, Paarl, Walker Bay, Franschhoek, etc.) | NGI / SAWIS | [Registro](docs/COBERTURA.md) |
| 🇨🇭 **Suiza** | 100% | 6 | AOC / DOC (Valais, Vaud, Genève, Ticino, etc.) | Natural Earth / OFAG | [Registry](docs/SWITZERLAND/REGISTRO_REGIONS.md) |
| 🇹🇳 **Túnez** | 100% | 2 | AOC (Grand Cru Mornag, Coteaux de Kélibia) | OTC / DGPA | [Registro](docs/COBERTURA.md) |
| 🇹🇷 **Turquía** | 100% | 9 | Bölge / GI (Trakya, Urla, Denizli, Kapadokya, etc.) | Natural Earth / TÜRKPATENT | [Registro](docs/TURKEY/REGISTRO_REGIONS.md) |
| 🇺🇦 **Ucrania** | 100% | 2 | Indicación Geográfica (Odesa & Besarabia, Transcarpatia) | StateGeoCadastre / Min. Agrario | [Registro](docs/COBERTURA.md) |
| 🇺🇾 **Uruguay** | 100% | 4 | Región Vitivinícola (Canelones, Maldonado, Colonia, Rivera) | SGM Uruguay / INAVI | [Registro](docs/COBERTURA.md) |

👉 **Para consultar las fichas descriptivas completas, zonificaciones y notas vitivinícolas de cada país, accede al [Informe Detallado de Cobertura Multipaís](docs/COBERTURA.md) (o [English Version](docs/COVERAGE.md)).**

**En números:**
* **867 regiones vitivinícolas oficiales** integradas en el visor web interactivo con filtros dinámicos en cascada por país, categoría y buscador instantáneo de municipios.
* **900+ capas vectoriales** estructuradas en el proyecto maestro QGIS (`QGIS/wine_world_wine.qgz`) divididas en grupos nacionales.
* **760+ pliegos oficiales (PDFs)** archivados en local en [`DOWNs/DOCs/`](DOWNs/DOCs/).
* **Librerías SQL completas** para cada país en `QGIS/<PAIS>/SQLs/`.

---

## 🌍 Expansión Global y Próximas Fronteras 🚀

Tras consolidar la cartografía del **Viejo Mundo y las grandes potencias vitivinícolas del Nuevo Mundo en 51 países** (incluyendo España, Francia, Italia, EE.UU., Argentina, Chile, Sudáfrica, Australia, Nueva Zelanda, Uruguay, Brasil, Canadá y México), **WINE³ai** proporciona una cobertura integral y unificada de la viticultura mundial.

Consulta nuestra [Guía de Expansión Global](docs/EXPANSION_GLOBAL.md) (o [English Version](docs/GLOBAL_EXPANSION.md)) para conocer la arquitectura modular y las pautas para proponer o incorporar nuevas regiones.

---

## 📄 Licencia y Atribución

Este proyecto tiene fines educativos, divulgativos y de investigación geográfica abierta. Todos los datos geográficos se basan en fuentes públicas oficiales:
- Cartografía municipal: *© Instituto Geográfico Nacional de España (IGN)*.
- Pliegos de condiciones: *Ministerio de Agricultura, Pesca y Alimentación (MAPA) y Consejos Reguladores*.

¡Salud y buen vino! 🍷
