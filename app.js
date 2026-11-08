// WINE³ai - Interactive Wine Maps & Terroir Intelligence

const I18N = {
  es: {
    title: "WINE³ai",
    subtitle: "World Wide Wine — Atlas e Inteligencia de Terruños",
    searchPlaceholder: "Buscar por DO, País, Región, Uva o Municipio...",
    allCountries: "Todos los Países",
    allCategories: "Todas las Categorías",
    catDOCa: "DOCa (Calificada)",
    catDO: "DO / DOC (Origen)",
    catAOC: "AOC (Francia)",
    catDOCG: "DOCG (Italia)",
    catVP: "Vino de Pago (VP)",
    catVC: "Vino de Calidad (VC)",
    allRegions: "Todas las Regiones",
    regionsFound: "denominaciones encontradas",
    munis: "municipios / comunas",
    grapesRed: "Uvas Tintas Principales",
    grapesWhite: "Uvas Blancas Principales",
    viewPliego: "📄 Ver Pliego de Condiciones Oficial (PDF)",
    viewAtlas: "🗺️ Abrir en Atlas.co",
    resetView: "Restablecer Vista",
    category: "Categoría",
    region: "Región / Zona",
    territory: "Delimitación Territorial",
    na: "No especificado en pliego",
    viewMunis: "Ver municipios / comunas",
    hideMunis: "Ocultar municipios / comunas",
    searchMunisPlaceholder: "Buscar municipio / comuna...",
    noMunisFound: "No se encontraron municipios",
    basemapTitle: "Cambiar mapa de referencia",
    bmVoyager: "Voyager (Color)",
    bmPositron: "Claro (Positron)",
    bmDark: "Oscuro (Dark Matter)",
    bmSatellite: "Satélite (ESRI)",
    bmTopo: "Topográfico (Relieve)",
    bmOsm: "OpenStreetMap",
    toggleSidebarHide: "Ocultar panel lateral",
    toggleSidebarShow: "Mostrar panel lateral",
    navGrapes: "Variedades de Uva",
    climateToggle: "Capa Climas",
    climateToggleTitle: "Activar/desactivar capa climática mundial",
    allClimates: "Todos los Climas",
    climateLabel: "Clima y Terruño",
    climateLegendTitle: "Climas Vitivinícolas Mundiales",
    climAtlantic: "🌊 Atlántico / Marítimo",
    climMedCoastal: "☀️ Mediterráneo Costero",
    climMedCont: "🏜️ Mediterráneo Continental / Meseta",
    climCont: "❄️ Continental",
    climAlpine: "🏔️ Alpino / Gran Altitud",
    climSubtrop: "🌋 Subtropical / Volcánico",
    regionsToggle: "Regiones Vitícolas",
    regionsToggleTitle: "Activar/desactivar capa de regiones vitivinícolas",
    climateToggle: "Capa Climas",
    climateToggleTitle: "Activar/desactivar capa climática mundial",
    showAllRegions: "Mostrar todas",
    hideAllRegions: "Ocultar todas",
    onMap: "en mapa",
    showOnMap: "Mostrar en el mapa",
    hideFromMap: "Ocultar del mapa",
    exportPDF: "Exportar PDF",
    exportPDFTitle: "Exportar vista actual del mapa en PDF A4 Horizontal",
    exportingPDF: "Generando PDF..."
  },
  en: {
    title: "WINE³ai",
    subtitle: "World Wide Wine — Maps & Terroir Intelligence",
    searchPlaceholder: "Search by Appellation, Country, Region, Grape or Municipality...",
    allCountries: "All Countries",
    allCategories: "All Classifications",
    catDOCa: "DOCa (Qualified)",
    catDO: "DO / DOC (Origin)",
    catAOC: "AOC (France)",
    catDOCG: "DOCG (Italy)",
    catVP: "Estate Wine / Pago (VP)",
    catVC: "Quality Wine (VC)",
    allRegions: "All Regions",
    regionsFound: "appellations found",
    munis: "municipalities / communes",
    grapesRed: "Key Red Varieties",
    grapesWhite: "Key White Varieties",
    viewPliego: "📄 View Official Specifications (PDF)",
    viewAtlas: "🗺️ Open in Atlas.co",
    resetView: "Reset View",
    category: "Classification",
    region: "Region / Zone",
    territory: "Territorial Scope",
    na: "Not specified in specifications",
    viewMunis: "View municipalities / communes",
    hideMunis: "Hide municipalities / communes",
    searchMunisPlaceholder: "Search municipality / commune...",
    noMunisFound: "No municipalities found",
    basemapTitle: "Change reference basemap",
    bmVoyager: "Voyager (Color)",
    bmPositron: "Light (Positron)",
    bmDark: "Dark (Dark Matter)",
    bmSatellite: "Satellite (ESRI)",
    bmTopo: "Topographic (Relief)",
    bmOsm: "OpenStreetMap",
    toggleSidebarHide: "Hide sidebar",
    toggleSidebarShow: "Show sidebar",
    navGrapes: "Grape Varieties",
    regionsToggle: "Wine Regions",
    regionsToggleTitle: "Toggle wine regions layer",
    climateToggle: "World Climate Layer",
    climateToggleTitle: "Toggle world climate zones layer",
    allClimates: "All Climates",
    climateLabel: "Climate & Terroir",
    climateLegendTitle: "World Viticultural Climates",
    climAtlantic: "🌊 Atlantic / Maritime",
    climMedCoastal: "☀️ Coastal Mediterranean",
    climMedCont: "🏜️ Continental Mediterranean",
    climCont: "❄️ Continental",
    climAlpine: "🏔️ Alpine / High Altitude",
    climSubtrop: "🌋 Subtropical / Volcanic",
    showAllRegions: "Show All",
    hideAllRegions: "Hide All",
    onMap: "on map",
    showOnMap: "Show on map",
    hideFromMap: "Hide from map",
    exportPDF: "Export PDF",
    exportPDFTitle: "Export current map view to A4 Landscape PDF",
    exportingPDF: "Generating PDF..."
  }
};

