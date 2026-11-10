// WINE³ai — Banco Canónico de Fichas de Examen & Cata Deductiva
// Estructurado estrictamente bajo los 3 grandes cánones internacionales:
// 1. WSET 3 (Wine & Spirit Education Trust)
// 2. CMS (Court of Master Sommeliers)
// 3. ASI (Association de la Sommellerie Internationale)
// Fuentes y Bibliografía: Jamie Goode (The Science of Wine), Pascaline Lepeltier (One Thousand Vines),
// Hugh Johnson & Jancis Robinson (The World Atlas of Wine, Wine Grapes), Julius Kühn-Institut (VIVC.de)

window.STUDY_CARDS = [
  // ==========================================
  // BLOQUE 1: WSET 3 (WINE & SPIRIT EDUCATION TRUST)
  // ==========================================
  {
    id: "card_wset_factors",
    standard: "WSET3",
    category: "Factores Naturales del Terruño (WSET 3)",
    question_es: "¿Cuáles son los 5 factores naturales fundamentales que definen el estilo, calidad y precio de un vino según el canon WSET Nivel 3?",
    answer_es: "1. Macroclima y latitud (insolación y temperatura estacional)\n2. Orografía y altitud (gradiente térmico vertical: -0.6°C cada 100m)\n3. Pendiente y orientación solar (aspecto: captación de radiación y drenaje de aire frío)\n4. Suelo y drenaje edáfico (retención hídrica, calor radiante y textura)\n5. Influencias hídricas o marítimas moderadoras (masas de agua, brisas marinas o nieblas matinales).",
    solution_es: "La interacción de estos factores determina la tasa de fotosíntesis, el ritmo de degradación del ácido málico y la síntesis de antocianos y polifenoles en el hollejo.",
    citation: "WSET Level 3 Specification & The World Atlas of Wine (Johnson & Robinson)"
  },
  {
    id: "card_ribera_vs_rioja",
    standard: "WSET3",
    category: "Terruño Comparado (WSET 3 / World Atlas of Wine)",
    question_es: "Compara el terruño de Ribera del Duero y Rioja Alta/Alavesa explicando cómo influyen la altitud y la oscilación térmica en la maduración del Tempranillo.",
    answer_es: "Ribera del Duero se sitúa entre 750 y 900+ m de altitud en la Meseta Norte, generando oscilaciones térmicas día/noche de hasta 20°C en agosto y septiembre. Esto preserva un ácido málico elevado y produce hollejos más gruesos con taninos y antocianos densos. Rioja Alta/Alavesa (400-600 m), protegida por la Sierra de Cantabria de vientos atlánticos, tiene un clima atlántico-mediterráneo más moderado, dando un Tempranillo con fruta roja más fresca, acidez lineal, menor graduación alcohólica potencial y taninos más sedosos.",
    solution_es: "En cata comparada WSET: Ribera = color rubí opaco, fruta negra madura, tanino alto y firme, 14.5-15% vol. Rioja Alta = fruta roja nítida, mayor frescura ácida, tanino medio (+), estructura más fluida.",
    citation: "The World Atlas of Wine (8th Ed.) & WSET 3 Study Guide"
  },
  {
    id: "card_suelos_llicorella",
    standard: "WSET3",
    category: "Geología & Edafología (WSET 3 / One Thousand Vines)",
    question_es: "¿Qué es el suelo de 'Llicorella' en la DOCa Priorat y cómo condiciona el comportamiento hídrico y el vigor de la vid?",
    answer_es: "La llicorella es una pizarra paleozoica del Carbonífero laminada y oscura, rica en mica y óxidos de hierro. Al fracturarse verticalmente, obliga a las raíces de Garnacha y Cariñena a profundizar hasta 10-15 metros en busca de humedad freática. Además, su color oscuro absorbe la radiación solar durante el día y la reirradia durante la noche, favoreciendo una maduración fenólica completa en rendimientos extremadamente bajos (<15-20 hl/ha).",
    solution_es: "Pascaline Lepeltier destaca que este confinamiento hídrico induce estrés hídrico moderado, limitando el tamaño de la baya y maximizando la concentración de taninos y extracto seco.",
    citation: "One Thousand Vines (Pascaline Lepeltier) & WSET 3"
  },
  {
    id: "card_crianza_biologica",
    standard: "WSET3",
    category: "Enología Especial (WSET 3)",
    question_es: "¿Cuáles son las condiciones fisicoquímicas necesarias para el desarrollo del velo de flor y qué transformaciones genera en el vino?",
    answer_es: "El velo de flor (levaduras del género Saccharomyces, principalmente beticus, cheresiensis, rouxii y montuliensis) requiere:\n- Graduación alcohólica estricta: entre 15.0% y 15.5% vol (por encima de 16% vol se inhibe).\n- Temperatura controlada: 15-20°C y humedad relativa alta (>70%).\n- Oxígeno: botas llenas a 5/6 (espacio de cabeza o 'dos puños').\n- Ausencia de SO2 libre elevado.\n\nTransformaciones moleculares:\n1. Metabolizan el oxígeno, evitando la oxidación y manteniendo el color pálido pajizo.\n2. Consumen glicerol (eliminando la sensación untuosa y dejando el vino ultra seco).\n3. Oxidan etanol a acetaldehído (notas punzantes de almendra cruda, masa de pan, manzana verde y tiza).\n4. Reducen la acidez volátil (ácido acético).",
    solution_es: "En cata SAT de WSET 3: Color limón pálido, aromas de intensidad pronunciada a levadura, masa madre, almendra verde; boca completamente seca, cuerpo ligero, acidez media, final largo y salino.",
    citation: "WSET Level 3 Wines Specification & The Science of Wine (Jamie Goode)"
  },
  {
    id: "card_crianza_oxidativa_jerez",
    standard: "WSET3",
    category: "Vinos Fortificados & Enología (WSET 3)",
    question_es: "¿Cómo se produce un Oloroso en el marco del sistema de Criaderas y Soleras y qué perfil organoléptico resulta?",
    answer_es: "El mosto base (generalmente de segunda prensa o con mayor estructura) se encabeza directamente a 17.0% vol con alcohol vínico, impidiendo la formación de velo de flor desde el inicio. El vino entra directamente en crianza oxidativa continua en botas de roble americano de 600 litros durante años o décadas. La evaporación lenta a través de la madera ('merma') concentra el alcohol (hasta 18-22% vol), la acidez y los extractos secos.",
    solution_es: "Descriptor SAT: Color ámbar a caoba oscuro; aromas pronunciados de nuez moscada, avellana tostada, higo seco, cuero, café y caramelo tostado; boca seca, con gran peso, acidez punzante y final eterno.",
    citation: "WSET Level 3 Wines Specification & Consejo Regulador Jerez-Xérès-Sherry"
  },
  {
    id: "card_maceracion_carbonica",
    standard: "WSET3",
    category: "Técnicas de Vinificación (WSET 3)",
    question_es: "¿Cuál es el mecanismo bioquímico de la maceración carbónica en racimo entero y qué perfil aromático distintivo genera?",
    answer_es: "Consiste en introducir racimos enteros sin estrujar en cubas selladas saturadas de dióxido de carbono (CO2). En ausencia de oxígeno, las células intactas de la uva inician una fermentación intracelular enzimática (anaeróbica):\n- El ácido málico se degrada enzimáticamente en un 30-50% (sin intervención de bacterias lácticas).\n- Se sintetizan hasta 1.5-2.0% vol de alcohol dentro de la uva sin levaduras.\n- Se sintetizan altas concentraciones de ésteres volátiles de fermentación: acetato de isoamilo y cinamato de etilo.\nCuando el alcohol intracelular rompe los hollejos, se prensa y las levaduras completan la fermentación del mosto.",
    solution_es: "Descriptores sensoriales WSET 3: Color rubí brillante con ribete violáceo, taninos extremadamente bajos y sedosos, y aromas hiperfrutales a plátano maduro, gominola de fresa, frambuesa confitada y chicle de canela.",
    citation: "WSET Level 3 Wines Specification & Jamie Goode (The Science of Wine)"
  },
  {
    id: "card_espumosos_autolisis",
    standard: "WSET3",
    category: "Espumosos & Método Tradicional (WSET 3)",
    question_es: "¿Qué es la autólisis de las levaduras en el método tradicional (Champagne / Cava) y a partir de qué mes de crianza en rima se hace sensorialmente perceptible?",
    answer_es: "Tras la segunda fermentación en botella ('toma de espuma'), las levaduras agotan los azúcares y mueren, depositándose como lías finas. A partir del 9º-12º mes, las enzimas celulares de la levadura degradan sus propias paredes de manoproteínas y liberan aminoácidos, lípidos y polipéptidos al vino.\nEste proceso aporta textura cremosa al paladar, estabilidad a la burbuja (espuma persistente de grano fino) y descriptores aromáticos terciarios de brioche, panadería recién horneada, galleta tostada y frutos secos.",
    solution_es: "WSET Nivel 3 exige identificar notas autolíticas (biscote, brioche) frente a aromas primarios frutales para evaluar la duración de la crianza sobre lías (mínimo 9 meses en Cava, 12 meses en Champagne, 36 meses en Gran Reserva).",
    citation: "WSET 3 Wines Handbook & The Science of Wine (Jamie Goode)"
  },
  {
    id: "card_wset_noble_rot_botrytis",
    standard: "WSET3",
    category: "Enología Especial & Botrytis (WSET 3)",
    question_es: "¿Qué condiciones meteorológicas exactas requiere la Podredumbre Noble (Botrytis cinerea) y qué impacto químico produce en vinos como Sauternes o Tokaji?",
    answer_es: "Requiere un ciclo diario bimórfico:\n1. Mañanas húmedas y brumosas (inducidas por la confluencia de ríos a distinta temperatura, como el Ciron y el Garona en Sauternes, o el Bodrog y el Tisza en Tokaj) que permiten al hongo perforar microscópicamente el hollejo.\n2. Tardes cálidas, soleadas y secas que impiden el paso a podredumbre gris (destructiva), evaporando el agua de la baya a través de las microperforaciones.\n\nImpacto químico:\n- Concentración brutal de azúcares (hasta 300-400 g/L) y acidez tartárica.\n- Aumento masivo de glicerol (sensación táctil untuosa y glicérica).\n- Generación de sotolón, fenilacetaldehído y lactonas que dan notas a miel, albaricoque desecado (orejones), mermelada de naranja amarga y jengibre.",
    solution_es: "SAT WSET 3: Color oro profundo o ámbar; acidez alta que compensa el dulzor elevado (evitando el empalago); final untuoso, largo y sumamente complejo.",
    citation: "WSET Level 3 Wines Specification & The World Atlas of Wine (Johnson & Robinson)"
  },

  // ==========================================
  // BLOQUE 2: CMS (COURT OF MASTER SOMMELIERS)
  // ==========================================
  {
    id: "card_cms_blind_deduction_steps",
    standard: "CMS",
    category: "Cata Deductiva & Metodología (CMS)",
    question_es: "¿Cuál es la secuencia formal de 4 pasos de la Deductive Tasting Grid de la Court of Master Sommeliers para deducir un vino a ciegas?",
    answer_es: "1. VISTA (Sight): Claridad, brillo, profundidad de color, color central vs color de menisco/ribete (rim variation), viscosidad/lágrimas (evaluación de graduación y residuo seco).\n2. NARIZ (Nose): Limpieza/condición, intensidad, perfil de fruta (roja, negra, azul, cítrica, de hueso; fresca, cocida, confitada), floral, vegetal/herbal, tierra/mineral, crianza en roble (francés vs americano, nuevo vs usado).\n3. BOCA (Palate): Dulzor, acidez, fenoles/taninos (intensidad y grano: tiza, polvo, terciopelo), alcohol, cuerpo, persistencia y confirmación del perfil retronasal.\n4. CONCLUSIÓN INICIAL & FINAL: Clima (frío/moderado/cálido), variedad o ensamblaje, Viejo Mundo vs Nuevo Mundo, país, apelación concreta y horquilla de añada (1-3 años).",
    solution_es: "En CMS, ningún vino se adivina: se deduce eliminando sistemáticamente hipótesis contradictorias mediante los marcadores sensoriales observados.",
    citation: "Court of Master Sommeliers Deductive Tasting Grid™"
  },
  {
    id: "card_cinarina",
    standard: "CMS",
    category: "Armonías & Bioquímica (CMS / Jamie Goode)",
    question_es: "¿Por qué las alcachofas son consideradas un alimento crítico para el maridaje y cuál es la solución técnica del sommelier?",
    answer_es: "Las alcachofas contienen cinarina (ácido 1,3-dicafeoilquínico). Este compuesto se une a los receptores del gusto dulce de las papilas gustativas sin activarlos inicialmente. Al tragar el vino o beber agua, la cinarina se lava rápidamente de los receptores, lo que provoca un rebote en el que los receptores se activan de golpe, haciendo que cualquier líquido posterior se perciba anormalmente empalagoso, dulce y metálico.",
    solution_es: "Solución técnica de sommelier: Vinos con nula presencia de azúcar residual y acidez punzante, preferiblemente con crianza biológica (Manzanilla de Sanlúcar o Fino de Jerez), donde el acetaldehído y la extrema salinidad contrarrestan la distorsión de la cinarina.",
    citation: "The Science of Wine (Jamie Goode) & CMS Food and Wine Matching Guidelines"
  },
  {
    id: "card_acid_salt",
    standard: "CMS",
    category: "Armonía Sensorial & Fisiología (CMS / ASI)",
    question_es: "¿Cómo interactúa la sal (NaCl) de un plato sobre la percepción de la acidez y el amargor del vino en el paladar?",
    answer_es: "El cloruro sódico (sal) bloquea y suprime los receptores de amargor y atenúa la percepción de acidez viva en la lengua. Al mismo tiempo, potencia la percepción de fruta, cuerpo y dulzor frutal del vino. Por tanto, un plato salado hace que un vino con acidez punzante (ej. Champagne brut nature o Sancerre) se perciba más suave, redondo y afrutado.",
    solution_es: "Regla CMS: La sal es el mejor amigo del sumiller para domar vinos con acidez muy elevada o con tanino ligeramente agresivo.",
    citation: "CMS Deductive Tasting & Food Pairing Guide"
  },
  {
    id: "card_cms_cabernet_sauvignon_pyrazines",
    standard: "CMS",
    category: "Marcadores de Uva & Enología (CMS / VIVC)",
    question_es: "¿Cuál es el marcador aromático químico por excelencia del Cabernet Sauvignon en climas frescos y cómo se diferencia de un defecto vegetal?",
    answer_es: "Las alquil-metoxipirazinas, principalmente la 3-isobutil-2-metoxipirazina (IBMP). Este compuesto se sintetiza en la baya antes del envero y se degrada progresivamente por exposición a la radiación solar y calor acumulado.\nEn climas frescos o añadas frías (Burdeos margen izquierda, Coonawarra, Valle del Maipo), un nivel sutil de 5-15 ng/L aporta el carácter varietal clásico a cassis, pimiento verde, hoja de grosellero negro y grafito. Si la uva no madura fenólica y termodinámicamente, supera los 30 ng/L, dominando con un aroma herbáceo verde, amargo y punzante que desequilibra el vino.",
    solution_es: "Descriptor CMS Deductive: Si en un tinto oscuro opaco con acidez alta y tanino alto y firme se detecta casis + pimiento verde + cedro/grafito ➔ Hipótesis inmediata: Cabernet Sauvignon de clima templado-fresco.",
    citation: "The Science of Wine (Jamie Goode) & VIVC Variety Catalogue (vivc.de: Cultivar 1929)"
  },
  {
    id: "card_nebbiolo_cms",
    standard: "CMS",
    category: "Cata Deductiva (CMS)",
    question_es: "En una cata a ciegas deductiva CMS, ¿cuáles son los 3 marcadores visuales y estructurales para no confundir Nebbiolo (Barolo/Barbaresco) con Pinot Noir?",
    answer_es: "1. VISTA: Ambos presentan capa baja-media translúcida, pero Nebbiolo muestra una evolución prematura hacia el color teja, anaranjado o granate incluso en añadas jóvenes (por déficit de antocianos trioxigenados estables).\n2. ESTRUCTURA EN BOCA: Pinot Noir tiene tanino medio a medio (+) sedoso y acidez media-alta. Nebbiolo posee un nivel masivo de tanino tánico y astringente (alto) combinado con una acidez tartárica punzante (alta) y alcohol elevado (14-15% vol).\n3. NARIZ: Mientras Pinot Noir se orienta a cereza roja, frambuesa, sotobosque húmedo y setas, Nebbiolo despliega 'alquitrán y rosas' (tar & roses), cuero curado, cereza agria, anís estrellado y trufa blanca.",
    solution_es: "En boca, el tanino 'grip' y masivo de Nebbiolo es la prueba inequívoca de descarte frente a Pinot Noir.",
    citation: "Court of Master Sommeliers Tasting Grid™"
  },
  {
    id: "card_syrah_rotundona",
    standard: "CMS",
    category: "Marcadores Químicos (CMS / Jamie Goode)",
    question_es: "¿Qué compuesto químico es responsable del aroma a pimienta negra en la Syrah/Shiraz y cómo varía según el clima?",
    answer_es: "El sesquiterpeno rotundona. Este compuesto aromático volátil tiene un umbral de detección humano excepcionalmente bajo (apenas 16 ng/L en vino tinto).\nSe acumula en el hollejo en concentraciones significativamente mayores en regiones frías o de maduración lenta (ej. Ródano Norte: Cornas, Côte-Rôtie; y climas marítimos fríos como Victoria / Grampians en Australia) que en regiones cálidas (Barossa Valley), donde se degrada por exceso de calor y da paso a notas de mermelada de mora y chocolate.",
    solution_es: "La presencia dominante de rotundona (pimienta negra recién molida) asociada a fruta negra ácida y violetas es el marcador cardinal de Syrah de clima templado/fresco en la cata deductiva CMS.",
    citation: "The Science of Wine (Jamie Goode) & Court of Master Sommeliers"
  },
  {
    id: "card_riesling_tdn",
    standard: "CMS",
    category: "Compuestos Volátiles (CMS / Jamie Goode)",
    question_es: "¿Qué es el compuesto TDN en la variedad Riesling y qué factores de viticultura promueven su aparición?",
    answer_es: "El TDN (1,1,6-trimetil-1,2-dihidronaftaleno) es un norisoprenoide derivado de la degradación carotenoides (luteína, betacaroteno) en el hollejo. Genera un aroma característico a hidrocarburo, queroseno, pedernal y cera de parafina.\nFactores que favorecen concentraciones elevadas de TDN:\n1. Elevada radiación solar ultravioleta directa sobre los racimos (deshojado temprano).\n2. Estrés hídrico moderado en verano.\n3. Suelos cálidos y pedregosos (esquistos de Mosela o granito de Alsacia).\n4. Años de envejecimiento en botella con bajo pH y alta acidez libre.",
    solution_es: "En cata CMS: La nota de petróleo/queroseno en un blanco con acidez vibrante, alcohol medio-bajo y ausencia de madera orienta inmediatamente la deducción hacia Riesling evolucionado.",
    citation: "The Science of Wine (Jamie Goode) & CMS Marker Guide"
  },
  {
    id: "card_pinot_noir_deductive",
    standard: "CMS",
    category: "Cata Deductiva Comparada (CMS)",
    question_es: "Compara el perfil deductivo CMS de un Pinot Noir de la Côte d'Or (Borgoña) frente a un Pinot Noir de Central Otago (Nueva Zelanda).",
    answer_es: "Borgoña (Viejo Mundo, clima continental fresco):\n- Vista: Capa rubí translúcida pálida.\n- Nariz: Dominio de tierra húmeda, hojarasca (forest floor), trufa, champiñón, arándano rojo fresco, cereza ácida y roble francés viejo integrado.\n- Boca: Acidez alta, tanino de grano fino medio, alcohol 13.0-13.5% vol, sensación etérea y mineral.\n\nCentral Otago (Nuevo Mundo, clima continental extremo del sur):\n- Vista: Capa rubí algo más densa y brillante con tintes violáceos.\n- Nariz: Fruta roja y negra explosiva (cereza negra madura, frambuesa silvestre), tomillo seco salvaje, violetas y roble nuevo especiado.\n- Boca: Acidez viva pero arropada por mayor cuerpo, taninos sedosos y maduros, alcohol 14.0-14.5% vol.",
    solution_es: "En la deducción CMS, la 'tierra vs fruta madura' define la pertenencia a Viejo o Nuevo Mundo.",
    citation: "Court of Master Sommeliers Blind Tasting Criteria"
  },

  // ==========================================
  // BLOQUE 3: ASI (ASSOCIATION DE LA SOMMELLERIE INTERNATIONALE)
  // ==========================================
  {
    id: "card_capsaicina",
    standard: "ASI",
    category: "Alimentos Críticos & Termorreceptores (ASI / Jamie Goode)",
    question_es: "¿Por qué el picante (capsaicina) no se debe maridar con tintos de alto tanino y alta graduación alcohólica según la normativa ASI?",
    answer_es: "La capsaicina no es un sabor, sino un compuesto químico que se une a los receptores de dolor y calor TRPV1 de la cavidad bucal. El alcohol etílico activa exactamente los mismos receptores TRPV1 reduciendo su umbral térmico (hace que ardan a temperatura corporal). Los taninos astringentes, al deshidratar la saliva y desnudar las mucosas, dejan los receptores desprotegidos. El resultado conjunto es una sensación de quemazón dolorosa e insoportable y una magnificación de la aspereza del vino.",
    solution_es: "Regla de Sumillería ASI: Platos picantes requieren vinos con baja graduación alcohólica (<11.5% vol), nula presencia tánica, elevada frescura y ligero azúcar residual (Off-dry Riesling alemán Kabinett o espumoso dulce tipo Moscato d'Asti), ya que el azúcar mitiga físicamente el estímulo TRPV1.",
    citation: "ASI Sommellerie Guidelines & Jamie Goode (The Science of Wine)"
  },
  {
    id: "card_jamon_iberico_oleico",
    standard: "ASI",
    category: "Armonías & Análisis Lipídico (ASI / Pascaline Lepeltier)",
    question_es: "¿Cuál es la explicación físico-química del maridaje canónico entre el Jamón Ibérico de Bellota y un vino de Crianza Biológica (Fino/Manzanilla)?",
    answer_es: "El jamón de bellota tiene un punto de fusión lipídico muy bajo (<28°C) gracias a su altísimo contenido en ácido oleico monoinsaturado (>55%), lo que tapiza las papilas gustativas de una película grasa untuosa persistente y rica en salazón. La Manzanilla y el Fino carecen completamente de glicerol (consumido por el velo de flor), poseen un pH muy bajo (alta acidez) y un contenido elevado en sales minerales y acetaldehídos punzantes.",
    solution_es: "La ausencia de glicerol y la riqueza salina actúan como un bisturí limpiador del paladar (efecto detergente no agresivo), disolviendo la capa de grasa tras cada bocado sin apagar los delicados aromas de bellota y curación.",
    citation: "One Thousand Vines (Pascaline Lepeltier) & ASI Harmony Protocols"
  },
  {
    id: "card_tca_umbral",
    standard: "ASI",
    category: "Defectos del Vino & Protocolo de Sala (ASI / Jamie Goode)",
    question_es: "¿Cuál es el compuesto químico responsable del olor a corcho ('cork taint'), su umbral de percepción humana y su impacto en sala?",
    answer_es: "El 2,4,6-Tricloroanisol (TCA), producido por hongos microscópicos (Penicillium, Trichoderma) en presencia de clorofenoles durante el tratamiento o almacenamiento del corcho o la bodega.\n- Umbral sensorial: Extraordinariamente bajo, perceptible por el ser humano a partir de 2 a 4 nanogramos por litro (partes por trillón, ng/L).\n- Efecto en copa: Incluso a concentraciones sub-umbral (1-2 ng/L) donde no huele a cartón mojado o humedad de sótano, el TCA actúa anestesiando los receptores olfativos, 'matando' y aplanando completamente la fruta, el frescor y la tipicidad del vino.",
    solution_es: "Protocolo ASI de Sala: La comprobación visual y olfativa de la botella por el sumiller antes de servir a la mesa del comensal tiene como objetivo primario detectar este defecto antes del servicio.",
    citation: "The Science of Wine (Jamie Goode) & ASI Technical Guidelines"
  },
  {
    id: "card_decantacion_vs_jarreo",
    standard: "ASI",
    category: "Servicio & Sala (Norma ASI)",
    question_es: "¿En qué se diferencia técnicamente la decantación con vela de la aireación/oxigenación (jarreo) y cuándo está contraindicada cada una?",
    answer_es: "1. Decantación con vela (Vinos viejos/maduros): Procedimiento delicado donde se trasiega el vino lentamente frente a un foco de luz (vela) para detener el flujo en el hombro de la botella en cuanto asomen los sedimentos o posos (precipitado de taninos polimerizados y antocianos). Contraindicación: Airear agresivamente un vino muy anciano puede oxidarlo y colapsar sus frágiles aromas terciarios en cuestión de 15 minutos.\n2. Jarreo / Oxigenación (Vinos jóvenes y vigorosos): Caída libre de vino en el decantador de base ancha para forzar contacto masivo con oxígeno atmosférico y volatilizar mercaptanos reductivos o suavizar taninos cerrados. Contraindicación: Nunca aplicar a añadas históricas con poso.",
    solution_es: "Regla ASI de Concurso: Presentar la botella al cliente, cortar la cápsula bajo el gollete inferior, descorchar sin ruido, limpiar la boca de la botella, encender la vela y trasvasar en un solo movimiento continuo sin interrupciones.",
    citation: "ASI Sommelier Competition Standards & Service Manual"
  },
  {
    id: "card_asi_serving_temperatures",
    standard: "ASI",
    category: "Temperaturas de Servicio Canónicas (Norma ASI)",
    question_es: "¿Cuáles son las temperaturas canónicas de servicio de vino fijadas por la ASI y por qué el término 'temperatura ambiente' es un anacronismo peligroso?",
    answer_es: "Cánones universales ASI:\n- Espumosos (Champagne, Cava): 6°C a 8°C (conserva la presión de CO2 y la tensión de burbuja).\n- Blancos jóvenes ligeros y secos: 7°C a 10°C.\n- Blancos estructurados con madera / Orange Wines: 10°C a 12°C.\n- Rosados: 8°C a 10°C.\n- Tintos ligeros (Pinot Noir, Mencía, Gamay): 12°C a 14°C.\n- Tintos de cuerpo y tanino (Ribera, Burdeos, Barolo): 16°C a 18°C (nunca más de 18°C).\n- Generosos dulces y fortificados: 12°C a 15°C (Finos/Manzanillas: 6-8°C).",
    solution_es: "El error de la 'temperatura ambiente': Proviene de los castillos y comedores señoriales del siglo XIX europeo (16-17°C). En salas y hogares contemporáneos a 22-24°C, el vino a 'temperatura ambiente' produce volatilidad agresiva del etanol, sensación de ardor alcohólico, flacidez estructural y pérdida total de frescura frutal.",
    citation: "ASI Guidelines for Sommelier Competitions & Pascaline Lepeltier"
  },
  {
    id: "card_asi_glassware_geometry",
    standard: "ASI",
    category: "Cristalería & Dinámica de Fluidos (ASI / Jamie Goode)",
    question_es: "¿Cómo afecta la geometría de la copa (volumen del cáliz, diámetro de apertura y chimenea) a la percepción sensorial del vino?",
    answer_es: "La copa no cambia la composición química del vino, pero gobierna la tasa de evaporación y concentración de compuestos volátiles:\n1. Volumen del cáliz (Headspace): Un cáliz amplio (estilo Burdeos o Borgoña) ofrece una mayor superficie de contacto líquido-aire, acelerando la liberación de aromas complejos y facilitando el arremolinado sin salpicaduras.\n2. Diámetro del borde (Chimenea): Una boca más estrecha actúa como embudo térmico concentrando los aromas volátiles más densos en la fosa nasal. Copas demasiado anchas dispersan los ésteres delicados.\n3. Ángulo de inclinación del sorbo: El diámetro y curvatura del borde obligan al degustador a inclinar la cabeza de manera distinta, depositando el primer impacto del flujo en diferentes áreas iniciales de la cavidad oral.",
    solution_es: "Norma ASI de Cristalería: Cristal fino (sin reborde grueso o 'roll'), cáliz en forma de tulipán cónico, fuste o tallo largo para sujetar la copa sin transmitir calor corporal al vino, y base perfectamente nivelada.",
    citation: "The Science of Wine (Jamie Goode) & ASI Standards"
  },
  {
    id: "card_asi_cheese_pairing_lipids",
    standard: "ASI",
    category: "Armonía Molecular con Quesos (ASI / Pascaline Lepeltier)",
    question_es: "¿Por qué el maridaje tradicional de quesos azules (Roquefort, Cabrales, Stilton) con tintos jóvenes potentes es un error sensorial y qué propone la sumillería contemporánea?",
    answer_es: "Los quesos azules presentan un alto contenido de sal (NaCl), grasas lácteas densas y compuestos aromáticos agresivos generados por Penicillium roqueforti (ácidos grasos libres de cadena corta como ácido butírico, caproico e isovalérico). Al combinarse con un tinto tánico con alta graduación:\n- Los taninos reaccionan con las proteínas y grasas del queso generando un regusto intensamente amargo y metálico.\n- La sal del queso resalta la astringencia y la dureza del tanino del tinto.",
    solution_es: "La solución científica ASI: Contraste osmótico y complementariedad. Vinos dulces nobles con alta acidez (Sauternes botritizado con Roquefort, Oporto Vintage con Stilton, o Fondillón con quesos curados). El azúcar residual equilibra la sal, la alta acidez corta la grasa láctea y la riqueza de ambos crea una tercera dimensión gustativa armoniosa.",
    citation: "One Thousand Vines (Pascaline Lepeltier) & ASI Food & Wine Standards"
  },
  {
    id: "card_asi_sommelier_service_ritual",
    standard: "ASI",
    category: "Protocolo & Ritual de Sala (Norma ASI)",
    question_es: "¿Cuál es el protocolo canónico de apertura y servicio de una botella de vino tranquilo en mesa según las normas de concurso ASI?",
    answer_es: "1. PRESENTACIÓN: Mostrar la botella al comensal anfitrión anunciando productor, apelación, variedad y añada, manteniendo la etiqueta visible.\n2. CORTE DE CÁPSULA: Cortar limpiamente la cápsula de estaño por debajo del gollete inferior (anillo inferior) para evitar que el vino toque restos de metal al verter. Retirar la cápsula con el lito y depositarla discretamente.\n3. LIMPIEZA INICIAL: Limpiar la boca exterior del gollete con el lito de tela antes de insertar la espiral.\n4. DESCORCHE: Introducir el sacacorchos en el centro del corcho, extraerlo verticalmente en dos tiempos sin perforar la base del tapón y silenciando el 'pop' final.\n5. EXAMEN DEL CORCHO: Inspeccionar visual y olfativamente el corcho, depositándolo en un platillo a la derecha del anfitrión.\n6. LIMPIEZA FINAL Y SERVICIO: Limpiar el interior de la boca de la botella, verter una dosis de cata (30-50 ml) al anfitrión por su derecha. Una vez aprobado, servir al resto de comensales siguiendo precedencias (mujeres o invitados primero, anfitrión en último lugar), finalizando cada vertido con un ligero giro de muñeca sin gotear.",
    solution_es: "La etiqueta de la botella debe permanecer orientada hacia el cliente en todo momento durante el servicio en sala.",
    citation: "ASI Guidelines for Best Sommelier of the World Competition"
  }
];
