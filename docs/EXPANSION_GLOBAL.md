# Guía de Expansión Global y Próximas Fronteras 🌍

[English Version](GLOBAL_EXPANSION.md) | **Versión en Español**

Este documento establece la arquitectura modular, técnica y colaborativa para continuar escalando **WINE³ai** (anteriormente *World Wine Wide*) a escala planetaria, documentando los hitos ya consolidados en el **Viejo Mundo** y guiando la integración sistemática de las regiones vitivinícolas del **Nuevo Mundo**.

---

## 1. Estado de la Colección y Arquitectura Consolidada

El proyecto ha completado de forma exhaustiva el censo oficial de **21 naciones vitivinícolas europeas, de Anatolia y de la cuenca mediterránea/caucásica**:

| Eje Territorial | Países Completados (100% Censo Oficial) | Regiones Demarcadas |
| :--- | :--- | :---: |
| **Europa Occidental e Ibérica** | 🇪🇸 España, 🇵🇹 Portugal, 🇫🇷 Francia, 🇮🇹 Italia | 578 DOs / AOCs / DOCGs |
| **Europa Central y Alpino-Adriática** | 🇩🇪 Alemania, 🇦🇹 Austria, 🇨🇭 Suiza, 🇸🇮 Eslovenia, 🇭🇷 Croacia, 🇨🇿 República Checa, 🇸🇰 Eslovaquia | 72 g.U. / DAC / ZGP / CHOP |
| **Mar Negro y Centroeuropa Oriental** | 🇭🇺 Hungría, 🇷🇴 Rumanía, 🇧🇬 Bulgaria, 🇲🇩 Moldavia | 39 Borvidékek / DOC / PGI / IGP |
| **Cáucaso Arqueológico, Anatolia y Levante** | 🇬🇪 Georgia, 🇬🇷 Grecia, 🇦🇲 Armenia, 🇨🇾 Chipre, 🇱🇧 Líbano, 🇹🇷 Turquía | 74 PDOs / POPs / GIs / Terruños |
| **Total Global Consolidado** | **21 Naciones Soberanas** | **763 Regiones Oficiales** |

### Estructura de Directorios Estandarizada
El repositorio organiza todos sus activos conforme a una jerarquía modular por país:

```
wine3ai/
├── index.html                   # Visor cartográfico web principal (MapLibre GL JS)
├── grapes.html                  # Analizador global de variedades de uva (gráficos circulares y tipología)
├── README.md                    # Documentación general en inglés (con tabla resumen y enlaces)
├── README_ES.md                 # Documentación general en español
├── data/                        # Datasets optimizados para producción web
│   ├── spain_wine_regions.geojson # 754 regiones vitivinícolas con polígonos, uvas y metadatos
│   ├── grape_varieties.json     # Base de datos de 675 variedades de uva normalizadas
│   └── *.js                     # Envoltorios JS para soporte local (file:// sin CORS)
├── docs/                        # Informes técnicos, metodológicos y registros nacionales
│   ├── COVERAGE.md              # Informe exhaustivo de cobertura en inglés
│   ├── COBERTURA.md             # Informe exhaustivo de cobertura en español
│   ├── METHODOLOGY.md           # Metodología técnica en inglés
│   ├── METODOLOGIA.md           # Metodología técnica en español
│   ├── GLOBAL_EXPANSION.md      # Guía de escalado en inglés
│   ├── EXPANSION_GLOBAL.md      # Guía de escalado en español
│   ├── SPAIN/ ... SWITZERLAND/  # 20 carpetas nacionales con sus registros detallados
├── DOWNs/                       # Repositorio de fuentes primarias
│   ├── DOCs/<PAIS>/             # 661 pliegos oficiales en PDF ordenados por país
│   └── natural_earth_vector/    # Cartografía administrativa vectorial de base
├── QGIS/                        # Capas SIG vectoriales (.gpkg) y proyectos .qgz
│   ├── wine_world_wine.qgz      # Proyecto QGIS maestro (782 capas en 21 grupos)
│   ├── <PAIS>/                  # Capas GeoPackage organizadas por país
│   └── <PAIS>/SQLs/             # Librerías de consultas SQL para filtros municipales
└── web/                         # Réplica sincronizada para despliegue web estático
```

---

## 2. La Próxima Frontera: El Nuevo Mundo Vitivinícola 🍷