const COUNTRY_NAMES = {
  'España': { es: 'España', en: 'Spain', flag: '🇪🇸' },
  'Francia': { es: 'Francia', en: 'France', flag: '🇫🇷' },
  'Italia': { es: 'Italia', en: 'Italy', flag: '🇮🇹' },
  'Portugal': { es: 'Portugal', en: 'Portugal', flag: '🇵🇹' },
  'Alemania': { es: 'Alemania', en: 'Germany', flag: '🇩🇪' },
  'Austria': { es: 'Austria', en: 'Austria', flag: '🇦🇹' },
  'Grecia': { es: 'Grecia', en: 'Greece', flag: '🇬🇷' },
  'Hungría': { es: 'Hungría', en: 'Hungary', flag: '🇭🇺' },
  'Georgia': { es: 'Georgia', en: 'Georgia', flag: '🇬🇪' },
  'República Checa': { es: 'República Checa', en: 'Czech Republic', flag: '🇨🇿' },
  'Suiza': { es: 'Suiza', en: 'Switzerland', flag: '🇨🇭' },
  'Eslovenia': { es: 'Eslovenia', en: 'Slovenia', flag: '🇸🇮' },
  'Croacia': { es: 'Croacia', en: 'Croatia', flag: '🇭🇷' },
  'Eslovaquia': { es: 'Eslovaquia', en: 'Slovakia', flag: '🇸🇰' },
  'Rumanía': { es: 'Rumanía', en: 'Romania', flag: '🇷🇴' },
  'Bulgaria': { es: 'Bulgaria', en: 'Bulgaria', flag: '🇧🇬' },
  'Moldavia': { es: 'Moldavia', en: 'Moldova', flag: '🇲🇩' },
  'Armenia': { es: 'Armenia', en: 'Armenia', flag: '🇦🇲' },
  'Chipre': { es: 'Chipre', en: 'Cyprus', flag: '🇨🇾' },
  'Líbano': { es: 'Líbano', en: 'Lebanon', flag: '🇱🇧' },
  'Turquía': { es: 'Turquía', en: 'Turkey', flag: '🇹🇷' },
  'Luxemburgo': { es: 'Luxemburgo', en: 'Luxembourg', flag: '🇱🇺' },
  'Reino Unido': { es: 'Reino Unido', en: 'United Kingdom', flag: '🇬🇧' },
  'Serbia': { es: 'Serbia', en: 'Serbia', flag: '🇷🇸' },
  'Macedonia del Norte': { es: 'Macedonia del Norte', en: 'North Macedonia', flag: '🇲🇰' },
  'Montenegro': { es: 'Montenegro', en: 'Montenegro', flag: '🇲🇪' },
  'Bosnia y Herzegovina': { es: 'Bosnia y Herzegovina', en: 'Bosnia and Herzegovina', flag: '🇧🇦' },
  'Argentina': { es: 'Argentina', en: 'Argentina', flag: '🇦🇷' },
  'Chile': { es: 'Chile', en: 'Chile', flag: '🇨🇱' },
  'Estados Unidos': { es: 'Estados Unidos', en: 'United States', flag: '🇺🇸' },
  'Sudáfrica': { es: 'Sudáfrica', en: 'South Africa', flag: '🇿🇦' },
  'Australia': { es: 'Australia', en: 'Australia', flag: '🇦🇺' },
  'Nueva Zelanda': { es: 'Nueva Zelanda', en: 'New Zealand', flag: '🇳🇿' },
  'Uruguay': { es: 'Uruguay', en: 'Uruguay', flag: '🇺🇾' },
  'Brasil': { es: 'Brasil', en: 'Brazil', flag: '🇧🇷' },
  'Bolivia': { es: 'Bolivia', en: 'Bolivia', flag: '🇧🇴' },
  'Perú': { es: 'Perú', en: 'Peru', flag: '🇵🇪' },
  'México': { es: 'México', en: 'Mexico', flag: '🇲🇽' },
  'Canadá': { es: 'Canadá', en: 'Canada', flag: '🇨🇦' }
};

let currentLang = 'en';
let allFeatures = [];
let filteredFeatures = [];
let selectedFeature = null;
let currentMunisList = [];
let wineRegionsLayerVisible = true;
let climateLayerVisible = false;
let climatePopup = null;
const visibleRegionIds = new Set();

function toggleWineRegionsLayer() {
  wineRegionsLayerVisible = !wineRegionsLayerVisible;
  const btn = document.getElementById('btn-toggle-regions');
  const vis = wineRegionsLayerVisible ? 'visible' : 'none';

  if (map.getLayer('wine-regions-fill')) {
    map.setLayoutProperty('wine-regions-fill', 'visibility', vis);
  }
  if (map.getLayer('wine-regions-line')) {
    map.setLayoutProperty('wine-regions-line', 'visibility', vis);
  }
  if (map.getLayer('wine-regions-highlight')) {
    map.setLayoutProperty('wine-regions-highlight', 'visibility', vis);
  }

  if (btn) {
    btn.classList.toggle('active', wineRegionsLayerVisible);
  }
  updateVisibilityCountUI();
}

function toggleRegionVisibility(id, e) {
  if (e) e.stopPropagation();
  if (visibleRegionIds.has(id)) {
    visibleRegionIds.delete(id);
  } else {
    visibleRegionIds.add(id);
  }
  updateMapVisibilityFilter();
  updateRegionCardsUI();
  updateVisibilityCountUI();
}

function showAllFilteredRegions() {
  filteredFeatures.forEach(f => visibleRegionIds.add(f.properties.id));
  updateMapVisibilityFilter();
  updateRegionCardsUI();
  updateVisibilityCountUI();
}

function hideAllFilteredRegions() {
  filteredFeatures.forEach(f => visibleRegionIds.delete(f.properties.id));
  updateMapVisibilityFilter();
  updateRegionCardsUI();
  updateVisibilityCountUI();
}

function updateMapVisibilityFilter() {
  if (!map.getLayer('wine-regions-fill')) return;
  const ids = filteredFeatures
    .map(f => f.properties.id)
    .filter(id => visibleRegionIds.has(id));

  map.setFilter('wine-regions-fill', ['in', 'id', ...ids]);
  if (map.getLayer('wine-regions-line')) {
    map.setFilter('wine-regions-line', ['in', 'id', ...ids]);
  }
}

function updateVisibilityCountUI() {
  const t = I18N[currentLang];
  const badge = document.getElementById('count-visible-badge');
  if (!badge) return;
  const filteredTotal = filteredFeatures.length;
  const visibleCount = filteredFeatures.filter(f => visibleRegionIds.has(f.properties.id)).length;

  if (!wineRegionsLayerVisible) {
    badge.textContent = `(0 ${t.onMap})`;
    badge.style.background = '#FEE2E2';
    badge.style.color = '#B91C1C';
  } else {
    badge.textContent = `(${visibleCount} ${t.onMap})`;
    if (visibleCount === 0) {
      badge.style.background = '#FEE2E2';
      badge.style.color = '#B91C1C';
    } else if (visibleCount === filteredTotal) {
      badge.style.background = '#DCFCE7';
      badge.style.color = '#15803D';
    } else {
      badge.style.background = '#FEF3C7';
      badge.style.color = '#B45309';
    }
  }
}

function updateRegionCardsUI() {
  const t = I18N[currentLang];
  document.querySelectorAll('.region-card').forEach(card => {
    const id = card.dataset.id;
    const isVis = visibleRegionIds.has(id);
    card.classList.toggle('region-hidden', !isVis);
    const visBtn = card.querySelector('.btn-card-visibility');
    if (visBtn) {
      visBtn.classList.toggle('active', isVis);
      visBtn.title = isVis ? t.hideFromMap : t.showOnMap;
      const iconSpan = visBtn.querySelector('.vis-icon');
      if (iconSpan) iconSpan.textContent = isVis ? '👁️' : '👁️‍🗨️';
    }
  });
}

const BASEMAP_STYLES = {
  voyager: 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json',
  positron: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
  dark: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
  satellite: {
    version: 8,
    sources: {
      'esri-satellite': {
        type: 'raster',
        tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'],
        tileSize: 256,
        attribution: '© Esri, Maxar, Earthstar Geographics'
      }
    },
    layers: [
      { id: 'esri-satellite-layer', type: 'raster', source: 'esri-satellite', minzoom: 0, maxzoom: 19 }
    ]
  },
  topo: {
    version: 8,
    sources: {
      'opentopo': {
        type: 'raster',
        tiles: ['https://tile.opentopomap.org/{z}/{x}/{y}.png'],
        tileSize: 256,
        attribution: 'Map: © OpenTopoMap, © OpenStreetMap'
      }
    },
    layers: [
      { id: 'opentopo-layer', type: 'raster', source: 'opentopo', minzoom: 0, maxzoom: 17 }
    ]
  },
  osm: {
    version: 8,
    sources: {
      'osm': {
        type: 'raster',
        tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
        tileSize: 256,
        attribution: '© OpenStreetMap contributors'
      }
    },
    layers: [
      { id: 'osm-layer', type: 'raster', source: 'osm', minzoom: 0, maxzoom: 19 }
    ]
  }
};

// Initialize MapLibre
const map = new maplibregl.Map({
  container: 'map',
  style: BASEMAP_STYLES.voyager,
  center: [2.5, 43.5],
  zoom: 5.0,
  preserveDrawingBuffer: true
});

map.addControl(new maplibregl.NavigationControl(), 'bottom-right');

