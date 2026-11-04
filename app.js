// World Wine Wide - Interactive Map App

const I18N = {
  es: {
    title: "World Wine Wide",
    subtitle: "Mapas Oficiales de Regiones Vitivinícolas",
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
    navGrapes: "Variedades de Uva"
  },
  en: {
    title: "World Wine Wide",
    subtitle: "Official Wine Region Maps",
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
    navGrapes: "Grape Varieties"
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
  'Turquía': { es: 'Turquía', en: 'Turkey', flag: '🇹🇷' }
};

let currentLang = 'en';
let allFeatures = [];
let filteredFeatures = [];
let selectedFeature = null;
let currentMunisList = [];

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
  zoom: 5.0
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

  // Re-apply filter
  if (map.getLayer('wine-regions-fill') && map.getLayer('wine-regions-line')) {
    const ids = filteredFeatures.map(f => f.properties.id);
    map.setFilter('wine-regions-fill', ['in', 'id', ...ids]);
    map.setFilter('wine-regions-line', ['in', 'id', ...ids]);
  }
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

function checkAndRestoreLayers() {
  if (map.isStyleLoaded() && allFeatures.length > 0 && !map.getLayer('wine-regions-fill')) {
    setupWineLayers();
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
      const resp = await fetch('data/spain_wine_regions.geojson?v=20261104c');
      data = await resp.json();
    }
    allFeatures = data.features;
    filteredFeatures = allFeatures;

    setupWineLayers();
    setLanguage(currentLang);

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

  filteredFeatures = allFeatures.filter(f => {
    const p = f.properties;
    const matchCountry = !country || p.country === country;
    const matchCat = !cat || p.category === cat;
    const matchReg = !reg || p.region === reg;
    const cInfo = COUNTRY_NAMES[p.country];
    const cEn = cInfo ? cInfo.en.toLowerCase() : '';
    const cEs = cInfo ? cInfo.es.toLowerCase() : '';
    const matchSearch = !search ||
      p.name.toLowerCase().includes(search) ||
      p.region.toLowerCase().includes(search) ||
      (p.country && p.country.toLowerCase().includes(search)) ||
      cEn.includes(search) ||
      cEs.includes(search) ||
      (p.grapes_red && p.grapes_red.toLowerCase().includes(search)) ||
      (p.grapes_white && p.grapes_white.toLowerCase().includes(search)) ||
      (p.munis && p.munis.some(m => m.toLowerCase().includes(search)));

    return matchCountry && matchCat && matchReg && matchSearch;
  });

  // Update map filter
  const ids = filteredFeatures.map(f => f.properties.id);
  if (map.getLayer('wine-regions-fill')) {
    map.setFilter('wine-regions-fill', ['in', 'id', ...ids]);
  }
  if (map.getLayer('wine-regions-line')) {
    map.setFilter('wine-regions-line', ['in', 'id', ...ids]);
  }

  renderRegionsList();
}

function renderRegionsList() {
  const container = document.getElementById('regions-list');
  const countEl = document.getElementById('count-badge');
  const t = I18N[currentLang];

  countEl.textContent = `${filteredFeatures.length} ${t.regionsFound}`;
  container.innerHTML = '';

  filteredFeatures.forEach(f => {
    const p = f.properties;
    const card = document.createElement('div');
    card.className = `region-card ${selectedFeature && selectedFeature.id === p.id ? 'selected' : ''}`;
    card.onclick = () => selectDO(p);

    const muniCount = p.munis_count || p.muni_count || (p.munis ? p.munis.length : 0);
    const cInfo = COUNTRY_NAMES[p.country];
    const flag = cInfo ? cInfo.flag : '🍷';
    const cDisplayName = cInfo ? cInfo[currentLang] : (p.country || '');

    card.innerHTML = `
      <div>
        <div class="card-title">${flag} ${p.name}</div>
        <div class="card-meta">${p.region}${cDisplayName ? ` (${cDisplayName})` : ''} • ${muniCount} ${t.munis}</div>
      </div>
      <span class="card-badge" style="background-color: ${p.color};">${p.category}</span>
    `;
    container.appendChild(card);
  });
}

function selectDO(inputProps) {
  const feat = allFeatures.find(f => f.properties.id === inputProps.id || f.properties.name === inputProps.name);
  const props = feat ? feat.properties : inputProps;
  selectedFeature = props;
  const t = I18N[currentLang];

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

  document.getElementById('brand-title').textContent = t.title;
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
  'Turquía': { center: [35.2, 39.0], zoom: 5.8 }
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
