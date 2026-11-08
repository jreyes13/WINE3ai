// WINE³ai — Grape Varieties Explorer Application Logic

const I18N = {
  en: {
    brandTitle: "WINE³ai",
    brandSubtitle: "Grape Varieties & Terroir Explorer",
    navMap: "Wine Regions Map",
    lblBasemap: "Reference Basemap",
    lblColorFilter: "Grape Color:",
    colorAll: "All",
    colorRed: "🔴 Red",
    colorWhite: "⚪ White",
    lblCountryFilter: "Country:",
    optCountryAll: "🌍 All Countries (39)",
    lblStyleFilter: "Wine Style:",
    optStyleAll: "All Wine Styles",
    optStyleStill: "🍷 Still Wine (Tranquilo)",
    optStyleSparkling: "🥂 Sparkling (Espumoso / Método Tradicional)",
    optStyleFortified: "🍯 Fortified & Dessert (Generoso / Dulce)",
    lblBlendFilter: "Production Type:",
    optBlendAll: "All Production Types",
    optBlendMono: "🍇 Monovarietal Focus (Single Variety)",
    optBlendCoupage: "🍷 Blends / Coupage (Assemblage)",
    lblSearchVariety: "Search Variety:",
    searchPlaceholder: "Search variety (e.g. Tempranillo, Pinot Noir...)",
    lblMatrixTitle: "Grape Varieties Catalog",
    optSortAlpha: "🔤 A-Z (Alphabetical)",
    optSortRegions: "📊 Most Appellations",
    btnMatrixExpand: "↕️ Expand Grid",
    btnMatrixCollapse: "↕️ Collapse Grid",
    noMatrixMatches: "No grape varieties match the selected filters.",
    btnClearFilters: "Reset All Filters",
    lblPopularGrapes: "Quick Select:",
    lblStatCountries: "Countries",
    lblStatRegions: "Appellations",
    lblStatMonovarietal: "Single Varietal Eligible",
    lblSynonyms: "Regional Synonyms:",
    noSynonyms: "No major synonyms recorded",
    origin: "Origin:",
    titleDonutChart: "Geographic Distribution by Country",
    subDonutChart: "Interactive share of appellations cultivating this variety",
    lblResetFilter: "Show All Countries",
    titleStylesChart: "Production Profiles & Blend Typology",
    subStylesChart: "Still vs. Sparkling vs. Fortified and Monovarietal vs. Blends",
    lblStylesTitle: "Wine Styles Distribution",
    lblLegStill: "Still Wine",
    lblLegSparkling: "Sparkling",
    lblLegFortified: "Fortified & Dessert",
    lblBlendTitle: "Blend & Varietal Focus",
    lblLegMono: "Single Varietal (Monovarietal)",
    lblLegBlend: "Traditional Blends (Coupage)",
    lblBenchmarkTitle: "Benchmark Appellations:",
    titleMapSection: "Geospatial Distribution Map",
    subMapSection: "Interactive locations of all authorized wine appellations cultivating this grape",
    lblPillCultivated: "📍 Cultivated Area",
    titleTableSection: "Authorized Appellations Directory",
    subTableSection: "Detailed list of wine regions, legal requirements, and wine styles",
    tableFilterPlaceholder: "Filter appellations or country...",
    appellationsFound: "Appellations",
    thCountry: "Country",
    thAppellation: "Appellation",
    thCategory: "Classification",
    thRegion: "Territory / Basin",
    thRole: "Presence & Requirement",
    thStyles: "Wine Styles",
    thActions: "Explore",
    btnViewMap: "🗺️ Zoom Map",
    btnPliego: "📄 Specs (PDF)",
    lblClearBoundary: "Clear boundary",
    lblActiveBoundary: "Active Boundary",
    btnOpenWineMap: "🗺️ Open in Wine Map",
    redBadge: "🔴 Red Variety",
    whiteBadge: "⚪ White Variety",
    noRegionsFound: "No appellations found for this selection."
  },
  es: {
    brandTitle: "WINE³ai",
    brandSubtitle: "Explorador de Variedades de Uva y Terruño",
    navMap: "Mapa de Regiones Vitivinícolas",
    lblBasemap: "Mapa de referencia",
    lblColorFilter: "Color de Uva:",
    colorAll: "Todas",
    colorRed: "🔴 Tinta",
    colorWhite: "⚪ Blanca",
    lblCountryFilter: "País:",
    optCountryAll: "🌍 Todos los Países (39)",
    lblStyleFilter: "Estilo de Vino:",
    optStyleAll: "Todos los Estilos",
    optStyleStill: "🍷 Vino Tranquilo",
    optStyleSparkling: "🥂 Espumoso (Método Tradicional)",
    optStyleFortified: "🍯 Generoso y Dulce",
    lblBlendFilter: "Tipo de Elaboración:",
    optBlendAll: "Todos los Tipos",
    optBlendMono: "🍇 Enfoque Monovarietal (Varietales)",
    optBlendCoupage: "🍷 Mezclas / Ensamblajes (Coupage)",
    lblSearchVariety: "Buscar Variedad:",
    searchPlaceholder: "Buscar variedad (ej. Tempranillo, Pinot Noir...)",
    lblMatrixTitle: "Catálogo de Variedades",
    optSortAlpha: "🔤 A-Z (Alfabético)",
    optSortRegions: "📊 Mayor Presencia",
    btnMatrixExpand: "↕️ Expandir Matriz",
    btnMatrixCollapse: "↕️ Reducir Matriz",
    noMatrixMatches: "No se encontraron variedades con los filtros seleccionados.",
    btnClearFilters: "Restablecer Filtros",
    lblPopularGrapes: "Selección Rápida:",
    lblStatCountries: "Países",
    lblStatRegions: "Denominaciones",
    lblStatMonovarietal: "Aptitud Monovarietal",
    lblSynonyms: "Sinónimos Regionales:",
    noSynonyms: "Sin sinónimos principales registrados",
    origin: "Origen:",
    titleDonutChart: "Distribución Geográfica por País",
    subDonutChart: "Porcentaje interactivo de denominaciones que cultivan esta variedad",
    lblResetFilter: "Mostrar Todos los Países",
    titleStylesChart: "Perfiles de Producción y Tipología de Mezcla",
    subStylesChart: "Vino tranquilo vs. espumoso vs. generoso y monovarietales vs. ensamblajes",
    lblStylesTitle: "Distribución de Estilos de Vino",
    lblLegStill: "Vino Tranquilo",
    lblLegSparkling: "Espumoso",
    lblLegFortified: "Generoso y Dulce",
    lblBlendTitle: "Enfoque de Elaboración",
    lblLegMono: "Monovarietal (Varietal)",
    lblLegBlend: "Mezcla Tradicional (Coupage)",
    lblBenchmarkTitle: "Denominaciones Emblemáticas:",
    titleMapSection: "Mapa de Distribución Geoespacial",
    subMapSection: "Localización interactiva de las denominaciones oficiales donde está autorizada",
    lblPillCultivated: "📍 Zona de Cultivo",
    titleTableSection: "Directorio de Denominaciones Autorizadas",
    subTableSection: "Relación detallada de zonas vitivinícolas, requisitos legales y estilos",
    tableFilterPlaceholder: "Filtrar por denominación o país...",
    appellationsFound: "Denominaciones",
    thCountry: "País",
    thAppellation: "Denominación",
    thCategory: "Clasificación",
    thRegion: "Territorio / Cuenca",
    thRole: "Presencia y Requisito",
    thStyles: "Estilos de Vino",
    thActions: "Explorar",
    btnViewMap: "🗺️ Ver en Mapa",
    btnPliego: "📄 Pliego (PDF)",
    lblClearBoundary: "Quitar límite",
    lblActiveBoundary: "Límite Activo",
    btnOpenWineMap: "🗺️ Ver en Mapa General",
    redBadge: "🔴 Variedad Tinta",
    whiteBadge: "⚪ Variedad Blanca",
    noRegionsFound: "No se encontraron denominaciones para esta selección."
  }
};

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
        tileSize: 256
      }
    },
    layers: [{ id: 'esri-sat', type: 'raster', source: 'esri-satellite' }]
  },
  topo: {
    version: 8,
    sources: {
      'opentopo': {
        type: 'raster',
        tiles: ['https://tile.opentopomap.org/{z}/{x}/{y}.png'],
        tileSize: 256
      }
    },
    layers: [{ id: 'opentopo-layer', type: 'raster', source: 'opentopo' }]
  }
};