function setupWineLayers() {
  if (!allFeatures || allFeatures.length === 0) return;
  if (!map.isStyleLoaded()) return;

  if (!map.getSource('wine-regions')) {
    map.addSource('wine-regions', {
      type: 'geojson',
      data: {
        type: 'FeatureCollection',
        features: allFeatures
      }
    });
  }

  if (!map.getLayer('wine-regions-fill')) {
    map.addLayer({
      id: 'wine-regions-fill',
      type: 'fill',
      source: 'wine-regions',
      layout: {
        'visibility': wineRegionsLayerVisible ? 'visible' : 'none'
      },
      paint: {
        'fill-color': ['get', 'color'],
        'fill-opacity': 0.65
      }
    });
  }

  if (!map.getLayer('wine-regions-line')) {
    map.addLayer({
      id: 'wine-regions-line',
      type: 'line',
      source: 'wine-regions',
      layout: {
        'visibility': wineRegionsLayerVisible ? 'visible' : 'none'
      },
      paint: {
        'line-color': '#FFFFFF',
        'line-width': 1.5,
        'line-opacity': 0.9
      }
    });
  }

  if (!map.getLayer('wine-regions-highlight')) {
    map.addLayer({
      id: 'wine-regions-highlight',
      type: 'line',
      source: 'wine-regions',
      layout: {
        'visibility': wineRegionsLayerVisible ? 'visible' : 'none'
      },
      paint: {
        'line-color': '#FFD700',
        'line-width': 3.5,
        'line-opacity': 1
      },
      filter: ['==', 'id', selectedFeature ? selectedFeature.id : '']
    });
  }

  // Bind layer interaction events
  bindMapInteractions();

  // Re-apply visibility filter
  updateMapVisibilityFilter();
}

function bindMapInteractions() {
  map.off('click', 'wine-regions-fill', onRegionClick);
  map.off('mouseenter', 'wine-regions-fill', onRegionEnter);
  map.off('mouseleave', 'wine-regions-fill', onRegionLeave);

  map.on('click', 'wine-regions-fill', onRegionClick);
  map.on('mouseenter', 'wine-regions-fill', onRegionEnter);
  map.on('mouseleave', 'wine-regions-fill', onRegionLeave);
}

function onRegionClick(e) {
  if (e.features && e.features.length > 0) {
    const feat = e.features[0];
    const match = allFeatures.find(f => f.properties.id === feat.properties.id || f.properties.name === feat.properties.name);
    selectDO(match ? match.properties : feat.properties);
  }
}

function onRegionEnter() {
  map.getCanvas().style.cursor = 'pointer';
}

function onRegionLeave() {
  map.getCanvas().style.cursor = '';
}

function setupClimateLayers() {
  if (!map.isStyleLoaded()) return;

  const climateData = (typeof window.WORLD_CLIMATE_ZONES !== 'undefined' && window.WORLD_CLIMATE_ZONES)
    ? window.WORLD_CLIMATE_ZONES
    : ((typeof WORLD_CLIMATE_ZONES !== 'undefined' && WORLD_CLIMATE_ZONES) ? WORLD_CLIMATE_ZONES : null);

  if (!climateData) return;

  if (!map.getSource('world-climate-zones')) {
    map.addSource('world-climate-zones', {
      type: 'geojson',
      data: climateData
    });
  }

  // Insert climate fill BEFORE wine-regions-fill if it exists so wine regions sit on top
  const beforeLayer = map.getLayer('wine-regions-fill') ? 'wine-regions-fill' : undefined;

  if (!map.getLayer('climate-zones-fill')) {
    map.addLayer({
      id: 'climate-zones-fill',
      type: 'fill',
      source: 'world-climate-zones',
      layout: {
        'visibility': climateLayerVisible ? 'visible' : 'none'
      },
      paint: {
        'fill-color': ['get', 'color'],
        'fill-opacity': 0.32
      }
    }, beforeLayer);
  }

  if (!map.getLayer('climate-zones-line')) {
    map.addLayer({
      id: 'climate-zones-line',
      type: 'line',
      source: 'world-climate-zones',
      layout: {
        'visibility': climateLayerVisible ? 'visible' : 'none'
      },
      paint: {
        'line-color': ['get', 'color'],
        'line-width': 0.75,
        'line-opacity': 0.55
      }
    }, beforeLayer);
  }

  bindClimateInteractions();
}

function bindClimateInteractions() {
  map.off('click', 'climate-zones-fill', onClimateClick);
  map.off('mouseenter', 'climate-zones-fill', onClimateEnter);
  map.off('mouseleave', 'climate-zones-fill', onClimateLeave);

  map.on('click', 'climate-zones-fill', onClimateClick);
  map.on('mouseenter', 'climate-zones-fill', onClimateEnter);
  map.on('mouseleave', 'climate-zones-fill', onClimateLeave);
}

function onClimateClick(e) {
  if (!climateLayerVisible) return;
  // If user clicked inside a wine region polygon, prioritize wine region detail
  if (map.getLayer('wine-regions-fill')) {
    const wineFeats = map.queryRenderedFeatures(e.point, { layers: ['wine-regions-fill'] });
    if (wineFeats && wineFeats.length > 0) return;
  }

  if (e.features && e.features.length > 0) {
    const feat = e.features[0];
    const p = feat.properties;
    const name = currentLang === 'es' ? (p.name_es || p.name) : (p.name_en || p.name);
    const desc = currentLang === 'es' ? (p.desc_es || '') : (p.desc_en || '');
    const icon = p.icon || '⛅';
    const color = p.color || '#0284C7';
    const koppen = p.koppen_code ? `<span style="display:inline-block; font-size:0.7rem; background:#F1F5F9; border:1px solid #CBD5E1; border-radius:4px; padding:1px 5px; color:#475569; margin-left:6px;">Köppen: ${p.koppen_code}</span>` : '';

    if (climatePopup) climatePopup.remove();

    climatePopup = new maplibregl.Popup({ offset: 12, closeButton: true })
      .setLngLat(e.lngLat)
      .setHTML(`
        <div style="font-family: inherit; max-width: 260px; padding: 2px;">
          <div style="display: flex; align-items: center; gap: 6px; font-weight: 700; color: ${color}; font-size: 0.95rem; margin-bottom: 4px;">
            <span>${icon}</span> <span>${name}</span> ${koppen}
          </div>
          <div style="font-size: 0.78rem; color: #334155; line-height: 1.35; margin-top: 4px;">
            ${desc}
          </div>
        </div>
      `)
      .addTo(map);
  }
}

function onClimateEnter() {
  if (climateLayerVisible) {
    map.getCanvas().style.cursor = 'pointer';
  }
}

function onClimateLeave() {
  if (climateLayerVisible) {
    map.getCanvas().style.cursor = '';
  }
}

function toggleClimateLayer() {
  climateLayerVisible = !climateLayerVisible;
  const btn = document.getElementById('btn-toggle-climate');
  const legend = document.getElementById('climate-map-legend');

  if (!map.getLayer('climate-zones-fill')) {
    setupClimateLayers();
  }

  const vis = climateLayerVisible ? 'visible' : 'none';
  if (map.getLayer('climate-zones-fill')) {
    map.setLayoutProperty('climate-zones-fill', 'visibility', vis);
  }
  if (map.getLayer('climate-zones-line')) {
    map.setLayoutProperty('climate-zones-line', 'visibility', vis);
  }

  if (btn) {
    btn.classList.toggle('active', climateLayerVisible);
  }
  if (legend) {
    legend.style.display = climateLayerVisible ? 'block' : 'none';
  }
  if (!climateLayerVisible && climatePopup) {
    climatePopup.remove();
  }
}

function checkAndRestoreLayers() {
  if (map.isStyleLoaded()) {
    if (allFeatures.length > 0 && !map.getLayer('wine-regions-fill')) {
      setupClimateLayers();
      setupWineLayers();
    } else if (!map.getLayer('climate-zones-fill')) {
      setupClimateLayers();
    }
  }
}

map.on('styledata', checkAndRestoreLayers);
map.on('idle', checkAndRestoreLayers);

