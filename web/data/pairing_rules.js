// WINE³ai — Base de Conocimiento de Armonías y Reglas de Sumillería
// Fuentes analíticas: Court of Master Sommeliers (CMS Food & Wine Matching Standards),
// Association de la Sommellerie Internationale (ASI) y The Science of Wine (Jamie Goode)

(function(root) {
  'use strict';

  var PAIRING_RULES = {
    // 1. PRINCIPIOS FÍSICO-QUÍMICOS Y ESTRUCTURALES FUNDAMENTALES (CMS & ASI)
    principles: {
      weight: {
        id: "weight",
        name_es: "Peso y Estructura (Cuerpo)",
        name_en: "Weight and Body",
        law: "El peso del vino debe igualar el peso del plato: ligero con ligero, corpulento con corpulento.",
        mechanic: "Si el vino es más ligero que la comida, se vuelve invisible; si es excesivamente pesado, apaga los matices del plato. Excepción: vinos ligeros con altísima acidez e intensidad sápida.",
        rule: "match_weight"
      },
      acidity: {
        id: "acidity",
        name_es: "La Acidez como Limpiador y Realzador",
        name_en: "Acidity Dynamics",
        law: "La acidez del vino debe igualar o superar la del plato. La acidez corta la grasa y la salinidad.",
        mechanic: "Un vino con menor acidez que la comida parecerá plano y fofo (flabby). La acidez estimula la salivación, refresca el paladar saturado por lípidos (aceite, mantequilla, salsas) y realza el núcleo sápido del alimento.",
        rule: "wine_acid_gte_food_acid"
      },
      tannins: {
        id: "tannins",
        name_es: "Dinámica del Tanino: Proteína vs Grasa vs Pescado",
        name_en: "Tannin & Protein/Fat Reactions",
        law: "Los taninos aman las proteínas y grasas animales; odian los aceites de pescado y el picante.",
        mechanic: "Las proteínas de la carne y las grasas emulsionan los polifenoles, suavizando la astringencia tánica. En cambio, tanino + aceites de pescado/yodo = regusto metálico y amargo. Tanino + picante = amplificación del ardor cáustico.",
        rule: "tannin_needs_fat_protein_avoids_fish_oil"
      },
      sweetness: {
        id: "sweetness",
        name_es: "Azúcar Residual y Picante",
        name_en: "Sweetness and Capsaicin Extinguisher",
        law: "El azúcar del vino debe igualar o superar al del plato. El azúcar es el antídoto natural del picante.",
        mechanic: "Si un vino seco se sirve con un postre o plato dulce, el vino se percibirá excesivamente ácido, amargo y punzante. Los gramos de azúcar residual (off-dry, demi-sec, dulzura noble) amortiguan el fuego de la capsaicina y armonizan platos salados-dulces.",
        rule: "wine_sugar_gte_food_sugar"
      },
      alcohol: {
        id: "alcohol",
        name_es: "Nivel de Alcohol e Intensidad Térmica",
        name_en: "Alcohol and Heat Interaction",
        law: "Alcohol + picante o salinidad extrema = sensación de quemazón cáustica.",
        mechanic: "El etanol activa los termorreceptores VR1 de la boca. En platos muy especiados o picantes, se deben preferir graduaciones moderadas (< 13.5% vol.) y vinos con frescura frutal.",
        rule: "moderate_alcohol_with_spicy"
      },
      effervescence: {
        id: "effervescence",
        name_es: "Efervescencia y Burbuja",
        name_en: "Carbonation Palate Scrubbing",
        law: "El carbónico actúa como un cepillo mecánico que resetea las papilas ante grasas intensas y umami.",
        mechanic: "La textura de la burbuja rompe las películas grasas de embutidos, fritos y quesos curados, preparando la boca para el siguiente bocado.",
        rule: "carbonation_cleans_fat_and_umami"
      }
    },

    // 2. EL CATÁLOGO DE ALIMENTOS DIFÍCILES (CMS, ASI & The Science of Wine)
    difficultFoods: {
      artichoke_asparagus: {
        id: "artichoke_asparagus",
        name_es: "Alcachofas y Espárragos",
        compound: "Cinarina (éster que altera receptores gustativos)",
        problem: "Bloquea los receptores dulces momentáneamente; al ingerir líquido inmediatamente después, se percibe un dulzor fantasma y los vinos tintos tánicos se tornan fuertemente metálicos y amargos.",
        solution_es: "Vinos con notas amargas nobles y herbáceas (Verdejo de Rueda sobre lías, Grüner Veltliner, Gewürztraminer seco) o vinos de Crianza Biológica con velo de flor (Fino, Manzanilla, Vin Jaune).",
        recommended_styles: ["fino", "manzanilla", "verdejo_lees", "gruner_veltliner", "sauvignon_blanc"]
      },
      vinegar_pickles: {
        id: "vinegar_pickles",
        name_es: "Vinagretas, Escabeches y Encurtidos",
        compound: "Ácido acético concentrado",
        problem: "Descoloca por completo la percepción de acidez del vino, haciéndolo parecer desvertebrado, agrio y punzante.",
        solution_es: "Generosos andaluces (Manzanilla pasada, Fino en rama, Amontillado) cuya sapidez y salinidad aguantan el vinagre, o blancos septentrionales de hiper-acidez cortante (Riesling seco del Mosela/Rheingau).",
        recommended_styles: ["manzanilla", "fino", "amontillado", "riesling_dry"]
      },
      egg: {
        id: "egg",
        name_es: "Huevos y Yemas Untuosas",
        compound: "Lecitina, sulfuros y capa lipídica adhesiva",
        problem: "Cubre y anestesia las papilas gustativas; además, los compuestos sulfurados chocan de frente con el roble y el tanino.",
        solution_es: "Espumosos Método Tradicional (Cava Brut Nature, Champagne, Corpinnat) cuyo carbónico y lías levantan la untuosidad, o tintos muy fluidos de maceración carbónica sin barrica (Beaujolais, Rioja joven).",
        recommended_styles: ["cava_brut_nature", "champagne", "mencia_joven", "beaujolais"]
      },
      spicy_capsaicin: {
        id: "spicy_capsaicin",
        name_es: "Picante Intenso (Capsaicina y Alil-isotiocianato)",
        compound: "Capsaicina (guindillas/chiles) y Alil isotiocianato (wasabi/mostaza)",
        problem: "Se fija a los receptores del dolor térmico; los vinos con mucho alcohol (> 14%) o tanino provocan un ardor insoportable.",
        solution_es: "Blancos con azúcar residual refrescante (Riesling Kabinett/Spätlese, Gewürztraminer de Alsacia, Chenin Blanc demi-sec) o vinos generosos glicéricos con temperatura fresca.",
        recommended_styles: ["riesling_kabinett", "gewurztraminer_alsace", "chenin_blanc_demisec", "amontillado"]
      },
      blue_cheese: {
        id: "blue_cheese",
        name_es: "Quesos Azules (Cabrales, Roquefort, Gorgonzola)",
        compound: "Penicillium roqueforti, alta salinidad y fermentación lipídica",
        problem: "La alta salinidad y pungencia destruye los tintos secos, dejándolos amargos y metálicos.",
        solution_es: "Maridaje por contraste dulce-salado: vinos dulces nobles (Pedro Ximénez, Oporto Tawny/Vintage, Sauternes, Fondillón de Alicante) o vinos generosos de gran vejez (Oloroso viejo).",
        recommended_styles: ["pedro_ximenez", "porto_tawny", "sauternes", "oloroso_dulce"]
      },
      oily_fish: {
        id: "oily_fish",
        name_es: "Pescados Azules y Grasos (Sardina, Caballa, Atún)",
        compound: "Ácidos grasos Omega-3 e histamina",
        problem: "Al entrar en contacto con taninos de madera o uva, se produce una reacción química que deja sabor a herrumbre / lata de conservas.",
        solution_es: "Blancos con nervio salino y acidez cortante (Albariño, Txakoli, Chablis), rosados frescos o tintos casi etéreos servidos a 14°C (Mencía gallega, Pinot Noir frío).",
        recommended_styles: ["albarino", "txakoli", "chablis", "mencia_galicia", "pinot_noir"]
      }
    },

    // 3. MATRIZ DE MARIDAJE EN 3 PRESUPUESTOS (El Sommelier de Bolsillo)
    budgetTiers: {
      budget: {
        id: "tier_budget",
        tier: 1,
        name_es: "Acierto Seguro / Best Value",
        name_en: "Smart Choice / Great Value",
        priceRange: "14€ - 26€",
        philosophy_es: "Máxima relación calidad-precio. Vinos jóvenes o con crianza justa, gran fruta y autenticidad varietal sin pagar sobreprecio de etiqueta de renombre.",
        badgeColor: "emerald"
      },
      balanced: {
        id: "tier_balanced",
        tier: 2,
        name_es: "Armonía Canónica / Sweet Spot",
        name_en: "Harmonic Match / Sweet Spot",
        priceRange: "28€ - 55€",
        philosophy_es: "El maridaje de libro de sumillería. Denominaciones históricas, crianzas equilibradas en roble fino, lías trabajadas y tipicidad intachable de terruño.",
        badgeColor: "amber"
      },
      prestige: {
        id: "tier_prestige",
        tier: 3,
        name_es: "Homenaje de Sumiller / Gran Reserva",
        name_en: "Sommelier's Trophy / Prestige",
        priceRange: "> 60€",
        philosophy_es: "Una ocasión memorable. Vinos de parcela singular, productores de culto, añadas con gran evolución o joyas centenarias que elevan el plato a obra de arte.",
        badgeColor: "rose"
      }
    },

    // 4. BANCO DE PLATOS Y PERFILES GASTRONÓMICOS EMBLAMÁTICOS
    dishesDatabase: [
      {
        id: "lechazo_churro",
        name_es: "Lechazo Churro Asado en Horno de Leña",
        region: "Castilla y León (Ribera del Duero / Aranda)",
        tags: ["carne", "cordero", "grasa", "asado"],
        weight: "alto",
        fat: "alto",
        protein: "alto",
        acidity: "bajo",
        salinity: "medio",
        spiciness: "nulo",
        cooking: "asado tradicional",
        sommelier_note_es: "La grasa fundente del lechazo y el colágeno gelatinoso reclaman un tinto con taninos estructurados que se integren con la proteína y una acidez balsámica que limpie la boca.",
        pairings: {
          budget: {
            wine: "Tinto Fino Roble (Ribera del Duero)",
            region: "D.O. Ribera del Duero",
            grapes: ["Tempranillo"],
            price_est: "16€ - 22€",
            why: "Mucha fruta roja fresca, toque tostado ligero y acidez vivaz que aligera el primer bocado sin saturar la cartera."
          },
          balanced: {
            wine: "Ribera del Duero Crianza (36 meses entre barrica y botella)",
            region: "D.O. Ribera del Duero (Burgos / Valladolid)",
            grapes: ["Tinto Fino"],
            price_est: "32€ - 45€",
            why: "La madera noble pulida aporta notas de regaliz y cedro; los taninos ya redondeados funden la grasa del lechazo en perfecta simbiosis regional castellana ('lo que crece junto, va junto')."
          },
          prestige: {
            wine: "Gran Reserva de Viñas Viejas en Suelo Calizo o Vega Sicilia Valbuena",
            region: "D.O. Ribera del Duero / Vinos de Pago",
            grapes: ["Tinto Fino", "Cabernet Sauvignon"],
            price_est: "85€ - 160€",
            why: "Complejidad terciaria infinita (tabaco, cuero, sotobosque). La mineralidad calcárea y la finura sedosa convierten el asado tradicional en un festín palaciego."
          }
        }
      },
      {
        id: "cecina_leon",
        name_es: "Cecina de León I.G.P. con AOVE y Almendras",
        region: "León / Castilla y León",
        tags: ["embutido", "ahumado", "salado", "umami"],
        weight: "medio-alto",
        fat: "medio",
        protein: "alto",
        acidity: "bajo",
        salinity: "alto",
        spiciness: "nulo",
        cooking: "curado / ahumado",
        sommelier_note_es: "El humo de roble y la marcada salazón secan el paladar; los taninos maderosos chocarían. La solución clásica magistral es el vino de Jerez o un tinto atlántico de baja graduación.",
        pairings: {
          budget: {
            wine: "Manzanilla de Sanlúcar de Barrameda",
            region: "D.O. Manzanilla - Sanlúcar de Barrameda",
            grapes: ["Palomino Fino"],
            price_est: "14€ - 18€",
            why: "La salinidad marina y el velo de flor cortan la grasa del vacuno, potenciando el sabor ahumado sin añadir astringencia."
          },
          balanced: {
            wine: "Mencía del Bierzo con crianza sobre lías en foudre",
            region: "D.O. Bierzo",
            grapes: ["Mencía"],
            price_est: "28€ - 38€",
            why: "Maridaje geográfico leonés: fruta silvestre ácida, fondo de pizarra y tanino etéreo que refresca la curación de la cecina."
          },
          prestige: {
            wine: "Amontillado V.O.S. (más de 20 años de crianza)",
            region: "D.O. Jerez-Xérès-Sherry",
            grapes: ["Palomino Fino"],
            price_est: "65€ - 110€",
            why: "Notas de frutos secos tostados, maderas centenarias y acidez sápida eterna que se funden de manera apoteósica con el ahumado de la carne curada."
          }
        }
      },
      {
        id: "arroz_marisco",
        name_es: "Arroz Caldoso o Paella de Marisco y Bogavante",
        region: "Levante / Mediterráneo",
        tags: ["arroz", "marisco", "iodo", "umami", "azafran"],
        weight: "medio",
        fat: "medio",
        protein: "medio",
        acidity: "medio-bajo",
        salinity: "medio-alto",
        spiciness: "nulo",
        cooking: "fondo de pescado / sofrito",
        sommelier_note_es: "El fumet de marisco concentrado y el azafrán exigen volumen glicérico, buena acidez cítrica y absoluto respeto por el yodo (prohibido taninos rugosos).",
        pairings: {
          budget: {
            wine: "Verdejo sobre lías finas de Segovia",
            region: "D.O. Rueda",
            grapes: ["Verdejo"],
            price_est: "14€ - 20€",
            why: "Toques herbáceos de hinojo y volumen cremoso en boca que respetan el sofrito marino sin desbordar el presupuesto."
          },
          balanced: {
            wine: "Godello de Valdeorras / Bierzo fermentado en barrica o Cava Brut Nature Reserva",
            region: "D.O. Valdeorras / D.O. Cava",
            grapes: ["Godello", "Xarel·lo"],
            price_est: "30€ - 42€",
            why: "La mineralidad pedregosa del Godello o la burbuja fina del Cava cortan la riqueza del arroz y limpian el paladar tras cada cucharada de marisco."
          },
          prestige: {
            wine: "Champagne Blanc de Blancs Grand Cru o Gran Albariño de Finca de Guarda",
            region: "AOC Champagne (Côte des Blancs) / Rías Baixas",
            grapes: ["Chardonnay", "Albariño"],
            price_est: "80€ - 140€",
            why: "La acidez cortante y calcárea del Chardonnay o Albariño centenario aporta una tensión eléctrica que eleva el bogavante a su máxima expresión gastronómica."
          }
        }
      },
      {
        id: "presa_iberica",
        name_es: "Presa Ibérica a la Brasa con Salsa de Setas",
        region: "Extremadura / Huelva / Salamanca",
        tags: ["carne", "cerdo_iberico", "brasa", "setas", "umami"],
        weight: "alto",
        fat: "alto",
        protein: "alto",
        acidity: "bajo",
        salinity: "medio",
        spiciness: "nulo",
        cooking: "brasa de carbón",
        sommelier_note_es: "La grasa infiltrada del cerdo ibérico de bellota y los aromas terrosos de las setas armonizan de fábula con vinos que posean tanino maduro y matices balsámicos de bosque.",
        pairings: {
          budget: {
            wine: "Garnacha Tinta de Viñas Viejas (Calatayud o Campo de Borja)",
            region: "D.O. Calatayud",
            grapes: ["Garnacha"],
            price_est: "15€ - 22€",
            why: "Explosión de ciruela madura, pimienta negra y tanino goloso y redondo que envuelve la grasa ibérica."
          },
          balanced: {
            wine: "Rioja Reserva de corte clásico (Tempranillo, Graciano)",
            region: "D.O.Ca. Rioja",
            grapes: ["Tempranillo", "Graciano"],
            price_est: "30€ - 48€",
            why: "Notas de vainilla, trufa y cuero de la crianza en roble americano/francés que dialogan directamente con las setas silvestres."
          },
          prestige: {
            wine: "Priorat de Parcela (Vi de Paratge / Gran Vinya Classificada)",
            region: "D.O.Q. Priorat",
            grapes: ["Cariñena", "Garnacha"],
            price_est: "75€ - 130€",
            why: "La llicorella (pizarra pura) confiere un carácter mineral imponente que, junto al tanino potente y maduro, crea una experiencia inolvidable junto al carbón de la brasa."
          }
        }
      },
      {
        id: "ostras_mariscos_vivos",
        name_es: "Ostras Frescas / Percebes / Almejas de Carril",
        region: "Galicia / Bretaña",
        tags: ["marisco", "crudo", "salinidad", "iodo", "fresco"],
        weight: "ligero",
        fat: "muy bajo",
        protein: "medio",
        acidity: "alto",
        salinity: "muy alto",
        spiciness: "nulo",
        cooking: "crudo",
        sommelier_note_es: "El yodo vivo y la salmuera pura son despiadados con los taninos y el roble. Se requiere acidez cítrica pura, mineralidad salina y cero contacto con madera pesada.",
        pairings: {
          budget: {
            wine: "Txakoli de Getaria o Muscadet Sèvre et Maine sur lie",
            region: "D.O. Getariako Txakolina / AOC Muscadet",
            grapes: ["Hondarrabi Zuri", "Melon de Bourgogne"],
            price_est: "14€ - 19€",
            why: "Una punzada de acidez cítrica marina y aguja natural que funciona como un chorrito de limón sobre la ostra."
          },
          balanced: {
            wine: "Albariño de la Subzona O Rosal o Valle del Salnés (Rías Baixas)",
            region: "D.O. Rías Baixas",
            grapes: ["Albariño"],
            price_est: "26€ - 38€",
            why: "Manzana verde, recuerdos salinos del Atlántico y volumen en boca por crianza sobre lías sin barrica."
          },
          prestige: {
            wine: "Chablis Premier Cru / Grand Cru (Kimmeridgien calcáreo)",
            region: "AOC Chablis (Bourgogne)",
            grapes: ["Chardonnay"],
            price_est: "70€ - 125€",
            why: "El suelo de fósiles marinos prehistóricos de Chablis y su acidez austera crean el maridaje canónico por antonomasia de la alta sumillería internacional."
          }
        }
      },
      {
        id: "curry_thai_picante",
        name_es: "Curry Rojo Tailandés o Tacos de Birria Especiada",
        region: "Cocina Asiática / Mexicana",
        tags: ["picante", "especias", "capsaicina", "leche_coco"],
        weight: "medio-alto",
        fat: "medio",
        protein: "medio",
        acidity: "medio",
        salinity: "medio",
        spiciness: "alto",
        cooking: "guiso especiado / picante",
        sommelier_note_es: "La capsaicina adormece la lengua e inflama el etanol. Descartar tintos de 14.5% o con madera astringente. Necesitamos azúcar residual, frescura y acidez aromática.",
        pairings: {
          budget: {
            wine: "Vinho Verde Loureiro / Alvarinho",
            region: "DOC Vinho Verde (Portugal)",
            grapes: ["Loureiro", "Alvarinho"],
            price_est: "12€ - 17€",
            why: "Baja graduación (10.5%-11.5%), ligera aguja refrescante y acidez cítrica que apaga el calor inmediatamente."
          },
          balanced: {
            wine: "Riesling Kabinett Feinherb (semi-seco del Valle del Mosel)",
            region: "Qualitätswein Mosel (Alemania)",
            grapes: ["Riesling"],
            price_est: "28€ - 38€",
            why: "Los 20-30 g/l de azúcar residual neutralizan la capsaicina al instante, mientras la acidez láser despierta los aromas de jengibre y cilantro."
          },
          prestige: {
            wine: "Gewürztraminer Grand Cru Vendanges Tardives (Alsacia)",
            region: "AOC Alsace Grand Cru",
            grapes: ["Gewürztraminer"],
            price_est: "65€ - 95€",
            why: "Notas exóticas de lichi, pétalos de rosa y cardamomo con un cuerpo glicérico untuoso que transforma el plato picante en una fiesta sensual."
          }
        }
      }
    ]
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = PAIRING_RULES;
  } else {
    root.PAIRING_RULES = PAIRING_RULES;
  }
})(typeof window !== 'undefined' ? window : globalThis);