const PALETTE = [
  '#991B1B', '#D97706', '#2563EB', '#059669', '#7C3AED',
  '#DB2777', '#EA580C', '#0891B2', '#4F46E5', '#65A30D',
  '#475569', '#B45309', '#047857', '#6D28D9', '#BE185D'
];

const ALL_COUNTRIES = [
  { key: 'Alemania', en: 'Germany', es: 'Alemania', flag: '🇩🇪' },
  { key: 'Argentina', en: 'Argentina', es: 'Argentina', flag: '🇦🇷' },
  { key: 'Armenia', en: 'Armenia', es: 'Armenia', flag: '🇦🇲' },
  { key: 'Australia', en: 'Australia', es: 'Australia', flag: '🇦🇺' },
  { key: 'Austria', en: 'Austria', es: 'Austria', flag: '🇦🇹' },
  { key: 'Bolivia', en: 'Bolivia', es: 'Bolivia', flag: '🇧🇴' },
  { key: 'Bosnia y Herzegovina', en: 'Bosnia and Herzegovina', es: 'Bosnia y Herzegovina', flag: '🇧🇦' },
  { key: 'Brasil', en: 'Brazil', es: 'Brasil', flag: '🇧🇷' },
  { key: 'Bulgaria', en: 'Bulgaria', es: 'Bulgaria', flag: '🇧🇬' },
  { key: 'Canadá', en: 'Canada', es: 'Canadá', flag: '🇨🇦' },
  { key: 'Chile', en: 'Chile', es: 'Chile', flag: '🇨🇱' },
  { key: 'Chipre', en: 'Cyprus', es: 'Chipre', flag: '🇨🇾' },
  { key: 'Croacia', en: 'Croatia', es: 'Croacia', flag: '🇭🇷' },
  { key: 'Eslovaquia', en: 'Slovakia', es: 'Eslovaquia', flag: '🇸🇰' },
  { key: 'Eslovenia', en: 'Slovenia', es: 'Eslovenia', flag: '🇸🇮' },
  { key: 'España', en: 'Spain', es: 'España', flag: '🇪🇸' },
  { key: 'Estados Unidos', en: 'United States', es: 'Estados Unidos', flag: '🇺🇸' },
  { key: 'Francia', en: 'France', es: 'Francia', flag: '🇫🇷' },
  { key: 'Georgia', en: 'Georgia', es: 'Georgia', flag: '🇬🇪' },
  { key: 'Grecia', en: 'Greece', es: 'Grecia', flag: '🇬🇷' },
  { key: 'Hungría', en: 'Hungary', es: 'Hungría', flag: '🇭🇺' },
  { key: 'Italia', en: 'Italy', es: 'Italia', flag: '🇮🇹' },
  { key: 'Líbano', en: 'Lebanon', es: 'Líbano', flag: '🇱🇧' },
  { key: 'Luxemburgo', en: 'Luxembourg', es: 'Luxemburgo', flag: '🇱🇺' },
  { key: 'Macedonia del Norte', en: 'North Macedonia', es: 'Macedonia del Norte', flag: '🇲🇰' },
  { key: 'México', en: 'Mexico', es: 'México', flag: '🇲🇽' },
  { key: 'Moldavia', en: 'Moldova', es: 'Moldavia', flag: '🇲🇩' },
  { key: 'Montenegro', en: 'Montenegro', es: 'Montenegro', flag: '🇲🇪' },
  { key: 'Nueva Zelanda', en: 'New Zealand', es: 'Nueva Zelanda', flag: '🇳🇿' },
  { key: 'Perú', en: 'Peru', es: 'Perú', flag: '🇵🇪' },
  { key: 'Portugal', en: 'Portugal', es: 'Portugal', flag: '🇵🇹' },
  { key: 'Reino Unido', en: 'United Kingdom', es: 'Reino Unido', flag: '🇬🇧' },
  { key: 'República Checa', en: 'Czech Republic', es: 'República Checa', flag: '🇨🇿' },
  { key: 'Rumanía', en: 'Romania', es: 'Rumanía', flag: '🇷🇴' },
  { key: 'Serbia', en: 'Serbia', es: 'Serbia', flag: '🇷🇸' },
  { key: 'Sudáfrica', en: 'South Africa', es: 'Sudáfrica', flag: '🇿🇦' },
  { key: 'Suiza', en: 'Switzerland', es: 'Suiza', flag: '🇨🇭' },
  { key: 'Turquía', en: 'Turkey', es: 'Turquía', flag: '🇹🇷' },
  { key: 'Uruguay', en: 'Uruguay', es: 'Uruguay', flag: '🇺🇾' }
];

let currentLang = 'en';
let allGrapes = [];
let selectedGrapeObj = null;
let activeCountryFilter = null;
let map = null;

// Option A: Dynamic full region polygon loading & caching
let fullRegionsPromise = null;
let fullRegionsIndex = null;
let activeRegionPolygon = null;
let activeMapPopup = null;

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  initMap();
  await loadGrapeData();
  populateCountryFilter();
  setupEventListeners();
  renderVarietyMatrix();
  selectGrape('Tempranillo');

  // Background preload full boundary geometries in idle time (does not block initial load)
  setTimeout(() => {
    ensureFullRegionsLoaded().catch(err => console.warn("Background preload info:", err));
  }, 600);
});