// Load Data
map.on('load', async () => {
  try {
    let data;
    if (typeof window.SPAIN_WINE_DATA !== 'undefined' && window.SPAIN_WINE_DATA) {
      data = window.SPAIN_WINE_DATA;
    } else if (typeof SPAIN_WINE_DATA !== 'undefined' && SPAIN_WINE_DATA) {
      data = SPAIN_WINE_DATA;
    } else {
      const resp = await fetch('data/spain_wine_regions.geojson?v=20261105a');
      data = await resp.json();
    }
    allFeatures = data.features;
    allFeatures.forEach(f => visibleRegionIds.add(f.properties.id));
    filteredFeatures = allFeatures;

    setupClimateLayers();
    setupWineLayers();
    setLanguage(currentLang);
    updateVisibilityCountUI();

  } catch (err) {
    console.error("Error loading GeoJSON:", err);
  }
});

function updateCountryFilterLabels(lang) {
  const select = document.getElementById('country-filter');
  const currentVal = select.value;
  const optCountryAll = document.getElementById('country-all-opt') || document.createElement('option');
  optCountryAll.value = "";
  optCountryAll.id = "country-all-opt";
  optCountryAll.textContent = I18N[lang].allCountries;

  // Sort country entries alphabetically by localized name in the active language
  const sortedEntries = Object.entries(COUNTRY_NAMES).sort((a, b) => {
    return a[1][lang].localeCompare(b[1][lang], lang);
  });

  select.innerHTML = '';
  select.appendChild(optCountryAll);

  for (const [key, data] of sortedEntries) {
    const opt = document.createElement('option');
    opt.value = key;
    opt.textContent = `${data.flag} ${data[lang]}`;
    if (key === currentVal) {
      opt.selected = true;
    }
    select.appendChild(opt);
  }
}

function populateCategoryFilter(selectedCountry = '') {
  const select = document.getElementById('category-filter');
  const currentVal = select.value;
  select.innerHTML = `<option value="" id="cat-all-opt">${I18N[currentLang].allCategories}</option>`;

  let features = allFeatures;
  if (selectedCountry) {
    features = allFeatures.filter(f => f.properties.country === selectedCountry);
  }
  const categories = [...new Set(features.map(f => f.properties.category).filter(Boolean))].sort();
  categories.forEach(cat => {
    const opt = document.createElement('option');
    opt.value = cat;
    opt.textContent = cat;
    if (cat === currentVal) opt.selected = true;
    select.appendChild(opt);
  });
}

function populateRegionFilter(selectedCountry = '', selectedCategory = '') {
  const select = document.getElementById('region-filter');
  const currentVal = select.value;
  select.innerHTML = `<option value="" id="reg-all-opt">${I18N[currentLang].allRegions}</option>`;

  let features = allFeatures;
  if (selectedCountry) {
    features = features.filter(f => f.properties.country === selectedCountry);
  }
  if (selectedCategory) {
    features = features.filter(f => f.properties.category === selectedCategory);
  }
  const regions = [...new Set(features.map(f => f.properties.region).filter(Boolean))].sort();
  regions.forEach(r => {
    const opt = document.createElement('option');
    opt.value = r;
    opt.textContent = r;
    if (r === currentVal) opt.selected = true;
    select.appendChild(opt);
  });
}

function applyFilters() {
  const search = document.getElementById('search-input').value.toLowerCase().trim();
  const country = document.getElementById('country-filter').value;
  const cat = document.getElementById('category-filter').value;
  const reg = document.getElementById('region-filter').value;
  const climate = document.getElementById('climate-filter') ? document.getElementById('climate-filter').value : '';

  filteredFeatures = allFeatures.filter(f => {
    const p = f.properties;
    const matchCountry = !country || p.country === country;
    const matchCat = !cat || p.category === cat;
    const matchReg = !reg || p.region === reg;
    const matchClimate = !climate || p.climate === climate;
    const cInfo = COUNTRY_NAMES[p.country];
    const cEn = cInfo ? cInfo.en.toLowerCase() : '';
    const cEs = cInfo ? cInfo.es.toLowerCase() : '';
    const matchSearch = !search ||
      p.name.toLowerCase().includes(search) ||
      p.region.toLowerCase().includes(search) ||
      (p.country && p.country.toLowerCase().includes(search)) ||
      cEn.includes(search) ||
      cEs.includes(search) ||
      (p.climate_name_en && p.climate_name_en.toLowerCase().includes(search)) ||
      (p.climate_name_es && p.climate_name_es.toLowerCase().includes(search)) ||
      (p.grapes_red && p.grapes_red.toLowerCase().includes(search)) ||
      (p.grapes_white && p.grapes_white.toLowerCase().includes(search)) ||
      (p.munis && p.munis.some(m => m.toLowerCase().includes(search)));

    return matchCountry && matchCat && matchReg && matchClimate && matchSearch;
  });

  updateMapVisibilityFilter();
  renderRegionsList();
  updateVisibilityCountUI();
}

function renderRegionsList() {
  const container = document.getElementById('regions-list');
  const countEl = document.getElementById('count-badge');
  const t = I18N[currentLang];

  countEl.textContent = `${filteredFeatures.length} ${t.regionsFound}`;
  container.innerHTML = '';

  filteredFeatures.forEach(f => {
    const p = f.properties;
    const isVis = visibleRegionIds.has(p.id);
    const isSel = selectedFeature && selectedFeature.id === p.id;
    const card = document.createElement('div');
    card.className = `region-card ${isSel ? 'selected' : ''} ${isVis ? '' : 'region-hidden'}`;
    card.dataset.id = p.id;

    const muniCount = p.munis_count || p.muni_count || (p.munis ? p.munis.length : 0);
    const cInfo = COUNTRY_NAMES[p.country];
    const flag = cInfo ? cInfo.flag : '🍷';
    const cDisplayName = cInfo ? cInfo[currentLang] : (p.country || '');

    card.innerHTML = `
      <div class="region-card-main">
        <div>
          <div class="card-title">${flag} ${p.name}</div>
          <div class="card-meta">${p.region}${cDisplayName ? ` (${cDisplayName})` : ''} • ${muniCount} ${t.munis}</div>
        </div>
        <span class="card-badge" style="background-color: ${p.color};">${p.category}</span>
      </div>
      <button class="btn-card-visibility ${isVis ? 'active' : ''}" title="${isVis ? t.hideFromMap : t.showOnMap}" aria-label="Toggle region visibility on map">
        <span class="vis-icon">${isVis ? '👁️' : '👁️‍🗨️'}</span>
      </button>
    `;

    card.querySelector('.region-card-main').onclick = () => selectDO(p);
    card.querySelector('.btn-card-visibility').onclick = (e) => toggleRegionVisibility(p.id, e);
    container.appendChild(card);
  });
}

