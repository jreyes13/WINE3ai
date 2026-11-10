// WINE³ai — WINEp3dIA: Base de Datos Enciclopédica y Artículos de Referencia
// Fuentes analíticas: WSET Nivel 3, Court of Master Sommeliers (CMS), Máster UDIMA y ASI

(function(root) {
  'use strict';

  var WINEPEDIA_ARTICLES = [
    // --- 1. ENOLOGÍA Y BIOQUÍMICA (UDIMA) ---
    {
      id: "velo_de_flor",
      title_es: "Crianza Biológica y Velo de Flor",
      title_en: "Biological Aging and 'Velo de Flor'",
      standard: "UDIMA",
      category_es: "Enología & Vinos Especiales",
      category_en: "Enology & Special Vinifications",
      badge_color: "amber",
      summary_es: "Formación espontánea de colonias de levaduras Saccharomyces en la superficie del vino en botas de roble a 5/6 de capacidad, protegiéndolo de la oxidación y transformando su perfil sensorial.",
      summary_en: "Spontaneous yeast veil (Saccharomyces) forming atop wine in oak butts filled to 5/6 capacity, preventing oxidation and drastically altering the flavor matrix.",
      content_es: "La crianza biológica es el pilar de los Finos y Manzanillas en el Marco de Jerez y Montilla-Moriles. Requiere una graduación alcohólica precisa de entre 15% y 15.5% vol. (un grado mayor mataría las levaduras; un grado menor permitiría el desarrollo de bacterias acéticas), temperatura moderada (18°-22°C) y humedad relativa alta. El velo consume alcohol, glicerol (eliminando la sensación untuosa y volviéndolo ultra-seco) y oxígeno disuelto, mientras genera acetaldehído. Este proceso confiere al vino notas punzantes de tiza, panadería, masa madre, almendra amarga y recuerdos salinos característicos.",
      content_en: "Biological aging is the benchmark process behind Fino and Manzanilla in Jerez and Montilla-Moriles. It demands a strictly controlled ABV between 15% and 15.5% (higher kills the flor; lower permits bacterial spoilage), 18°-22°C temperature, and high humidity. The yeast consumes oxygen, alcohol, and glycerol—yielding an intensely bone-dry mouthfeel—while releasing acetaldehydes that impart savory notes of baker's dough, almond, and chalky salinity.",
      key_takeaways_es: [
        "Protección 100% anaeróbica: el velo impide el contacto del vino con el aire.",
        "Consumo total de glicerol: provoca una sequedad absoluta en boca sin rastro de dulzor.",
        "Generación de acetaldehído: responsable de los aromas de almendra y panadería."
      ],
      key_takeaways_en: [
        "Complete anaerobic barrier against oxygen oxidation.",
        "Full consumption of glycerol yielding bone-dry texture.",
        "Acetaldehyde production creating signature chalky almond aromas."
      ],
      related_grapes: ["Palomino Fino", "Pedro Ximénez"],
      related_regions: ["Jerez-Xérès-Sherry", "Manzanilla de Sanlúcar", "Montilla-Moriles", "Jura (Vin Jaune)"],
      tags: ["jerez", "enologia", "flor", "biologica", "palomino"]
    },
    {
      id: "fermentacion_malolactica",
      title_es: "Fermentación Maloláctica (FML)",
      title_en: "Malolactic Fermentation (MLF)",
      standard: "UDIMA",
      category_es: "Bioquímica Enológica",
      category_en: "Enological Biochemistry",
      badge_color: "amber",
      summary_es: "Conversión microbiológica catalizada por bacterias lácticas (Oenococcus oeni) que descarboxila el ácido málico en ácido láctico, suavizando la acidez del vino.",
      summary_en: "Bacterial conversion by Oenococcus oeni decarboxylating sharp malic acid into smooth lactic acid and releasing buttery diacetyl.",
      content_es: "La FML no es una fermentación en sentido estricto, sino una descarboxilación bacteriana enzimática secundaria. El ácido málico (mismo ácido punzante de las manzanas verdes) pierde una molécula de CO2 y se transforma en ácido láctico (ácido suave presente en la leche fermentada). Este proceso reduce la acidez total, eleva ligeramente el pH (0.1 - 0.3 puntos), confiere estabilidad microbiológica y aporta untuosidad. En vinos tintos es prácticamente obligatoria para redondear taninos. En blancos (como en Borgoña / Chardonnay de guarda) aporta notas de mantequilla fresca y nata mediante la síntesis del compuesto diacetilo.",
      content_en: "MLF is an enzymatic bacterial transformation wherein dicarboxylic malic acid (green apple tartness) is converted into monocarboxylic lactic acid (dairy smoothness), releasing CO2. This reduces total titratable acidity, slightly increases pH, and stabilizes the wine. Virtually all premium reds undergo MLF. In whites (notably cool-climate Chardonnays), it imparts creamy texture and buttery nuances via diacetyl.",
      key_takeaways_es: [
        "Transforma la acidez cortante y angular en una sensación redonda y láctea.",
        "Síntesis de diacetilo: responsable aromático de notas de mantequilla, brioche y nata.",
        "Casi universal en tintos; selectiva en blancos de guarda con madera."
      ],
      key_takeaways_en: [
        "Softens harsh tart acidity into round lactic creaminess.",
        "Synthesizes diacetyl, imparting butter and brioche notes.",
        "Standard in red winemaking; stylistic choice in rich white wines."
      ],
      related_grapes: ["Chardonnay", "Tempranillo", "Cabernet Sauvignon", "Pinot Noir"],
      related_regions: ["Bourgogne", "Rioja", "Ribera del Duero", "Bordeaux"],
      tags: ["enologia", "bioquimica", "fml", "malico", "lactico", "diacetilo"]
    },
    {
      id: "antagonismo_cinarina",
      title_es: "Cinarina y Alimentos Antagónicos del Vino",
      title_en: "Cynarine and Wine-Antagonistic Foods",
      standard: "UDIMA",
      category_es: "Armonías & Análisis Sensorial",
      category_en: "Pairing & Sensory Analysis",
      badge_color: "amber",
      summary_es: "Estudio molecular de compuestos presentes en alcachofas y espárragos que bloquean receptores gustativos, generando falsos dulzores y notas metálicas en tintos tánicos.",
      summary_en: "Molecular study of cynarine in artichokes and asparagus temporarily inhibiting sweet tastebuds, turning red wines unpleasantly bitter and metallic.",
      content_es: "En los apuntes de cata y sumillería de UDIMA (Prof. Diego González Barbolla), se analiza cómo la cinarina (ácido 1,3-dicafeoilquínico) es un éster natural que adormece temporalmente los receptores gustativos del dulzor en las papilas de la lengua. Al dar un sorbo de agua o vino inmediatamente después, los receptores se reactivan de golpe, transmitiendo una ilusión de dulzor anómala que descoordina la percepción sensorial. Con vinos tintos de alta carga tánica o madera, la reacción produce un regusto fuertemente astringente y metálico (similar a chupar una moneda de cobre). La solución técnica es maridarlos con variedades de amargor noble (Verdejo de lías) o vinos de crianza biológica (Fino/Manzanilla) donde el acetaldehído y la salinidad neutralizan la cinarina.",
      content_en: "Artichokes and green asparagus contain cynarine, an organic compound that temporarily paralyses sweet taste receptors. Once rinsed with wine or water, tastebuds overcompensate, creating perceived sweetness while tannins trigger aggressive metallic aftertastes. Master sommeliers resolve this via bitter-edged whites (Verdejo, Grüner Veltliner) or biological flor aging (Fino/Manzanilla), whose acetaldehydes cut through cynarine.",
      key_takeaways_es: [
        "Inhibe receptores del dulzor provocando disonancia organoléptica.",
        "Provoca reacción metálica desagradable con taninos y crianza en roble.",
        "Maridaje de resolución: Crianza biológica bajo velo de flor o blancos sobre lías."
      ],
      key_takeaways_en: [
        "Paralyzes sweetness receptors causing deceptive aftertaste.",
        "Causes metallic and harsh bitter clash with red tannins.",
        "Master pairing remedy: Biological flor wines or lees-aged whites."
      ],
      related_grapes: ["Verdejo", "Grüner Veltliner", "Palomino Fino", "Sauvignon Blanc"],
      related_regions: ["Rueda", "Jerez", "Sanlúcar", "Wachau"],
      tags: ["armonias", "cinarina", "alcachofa", "quimica", "sumilleria"]
    },
    {
      id: "defectos_vino_tca_reduccion",
      title_es: "Defectos del Vino: TCA, Reducción y Brettanomyces",
      title_en: "Wine Faults: TCA, Reduction & Brettanomyces",
      standard: "UDIMA",
      category_es: "Control de Calidad & Enología",
      category_en: "Quality Control & Enology",
      badge_color: "amber",
      summary_es: "Diagnóstico organoléptico de las tres grandes alteraciones que inutilizan o desvían el perfil limpio de un vino: olor a corcho, sulfhídrico y levaduras contaminantes.",
      summary_en: "Sensory diagnostic of the primary wine faults: 2,4,6-trichloroanisole (cork taint), volatile sulfur reduction, and Brettanomyces 4-ethylphenol contamination.",
      content_es: "1. **TCA (2,4,6-Tricloroanisol):** Provocado por hongos microscópicos que entran en contacto con compuestos clorados usados históricamente en la limpieza de corchos. Olor inconfundible a cartón mojado, sótano húmedo o perro mojado; anula por completo la fruta del vino. Umbral de detección humano de apenas 1 a 4 partes por billón (ng/L).\n2. **Reducción:** Falta de oxígeno disuelto durante la fermentación o crianza en botella. Genera sulfuro de hidrógeno (H2S) y mercaptanos (huevo podrido, cerilla quemada, col cocida, caucho). Puede mitigarse en copas aireando enérgicamente o con contacto con cobre si es leve.\n3. **Brettanomyces bruxellensis:** Levadura contaminante que metaboliza ácidos hidroxicinámicos produciendo 4-etilfenol y 4-etilguayacol. Recuerdos de establo, cuadra, sudor de caballo, cuero rancio y tiritas medicinales.",
      content_en: "1. **TCA (Cork Taint):** Fungal interaction with chlorophenols creating 2,4,6-trichloroanisole. Smells of wet cardboard and moldy basements; mutes fruit even at threshold levels of 1-4 ng/L.\n2. **Reduction:** Oxygen starvation yielding volatile sulfur compounds (H2S, mercaptans) showing rotten eggs, burnt matches, and boiled cabbage.\n3. **Brettanomyces:** Spoilage yeast producing 4-ethylphenol, creating barnyard, sweaty horse blanket, and medicinal band-aid aromas.",
      key_takeaways_es: [
        "TCA anula irreversiblemente la expresión frutal de la copa.",
        "La reducción leve puede disiparse con oxigenación o decantación.",
        "Brettanomyces genera aromas de cuero viejo, sudor animal y establo."
      ],
      key_takeaways_en: [
        "TCA irreversibly obliterates varietal fruit expression.",
        "Mild reduction can occasionally blow off with decanting.",
        "Brett creates distinct barnyard and band-aid volatile markers."
      ],
      related_grapes: ["Cualquier variedad"],
      related_regions: ["Global"],
      tags: ["defectos", "tca", "corcho", "reduccion", "brett", "enologia"]
    },

    // --- 2. CATA DEDUCTIVA Y MARCADO DE VARIEDADES (CMS) ---
    {
      id: "cms_deductive_grid",
      title_es: "La Cuadrícula Deductiva de Cata a Ciegas (CMS)",
      title_en: "The CMS Deductive Blind Tasting Grid",
      standard: "CMS",
      category_es: "Cata Deductiva & Metodología",
      category_en: "Deductive Tasting & Methodology",
      badge_color: "rose",
      summary_es: "El método de lógica formal estricta del Court of Master Sommeliers para deducir variedad, procedencia de terruño, clima y añada a partir de evidencias sensoriales objetivas.",
      summary_en: "The formal logic grid of the Court of Master Sommeliers linking sensory evidence in glass directly to grape variety, climate, terroir origin, and vintage.",
      content_es: "La metodología deductiva de CMS se estructura en 4 fases secuenciales sin saltos:\n\n1. **Sight (Vista):** Claridad, brillo, profundidad de color (pálido, medio, profundo), matiz (rojo rubí, granate, teja, púrpura; limón, oro, ámbar) y el menisco. Densidad de lágrimas (viscosidad ligada a alcohol y azúcar residual).\n2. **Nose (Nariz):** Condición (limpio/defectuoso), intensidad, carácter de la fruta (fresca, madura, compotada, desecada), notas florales, vegetales/pirazinas, terrosas/minerales (piedra caliza, grafito, pizarra) y roble (francés vs americano, tostado, vainilla, humo).\n3. **Palate (Boca):** Nivel de sequedad/dulzor, nivel exacto de acidez (baja, media-, media, media+, alta), grano y textura del tanino, graduación alcohólica percibida, cuerpo y longitud del final (finish).\n4. **Conclusion (Deducción Final):** Síntesis lógica. Si hay acidez alta, fruta roja crujiente, color rubí traslúcido y sotobosque ➔ Clima frío del Viejo Mundo ➔ Pinot Noir de Borgoña.",
      content_en: "The Court of Master Sommeliers deductive grid operates through strict sensory logic:\n\n1. **Sight:** Clarity, color core vs rim variation, staining of tears, viscosity.\n2. **Nose:** Fruit condition (tart, ripe, stewed), earth/mineral (crushed rock, limestone, clay), wood (French vs American, toast level, spices).\n3. **Palate:** Sugar, precise acidity scale, tannin quality and grip, alcohol warmth, body, and persistent finish.\n4. **Conclusion:** Initial conclusion (Old vs New World, cool vs warm climate) leads inevitably to final deduction (grape, country, region, vintage bracket).",
      key_takeaways_es: [
        "No se adivina: cada conclusión debe apoyarse en evidencias descritas previamente en boca y nariz.",
        "Distingue el Viejo Mundo (fruta contenida, mineralidad, tierra) del Nuevo Mundo (fruta exuberante, alcohol generoso).",
        "El menisco y los tonos teja delatan la curva de envejecimiento."
      ],
      key_takeaways_en: [
        "Never guess: deductions must stem strictly from documented sensory facts.",
        "Clear distinction: Old World (earth/mineral focus) vs New World (fruit/alcohol dominance).",
        "Rim variation objectively reveals the oxidation curve and aging age."
      ],
      related_grapes: ["Todas las variedades nobles"],
      related_regions: ["Bordeaux", "Bourgogne", "Napa Valley", "Piedmont", "Rioja"],
      tags: ["cms", "cata_a_ciegas", "deductive_grid", "metodologia", "sumiller"]
    },
    {
      id: "grape_markers_pirazinas_terpenos",
      title_es: "Marcadores de Uva: Pirazinas, Terpenos y Rotundona",
      title_en: "Grape Markers: Pyrazines, Terpenes & Rotundone",
      standard: "CMS",
      category_es: "Marcadores Químicos & Aromas",
      category_en: "Chemical Markers & Varietal Aromas",
      badge_color: "rose",
      summary_es: "Moléculas aromáticas congénitas de variedades específicas que actúan como huellas dactilares irrefutables en el examen de cata a ciegas.",
      summary_en: "Congenital varietal aroma compounds that serve as unambiguous chemical fingerprints in blind sommelier examinations.",
      content_es: "El Court of Master Sommeliers cataloga 'Grape Markers' clave:\n\n1. **Metoxipirazinas (IBMP):** Aportan notas inconfundibles de pimiento verde, hoja de tomatera, espárrago fresco y grosella negra silvestre. Típicas de la familia bordelesa: Cabernet Sauvignon, Cabernet Franc, Carmenère y Sauvignon Blanc en climas moderados/frescos.\n2. **Rotundona:** Sesquiterpeno responsable directo del aroma a pimienta negra recién molida y grano de pimienta blanca. Huella dactilar de la Syrah/Shiraz y de la variedad austríaca Grüner Veltliner.\n3. **Monoterpenos (Linalool, Geraniol):** Compuestos florales intensos de jazmín, azahar, uva fresca y lavanda. Identificadores de Moscatel, Torrontés, Gewürztraminer y Malvasía.\n4. **TDN (1,1,6-trimetil-1,2-dihidronaftaleno):** Proporciona la nota mineral punzante de queroseno, petróleo e hidrocarburo en Riesling evolucionado.",
      content_en: "The CMS identifies key chemical 'Grape Markers':\n\n1. **Methoxypyrazines:** Green bell pepper, tomato leaf, and cassis bud characteristic of the Cabernet family and Sauvignon Blanc.\n2. **Rotundone:** Freshly cracked black peppercorn aroma defining Syrah/Shiraz and Grüner Veltliner.\n3. **Terpenes:** High floral perfume (linalool, geraniol) distinguishing Muscat, Torrontés, and Gewürztraminer.\n4. **TDN:** Hydrocarbon/petrol nuance signature of aged Rieslings grown on slate and hot sun exposure.",
      key_takeaways_es: [
        "Pirazinas = Familia Cabernet y Sauvignon Blanc en zonas de maduración moderada.",
        "Rotundona = Pimienta negra indiscutible de la Syrah del Ródano y Grüner Veltliner.",
        "TDN = Hidrocarburo noble característico del Riesling de guarda."
      ],
      key_takeaways_en: [
        "Pyrazines define cool/moderate Cabernet and Sauvignon Blanc.",
        "Rotundone explains the distinct cracked pepper note of Syrah.",
        "TDN produces the petrol hallmark of mature Riesling."
      ],
      related_grapes: ["Cabernet Sauvignon", "Sauvignon Blanc", "Syrah", "Grüner Veltliner", "Riesling"],
      related_regions: ["Bordeaux", "Loire", "Rhône Valley", "Wachau", "Mosel"],
      tags: ["cms", "pirazinas", "terpenos", "rotundona", "grape_markers", "tdn"]
    },

    // --- 3. TERRUÑO Y FACTORES NATURALES (WSET 3) ---
    {
      id: "wset_factores_naturales",
      title_es: "Los 4 Factores Naturales del Terruño (WSET 3)",
      title_en: "The 4 Natural Terroir Factors (WSET 3)",
      standard: "WSET3",
      category_es: "Terruño & Factores Ambientales",
      category_en: "Terroir & Environmental Factors",
      badge_color: "purple",
      summary_es: "El marco conceptual del WSET para vincular objetivamente el clima, suelo, orografía y masa vegetal con el estilo, precio y calidad final del vino.",
      summary_en: "The WSET Level 3 framework methodically connecting macroclimate, soil physics, aspect/slope, and biology directly to wine style and price tier.",
      content_es: "WSET Nivel 3 enseña a analizar cada viñedo a través de una lente causal estricta:\n\n1. **Clima:** Temperatura media, grado de insolación, pluviometría estacional y el índice de continentalidad (diferencia de temperatura entre el verano y el invierno) o amplitud térmica día-noche. Las noches frías preservan la acidez málica y los aromas frescos; los días cálidos maduran taninos y azúcares.\n2. **Suelo:** Física del suelo (retención hídrica vs drenaje). Suelos arcillosos retienen agua y mantienen temperaturas frías; suelos pedregosos (galets, pizarras) drenan y reflejan el calor nocturno hacia los racimos.\n3. **Topografía & Aspecto:** Orientación hacia el sol (laderas expuestas al sur en el hemisferio norte) y altitud (por cada 100 m de elevación, la temperatura media desciende ~0.6°C, extendiendo el ciclo vegetativo).\n4. **Factor Biológico:** Presión fúngica (mildiu, oídio), enfermedades de madera y la biodiversidad microbiológica del suelo.",
      content_en: "WSET Level 3 evaluates terroir through an objective causal matrix:\n\n1. **Climate:** Solar radiation, temperature, rainfall, and diurnal range. Cool nights preserve malic acid; warm sunny days ripen sugars and anthocyanins.\n2. **Soil:** Moisture retention vs free drainage. Heavy clays remain cool and wet; rocky pebbles reflect daytime heat to extend evening ripening.\n3. **Topography:** Slope angle, southern aspect (in Northern Hemisphere), and altitude (every 100m climb drops ambient temperature by ~0.6°C).\n4. **Biological environment:** Disease pressure, mycorrhizal networks, and vine balance.",
      key_takeaways_es: [
        "La altitud y la amplitud térmica conservan la acidez natural del racimo.",
        "El drenaje del suelo regula el vigor vegetativo forzando a la vid a profundizar raíces.",
        "La orientación de ladera maximiza la interceptación de rayos solares en climas límite."
      ],
      key_takeaways_en: [
        "Altitude and diurnal shifts preserve natural crisp grape acidity.",
        "Good soil drainage curbs excess vine vigor and deepens roots.",
        "Slope aspect optimizes solar angle in marginal cool climates."
      ],
      related_grapes: ["Tempranillo", "Riesling", "Pinot Noir", "Nebbiolo"],
      related_regions: ["Ribera del Duero", "Mosel", "Bourgogne", "Barolo", "Mendoza"],
      tags: ["wset3", "terroir", "clima", "suelo", "altitud", "viticultura"]
    },
    {
      id: "geologia_suelos_emblematicos",
      title_es: "Geología del Vino: Albariza, Llicorella, Kimmeridgien y Galets",
      title_en: "Wine Geology: Albariza, Llicorella, Kimmeridgian & Galets",
      standard: "WSET3",
      category_es: "Edafología & Geología",
      category_en: "Soil Science & Geology",
      badge_color: "purple",
      summary_es: "Análisis edafológico de los 4 suelos históricos más famosos del mundo del vino y su impacto físico-químico en la hidratación y mineralidad de la viña.",
      summary_en: "Edafological study of the world's 4 most iconic vineyard soils and their direct physical influence on moisture regulation and mineral expression.",
      content_es: "1. **Albariza (Jerez / Marco Superior):** Margas calcáreas blancas con hasta un 40-50% de carbonato cálcico. Durante las lluvias otoñales absorbe agua como una esponja; en verano se calcina la superficie creando una costra blanca refractaria que impide la evaporación del agua subterránea, permitiendo que la Palomino sobreviva al calor seco andaluz.\n2. **Llicorella (Priorat):** Láminas de pizarra desmenuzable con inclusiones de cuarzo y mica. Suelo pobre, casi sin materia orgánica, que obliga a las raíces de Garnacha y Cariñena a penetrar hasta 15-20 metros en busca de humedad, aportando una concentración y mineralidad pétrea legendaria.\n3. **Kimmeridgien (Chablis / Champagne):** Arcilla margosa jurásica formada hace 150 millones de años, cuajada de fósiles prehistóricos de ostras (*Exogyra virgula*). Aporta la tensión ácida, austeridad y salinidad marina del gran Chardonnay septentrional.\n4. **Galets Roulés (Châteauneuf-du-Pape):** Grandes cantos rodados de cuarcita arrastrados por los glaciares alpinos a lo largo del Ródano. Absorben el calor diurno y lo liberan de noche sobre las cepas de Garnacha, asegurando maduraciones fenólicas opulentas.",
      content_en: "1. **Albariza (Jerez):** Chalky white marl holding up to 50% calcium carbonate. Forms an impermeable crust in summer, locking in winter rain for deep roots during drought.\n2. **Llicorella (Priorat):** Dark slate and quartz plates forcing vines downward 15+ meters into bedrock fractures, yielding low yields of intense, mineral-driven Cariñena and Garnacha.\n3. **Kimmeridgian (Chablis):** Ancient Jurassic seabed packed with fossilized oyster shells (*Exogyra virgula*), responsible for Chablis' famous flinty, saline edge.\n4. **Galets Roulés (Châteauneuf-du-Pape):** Smooth quartzite river stones radiating stored daytime sun during the night, guaranteeing high alcoholic and phenolic ripeness in Grenache.",
      key_takeaways_es: [
        "Albariza: esponja de humedad bajo el sol abrasador de Andalucía.",
        "Llicorella: pizarra fósil que confiere al Priorat su perfil concentrado y oscuro.",
        "Kimmeridgien: lecho marino jurásico de fósiles que electrifica Chablis.",
        "Galets Roulés: radiadores térmicos nocturnos en el Valle del Ródano."
      ],
      key_takeaways_en: [
        "Albariza acts as a deep natural reservoir against Mediterranean drought.",
        "Llicorella slate limits yields and elevates mineral depth.",
        "Kimmeridgian ancient fossils deliver unmistakable flinty tension.",
        "Galets stones radiate heat, ensuring rich Southern Rhône ripeness."
      ],
      related_grapes: ["Palomino Fino", "Garnacha", "Cariñena", "Chardonnay"],
      related_regions: ["Jerez-Xérès-Sherry", "Priorat", "Chablis", "Châteauneuf-du-Pape"],
      tags: ["suelos", "geologia", "albariza", "llicorella", "kimmeridgien", "galets"]
    },

    // --- 4. PROTOCOLO DE SALA Y ESTÁNDARES GLOBALES (ASI) ---
    {
      id: "asi_servicio_temperaturas",
      title_es: "Temperaturas de Servicio y Decantación (Norma ASI)",
      title_en: "Serving Temperatures & Decanting (ASI Standards)",
      standard: "ASI",
      category_es: "Servicio & Protocolo de Sala",
      category_en: "Service & Dining Protocol",
      badge_color: "emerald",
      summary_es: "La guía térmica y técnica de la Association de la Sommellerie Internationale para la correcta apertura, decantación y servicio en copa de cada tipología de vino.",
      summary_en: "The definitive temperature and decanting protocol established by the Association de la Sommellerie Internationale for world-class sommelier service.",
      content_es: "La temperatura modula la volatilidad aromática y la percepción gustativa: el frío apaga aromas y resalta la acidez y los taninos; el calor resalta el alcohol y la sensación dulce. La norma ASI establece:\n\n* **Espumosos y Cava / Champagne:** 6°C - 8°C (preserva la burbuja y realza la frescura viva).\n* **Blancos Jóvenes y Ligeros (Albariño, Sauvignon):** 8°C - 10°C.\n* **Blancos con Crianza y Gran Cuerpo (Chardonnay con barrica, Viña Tondonia Blanco):** 10°C - 12°C (permite que los aromas terciarios y lías se expresen).\n* **Tintos Ligeros y Fluidos (Mencía joven, Beaujolais, Pinot Noir):** 12°C - 14°C.\n* **Tintos de Crianza, Reserva y Gran Estructura (Ribera, Rioja, Burdeos, Barolo):** 15°C - 18°C (nunca por encima de 18°C para evitar la evaporación de etanol).\n* **Vinos Generosos y Fortificados:** Finos a 7°-9°C; Amontillados y Olorosos a 12°-14°C; Oportos a 15°-17°C.\n\n**Decantación vs Aireación:** Se decanta para separar sedimentos en botellas viejas con luz de vela sin agitar; se trasiega a jarra/carafina para oxigenar tintos jóvenes de alta concentración tánica.",
      content_en: "Temperature regulates volatile evaporation and palate perception. Cold enhances crispness and accentuates tannins; warmth amplifies alcohol vapor and perceived sweetness. Official ASI ranges:\n\n* **Sparkling:** 6°C - 8°C (tightens bubble structure and crisp freshness).\n* **Light Crisp Whites:** 8°C - 10°C.\n* **Oaked & Mature Whites:** 10°C - 12°C (releases tertiary lees/oak complexities).\n* **Light Body Reds:** 12°C - 14°C.\n* **Full-Bodied Structured Reds:** 15°C - 18°C (never exceed 18°C to prevent alcohol vapors).\n* **Fortified:** Dry flor at 7°-9°C; oxidative styles at 12°-14°C; Vintage Port at 15°-17°C.\n\n**Decanting vs Aerating:** Decant gently over candlelight to isolate solids in aged bottles; aerate vigorously in wide decanters to awaken closed young reds.",
      key_takeaways_es: [
        "Temperaturas > 18°C desvirtúan cualquier tinto haciendo predominar el alcohol.",
        "Los blancos de gran crianza pierden complejidad si se sirven gélidos de nevera.",
        "Decantar es separar sedimentos; jarrear/oxigenar es abrir vinos cerrados por juventud."
      ],
      key_takeaways_en: [
        "Temperatures exceeding 18°C ruin structure by magnifying ethanol fumes.",
        "Prestigious oaked whites served freezing cold lose their aromatic complexity.",
        "Decanting separates solids; aeration introduces oxygen to young closed wines."
      ],
      related_grapes: ["Tempranillo", "Chardonnay", "Pinot Noir", "Palomino Fino"],
      related_regions: ["Global"],
      tags: ["asi", "servicio", "temperaturas", "decantacion", "protocolo", "sommelier"]
    },

    // --- 5. ARTÍCULOS ADICIONALES DE REFERENCIA ---
    {
      id: "maceracion_carbonica_elaboracion",
      title_es: "Maceración Carbónica: Bioquímica Intracelular",
      title_en: "Carbonic Maceration: Intracellular Biochemistry",
      standard: "UDIMA",
      category_es: "Vinificación en Tintos",
      category_en: "Red Wine Vinification",
      badge_color: "amber",
      summary_es: "Fermentación enzimática anaeróbica dentro del grano de uva sin estrujar, liberando aromas de plátano y fresa silvestre mediante acetato de isoamilo con extracción tánica mínima.",
      summary_en: "Anaerobic intracellular enzymatic fermentation inside uncrushed whole grape berries, synthesizing isoamyl acetate (banana/candy) with minimal tannin extraction.",
      content_es: "La maceración carbónica tradicional (propia de Rioja Alavesa y Beaujolais) exige introducir racimos enteros e intactos dentro de un depósito sellado saturado de CO2 a 30°-32°C. En estas condiciones de asfixia celular, las enzimas endógenas de la propia uva metabolizan un 20-30% de los azúcares directamente a etanol sin intervención de levaduras, degradan hasta la mitad del ácido málico y transfieren el color de los antocianos de la piel hacia la pulpa sin disolver los taninos amargos de las pepitas. El rasgo organoléptico definitorio es la síntesis de ésteres volátiles, especialmente el acetato de isoamilo (chuchería de plátano, fresa ácida, kirsch y toque de clavo de olor). Son vinos sedosos, explosivamente frutales y diseñados para consumo inmediato.",
      content_en: "Traditional carbonic maceration involves sealing whole, uncrushed grape clusters in a CO2-saturated tank at 30°-32°C. Under cellular asphyxiation, the grape's own enzymes convert ~20% of sugar into ethanol without yeast, degrade half the malic acid, and pull anthocyanin pigments from skins into the pulp without extracting bitter seed tannins. It produces high levels of isoamyl acetate, yielding characteristic aromas of bubblegum, banana, raspberry, and cinnamon, creating juicy, low-tannin reds ready for early drinking.",
      key_takeaways_es: [
        "Fermentación intracelular sin presencia de levaduras iniciales.",
        "Gran extracción de color con nula extracción de taninos amargos de pepitas.",
        "Perfil aromático dominado por acetato de isoamilo (plátano y frutas rojas confitadas)."
      ],
      key_takeaways_en: [
        "Pure intracellular fermentation without yeast intervention in the primary phase.",
        "Vibrant color extraction with near-zero harsh seed tannin pickup.",
        "Flavor profile dominated by isoamyl acetate (banana, candied berry, bubblegum)."
      ],
      related_grapes: ["Tempranillo", "Gamay", "Garnacha"],
      related_regions: ["Rioja Alavesa", "Beaujolais", "Vinos de Madrid"],
      tags: ["enologia", "maceracion_carbonica", "fermentacion", "isoamilo", "rioja", "gamay"]
    },
    {
      id: "criaderas_y_soleras_jerez",
      title_es: "El Sistema Dinámico de Criaderas y Soleras",
      title_en: "The Criaderas and Solera Fractional Aging System",
      standard: "UDIMA",
      category_es: "Enología & Vinos Especiales",
      category_en: "Enology & Special Vinifications",
      badge_color: "amber",
      summary_es: "Método dinámico de envejecimiento fraccionario en cascada de botas de roble americano que garantiza la consistencia organoléptica y la longevidad de los vinos de Jerez y Montilla.",
      summary_en: "Dynamic fractional blending cascade of American oak butts ensuring sensory consistency and perpetual continuity in Jerez and Montilla wines.",
      content_es: "A diferencia de la crianza estática por añadas (vintage), el sistema de criaderas y soleras es un proceso de mezcla fraccionada continua. Las botas se organizan en escalas según su edad: la escala más cercana al suelo (la Solera) contiene el vino de mayor vejez; sobre ella se apilan las Criaderas (1ª criadera, 2ª criadera, etc., hasta 8 o 10 escalas en grandes bodegas). Periódicamente se realiza la 'saca' (extracción de hasta un tercio del volumen de la Solera para embotellar) y el 'rocío' (reposición del volumen extraído con vino de la 1ª criadera, y así sucesivamente en cascada). En crianza biológica, el rocío aporta nutrientes y micronutrientes frescos que mantienen vivo el velo de flor; en crianza oxidativa, la evaporación a través del roble poroso (la merma) concentra acidez, glicerol y grado alcohólico año tras año.",
      content_en: "Unlike static vintage aging, the Solera system is a perpetual fractional blending process. American oak butts are stacked in tiers: the bottom row (Solera) holds the oldest wine; upper tiers (Criaderas) hold progressively younger stages. When wine is drawn for bottling ('saca', max 1/3 volume), it is refreshed ('rocío') with wine from the tier above. In biological aging, this feeds fresh nutrients to the flor veil; in oxidative aging, barrel breathing evaporates water, concentrating acidity, alcohol, and nutty complexity over decades.",
      key_takeaways_es: [
        "Garantiza una calidad idéntica e inmutable botella tras botella a lo largo de décadas.",
        "El rocío nutre continuamente las levaduras del velo de flor.",
        "La evaporación ('merma') en soleras oxidativas concentra la sapidez y eleva el grado natural."
      ],
      key_takeaways_en: [
        "Guarantees absolute consistency across decades of bottling.",
        "Replenishment feeds essential micronutrients to the delicate flor yeast.",
        "Oxidative evaporation concentrates dry extract, alcohol, and acidity."
      ],
      related_grapes: ["Palomino Fino", "Pedro Ximénez"],
      related_regions: ["Jerez-Xérès-Sherry", "Manzanilla de Sanlúcar", "Montilla-Moriles"],
      tags: ["jerez", "solera", "criaderas", "saca", "rocio", "enologia"]
    },
    {
      id: "ribera_vs_rioja_terruno",
      title_es: "Terruño Comparado: Ribera del Duero vs Rioja",
      title_en: "Comparative Terroir: Ribera del Duero vs Rioja",
      standard: "WSET3",
      category_es: "Terruño & Factores Ambientales",
      category_en: "Terroir & Environmental Factors",
      badge_color: "purple",
      summary_es: "Análisis geoclimático y edafológico de cómo la altitud de la meseta castellana y la influencia atlántica del valle del Ebro moldean dos expresiones magistrales pero opuestas de la Tempranillo.",
      summary_en: "Geoclimatic and soil analysis of how Castilian plateau elevation and Ebro Atlantic influence shape two distinct master expressions of Tempranillo.",
      content_es: "Ribera del Duero y Rioja representan las dos cumbres de la Tempranillo en el mundo, pero sus factores naturales son profundamente divergentes:\n\n* **Ribera del Duero:** Viñedos entre 750 y 950 metros de altitud en la meseta castellana. Clima continental extremo con inviernos de hasta -15°C, veranos secos y oscilaciones térmicas día-noche de más de 20°C en época de maduración. Esta amplitud térmica induce a la uva a generar un hollejo grueso, resultando en vinos de capa profunda, taninos masticables muy potentes, acidez fresca y notas de fruta negra silvestre (mora, ciruela) y balsámicos.\n* **Rioja (Alta y Alavesa):** Viñedos entre 350 y 650 metros en el valle del Ebro, resguardados por la Sierra de Cantabria que frena las borrascas del Cantábrico pero permite la entrada de una suave humedad atlántica. Suelos arcillo-calcáreos y aluviales que producen una Tempranillo de acidez más integrada, tanino fino y sedoso, aromas de fruta roja fresca (fresa, cereza) y una asombrosa aptitud para crianzas prolongadas en barrica de roble americano y francés.",
      content_en: "Ribera del Duero and Rioja showcase contrasting expressions of Tempranillo based on elevation and climate:\n\n* **Ribera del Duero:** High-altitude plateau (750-950m) with extreme continentality and 20°C+ diurnal range. Cool nights thicken skins, generating deep purple extraction, bold structural tannins, crisp natural acidity, and dark blackberry character.\n* **Rioja (Alta/Alavesa):** Lower elevation (350-650m) sheltered by Sierra de Cantabria, blending Atlantic coolness with Mediterranean warmth on chalky-clay soils. Produces brighter red-fruit aromatics, silken tannins, and legendary capacity for extended oxidative oak aging.",
      key_takeaways_es: [
        "Ribera del Duero: Altitud extrema ➔ Hollejo grueso ➔ Potencia, fruta negra y tanino muscular.",
        "Rioja: Influencia atlántica moderadora ➔ Fruta roja viva, tanino pulido y finura terciaria de guarda.",
        "La oscilación térmica diurna es el factor clave que preserva la acidez en Ribera."
      ],
      key_takeaways_en: [
        "Ribera: High altitude creates thicker skins, muscular tannins, and dark fruit power.",
        "Rioja: Atlantic moderation yields brighter red fruit, silken texture, and oak harmony.",
        "Diurnal shift is the decisive terroir lever preserving natural acidity in Ribera."
      ],
      related_grapes: ["Tempranillo", "Garnacha", "Graciano"],
      related_regions: ["Ribera del Duero", "Rioja"],
      tags: ["wset3", "ribera_del_duero", "rioja", "tempranillo", "terruno", "clima"]
    },
    {
      id: "metodo_tradicional_autolisis_espuma",
      title_es: "Método Tradicional: Segunda Fermentación y Autólisis",
      title_en: "Traditional Method: Secondary Fermentation and Autolysis",
      standard: "UDIMA",
      category_es: "Espumosos & Método Tradicional",
      category_en: "Sparkling & Traditional Method",
      badge_color: "amber",
      summary_es: "Cinética de la segunda fermentación en botella (prise de mousse), generación de 5-6 atmósferas de presión de CO2 y la liberación de manoproteínas enriquecedoras de la espuma.",
      summary_en: "Kinetics of in-bottle secondary fermentation (prise de mousse), 5-6 bars of CO2 pressure generation, and yeast mannoprotein release during prolonged aging.",
      content_es: "El método tradicional (Champenoise / Cava / Corpinnat) se inicia con la adición del 'licor de tiraje' (vino base + azúcar de caña ~24 g/L + levaduras seleccionadas y clarificante) y el sellado de la botella con chapa corona. Durante 6 a 8 semanas en rima a 12°-15°C se produce la 'prise de mousse': las levaduras fermentan el azúcar, produciendo aproximadamente 1.2-1.3% más de alcohol y liberando dióxido de carbono que, al estar confinado, se disuelve en el líquido creando entre 5 y 6 atmósferas de presión. Una vez agotado el azúcar, las levaduras mueren y se inicia la autólisis enzimática (mínimo 9 meses en Cava estándar, 15 meses en Champagne, 30 meses en Gran Reserva). Las paredes de las levaduras liberan manoproteínas, coloides y aminoácidos que aportan una textura cremosa inigualable en el centro de boca, reducen la astringencia y generan los aromas terciarios característicos de panadería, masa madre, frutos secos y brioche.",
      content_en: "The traditional method commences with the addition of the 'liqueur de tirage' (base wine, ~24 g/L sugar, selected yeasts) followed by crown-capping. Over 6-8 weeks at 12°-15°C, the 'prise de mousse' occurs: yeast ferments the sugar, raising alcohol by ~1.3% and dissolving CO2 under 5 to 6 bars of pressure. Following fermentation, yeasts die and undergo enzymatic autolysis (minimum 15 months in Champagne, 30+ months in Grand Reserves). Broken cell walls release mannoproteins and amino acids, conferring velvety creaminess, stabilizing the fine bead, and imparting toasted brioche and almond nuances.",
      key_takeaways_es: [
        "24 g/L de azúcar en el tiraje generan con precisión matemática ~6 atmósferas de presión.",
        "La autólisis prolongada sobre lías aporta la textura cremosa y notas de brioche/pan tostado.",
        "Las manoproteínas protegen la estabilidad de la burbuja y suavizan el paladar."
      ],
      key_takeaways_en: [
        "24 g/L sugar addition reliably yields ~6 bars of atmospheric CO2 pressure.",
        "Extended yeast autolysis produces creamy mousse and toasted brioche flavors.",
        "Mannoproteins coat the palate, curbing astringency and stabilizing bubble persistence."
      ],
      related_grapes: ["Chardonnay", "Pinot Noir", "Xarel·lo", "Macabeo", "Parellada"],
      related_regions: ["Champagne", "Cava", "Corpinnat", "Franciacorta"],
      tags: ["espumosos", "metodo_tradicional", "champagne", "cava", "autolisis", "lias"]
    }
  ];

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = WINEPEDIA_ARTICLES;
  } else {
    root.WINEPEDIA_ARTICLES = WINEPEDIA_ARTICLES;
  }
})(typeof window !== 'undefined' ? window : globalThis);
