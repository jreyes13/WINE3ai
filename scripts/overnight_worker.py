#!/usr/bin/env python3
"""
WINE³ai — Overnight Autonomous Content Generator
Runs locally via LM Studio (http://localhost:1234) until 06:45 AM.
Generates high-precision, canonical enological content across:
  1. WINEp3dIA Articles (Soils, Vinifications, Vine Biology, Chemistry/Faults, Terroir)
  2. Sommelier Exam Flashcards (WSET 3, CMS Deductive, ASI Global, Diploma Cases)
  3. Grape Varieties Profiles (Tasting descriptors, Terroir, Molecular Pairings)

Prints on-screen for every card:
  - Card number / total
  - Card title and category
  - LM Studio tokens used (Prompt, Completion, Reasoning)
  - Time elapsed and running cumulative tokens
"""

import sys
import os
import json
import time
import re
from datetime import datetime, timedelta

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

# Cumulative counters
stats = {
    "total_generated": 0,
    "total_prompt_tokens": 0,
    "total_completion_tokens": 0,
    "total_reasoning_tokens": 0,
    "total_tokens": 0
}

def log(msg, to_file_only=False):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now_str}] {msg}"
    if not to_file_only:
        print(entry, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

FORCE_RUN = "--now" in sys.argv or "--force" in sys.argv or "--continue" in sys.argv

def is_time_up():
    if FORCE_RUN:
        return False
    now = datetime.now()
    # Graceful stop between 06:45 and 07:00 AM (or if it's already between 07:00 and 20:00)
    if now.hour == 6 and now.minute >= 45:
        return True
    if 7 <= now.hour < 20:
        return True
    return False

def get_target_cutoff():
    now = datetime.now()
    if FORCE_RUN:
        return "Modo continuo (--now / --force activo: finalizará al agotar catálogo)"
    if now.hour < 7:
        cutoff = now.replace(hour=6, minute=45, second=0, microsecond=0)
    else:
        cutoff = (now + timedelta(days=1)).replace(hour=6, minute=45, second=0, microsecond=0)
    return cutoff.strftime("%Y-%m-%d %H:%M:%S")

def extract_json(raw_text):
    if not raw_text:
        return None
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', raw_text)
    if match:
        raw_text = match.group(1)
    try:
        return json.loads(raw_text)
    except Exception:
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
# EXPANDED QUEUES OF CURATED TASKS
# ==========================================

WINEPEDIA_TOPICS = [
    # Suelos y Geología (20)
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
    {"id": "suelo_aluvial_grava_graves", "title": "Terrazas Aluviales y Gravas de Graves", "area": "Edafología", "focus": "Gravas cuarcíticas depositadas por el Garona, drenaje y maduración de Cabernet Sauvignon"},
    {"id": "suelo_pizarra_bierzo", "title": "Pizarras y Suelos de Ladera en el Bierzo", "area": "Edafología", "focus": "Estratificación de pizarras descompuestas en laderas altas y frescura mineral de la Mencía"},
    {"id": "suelo_flysch_txakoli", "title": "El Flysch Litoral y Areniscas del Cantábrico", "area": "Edafología", "focus": "Alternancia de rocas duras y blandas, alta pluviometría y drenaje en Getaria y Bizkaia"},
    {"id": "suelo_serpentinita_etna", "title": "Suelos Volcánicos del Monte Etna", "area": "Edafología", "focus": "Lavas volcánicas estratificadas de diferentes erupciones, altitud hasta 1.000m y Nerello Mascalese"},
    {"id": "suelo_caliza_paramo_ribera", "title": "Calizas del Páramo en Ribera del Duero", "area": "Edafología", "focus": "Horizontes calizos a más de 850m de altitud, oscilación térmica extrema y acidez en Fuentecén y Pesquera"},

    # Vinificaciones Especiales y Enología (25)
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
    {"id": "crianza_biologica_velo_flor", "title": "Crianza Biológica bajo Velo de Flor", "area": "Enología", "focus": "Levaduras Saccharomyces beticus/cheresiensis, consumo de glicerol y alcohol, síntesis de acetaldehído"},
    {"id": "fondillon_alicante_envejecimiento", "title": "Fondillón de Alicante y Vinos Rancios", "area": "Enología", "focus": "Sobremaduración en cepa de Monastrell, fermentación natural sin encabezar y más de 10 años en toneles monoveros"},
    {"id": "tanques_hormigon_deposito_huevo", "title": "Depósitos Ovoides de Hormigón y Vórtice", "area": "Enología", "focus": "Corrientes de convección continuas en forma de huevo, suspensión natural de lías y aislamiento térmico"},
    {"id": "delestage_vs_remontado_pigeage", "title": "Gestión del Sombrero: Délestage vs Remontado vs Pigeage", "area": "Enología", "focus": "Oxigenación de mosto, rotura del sombrero, dispersión térmica y extracción suave de color"},
    {"id": "maceracion_postfermentativa_caliente", "title": "Maceración Postfermentativa en Caliente", "area": "Enología", "focus": "Mantenimiento a 28-30°C post-fermentación alcohólica para polimerización tánica y redondez en boca"},
    {"id": "autolisis_champagne_manoproteinas", "title": "Cinética de la Autólisis en Vinos Espumosos", "area": "Enología", "focus": "Degradación celular tras 15-36 meses, liberación de aminoácidos, persistencia y finura de burbuja"},
    {"id": "pasteurizacion_flash_vs_filtracion", "title": "Estabilización Microbiológica: Filtración Tangencial vs Lenticular", "area": "Enología", "focus": "Porosidad en micras, retención de levaduras y bacterias sin despojar coloides protectores"},
    {"id": "vinos_dulces_naturales_encabezado", "title": "Vins Doux Naturels (VDN) y Mutage", "area": "Enología", "focus": "Adición de alcohol neutro a 96% durante fermentación (mutage sur grain) en Roussillon y Banyuls"},
    {"id": "acidificacion_vs_desacidificacion", "title": "Corrección de Acidez en Mosto y Vino", "area": "Enología", "focus": "Adición de ácido tartárico en climas cálidos vs precipitación de bitartratos con carbonato potásico"},
    {"id": "clarificacion_vegana_proteinas", "title": "Clarificación con Proteínas Vegetales vs Enológicas Clásicas", "area": "Enología", "focus": "Proteína de guisante y patata vs albúmina de huevo e ictiocola, afinidad electrostática con taninos"},

    # Fisiología de la Vid, Bioquímica y Defectos (25)
    {"id": "ciclo_vegetativo_vid_fenologia", "title": "Ciclo Biológico Anual de la Vid", "area": "Viticultura", "focus": "Lloro, desborre, floración, cuajado, envero, maduración fenólica y parada invernal"},
    {"id": "sistemas_conduccion_guyot_gobelet", "title": "Sistemas de Conducción: Vaso vs Guyot vs Espaldera", "area": "Viticultura", "focus": "Gestión del dosel vegetal (canopy management), sombreo, exposición fotosintética y mecanización"},
    {"id": "pie_franco_vs_portainjertos_filoxera", "title": "Patrones Porta-injertos y Filoxera", "area": "Viticultura", "focus": "Daktulosphaira vitifoliae, cruces con Vitis riparia y rupestris, adaptación a caliza y sequía"},
    {"id": "estres_hidrico_fotosintesis_taninos", "title": "Déficit Hídrico Controlado (RDI)", "area": "Viticultura", "focus": "Potencial hídrico en hoja, inhibición del crecimiento vegetativo y síntesis de polifenoles"},
    {"id": "pirazinas_verdor_cabernet", "title": "Metoxipirazinas y Madurez de la Uva", "area": "Bioquímica", "focus": "3-isobutil-2-metoxipiracina (IBMP), aroma a pimiento verde en Cabernet Sauvignon y Sauvignon Blanc"},
    {"id": "rotundona_pimienta_syrah", "title": "Rotundona: El Sesquiterpeno de la Pimienta Negra", "area": "Bioquímica", "focus": "Umbral de percepción bajísimo en Syrah/Shiraz y Grüner Veltliner en climas frescos"},
    {"id": "esteres_fermentacion_tioles", "title": "Tioles Volátiles: Fruta Tropical y Boj", "area": "Bioquímica", "focus": "Precursores cisteínicos en Sauvignon Blanc y Verdejo (3MHA, 3MH, 4MMP), aromas de maracuyá"},
    {"id": "oidio_vs_mildiu_hongos", "title": "Mildiu (Plasmopara) vs Oídio (Uncinula)", "area": "Sanidad Vegetal", "focus": "Manchas de aceite y pelusa blanca, condiciones de 10-10-10, tratamientos con cobre y azufre"},
    {"id": "enfermedades_madera_yesca", "title": "Enfermedades de Madera: Yesca y Eutiosis", "area": "Sanidad Vegetal", "focus": "Hongos vasculares, apoplejía de la vid, corte y desinfección en poda de respeto"},
    {"id": "seleccion_masal_vs_clonal", "title": "Selección Masal vs Selección Clonal", "area": "Viticultura", "focus": "Preservación de biodiversidad genética varietal frente a uniformidad sanitaria y productiva"},
    {"id": "defecto_brettanomyces_fenoles", "title": "Brettanomyces: 4-Etilfenol y 4-Etilguayacol", "area": "Defectos", "focus": "Notas de establo, sudor de caballo y cuero rancio; factores de SO2 libre, pH y temperatura"},
    {"id": "defecto_reduccion_h2s_mercaptanos", "title": "Reducción de Azufre: Sulfhídrico y Mercaptanos", "area": "Defectos", "focus": "H2S (huevos podridos), metanotiol y etanotiol; choque con cobre y prevención en fermentación"},
    {"id": "defecto_tca_corcho_anisoles", "title": "Tricloroanisol (TCA) y Contaminación de Corcho", "area": "Defectos", "focus": "2,4,6-Tricloroanisol, umbral de detección en nanogramos, enmascaramiento frutal y humedad"},
    {"id": "defecto_acidez_volatil_acetato", "title": "Acidez Volátil: Ácido Acético y Acetato de Etilo", "area": "Defectos", "focus": "Bacterias acéticas (Acetobacter), aromas a vinagre y pegamento/disolvente, límites legales"},
    {"id": "defecto_oxidacion_acetaldehido", "title": "Oxidación Prematura (Premox) y Acetaldehído", "area": "Defectos", "focus": "Pérdida de SO2 molecular, pardeamiento enzimático, notas de manzana oxidada y barniz"},
    {"id": "defecto_mousiness_picado_raton", "title": "Mousiness (Sabor a Ratón / Goût de Souris)", "area": "Defectos", "focus": "Tetrahidropiridinas producidas por Brettanomyces y bacterias lácticas con pH salival alto"},
    {"id": "terpenos_aroma_moscatel_riesling", "title": "Terpenos: Linalool, Geraniol y Nerol", "area": "Bioquímica", "focus": "Moléculas aromáticas florales libres y glicosiladas en Moscatel, Gewürztraminer y Riesling"},
    {"id": "antocianos_copigmentacion_color", "title": "Antocianos y Fenómeno de Copigmentación", "area": "Bioquímica", "focus": "Malvidina, petunidina y peonidina; estabilización con flavonoides y taninos condensados"},
    {"id": "portainjertos_sequia_110r_1103p", "title": "Portainjertos para Sequía y Caliza: 110 Richter y 1103 Paulsen", "area": "Viticultura", "focus": "Raíz profunda, vigor radicular y compatibilidad con sequías prolongadas del cambio climático"},
    {"id": "poda_respeto_simonit_sirch", "title": "Poda de Respeto y Flujo de Savia (Método Simonit & Sirch)", "area": "Viticultura", "focus": "Ramificación controlada, conos de desecación pequeños y longevidad en cepas viejas"},
    {"id": "viticultura_biodinamica_preparados", "title": "Principios Biodinámicos: Preparados 500 y 501", "area": "Viticultura", "focus": "Sílice de cuerno y estiércol fermentado, influencia lunar y certificación Demeter"},
    {"id": "climas_viticolas_huglin_winkler", "title": "Índices Bioclimáticos de Winkler y Huglin", "area": "Climatología", "focus": "Grados-día acumulados, clasificación térmica de regiones del mundo para aptitud varietal"},
    {"id": "matorrales_aromaticos_garriga", "title": "Aromas de Garriga, Tomillar y Maquia", "area": "Terruño", "focus": "Deposición aérea de aceites esenciales volátiles de romero, jara y tomillo sobre la pruina"},
    {"id": "polifenoles_ipt_indice_madurez", "title": "Índice de Polifenoles Totales (IPT) y Madurez Fenólica", "area": "Enología", "focus": "Absorbancia a 280 nm, cata de hollejos y pepitas para fijar la fecha óptima de vendimia"},
    {"id": "geosmina_tierra_humeda_botrytis", "title": "Geosmina y Hongos Parásitos en Vendimia", "area": "Sanidad Vegetal", "focus": "Penicillium expansum y Botrytis en vendimias lluviosas, olor a remolacha y tierra mojada"}
]

STUDY_CARD_TOPICS = [
    # WSET 3: Factores Naturales, Regiones y Estilos (30)
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
    {"standard": "WSET3", "category": "Regiones de Italia", "topic": "Diferencias de suelo de Barolo (Helveciano vs Tortoniano) y su impacto en taninos de Nebbiolo"},
    {"standard": "WSET3", "category": "Regiones de Italia", "topic": "Método Ripasso en Valpolicella: pase sobre orujos calientes de Amarone y re-fermentación"},
    {"standard": "WSET3", "category": "Regiones de Francia", "topic": "La jerarquía de Borgoña: Regional, Comunal (Village), Premier Cru y Grand Cru"},
    {"standard": "WSET3", "category": "Regiones de Francia", "topic": "El Mistral en el Valle del Ródano: reducción de enfermedades fúngicas y estrés en espalderas"},
    {"standard": "WSET3", "category": "Vinos Espumosos", "topic": "Estilos de Champagne: Blanc de Blancs, Blanc de Noirs, Rosé d'assemblage y Millésimé"},
    {"standard": "WSET3", "category": "Vinos Espumosos", "topic": "El papel del licor de expedición (dosage) y categorías desde Brut Nature hasta Doux"},
    {"standard": "WSET3", "category": "Regiones de Portugal", "topic": "Las tres subregiones del Douro: Baixo Corgo, Cima Corgo y Douro Superior"},
    {"standard": "WSET3", "category": "Regiones de Portugal", "topic": "Oporto Ruby vs Tawny: diferencias de crianza reductiva en gran tonel vs oxidativa en pipa"},
    {"standard": "WSET3", "category": "Nuevo Mundo", "topic": "La corriente de Humboldt en Chile: por qué valles como Casablanca producen vinos de clima frío"},
    {"standard": "WSET3", "category": "Nuevo Mundo", "topic": "Altitud en Salta (Cafayate, Argentina): radiación UV, grosor del hollejo y Torrontés aromático"},
    {"standard": "WSET3", "category": "Nuevo Mundo", "topic": "Gimblett Gravels en Hawke's Bay (Nueva Zelanda): acumulación térmica y Syrah/Bordeaux blends"},
    {"standard": "WSET3", "category": "Nuevo Mundo", "topic": "Efecto moderador de los Grandes Lagos en Niágara (Canadá) para la producción de Icewine"},
    {"standard": "WSET3", "category": "Regiones de España", "topic": "Priorat: laderas escarpadas (costers), suelos de llicorella y Garnacha/Cariñena vieja"},
    {"standard": "WSET3", "category": "Regiones de España", "topic": "Rueda y Verdejo: vendimia nocturna a baja temperatura para preservar tioles volátiles"},
    {"standard": "WSET3", "category": "Regiones de España", "topic": "Rías Baixas: sistema de conducción en parral (pergola) para alejar uvas de la humedad del suelo"},
    {"standard": "WSET3", "category": "Regiones de España", "topic": "Cava: variedades autóctonas Macabeo, Xarel·lo y Parellada y crianza mínima en rima"},
    {"standard": "WSET3", "category": "Enología de Fortificados", "topic": "Madeira y el proceso de Estufagem vs Canteiro: imitación térmica de las travesías ecuatoriales"},
    {"standard": "WSET3", "category": "Enología de Fortificados", "topic": "El sistema de Criaderas y Soleras: homogeneidad, vejez media calculada y tasa de saca"},

    # CMS Deductive Tasting & Sommelier (30)
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
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata deductiva de Chardonnay: Chablis vs Puligny-Montrachet vs Napa Valley oaked"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Identificación en copa de Tempranillo clásico de Rioja (roble americano/eneldo) vs Ribera del Duero moderna"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata ciega de Gamay de Beaujolais Cru (Morgon) vs Pinot Noir de Village de Borgoña"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Deducción de Malbec de Mendoza (altitud) vs Malbec de Cahors (tánico y rústico)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Identificación de Chenin Blanc de Vouvray (seco/semiseco) vs Riesling del Rheingau"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata deductiva de Albariño de Rías Baixas vs Grüner Veltliner de Wachau"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Identificación de Zinfandel de California vs Primitivo de Manduria: alcohol, madurez y especias"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata ciega de Carmenère de Colchagua vs Merlot de Burdeos margen derecha"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje con alcachofas y espárragos: el compuesto cinarina y la elección de vinos herbáceos o Jerez"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Armonía para cordero lechal asado: taninos firmes, acidez viva y Tempranillo de Ribera del Duero"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje para foie gras mi-cuit: por qué el ácido de un vino dulce botritizado equilibra los lípidos"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje de contraste vs afinidad: postres de frutos rojos con Brachetto d'Acqui o Recioto"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Apertura ceremonial de botellas de espumoso sin ruido de estampido (le soupir de la dame)"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Gestión del servicio de maridaje por copas en un menú degustación de 9 pases"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Identificación de la acescencia y cómo distinguirla de la alta acidez tartárica de un vino joven"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Turbidez bacteriana vs posos naturales de materia colorante: diagnóstico visual"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Diferenciación de añadas cálidas vs frías mediante el análisis del alcohol y la fruta confitada"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Oxigenación en decantador: vinos que mejoran vs vinos ancianos frágiles que colapsan"},

    # ASI Global Sommelier Standards (30)
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
    {"standard": "ASI", "category": "Vinos del Mundo", "topic": "La corriente fría de Humboldt y su impacto en los valles costeros de Chile (Casablanca, San Antonio)"},
    {"standard": "ASI", "category": "Vinos del Mundo", "topic": "Vinos de Grecia: el terroir de Santorini, suelo de pumita y sistema de conducción kouloura en canasta"},
    {"standard": "ASI", "category": "Vinos del Mundo", "topic": "Vinos de Hungría: Tokaji Aszú, el suelo volcánico de Zemplén y la variedad Furmint"},
    {"standard": "ASI", "category": "Vinos del Mundo", "topic": "Vinos de Austria: Grüner Veltliner en Kamptal y Kremstal, y los Riesling de terrazas del Danubio"},
    {"standard": "ASI", "category": "Vinos del Mundo", "topic": "El Líbano y el Valle de la Becá: altitud a 1.000m, viñedos de Château Musar y Cinsault/Cabernet"},
    {"standard": "ASI", "category": "Vinos del Mundo", "topic": "Viticultura en Japón (Koshu en Yamanashi): suelos volcánicos, sombrillas de papel contra la lluvia"},
    {"standard": "ASI", "category": "Armonía y Gastronomía Global", "topic": "Maridaje con quesos de pasta blanda y corteza enmohecida (Brie, Camembert): sidra, Champagne o tinto ligero"},
    {"standard": "ASI", "category": "Armonía y Gastronomía Global", "topic": "Maridaje con caviar de esturión: Champagne Extra Brut vs Vodka helado tradicional"},
    {"standard": "ASI", "category": "Armonía y Gastronomía Global", "topic": "Maridaje para platos con trufa negra (Tuber melanosporum): terciarios de Barolo maduro o Rioja Gran Reserva"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Protocolo para la preparación y servicio de un cóctel clásico en la mesa de sumiller (Dry Martini / Negroni)"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Identificación de aguas minerales (mineralización débil, media, fuerte) y su armonía con vinos"},
    {"standard": "ASI", "category": "Legislación & Normativa", "topic": "La nueva pirámide de calidad en Rioja: Vinos de Zona, Vinos de Municipio y Viñedos Singulares"},
    {"standard": "ASI", "category": "Legislación & Normativa", "topic": "La clasificación de Priorat: Vi de Vila, Vi de Paratge, Vinya Classificada y Gran Vinya Classificada"},
    {"standard": "ASI", "category": "Legislación & Normativa", "topic": "El sistema DOCG en Italia: requisitos de rendimiento, comités de cata y precintos estatales"},
    {"standard": "ASI", "category": "Enología & Cata", "topic": "Evolución cromática del vino: de violáceo a teja en tintos, y de amarillo pajizo a ámbar en blancos"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Gestión de quejas de temperatura en sala: cómo enfriar una botella de tinto sobrecalentada en minutos"},
    {"standard": "ASI", "category": "Armonía y Gastronomía Global", "topic": "Cocina tailandesa e india con leche de coco y especias: armonía con Gewürztraminer o Riesling Spätlese"},
    {"standard": "ASI", "category": "Vinos del Mundo", "topic": "China (Ningxia, Helan Mountain): clima continental extremo, enterramiento invernal de cepas"},
    {"standard": "ASI", "category": "Protocolo de Sala & Deontología", "topic": "Gestión de la bodega del restaurante: rotación de stock, control de humedad (70%) y vibraciones"}
]

GRAPES_TO_ENRICH = [
    # Tintas Españolas Autóctonas y Tradicionales (25)
    "Tempranillo", "Garnacha", "Mencia", "Bobal", "Monastrell", 
    "Graciano", "Carignan", "Prieto Picudo", "Rufete", "Juan Garcia",
    "Souson", "Brancellao", "Caino Tinto", "Espadeiro", "Listan Negro",
    "Negramoll", "Baboso Negro", "Vijariego Negro", "Tintilla de Rota", "Maturana Tinta",
    "Garnacha Tintorera", "Garnacha Peluda", "Callet", "Fogoneu", "Manto Negro",

    # Blancas Españolas Autóctonas y Tradicionales (25)
    "Albarino", "Verdejo", "Godello", "Treixadura", "Loureira",
    "Caino Blanco", "Torrontes Iberico", "Palomino Fino", "Pedro Ximenez", "Macabeo",
    "Xarello", "Parellada", "Garnacha Blanca", "Albillo Mayor", "Albillo Real",
    "Malvasia Volcanica", "Malvasia Aromatica", "Hondarrabi Zuri", "Albarin Blanco", "Dona Blanca",
    "Listan Blanco", "Vijariego Blanco", "Prensal Blanc", "Giro Ros", "Merseguera",

    # Tintas Internacionales Emblemáticas (30)
    "Cabernet Sauvignon", "Merlot", "Pinot Noir", "Syrah", "Nebbiolo",
    "Sangiovese", "Malbec", "Cabernet Franc", "Gamay", "Mourvedre",
    "Touriga Nacional", "Touriga Franca", "Barbera", "Carmenere", "Tannat",
    "Pinotage", "Zinfandel", "Corvina", "Rondinella", "Aglianico",
    "Nero d Avola", "Nerello Mascalese", "Primitivo", "Baga", "Blaufraenkisch",
    "Zweigelt", "Saperavi", "Xinomavro", "Agiorgitiko", "Petit Verdot",

    # Blancas Internacionales Emblemáticas (30)
    "Chardonnay", "Sauvignon Blanc", "Riesling", "Chenin Blanc", "Viognier",
    "Semillon", "Gewurztraminer", "Pinot Gris", "Gruner Veltliner", "Assyrtiko",
    "Furmint", "Glera", "Marsanne", "Roussanne", "Melon de Bourgogne",
    "Savagnin", "Aligote", "Garganega", "Cortese", "Verdicchio",
    "Fiano", "Greco di Tufo", "Vermentino", "Carricante", "Moschofilero",
    "Harlevelu", "Torrontes Riojano", "Pinot Blanc", "Silvaner", "Muller-Thurgau"
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

    raw, usage = query_lm(
        prompt, 
        system_prompt="Eres un Master Sommelier y enólogo doctorado. Mantén tu razonamiento interno breve y conciso (máximo 250 palabras). Responde única y exclusivamente con el JSON solicitado.",
        max_tokens=5000,
        return_usage=True
    )
    return extract_json(raw), usage

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

    raw, usage = query_lm(
        prompt, 
        system_prompt="Eres examinador oficial de Master Sommelier y WSET Diploma. Razonamiento interno breve y conciso (máximo 250 palabras). Responde exclusivamente con el JSON.",
        max_tokens=5000,
        return_usage=True
    )
    return extract_json(raw), usage

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

    raw, usage = query_lm(
        prompt, 
        system_prompt="Eres un ampelógrafo y Master of Wine. Razonamiento interno breve y conciso (máximo 200 palabras). Responde exclusivamente con el JSON.",
        max_tokens=5000,
        return_usage=True
    )
    return extract_json(raw), usage

def print_card_banner(idx, total_in_catalog, title, category, elapsed, usage, success=True):
    pt = usage.get("prompt_tokens", 0)
    ct = usage.get("completion_tokens", 0)
    tt = usage.get("total_tokens", 0)
    rt = usage.get("reasoning_tokens", 0)

    stats["total_prompt_tokens"] += pt
    stats["total_completion_tokens"] += ct
    stats["total_tokens"] += tt
    stats["total_reasoning_tokens"] += rt
    if success:
        stats["total_generated"] += 1

    sep = "─" * 78
    status_str = f"✓ ÉXITO ({elapsed:.1f}s)" if success else f"⚠️ FALLO / REINTENTO ({elapsed:.1f}s)"
    
    print(f"\n{sep}", flush=True)
    print(f"📦 [FICHA #{idx}/{total_in_catalog}] {title} [{category}]", flush=True)
    print(f"   Estado: {status_str}", flush=True)
    print(f"   📊 Tokens LM Studio : {tt:,} tokens (Prompt: {pt:,} | Gen: {ct:,} | Razonamiento: {rt:,})", flush=True)
    print(f"   📈 Acumulado noche  : {stats['total_tokens']:,} tokens locales | Generadas: {stats['total_generated']}", flush=True)
    print(f"{sep}\n", flush=True)

# ==========================================
# MAIN OVERNIGHT WORKER LOOP
# ==========================================

def main():
    start_time = datetime.now()
    cutoff_str = get_target_cutoff()

    total_catalog = len(WINEPEDIA_TOPICS) + len(STUDY_CARD_TOPICS) + len(GRAPES_TO_ENRICH)

    print("\n" + "=" * 78, flush=True)
    print("🍷 WINE³ai — GENERADOR AUTÓNOMO LOCAL CON LM STUDIO (OFFLINE)", flush=True)
    print("=" * 78, flush=True)
    print(f"⏰ HORA DE INICIO           : {start_time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print(f"🛑 FINALIZACIÓN PROGRAMADA : {cutoff_str}", flush=True)
    print(f"💻 MOTOR LOCAL             : LM Studio (http://localhost:1234/v1) · qwen/qwen3.5-9b", flush=True)
    print(f"⚡ ACELERACIÓN              : Apple Metal GPU (Inferencia Local en Mac)", flush=True)
    print(f"💰 CONSUMO EN NUBE         : 0 tokens (100% gratuito y privado)", flush=True)
    print(f"📋 CATÁLOGO DISPONIBLE     : {total_catalog} fichas en cola:", flush=True)
    print(f"   ├─ WINEp3dIA Articles   : {len(WINEPEDIA_TOPICS)} artículos enciclopédicos", flush=True)
    print(f"   ├─ Study Flashcards     : {len(STUDY_CARD_TOPICS)} fichas de examen (WSET 3, CMS, ASI)", flush=True)
    print(f"   └─ Grape Varieties      : {len(GRAPES_TO_ENRICH)} variedades de uva mundiales", flush=True)
    print("=" * 78 + "\n", flush=True)

    log(f"Starting worker. Target cutoff: {cutoff_str}. Total catalog: {total_catalog} items.", to_file_only=True)

    generated_articles = []
    generated_cards = []
    generated_grapes = []

    # Load existing generated checkpoints
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
    existing_card_ids = set(c.get("id") for c in generated_cards if isinstance(c, dict))
    existing_grape_names = set(g.get("grape") for g in generated_grapes if isinstance(g, dict))

    current_item_counter = 0

    # 1. PROCESS WINEPEDIA QUEUE
    print(f"▶ INICIANDO COLA 1: WINEp3dIA ({len(WINEPEDIA_TOPICS)} artículos)...", flush=True)
    for topic in WINEPEDIA_TOPICS:
        current_item_counter += 1
        if is_time_up():
            log("Time limit reached (06:45 AM). Gracefully halting generator.")
            break

        if topic["id"] in existing_article_ids:
            continue

        start_t = time.time()
        try:
            res, usage = generate_winepedia_article(topic)
        except Exception as err:
            res, usage = None, {}

        elapsed = time.time() - start_t

        if res and isinstance(res, dict) and "title_es" in res:
            generated_articles.append(res)
            existing_article_ids.add(topic["id"])
            save_checkpoint("winepedia_articles", generated_articles)
            print_card_banner(current_item_counter, total_catalog, topic['title'], "WINEp3dIA", elapsed, usage, success=True)
        else:
            print_card_banner(current_item_counter, total_catalog, topic['title'], "WINEp3dIA", elapsed, usage, success=False)
        
        time.sleep(2)

    # 2. PROCESS STUDY CARDS QUEUE
    if not is_time_up():
        print(f"\n▶ INICIANDO COLA 2: Flashcards de Examen ({len(STUDY_CARD_TOPICS)} temas)...", flush=True)
        for i, card_task in enumerate(STUDY_CARD_TOPICS, 1):
            current_item_counter += 1
            if is_time_up():
                log("Time limit reached (06:45 AM). Gracefully halting generator.")
                break

            card_id = f"card_{card_task['standard'].lower()}_{i:03d}"
            if card_id in existing_card_ids:
                continue

            start_t = time.time()
            try:
                res, usage = generate_study_card(card_task, i)
            except Exception as err:
                res, usage = None, {}

            elapsed = time.time() - start_t

            if res and isinstance(res, dict) and "question_es" in res:
                generated_cards.append(res)
                existing_card_ids.add(card_id)
                save_checkpoint("study_cards", generated_cards)
                print_card_banner(current_item_counter, total_catalog, card_task['topic'], f"{card_task['standard']} Exam", elapsed, usage, success=True)
            else:
                print_card_banner(current_item_counter, total_catalog, card_task['topic'], f"{card_task['standard']} Exam", elapsed, usage, success=False)
            
            time.sleep(2)

    # 3. PROCESS GRAPE PROFILES QUEUE
    if not is_time_up():
        print(f"\n▶ INICIANDO COLA 3: Perfiles de Variedades de Uva ({len(GRAPES_TO_ENRICH)} variedades)...", flush=True)
        for grape in GRAPES_TO_ENRICH:
            current_item_counter += 1
            if is_time_up():
                log("Time limit reached (06:45 AM). Gracefully halting generator.")
                break

            if grape in existing_grape_names:
                continue

            start_t = time.time()
            try:
                res, usage = generate_grape_profile(grape)
            except Exception as err:
                res, usage = None, {}

            elapsed = time.time() - start_t

            if res and isinstance(res, dict) and "profile" in res:
                generated_grapes.append(res)
                existing_grape_names.add(grape)
                save_checkpoint("grape_profiles", generated_grapes)
                print_card_banner(current_item_counter, total_catalog, grape, "Variedad de Uva", elapsed, usage, success=True)
            else:
                print_card_banner(current_item_counter, total_catalog, grape, "Variedad de Uva", elapsed, usage, success=False)

            time.sleep(2)

    # FINAL REPORT COMPILATION
    now_end = datetime.now()
    duration = now_end - start_time

    print("\n" + "=" * 78, flush=True)
    print("🎉 GENERACIÓN NOCTURNA COMPLETADA CON ÉXITO", flush=True)
    print("=" * 78, flush=True)
    print(f"⏰ HORA DE FINALIZACIÓN       : {now_end.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print(f"⏱️ TIEMPO TOTAL TRANSCURRIDO  : {str(duration).split('.')[0]}", flush=True)
    print(f"📋 FICHAS NUEVAS GENERADAS     : {stats['total_generated']}", flush=True)
    print(f"   ├─ Artículos WINEp3dIA      : {len(generated_articles)} acumulados", flush=True)
    print(f"   ├─ Flashcards de Estudio    : {len(generated_cards)} acumuladas", flush=True)
    print(f"   └─ Perfiles de Uva          : {len(generated_grapes)} acumulados", flush=True)
    print(f"📊 TOKENS LM STUDIO INVERTIDOS : {stats['total_tokens']:,} tokens locales", flush=True)
    print(f"   ├─ Prompt tokens            : {stats['total_prompt_tokens']:,}", flush=True)
    print(f"   ├─ Generation tokens        : {stats['total_completion_tokens']:,}", flush=True)
    print(f"   └─ Reasoning (Pensamiento)  : {stats['total_reasoning_tokens']:,}", flush=True)
    print(f"💰 GASTO EN LA NUBE            : 0€ (0 tokens externos consumidos)", flush=True)
    print("=" * 78 + "\n", flush=True)

    # Generate Markdown Summary Report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 🍷 WINE³ai — Informe de Generación Nocturna (LM Studio)\n\n")
        f.write(f"- **Fecha y hora de finalización:** {now_end.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **Consumo de tokens en la nube:** **0 tokens** (100% inferencia local GPU en Apple Silicon)\n")
        f.write(f"- **Total tokens procesados localmente:** **{stats['total_tokens']:,} tokens**\n")
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

    log(f"Executive report written to {REPORT_FILE}", to_file_only=True)

    # Compile into production data assets
    try:
        print("⚡ Compilando automáticamente en los ficheros de producción de WINE³ai...", flush=True)
        from scripts.compile_generated_data import main as compile_data
        compile_data()
        print("✓ Compilación a ficheros de producción completada con éxito.", flush=True)
    except Exception as e:
        print(f"⚠️ Error en compilación automática: {e}", flush=True)

if __name__ == "__main__":
    main()