function selectDO(inputProps) {
  const feat = allFeatures.find(f => f.properties.id === inputProps.id || f.properties.name === inputProps.name);
  const props = feat ? feat.properties : inputProps;
  selectedFeature = props;
  const t = I18N[currentLang];

  // If region is currently hidden, make it visible on map
  if (!visibleRegionIds.has(props.id)) {
    visibleRegionIds.add(props.id);
    if (!wineRegionsLayerVisible) {
      wineRegionsLayerVisible = true;
      const btn = document.getElementById('btn-toggle-regions');
      if (btn) btn.classList.add('active');
      if (map.getLayer('wine-regions-fill')) map.setLayoutProperty('wine-regions-fill', 'visibility', 'visible');
      if (map.getLayer('wine-regions-line')) map.setLayoutProperty('wine-regions-line', 'visibility', 'visible');
      if (map.getLayer('wine-regions-highlight')) map.setLayoutProperty('wine-regions-highlight', 'visibility', 'visible');
    }
    updateMapVisibilityFilter();
    updateRegionCardsUI();
    updateVisibilityCountUI();
  }

  // Highlight on map
  map.setFilter('wine-regions-highlight', ['==', 'id', props.id]);

  // Find geometry bbox to zoom
  if (feat) {
    const coords = getFlattenedCoords(feat.geometry);
    const bounds = coords.reduce((b, coord) => b.extend(coord), new maplibregl.LngLatBounds(coords[0], coords[0]));
    map.fitBounds(bounds, { padding: 120, maxZoom: 10, duration: 1200 });
  }

  // Update Detail Panel
  const panel = document.getElementById('detail-panel');
  document.getElementById('detail-badge').textContent = props.category;
  document.getElementById('detail-badge').style.backgroundColor = props.color;
  document.getElementById('detail-title').textContent = props.name;

  const countryInfo = COUNTRY_NAMES[props.country];
  const flag = countryInfo ? countryInfo.flag : '';
  const countryLabel = countryInfo ? countryInfo[currentLang] : props.country;
  document.getElementById('detail-region').innerHTML = `<span style="font-size: 1.05rem;">📍</span> ${props.region} ${flag ? `(${flag} ${countryLabel})` : ''}`;

  const muniCount = props.munis_count || props.muni_count || (props.munis ? props.munis.length : 0);
  document.getElementById('detail-munis').textContent = `${muniCount} ${t.munis}`;
  document.getElementById('detail-grapes-red').textContent = props.grapes_red || t.na;
  document.getElementById('detail-grapes-white').textContent = props.grapes_white || t.na;

  // Update Climate in Detail Panel
  const climateItem = document.getElementById('detail-climate-item');
  const climateBadge = document.getElementById('detail-climate-badge');
  const climateDesc = document.getElementById('detail-climate-desc');

  if (climateBadge && climateDesc) {
    if (props.climate) {
      const climName = currentLang === 'es' ? (props.climate_name_es || props.climate) : (props.climate_name_en || props.climate);
      const climDesc = currentLang === 'es' ? (props.climate_desc_es || '') : (props.climate_desc_en || '');
      const climIcon = props.climate_icon || '⛅';
      const climColor = props.climate_color || '#0284C7';

      climateBadge.innerHTML = `<span>${climIcon}</span> <span>${climName}</span>`;
      climateBadge.style.borderColor = climColor;
      climateBadge.style.backgroundColor = climColor + '18';
      climateDesc.textContent = climDesc;
      if (climateItem) climateItem.style.display = 'flex';
    } else {
      if (climateItem) climateItem.style.display = 'none';
    }
  }

  // Setup Municipalities list safely
  let munis = props.munis;
  if (typeof munis === 'string') {
    try {
      munis = JSON.parse(munis);
    } catch (e) {
      munis = munis.split(',').map(s => s.trim());
    }
  }
  currentMunisList = Array.isArray(munis) ? munis : [];

  const dropdown = document.getElementById('munis-dropdown');
  dropdown.open = false;
  document.getElementById('munis-search').value = '';
  document.getElementById('munis-search').placeholder = t.searchMunisPlaceholder;
  renderMunisChips(currentMunisList);
  updateMunisToggleLabel();

  const btnPliego = document.getElementById('btn-pliego');
  if (props.pliego) {
    btnPliego.href = `https://github.com/jreyes13/wine_world_wide/blob/main/${encodeURI(props.pliego)}`;
    btnPliego.style.display = 'flex';
  } else {
    btnPliego.style.display = 'none';
  }

  panel.classList.add('active');
  renderRegionsList();

  setTimeout(() => {
    const selectedCard = document.querySelector('.region-card.selected');
    if (selectedCard) {
      selectedCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }, 50);
}

function renderMunisChips(munis) {
  const container = document.getElementById('munis-chips');
  const t = I18N[currentLang];
  container.innerHTML = '';

  let list = munis;
  if (typeof list === 'string') {
    try { list = JSON.parse(list); } catch (e) { list = [list]; }
  }
  if (!Array.isArray(list) || list.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'munis-empty';
    empty.textContent = t.noMunisFound;
    container.appendChild(empty);
    return;
  }

  list.forEach(m => {
    const chip = document.createElement('span');
    chip.className = 'muni-chip';
    chip.textContent = m;
    container.appendChild(chip);
  });
}

function updateMunisToggleLabel() {
  const dropdown = document.getElementById('munis-dropdown');
  const label = document.getElementById('lbl-toggle-munis');
  const t = I18N[currentLang];
  const count = currentMunisList ? currentMunisList.length : 0;
  if (dropdown.open) {
    label.textContent = `${t.hideMunis} (${count})`;
  } else {
    label.textContent = `${t.viewMunis} (${count})`;
  }
}

function getFlattenedCoords(geom) {
  const coords = [];
  function extract(arr) {
    if (typeof arr[0] === 'number') {
      coords.push(arr);
    } else {
      arr.forEach(extract);
    }
  }
  extract(geom.coordinates);
  return coords;
}

function closeDetail() {
  document.getElementById('detail-panel').classList.remove('active');
  map.setFilter('wine-regions-highlight', ['==', 'id', '']);
  selectedFeature = null;
  renderRegionsList();
}

function setLanguage(lang) {
  currentLang = lang;
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.dataset.lang === lang));
  const t = I18N[lang];

  const brandTitleEl = document.getElementById('brand-title');
  if (brandTitleEl) {
    brandTitleEl.innerHTML = `WINE<span class="brand-exp">³</span><span class="brand-ai">ai</span>`;
  }
  document.getElementById('brand-subtitle').textContent = t.subtitle;
  document.getElementById('search-input').placeholder = t.searchPlaceholder;
  
  const navGrapesText = document.getElementById('nav-grapes-text');
  if (navGrapesText) navGrapesText.textContent = t.navGrapes;

  const optCountryAll = document.getElementById('country-all-opt');
  if (optCountryAll) optCountryAll.textContent = t.allCountries;

  updateCountryFilterLabels(lang);

  const sidebarToggle = document.getElementById('sidebar-toggle');
  const sidebarEl = document.getElementById('sidebar');
  if (sidebarToggle && sidebarEl) {
    const isCollapsed = sidebarEl.classList.contains('collapsed');
    sidebarToggle.title = isCollapsed ? t.toggleSidebarShow : t.toggleSidebarHide;
  }

  document.getElementById('cat-all-opt').textContent = t.allCategories;
  const optDoca = document.getElementById('cat-doca-opt');
  if (optDoca) optDoca.textContent = t.catDOCa;
  const optDo = document.getElementById('cat-do-opt');
  if (optDo) optDo.textContent = t.catDO;
  const optVp = document.getElementById('cat-vp-opt');
  if (optVp) optVp.textContent = t.catVP;
  const optVc = document.getElementById('cat-vc-opt');
  if (optVc) optVc.textContent = t.catVC;

  const optRegAll = document.getElementById('reg-all-opt');
  if (optRegAll) optRegAll.textContent = t.allRegions;

  // Climate filter options
  const optClimAll = document.getElementById('clim-all-opt');
  if (optClimAll) optClimAll.textContent = t.allClimates;
  const optClimMedCo = document.getElementById('clim-med-coastal-opt');
  if (optClimMedCo) optClimMedCo.textContent = t.climMedCoastal;
  const optClimMedCt = document.getElementById('clim-med-cont-opt');
  if (optClimMedCt) optClimMedCt.textContent = t.climMedCont;
  const optClimAtl = document.getElementById('clim-atlantic-opt');
  if (optClimAtl) optClimAtl.textContent = t.climAtlantic;
  const optClimCont = document.getElementById('clim-cont-opt');
  if (optClimCont) optClimCont.textContent = t.climCont;
  const optClimAlp = document.getElementById('clim-alpine-opt');
  if (optClimAlp) optClimAlp.textContent = t.climAlpine;
  const optClimSub = document.getElementById('clim-subtrop-opt');
  if (optClimSub) optClimSub.textContent = t.climSubtrop;

  // Topnav Layer Toggles
  const txtRegionsToggle = document.getElementById('txt-regions-toggle');
  if (txtRegionsToggle) txtRegionsToggle.textContent = t.regionsToggle;
  const btnRegionsToggle = document.getElementById('btn-toggle-regions');
  if (btnRegionsToggle) btnRegionsToggle.title = t.regionsToggleTitle;

  const txtClimateToggle = document.getElementById('txt-climate-toggle');
  if (txtClimateToggle) txtClimateToggle.textContent = t.climateToggle;
  const btnClimateToggle = document.getElementById('btn-toggle-climate');
  if (btnClimateToggle) btnClimateToggle.title = t.climateToggleTitle;

  const lblClimate = document.getElementById('lbl-climate');
  if (lblClimate) lblClimate.textContent = t.climateLabel;

  // Climate Legend elements
  const lblClimateLegTitle = document.getElementById('lbl-climate-legend-title');
  if (lblClimateLegTitle) lblClimateLegTitle.textContent = `⛅ ${t.climateLegendTitle}`;
  const legAtl = document.getElementById('leg-clim-atlantic');
  if (legAtl) legAtl.textContent = t.climAtlantic;
  const legMedCo = document.getElementById('leg-clim-med-coastal');
  if (legMedCo) legMedCo.textContent = t.climMedCoastal;
  const legMedCt = document.getElementById('leg-clim-med-cont');
  if (legMedCt) legMedCt.textContent = t.climMedCont;
  const legCont = document.getElementById('leg-clim-cont');
  if (legCont) legCont.textContent = t.climCont;
  const legAlp = document.getElementById('leg-clim-alpine');
  if (legAlp) legAlp.textContent = t.climAlpine;
  const legSub = document.getElementById('leg-clim-subtrop');
  if (legSub) legSub.textContent = t.climSubtrop;

  // Visibility action buttons
  const txtShowAll = document.getElementById('txt-show-all');
  if (txtShowAll) txtShowAll.textContent = t.showAllRegions;
  const btnShowAll = document.getElementById('btn-show-all-regions');
  if (btnShowAll) btnShowAll.title = t.showAllRegions;

  const txtHideAll = document.getElementById('txt-hide-all');
  if (txtHideAll) txtHideAll.textContent = t.hideAllRegions;
  const btnHideAll = document.getElementById('btn-hide-all-regions');
  if (btnHideAll) btnHideAll.title = t.hideAllRegions;

  // Export PDF action button
  const txtExportPdf = document.getElementById('txt-export-pdf');
  if (txtExportPdf) txtExportPdf.textContent = t.exportPDF;
  const btnExportPdf = document.getElementById('btn-export-pdf');
  if (btnExportPdf) btnExportPdf.title = t.exportPDFTitle;

  updateVisibilityCountUI();

  document.getElementById('lbl-territory').textContent = t.territory;
  document.getElementById('lbl-grapes-red').textContent = t.grapesRed;
  document.getElementById('lbl-grapes-white').textContent = t.grapesWhite;
  document.getElementById('btn-pliego-txt').textContent = t.viewPliego;

  const munisSearch = document.getElementById('munis-search');
  if (munisSearch) {
    munisSearch.placeholder = t.searchMunisPlaceholder;
  }
  updateMunisToggleLabel();
  renderMunisChips(currentMunisList);

  if (selectedFeature) {
    const countryInfo = COUNTRY_NAMES[selectedFeature.country];
    const flag = countryInfo ? countryInfo.flag : '';
    const countryLabel = countryInfo ? countryInfo[currentLang] : selectedFeature.country;
    document.getElementById('detail-region').innerHTML = `<span style="font-size: 1.05rem;">📍</span> ${selectedFeature.region} ${flag ? `(${flag} ${countryLabel})` : ''}`;

    if (selectedFeature.climate) {
      const climateBadge = document.getElementById('detail-climate-badge');
      const climateDesc = document.getElementById('detail-climate-desc');
      const climName = lang === 'es' ? (selectedFeature.climate_name_es || selectedFeature.climate) : (selectedFeature.climate_name_en || selectedFeature.climate);
      const climDesc = lang === 'es' ? (selectedFeature.climate_desc_es || '') : (selectedFeature.climate_desc_en || '');
      const climIcon = selectedFeature.climate_icon || '⛅';
      if (climateBadge) climateBadge.innerHTML = `<span>${climIcon}</span> <span>${climName}</span>`;
      if (climateDesc) climateDesc.textContent = climDesc;
    }
  }

  const basemapSelect = document.getElementById('basemap-select');
  if (basemapSelect) {
    basemapSelect.title = t.basemapTitle;
    const optVoy = document.getElementById('bm-voyager-opt');
    if (optVoy) optVoy.textContent = t.bmVoyager;
    const optPos = document.getElementById('bm-positron-opt');
    if (optPos) optPos.textContent = t.bmPositron;
    const optDark = document.getElementById('bm-dark-opt');
    if (optDark) optDark.textContent = t.bmDark;
    const optSat = document.getElementById('bm-satellite-opt');
    if (optSat) optSat.textContent = t.bmSatellite;
    const optTopo = document.getElementById('bm-topo-opt');
    if (optTopo) optTopo.textContent = t.bmTopo;
    const optOsm = document.getElementById('bm-osm-opt');
    if (optOsm) optOsm.textContent = t.bmOsm;
  }

  // Refresh dynamic filters labels
  const selCountry = document.getElementById('country-filter').value;
  const selCat = document.getElementById('category-filter').value;
  populateCategoryFilter(selCountry);
  populateRegionFilter(selCountry, selCat);

  renderRegionsList();
}