function initMap() {
  map = new maplibregl.Map({
    container: 'grape-map',
    style: BASEMAP_STYLES.voyager,
    center: [10.0, 47.0],
    zoom: 4.2
  });

  map.addControl(new maplibregl.NavigationControl({ showCompass: true }), 'top-right');
}

async function loadGrapeData() {
  if (typeof window.GRAPE_VARIETIES_DATA !== 'undefined' && window.GRAPE_VARIETIES_DATA) {
    allGrapes = window.GRAPE_VARIETIES_DATA;
  } else {
    try {
      const resp = await fetch('data/grape_varieties.json');
      allGrapes = await resp.json();
    } catch (e) {
      console.error("Could not load grape varieties json:", e);
    }
  }
}

function populateCountryFilter() {
  const select = document.getElementById('country-filter');
  if (!select) return;
  const currentVal = select.value || 'all';
  select.innerHTML = '';

  const optAll = document.createElement('option');
  optAll.value = 'all';
  optAll.id = 'opt-country-all';
  optAll.textContent = I18N[currentLang].optCountryAll;
  select.appendChild(optAll);

  const sorted = [...ALL_COUNTRIES].sort((a, b) => {
    const nameA = currentLang === 'es' ? a.es : a.en;
    const nameB = currentLang === 'es' ? b.es : b.en;
    return nameA.localeCompare(nameB);
  });

  sorted.forEach(c => {
    const opt = document.createElement('option');
    opt.value = c.key;
    const name = currentLang === 'es' ? c.es : c.en;
    opt.textContent = `${c.flag} ${name}`;
    select.appendChild(opt);
  });

  select.value = currentVal;
}

function getFilteredGrapes() {
  const colorFilter = document.querySelector('#color-filter-group .seg-btn.active')?.dataset.color || 'all';
  const countryFilter = document.getElementById('country-filter')?.value || 'all';
  const styleFilter = document.getElementById('style-filter')?.value || 'all';
  const blendFilter = document.getElementById('blend-filter')?.value || 'all';
  const searchQuery = (document.getElementById('grape-search')?.value || '').toLowerCase().trim();

  return allGrapes.filter(g => {
    // 1. Color filter
    if (colorFilter !== 'all' && g.color !== colorFilter) {
      return false;
    }

    // 2. Country filter
    if (countryFilter !== 'all') {
      const matchCountry = g.countries_breakdown && g.countries_breakdown.some(c => 
        c.country === countryFilter || c.country_es === countryFilter || c.country_en === countryFilter
      );
      if (!matchCountry) return false;
    }

    // 3. Style filter
    if (styleFilter !== 'all') {
      if (!g.styles_breakdown || (g.styles_breakdown[styleFilter] || 0) === 0) {
        return false;
      }
    }

    // 4. Blend filter
    if (blendFilter !== 'all') {
      if (!g.blend_breakdown || (g.blend_breakdown[blendFilter] || 0) === 0) {
        return false;
      }
    }

    // 5. Search query
    if (searchQuery) {
      const matchName = g.name.toLowerCase().includes(searchQuery);
      const matchSyn = g.synonyms && g.synonyms.some(s => s.toLowerCase().includes(searchQuery));
      if (!matchName && !matchSyn) return false;
    }

    return true;
  });
}

function renderVarietyMatrix() {
  const container = document.getElementById('variety-matrix-grid');
  const counter = document.getElementById('matrix-counter');
  if (!container) return;

  const filtered = getFilteredGrapes();
  const t = I18N[currentLang];

  if (counter) {
    counter.textContent = currentLang === 'es'
      ? `Mostrando ${filtered.length} de ${allGrapes.length} variedades`
      : `Showing ${filtered.length} of ${allGrapes.length} varieties`;
  }

  container.innerHTML = '';

  if (filtered.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'matrix-empty-state';
    empty.innerHTML = `
      <p>${t.noMatrixMatches}</p>
      <button type="button" class="btn-clear-filters" id="btn-matrix-clear">${t.btnClearFilters}</button>
    `;
    container.appendChild(empty);
    document.getElementById('btn-matrix-clear')?.addEventListener('click', resetAllFilters);
    return;
  }

  // Sort: Alphabetical (A-Z) by default, or by presence in appellations
  const sortMode = document.getElementById('matrix-sort-select')?.value || 'alpha';
  const sorted = [...filtered].sort((a, b) => {
    if (sortMode === 'regions') {
      if (b.total_regions !== a.total_regions) {
        return b.total_regions - a.total_regions;
      }
    }
    return a.name.localeCompare(b.name, currentLang, { sensitivity: 'base' });
  });

  sorted.forEach(g => {
    const btn = document.createElement('button');
    const isSelected = selectedGrapeObj && (selectedGrapeObj.name.toLowerCase() === g.name.toLowerCase() || selectedGrapeObj.id === g.id);
    btn.className = `variety-card ${g.color} ${isSelected ? 'active' : ''}`;
    btn.dataset.name = g.name;

    const flags = (g.countries_breakdown || []).slice(0, 3).map(c => c.flag).join(' ');
    const regLabel = currentLang === 'es' ? 'reg.' : 'reg.';

    btn.innerHTML = `
      <div class="vcard-top">
        <span class="vcard-color-dot ${g.color}"></span>
        <span class="vcard-name" title="${g.name}">${g.name}</span>
      </div>
      <div class="vcard-meta">
        <span class="vcard-regions">${g.total_regions} ${regLabel}</span>
        <span class="vcard-flags" title="${(g.countries_breakdown || []).map(c => c.country).join(', ')}">${flags}</span>
      </div>
    `;

    btn.addEventListener('click', () => {
      selectGrape(g.name);
    });

    container.appendChild(btn);
  });
}

function resetAllFilters() {
  document.querySelectorAll('#color-filter-group .seg-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.color === 'all');
  });
  const countrySelect = document.getElementById('country-filter');
  if (countrySelect) countrySelect.value = 'all';
  const styleSelect = document.getElementById('style-filter');
  if (styleSelect) styleSelect.value = 'all';
  const blendSelect = document.getElementById('blend-filter');
  if (blendSelect) blendSelect.value = 'all';
  const searchInput = document.getElementById('grape-search');
  if (searchInput) searchInput.value = '';
  activeCountryFilter = null;

  renderVarietyMatrix();
  if (allGrapes.length > 0) {
    selectGrape('Tempranillo');
  }
}

