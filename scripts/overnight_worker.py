#!/usr/bin/env python3
"""
WINE³ai — Overnight Autonomous Content Generator
Runs locally via LM Studio (http://localhost:1234) until 06:45 AM (before 07:00 AM).
Generates high-precision, canonical enological content across:
  1. WINEp3dIA Articles (Soils, Vinifications, Vine Biology, Chemistry/Faults)
  2. Sommelier Exam Flashcards (WSET 3, CMS Deductive, ASI Global)
  3. Grape Varieties Profiles (Tasting descriptors, Terroir, Pairings)
  4. Appellations of Spain and the World (Key benchmark DOs/AOCs)
"""

import sys
import os
import json
import time
import re
from datetime import datetime

# Add project root to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.append(PROJECT_ROOT)

from scripts.lm_studio import query_lm

LOG_FILE = os.path.join(PROJECT_ROOT, "logs", "overnight_generation.log")
GENERATED_DIR = os.path.join(PROJECT_ROOT, "data", "generated")
REPORT_FILE = os.path.join(PROJECT_ROOT, "OVERNIGHT_REPORT.md")

os.makedirs(GENERATED_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log(msg):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now_str}] {msg}"
    print(entry, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

FORCE_RUN = "--now" in sys.argv or "--force" in sys.argv or "--continue" in sys.argv

def is_time_up():
    if FORCE_RUN:
        return False
    now = datetime.now()
    # Stop between 06:45 and 07:00 (or if it's already 7 AM or later)
    if now.hour == 6 and now.minute >= 45:
        return True
    if 7 <= now.hour < 20: # If past 7:00 AM
        return True
    return False

def extract_json(raw_text):
    if not raw_text:
        return None
    # Strip markdown code blocks if present
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', raw_text)
    if match:
        raw_text = match.group(1)
    
    # Try parsing direct JSON
    try:
        return json.loads(raw_text)
    except Exception:
        # Try to find opening and closing brace
        start = raw_text.find('{')
        end = raw_text.rfind('}')
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(raw_text[start:end+1])
            except Exception:
                pass
    return None

def save_checkpoint(category, data):
    filepath = os.path.join(GENERATED_DIR, f"{category}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==========================================
# QUEUES OF CURATED TASKS
# ==========================================

WINEPEDIA_TOPICS = [
    # Suelos y Geología (15)
    {"id": "suelo_albariza_jerez", "title": "Suelo de Albariza", "area": "Edafología", "focus": "Carbonato cálcico, margas blancas, retención hídrica en Marco de Jerez"},
    {"id": "suelo_llicorella_priorat", "title": "Suelo de Llicorella", "area": "Edafología", "focus": "Pizarras paleozoicas descompuestas, cuarzo y mica, baja fertilidad en DOCa Priorat"},
    {"id": "suelo_kimmeridgiense_chablis", "title": "Caliza Kimmeridgiense", "area": "Edafología", "focus": "Fósiles marinos Exogyra virgula, margas calcáreas en Chablis y Sancerre"},
    {"id": "suelo_galets_roules_rhone", "title": "Galets Roulés de Châteauneuf-du-Pape", "area": "Edafología", "focus": "Cantos rodados cuarcíticos alpinos, acumulación térmica y radiación nocturna"},
    {"id": "suelo_loess_austria", "title": "Suelos de Loess", "area": "Edafología", "focus": "Sedimento eólico periglacial limoso, retención de agua y acidez en Kamptal y Wagram"},
    {"id": "suelo_terra_rossa_coonawarra", "title": "Terra Rossa de Coonawarra", "area": "Edafología", "focus": "Arcilla roja rica en óxido de hierro sobre caliza porosa en South Australia"},
    {"id": "suelo_basalto_volcanico_canarias", "title": "Terruño Volcánico: Basaltos y Lapilli", "area": "Edafología", "focus": "Cenizas volcánicas (picón), basalto poroso y viñedos de pie franco en Canarias y Etna"},
    {"id": "suelo_tuffeau_loire", "title": "Toba Calcárea (Tuffeau) del Loira", "area": "Edafología", "focus": "Tiza porosa sedimentaria del cretácico, galerías subterráneas y frescura en Vouvray y Chinon"},
    {"id": "suelo_margas_azules_jura", "title": "Margas Azules del Jura", "area": "Edafología", "focus": "Marnes bleues del Lias, concentración mineral y perfil del Savagnin en Château-Chalon"},
    {"id": "suelo_silex_pedernal", "title": "Silex y Pedernal", "area": "Edafología", "focus": "Dióxido de silicio, notas de piedra de fusil (pierre à fusil) en Pouilly-Fumé"},
    {"id": "suelo_arenas_colares_rueda", "title": "Suelos Arenosos y Resistencia a Filoxera", "area": "Edafología", "focus": "Dunas litorales de Colares y arenas silíceas de Rueda con viñedos centenarios en pie franco"},
    {"id": "suelo_granito_cornas_riasbaixas", "title": "Granito Descompuesto (Xabre / Gore)", "area": "Edafología", "focus": "Arenas graníticas ácidas, drenaje extremo y tensión mineral en Rías Baixas y Cornas"},
    {"id": "suelo_esquisto_douro", "title": "Esquisto Foliado del Alto Douro", "area": "Edafología", "focus": "Lajas de esquisto verticalmente fracturadas para penetración radicular extrema en Portugal"},
    {"id": "suelo_caliza_jurassica_bourgogne", "title": "Caliza Oolítica de la Côte d'Or", "area": "Edafología", "focus": "Calizas jurásicas batienses y bajocienses, drenaje y pH óptimo para Pinot Noir y Chardonnay"},
    {"id": "suelo_arcillas_pesadas_pomerol", "title": "Arcillas Azules de Pomerol", "area": "Edafología", "focus": "Boutonnière de argile bleue en Pétrus, retención de humedad y opulencia del Merlot"},

    # Vinificaciones Especiales y Enología (15)
    {"id": "maceracion_carbonica_racimo_entero", "title": "Maceración Carbónica y Semicarbónica", "area": "Enología", "focus": "Fermentación intracelular sin oxígeno, degradación del ácido málico, aromas de plátano y fresa"},
    {"id": "batonnage_lias_finas", "title": "Crianza sobre Lías Finas y Bâtonnage", "area": "Enología", "focus": "Autólisis de Saccharomyces, liberación de manoproteínas, untuosidad y protección redox"},
    {"id": "metodo_champenoise_vs_charmat", "title": "Método Tradicional vs Charmat vs Ancestral", "area": "Enología", "focus": "Segunda fermentación en botella vs autoclave vs una sola fermentación con carbónico natural"},
    {"id": "podredumbre_noble_botrytis", "title": "Podredumbre Noble (Botrytis cinerea)", "area": "Enología", "focus": "Condiciones de nieblas matinales y tardes secas, concentración de azúcares y ácido glicónico en Sauternes y Tokaj"},
    {"id": "tecnica_appassimento_amarone", "title": "Técnica del Appassimento", "area": "Enología", "focus": "Deshidratación pasiva de uvas en esteras de bambú (fruttai), glicerol y concentración fenólica en Valpolicella"},
    {"id": "vinos_naranjas_maceracion_blancos", "title": "Vinos Naranjas (Skin-Contact White Wines)", "area": "Enología", "focus": "Maceración prolongada de uvas blancas con hollejos y raspón, extracción de taninos y flavonoides"},
    {"id": "fermentacion_anforas_qvevri", "title": "Vinificación en Ánforas de Barro y Qvevri", "area": "Enología", "focus": "Tradición milenaria georgiana (UNESCO), microoxigenación neutra sin cesión de madera"},
    {"id": "fermentacion_malolactica_diacetilo", "title": "Fermentación Maloláctica (FML)", "area": "Bioquímica", "focus": "Conversión de ácido málico en láctico por Oenococcus oeni, síntesis de diacetilo y redondez"},
    {"id": "crianza_oxidativa_soleras", "title": "Crianza Oxidativa: Olorosos, Madeiras y Tawnies", "area": "Enología", "focus": "Merma por transpiración en barrica, concentración alcohólica, aldehídos, lactonas y frutos secos"},
    {"id": "microoxigenacion_taninos", "title": "Microoxigenación (Micro-Bullage)", "area": "Enología", "focus": "Inyección controlada de microburbujas de O2, polimerización de antocianos y estabilización de color"},
    {"id": "roble_frances_vs_americano", "title": "Roble Francés vs Americano vs Húngaro", "area": "Enología", "focus": "Quercus petraea vs Quercus alba, densidad de poro, lactonas de roble (coco) y eugenol (clavo)"},
    {"id": "criomaceracion_prefermentativa", "title": "Criomaceración Prefermentativa en Frío", "area": "Enología", "focus": "Maceración a 4-8°C con nieve carbónica previa a la fermentación para extracción aromática pura"},
    {"id": "prensado_directo_vs_sangrado", "title": "Prensado Directo vs Sangrado (Saignée) para Rosados", "area": "Enología", "focus": "Diferencias técnicas, color provenzal tenue vs mayor estructura fenólica"},
    {"id": "desfangado_estatico_mostos", "title": "Desfangado Estático y Flotación", "area": "Enología", "focus": "Clarificación de mostos blancos por frío y turbidez controlada (NTU) antes de fermentar"},
    {"id": "icewine_eiswein_crioconcentracion", "title": "Icewine (Eiswein): Crioconcentración Natural", "area": "Enología", "focus": "Vendimia a -7°C/-8°C con uvas congeladas en la cepa, congelación del agua celular y mosto hiperconcentrado"},

    # Fisiología de la Vid y Bioquímica (10)
    {"id": "ciclo_vegetativo_vid_fenologia", "title": "Ciclo Biológico Anual de la Vid", "area": "Viticultura", "focus": "Lloro, desborre, floración, cuajado, envero, maduración fenólica y parada invernal"},
    {"id": "sistemas_conduccion_guyot_gobelet", "title": "Sistemas de Conducción: Vaso vs Guyot vs Espaldera", "area": "Viticultura", "focus": "Gestión del dosel vegetal (canopy management), sombreo, exposición fotosintética y mecanización"},
    {"id": "pie_franco_vs_portainjertos_filoxera", "title": "Patrones Porta-injertos y Filoxera", "area": "Viticultura", "focus": "Daktulosphaira vitifoliae, cruces con Vitis riparia y rupestris, adaptación a caliza y sequía"},
    {"id": "estres_hidrico_fotosintesis_taninos", "title": "Déficit Hídrico Controlado (RDI)", "area": "Viticultura", "focus": "Potencial hídrico en hoja, inhibición del crecimiento vegetativo y síntesis de polifenoles"},
    {"id": "pirazinas_verdor_cabernet", "title": "Metoxipirazinas y Madurez de la Uva", "area": "Bioquímica", "focus": "3-isobutil-2-metoxipiracina (IBMP), aroma a pimiento verde en Cabernet Sauvignon y Sauvignon Blanc"},
    {"id": "rotundona_pimienta_syrah", "title": "Rotundona: El Sesquiterpeno de la Pimienta Negra", "area": "Bioquímica", "focus": "Umbral de percepción bajísimo en Syrah/Shiraz y Grüner Veltliner en climas frescos"},
    {"id": "esteres_fermentacion_tioles", "title": "Tioles Volátiles: Fruta Tropical y Boj", "area": "Bioquímica", "focus": "Precursores cisteínicos en Sauvignon Blanc y Verdejo (3MHA, 3MH, 4MMP), aromas de maracuyá"},
    {"id": "oidio_vs_mildiu_hongos", "title": "Mildiu (Plasmopara) vs Oídio (Uncinula)", "area": "Sanidad Vegetal", "focus": "Manchas de aceite y pelusa blanca, condiciones de 10-10-10, tratamientos con cobre y azufre"},
    {"id": "enfermedades_madera_yesca", "title": "Enfermedades de Madera: Yesca y Eutiosis", "area": "Sanidad Vegetal", "focus": "Hongos vasculares, apoplejía de la vid, corte y desinfección en poda de respeto"},
    {"id": "seleccion_masal_vs_clonal", "title": "Selección Masal vs Selección Clonal", "area": "Viticultura", "focus": "Preservación de biodiversidad genética varietal frente a uniformidad sanitaria y productiva"}
]

STUDY_CARD_TOPICS = [
    # WSET 3 (12)
    {"standard": "WSET3", "category": "Terruño & Factores Naturales", "topic": "Influencia de las nieblas matinales de San Pablo Bay en Carneros y Napa Valley"},
    {"standard": "WSET3", "category": "Climas del Mundo", "topic": "Efecto Föhn en Mendoza (Viento Zonda) y en Suiza central sobre la maduración de la uva"},
    {"standard": "WSET3", "category": "Enología & Estilos", "topic": "Diferencia química y organoléptica entre Oloroso y Amontillado en el Marco de Jerez"},
    {"standard": "WSET3", "category": "Viticultura & Poda", "topic": "Poda Guyot simple vs cordón Royat: objetivos productivos y prevención de heladas"},
    {"standard": "WSET3", "category": "Regiones del Mundo", "topic": "Clasificación de calidad en Burdeos: 1855 Médoc vs Saint-Émilion Grand Cru vs Graves"},
    {"standard": "WSET3", "category": "Regiones del Mundo", "topic": "Factores de calidad en Mosel: pendientes extremas de pizarra azul y moderación por el río"},
    {"standard": "WSET3", "category": "Vinificaciones Especiales", "topic": "Condiciones exactas para la elaboración de Tokaji Aszú y medición en puttonyos / azúcar residual"},
    {"standard": "WSET3", "category": "Variedades & Estilos", "topic": "Riesling de Clare Valley vs Mosel: acidez, cuerpo y notas de kerosene (TDN)"},
    {"standard": "WSET3", "category": "Viticultura & Suelo", "topic": "Por qué la caliza albariza retiene agua en inviernos lluviosos y forma una costra en veranos secos"},
    {"standard": "WSET3", "category": "Enología de Tintos", "topic": "Impacto de la temperatura de fermentación en tintos (28-32°C) en la extracción de taninos"},
    {"standard": "WSET3", "category": "Enología de Blancos", "topic": "Uso de barricas de roble y fermentación maloláctica en Chardonnay de Chablis vs Meursault"},
    {"standard": "WSET3", "category": "Regiones de España", "topic": "Rioja Alta, Rioja Alavesa y Rioja Oriental: contrastes de clima, suelo y variedad predominante"},

    # CMS Deductive Tasting & Sommelier (12)
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Deducción ciega: cómo distinguir un Pinot Noir de Borgoña de un Pinot Noir de Central Otago"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Identificación de Cabernet Sauvignon vs Cabernet Franc: pirazinas, estructura tánica y frutos negros"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Distinción visual y olfativa de Nebbiolo (Barolo) vs Sangiovese (Brunello di Montalcino)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata ciega de Syrah de Cornas (Ródano Norte) vs Shiraz de Barossa Valley (Australia)"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Identificación y química del defecto de reducción (H2S, mercaptanos) y cómo remediarlo en copa"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Identificación sensorial de Brettanomyces (4-etilfenol / 4-etilguayacol) frente a crianza en roble viejo"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje con platos ricos en Umami (champiñones, soja, parmesano): impacto en amargor y acidez"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje para alimentos picantes (capsaicina): por qué el alcohol alto y el tanino empeoran el ardor"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Armonía molecular: Sauternes y queso Roquefort (sal marina, penicillium roqueforti y botrytis)"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Protocolo de decantación de un oporto Vintage de más de 30 años con poso y uso de pinzas al rojo"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Temperaturas óptimas de servicio según el Court of Master Sommeliers para diferentes estilos de vino"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata deductiva de Sauvignon Blanc: Valle del Loira (Sancerre) vs Marlborough (Nueva Zelanda)"},

    # ASI Global Sommelier Standards (12)
    {"standard": "ASI", "category": "Protocolo de Sala & Deontología", "topic": "Protocolo ASI de sustitución ante una botella defectuosa (TCA) sin incomodar al cliente"},
    {"standard": "ASI", "category": "Armonía y Gastronomía Global", "topic": "Maridaje de vanguardia para ostras frescas: Albariño sobre lías vs Muscadet Sèvre et Maine vs Chablis"},
    {"standard": "ASI", "category": "Vinos del Mundo", "topic": "Vinos fortificados: diferencias de elaboración entre Porto, Madeira, Jerez y Marsala"},
    {"standard": "ASI", "category": "Legislación & Normativa", "topic": "Sistema de clasificación VDP en Alemania: Gutswein, Ortswein, Erste Lage y Grosse Lage (GG)"},
    {"standard": "ASI", "category": "Vinos del Mundo", "topic": "Las 3 zonas vitivinícolas de Sudáfrica (Costera, Breede River Valley, Cape South Coast) y Chenin Blanc"},
    {"standard": "ASI", "category": "Vinos del Mundo", "topic": "Vinos de Georgia: la fermentación en Qvevri y el método tradicional de maceración en Kakheti"},
    {"standard": "ASI", "category": "Armonía y Gastronomía Global", "topic": "Maridaje con chocolate negro 85% de pureza: por qué los tintos secos fracasan y la solución con Pedro Ximénez o Banyuls"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Protocolo de cata de copas Riedel / Zalto: cómo la forma del cáliz modifica la dispersión aromática"},
    {"standard": "ASI", "category": "Enología & Cata", "topic": "El fenómeno de la luz (Goût de lumière) en vinos embotellados en vidrio transparente y riboflavina"},
    {"standard": "ASI", "category": "Legislación & Normativa", "topic": "Las categorías de envejecimiento en España: Crianza, Reserva y Gran Reserva según ley de la viña y el vino"},
    {"standard": "ASI", "category": "Armonía y Gastronomía Global", "topic": "Maridaje con pescados azules grasos (atún rojo, salmón): taninos suaves, acidez alta y Mencía / Pinot Noir"},
    {"standard": "ASI", "category": "Vinos del Mundo", "topic": "La corriente fría de Humboldt y su impacto en los valles costeros de Chile (Casablanca, San Antonio)"}
]

GRAPES_TO_ENRICH = [
    # Top 40 variedades emblemáticas
    "Tempranillo", "Cabernet Sauvignon", "Merlot", "Pinot Noir", "Syrah", "Nebbiolo", 
    "Sangiovese", "Garnacha", "Malbec", "Cabernet Franc", "Gamay", "Mourvedre", 
    "Touriga Nacional", "Mencia", "Barbera", "Carmenere", "Tannat", "Pinotage",
    "Chardonnay", "Sauvignon Blanc", "Riesling", "Chenin Blanc", "Albarino", "Viognier", 
    "Semillon", "Gewurztraminer", "Pinot Gris", "Gruner Veltliner", "Verdejo", "Godello",
    "Assyrtiko", "Furmint", "Glera", "Palomino Fino", "Pedro Ximenez", "Zinfandel",
    "Bobal", "Graciano", "Carignan", "Corvina"
]

def generate_winepedia_article(item):
    prompt = f"""Genera un artículo técnico canónico para WINEp3dIA sobre '{item['title']}' ({item['area']}).
Enfoque: {item['focus']}.
Devuelve EXCLUSIVAMENTE un objeto JSON válido con esta estructura:
{{
  "id": "{item['id']}",
  "standard": "WSET3",
  "category_es": "{item['area']} & Terruño",
  "category_en": "Enology & Terroir",
  "badge_color": "amber",
  "title_es": "{item['title']}: Mecanismo y Relevancia Enológica",
  "title_en": "{item['title']}: Mechanism and Enological Significance",
  "summary_es": "Resumen técnico sintético en 1 o 2 frases.",
  "summary_en": "Synthetic technical summary in 1 or 2 sentences.",
  "content_es": "Desarrollo técnico exhaustivo de 2-3 párrafos explicando principios bioquímicos, enológicos y su impacto sensorial.",
  "content_en": "Thorough technical English explanation of 2-3 paragraphs covering biochemical mechanisms and sensorial traits.",
  "key_takeaways_es": [
    "Punto clave técnico 1",
    "Punto clave técnico 2",
    "Punto clave técnico 3"
  ],
  "key_takeaways_en": [
    "Key technical takeaway 1",
    "Key technical takeaway 2",
    "Key technical takeaway 3"
  ],
  "related_grapes": ["Variedad1", "Variedad2"],
  "related_regions": ["Region1", "Region2"],
  "tags": ["{item['id'].replace('_', ' ')}", "enologia", "terruño"]
}}
Responde SOLO con el código JSON."""

    raw = query_lm(
        prompt, 
        system_prompt="Eres un Master Sommelier y enólogo doctorado. Mantén tu razonamiento interno breve y conciso (máximo 300 palabras). Responde única y exclusivamente con el JSON solicitado.",
        max_tokens=3500
    )
    return extract_json(raw)

def generate_study_card(item, card_index):
    prompt = f"""Genera una ficha de estudio y cata deductiva de alta precisión para el canon {item['standard']}.
Categoría: {item['category']}.
Tema específico: {item['topic']}.
Devuelve EXCLUSIVAMENTE un objeto JSON bilingüe válido con esta estructura:
{{
  "id": "card_{item['standard'].lower()}_{card_index:03d}",
  "standard": "{item['standard']}",
  "category": "{item['category']} ({item['standard']})",
  "category_en": "{item['category']} ({item['standard']})",
  "question_es": "Pregunta analítica profunda de examen o caso clínico de sumillería en español.",
  "question_en": "Deep analytical examination or sommelier case question in English.",
  "answer_es": "Deducción técnica completa y argumentada estructurada con puntos clave en español.",
  "answer_en": "Thorough technical deduction structured with key bullet points in English.",
  "solution_es": "Consejo práctico de sumiller en sala o clave mnemotécnica en español.",
  "solution_en": "Practical floor sommelier advice or mnemonic exam key in English.",
  "citation": "Canon oficial {item['standard']} & The Oxford Companion to Wine"
}}
Responde SOLO con el JSON."""

    raw = query_lm(
        prompt, 
        system_prompt="Eres examinador oficial de Master Sommelier y WSET Diploma. Razonamiento interno breve y conciso (máximo 250 palabras). Responde exclusivamente con el JSON.",
        max_tokens=2500
    )
    return extract_json(raw)

def generate_grape_profile(grape_name):
    prompt = f"""Genera la ficha organoléptica y ampelográfica exhaustiva para la variedad de uva '{grape_name}'.
Devuelve EXCLUSIVAMENTE un objeto JSON válido con esta estructura:
{{
  "grape": "{grape_name}",
  "profile": {{
    "acidity": "Media / Alta / etc",
    "tannin": "Bajo / Medio / Alto / etc",
    "alcohol": "Medio (13-14%) / etc",
    "body": "Medio / Completo / Ligero",
    "aromas_primary": ["Aroma 1", "Aroma 2", "Aroma 3", "Aroma 4"],
    "aromas_secondary": ["Aroma fermentativo 1", "Aroma 2"],
    "aromas_tertiary": ["Aroma envejecimiento 1", "Aroma 2"],
    "benchmark_appellations": ["DO/AOC 1 (Pais)", "DO/AOC 2 (Pais)", "DO/AOC 3 (Pais)"],
    "ideal_food_pairings": ["Maridaje 1", "Maridaje 2", "Maridaje 3"]
  }},
  "sommelier_note_es": "Nota de cata técnica de 2 frases sobre el carácter de la variedad.",
  "sommelier_note_en": "Technical 2-sentence tasting note on varietal signature."
}}
Responde SOLO con el JSON."""

    raw = query_lm(
        prompt, 
        system_prompt="Eres un ampelógrafo y Master of Wine. Razonamiento interno breve y conciso (máximo 250 palabras). Responde exclusivamente con el JSON.",
        max_tokens=2500
    )
    return extract_json(raw)

# ==========================================
# MAIN OVERNIGHT WORKER LOOP
# ==========================================

def main():
    log("==================================================")
    log("STARTING OVERNIGHT AUTONOMOUS GENERATOR")
    log(f"Current local time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("Target cutoff: 06:45 AM (before 07:00 AM)")
    log("==================================================")

    generated_articles = []
    generated_cards = []
    generated_grapes = []

    # Load existing generated checkpoints if any
    winepedia_file = os.path.join(GENERATED_DIR, "winepedia_articles.json")
    if os.path.exists(winepedia_file):
        try:
            with open(winepedia_file, "r", encoding="utf-8") as f:
                generated_articles = json.load(f)
        except Exception:
            pass

    cards_file = os.path.join(GENERATED_DIR, "study_cards.json")
    if os.path.exists(cards_file):
        try:
            with open(cards_file, "r", encoding="utf-8") as f:
                generated_cards = json.load(f)
        except Exception:
            pass

    grapes_file = os.path.join(GENERATED_DIR, "grape_profiles.json")
    if os.path.exists(grapes_file):
        try:
            with open(grapes_file, "r", encoding="utf-8") as f:
                generated_grapes = json.load(f)
        except Exception:
            pass

    existing_article_ids = set(a.get("id") for a in generated_articles if isinstance(a, dict))
    existing_card_topics = set(c.get("question_es", "")[:30] for c in generated_cards if isinstance(c, dict))
    existing_grape_names = set(g.get("grape") for g in generated_grapes if isinstance(g, dict))

    # 1. PROCESS WINEPEDIA QUEUE
    log(f"Queue 1: WINEp3dIA Articles ({len(WINEPEDIA_TOPICS)} topics in catalog)")
    for i, topic in enumerate(WINEPEDIA_TOPICS, 1):
        if is_time_up():
            log("Time limit reached (>= 06:45 AM). Gracefully halting generator.")
            break

        if topic["id"] in existing_article_ids:
            continue

        start_t = time.time()
        log(f"[WINEp3dIA {i}/{len(WINEPEDIA_TOPICS)}] Generating '{topic['title']}'...")
        try:
            res = generate_winepedia_article(topic)
        except Exception as err:
            log(f"  -> ERROR during generation: {err}")
            res = None
        elapsed = time.time() - start_t

        if res and isinstance(res, dict) and "title_es" in res:
            generated_articles.append(res)
            existing_article_ids.add(topic["id"])
            save_checkpoint("winepedia_articles", generated_articles)
            log(f"  -> SUCCESS in {elapsed:.1f}s: '{res.get('title_es')}'")
        else:
            log(f"  -> WARNING: Failed to generate valid JSON for '{topic['title']}' ({elapsed:.1f}s)")
        
        # Polite 2s pause
        time.sleep(2)

    # 2. PROCESS STUDY CARDS QUEUE
    if not is_time_up():
        log(f"Queue 2: Study Cards ({len(STUDY_CARD_TOPICS)} cards in catalog)")
        for i, card_task in enumerate(STUDY_CARD_TOPICS, 1):
            if is_time_up():
                log("Time limit reached (>= 06:45 AM). Gracefully halting generator.")
                break

            card_id = f"card_{card_task['standard'].lower()}_{i:03d}"
            start_t = time.time()
            log(f"[CARDS {i}/{len(STUDY_CARD_TOPICS)}] Generating {card_task['standard']} card: '{card_task['topic']}'...")
            try:
                res = generate_study_card(card_task, i)
            except Exception as err:
                log(f"  -> ERROR during card generation: {err}")
                res = None
            elapsed = time.time() - start_t

            if res and isinstance(res, dict) and "question_es" in res:
                generated_cards.append(res)
                save_checkpoint("study_cards", generated_cards)
                log(f"  -> SUCCESS in {elapsed:.1f}s: Question generated.")
            else:
                log(f"  -> WARNING: Failed to generate valid card JSON ({elapsed:.1f}s)")
            
            time.sleep(2)

    # 3. PROCESS GRAPE PROFILES QUEUE
    if not is_time_up():
        log(f"Queue 3: Grape Varieties Enriched Profiles ({len(GRAPES_TO_ENRICH)} varieties in catalog)")
        for i, grape in enumerate(GRAPES_TO_ENRICH, 1):
            if is_time_up():
                log("Time limit reached (>= 06:45 AM). Gracefully halting generator.")
                break

            if grape in existing_grape_names:
                continue

            start_t = time.time()
            log(f"[GRAPES {i}/{len(GRAPES_TO_ENRICH)}] Generating profile for '{grape}'...")
            try:
                res = generate_grape_profile(grape)
            except Exception as err:
                log(f"  -> ERROR during grape profile: {err}")
                res = None
            elapsed = time.time() - start_t

            if res and isinstance(res, dict) and "profile" in res:
                generated_grapes.append(res)
                existing_grape_names.add(grape)
                save_checkpoint("grape_profiles", generated_grapes)
                log(f"  -> SUCCESS in {elapsed:.1f}s: '{grape}' profile ready.")
            else:
                log(f"  -> WARNING: Failed to generate profile for '{grape}' ({elapsed:.1f}s)")

            time.sleep(2)

    # FINAL REPORT COMPILATION
    now_end = datetime.now()
    log("==================================================")
    log("OVERNIGHT BATCH FINISHED")
    log(f"Finished at: {now_end.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Total WINEp3dIA Articles Generated: {len(generated_articles)}")
    log(f"Total Study Flashcards Generated: {len(generated_cards)}")
    log(f"Total Grape Profiles Generated: {len(generated_grapes)}")
    log("==================================================")

    # Generate Markdown Summary Report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 🍷 WINE³ai — Informe de Generación Nocturna (LM Studio)\n\n")
        f.write(f"- **Fecha y hora de finalización:** {now_end.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **Consumo de tokens en la nube:** **0 tokens** (100% inferencia local GPU en Apple M3 Pro)\n")
        f.write(f"- **Total artículos técnicos generados:** {len(generated_articles)}\n")
        f.write(f"- **Total fichas de examen generadas:** {len(generated_cards)}\n")
        f.write(f"- **Total perfiles de uvas generados:** {len(generated_grapes)}\n\n")
        
        f.write("## 1. Artículos Nuevos de WINEp3dIA\n\n")
        for a in generated_articles:
            f.write(f"- **{a.get('title_es', 'Sin título')}** (`{a.get('id', '')}`) — *{a.get('summary_es', '')}*\n")
            
        f.write("\n## 2. Flashcards de Examen Nuevas\n\n")
        for c in generated_cards:
            f.write(f"- **[{c.get('standard', '')}]** {c.get('question_es', '')}\n")
            
        f.write("\n## 3. Variedades de Uva Enriquecidas\n\n")
        for g in generated_grapes:
            f.write(f"- **{g.get('grape', '')}**: Acidez: {g.get('profile', {}).get('acidity', '')} | Tanino: {g.get('profile', {}).get('tannin', '')} | Maridaje: {', '.join(g.get('profile', {}).get('ideal_food_pairings', []))}\n")

    log(f"Executive report written to {REPORT_FILE}")

    # Compile into production data assets
    try:
        log("Auto-compiling generated content into production assets...")
        from scripts.compile_generated_data import main as compile_data
        compile_data()
        log("Compilation to production files completed successfully.")
    except Exception as e:
        log(f"Auto-compilation error: {e}")

if __name__ == "__main__":
    main()