Completada la cartografía del Viejo Mundo, la hoja de ruta del proyecto enfoca su expansión hacia las regiones emblemáticas de las Américas, Oceanía y Sudáfrica:

### 🇺🇸 Estados Unidos
* **Organismo Normativo:** **Alcohol and Tobacco Tax and Trade Bureau (TTB)** — *American Viticultural Areas (AVAs)* reguladas bajo el Título 27 del Código de Regulaciones Federales (27 CFR Part 9).
* **Cartografía Base:** **US Census Bureau (TIGER/Line)** a nivel de Condados (*Counties*) y Límites AVA vectoriales del TTB.
* **Zonas Prioritarias:**
  * **California:** Napa Valley (y sus 16 sub-AVAs: Oakville, Rutherford, Stags Leap District, Howell Mountain, Mount Veeder, Los Carneros), Sonoma County (Russian River Valley, Alexander Valley, Sonoma Coast, Dry Creek Valley), Paso Robles, Santa Barbara County (Sta. Rita Hills, Santa Maria Valley).
  * **Oregón:** Willamette Valley (Dundee Hills, Ribbon Ridge, Eola-Amity Hills, Yamhill-Carlton).
  * **Washington:** Columbia Valley, Walla Walla Valley, Red Mountain, Yakima Valley.

### 🇦🇷 Argentina
* **Organismo Normativo:** **Instituto Nacional de Vitivinicultura (INV)** — *Indicaciones Geográficas (IG)* y *Denominaciones de Origen Controlada (DOC)* (Ley 25.163).
* **Cartografía Base:** **Instituto Geográfico Nacional de Argentina (IGN)** a nivel de Departamentos y Distritos.
* **Zonas Prioritarias:**
  * **Mendoza:** Valle de Uco (Gualtallary, Paraje Altamira, San Pablo, Los Chacayes, Vista Flores), Luján de Cuyo (Las Compuertas, Vistalba, Agrelo, Perdriel), Maipú (Barrancas).
  * **Salta & Valles Calchaquíes:** Cafayate, Molinos, Cachi (viñedos extremos de altura hasta 3.111 m).
  * **San Juan:** Valle de Pedernal, Valle de Calingasta.
  * **Patagonia:** Río Negro (Alto Valle) y Neuquén (San Patricio del Chañar).

### 🇨🇱 Chile
* **Organismo Normativo:** **Servicio Agrícola y Ganadero (SAG)** — *Denominaciones de Origen (DO)* reguladas por el Decreto 464 de Zonificación Vitícola y sus complementos (*Costa, Entre Cordilleras, Andes*).
* **Cartografía Base:** **Instituto Geográfico Militar (IGM Chile)** y división político-administrativa comunal/provincial.
* **Zonas Prioritarias:**
  * **Región Vitícola del Valle Central:** Valle del Maipo (Maipo Alto, Pirque, Puente Alto), Valle de Colchagua (Apalta, Los Lingues), Valle de Cachapoal (Peumo), Valle de Curicó, Valle del Maule.
  * **Valles Costeros:** Valle de Casablanca, Valle de Leyda, Valle de San Antonio, Valle del Limarí.
  * **Valles Australes y de Secano:** Valle del Itata (cepas patrimoniales País y Cinsault), Valle del Bío-Bío.

### 🇦🇺 Australia
* **Organismo Normativo:** **Wine Australia** — *Geographical Indications (GI)* bajo la *Wine Australia Act 2013*.
* **Cartografía Base:** **Geoscience Australia** y el *Register of Protected GIs*.
* **Zonas Prioritarias:**
  * **South Australia:** Barossa Valley, Eden Valley, McLaren Vale, Clare Valley, Coonawarra, Adelaide Hills.
  * **Western Australia:** Margaret River, Great Southern.
  * **Victoria:** Yarra Valley, Mornington Peninsula, Heathcote, Rutherglen.
  * **New South Wales:** Hunter Valley.

### 🇿🇦 Sudáfrica
* **Organismo Normativo:** **South African Wine Industry Information and Systems (SAWIS)** — Sistema *Wine of Origin (WO)* regulado por la *Liquor Products Act 60 of 1989*.
* **Cartografía Base:** **Municipal Demarcation Board (MDB)** y cartografía de Distritos y Wards de SAWIS.
* **Zonas Prioritarias:**
  * **Coastal Region:** Stellenbosch, Paarl, Swartland, Franschhoek, Constantia, Durbanville.
  * **Cape South Coast:** Walker Bay (Hemel-en-Aarde), Elgin.
  * **Breede River Valley:** Robertson.