function selectGrape(grapeName) {
  const match = allGrapes.find(g => g.name.toLowerCase() === grapeName.toLowerCase() || g.id === grapeName.toLowerCase());
  if (!match) return;

  selectedGrapeObj = match;
  clearActivePolygon(false);

  const countrySelect = document.getElementById('country-filter');
  if (countrySelect && countrySelect.value !== 'all') {
    activeCountryFilter = countrySelect.value;
  } else {
    activeCountryFilter = null;
  }

  renderHeroCard();
  renderDonutChart();
  renderStylesChart();
  updateMapRegions();
  renderTable();

  // Highlight active variety card in matrix
  document.querySelectorAll('.variety-card').forEach(c => {
    c.classList.toggle('active', c.dataset.name === selectedGrapeObj.name);
  });
}

function renderHeroCard() {
  if (!selectedGrapeObj) return;
  const g = selectedGrapeObj;
  const t = I18N[currentLang];

  const badge = document.getElementById('hero-color-badge');
  badge.textContent = g.color === 'red' ? t.redBadge : t.whiteBadge;
  badge.className = `hero-color-badge ${g.color === 'white' ? 'white-badge' : ''}`;

  document.getElementById('hero-grape-name').textContent = g.name;
  document.getElementById('hero-origin').innerHTML = `📍 ${t.origin} <span>${g.origin}</span>`;

  document.getElementById('stat-countries').textContent = g.countries_count;
  document.getElementById('stat-regions').textContent = g.total_regions;
  document.getElementById('stat-monovarietal').textContent = `${g.blend_breakdown.monovarietal_pct}%`;

  const desc = currentLang === 'es' ? g.desc_es : g.desc_en;
  document.getElementById('hero-description').textContent = desc;

  const synWrap = document.getElementById('hero-synonyms-chips');
  synWrap.innerHTML = '';
  if (g.synonyms && g.synonyms.length > 0) {
    g.synonyms.forEach(syn => {
      const sp = document.createElement('span');
      sp.className = 'syn-chip';
      sp.textContent = syn;
      synWrap.appendChild(sp);
    });
  } else {
    const sp = document.createElement('span');
    sp.className = 'syn-chip';
    sp.style.fontStyle = 'italic';
    sp.textContent = t.noSynonyms;
    synWrap.appendChild(sp);
  }
}

/* Donut Chart SVG Rendering */
function renderDonutChart() {
  if (!selectedGrapeObj) return;
  const g = selectedGrapeObj;
  const t = I18N[currentLang];

  const svg = document.getElementById('donut-svg');
  svg.innerHTML = '';

  const legend = document.getElementById('donut-legend');
  legend.innerHTML = '';

  const total = g.total_regions;
  document.getElementById('donut-center-count').textContent = total;
  document.getElementById('donut-center-label').textContent = t.appellationsFound;

  const btnReset = document.getElementById('btn-reset-country-filter');
  btnReset.style.display = activeCountryFilter ? 'inline-flex' : 'none';

  const radius = 110;
  const strokeWidth = 38;
  const cx = 160;
  const cy = 160;
  const circumference = 2 * Math.PI * radius;

  let currentOffset = 0;

  g.countries_breakdown.forEach((item, index) => {
    const color = PALETTE[index % PALETTE.length];
    const pct = item.percentage / 100;
    const strokeDasharray = `${pct * circumference} ${(1 - pct) * circumference}`;
    const strokeDashoffset = -currentOffset;
    currentOffset += pct * circumference;

    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', cx);
    circle.setAttribute('cy', cy);
    circle.setAttribute('r', radius);
    circle.setAttribute('fill', 'transparent');
    circle.setAttribute('stroke', color);
    circle.setAttribute('stroke-width', strokeWidth);
    circle.setAttribute('stroke-dasharray', strokeDasharray);
    circle.setAttribute('stroke-dashoffset', strokeDashoffset);
    circle.setAttribute('class', 'donut-slice');

    const countryName = currentLang === 'es' ? item.country_es : item.country_en;
    const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
    title.textContent = `${item.flag} ${countryName}: ${item.count} (${item.percentage}%)`;
    circle.appendChild(title);

    circle.addEventListener('click', () => {
      toggleCountryFilter(item.country);
    });

    svg.appendChild(circle);

    // Legend Row
    const row = document.createElement('div');
    row.className = `legend-row ${activeCountryFilter === item.country ? 'active' : ''}`;
    row.innerHTML = `
      <div class="legend-left">
        <span class="color-dot" style="background: ${color}"></span>
        <span>${item.flag} ${countryName}</span>
      </div>
      <span class="legend-pct">${item.percentage}% (${item.count})</span>
    `;
    row.addEventListener('click', () => {
      toggleCountryFilter(item.country);
    });
    legend.appendChild(row);
  });
}

function toggleCountryFilter(country) {
  const countrySelect = document.getElementById('country-filter');
  if (activeCountryFilter === country) {
    activeCountryFilter = null;
    if (countrySelect) countrySelect.value = 'all';
  } else {
    activeCountryFilter = country;
    if (countrySelect) countrySelect.value = country;
  }
  renderVarietyMatrix();
  renderDonutChart();
  updateMapRegions();
  renderTable();
}

function renderStylesChart() {
  if (!selectedGrapeObj) return;
  const g = selectedGrapeObj;
  const t = I18N[currentLang];
  const total = g.total_regions || 1;

  const still = g.styles_breakdown.still || 0;
  const sparkling = g.styles_breakdown.sparkling || 0;
  const fortified = g.styles_breakdown.fortified_sweet || 0;

  const stillPct = Math.round((still / total) * 100);
  const sparkPct = Math.round((sparkling / total) * 100);
  const fortPct = Math.max(0, 100 - stillPct - sparkPct);

  document.getElementById('seg-still').style.width = `${stillPct}%`;
  document.getElementById('seg-sparkling').style.width = `${sparkPct}%`;
  document.getElementById('seg-fortified').style.width = `${fortPct}%`;

  document.getElementById('styles-meta').textContent = 
    `${t.lblLegStill}: ${still} (${stillPct}%) | ${t.lblLegSparkling}: ${sparkling} (${sparkPct}%) | ${t.lblLegFortified}: ${fortified} (${fortPct}%)`;

  const monoPct = g.blend_breakdown.monovarietal_pct || 0;
  const blendPct = g.blend_breakdown.blend_pct || 0;

  document.getElementById('seg-mono').style.width = `${monoPct}%`;
  document.getElementById('seg-blend').style.width = `${blendPct}%`;

  document.getElementById('blend-meta').textContent = 
    `${t.lblLegMono}: ${monoPct}% | ${t.lblLegBlend}: ${blendPct}%`;

  // Benchmark text highlight
  const benchmarkWrap = document.getElementById('lbl-benchmark-desc');
  const benchmarkRegions = g.regions.filter(r => r.pct && r.pct >= 70).slice(0, 4);
  if (benchmarkRegions.length > 0) {
    const listNames = benchmarkRegions.map(r => `${r.name} (${r.pct}%)`).join(', ');
    benchmarkWrap.textContent = listNames;
  } else {
    benchmarkWrap.textContent = g.regions.slice(0, 3).map(r => `${r.name} (${r.country})`).join(', ');
  }
}

