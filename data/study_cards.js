// WINE³ai — Banco de Fichas de Estudio y Quizzes de Sumillería
// Fuentes analíticas: WSET Nivel 3, Court of Master Sommeliers (CMS), Máster UDIMA y ASI

(function(root) {
  'use strict';

  var STUDY_CARDS = [
    // --- 1. ARMONÍAS, QUÍMICA & ALIMENTOS CRÍTICOS (UDIMA) ---
    {
      id: "card_cinarina",
      category: "Armonías & Química (UDIMA)",
      standard: "UDIMA",
      question_es: "¿Por qué las alcachofas son consideradas un enemigo clásico del maridaje y qué vino recomienda la sumillería?",
      answer_es: "Contienen cinarina, un compuesto que inhibe temporalmente los receptores del dulzor. Al beber un líquido después, el agua sabe dulce y los vinos tintos tánicos se perciben fuertemente amargos y metálicos.",
      solution_es: "Se solventa con vinos que tengan amargores nobles (Verdejo sobre lías, Grüner Veltliner) o vinos de crianza biológica bajo velo de flor (Fino o Manzanilla de Sanlúcar).",
      tags: ["armonias", "quimica", "alcachofas", "cinarina"]
    },
    {
      id: "card_acid_salt",
      category: "Armonía & Sensorial (CMS & UDIMA)",
      standard: "CMS / UDIMA",
      question_es: "¿Cómo interactúa la sal de un alimento (ej. jamón ibérico o anchoas) con la acidez y los taninos del vino?",
      answer_es: "La sal reduce la percepción de acidez y amargor del vino, realzando su fruta y volumen. Sin embargo, platos salados con vinos fuertemente tánicos pueden desbalancearse si el alimento carece de grasa suficiente.",
      solution_es: "Por eso el Jamón Ibérico de Bellota marida a la perfección con Manzanilla, Fino o Espumosos Brut Nature: la sal y la grasa infiltrada se complementan con la acidez y las lías.",
      tags: ["armonias", "jamon", "sal"]
    },
    {
      id: "card_capsaicina",
      category: "Alimentos Críticos (UDIMA)",
      standard: "UDIMA",
      question_es: "¿Por qué el alcohol y el tanino empeoran las comidas picantes y cuál es la solución molecular?",
      answer_es: "La capsaicina estimula los receptores térmicos vaniloides (TRPV1). El etanol reduce el umbral de activación de estos receptores, aumentando drásticamente la sensación de quemazón. Los taninos aportan astringencia desagradable al paladar inflamado.",
      solution_es: "La solución: vinos con baja graduación alcohólica y azúcar residual (Riesling Kabinett/Spätlese alemán, Chenin Blanc demi-sec) o vinos generosos con textura grasa/glicérica.",
      tags: ["picante", "quimica", "capsaicina"]
    },
    {
      id: "card_jamon_iberico_oleico",
      category: "Armonías & Productos (UDIMA)",
      standard: "UDIMA",
      question_es: "¿Qué características lipídicas tiene el Jamón Ibérico de Bellota y por qué la sumillería descarta los tintos de alta madera?",
      answer_es: "El cerdo alimentado con bellota presenta más de un 55-58% de ácido oleico monoinsaturado, con punto de fusión a 28°C (se funde en la lengua). Los taninos secantes de un tinto maderoso coagulan la grasa en el paladar, tapando la delicadeza del jamón.",
      solution_es: "La armonía canónica es un vino de crianza biológica (Fino/Manzanilla) o espumoso Brut Nature: limpian la película grasa y potencian el umami sin restar elegancia.",
      tags: ["jamon", "armonias", "oleico", "jerez"]
    },

    // --- 2. CATA DEDUCTIVA & MARCADORES DE UVA (CMS) ---
    {
      id: "card_cms_grape_markers",
      category: "Cata Deductiva (CMS)",
      standard: "CMS",
      question_es: "¿Cuáles son los marcadores deductivos clave (Grape Markers) del Cabernet Sauvignon de clima moderado?",
      answer_es: "Cassis / grosella negra, ciruela negra, pimiento verde (pirazinas), grafito, cedro y hojas de tabaco. En boca: acidez media-alta, taninos firmes y cuerpo completo.",
      solution_es: "Si en la cata a ciegas identificas pirazina evidente (nota vegetal/pimiento) junto a cassis concentrado y tanino estructurado, la deducción lógica apunta a Cabernet Sauvignon (Burdeos Izquierda o clima moderado).",
      tags: ["deductive_tasting", "cms", "cabernet", "pirazinas"]
    },
    {
      id: "card_nebbiolo_cms",
      category: "Cata Deductiva (CMS)",
      standard: "CMS",
      question_es: "¿Cómo delata la copa a ciegas una uva Nebbiolo (Barolo / Barbaresco) según la parrilla del Master Sommelier?",
      answer_es: "Vista engañosa: color rubí pálido o granate translúcido con evidente menisco anaranjado/teja prematuro. Nariz: alquitrán ('tar'), pétalos de rosa marchita, cereza ácida, arcilla y cuero. Boca: contraste demoledor con acidez punzante y taninos masivos.",
      solution_es: "La paradoja visual (parece ligero como un Pinot viejo) confrontada con la artillería en boca (tanino agresivo y acidez láser) es la firma indiscutible de Nebbiolo.",
      tags: ["cms", "nebbiolo", "barolo", "piamonte"]
    },
    {
      id: "card_syrah_rotundona",
      category: "Marcadores Químicos (CMS)",
      standard: "CMS",
      question_es: "¿Qué molécula aromática diferencia a la Syrah de la Garnacha en cata a ciegas?",
      answer_es: "La rotundona: un sesquiterpeno que aporta un aroma inequívoco a grano de pimienta negra recién molida, carne ahumada y aceituna negra tapenade. La Garnacha, en cambio, ofrece fruta roja madura (fresa confitada), pimienta blanca y mayor sensación alcohólica.",
      solution_es: "Pimienta negra crujiente + acidez media-alta + tanino firme ➔ Syrah del Ródano Norte (Hermitage, Cornas, Côte-Rôtie).",
      tags: ["cms", "syrah", "rotundona", "pimienta"]
    },
    {
      id: "card_riesling_tdn",
      category: "Marcadores de Uva (CMS)",
      standard: "CMS",
      question_es: "¿Qué compuesto genera las notas de petróleo/hidrocarburo en el Riesling y bajo qué condiciones de cultivo se maximiza?",
      answer_es: "El TDN (1,1,6-trimetil-1,2-dihidronaftaleno). Se origina por degradación de carotenoides presentes en el hollejo, incentivados por una intensa exposición solar sobre pendientes pizarrosas, bajo rendimiento y estrés hídrico moderado.",
      solution_es: "En cata a ciegas: lima kaffir, acidez hiper-alta, textura tensa y fondo mineral de hidrocarburo = Riesling de guarda.",
      tags: ["cms", "riesling", "tdn", "petroleo", "mosel"]
    },
    {
      id: "card_pinot_noir_deductive",
      category: "Cata Deductiva (CMS)",
      standard: "CMS",
      question_es: "¿Cómo se distingue un Pinot Noir de Borgoña (Viejo Mundo) de uno de Oregón o California (Nuevo Mundo)?",
      answer_es: "El Borgoña exhibe acidez alta, color rubí pálido, fruta roja crujiente (arándano, grosella) con notas dominantes de suelo de bosque húmedo, sotobosque y setas. El de Nuevo Mundo muestra fruta más dulce y madura (cereza negra), especias de roble tostado, alcohol superior (> 14%) y taninos más sedosos.",
      solution_es: "La presencia de tierra mojada / sotobosque frente a la opulencia de fruta madura define el origen climáticogeográfico en la deducción de CMS.",
      tags: ["cms", "pinot_noir", "borgona", "nuevo_mundo"]
    },

    // --- 3. ENOLOGÍA & VINIFICACIONES ESPECIALES (UDIMA) ---
    {
      id: "card_crianza_biologica",
      category: "Enología y Vinos Especiales (UDIMA)",
      standard: "UDIMA",
      question_es: "¿Qué condiciones bioquímicas caracterizan la Crianza Biológica en el marco de Jerez y Montilla?",
      answer_es: "Desarrollo del 'velo de flor' (levaduras del género Saccharomyces) en la superficie del vino en botas a 5/6 de capacidad. Consume alcohol, glicerol y oxígeno, aportando acetaldehído y notas punzantes de panadería, frutos secos y tiza.",
      solution_es: "El velo de flor protege al vino de la oxidación, manteniendo su color pálido y confiriéndole un perfil seco, punzante y salino único en el mundo.",
      tags: ["jerez", "enologia", "biologica", "velo_de_flor"]
    },
    {
      id: "card_crianza_oxidativa_jerez",
      category: "Enología Especial (UDIMA)",
      standard: "UDIMA",
      question_es: "¿Qué diferencia la crianza oxidativa del Oloroso de la crianza del Amontillado?",
      answer_es: "El Oloroso se encabeza directamente a 17° vol., impidiendo que nazca el velo de flor; envejece en contacto directo con el oxígeno, oscureciéndose y concentrando alcohol por evaporación ('merma'). El Amontillado es un vino dual: primero tiene crianza biológica bajo velo de flor y, tras agotarse este, pasa a crianza oxidativa.",
      solution_es: "El Amontillado conserva la finura punzante y salina de la flor unida a los frutos secos y barniz de la oxidación posterior.",
      tags: ["jerez", "enologia", "oloroso", "amontillado", "oxidativa"]
    },
    {
      id: "card_maceracion_carbonica",
      category: "Vinificación en Tintos (UDIMA)",
      standard: "UDIMA",
      question_es: "¿Cómo funciona la Maceración Carbónica y qué aroma delata este método en copa?",
      answer_es: "Se introducen racimos enteros sin estrujar en un depósito saturado de dióxido de carbono (CO2). En ausencia de oxígeno, se produce una fermentación enzimática intracelular dentro de cada grano de uva sin levaduras, desdoblando azúcares y ácido málico. Sintetiza acetato de isoamilo, responsable de los aromas de plátano, gominola y canela.",
      solution_es: "Vinos tintos de color púrpura vivo, taninos ultra-suaves, acidez fresca y notas de fruta golosa (Rioja Alavesa joven de cosechero, Beaujolais Nouveau).",
      tags: ["enologia", "maceracion_carbonica", "rioja", "beaujolais"]
    },
    {
      id: "card_espumosos_autolisis",
      category: "Espumosos & Método Tradicional (UDIMA)",
      standard: "UDIMA",
      question_es: "¿En qué consiste la autólisis de las levaduras en el método tradicional (Champagne / Cava) y qué aporta?",
      answer_es: "Tras la segunda fermentación en botella, las levaduras mueren y sus membranas celulares se rompen por acción de sus propias enzimas líticas. Este proceso libera manoproteínas y aminoácidos que enriquecen el vino con volumen en boca, estabilizan la espuma y generan aromas de pan brioche, galleta, masa tostada y frutos secos.",
      solution_es: "Un mínimo de 15 a 36 meses sobre lías garantiza la complejidad autolítica que distingue a los grandes espumosos de guarda.",
      tags: ["espumosos", "champagne", "cava", "autolisis", "lias"]
    },
    {
      id: "card_tca_umbral",
      category: "Defectos del Vino (UDIMA)",
      standard: "UDIMA",
      question_es: "¿Cuál es el umbral de detección del TCA (2,4,6-tricloroanisol) y por qué arruina la experiencia sensorial?",
      answer_es: "El umbral medio humano se sitúa entre 1 y 4 nanogramos por litro (partes por billón). No solo aporta olor a cartón mojado y humedad de sótano, sino que tiene un efecto anestesiante sobre los bulbos olfatorios que suprime por completo los aromas frutales y florales del vino.",
      solution_es: "Ante la sospecha de corcho, el protocolo de sumillería exige retirar la botella de inmediato sin discutir con el comensal.",
      tags: ["defectos", "tca", "corcho", "enologia"]
    },

    // --- 4. TERRUÑO, GEOLOGÍA & FACTORES NATURALES (WSET 3) ---
    {
      id: "card_wset_factors",
      category: "Factores Naturales (WSET 3)",
      standard: "WSET3",
      question_es: "Según el canon WSET 3, ¿cuáles son los 4 factores naturales fundamentales que definen el terruño?",
      answer_es: "1. El clima (temperatura, insolación, pluviometría, continentalidad/maritimidad).\n2. El suelo (retención hídrica, drenaje, nutrientes, reflexión solar de guijarros).\n3. La topografía (altitud, orientación de la ladera, pendiente).\n4. El factor biológico (microbiota del suelo y plagas/vectores).",
      solution_es: "WSET 3 enseña a vincular cada rasgo de la copa (ej. alta acidez por altitud o noches frías) directamente con un factor ambiental específico.",
      tags: ["wset3", "terroir", "clima", "suelo"]
    },
    {
      id: "card_ribera_vs_rioja",
      category: "Terruño & Comparativa (WSET 3)",
      standard: "WSET3",
      question_es: "¿Qué factores climáticos diferencian la expresión de la Tempranillo en Ribera del Duero frente a Rioja?",
      answer_es: "Ribera del Duero se sitúa en la meseta castellana a gran altitud (750 - 950 m) con continentalidad extrema: inviernos gélidos, veranos cortos y oscilaciones térmicas de hasta 20°C entre día y noche que engrosan el hollejo, aportando gran color, tanino potente y acidez vivaz. Rioja (a menor altitud, 350 - 650 m) goza de influencia atlántica moderadora y suelos arcillo-calcáreos que favorecen un perfil más aromático, sedoso y de acidez integrada.",
      solution_es: "Ribera = Estructura, músculo, fruta negra concentrada. Rioja = Elegancia, fruta roja fresca, complejidad de crianza.",
      tags: ["wset3", "ribera_del_duero", "rioja", "tempranillo"]
    },
    {
      id: "card_suelos_llicorella",
      category: "Geología & Edafología (WSET 3)",
      standard: "WSET3",
      question_es: "¿Qué propiedades físicas tiene la Llicorella del Priorat y cómo modela el vino de Garnacha y Cariñena?",
      answer_es: "Es una pizarra paleozoica carbonífera de estructura laminar con mica y cuarzo. Es un suelo sumamente pobre en nutrientes que no retiene agua en superficie, forzando a las raíces a fisurar la roca hasta 15-20 m de profundidad. Las lajas oscuras se calientan durante el día e irradian calor por la noche.",
      solution_es: "Origina rendimientos mínimos (< 1 kg por cepa), taninos maduros y una inconfundible mineralidad de grafito y piedra caliente.",
      tags: ["wset3", "priorat", "llicorella", "suelos", "geologia"]
    },

    // --- 5. PROTOCOLO DE SALA & DIRECTRICES DE SERVICIO (ASI) ---
    {
      id: "card_decantacion_vs_jarreo",
      category: "Servicio & Sala (Norma ASI)",
      standard: "ASI",
      question_es: "Según el estándar de la ASI, ¿en qué se diferencia la decantación del jarreado (trasiego) y cuándo se aplica cada una?",
      answer_es: "La decantación se realiza sobre una vela encendida con movimiento pausado y continuo para separar sedimentos sólidos en vinos viejos sin oxigenarlos en exceso. El jarreado (aireación) se realiza volcando el vino con fuerza en un decantador de base ancha para aportar oxígeno a vinos jóvenes tánicos que se encuentran aromáticamente cerrados o reducidos.",
      solution_es: "Nunca agitar un vino viejo en decantador: el choque brusco de oxígeno puede destruir sus delicados aromas terciarios en minutos.",
      tags: ["asi", "servicio", "decantacion", "protocolo", "sumiller"]
    }
  ];

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = STUDY_CARDS;
  } else {
    root.STUDY_CARDS = STUDY_CARDS;
  }
})(typeof window !== 'undefined' ? window : globalThis);