const COUNTRY_CENTERS = {
  'España': { center: [-3.7, 40.4], zoom: 5.8 },
  'Francia': { center: [2.2, 46.5], zoom: 5.6 },
  'Italia': { center: [12.5, 42.5], zoom: 5.8 },
  'Portugal': { center: [-8.2, 39.5], zoom: 6.6 },
  'Alemania': { center: [10.4, 51.1], zoom: 6.0 },
  'Austria': { center: [14.5, 47.5], zoom: 6.5 },
  'Grecia': { center: [23.5, 38.3], zoom: 6.2 },
  'Hungría': { center: [19.5, 47.1], zoom: 6.8 },
  'Georgia': { center: [44.0, 42.0], zoom: 6.8 },
  'República Checa': { center: [16.0, 49.3], zoom: 7.0 },
  'Suiza': { center: [8.2, 46.8], zoom: 7.8 },
  'Eslovenia': { center: [14.8, 46.1], zoom: 8.2 },
  'Croacia': { center: [16.4, 44.5], zoom: 7.0 },
  'Eslovaquia': { center: [19.5, 48.7], zoom: 7.2 },
  'Rumanía': { center: [24.9, 45.9], zoom: 6.6 },
  'Bulgaria': { center: [25.5, 42.7], zoom: 7.0 },
  'Moldavia': { center: [28.8, 47.0], zoom: 7.5 },
  'Armenia': { center: [44.8, 40.2], zoom: 7.5 },
  'Chipre': { center: [33.1, 35.0], zoom: 8.5 },
  'Líbano': { center: [35.8, 33.9], zoom: 8.3 },
  'Turquía': { center: [35.2, 39.0], zoom: 5.8 },
  'Luxemburgo': { center: [6.35, 49.6], zoom: 9.0 },
  'Reino Unido': { center: [-0.5, 51.2], zoom: 6.8 },
  'Serbia': { center: [20.9, 44.2], zoom: 7.2 },
  'Macedonia del Norte': { center: [22.0, 41.5], zoom: 7.8 },
  'Montenegro': { center: [19.2, 42.4], zoom: 8.5 },
  'Bosnia y Herzegovina': { center: [17.8, 43.3], zoom: 8.0 },
  'Argentina': { center: [-68.8, -33.5], zoom: 5.5 },
  'Chile': { center: [-71.2, -34.5], zoom: 5.8 },
  'Estados Unidos': { center: [-119.5, 38.5], zoom: 5.2 },
  'Sudáfrica': { center: [19.5, -33.8], zoom: 7.5 },
  'Australia': { center: [136.0, -32.5], zoom: 4.8 },
  'Nueva Zelanda': { center: [173.5, -41.5], zoom: 5.6 },
  'Uruguay': { center: [-56.0, -33.0], zoom: 6.8 },
  'Brasil': { center: [-52.0, -29.0], zoom: 6.5 },
  'Bolivia': { center: [-65.0, -20.5], zoom: 6.8 },
  'Perú': { center: [-75.0, -14.0], zoom: 6.5 },
  'México': { center: [-102.0, 26.0], zoom: 5.0 },
  'Canadá': { center: [-85.0, 46.0], zoom: 4.8 }
};