/* Option A: Hybrid Vector Polygons Loader & MapLibre Integration */
async function ensureFullRegionsLoaded() {
  if (fullRegionsIndex) return fullRegionsIndex;
  if (!fullRegionsPromise) {
    fullRegionsPromise = (async () => {
      let data = null;
      if (typeof SPAIN_WINE_DATA !== 'undefined' && SPAIN_WINE_DATA) {
        data = SPAIN_WINE_DATA;
      } else if (typeof window !== 'undefined' && typeof window.SPAIN_WINE_DATA !== 'undefined' && window.SPAIN_WINE_DATA) {
        data = window.SPAIN_WINE_DATA;
      } else {
        try {
          const resp = await fetch('data/spain_wine_regions.geojson');
          if (resp.ok) {
            data = await resp.json();
          }
        } catch (e) {
          console.warn("GeoJSON fetch deferred or fallback required:", e);
        }
        if (!data) {
          await new Promise((resolve) => {
            const script = document.createElement('script');
            script.src = 'data/spain_wine_regions.js';
            script.onload = resolve;
            script.onerror = resolve;
            document.head.appendChild(script);
          });
          if (typeof SPAIN_WINE_DATA !== 'undefined' && SPAIN_WINE_DATA) {
            data = SPAIN_WINE_DATA;
          } else if (typeof window !== 'undefined' && typeof window.SPAIN_WINE_DATA !== 'undefined') {
            data = window.SPAIN_WINE_DATA;
          }
        }
      }

      const byId = new Map();
      const byName = new Map();
      if (data && data.features) {
        for (let i = 0; i < data.features.length; i++) {
          const f = data.features[i];
          if (f.properties) {
            if (f.properties.id) byId.set(f.properties.id, f);
            if (f.properties.name) byName.set(f.properties.name.toLowerCase().trim(), f);
          }
        }
      }
      fullRegionsIndex = { byId, byName };
      return fullRegionsIndex;
    })();
  }
  return fullRegionsPromise;
}

function extendBoundsWithGeom(bounds, geom) {
  if (!geom || !geom.coordinates) return;
  const coords = geom.coordinates;
  if (geom.type === 'Polygon') {
    for (let r = 0; r < coords.length; r++) {
      for (let p = 0; p < coords[r].length; p++) {
        bounds.extend(coords[r][p]);
      }
    }
  } else if (geom.type === 'MultiPolygon') {
    for (let m = 0; m < coords.length; m++) {
      for (let r = 0; r < coords[m].length; r++) {
        for (let p = 0; p < coords[m][r].length; p++) {
          bounds.extend(coords[m][r][p]);
        }
      }
    }
  } else if (geom.type === 'Point') {
    bounds.extend(coords);
  }
}

function ensurePolygonLayers() {
  if (!map) return;

  if (!map.getSource('active-region-polygon')) {
    map.addSource('active-region-polygon', {
      type: 'geojson',
      data: { type: 'FeatureCollection', features: [] }
    });
  }

  const beforeLayer = map.getLayer('grape-regions-circles') ? 'grape-regions-circles' : undefined;

  if (!map.getLayer('active-region-fill')) {
    map.addLayer({
      id: 'active-region-fill',
      type: 'fill',
      source: 'active-region-polygon',
      paint: {
        'fill-color': ['coalesce', ['get', 'color'], '#7C2D12'],
        'fill-opacity': 0.42
      }
    }, beforeLayer);
  }

  if (!map.getLayer('active-region-line')) {
    map.addLayer({
      id: 'active-region-line',
      type: 'line',
      source: 'active-region-polygon',
      paint: {
        'line-color': ['coalesce', ['get', 'color'], '#7C2D12'],
        'line-width': 2.8,
        'line-opacity': 0.95
      }
    }, beforeLayer);
  }
}

async function highlightAndZoomToRegion(regionId, regionName, centroid) {
  if (!map) return;

  // Smooth scroll towards the map if not in full view
  const mapCard = document.querySelector('.map-section-card');
  if (mapCard) {
    mapCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  // Find region in current grape variety list
  const regObj = selectedGrapeObj?.regions.find(r => 
    r.id === regionId || (r.name && r.name.toLowerCase() === (regionName || '').toLowerCase())
  );

  const badge = document.getElementById('active-polygon-badge');
  const badgeName = document.getElementById('active-polygon-name');
  if (badge && badgeName) {
    badgeName.textContent = regionName || regObj?.name || regionId;
    badge.style.display = 'inline-flex';
  }

  ensurePolygonLayers();

  const idx = await ensureFullRegionsLoaded();
  let feature = null;
  if (idx) {
    if (regionId && idx.byId.has(regionId)) {
      feature = idx.byId.get(regionId);
    } else if (regionName && idx.byName.has(regionName.toLowerCase().trim())) {
      feature = idx.byName.get(regionName.toLowerCase().trim());
    } else if (regObj && idx.byName.has(regObj.name.toLowerCase().trim())) {
      feature = idx.byName.get(regObj.name.toLowerCase().trim());
    }
  }

  const regionColor = regObj?.color || feature?.properties?.color || (selectedGrapeObj?.color === 'red' ? '#991B1B' : '#D97706');

  if (feature && feature.geometry) {
    activeRegionPolygon = feature;
    const polyGeojson = {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        geometry: feature.geometry,
        properties: {
          id: feature.properties?.id || regionId,
          name: feature.properties?.name || regionName,
          color: regionColor
        }
      }]
    };
    if (map.getSource('active-region-polygon')) {
      map.getSource('active-region-polygon').setData(polyGeojson);
    }

    const bounds = new maplibregl.LngLatBounds();
    extendBoundsWithGeom(bounds, feature.geometry);

    if (!bounds.isEmpty()) {
      map.fitBounds(bounds, {
        padding: { top: 60, bottom: 60, left: 60, right: 60 },
        duration: 1200,
        maxZoom: 11.5
      });
    } else if (centroid) {
      map.flyTo({ center: centroid, zoom: 9.5, duration: 1000 });
    }
  } else {
    if (map.getSource('active-region-polygon')) {
      map.getSource('active-region-polygon').setData({ type: 'FeatureCollection', features: [] });
    }
    if (centroid) {
      map.flyTo({ center: centroid, zoom: 9.5, duration: 1000 });
    }
  }

  let popupCoords = centroid;
  if (!popupCoords && feature && feature.geometry) {
    const b = new maplibregl.LngLatBounds();
    extendBoundsWithGeom(b, feature.geometry);
    if (!b.isEmpty()) {
      popupCoords = b.getCenter().toArray();
    }
  }
  if (popupCoords) {
    showRegionPopup(regObj, feature, popupCoords);
  }
}

