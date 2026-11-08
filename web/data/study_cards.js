// WINE³ai — Banco de Fichas de Estudio y Quizzes de Sumillería
// Fuentes analíticas: WSET Nivel 3, Court of Master Sommeliers (CMS) y Máster UDIMA

(function(root) {
  'use strict';

  var STUDY_CARDS = [
    {
      id: "card_cinarina",
      category: "Armonías & Química (UDIMA)",
      standard: "UDIMA",
      question_es: "¿Por qué las alcachofas son consideradas un enemigo clásico del maridaje y qué vino recomienda la sumillería?",
      answer_es: "Contienen cinarina, un compuesto que inhibe temporalmente los receptores del dulzor. Al beber un líquido después, el agua sabe dulce y los vinos tintos tánicos se perciben fuertemente amargos y metálicos.",
      solution_es: "Se solventa con vinos que tengan amargores nobles (Verdejo sobre lías, Grüner Veltliner) o vinos de crianza biológica bajo velo de flor (Fino o Manzanilla de Sanlúcar).",
      tags: ["armonias", "quimica", "alcachofas"]
    },
    {
      id: "card_cms_grape_markers",
      category: "Cata Deductiva (CMS)",
      standard: "CMS",
      question_es: "¿Cuáles son los marcadores deductivos clave (Grape Markers) del Cabernet Sauvignon de clima moderado?",
      answer_es: "Cassis / grosella negra, ciruela negra, pimiento verde (pirazinas), grafito, cedro y hojas de tabaco. En boca: acidez media-alta, taninos firmes y cuerpo completo.",
      solution_es: "Si en la cata a ciegas identificas pirazina evidente (nota vegetal/pimiento) junto a cassis concentrado y tanino estructurado, la deducción lógica apunta a Cabernet Sauvignon (Burdeos Izquierda o clima moderado).",
      tags: ["deductive_tasting", "cms", "cabernet"]
    },
    {
      id: "card_wset_factors",
      category: "Factores Naturales (WSET 3)",
      standard: "WSET3",
      question_es: "Según el canon WSET 3, ¿cuáles son los 4 factores naturales fundamentales que definen el terruño?",
      answer_es: "1. El clima (temperatura, insolación, pluviometría, continentalidad/maritimidad).\n2. El suelo (retención hídrica, drenaje, nutrientes, reflexión solar de guijarros).\n3. La topografía (altitud, orientación de la ladera, pendiente).\n4. El factor biológico (microbiota del suelo y plagas/vectores).",
      solution_es: "WSET 3 enseña a vincular cada rasgo de la copa (ej. alta acidez por altitud o noches frías) directamente con un factor ambiental específico.",
      tags: ["wset3", "terroir", "clima"]
    },
    {
      id: "card_crianza_biologica",
      category: "Enología y Vinos Especiales (UDIMA)",
      standard: "UDIMA",
      question_es: "¿Qué condiciones bioquímicas caracterizan la Crianza Biológica en el marco de Jerez y Montilla?",
      answer_es: "Desarrollo del 'velo de flor' (levaduras del género Saccharomyces) en la superficie del vino en botas a 5/6 de capacidad. Consume alcohol, glicerol y oxígeno, aportando acetaldehído y notas punzantes de panadería, frutos secos y tiza.",
      solution_es: "El velo de flor protege al vino de la oxidación, manteniendo su color pálido y confiriéndole un perfil seco, punzante y salino único en el mundo.",
      tags: ["jerez", "enologia", "biologica"]
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
    }
  ];

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = STUDY_CARDS;
  } else {
    root.STUDY_CARDS = STUDY_CARDS;
  }
})(typeof window !== 'undefined' ? window : globalThis);