// Event Listeners
document.getElementById('search-input').addEventListener('input', applyFilters);
document.getElementById('category-filter').addEventListener('change', (e) => {
  const selCountry = document.getElementById('country-filter').value;
  populateRegionFilter(selCountry, e.target.value);
  applyFilters();
});
document.getElementById('region-filter').addEventListener('change', applyFilters);
document.getElementById('country-filter').addEventListener('change', (e) => {
  const selCountry = e.target.value;
  populateCategoryFilter(selCountry);
  populateRegionFilter(selCountry);
  applyFilters();
  if (COUNTRY_CENTERS[selCountry]) {
    map.flyTo({
      center: COUNTRY_CENTERS[selCountry].center,
      zoom: COUNTRY_CENTERS[selCountry].zoom,
      essential: true
    });
  } else {
    map.flyTo({
      center: [10.0, 47.0],
      zoom: 4.8,
      essential: true
    });
  }
});

document.getElementById('btn-close-detail').addEventListener('click', closeDetail);
document.querySelectorAll('.lang-btn').forEach(btn => {
  btn.addEventListener('click', (e) => setLanguage(e.target.dataset.lang));
});

// Basemap Switcher
const basemapSelectEl = document.getElementById('basemap-select');
if (basemapSelectEl) {
  basemapSelectEl.addEventListener('change', (e) => {
    const key = e.target.value;
    const style = BASEMAP_STYLES[key];
    if (style) {
      map.setStyle(style);
    }
  });
}

// Dropdown & Search for Municipalities
const munisSearchInput = document.getElementById('munis-search');
if (munisSearchInput) {
  munisSearchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    if (!query) {
      renderMunisChips(currentMunisList);
    } else {
      const filtered = currentMunisList.filter(m => m.toLowerCase().includes(query));
      renderMunisChips(filtered);
    }
  });
}

const munisDropdown = document.getElementById('munis-dropdown');
if (munisDropdown) {
  munisDropdown.addEventListener('toggle', () => {
    updateMunisToggleLabel();
  });
}

// Collapsible Sidebar Drawer Toggle
const sidebarToggleBtn = document.getElementById('sidebar-toggle');
const sidebarEl = document.getElementById('sidebar');
if (sidebarToggleBtn && sidebarEl) {
  sidebarToggleBtn.addEventListener('click', () => {
    sidebarEl.classList.toggle('collapsed');
    const isCollapsed = sidebarEl.classList.contains('collapsed');
    const t = I18N[currentLang];
    sidebarToggleBtn.title = isCollapsed ? t.toggleSidebarShow : t.toggleSidebarHide;
    setTimeout(() => {
      if (typeof map !== 'undefined' && map.resize) {
        map.resize();
      }
    }, 360);
  });
}

// Wine Regions Layer Toggle (Topnav)
const btnToggleRegions = document.getElementById('btn-toggle-regions');
if (btnToggleRegions) {
  btnToggleRegions.addEventListener('click', toggleWineRegionsLayer);
}

// World Climate Layer Toggle (Topnav)
const btnToggleClimate = document.getElementById('btn-toggle-climate');
if (btnToggleClimate) {
  btnToggleClimate.addEventListener('click', toggleClimateLayer);
}

// Climate Filter Selector
const climateFilterEl = document.getElementById('climate-filter');
if (climateFilterEl) {
  climateFilterEl.addEventListener('change', applyFilters);
}

// Climate Legend Close Button
const btnCloseClimateLegend = document.getElementById('btn-close-climate-legend');
if (btnCloseClimateLegend) {
  btnCloseClimateLegend.addEventListener('click', () => {
    const legend = document.getElementById('climate-map-legend');
    if (legend) legend.style.display = 'none';
  });
}

// Show All / Hide All Wine Regions (Sidebar)
const btnShowAllRegions = document.getElementById('btn-show-all-regions');
if (btnShowAllRegions) {
  btnShowAllRegions.addEventListener('click', showAllFilteredRegions);
}

const btnHideAllRegions = document.getElementById('btn-hide-all-regions');
if (btnHideAllRegions) {
  btnHideAllRegions.addEventListener('click', hideAllFilteredRegions);
}