function showRegionPopup(regObj, feature, coords) {
  if (!map) return;
  if (activeMapPopup) {
    activeMapPopup.remove();
  }

  const t = I18N[currentLang];
  const name = regObj?.name || feature?.properties?.name || 'Region';
  const country = regObj?.country || feature?.properties?.country || '';
  const countryFlag = regObj?.country_flag || '🌍';
  const category = regObj?.category || feature?.properties?.category || '';
  const role = regObj?.role || 'Authorized';
  const color = regObj?.color || feature?.properties?.color || '#7C2D12';
  const styles = regObj?.styles ? regObj.styles.map(s => {
    if (s === 'still') return '🍷 Still';
    if (s === 'sparkling') return '🥂 Sparkling';
    if (s === 'fortified_sweet') return '🍯 Fortified';
    return s;
  }).join(' • ') : '';
  const pliego = regObj?.pliego || feature?.properties?.pliego;

  const html = `
    <div class="grape-popup-content">
      <div class="popup-top">
        <span class="popup-cat" style="background: ${color}">${category}</span>
        <span class="popup-country">${countryFlag} ${country}</span>
      </div>
      <h4 class="popup-title">${name}</h4>
      <div class="popup-role-box">
        <span class="popup-role-badge">${role}</span>
        ${styles ? `<div class="popup-styles">${styles}</div>` : ''}
      </div>
      <div class="popup-actions">
        <a href="index.html?do=${encodeURIComponent(name)}" target="_blank" class="btn-popup-action">
          ${t.btnOpenWineMap || '🗺️ Open in Wine Map'}
        </a>
        ${pliego ? `
          <a href="https://github.com/jreyes13/wine_world_wide/blob/main/${encodeURI(pliego)}" target="_blank" rel="noopener noreferrer" class="btn-popup-action secondary">
            ${t.btnPliego}
          </a>
        ` : ''}
      </div>
    </div>
  `;

  activeMapPopup = new maplibregl.Popup({ closeButton: true, closeOnClick: false, offset: 12 })
    .setLngLat(coords)
    .setHTML(html)
    .addTo(map);
}

function clearActivePolygon(refit = true) {
  activeRegionPolygon = null;
  const badge = document.getElementById('active-polygon-badge');
  if (badge) badge.style.display = 'none';

  if (map && map.getSource('active-region-polygon')) {
    map.getSource('active-region-polygon').setData({ type: 'FeatureCollection', features: [] });
  }

  if (activeMapPopup) {
    activeMapPopup.remove();
    activeMapPopup = null;
  }

  if (refit && map && selectedGrapeObj) {
    fitToAllGrapeRegions();
  }
}

function fitToAllGrapeRegions() {
  if (!map || !selectedGrapeObj) return;
  let regions = selectedGrapeObj.regions;
  if (activeCountryFilter) {
    regions = regions.filter(r => r.country === activeCountryFilter);
  }
  if (regions.length > 0) {
    const bounds = new maplibregl.LngLatBounds();
    regions.forEach(r => {
      if (r.centroid) bounds.extend(r.centroid);
    });
    if (!bounds.isEmpty()) {
      map.fitBounds(bounds, { padding: 60, maxZoom: 8, duration: 1000 });
    }
  }
}

/* MapLibre GeoJSON Points Update */
function updateMapRegions() {
  if (!map || !selectedGrapeObj) return;

  let regions = selectedGrapeObj.regions;
  if (activeCountryFilter) {
    regions = regions.filter(r => r.country === activeCountryFilter);
  }

  // Apply secondary filters
  const colorFilter = document.querySelector('.seg-btn.active').dataset.color;
  const styleFilter = document.getElementById('style-filter').value;
  const blendFilter = document.getElementById('blend-filter').value;

  if (styleFilter !== 'all') {
    regions = regions.filter(r => r.styles.includes(styleFilter));
  }
  if (blendFilter !== 'all') {
    regions = regions.filter(r => r.blend_type === blendFilter);
  }

  const features = regions.map(r => ({
    type: 'Feature',
    geometry: {
      type: 'Point',
      coordinates: r.centroid
    },
    properties: {
      id: r.id,
      name: r.name,
      country: r.country,
      country_flag: r.country_flag,
      category: r.category,
      region: r.region,
      role: r.role,
      pct: r.pct || '',
      color: selectedGrapeObj.color === 'red' ? '#991B1B' : '#D97706'
    }
  }));

  const geojson = {
    type: 'FeatureCollection',
    features: features
  };

  ensurePolygonLayers();

  if (map.getSource('grape-regions')) {
    map.getSource('grape-regions').setData(geojson);
  } else {
    map.addSource('grape-regions', {
      type: 'geojson',
      data: geojson
    });

    map.addLayer({
      id: 'grape-regions-circles',
      type: 'circle',
      source: 'grape-regions',
      paint: {
        'circle-radius': [
          'interpolate', ['linear'], ['zoom'],
          3, 6,
          6, 12,
          10, 18
        ],
        'circle-color': ['get', 'color'],
        'circle-opacity': 0.85,
        'circle-stroke-width': 2,
        'circle-stroke-color': '#FFFFFF'
      }
    });

    // Map Click and Popups: clicking circle marker highlights polygon & zooms
    map.on('click', 'grape-regions-circles', (e) => {
      if (!e.features.length) return;
      const f = e.features[0];
      const p = f.properties;
      highlightAndZoomToRegion(p.id, p.name, f.geometry.coordinates);
    });

    // Clicking polygon fill triggers zoom and popup
    map.on('click', 'active-region-fill', (e) => {
      if (!e.features.length) return;
      const f = e.features[0];
      const p = f.properties;
      highlightAndZoomToRegion(p.id, p.name, [e.lngLat.lng, e.lngLat.lat]);
    });

    map.on('mouseenter', 'grape-regions-circles', () => {
      map.getCanvas().style.cursor = 'pointer';
    });
    map.on('mouseleave', 'grape-regions-circles', () => {
      map.getCanvas().style.cursor = '';
    });
    map.on('mouseenter', 'active-region-fill', () => {
      map.getCanvas().style.cursor = 'pointer';
    });
    map.on('mouseleave', 'active-region-fill', () => {
      map.getCanvas().style.cursor = '';
    });
  }

  // Zoom to fit bounds of regions only if no polygon is actively isolated
  if (!activeRegionPolygon && features.length > 0) {
    const bounds = new maplibregl.LngLatBounds();
    features.forEach(f => bounds.extend(f.geometry.coordinates));
    map.fitBounds(bounds, { padding: 60, maxZoom: 8, duration: 1000 });
  }
}