### 🇳🇿 Nueva Zelanda
* **Organismo Normativo:** **New Zealand Winegrowers** y la *Intellectual Property Office of New Zealand (IPONZ)* — *Geographical Indications (Registration) Act 2016*.
* **Cartografía Base:** **Land Information New Zealand (LINZ)**.
* **Zonas Prioritarias:**
  * **Isla Sur:** Marlborough (Wairau Valley, Awatere Valley), Central Otago (Bannockburn, Gibbston, Wanaka), Nelson, Waipara Valley.
  * **Isla Norte:** Hawke's Bay (Gimblett Gravels, Bridge Pa), Martinborough / Wairarapa.

---

## 3. Protocolo Estándar para Integrar un Nuevo País o Denominación

Para asegurar la máxima rigurosidad y compatibilidad con el ecosistema de **World Wine Wide**, cualquier nueva incorporación debe seguir este proceso de cinco pasos:

```
[1. Pliego Oficial PDF] ──> [2. Cartografía Oficial] ──> [3. Filtrado SQL en QGIS]
                                                                  │
[5. Publicación Web] <── [4. Exportación GeoJSON / GPKG] <────────┘
```

1. **Obtención del Pliego Oficial:** Descargar el documento legal normativo que delimita la denominación y archivarlo como PDF en `DOWNs/DOCs/<PAIS>/`.
2. **Adquisición de Capas Administrativas:** Descargar las unidades territoriales base de la agencia oficial nacional o de datasets normalizados de alta resolución.
3. **Construcción del Filtro SQL:** Crear la expresión de selección por nombres o identificadores en QGIS y versionarla en `QGIS/<PAIS>/SQLs/`.
4. **Empaquetado Vectorial:** Exportar la selección en formato GeoPackage (`QGIS/<PAIS>/...`) con coordenadas transformadas a **WGS84 (EPSG:4326)**.
5. **Integración Web y Análisis de Variedades:**
   * Agregar la entidad con sus metadatos (categoría, uvas tintas, uvas blancas, color, enlace al pliego) en `data/spain_wine_regions.geojson`.
   * Ejecutar `scratch/build_grape_database.py` para sincronizar automáticamente el nuevo país con el explorador de variedades `grapes.html`.
   * Registrar la denominación en `docs/<PAIS>/REGISTRO_...md` y actualizar las tablas de cobertura en `README.md`, `README_ES.md`, `COVERAGE.md` y `COBERTURA.md`.

---

## 4. Plantilla de Contribución para Nuevas Regiones

Al abrir un *Pull Request* o *Issue* en GitHub para proponer o incorporar una denominación, utiliza la siguiente plantilla homologada:

```markdown
### [Nombre de la Denominación / Región Vitivinícola]

- **País y Macro-región:** [Ej. Argentina / Mendoza / Valle de Uco]
- **Figura de Calidad Oficial:** [AVA / IG / DOC / DO / WO / GI]
- **Organismo Regulador:** [Ej. INV / TTB / SAG / Wine Australia]
- **Documento Normativo Oficial:** [Enlace o nombre del archivo PDF archivado en DOWNs/DOCs/<PAIS>/]
- **Cartografía Administrativa Base:** [Agencia oficial de mapeo y año de la capa]
- **Campo de Filtrado:** [Ej. `NAME`, `FIPS`, `INSEE_COM`, etc.]
- **Consulta de Selección SQL:**
  ```sql
  "NAME_UNIT" IN ('Unidad 1', 'Unidad 2', 'Unidad 3')
  ```
- **Archivo GeoPackage Resultante:** `QGIS/<PAIS>/<REGION>/<Nombre_DO>.gpkg`
- **Variedades de Uva Principales:**
  - Tintas: [Ej. Malbec (min 85%), Cabernet Franc, Merlot]
  - Blancas: [Ej. Chardonnay, Torrontés, Sauvignon Blanc]
- **Estilos de Vino Elaborados:** [Tranquilo / Espumoso / Fortificado]
- **Enfoque de Mezcla:** [Monovarietal / Ensamblaje]
```

---

*¡Juntos estamos construyendo la cartografía vitivinícola definitiva y abierta del mundo!* 🍷