// Export Map to PDF (A4 Landscape)
async function exportMapToPDF() {
  const jsPDFClass = (window.jspdf && window.jspdf.jsPDF) || window.jsPDF;
  if (!jsPDFClass) {
    alert(currentLang === 'es' ? 'La librería de exportación a PDF no se encuentra disponible.' : 'PDF export library is not available.');
    return;
  }

  const btnExport = document.getElementById('btn-export-pdf');
  const txtExport = document.getElementById('txt-export-pdf');
  const origTxt = txtExport ? txtExport.textContent : '';

  try {
    if (btnExport) btnExport.disabled = true;
    if (txtExport) txtExport.textContent = I18N[currentLang].exportingPDF;

    // Force map render to populate WebGL canvas buffer
    map.triggerRepaint();
    await new Promise(resolve => map.once('render', resolve));

    const canvas = map.getCanvas();
    const imgData = canvas.toDataURL('image/jpeg', 0.95);

    // Initialize A4 landscape PDF (297 x 210 mm)
    const pdf = new jsPDFClass({
      orientation: 'landscape',
      unit: 'mm',
      format: 'a4'
    });

    const isEs = currentLang === 'es';
    const pageWidth = 297;
    const pageHeight = 210;
    const margin = 10;
    const contentWidth = pageWidth - (margin * 2); // 277 mm

    // Header Background Accent Bar
    pdf.setFillColor(114, 47, 55); // Burgundy #722F37
    pdf.rect(margin, 8, 3.5, 13, 'F');

    // Title & Subtitle
    pdf.setFont('helvetica', 'bold');
    pdf.setFontSize(16);
    pdf.setTextColor(114, 47, 55);
    pdf.text('WINE3ai', margin + 6, 14);

    pdf.setFont('helvetica', 'normal');
    pdf.setFontSize(8.5);
    pdf.setTextColor(100, 100, 100);
    const subText = isEs 
      ? 'Atlas Mundial de Regiones Vitivinicilas, Climas y Terruño'
      : 'World Atlas of Wine Regions, Climates & Terroir Intelligence';
    pdf.text(subText, margin + 6, 19);

    // Metadata Right Column
    pdf.setFontSize(8);
    pdf.setTextColor(80, 80, 80);

    const countrySelect = document.getElementById('country-filter');
    const selectedCountryVal = countrySelect ? countrySelect.value : 'all';
    let scopeText = isEs ? 'Ambito: Todos los Paises' : 'Scope: All Countries';
    if (selectedCountryVal !== 'all' && COUNTRY_NAMES[selectedCountryVal]) {
      const cLabel = COUNTRY_NAMES[selectedCountryVal][currentLang] || selectedCountryVal;
      scopeText = (isEs ? 'Pais: ' : 'Country: ') + cLabel;
    }

    const visibleCount = (typeof visibleRegionIds !== 'undefined')
      ? filteredFeatures.filter(f => visibleRegionIds.has(f.properties.id)).length
      : 0;
    const totalCount = allFeatures.length;
    const regionsStatus = wineRegionsLayerVisible
      ? `${visibleCount}/${totalCount} ${isEs ? 'regiones visibles' : 'visible regions'}`
      : (isEs ? 'Capa Regiones oculta' : 'Regions Layer hidden');

    const climateStatus = climateLayerVisible
      ? (isEs ? 'Capa Clima activa' : 'Climate Layer active')
      : (isEs ? 'Capa Clima oculta' : 'Climate Layer hidden');

    const dateStr = new Date().toLocaleDateString(isEs ? 'es-ES' : 'en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });

    const metaLine1 = `${scopeText}  •  ${regionsStatus}`;
    const metaLine2 = `${climateStatus}  •  ${dateStr}`;

    pdf.text(metaLine1, pageWidth - margin, 13.5, { align: 'right' });
    pdf.text(metaLine2, pageWidth - margin, 18.5, { align: 'right' });

    // Divider line
    pdf.setDrawColor(210, 200, 195);
    pdf.setLineWidth(0.3);
    pdf.line(margin, 23.5, pageWidth - margin, 23.5);

    // Map Area bounds: y = 25.5 to y = 199.5 (height = 174 mm)
    const maxMapH = 174;
    const maxMapW = contentWidth;
    const canvasAspect = canvas.width / canvas.height;

    let drawW = maxMapW;
    let drawH = drawW / canvasAspect;
    if (drawH > maxMapH) {
      drawH = maxMapH;
      drawW = drawH * canvasAspect;
    }
    const drawX = margin + (maxMapW - drawW) / 2;
    const drawY = 25.5 + (maxMapH - drawH) / 2;

    // Render Map snapshot
    pdf.addImage(imgData, 'JPEG', drawX, drawY, drawW, drawH);

    // Frame border
    pdf.setDrawColor(180, 180, 180);
    pdf.setLineWidth(0.35);
    pdf.rect(drawX, drawY, drawW, drawH);

    // If Climate Layer is active, draw Climate Legend inside map overlay
    if (climateLayerVisible) {
      const legW = 68;
      const legH = 26;
      const legX = drawX + 3.5;
      const legY = drawY + drawH - legH - 3.5;

      // Card Background with border
      pdf.setFillColor(255, 255, 255);
      pdf.setDrawColor(190, 190, 190);
      pdf.setLineWidth(0.25);
      pdf.roundedRect(legX, legY, legW, legH, 1.5, 1.5, 'FD');

      // Card Title
      pdf.setFont('helvetica', 'bold');
      pdf.setFontSize(7.5);
      pdf.setTextColor(40, 40, 40);
      pdf.text(isEs ? 'ZONAS CLIMATICAS' : 'CLIMATE ZONES', legX + 3, legY + 4.5);

      // Climate items
      const climItems = [
        { label: isEs ? 'Atlantico / Maritimo' : 'Atlantic / Maritime', rgb: [56, 189, 248] },
        { label: isEs ? 'Continental' : 'Continental', rgb: [52, 211, 153] },
        { label: isEs ? 'Medit. Costero' : 'Coastal Med.', rgb: [251, 191, 36] },
        { label: isEs ? 'Alpino / Altitud' : 'Alpine / Altitude', rgb: [167, 139, 250] },
        { label: isEs ? 'Medit. Continental' : 'Continental Med.', rgb: [251, 146, 60] },
        { label: isEs ? 'Subtropical / Volc.' : 'Subtropical / Volc.', rgb: [251, 113, 133] }
      ];

      pdf.setFont('helvetica', 'normal');
      pdf.setFontSize(6.5);

      climItems.forEach((item, idx) => {
        const col = idx % 2;
        const row = Math.floor(idx / 2);
        const ix = legX + 3 + (col * 33);
        const iy = legY + 8 + (row * 5.5);

        // Color box
        pdf.setFillColor(item.rgb[0], item.rgb[1], item.rgb[2]);
        pdf.setDrawColor(120, 120, 120);
        pdf.setLineWidth(0.15);
        pdf.rect(ix, iy - 2.2, 3, 3, 'FD');

        // Label
        pdf.setTextColor(60, 60, 60);
        pdf.text(item.label, ix + 4.5, iy);
      });
    }

    // If a Region is selected, draw Selected Region Callout overlay
    if (selectedFeature) {
      const cardW = 75;
      const cardH = selectedFeature.climate ? 25 : 20;
      const cardX = drawX + drawW - cardW - 3.5;
      const cardY = drawY + 3.5;

      pdf.setFillColor(255, 255, 255);
      pdf.setDrawColor(114, 47, 55);
      pdf.setLineWidth(0.3);
      pdf.roundedRect(cardX, cardY, cardW, cardH, 1.5, 1.5, 'FD');

      // Top colored badge bar
      pdf.setFillColor(114, 47, 55);
      pdf.rect(cardX, cardY, cardW, 2.5, 'F');

      pdf.setFont('helvetica', 'bold');
      pdf.setFontSize(8);
      pdf.setTextColor(114, 47, 55);
      const nameTxt = pdf.splitTextToSize(selectedFeature.name || '', cardW - 6);
      pdf.text(nameTxt, cardX + 3, cardY + 6.5);

      pdf.setFont('helvetica', 'normal');
      pdf.setFontSize(7);
      pdf.setTextColor(80, 80, 80);

      const countryInfo = COUNTRY_NAMES[selectedFeature.country];
      const cName = countryInfo ? countryInfo[currentLang] : (selectedFeature.country || '');
      const catName = selectedFeature.category || '';
      pdf.text(`${catName} • ${selectedFeature.region || ''} (${cName})`, cardX + 3, cardY + 11);

      if (selectedFeature.climate) {
        const cTitle = isEs ? (selectedFeature.climate_name_es || selectedFeature.climate) : (selectedFeature.climate_name_en || selectedFeature.climate);
        pdf.setFont('helvetica', 'italic');
        pdf.setTextColor(90, 90, 90);
        pdf.text(`${isEs ? 'Clima' : 'Climate'}: ${cTitle}`, cardX + 3, cardY + 15.5);
      }

      if (selectedFeature.varieties_red || selectedFeature.varieties_white) {
        pdf.setFont('helvetica', 'normal');
        pdf.setFontSize(6.5);
        pdf.setTextColor(110, 110, 110);
        const grapesTxt = isEs ? 'Variedades documentadas en ficha' : 'Varieties documented in detail card';
        pdf.text(grapesTxt, cardX + 3, cardY + (selectedFeature.climate ? 20 : 16));
      }
    }

    // Footer
    pdf.setFont('helvetica', 'normal');
    pdf.setFontSize(7);
    pdf.setTextColor(120, 120, 120);
    const footerLeft = isEs
      ? 'WINE3ai • Formato A4 Horizontal (297 x 210 mm) • Proyeccion Web Mercator'
      : 'WINE3ai • Standard A4 Landscape (297 x 210 mm) • Web Mercator Projection';
    const footerRight = isEs
      ? 'WINE3ai • Fuente: MAPA Espana / Elaboracion propia • github.com/jreyes13/wine3ai'
      : 'WINE3ai • Source: MAPA Spain / Own compilation • github.com/jreyes13/wine3ai';

    pdf.text(footerLeft, margin, 204.5);
    pdf.text(footerRight, pageWidth - margin, 204.5, { align: 'right' });

    // File download
    const dateFileStr = new Date().toISOString().slice(0, 10);
    const scopeSlug = selectedCountryVal !== 'all' ? selectedCountryVal : 'World';
    const cleanFilename = `WINE3ai_Map_${scopeSlug}_${dateFileStr}.pdf`;
    pdf.save(cleanFilename);

  } catch (err) {
    console.error('Error generating PDF:', err);
    alert((currentLang === 'es' ? 'Error al generar el PDF: ' : 'Error generating PDF: ') + (err.message || err));
  } finally {
    if (btnExport) btnExport.disabled = false;
    if (txtExport) txtExport.textContent = origTxt || I18N[currentLang].exportPDF;
  }
}

// Export PDF Button Listener
const btnExportPdf = document.getElementById('btn-export-pdf');
if (btnExportPdf) {
  btnExportPdf.addEventListener('click', exportMapToPDF);
}