/* Appellations Directory Table */
function renderTable() {
  if (!selectedGrapeObj) return;
  const tbody = document.getElementById('regions-table-body');
  tbody.innerHTML = '';
  const t = I18N[currentLang];

  let regions = selectedGrapeObj.regions;

  if (activeCountryFilter) {
    regions = regions.filter(r => r.country === activeCountryFilter);
  }

  const colorFilter = document.querySelector('.seg-btn.active').dataset.color;
  const styleFilter = document.getElementById('style-filter').value;
  const blendFilter = document.getElementById('blend-filter').value;

  if (styleFilter !== 'all') {
    regions = regions.filter(r => r.styles.includes(styleFilter));
  }
  if (blendFilter !== 'all') {
    regions = regions.filter(r => r.blend_type === blendFilter);
  }

  const query = document.getElementById('table-filter-input').value.toLowerCase().trim();
  if (query) {
    regions = regions.filter(r => 
      r.name.toLowerCase().includes(query) || 
      r.country.toLowerCase().includes(query) ||
      (r.country_en && r.country_en.toLowerCase().includes(query)) ||
      r.region.toLowerCase().includes(query)
    );
  }

  document.getElementById('table-counter-badge').textContent = `${regions.length} ${t.appellationsFound}`;

  if (regions.length === 0) {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td colspan="7" style="text-align: center; color: var(--text-muted); padding: 2rem;">${t.noRegionsFound}</td>`;
    tbody.appendChild(tr);
    return;
  }

  regions.forEach(r => {
    const tr = document.createElement('tr');
    const countryName = currentLang === 'es' ? r.country_es : r.country_en;
    const isBenchmark = r.pct && r.pct >= 75;
    const isDominant = r.pct && r.pct >= 50 && r.pct < 75;

    let roleBadgeClass = 'td-role-tag';
    if (isBenchmark) roleBadgeClass += ' benchmark';
    else if (isDominant) roleBadgeClass += ' dominant';

    const stylesBadges = r.styles.map(s => {
      if (s === 'still') return '🍷 Still';
      if (s === 'sparkling') return '🥂 Sparkling';
      if (s === 'fortified_sweet') return '🍯 Fortified';
      return s;
    }).join(' • ');

    tr.innerHTML = `
      <td><strong>${r.country_flag} ${countryName}</strong></td>
      <td><strong>${r.name}</strong></td>
      <td><span class="td-cat-badge" style="background: ${r.color || '#7C2D12'}">${r.category}</span></td>
      <td>${r.region}</td>
      <td><span class="${roleBadgeClass}">${r.role}</span></td>
      <td><span style="font-size: 0.78rem; color: #475569;">${stylesBadges}</span></td>
      <td>
        <div class="td-actions">
          <button class="btn-table-action btn-zoom-map" data-id="${r.id}" data-name="${r.name}" data-lng="${r.centroid[0]}" data-lat="${r.centroid[1]}">
            ${t.btnViewMap}
          </button>
          ${r.pliego ? `<a href="https://github.com/jreyes13/wine_world_wide/blob/main/${encodeURI(r.pliego)}" target="_blank" rel="noopener noreferrer" class="btn-table-action">${t.btnPliego}</a>` : ''}
        </div>
      </td>
    `;

    tbody.appendChild(tr);
  });

  // Attach zoom buttons: highlights exact polygon boundary and fits bounds smoothly
  document.querySelectorAll('.btn-zoom-map').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const btnElem = e.currentTarget;
      const id = btnElem.dataset.id;
      const name = btnElem.dataset.name;
      const lng = parseFloat(btnElem.dataset.lng);
      const lat = parseFloat(btnElem.dataset.lat);
      highlightAndZoomToRegion(id, name, [lng, lat]);
    });
  });
}

/* Event Listeners Setup */
function setupEventListeners() {
  // Boundary Clear Button
  const btnClearPoly = document.getElementById('btn-clear-polygon');
  if (btnClearPoly) {
    btnClearPoly.addEventListener('click', () => {
      clearActivePolygon(true);
    });
  }

  // Language Switcher
  document.getElementById('btn-lang-en').addEventListener('click', () => setLanguage('en'));
  document.getElementById('btn-lang-es').addEventListener('click', () => setLanguage('es'));

  // Color Filter Segmented Buttons
  document.querySelectorAll('#color-filter-group .seg-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('#color-filter-group .seg-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      renderVarietyMatrix();
      
      const filtered = getFilteredGrapes();
      if (filtered.length > 0) {
        const isStillInList = filtered.some(g => g.name === selectedGrapeObj?.name);
        if (!isStillInList) {
          selectGrape(filtered[0].name);
        } else {
          updateMapRegions();
          renderTable();
        }
      }
    });
  });

  // Country Filter Dropdown
  document.getElementById('country-filter').addEventListener('change', (e) => {
    const val = e.target.value;
    activeCountryFilter = val === 'all' ? null : val;
    renderVarietyMatrix();

    const filtered = getFilteredGrapes();
    if (filtered.length > 0) {
      const isStillInList = filtered.some(g => g.name === selectedGrapeObj?.name);
      if (!isStillInList) {
        selectGrape(filtered[0].name);
      } else {
        renderDonutChart();
        updateMapRegions();
        renderTable();
      }
    }
  });

  // Wine Style Filter
  document.getElementById('style-filter').addEventListener('change', () => {
    renderVarietyMatrix();
    const filtered = getFilteredGrapes();
    if (filtered.length > 0) {
      const isStillInList = filtered.some(g => g.name === selectedGrapeObj?.name);
      if (!isStillInList) {
        selectGrape(filtered[0].name);
      } else {
        updateMapRegions();
        renderTable();
      }
    }
  });

  // Blend Focus Filter
  document.getElementById('blend-filter').addEventListener('change', () => {
    renderVarietyMatrix();
    const filtered = getFilteredGrapes();
    if (filtered.length > 0) {
      const isStillInList = filtered.some(g => g.name === selectedGrapeObj?.name);
      if (!isStillInList) {
        selectGrape(filtered[0].name);
      } else {
        updateMapRegions();
        renderTable();
      }
    }
  });

  // Table Search Filter
  document.getElementById('table-filter-input').addEventListener('input', renderTable);

  // Reset Country Filter Button (from Donut Chart area)
  document.getElementById('btn-reset-country-filter').addEventListener('click', () => {
    activeCountryFilter = null;
    const countrySelect = document.getElementById('country-filter');
    if (countrySelect) countrySelect.value = 'all';
    renderVarietyMatrix();
    renderDonutChart();
    updateMapRegions();
    renderTable();
  });

  // Matrix Grid Height Toggle
  document.getElementById('btn-matrix-toggle').addEventListener('click', () => {
    const grid = document.getElementById('variety-matrix-grid');
    const isExpanded = grid.classList.toggle('expanded');
    const t = I18N[currentLang];
    document.getElementById('btn-matrix-toggle-text').textContent = isExpanded ? t.btnMatrixCollapse : t.btnMatrixExpand;
  });

  // Matrix Sort Selector (Alphabetical vs Regions)
  document.getElementById('matrix-sort-select').addEventListener('change', renderVarietyMatrix);

  // Basemap Switcher
  document.getElementById('basemap-select').addEventListener('change', (e) => {
    const style = BASEMAP_STYLES[e.target.value];
    if (style && map) {
      map.setStyle(style);
      map.once('styledata', () => {
        updateMapRegions();
      });
    }
  });

  // Search Box (Real-time live matrix filter + Autocomplete)
  const searchInput = document.getElementById('grape-search');
  const autoList = document.getElementById('autocomplete-list');

  searchInput.addEventListener('input', (e) => {
    renderVarietyMatrix();

    const q = e.target.value.toLowerCase().trim();
    if (!q) {
      autoList.classList.remove('active');
      return;
    }

    const filtered = getFilteredGrapes();
    const matches = filtered.filter(g => 
      g.name.toLowerCase().includes(q) ||
      (g.synonyms && g.synonyms.some(s => s.toLowerCase().includes(q)))
    ).slice(0, 10);

    autoList.innerHTML = '';
    if (matches.length === 0) {
      autoList.classList.remove('active');
      return;
    }

    matches.forEach(g => {
      const item = document.createElement('div');
      item.className = 'autocomplete-item';
      item.innerHTML = `
        <div>
          <strong>${g.name}</strong> 
          <span style="font-size: 0.75rem; color: #64748B;">(${g.color === 'red' ? '🔴 Red' : '⚪ White'})</span>
        </div>
        <span style="font-size: 0.75rem; font-weight: 700; color: #7C2D12;">${g.total_regions} DOs</span>
      `;
      item.addEventListener('click', () => {
        searchInput.value = g.name;
        autoList.classList.remove('active');
        selectGrape(g.name);
      });
      autoList.appendChild(item);
    });

    autoList.classList.add('active');
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-group')) {
      autoList.classList.remove('active');
    }
  });
}

function setLanguage(lang) {
  currentLang = lang;
  document.getElementById('btn-lang-en').classList.toggle('active', lang === 'en');
  document.getElementById('btn-lang-es').classList.toggle('active', lang === 'es');

  const t = I18N[lang];

  const brandTitleEl = document.getElementById('brand-title');
  if (brandTitleEl) {
    brandTitleEl.innerHTML = `WINE<span class="brand-exp">³</span><span class="brand-ai">ai</span>`;
  }
  document.getElementById('brand-subtitle').textContent = t.brandSubtitle;
  document.getElementById('nav-map-text').textContent = t.navMap;
  document.getElementById('lbl-basemap').title = t.lblBasemap;
  document.getElementById('lbl-color-filter').textContent = t.lblColorFilter;
  document.getElementById('btn-color-all').textContent = t.colorAll;
  document.getElementById('btn-color-red').textContent = t.colorRed;
  document.getElementById('btn-color-white').textContent = t.colorWhite;

  document.getElementById('lbl-country-filter').textContent = t.lblCountryFilter;
  populateCountryFilter();

  document.getElementById('lbl-style-filter').textContent = t.lblStyleFilter;
  document.getElementById('opt-style-all').textContent = t.optStyleAll;
  document.getElementById('opt-style-still').textContent = t.optStyleStill;
  document.getElementById('opt-style-sparkling').textContent = t.optStyleSparkling;
  document.getElementById('opt-style-fortified').textContent = t.optStyleFortified;

  document.getElementById('lbl-blend-filter').textContent = t.lblBlendFilter;
  document.getElementById('opt-blend-all').textContent = t.optBlendAll;
  document.getElementById('opt-blend-mono').textContent = t.optBlendMono;
  document.getElementById('opt-blend-coupage').textContent = t.optBlendCoupage;

  document.getElementById('lbl-search-variety').textContent = t.lblSearchVariety;
  document.getElementById('grape-search').placeholder = t.searchPlaceholder;

  document.getElementById('lbl-matrix-title').textContent = t.lblMatrixTitle;
  document.getElementById('opt-sort-alpha').textContent = t.optSortAlpha;
  document.getElementById('opt-sort-regions').textContent = t.optSortRegions;
  const isExpanded = document.getElementById('variety-matrix-grid')?.classList.contains('expanded');
  document.getElementById('btn-matrix-toggle-text').textContent = isExpanded ? t.btnMatrixCollapse : t.btnMatrixExpand;

  document.getElementById('lbl-stat-countries').textContent = t.lblStatCountries;
  document.getElementById('lbl-stat-regions').textContent = t.lblStatRegions;
  document.getElementById('lbl-stat-monovarietal').textContent = t.lblStatMonovarietal;
  document.getElementById('lbl-synonyms').textContent = t.lblSynonyms;

  document.getElementById('title-donut-chart').textContent = t.titleDonutChart;
  document.getElementById('sub-donut-chart').textContent = t.subDonutChart;
  document.getElementById('lbl-reset-filter').textContent = t.lblResetFilter;

  document.getElementById('title-styles-chart').textContent = t.titleStylesChart;
  document.getElementById('sub-styles-chart').textContent = t.subStylesChart;
  document.getElementById('lbl-styles-title').textContent = t.lblStylesTitle;
  document.getElementById('lbl-leg-still').textContent = t.lblLegStill;
  document.getElementById('lbl-leg-sparkling').textContent = t.lblLegSparkling;
  document.getElementById('lbl-leg-fortified').textContent = t.lblLegFortified;

  document.getElementById('lbl-blend-title').textContent = t.lblBlendTitle;
  document.getElementById('lbl-leg-mono').textContent = t.lblLegMono;
  document.getElementById('lbl-leg-blend').textContent = t.lblLegBlend;
  document.getElementById('lbl-benchmark-title').textContent = t.lblBenchmarkTitle;

  document.getElementById('title-map-section').textContent = t.titleMapSection;
  document.getElementById('sub-map-section').textContent = t.subMapSection;
  document.getElementById('lbl-pill-cultivated').textContent = t.lblPillCultivated;
  const btnClearPoly = document.getElementById('btn-clear-polygon');
  if (btnClearPoly) btnClearPoly.title = t.lblClearBoundary;

  document.getElementById('title-table-section').textContent = t.titleTableSection;
  document.getElementById('sub-table-section').textContent = t.subTableSection;
  document.getElementById('table-filter-input').placeholder = t.tableFilterPlaceholder;

  document.getElementById('th-country').textContent = t.thCountry;
  document.getElementById('th-appellation').textContent = t.thAppellation;
  document.getElementById('th-category').textContent = t.thCategory;
  document.getElementById('th-region').textContent = t.thRegion;
  document.getElementById('th-role').textContent = t.thRole;
  document.getElementById('th-styles').textContent = t.thStyles;
  document.getElementById('th-actions').textContent = t.thActions;

  document.getElementById('footer-link-map').textContent = t.navMap;

  renderVarietyMatrix();
  renderHeroCard();
  renderDonutChart();
  renderStylesChart();
  renderTable();
}
