/**
 * WINE³ai — Grape Pedigree & Genetic Lineage Database
 * Curated from VIVC (Vitis International Variety Catalogue) - Julius Kühn-Institut (JKI)
 * and DNA microsatellite SSR-marker studies (ICVV, CSIC, IMIDRA, UC Davis, INRAE).
 */

window.GRAPE_PEDIGREE_DATA = {
  // 1. Tempranillo
  tempranillo: {
    id: "tempranillo",
    name: "Tempranillo",
    prime_name: "TEMPRANILLO TINTO",
    vivc_id: 12350,
    color: "red",
    country_origin: "España",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural espontáneo (confirmado por marcadores SSR)",
    pedigree_type_en: "Natural spontaneous cross (confirmed by SSR markers)",
    parent1: {
      name: "Albillo Mayor",
      id: "albillo_mayor",
      color: "white",
      flag: "🇪🇸",
      origin_es: "Ribera del Duero / Castilla",
      origin_en: "Ribera del Duero / Castile, Spain",
      vivc_id: 236
    },
    parent2: {
      name: "Benedicto",
      id: "benedicto",
      color: "red",
      flag: "🇪🇸",
      origin_es: "Aragón / Valle del Ebro",
      origin_en: "Aragon / Ebro Valley, Spain",
      vivc_id: 1145
    },
    mutations: [
      {
        name: "Tempranillo Blanco",
        id: "tempranillo_blanco",
        color: "white",
        year: 1988,
        place_es: "Murillo de Río Leza (DOCa Rioja)",
        place_en: "Murillo de Río Leza (DOCa Rioja, Spain)",
        vivc_id: 23223,
        note_es: "Mutación somática de color descubierta en un único sarmiento albino de una cepa centenaria.",
        note_en: "Somatic color mutation discovered on a single white shoot of a centenarian vine."
      }
    ],
    offspring: [
      { name: "Cruces enológicos experimentales y selecciones clonales ibéricas", vivc_id: null }
    ],
    discovery_es: "Identificado en 2012 por investigadores del IMIDRA e ICVV (Javier Ibáñez et al.), demostrando que la uva tinta reina de España nació del enlace natural entre una madre blanca de la Meseta Norte y un padre tinto aragonés.",
    discovery_en: "Identified in 2012 by researchers at IMIDRA and ICVV (Javier Ibáñez et al.), proving that Spain's flagship red grape originated from a natural cross between a white Castilian mother and an Aragonese red father."
  },

  // 2. Cabernet Sauvignon
  cabernet_sauvignon: {
    id: "cabernet_sauvignon",
    name: "Cabernet Sauvignon",
    prime_name: "CABERNET SAUVIGNON",
    vivc_id: 1927,
    color: "red",
    country_origin: "Francia",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural espontáneo (Burdeos, s. XVII)",
    pedigree_type_en: "Natural spontaneous cross (Bordeaux, 17th century)",
    parent1: {
      name: "Cabernet Franc",
      id: "cabernet_franc",
      color: "red",
      flag: "🇫🇷",
      origin_es: "Pirineos / Burdeos / País Vasco",
      origin_en: "Pyrenees / Bordeaux / Basque Country",
      vivc_id: 1926
    },
    parent2: {
      name: "Sauvignon Blanc",
      id: "sauvignon_blanc",
      color: "white",
      flag: "🇫🇷",
      origin_es: "Burdeos / Valle del Loira",
      origin_en: "Bordeaux / Loire Valley",
      vivc_id: 10790
    },
    mutations: [],
    offspring: [],
    discovery_es: "Descubierto en 1997 por la Dra. Carole Meredith y John Bowers en la Universidad de California, Davis: uno de los primeros hitos de la ampelografía genética molecular.",
    discovery_en: "Discovered in 1997 by Dr. Carole Meredith and John Bowers at UC Davis: a foundational milestone in molecular ampelography."
  },

  // 3. Merlot
  merlot: {
    id: "merlot",
    name: "Merlot",
    prime_name: "MERLOT NOIR",
    vivc_id: 7657,
    color: "red",
    country_origin: "Francia",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural espontáneo (Burdeos)",
    pedigree_type_en: "Natural spontaneous cross (Bordeaux)",
    parent1: {
      name: "Magdeleine Noire des Charentes",
      id: "magdeleine_noire",
      color: "red",
      flag: "🇫🇷",
      origin_es: "Bretaña / Charentes (Variedad ancestral)",
      origin_en: "Brittany / Charentes (Ancestral grape)",
      vivc_id: 23152
    },
    parent2: {
      name: "Cabernet Franc",
      id: "cabernet_franc",
      color: "red",
      flag: "🇫🇷",
      origin_es: "Burdeos / País Vasco",
      origin_en: "Bordeaux / Basque Country",
      vivc_id: 1926
    },
    mutations: [],
    offspring: [],
    discovery_es: "Confirmado en 2009 por Jean-Michel Boursiquot: comparte como padre a Cabernet Franc con Cabernet Sauvignon y Carmenère.",
    discovery_en: "Confirmed in 2009 by Jean-Michel Boursiquot: shares Cabernet Franc as a parent with Cabernet Sauvignon and Carmenère."
  },

  // 4. Chardonnay
  chardonnay: {
    id: "chardonnay",
    name: "Chardonnay",
    prime_name: "CHARDONNAY BLANC",
    vivc_id: 2455,
    color: "white",
    country_origin: "Francia",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural espontáneo medieval (Borgoña)",
    pedigree_type_en: "Medieval natural spontaneous cross (Burgundy)",
    parent1: {
      name: "Pinot Noir",
      id: "pinot_noir",
      color: "red",
      flag: "🇫🇷",
      origin_es: "Borgoña (Patriarca noble)",
      origin_en: "Burgundy (Noble patriarch)",
      vivc_id: 9279
    },
    parent2: {
      name: "Gouais Blanc",
      id: "gouais_blanc",
      color: "white",
      flag: "🇫🇷",
      origin_es: "Europa Central / Este de Francia (Heunisch Weiss)",
      origin_en: "Central Europe / Eastern France (Heunisch Weiss)",
      vivc_id: 5364
    },
    mutations: [],
    offspring: [],
    discovery_es: "Descubierto en 1999 en UC Davis: Pinot y la humilde Gouais Blanc (despreciada en la Edad Media) concibieron a la reina de las uvas blancas.",
    discovery_en: "Discovered in 1999 at UC Davis: noble Pinot and peasant Gouais Blanc gave birth to the queen of white grapes."
  },

  // 5. Pinot Noir
  pinot_noir: {
    id: "pinot_noir",
    name: "Pinot Noir",
    prime_name: "PINOT NOIR",
    vivc_id: 9279,
    color: "red",
    country_origin: "Francia",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Variedad Ancestral Fundadora (Patriarca milenario)",
    pedigree_type_en: "Ancestral Founder Variety (Ancient patriarch)",
    parent1: null,
    parent2: null,
    mutations: [
      { name: "Pinot Gris", id: "pinot_gris", color: "white", vivc_id: 9275, note_es: "Mutación somática de color gris/rosáceo.", note_en: "Greyish/pinkish somatic color mutation." },
      { name: "Pinot Blanc", id: "pinot_blanc", color: "white", vivc_id: 9272, note_es: "Mutación albina completa de la baya.", note_en: "Complete white berry mutation." },
      { name: "Pinot Meunier", id: "pinot_meunier", color: "red", vivc_id: 9280, note_es: "Quimera epidérmica con vellosidad blanca en hojas.", note_en: "Chimeric epidermal mutation with white downy leaves." }
    ],
    offspring: [
      { name: "Chardonnay (× Gouais Blanc)", vivc_id: 2455 },
      { name: "Gamay (× Gouais Blanc)", vivc_id: 4377 },
      { name: "Aligoté (× Gouais Blanc)", vivc_id: 312 },
      { name: "Pinotage (× Cinsault)", vivc_id: 9286 }
    ],
    discovery_es: "Una de las cepas más antiguas domesticadas de Vitis vinifera, cultivada en Borgoña desde la época romana.",
    discovery_en: "One of the oldest domesticated Vitis vinifera cultivars, cultivated in Burgundy since Roman antiquity."
  },

  // 6. Syrah
  syrah: {
    id: "syrah",
    name: "Syrah",
    prime_name: "SYRAH",
    vivc_id: 11766,
    color: "red",
    country_origin: "Francia",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural espontáneo (Ródano Norte)",
    pedigree_type_en: "Natural spontaneous cross (Northern Rhône)",
    parent1: {
      name: "Dureza",
      id: "dureza",
      color: "red",
      flag: "🇫🇷",
      origin_es: "Ardèche / Ródano",
      origin_en: "Ardèche / Rhône",
      vivc_id: 3733
    },
    parent2: {
      name: "Mondeuse Blanche",
      id: "mondeuse_blanche",
      color: "white",
      flag: "🇫🇷",
      origin_es: "Saboya / Alpes franceses",
      origin_en: "Savoie / French Alps",
      vivc_id: 7924
    },
    mutations: [],
    offspring: [],
    discovery_es: "Descubierto en 1998 por Carole Meredith (UC Davis) y Jean-Michel Boursiquot (INRAE): desmintió el mito de que provenía de Shiraz (Persia) o Siracusa (Sicilia).",
    discovery_en: "Discovered in 1998 by Carole Meredith and Jean-Michel Boursiquot: debunked myths linking Syrah to Shiraz (Persia) or Syracuse (Sicily)."
  },

  // 7. Cabernet Franc
  cabernet_franc: {
    id: "cabernet_franc",
    name: "Cabernet Franc",
    prime_name: "CABERNET FRANC",
    vivc_id: 1926,
    color: "red",
    country_origin: "Francia / País Vasco",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Variedad Ancestral Fundadora de Burdeos y Pirineos",
    pedigree_type_en: "Ancestral Founder Variety of Bordeaux and Pyrenees",
    parent1: null,
    parent2: null,
    mutations: [],
    offspring: [
      { name: "Cabernet Sauvignon (× Sauvignon Blanc)", vivc_id: 1927 },
      { name: "Merlot (× Magdeleine Noire)", vivc_id: 7657 },
      { name: "Carmenère (× Gros Cabernet)", vivc_id: 2125 }
    ],
    discovery_es: "El gran patriarca de los tintos atlánticos. Originario según la evidencia histórica de las estribaciones pirenaicas y el País Vasco.",
    discovery_en: "The great patriarch of Atlantic reds. Historically rooted in the Pyrenean foothills and Basque Country."
  },

  // 8. Sauvignon Blanc
  sauvignon_blanc: {
    id: "sauvignon_blanc",
    name: "Sauvignon Blanc",
    prime_name: "SAUVIGNON BLANC",
    vivc_id: 10790,
    color: "white",
    country_origin: "Francia",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural (Valle del Loira / Burdeos)",
    pedigree_type_en: "Natural cross (Loire Valley / Bordeaux)",
    parent1: {
      name: "Savagnin (Traminer)",
      id: "savagnin",
      color: "white",
      flag: "🇫🇷",
      origin_es: "Jura / Europa Central",
      origin_en: "Jura / Central Europe",
      vivc_id: 12628
    },
    parent2: {
      name: "Progenitor desconocido",
      id: null,
      color: "white",
      flag: "❓",
      origin_es: "Desconocido",
      origin_en: "Unknown",
      vivc_id: null
    },
    mutations: [],
    offspring: [
      { name: "Cabernet Sauvignon (× Cabernet Franc)", vivc_id: 1927 }
    ],
    discovery_es: "Hijo directo de la milenaria Savagnin/Traminer y padre de Cabernet Sauvignon.",
    discovery_en: "Direct offspring of ancient Savagnin/Traminer and parent to Cabernet Sauvignon."
  },

  // 9. Garnacha / Grenache
  garnacha: {
    id: "garnacha",
    name: "Garnacha Tinta",
    prime_name: "GARNACHA TINTA",
    vivc_id: 4461,
    color: "red",
    country_origin: "España",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Variedad Ancestral Ibérica (Corona de Aragón)",
    pedigree_type_en: "Ancestral Iberian Variety (Crown of Aragon)",
    parent1: null,
    parent2: null,
    mutations: [
      { name: "Garnacha Blanca", id: "garnacha_blanca", color: "white", vivc_id: 4457, note_es: "Mutación albina de color de la baya.", note_en: "White berry somatic mutation." },
      { name: "Garnacha Peluda", id: "garnacha_peluda", color: "red", vivc_id: 4463, note_es: "Mutación morfológica con vellosidad en envés foliar.", note_en: "Morphological mutation with downy leaf undersides." }
    ],
    offspring: [
      { name: "Garnacha Tintorera / Alicante Henri Bouschet (× Petit Bouschet, 1866)", vivc_id: 243 }
    ],
    discovery_es: "Nacida en el noreste de España y propagada por el Mediterráneo (Cerdeña como Cannonau, Rosellón, Ródano).",
    discovery_en: "Born in north-eastern Spain and propagated across the Mediterranean (Sardinia as Cannonau, Roussillon, Southern Rhône)."
  },

  // 10. Verdejo
  verdejo: {
    id: "verdejo",
    name: "Verdejo",
    prime_name: "VERDEJO BLANCO",
    vivc_id: 12949,
    color: "white",
    country_origin: "España",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural ibérico (Castilla / Rueda)",
    pedigree_type_en: "Iberian natural cross (Castile / Rueda)",
    parent1: {
      name: "Savagnin Blanc (Traminer)",
      id: "savagnin",
      color: "white",
      flag: "🇫🇷",
      origin_es: "Europa Central / Jura",
      origin_en: "Central Europe / Jura",
      vivc_id: 12628
    },
    parent2: {
      name: "Castellana Blanca",
      id: "castellana_blanca",
      color: "white",
      flag: "🇪🇸",
      origin_es: "Castilla y León (Autóctona ancestral)",
      origin_en: "Castile and Leon (Ancestral native)",
      vivc_id: 2181
    },
    mutations: [],
    offspring: [],
    discovery_es: "Investigaciones del CSIC demostraron que Verdejo y Godello comparten a Savagnin y Castellana Blanca como padres: son variedades hermanas biológicas.",
    discovery_en: "CSIC genetic research proved that Verdejo and Godello share Savagnin and Castellana Blanca as parents: they are full biological siblings."
  },

  // 11. Godello
  godello: {
    id: "godello",
    name: "Godello",
    prime_name: "GOUVEIO",
    vivc_id: 4874,
    color: "white",
    country_origin: "España / Portugal",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural (Galicia / Valdeorras / Douro)",
    pedigree_type_en: "Natural cross (Galicia / Valdeorras / Douro)",
    parent1: {
      name: "Savagnin Blanc (Traminer)",
      id: "savagnin",
      color: "white",
      flag: "🇫🇷",
      origin_es: "Europa Central / Jura",
      origin_en: "Central Europe / Jura",
      vivc_id: 12628
    },
    parent2: {
      name: "Castellana Blanca",
      id: "castellana_blanca",
      color: "white",
      flag: "🇪🇸",
      origin_es: "Castilla y León (Autóctona ancestral)",
      origin_en: "Castile and Leon (Ancestral native)",
      vivc_id: 2181
    },
    mutations: [],
    offspring: [],
    discovery_es: "Hermana genética del Verdejo rescatada de la extinción en los años 70 en Valdeorras por el proyecto Revival.",
    discovery_en: "Genetic sibling of Verdejo, rescued from near-extinction in the 1970s in Valdeorras by Project Revival."
  },

  // 12. Albariño
  albarino: {
    id: "albarino",
    name: "Albariño",
    prime_name: "ALVARINHO",
    vivc_id: 221,
    color: "white",
    country_origin: "España / Portugal",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Variedad Ancestral Galaico-Portuguesa",
    pedigree_type_en: "Ancestral Galician-Portuguese Variety",
    parent1: null,
    parent2: null,
    mutations: [],
    offspring: [],
    discovery_es: "Los análisis de ADN descartaron la leyenda monástica de que procedía de Riesling traído por los monjes de Cluny: es una cepa 100% autóctona del noroeste peninsular emparentada con Loureiro y Caíño Blanco.",
    discovery_en: "DNA profiling dismissed the monk legend attributing its origin to German Riesling brought by Cluny pilgrims: it is 100% indigenous to the NW Iberian peninsula, closely related to Loureiro."
  },

  // 13. Sangiovese
  sangiovese: {
    id: "sangiovese",
    name: "Sangiovese",
    prime_name: "SANGIOVESE",
    vivc_id: 10680,
    color: "red",
    country_origin: "Italia",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural (Toscana / Sur de Italia)",
    pedigree_type_en: "Natural cross (Tuscany / Southern Italy)",
    parent1: {
      name: "Ciliegiolo",
      id: "ciliegiolo",
      color: "red",
      flag: "🇮🇹",
      origin_es: "Toscana / Umbría",
      origin_en: "Tuscany / Umbria",
      vivc_id: 2639
    },
    parent2: {
      name: "Calabrese di Montenuovo",
      id: "calabrese_montenuovo",
      color: "red",
      flag: "🇮🇹",
      origin_es: "Campania / Calabria",
      origin_en: "Campania / Calabria",
      vivc_id: 1968
    },
    mutations: [],
    offspring: [],
    discovery_es: "El alma de Chianti, Brunello di Montalcino y Vino Nobile es hija del enlace entre la toscana Ciliegiolo y una variedad ancestral del sur de Italia.",
    discovery_en: "The heart of Chianti, Brunello and Vino Nobile derives from Ciliegiolo and an ancient Southern Italian variety."
  },

  // 14. Macabeo / Viura
  macabeo: {
    id: "macabeo",
    name: "Macabeo / Viura",
    prime_name: "MACABEO",
    vivc_id: 7037,
    color: "white",
    country_origin: "España",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural (Valle del Ebro / Cataluña)",
    pedigree_type_en: "Natural cross (Ebro Valley / Catalonia)",
    parent1: {
      name: "Brustiano Falso",
      id: "brustiano_falso",
      color: "white",
      flag: "🇪🇸",
      origin_es: "Península Ibérica",
      origin_en: "Iberian Peninsula",
      vivc_id: 1710
    },
    parent2: {
      name: "Hebén",
      id: "heben",
      color: "white",
      flag: "🇪🇸",
      origin_es: "Península Ibérica (Cepa morisca ancestral)",
      origin_en: "Iberian Peninsula (Moorish ancestral grape)",
      vivc_id: 5300
    },
    mutations: [],
    offspring: [],
    discovery_es: "Hijo de Hebén, la gran uva madre andalusí documentada por Alonso de Herrera en 1513, que dio origen a decenas de variedades peninsulares.",
    discovery_en: "Descendant of Hebén, the great Andalusian matriarch grape documented by Gabriel Alonso de Herrera in 1513."
  },

  // 15. Xarel·lo
  xarello: {
    id: "xarello",
    name: "Xarel·lo",
    prime_name: "XARELLO",
    vivc_id: 13270,
    color: "white",
    country_origin: "España",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural catalán (Penedès)",
    pedigree_type_en: "Catalan natural cross (Penedès)",
    parent1: {
      name: "Brustiano Falso",
      id: "brustiano_falso",
      color: "white",
      flag: "🇪🇸",
      origin_es: "Península Ibérica",
      origin_en: "Iberian Peninsula",
      vivc_id: 1710
    },
    parent2: {
      name: "Gibi (Hebén)",
      id: "gibi_heben",
      color: "white",
      flag: "🇪🇸",
      origin_es: "Península Ibérica",
      origin_en: "Iberian Peninsula",
      vivc_id: 5300
    },
    mutations: [],
    offspring: [],
    discovery_es: "La columna vertebral del Cava y Corpinnat por su altísimo contenido en resveratrol y acidez natural, emparentada biológicamente con Macabeo.",
    discovery_en: "The backbone of high-end sparkling wines (Cava, Corpinnat), exceptionally rich in natural resveratrol and acid tension."
  },

  // 16. Pedro Ximénez
  pedro_ximenez: {
    id: "pedro_ximenez",
    name: "Pedro Ximénez",
    prime_name: "PEDRO XIMENEZ",
    vivc_id: 9080,
    color: "white",
    country_origin: "España",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural andaluz (Montilla / Jerez)",
    pedigree_type_en: "Andalusian natural cross (Montilla / Jerez)",
    parent1: {
      name: "Hebén",
      id: "heben",
      color: "white",
      flag: "🇪🇸",
      origin_es: "Andalucía (Matriarca morisca)",
      origin_en: "Andalusia (Moorish matriarch)",
      vivc_id: 5300
    },
    parent2: {
      name: "Progenitor desconocido",
      id: null,
      color: "white",
      flag: "❓",
      origin_es: "Desconocido",
      origin_en: "Unknown",
      vivc_id: null
    },
    mutations: [],
    offspring: [],
    discovery_es: "Desmitificado su supuesto origen alemán (el mito del soldado Peter Siemens de Flandes): el ADN probó que es 100% andaluza e hija de la variedad morisca Hebén.",
    discovery_en: "The myth linking PX to German soldier Peter Siemens from Flanders was refuted by DNA: it is an indigenous Andalusian grape sired by Hebén."
  },

  // 17. Palomino Fino
  palomino_fino: {
    id: "palomino_fino",
    name: "Palomino Fino",
    prime_name: "PALOMINO FINO",
    vivc_id: 8888,
    color: "white",
    country_origin: "España",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural andaluz (Marco de Jerez)",
    pedigree_type_en: "Andalusian natural cross (Jerez Sherry Region)",
    parent1: {
      name: "Beba",
      id: "beba",
      color: "white",
      flag: "🇪🇸",
      origin_es: "Andalucía / Extremadura",
      origin_en: "Andalusia / Extremadura",
      vivc_id: 974
    },
    parent2: {
      name: "Progenitor desconocido",
      id: null,
      color: "white",
      flag: "❓",
      origin_es: "Desconocido",
      origin_en: "Unknown",
      vivc_id: null
    },
    mutations: [],
    offspring: [],
    discovery_es: "La reina del velo de flor y de los suelos de albariza del Marco de Jerez y Manzanilla de Sanlúcar.",
    discovery_en: "The queen grape of biological flor aging and white albariza chalk soils in Jerez and Sanlúcar."
  },

  // 18. Mencía
  mencia: {
    id: "mencia",
    name: "Mencía",
    prime_name: "JAEN DU DAO",
    vivc_id: 7623,
    color: "red",
    country_origin: "España / Portugal",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Variedad Ancestral Ibérica (Bierzo / Ribeira Sacra / Dão)",
    pedigree_type_en: "Ancestral Iberian Variety (Bierzo / Ribeira Sacra / Dão)",
    parent1: null,
    parent2: null,
    mutations: [],
    offspring: [],
    discovery_es: "El ADN demostró que es genéticamente idéntica a la Jaen de Portugal y desmintió su supuesto parentesco con Cabernet Franc.",
    discovery_en: "DNA profiling confirmed Mencía is identical to Portugal's Jaen grape, completely debunking the old myth that it derived from Cabernet Franc."
  },

  // 19. Gamay
  gamay: {
    id: "gamay",
    name: "Gamay",
    prime_name: "GAMAY NOIR",
    vivc_id: 4377,
    color: "red",
    country_origin: "Francia",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural medieval (Borgoña / Beaujolais)",
    pedigree_type_en: "Medieval natural cross (Burgundy / Beaujolais)",
    parent1: {
      name: "Pinot Noir",
      id: "pinot_noir",
      color: "red",
      flag: "🇫🇷",
      origin_es: "Borgoña",
      origin_en: "Burgundy",
      vivc_id: 9279
    },
    parent2: {
      name: "Gouais Blanc",
      id: "gouais_blanc",
      color: "white",
      flag: "🇫🇷",
      origin_es: "Centroeuropa",
      origin_en: "Central Europe",
      vivc_id: 5364
    },
    mutations: [],
    offspring: [],
    discovery_es: "Hermana completa de Chardonnay y Aligoté, expulsada de Borgoña en 1395 por el Duque Felipe el Atrevido y coronada en los suelos graníticos de Beaujolais.",
    discovery_en: "Full sibling of Chardonnay and Aligoté, banished from Burgundy in 1395 by Duke Philip the Bold and crowned in Beaujolais granite soils."
  },

  // 20. Carmenère
  carmenere: {
    id: "carmenere",
    name: "Carmenère",
    prime_name: "CARMENERE",
    vivc_id: 2125,
    color: "red",
    country_origin: "Francia / Chile",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural (Burdeos histórico)",
    pedigree_type_en: "Natural cross (Historic Bordeaux)",
    parent1: {
      name: "Cabernet Franc",
      id: "cabernet_franc",
      color: "red",
      flag: "🇫🇷",
      origin_es: "Burdeos / País Vasco",
      origin_en: "Bordeaux / Basque Country",
      vivc_id: 1926
    },
    parent2: {
      name: "Gros Cabernet",
      id: "gros_cabernet",
      color: "red",
      flag: "🇫🇷",
      origin_es: "Burdeos",
      origin_en: "Bordeaux",
      vivc_id: 5041
    },
    mutations: [],
    offspring: [],
    discovery_es: "Desaparecida de Burdeos tras la filoxera y redescubierta en 1994 en Chile por el ampelógrafo Jean-Michel Boursiquot (confundida como Merlot).",
    discovery_en: "Presumed extinct after phylloxera in Bordeaux until rediscovered in Chile in 1994 by ampelographer Jean-Michel Boursiquot."
  },

  // 21. Malbec / Cot
  malbec: {
    id: "malbec",
    name: "Malbec / Cot",
    prime_name: "COT",
    vivc_id: 2880,
    color: "red",
    country_origin: "Francia / Argentina",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural (Suroeste de Francia / Cahors)",
    pedigree_type_en: "Natural cross (South-West France / Cahors)",
    parent1: {
      name: "Prunelard",
      id: "prunelard",
      color: "red",
      flag: "🇫🇷",
      origin_es: "Gaillac / Suroeste de Francia",
      origin_en: "Gaillac / South-West France",
      vivc_id: 9790
    },
    parent2: {
      name: "Magdeleine Noire des Charentes",
      id: "magdeleine_noire",
      color: "red",
      flag: "🇫🇷",
      origin_es: "Charentes / Bretaña",
      origin_en: "Charentes / Brittany",
      vivc_id: 23152
    },
    mutations: [],
    offspring: [],
    discovery_es: "Hermana materna de Merlot (comparten como madre a Magdeleine Noire), nacida en Cahors y encumbrada en los viñedos de gran altitud de Mendoza.",
    discovery_en: "Maternal half-sibling of Merlot (sharing Magdeleine Noire), born in Cahors and elevated to global stardom in Mendoza's high-altitude terroirs."
  },

  // 22. Riesling
  riesling: {
    id: "riesling",
    name: "Riesling",
    prime_name: "RIESLING WEISS",
    vivc_id: 10077,
    color: "white",
    country_origin: "Alemania",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural renano (Valle del Rin)",
    pedigree_type_en: "Rhenish natural cross (Rhine Valley)",
    parent1: {
      name: "Gouais Blanc (Heunisch Weiss)",
      id: "gouais_blanc",
      color: "white",
      flag: "🇩🇪",
      origin_es: "Centroeuropa",
      origin_en: "Central Europe",
      vivc_id: 5364
    },
    parent2: {
      name: "Traminer (Savagnin) × Vid silvestre",
      id: "traminer_sylvestris",
      color: "white",
      flag: "🇩🇪",
      origin_es: "Valle del Rin",
      origin_en: "Rhine Valley",
      vivc_id: null
    },
    mutations: [],
    offspring: [
      { name: "Müller-Thurgau (× Madeleine Royale, 1882)", vivc_id: 8117 }
    ],
    discovery_es: "Mencionada documentalmente por primera vez en 1435 en Rüsselsheim; combina la acidez de Gouais Blanc con la nobleza aromática de Traminer.",
    discovery_en: "First documented in 1435 in Rüsselsheim; marries the crisp acidity of Gouais Blanc with the aromatic nobility of Traminer."
  },

  // 23. Monastrell / Mourvèdre
  monastrell: {
    id: "monastrell",
    name: "Monastrell / Mourvèdre",
    prime_name: "MOURVEDRE",
    vivc_id: 7915,
    color: "red",
    country_origin: "España",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Variedad Ancestral Ibérica (Camp de Morvedre / Sagunto)",
    pedigree_type_en: "Ancestral Iberian Variety (Camp de Morvedre / Sagunto)",
    parent1: null,
    parent2: null,
    mutations: [],
    offspring: [],
    discovery_es: "Su nombre internacional Mourvèdre deriva de Morvedre (Sagunto, Valencia), desde donde se exportó a Francia y al Ródano (como la M de GSM).",
    discovery_en: "Its international name Mourvèdre derives from Morvedre (Sagunto, Valencia), exported to Provence, Bandol and Rhône (the 'M' in GSM blends)."
  },

  // 24. Torrontés Riojano
  torrontes: {
    id: "torrontes",
    name: "Torrontés Riojano",
    prime_name: "TORRONTES RIOJANO",
    vivc_id: 12518,
    color: "white",
    country_origin: "Argentina",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Cruce natural criollo (Argentina)",
    pedigree_type_en: "Criollo natural cross (Argentina)",
    parent1: {
      name: "Criolla Chica (Listán Prieto / Misión)",
      id: "criolla_chica",
      color: "red",
      flag: "🇦🇷",
      origin_es: "Castilla / Islas Canarias (Llegada a América en s. XVI)",
      origin_en: "Castile / Canary Islands (Brought to the Americas in 16th century)",
      vivc_id: 6860
    },
    parent2: {
      name: "Moscatel de Alejandría",
      id: "moscatel",
      color: "white",
      flag: "🇪🇸",
      origin_es: "Mediterráneo",
      origin_en: "Mediterranean",
      vivc_id: 8241
    },
    mutations: [],
    offspring: [],
    discovery_es: "La uva blanca insignia de Argentina nació en la época colonial del cruce espontáneo entre la uva de los misioneros españoles y la aromática Moscatel.",
    discovery_en: "Argentina's flagship white grape arose in colonial times from a natural cross between the Spanish Mission grape and aromatic Muscat of Alexandria."
  },

  // 25. Albillo Mayor
  albillo_mayor: {
    id: "albillo_mayor",
    name: "Albillo Mayor",
    prime_name: "ALBILLO MAYOR",
    vivc_id: 236,
    color: "white",
    country_origin: "España",
    species: "Vitis vinifera L.",
    pedigree_type_es: "Variedad Ancestral Castellana (Progenitora de Tempranillo)",
    pedigree_type_en: "Ancestral Castilian Variety (Parent of Tempranillo)",
    parent1: null,
    parent2: null,
    mutations: [],
    offspring: [
      { name: "Tempranillo (× Benedicto)", vivc_id: 12350 }
    ],
    discovery_es: "Uva blanca autóctona autorizada para los nuevos vinos blancos de la DO Ribera del Duero y madre genética certificada del Tempranillo.",
    discovery_en: "Native white grape authorized for Ribera del Duero whites and certified biological mother of Tempranillo."
  }
};
