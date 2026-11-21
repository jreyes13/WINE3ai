#!/usr/bin/env python3
"""
WINE³ai — Overnight Autonomous Content Generator
Runs locally via LM Studio (http://localhost:1234).
Generates high-precision, canonical enological content across:
  1. WINEp3dIA Articles (Soils, Vinifications, Vine Biology, Chemistry/Faults, Terroir)
  2. Sommelier Exam Flashcards (WSET 3, CMS Deductive, ASI Global, MW/Diploma cases)
  3. Grape Varieties Profiles (Tasting descriptors, Terroir, Molecular Pairings)

Command Line Options:
  --start HH:MM   Start time (defaults to right now)
  --end   HH:MM   End time (e.g. 06:45)
  --hours N       Duration in hours (defaults to 3h if neither --end nor --hours is set)
"""

import sys
import os
import json
import time
import re
import platform
import argparse
from datetime import datetime, timedelta

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

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
# 450+ CURATED TOPICS (MAXIMUM YIELD)
# ==========================================

WINEPEDIA_TOPICS = [
    # Suelos y Geología (30)
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
    {"id": "suelo_caliza_alberese_toscana", "title": "Caliza Alberese y Galestro en Chianti", "area": "Edafología", "focus": "Margas arcillosas laminadas (Galestro) y caliza densa (Alberese), estructura del Sangiovese"},
    {"id": "suelo_toba_volcanica_campania", "title": "Toba Volcánica de Campania e Irpinia", "area": "Edafología", "focus": "Cenizas piroclásticas compactadas del Vesubio, mineralidad de Greco di Tufo y Fiano"},
    {"id": "suelo_pizarras_azules_mosela", "title": "Pizarra Devónica Azul del Valle del Mosela", "area": "Edafología", "focus": "Pizarras laminares que retienen calor solar y aportan acidez cortante al Riesling"},
    {"id": "suelo_grewacke_marlborough", "title": "Grava Aluvial Greywacke de Marlborough", "area": "Edafología", "focus": "Piedras fluviales redondeadas de arenisca metamórfica en el valle de Wairau"},
    {"id": "suelo_pedernal_sancerre_caillottes", "title": "Terres Blanches, Caillottes y Silex en Sancerre", "area": "Edafología", "focus": "Los tres terruños geológicos de Sancerre y su impacto en la aromática del Sauvignon Blanc"},
    {"id": "suelo_arcillo_calcario_bairrada", "title": "Arcillas Calcáreas de Bairrada", "area": "Edafología", "focus": "Suelos densos y frescos que modulan los taninos austeros de la Baga tradicional"},
    {"id": "suelo_arenas_doradas_toro", "title": "Arenas Silíceas y Cantos Rodados de Toro", "area": "Edafología", "focus": "Viñedos centenarios en pie franco a 700m de altitud y concentración tánica de Tinta de Toro"},
    {"id": "suelo_greda_pumita_santorini", "title": "Pumita y Ceniza Volcánica de Santorini", "area": "Edafología", "focus": "Suelos asfícticos hiper-porosos sin materia orgánica, resistencia a filoxera y Assyrtiko"},
    {"id": "suelo_granito_arribes_duero", "title": "Batolito Granítico de los Arribes del Duero", "area": "Edafología", "focus": "Terrazas vertiginosas de granito sobre el cañón del Duero, Juan García y Rufete"},
    {"id": "suelo_yesos_calizos_madrid", "title": "Suelos Yesíferos y Calizos de Vinos de Madrid", "area": "Edafología", "focus": "Subzona de Arganda sobre vegas aluviales y margas yesíferas, Tempranillo y Malvar"},

    # Vinificaciones Especiales y Enología (40)
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
    {"id": "filtracion_tangencial_vs_lenticular", "title": "Estabilización Microbiológica: Filtración Tangencial vs Lenticular", "area": "Enología", "focus": "Porosidad en micras, retención de levaduras y bacterias sin despojar coloides protectores"},
    {"id": "vinos_dulces_naturales_encabezado", "title": "Vins Doux Naturels (VDN) y Mutage", "area": "Enología", "focus": "Adición de alcohol neutro a 96% durante fermentación (mutage sur grain) en Roussillon y Banyuls"},
    {"id": "acidificacion_vs_desacidificacion", "title": "Corrección de Acidez en Mosto y Vino", "area": "Enología", "focus": "Adición de ácido tartárico en climas cálidos vs precipitación de bitartratos con carbonato potásico"},
    {"id": "clarificacion_vegana_proteinas", "title": "Clarificación con Proteínas Vegetales vs Enológicas Clásicas", "area": "Enología", "focus": "Proteína de guisante y patata vs albúmina de huevo e ictiocola, afinidad electrostática con taninos"},
    {"id": "fermentacion_espontanea_indigenas", "title": "Fermentación Espontánea con Levaduras Indígenas", "area": "Enología", "focus": "Sucesión ecológica: Kloeckera/Hanseniaspora inicial seguida de cepas nativas de Saccharomyces"},
    {"id": "termo_vinificacion_termomaceracion", "title": "Termovinificación y Flash-Détente", "area": "Enología", "focus": "Calentamiento rápido a 70-80°C y vacío instantáneo para extracción de color sin taninos astringentes"},
    {"id": "uso_fudres_toneles_gran_volumen", "title": "Crianza en Foudres y Botti de Gran Capacidad", "area": "Enología", "focus": "Volúmenes de 2.000 a 5.000 litros, mínima cesión de tanino maderero y microoxigenación lenta"},
    {"id": "crianza_submarina_presion_luz", "title": "Crianza Submarina de Vinos", "area": "Enología", "focus": "Presión hiperbárica marina, ausencia total de luz y oscilación térmica constante bajo el mar"},
    {"id": "desalcoholizacion_columna_conos", "title": "Desalcoholización: Columnas de Conos Rotatorios (SCC)", "area": "Enología", "focus": "Destilación a bajo vacío y baja temperatura para separar aromas volátiles antes de extraer etanol"},
    {"id": "glicerol_cuerpo_fermentacion", "title": "Síntesis de Glicerol durante la Fermentación", "area": "Bioquímica", "focus": "Vía gliceropirúvica de Saccharomyces, sensación de untuosidad y dulzor aparente sin azúcar residual"},
    {"id": "hiperoxidacion_mostos_blancos", "title": "Hiperoxidación de Mostos Blancos", "area": "Enología", "focus": "Saturación intencionada de O2 antes de fermentar para precipitar polifenoles oxidables y estabilizar color"},
    {"id": "levaduras_no_saccharomyces", "title": "Uso de Levaduras No-Saccharomyces en Co-Inoculación", "area": "Enología", "focus": "Torulaspora delbrueckii, Lachancea thermotolerans (ácido láctico) y Metschnikowia pulcherrima"},
    {"id": "taninos_enologicos_adicion", "title": "Taninos Enológicos: Gálicos, Elágicos y Proantocianídicos", "area": "Enología", "focus": "Protección antioxidante en vendimia, fijación de materia colorante y estructura de boca"},
    {"id": "estabilizacion_tartarica_carboximetilcelulosa", "title": "Estabilización Tartárica: CMC, Poliaspartato y Frío", "area": "Enología", "focus": "Inhibición de nucleación de cristales de bitartrato potásico mediante coloides protectores"},
    {"id": "vino_de_paja_passerillage", "title": "Vin de Paille y Passerillage sur Souche", "area": "Enología", "focus": "Pasificación sobre paja en Jura y pasificación natural en cepa en Monbazillac y Jurançon"},
    {"id": "sulfitos_so2_libre_molecular", "title": "El SO2 Molecular y el pH del Vino", "area": "Bioquímica", "focus": "Fracción activa antimicrobiana del sulfuroso en función del pH logarítmico del vino"},
    {"id": "espumosos_petnat_metodo_ancestral", "title": "Pét-Nat y el Método Ancestral", "area": "Enología", "focus": "Embotellado a mitad de la fermentación primaria sin tiraje, sin degüelle y con sedimento de lías"},
    {"id": "maceracion_pelicular_frio_blancos", "title": "Maceración Pelicular en Frío para Blancos Aromáticos", "area": "Enología", "focus": "Contacto de mosto con hollejos a 10°C durante 6-18h para extraer aromas terpénicos y tiólicos"},
    {"id": "barricas_tostado_ligero_medio_fuerte", "title": "Grados de Tostado en Barricas de Roble", "area": "Enología", "focus": "Tostado ligero (notas florales/frescas) vs medio (vainilla/especias) vs fuerte (humo/café/furfural)"},

    # Fisiología, Bioquímica, Clima y Defectos (50)
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
    {"id": "geosmina_tierra_humeda_botrytis", "title": "Geosmina y Hongos Parásitos en Vendimia", "area": "Sanidad Vegetal", "focus": "Penicillium expansum y Botrytis en vendimias lluviosas, olor a remolacha y tierra mojada"},
    {"id": "defecto_golpe_luz_riboflavina", "title": "Gusto de Luz (Goût de Lumière) y Riboflavina", "area": "Defectos", "focus": "Fotooxidación de riboflavina y metionina en botellas de vidrio transparente formando dimetilsulfuro"},
    {"id": "defecto_quercus_lactonas_sobremaduracion", "title": "Lactonas de Roble y Compuestos de Tostado", "area": "Enología", "focus": "Cis y trans-whiskey lactonas, vainillina, eugenol y guayacol aportados por el roble"},
    {"id": "defecto_manitol_enfermedad_agridulce", "title": "Fermentación Manítica (Enfermedad Agridulce)", "area": "Defectos", "focus": "Bacterias lácticas heterofermentativas degradando fructosa a manitol en vinos de clima cálido"},
    {"id": "defecto_flores_vino_candida", "title": "Flores del Vino (Candida, Pichia, Hansenula)", "area": "Defectos", "focus": "Velo blanco micelar en depósitos con cámara de aire, oxidación de alcohol a acetaldehído"},
    {"id": "resveratrol_estilbenos_salud", "title": "Resveratrol y Estilbenos en el Hollejo", "area": "Bioquímica", "focus": "Fitoalexina sintetizada por la vid como respuesta inmunitaria a hongos, propiedades antioxidantes"},
    {"id": "tdn_aroma_petroleo_riesling", "title": "TDN (1,1,6-Trimetil-1,2-dihidronaftaleno) en Riesling", "area": "Bioquímica", "focus": "Degradación de carotenoides por alta insolación y estrés hídrico, notas de keroseno"},
    {"id": "metales_pesados_quiebra_ferrica_cuprica", "title": "Quiebra Férrica y Quiebra Cúprica", "area": "Enología", "focus": "Precipitación coloidal de fosfato férrico (quiebra azul/blanca) y sulfuro de cobre en botella"},
    {"id": "corcho_alcornoque_suberina", "title": "Fisiología del Alcornoque (Quercus suber) y Suberina", "area": "Enología", "focus": "Extracción de corteza (saca), elasticidad de la suberina y micro-permeabilidad al oxígeno"},
    {"id": "tapones_sinteticos_vs_rosca_stelvin", "title": "Cierres Alternativos: Tapón de Rosca (Stelvin) y Sintéticos", "area": "Enología", "focus": "Tasa de transmisión de oxígeno (OTR), conservación de aromas reductivos y frescura varietal"},
    {"id": "envero_cambio_color_acumulacion_azucar", "title": "El Envero (Véraison): Fisiología y Bioquímica", "area": "Viticultura", "focus": "Parada de división celular, ablandamiento de la baya, traslocación de sacarosa y degradación de málico"},
    {"id": "acidos_organicos_tartarico_malico_citrico", "title": "Ácidos Orgánicos: Tartárico, Málico y Succínico", "area": "Bioquímica", "focus": "Curvas de degradación de ácido málico por respiración celular en veranos calurosos vs estabilidad del tartárico"},
    {"id": "taninos_condensados_proantocianidinas", "title": "Taninos Condensados: Hollejo vs Pepita vs Raspón", "area": "Bioquímica", "focus": "Grado de polimerización medio (mDP), amargor de taninos cortos de pepita vs sedosidad de hollejo"},
    {"id": "aromas_varietales_tiolicos_precursores", "title": "Precursores Glicosilados y Aromas Ocultos", "area": "Bioquímica", "focus": "Glucósidos de monoterpenos hidrolizados por enzimas beta-glucosidasas durante la fermentación"},
    {"id": "fototropismo_y_orientacion_hileras", "title": "Orientación de Hileras: Norte-Sur vs Este-Oeste", "area": "Viticultura", "focus": "Interceptación de radiación solar, sombreo mutuo y protección contra el golpe de sol en racimos"},
    {"id": "heladas_inversion_termica_molinos", "title": "Control de Heladas Primaverales: Torres de Viento y Velas", "area": "Viticultura", "focus": "Inversión térmica nocturna, mezcla de capas de aire y aspersión de agua para calor latente"},
    {"id": "sequia_cavitacion_xilema", "title": "Cavitación del Xilema por Estrés Hídrico Severo", "area": "Viticultura", "focus": "Embolias de aire en los vasos conductores, marchitamiento de racimos y pérdida de hojas basales"},
    {"id": "viñas_viejas_equilibrio_rendimiento", "title": "La Fisiología de las Viñas Viejas (Old Vines)", "area": "Viticultura", "focus": "Sistema radicular a más de 5 metros, autorregulación de carga, maduración regular y equilibrio"},
    {"id": "suelos_vivos_micorrizas_hongos", "title": "Simbiosis Micorrícica en el Viñedo", "area": "Edafología", "focus": "Glomeromicetos en raíces de vid, absorción de fósforo y micronutrientes, resistencia a sequía"},
    {"id": "cubiertas_vegetales_espontaneas_sembradas", "title": "Cubiertas Vegetales: Gramíneas vs Leguminosas", "area": "Viticultura", "focus": "Fijación biológica de nitrógeno, competencia hídrica controlada y prevención de la erosión del suelo"},
    {"id": "biodiversidad_islas_vegetacion_setos", "title": "Corredores Biológicos y Fauna Auxiliar en el Viñedo", "area": "Viticultura", "focus": "Control biológico de la polilla del racimo (Lobesia botrana) mediante murciélagos e insectos depredadores"},
    {"id": "densidad_plantacion_competencia", "title": "Densidad de Plantación: 2.000 vs 10.000 cepas/ha", "area": "Viticultura", "focus": "Marco mediterráneo amplio en vaso vs alta densidad en Burdeos/Borgoña para forzar raíz profunda"},
    {"id": "poda_en_verde_despunte_desnietado", "title": "Operaciones en Verde: Despunte, Desnietado y Aclareo de Racimos", "area": "Viticultura", "focus": "Eliminación de brotes no fértiles, control de vigor apical y concentración en vendimia en verde"},
    {"id": "madurez_tecnologica_vs_fenolica_aromatica", "title": "Las 3 Madureces: Tecnológica, Fenólica y Aromática", "area": "Viticultura", "focus": "Desfase entre acumulación de azúcar (Brix/Baumé) y degradación de taninos verdes en veranos cálidos"},
    {"id": "microclima_bosques_masas_agua", "title": "Influencia de Masas de Agua y Bosques en el Mesoclima", "area": "Terruño", "focus": "Capacidad calorífica del agua (ríos, lagos y mares) para suavizar extremos térmicos y reflejar luz"},
    {"id": "viento_mistral_tramontana_cierzo", "title": "Vientos Dominantes en el Viñedo: Mistral, Cierzo y Tramontana", "area": "Climatología", "focus": "Secado rápido del dosel vegetal, reducción de humedad relativa y modelado del porte de la cepa"}
,
    # --- CANON CMS: CATA DEDUCTIVA, COMPARADA Y DEFECTOS (25) ---
    {"id": "cms_deductive_visual_analysis", "standard": "CMS", "area": "Cata Deductiva", "title": "La Fase Visual CMS: Menisco, Turbidez y Lágrima", "focus": "Gradiente de color, ribete, viscosidad y edad estimada bajo la cuadrícula deductiva"},
    {"id": "cms_deductive_fruit_condition", "standard": "CMS", "area": "Cata Deductiva", "title": "Condición de la Fruta en Cata Deductiva CMS", "focus": "Diferenciación organoléptica: fruta fresca, madura, sobremadura, mermelada y pasa"},
    {"id": "cms_deductive_earth_mineral_markers", "standard": "CMS", "area": "Cata Deductiva", "title": "Marcadores Terrosos y Minerales del Viejo Mundo", "focus": "Identificación a ciegas de notas de tiza, pedernal, champiñón, sotobosque y pizarra"},
    {"id": "cms_comparative_syrah_vs_shiraz", "standard": "CMS", "area": "Cata Deductiva Comparada", "title": "Cata Comparada: Syrah del Ródano Norte vs Shiraz de Barossa", "focus": "Rotundona, pimienta negra y acidez cortante vs fruta negra confitada, chocolate y roble americano"},
    {"id": "cms_comparative_cabernet_bordeaux_napa", "standard": "CMS", "area": "Cata Deductiva Comparada", "title": "Cata Comparada: Burdeos Margen Izquierda vs Napa Valley Cabernet", "focus": "Grava, cedro, cassis y taninos austeros vs fruta madura exuberante, vainilla y taninos sedosos"},
    {"id": "cms_comparative_chardonnay_chablis_meursault", "standard": "CMS", "area": "Cata Deductiva Comparada", "title": "Cata Comparada: Chablis Mineral vs Meursault de Lías y Roble", "focus": "Acidez cortante, manzana verde y concha marina vs avellana, mantequilla y textura untuosa"},
    {"id": "cms_comparative_sauvignon_sancerre_marlborough", "standard": "CMS", "area": "Cata Deductiva Comparada", "title": "Cata Comparada: Sancerre Calcáreo vs Marlborough Tiolítico", "focus": "Tiza, grosella y hierba seca vs fruta de la pasión, maracuyá y boj punzante"},
    {"id": "cms_comparative_pinot_bourgogne_oregon", "standard": "CMS", "area": "Cata Deductiva Comparada", "title": "Cata Comparada: Borgoña Village vs Willamette Valley vs Central Otago", "focus": "Sotobosque, cereza ácida y tensión vs frambuesa silvestre, especias de roble y taninos densos"},
    {"id": "cms_comparative_sangiovese_tempranillo", "standard": "CMS", "area": "Cata Deductiva Comparada", "title": "Cata Comparada: Sangiovese (Chianti) vs Tempranillo (Rioja Reserva)", "focus": "Cereza agria, tanino astringente y té negro vs cuero, eneldo, vainilla y fruta roja madura"},
    {"id": "cms_comparative_malbec_cahors_mendoza", "standard": "CMS", "area": "Cata Deductiva Comparada", "title": "Cata Comparada: Malbec de Cahors vs Malbec de Altura de Mendoza", "focus": "Austeridad caliza, taninos agrestes y mora salvaje vs violetas, tanino aterciopelado y ciruela"},
    {"id": "cms_wine_flaws_volatile_acidity", "standard": "CMS", "area": "Defectos del Vino", "title": "Acidez Volátil y Acetato de Etilo en Sala", "focus": "Ácido acético y pegamento/disolvente: umbrales olfativos y distinción frente al ácido tartárico"},
    {"id": "cms_wine_flaws_brettanomyces", "standard": "CMS", "area": "Defectos del Vino", "title": "Brettanomyces: 4-Etilfenol y 4-Etilguayacol", "focus": "Huella de establo, sudor de caballo y cuero frente a complejidad terciaria de crianza"},
    {"id": "cms_wine_flaws_reduction_sulfides", "standard": "CMS", "area": "Defectos del Vino", "title": "Compuestos Azufrados y Reducción: H2S y Mercaptanos", "focus": "De huevo podrido a caucho quemado y col cocida: cinética redox y aireación correctiva"},
    {"id": "cms_wine_flaws_oxidation_aldehydes", "standard": "CMS", "area": "Defectos del Vino", "title": "Oxidación Prematura (Premox) y Acetaldehído", "focus": "Pérdida de SO2 libre, manzana magullada, color ámbar no intencionado y colapso en boca"},
    {"id": "cms_sommelier_service_decanting", "standard": "CMS", "area": "Servicio de Sala", "title": "Técnica de Decantación: Vinos Jóvenes vs Vinos Ancianos", "focus": "Jarreo enérgico para oxigenación vs separación lenta de sedimento con vela sin shock térmico"},
    {"id": "cms_sommelier_cellar_management", "standard": "CMS", "area": "Servicio de Sala", "title": "Gestión de Cava en Alta Restauración: Rotación y FIFO", "focus": "Humedad relativa del 70%, temperatura estable a 12°C, estanterías antivibración e inventario"},
    {"id": "cms_sommelier_wine_pricing_margins", "standard": "CMS", "area": "Servicio de Sala", "title": "Estructura de Márgenes y Carta de Vinos Rentable", "focus": "Estrategia de pricing por coeficiente decreciente, vinos de rotación y joyas de guarda"},
    {"id": "cms_food_pairing_umami_interaction", "standard": "CMS", "area": "Maridaje Deductivo", "title": "El Efecto del Umami en la Percepción Tánica y la Acidez", "focus": "Por qué el glutamato monosódico endurece el vino y qué estilos (burbujas, Jerez) triunfan"},
    {"id": "cms_food_pairing_sweet_savory_acid", "standard": "CMS", "area": "Maridaje Deductivo", "title": "Interacción entre Dulzor Residual, Acidez y Comida Grasa", "focus": "Contraste ácido-grasa y armonía azúcar-picor en cocina asiática y quesos azules"},
    {"id": "cms_blind_tasting_oak_identification", "standard": "CMS", "area": "Cata Deductiva", "title": "Identificación de Crianza en Roble: Francés vs Americano", "focus": "Vainillina, lactonas del roble americano (coco) vs eugenol, clavo y tanino sutil francés"},
    {"id": "cms_blind_tasting_climate_deduction", "standard": "CMS", "area": "Cata Deductiva", "title": "Deducción de Clima: Frío, Moderado y Cálido", "focus": "Correlación fisiológica entre grado alcohólico volumétrico, acidez total titulable y color"},
    {"id": "cms_fortified_wines_port_system", "standard": "CMS", "area": "Enología & Fortificados", "title": "El Sistema Canónico del Vino de Oporto: Ruby vs Tawny", "focus": "Crianza reductiva en balseiros vs oxidativa en pipas, añadas declaradas Vintage y Colheitas"},
    {"id": "cms_fortified_wines_madeira_styles", "standard": "CMS", "area": "Enología & Fortificados", "title": "Estilos Canónicos de Madeira: Sercial a Malvasia", "focus": "Calor artificial (Estufagem) vs calor solar (Canteiro), acidez volátil legal y perfiles secos a dulces"},
    {"id": "cms_sparkling_champagne_assemblage", "standard": "CMS", "area": "Espumosos & Método Tradicional", "title": "El Assemblage en Champagne: Vinos de Reserva y Dosage", "focus": "Construcción del estilo de maison, autólisis de levaduras sobre rima y equilibrio del licor"},
    {"id": "cms_service_champagne_opening", "standard": "CMS", "area": "Servicio de Sala", "title": "Protocolo de Apertura Silenciosa de Champagne en Mesa", "focus": "Giro de la base de la botella, contención del corcho a 45 grados y servicio sin espuma excesiva"},

    # --- CANON ASI: PROTOCOLO DE SALA, BEBIDAS DEL MUNDO Y DEGUSTACIÓN (25) ---
    {"id": "asi_sommelier_deontology_ethics", "standard": "ASI", "area": "Sumillería & Sala", "title": "Código Deontológico y Ética del Sumiller (Norma ASI)", "focus": "Neutralidad comercial, fidelidad al cliente, discreción en mesa y elegancia postural"},
    {"id": "asi_practical_candle_decanting", "standard": "ASI", "area": "Sumillería & Sala", "title": "Decantación con Vela para Vinos con Sedimento (Norma ASI)", "focus": "Luz de vela en el hombro de la botella, vertido continuo sin retorno y detección de posos"},
    {"id": "asi_beverage_sake_grades", "standard": "ASI", "area": "Bebidas del Mundo", "title": "Clasificación Canónica del Sake: Junmai, Ginjo y Daiginjo", "focus": "Tasa de pulido del arroz (Seimai-buai), adición de alcohol destilado y aromas de ginjo-ka"},
    {"id": "asi_beverage_sake_service", "standard": "ASI", "area": "Bebidas del Mundo", "title": "Protocolo de Servicio, Cristalería y Temperaturas del Sake", "focus": "Desde Kan-zake (tibio) a Reishu (frío), uso de ochoko, tokkuri y copa de vino blanco"},
    {"id": "asi_beverage_craft_beer_styles", "standard": "ASI", "area": "Bebidas del Mundo", "title": "Estilos de Cerveza y Fermentación: Ales, Lagers y Lambic", "focus": "Fermentación alta vs baja vs espontánea, lúpulo, IBUs y maridaje gastronómico"},
    {"id": "asi_beverage_mineral_waters", "standard": "ASI", "area": "Bebidas del Mundo", "title": "La Sumillería del Agua Mineral: Residuo Seco y TDS", "focus": "Aguas de baja vs alta mineralización, carbónico natural vs añadido y armonía con vinos y platos"},
    {"id": "asi_beverage_tequila_mezcal", "standard": "ASI", "area": "Destilados del Mundo", "title": "Agaves y Destilados de México: Tequila vs Mezcal", "focus": "Agave Tequilana Weber vs Agave Espadín/silvestres, hornos cónicos de tierra y destilación en alambique"},
    {"id": "asi_beverage_whisky_styles", "standard": "ASI", "area": "Destilados del Mundo", "title": "Geografía del Whisky: Scotch, Irish y Bourbon", "focus": "Malteado con turba vs triple destilación vs mash bill con 51% de maíz y roble nuevo carbonizado"},
    {"id": "asi_beverage_brandy_cognac_armagnac", "standard": "ASI", "area": "Destilados del Mundo", "title": "Cognac vs Armagnac: Terruños y Alambiques", "focus": "Doble destilación charentaise vs columna continua armagnaçaise, Ugni Blanc y cru Grande Champagne"},
    {"id": "asi_service_large_formats", "standard": "ASI", "area": "Sumillería & Sala", "title": "Servicio de Grandes Formatos: Magnum, Jeroboam y Matusalén", "focus": "Evolución lenta en botella grande, técnicas de sujeción ergonómica y escanciado equilibrado"},
    {"id": "asi_glassware_geometry_science", "standard": "ASI", "area": "Física de la Cristalería", "title": "Geometría de la Copa: Difusión Aromática y Vertido", "focus": "Relación entre diámetro de chimenea, volumen de cámara de evaporación y caída en papilas"},
    {"id": "asi_viticulture_biodynamic_preparations", "standard": "ASI", "area": "Viticultura Sostenible", "title": "Viticultura Biodinámica: Preparados 500 y 501", "focus": "Boñiga en cuerno fermentada (500) y sílice molida (501), dinamización en agua y certificación Demeter"},
    {"id": "asi_viticulture_regenerative_agroforestry", "standard": "ASI", "area": "Viticultura Sostenible", "title": "Viticultura Regenerativa: Captura de Carbono y Suelo Vivo", "focus": "Siembra de leguminosas, pastoreo dirigido entre hileras y eliminación de laboreo destructivo"},
    {"id": "asi_sommelier_cheese_cart_pairing", "standard": "ASI", "area": "Sumillería & Armonías", "title": "El Carro de Quesos: Armonías de Afinidad y Osmosis", "focus": "Quesos de pasta blanda, lavada, dura y azul: maridajes con blancos ácidos, espumosos y dulces nobles"},
    {"id": "asi_sommelier_cigar_fortified_pairing", "standard": "ASI", "area": "Sumillería & Sala", "title": "Protocolo de Servicio de Puros con Vinos Fortificados", "focus": "Corte con guillotina, encendido con fósforo de cedro y maridaje con Rancio, Tawny y PX"},
    {"id": "asi_sensory_trpv1_capsaicin", "standard": "ASI", "area": "Fisiología Sensorial", "title": "Receptores TRPV1 y Comida Picante ante el Vino Tánico", "focus": "Termorreceptores orales activados por capsaicina: vasodilatación, quemazón y astringencia desbocada"},
    {"id": "asi_sensory_salt_acid_tannin_balance", "standard": "ASI", "area": "Fisiología Sensorial", "title": "El Rol de la Sal en la Supresión del Amargor y la Acidez", "focus": "Mecanismo iónico oral del cloruro sódico que redondea vinos tánicos y amortigua acidez punzante"},
    {"id": "asi_service_table_presentation_drill", "standard": "ASI", "area": "Sumillería & Sala", "title": "Presentación Canónica de la Botella al Comensal", "focus": "Anuncio claro de bodega, denominación y añada, etiqueta visible en lito y confirmación del anfitrión"},
    {"id": "asi_service_cork_inspection", "standard": "ASI", "area": "Sumillería & Sala", "title": "Inspección Canónica del Corcho en Sala", "focus": "Comprobación de humedad, elasticidad y aromas antes de depositarlo en platillo auxiliar frente al anfitrión"},
    {"id": "asi_blind_tasting_competition_format", "standard": "ASI", "area": "Competición Internacional", "title": "La Cuadrícula de Cata de Competición ASI", "focus": "Gestión del tiempo (4 minutos por copa), vocabulario sensorial internacional y sugerencia comercial"},
    {"id": "asi_beverage_vermouth_aromatized_wines", "standard": "ASI", "area": "Bebidas del Mundo", "title": "Vinos Aromatizados y Vermut: El Ritual del Aperitivo", "focus": "Artemisia absinthium, infusiones botánicas, azúcar y servicio con piel de cítrico"},
    {"id": "asi_beverage_tea_sommellerie", "standard": "ASI", "area": "Bebidas del Mundo", "title": "Sumillería de Infusiones y Té en la Mesa Gastronómica", "focus": "Tés verdes (Sencha), fermentados (Pu-erh) y semifermentados (Oolong) como alternativa al vino"},
    {"id": "asi_beverage_coffee_specialty", "standard": "ASI", "area": "Bebidas del Mundo", "title": "Café de Especialidad y Protocolo de Cierre de Sala", "focus": "Procesos de lavado, natural y honey en Arábica: extracción y maridaje con petit fours"},
    {"id": "asi_cellar_wine_preservation_systems", "standard": "ASI", "area": "Sumillería & Sala", "title": "Sistemas de Conservación por Copas: Gas Inerte y Coravin", "focus": "Inyección de gas argón grado enológico para evitar oxidación en botellas de alta gama abiertas"},
    {"id": "asi_sommelier_conflict_spoilage_resolution", "standard": "ASI", "area": "Sumillería & Sala", "title": "Resolución de Disconformidad por Vino Defectuoso en Sala", "focus": "Validación cortés sin discusión, retirada inmediata de la botella y sugerencia de alternativa óptima"},



    # ==========================================================================
    # NUEVA SERIE MASTER ENCLOPÉDICA: Bioquímica, Viticultura y Grandes Terruños
    # ==========================================================================
    {"id": "enologia_crioextraccion_maceracion_prefermentativa", "title": "Crioextracción y Maceración Prefermentativa en Frío", "area": "Enología", "focus": "Extracción selectiva de precursores tiólicos y antocianos sin polifenoles astringentes"},
    {"id": "enologia_autolisis_manoproteinas_levadura", "title": "Dinámica de Autólisis y Liberación de Manoproteínas", "area": "Enología", "focus": "Degradación enzimática de la pared celular de Saccharomyces, estabilidad coloidal y volumen"},
    {"id": "enologia_esteres_acetatos_fermentativos", "title": "Ésteres Etílicos y Acetatos: Rutas Bioquímicas", "area": "Enología", "focus": "Formación de hexanoato y octanoato de etilo, degradación térmica y pérdida aromática"},
    {"id": "enologia_diacetilo_fermentacion_malolactica", "title": "El Diacetilo y la Fermentación Maloláctica", "area": "Enología", "focus": "Síntesis por Oenococcus oeni a partir de ácido cítrico, notas de mantequilla y prevención de niveles excesivos"},
    {"id": "enologia_metoxipirazinas_cinetica_degradacion", "title": "Metoxipirazinas: Cinética de Síntesis y Degradación", "area": "Enología", "focus": "IBMP y IPMP en Cabernet Sauvignon y Sauvignon Blanc, defoliación e insolación térmica"},
    {"id": "enologia_rotundona_pimienta_negra_sesquiterpeno", "title": "La Rotundona: El Marcador de Pimienta en Syrah", "area": "Enología", "focus": "Sesquiterpeno bicíclico, biosíntesis en hollejo y umbrales sensoriales en partes por trillón"},
    {"id": "enologia_microoxigenacion_polimerizacion_tanica", "title": "Microoxigenación (Mox) y Enlaces Antociano-Tanino", "area": "Enología", "focus": "Inyección controlada de microdosis de O2 para formación de pigmentos poliméricos estables"},
    {"id": "enologia_taninos_elagicos_vs_proantocianidinas", "title": "Taninos Elágicos del Roble vs Proantocianidinas de la Uva", "area": "Enología", "focus": "Diferencias estructurales, reactividad salival y aporte de vanillina y furfural"},
    {"id": "enologia_estabilizacion_tartarica_cmc_electro", "title": "Estabilización Tartárica Moderna: CMC, Manoproteínas y Electrodiálisis", "area": "Enología", "focus": "Inhibición de cristalización de bitartrato potásico sin frío extremo"},
    {"id": "enologia_aminas_biogenas_control_enologico", "title": "Aminas Biógenas: Histamina, Tiramina y Putrescina", "area": "Enología", "focus": "Descarboxilación bacteriana de aminoácidos, control de higiene y cepas de bacterias lácticas seleccionadas"},
    {"id": "enologia_equilibrios_dioxido_azufre_so2_molecular", "title": "El SO2 Molecular y el pH: Termodinámica de la Protección", "area": "Enología", "focus": "Proporción de SO2 activo frente al pH del vino y cálculo estequiométrico antimicrobiano"},
    {"id": "enologia_enzimas_pectoliticas_clarificacion", "title": "Enzimas Pectolíticas en Desfangado y Clarificación", "area": "Enología", "focus": "Hidrólisis de pectinas en mostos blancos, reducción de turbidez y filtrabilidad"},
    {"id": "enologia_levaduras_no_saccharomyces_torulaspora", "title": "Levaduras No-Saccharomyces: Torulaspora, Metschnikowia y Lachancea", "area": "Enología", "focus": "Bio-protección, síntesis de acidez láctica biológica y complejidad en fermentaciones mixtas"},
    {"id": "enologia_nutricion_nitrogenada_yan_aminoacidos", "title": "Nitrógeno Asimilable por Levaduras (YAN) y Estrés Fermentativo", "area": "Enología", "focus": "Nitrógeno amoniacal vs orgánico, prevención de H2S y paradas de fermentación"},
    {"id": "enologia_clarificacion_espontanea_floculacion", "title": "Clarificación Espontánea y Coagulación de Coloides", "area": "Enología", "focus": "Cargas electrostáticas de proteínas, taninos y polisacáridos en la caída de posos"},
    {"id": "enologia_lactonas_del_roble_cis_trans", "title": "Lactonas del Roble (Quercus lactones): Isómeros Cis y Trans", "area": "Enología", "focus": "Aromas de coco y madera fresca, tostado de barrica y origen del roble blanco americano"},
    {"id": "enologia_acidez_volatil_mecanismo_sintesis", "title": "Ácido Acético y Acetato de Etilo: Límites y Rutas", "area": "Enología", "focus": "Oxidación de etanol por Acetobacter y levaduras osmófilas durante vendimia dañada"},
    {"id": "enologia_polifenoles_indices_folin_ci_ipt", "title": "Índices Analíticos de Polifenoles: IPT, Antocianos y Color", "area": "Enología", "focus": "Medición de absorbancia a 280, 420, 520 y 620 nm y diagnóstico de extracción"},
    {"id": "enologia_sotolon_crianza_oxidativa_vin_jaune", "title": "El Sotolón y la Crianza Oxidativa Prolongada", "area": "Enología", "focus": "Lactona furanona aromática, marcadores de nuez, curry y arce en Jura, Jerez y Madeira"},
    {"id": "enologia_fisiologia_levadura_flor_saccharomyces_bayanus", "title": "Fisiología de la Levadura de Flor (Saccharomyces beticus)", "area": "Enología", "focus": "Metabolismo oxidativo de etanol a acetaldehído y consumo de glicerol bajo velo"},
    {"id": "viticultura_indice_winkler_huglin_bioclimatico", "title": "Índices Bioclimáticos de Winkler, Huglin y Noches Frescas", "area": "Viticultura", "focus": "Suma térmica diurna, radiación latitudinal y zonificación de variedades mundiales"},
    {"id": "viticultura_patrones_portainjertos_filoxera_sequia", "title": "Patrones y Portainjertos: De 110R y 140Ru a Fercal y Richter 110", "area": "Viticultura", "focus": "Resistencia radicular a caliza activa (IPC), nematodos y tolerancia al estrés hídrico"},
    {"id": "viticultura_enfermedades_madera_esca_eutipiosis", "title": "Enfermedades Fúngicas de la Madera: Esca, BDA y Eutipiosis", "area": "Viticultura", "focus": "Complejo fúngico vascular, necrosis del xilema y técnicas de poda de respeto Guyot-Poussard"},
    {"id": "viticultura_flavescencia_dorada_scaphoideus", "title": "Flavescencia Dorada y la Fitoplasmosis de la Vid", "area": "Viticultura", "focus": "Vector Scaphoideus titanus, amarillamiento foliar, enrollamiento y cuarentena legal"},
    {"id": "viticultura_potencial_hidrico_foliar_scholander", "title": "El Potencial Hídrico Foliar y la Cámara de Scholander", "area": "Viticultura", "focus": "Medición de tensión xilemática en pre-amanecer para gestión del riego de precisión"},
    {"id": "viticultura_fotosintesis_superficie_foliar_exposicion", "title": "Ratio Superficie Foliar / Peso de Cosecha (SFE)", "area": "Viticultura", "focus": "Equilibrio entre m2 de masa vegetal expuesta y kg de fruta para maduración fenólica completa"},
    {"id": "viticultura_poda_respeto_arquitectura_flujo_savia", "title": "Poda de Respeto y Preservación de los Flujos de Savia", "area": "Viticultura", "focus": "Evitar conos de desecación internos, poda corta y cicatrización natural de brazos"},
    {"id": "viticultura_clones_seleccion_masal_vs_clonal", "title": "Selección Masal vs Selección Clonal Certificada", "area": "Viticultura", "focus": "Diversidad genética intra-varietal, resiliencia a plagas e identidad de viñedos históricos"},
    {"id": "viticultura_cubiertas_vegetales_biodiversidad_edafica", "title": "Cubiertas Vegetales y Red Trófica del Suelo", "area": "Viticultura", "focus": "Micorrizas arbusculares, fijación de nitrógeno por leguminosas y descompactación radicular"},
    {"id": "viticultura_estres_termico_golpe_de_calor_resveratrol", "title": "Golpes de Calor y Quemaduras Solares en Racimo", "area": "Viticultura", "focus": "Bloqueo fotosintético a >35°C, degradación de antocianos y aplicación de caolín"},
    {"id": "terroir_cote_rotie_ampuis_brune_blonde", "title": "Côte-Rôtie: Las Pendientes de Ampuis, Côte Brune y Côte Blonde", "area": "Geografía & Terruño", "focus": "Micaesquistos vs calizas ferruginosas, cofermentación tradicional con 5-20% de Viognier"},
    {"id": "terroir_hermitage_colina_bessards_meal", "title": "La Colina de Hermitage: Granitos de Les Bessards y Gravas de Le Méal", "area": "Geografía & Terruño", "focus": "Diversidad geomorfológica del espolón granítico sobre el Ródano y longevidad de Syrah"},
    {"id": "terroir_clos_vougeot_muro_monjes_cister", "title": "Clos de Vougeot: Los 50 Hectáreas del Muro Cisterciense", "area": "Geografía & Terruño", "focus": "Estratificación de suelos aluviales, medios y superiores entre más de 80 propietarios"},
    {"id": "terroir_montrachet_chevalier_batard_microparcelas", "title": "Le Montrachet y sus Satélites: El Panteón del Chardonnay", "area": "Geografía & Terruño", "focus": "Laderas orientadas al este sobre caliza jurásica batoniensa en Puligny y Chassagne"},
    {"id": "terroir_barolo_cannubi_cerequio_brunate", "title": "Los Grandes Crus de Barolo: Cannubi, Cerequio, Rocche y Brunate", "area": "Geografía & Terruño", "focus": "Confluencia de margas tortonianas de Sant'Agata y areniscas helvéticas de Diano d'Alba"},
    {"id": "terroir_brunello_montalcino_cuadrantes_clima", "title": "Brunello di Montalcino: Los Cuatro Cuadrantes Geográficos", "area": "Geografía & Terruño", "focus": "Diferencias entre el norte fresco pizarroso, el sur soleado de Sant'Angelo y Castelnuovo"},
    {"id": "terroir_priorat_costers_llicorella_escaladei", "title": "Priorat: Los Costers de Escaladei y la Sierra de Montsant", "area": "Geografía & Terruño", "focus": "Pizarras paleozoicas descompuestas en pendientes del 60% cultivadas en terrazas manuales"},
    {"id": "terroir_ribeira_sacra_bancales_sil_mino", "title": "Ribeira Sacra: La Viticultura Heroica de los Cañones del Sil y Miño", "area": "Geografía & Terruño", "focus": "Bancales vertiginosos de granito y esquisto, microclima atlántico-continental y Mencía"},
    {"id": "terroir_marco_jerez_pagos_miraflores_macharnudo", "title": "Los Pagos Históricos del Marco de Jerez: Macharnudo, Carrascal y Miraflores", "area": "Geografía & Terruño", "focus": "Albarizas lentejuelas, barajuelas y lustrillos y su influencia mineral en la crianza de la flor"},
    {"id": "terroir_rioja_subzonas_sonsierra_oriental", "title": "La Sonsierra Riojana y los Contrastes con Rioja Oriental", "area": "Geografía & Terruño", "focus": "Terrazas calizas bajo la Sierra de Cantabria frente al valle cálido aluvial del Ebro"},
    {"id": "terroir_gualtallary_altamira_valle_uco_calcareo", "title": "Gualtallary y Paraje Altamira: Calizas de Altura en Valle de Uco", "area": "Geografía & Terruño", "focus": "Grava aluvial recubierta de carbonato de calcio a 1.400m de altitud en los Andes"},
    {"id": "terroir_coonawarra_terra_rossa_ridge", "title": "El Lomo de Terra Rossa de Coonawarra", "area": "Geografía & Terruño", "focus": "Estrecha franja de 15km de arcilla roja rica en hierro sobre caliza marina terciaria"},
    {"id": "terroir_gimlett_gravels_hawkes_bay", "title": "Gimblett Gravels de Hawke's Bay: Suelo Pétreo Antiguo", "area": "Geografía & Terruño", "focus": "Lecho fluvial seco depositado por el río Ngaruroro, acumulación térmica y Syrah de clase mundial"},
    {"id": "terroir_central_otago_bannockburn_bendigo", "title": "Central Otago: Bannockburn, Bendigo y Gibbston Valley", "area": "Geografía & Terruño", "focus": "La región vitícola más interior de Nueva Zelanda sobre esquisto y grava glaciar para Pinot Noir"},
    {"id": "terroir_wachau_terrazas_achleiten_singerriedel", "title": "Las Terrazas de Piedra Seca de Wachau: Achleiten y Singerriedel", "area": "Geografía & Terruño", "focus": "Gneis migmatítico de los bosques primarios austríacos sobre el Danubio para Grüner Veltliner"},
    {"id": "terroir_tokaj_primeros_pagos_1730", "title": "Tokaj-Hegyalja: La Primera Clasificación de Pagos del Mundo (1730)", "area": "Geografía & Terruño", "focus": "Lavas riolíticas, toba volcánica y confluencia de nieblas de los ríos Bodrog y Tisza"},
    {"id": "terroir_santorini_kouloura_suelo_asphyctico", "title": "Santorini y la Cesta Kouloura: Viento Etesio y Pumita Volcánica", "area": "Geografía & Terruño", "focus": "Poda ancestral circular para proteger racimos de la arena abrasiva y sequía extrema"},
    {"id": "terroir_etna_contrade_passopisciaro_arcuria", "title": "Las Contrade del Etna: Coladas de Lava y Nerello Mascalese", "area": "Geografía & Terruño", "focus": "Diferenciación geológica entre coladas volcánicas de 1614, 1800 y 1981 en laderas norteñas"},
    {"id": "vinos_madeira_estufagem_vs_canteiro", "title": "Madeira: El Proceso Térmico de Estufagem vs Canteiro", "area": "Vinos del Mundo", "focus": "Caramelización y maderización de Sercial, Verdelho, Bual y Malvasia"},
    {"id": "vinos_vin_jaune_chateau_chalon_savagnin", "title": "Vin Jaune de Château-Chalon: Seis Años Bajo Velo", "area": "Vinos del Mundo", "focus": "Crianza en barricas viejas de 228 litros sin relleno (ouillage), sotolón y longevidad centenaria"},
    {"id": "vinos_commandaria_chipre_el_vino_mas_antiguo", "title": "Commandaria de Chipre: El Vino con Denominación más Antiguo del Mundo", "area": "Vinos del Mundo", "focus": "Pasificación al sol de uvas Xynisteri y Mavro al pie del Monte Troodos"},
    {"id": "vinos_tokaji_eszencia_presion_osmotica", "title": "Tokaji Eszencia: El Néctar de Auto-Prensado", "area": "Vinos del Mundo", "focus": "Concentración extrema de 450-800 g/L de azúcar, fermentación de años por levaduras osmotolerantes"},
    {"id": "vinos_oporto_vintage_vs_colheita_tawny", "title": "Oporto: La Dicotomía entre Vintage (Botella) y Colheita (Pipa)", "area": "Vinos del Mundo", "focus": "Evolución reductiva protegida frente a la microoxigenación en maderas de roble de 550 litros"},
    {"id": "vinos_icewine_eiswein_crioextraccion_natural", "title": "Icewine y Eiswein: La Vendimia a -8°C Bajo Hielo", "area": "Vinos del Mundo", "focus": "Presión en prensa con agua congelada retenida en cristales y mosto hiperconcentrado"},
    {"id": "vinos_marsala_vergine_stravecchio_soleras", "title": "Marsala Vergine Stravecchio: El Tesoro de Sicilia", "area": "Vinos del Mundo", "focus": "Crianza en soleras con fortificación en alcohol vínico puro sin mosto cocido (mosto cotto)"},
    {"id": "vinos_recioto_della_valpolicella_parada_fermentativa", "title": "Recioto della Valpolicella: El Origen Dulce del Amarone", "area": "Vinos del Mundo", "focus": "Parada espontánea o forzada de fermentación para preservar azúcares nobles de uvas pasificadas"},
    {"id": "vinos_rutherglen_muscat_soleras_calidas", "title": "Rutherglen Muscat de Victoria: Soleras en Almacenes de Chapa", "area": "Vinos del Mundo", "focus": "Oxidación acelerada por calor estival australiano en botas de roble viejo"},
    {"id": "vinos_vin_de_paille_jura_hermitage", "title": "Vin de Paille: La Tradición del Vino de Paja en Jura y Hermitage", "area": "Vinos del Mundo", "focus": "Deshidratación en esteras de paja durante meses antes del prensado de invierno"},

    # --- Expansión a 1,450 Fichas: Denominaciones y Terruños de Élite (+172) ---
    {"id": "dop_espana_ribera_del_guadiana", "title": "D.O. Ribera del Guadiana", "area": "Regiones de España", "focus": "Las seis subzonas de Extremadura (Tierra de Barros, Matanegra), suelos arcillosos y Pardina/Tempranillo"},
    {"id": "dop_espana_jumilla", "title": "D.O.P. Jumilla", "area": "Regiones de España", "focus": "El reino de la Monastrell en pie franco, suelos calizos pardos y oscilación térmica continental-mediterránea"},
    {"id": "dop_espana_yecla", "title": "D.O. Yecla", "area": "Regiones de España", "focus": "Campo Arriba y Campo Abajo, altitud hasta 900m, calizas pedregosas y Monastrell concentrada"},
    {"id": "dop_espana_bullas", "title": "D.O. Bullas", "area": "Regiones de España", "focus": "Valle del Aceniche y ladera del Castellar, viticultura de montaña en el interior de Murcia"},
    {"id": "dop_espana_calatayud", "title": "D.O.P. Calatayud", "area": "Regiones de España", "focus": "Garnachas viejas de altura (hasta 1.000m), pizarras rojas del Sistema Ibérico y frescura mineral"},
    {"id": "dop_espana_campo_de_borja", "title": "D.O. Campo de Borja: El Imperio de la Garnacha", "area": "Regiones de España", "focus": "Tres pisos altitudinales bajo el influjo del Moncayo y el Cierzo desecante"},
    {"id": "dop_espana_carinena", "title": "D.O.P. Cariñena", "area": "Regiones de España", "focus": "Suelos aluviales pedregosos (cascajos), viñedos históricos y adaptación de la variedad homónima"},
    {"id": "dop_espana_somontano", "title": "D.O. Somontano", "area": "Regiones de España", "focus": "Prepirineo oscense, confluencia de calizas y areniscas, Moristel, Parraleta y castas internacionales"},
    {"id": "dop_espana_arlanza", "title": "D.O. Arlanza", "area": "Regiones de España", "focus": "Ribera alta del río Arlanza entre Burgos y Palencia, altitud de 850-1.000m y Tinta del País de guarda"},
    {"id": "dop_espana_cigales", "title": "D.O. Cigales", "area": "Regiones de España", "focus": "El rosado (clarete) tradicional de cofermentación tinto/blanco y tintos estructurados sobre terrazas aluviales"},
    {"id": "dop_espana_arribes", "title": "D.O. Arribes", "area": "Regiones de España", "focus": "Cañones graníticos del Duero internacional, bancales vertiginosos y biodiversidad de Juan García y Bruñal"},
    {"id": "dop_espana_tierra_del_vino_zamora", "title": "D.O. Tierra del Vino de Zamora", "area": "Regiones de España", "focus": "Suelos profundos aluviales sobre margas terciarias, cepas centenarias de Tempranillo"},
    {"id": "dop_espana_cebreros", "title": "D.O.P. Cebreros (Gredos)", "area": "Regiones de España", "focus": "Pizarras y granitos de la Sierra de Gredos, altitud extrema y Garnachas y Albillos Reales minerales"},
    {"id": "dop_espana_vinos_de_madrid", "title": "D.O. Vinos de Madrid", "area": "Regiones de España", "focus": "Las cuatro subzonas: San Martín (granito), Navalcarnero (arenas), Arganda (calizas) y El Molar (pizarras)"},
    {"id": "dop_espana_mentrida", "title": "D.O. Méntrida", "area": "Regiones de España", "focus": "Laderas del Guadarrama toledano, arenas silíceas de disgregación granítica y Garnacha de viñas viejas"},
    {"id": "dop_espana_manchuela", "title": "D.O. Manchuela", "area": "Regiones de España", "focus": "Valles de los ríos Júcar y Cabriel, vientos solanos del Mediterráneo y la personalidad de la uva Bobal"},
    {"id": "dop_espana_ribera_del_jucar", "title": "D.O. Ribera del Júcar", "area": "Regiones de España", "focus": "Cantos rodados fluviales sobre fondos arcillo-calcáreos en Cuenca, maceraciones prolongadas"},
    {"id": "dop_espana_almansa", "title": "D.O. Almansa", "area": "Regiones de España", "focus": "Corredor de transición entre la Meseta y el Levante, calizas y suelos pedregosos con Garnacha Tintorera"},
    {"id": "dop_espana_valdepenas", "title": "D.O. Valdepeñas", "area": "Regiones de España", "focus": "Cuenca del Jabalón en Campo de Calatrava, calizas y arcillas pardas con Cencibel y Airén"},
    {"id": "dop_espana_utiel_requena", "title": "D.O.P. Utiel-Requena", "area": "Regiones de España", "focus": "Meseta interior a 750m, la cuna histórica mundial de la uva Bobal y tintos de gran polifenol"},
    {"id": "dop_espana_alicante", "title": "D.O.P. Alicante y el Fondillón", "area": "Regiones de España", "focus": "Vinares y Marina Alta: el Fondillón noble de Monastrell sobremadura y crianza en tonel monovero"},
    {"id": "dop_espana_valencia", "title": "D.O. Valencia: Alto Turia y Clariano", "area": "Regiones de España", "focus": "De las nieves de Titaguas (Merseguera de altura) a los valles soleados de Fontanares (Mandó y Forcallat)"},
    {"id": "dop_espana_binissalem_mallorca", "title": "D.O. Binissalem (Mallorca)", "area": "Regiones de España", "focus": "Laderas de la Sierra de Tramuntana, suelos de call vermell y uvas Manto Negro y Moll"},
    {"id": "dop_espana_pla_i_llevant", "title": "D.O. Pla i Llevant (Mallorca)", "area": "Regiones de España", "focus": "Vientos marinos de marinada, suelos arcillo-calcáreos y uvas Callet, Fogoneu y Gorgollassa"},
    {"id": "dop_espana_lanzarote_cenizas", "title": "D.O.P. Lanzarote: Paisaje de La Geria", "area": "Regiones de España", "focus": "Hoyos excavados en ceniza volcánica (lapilli/picón), muros cortaviento de piedra y Malvasía Volcánica"},
    {"id": "dop_espana_valle_orotava_cordon_trenzado", "title": "D.O. Valle de La Orotava", "area": "Regiones de España", "focus": "El sistema único mundial de cordón trenzado de hasta 15 metros, laderas norte de Tenerife y Listán Negro"},
    {"id": "dop_espana_tacoronte_acentejo", "title": "D.O. Tacoronte-Acentejo", "area": "Regiones de España", "focus": "Suelos volcánicos arcillosos fértiles bajo la influencia directa del mar de nubes de los Alisios"},
    {"id": "dop_espana_valle_guimar", "title": "D.O. Valle de Güímar", "area": "Regiones de España", "focus": "Pendientes vertiginosas desde el nivel del mar hasta 1.400m en Tenerife sur, Malvasía y Listán Blanco"},
    {"id": "dop_espana_ycoden_daute_isora", "title": "D.O. Ycoden-Daute-Isora", "area": "Regiones de España", "focus": "Noroeste de Tenerife, malpaíses basálticos y viñedos centenarios en pie franco con Baboso Negro y Vijariego"},
    {"id": "dop_espana_abona", "title": "D.O. Abona", "area": "Regiones de España", "focus": "Los viñedos más altos de España en Vilaflor (hasta 1.700m de altitud) sobre toba blanca pumítica"},
    {"id": "dop_espana_la_palma", "title": "D.O. La Palma: Fuencaliente y Las Breñas", "area": "Regiones de España", "focus": "Lavas históricas de volcanes de San Antonio y Teneguía, Malvasía dulce aromática y Negramoll"},
    {"id": "dop_espana_el_hierro", "title": "D.O. El Hierro", "area": "Regiones de España", "focus": "La isla más occidental, laderas de El Golfo y Frontera sobre basalto negro y uva Verijadiego/Vijariego"},
    {"id": "dop_espana_la_gomera", "title": "D.O. La Gomera", "area": "Regiones de España", "focus": "Bancales de piedra seca colgados sobre barrancos imposibles y la exclusiva uva Forastera Gomera"},
    {"id": "dop_espana_cava_parajes_calificados", "title": "D.O. Cava: Parajes Calificados y Zonificación", "area": "Regiones de España", "focus": "Comtats de Barcelona, Valle del Ebro, Viñedos de Almendralejo y Requena; requisitos de Guarda Superior"},
    {"id": "dop_espana_corpinnat_clasica_penedes", "title": "Corpinnat y Clàssic Penedès: Métodos de Excelencia", "area": "Regiones de España", "focus": "100% uva ecológica, vendimia manual, crianzas mínimas de 18 a 60 meses y vinificación en la propiedad"},
    {"id": "aoc_francia_pauillac", "title": "AOC Pauillac: La Meca del Cabernet Sauvignon", "area": "Regiones de Francia", "focus": "Gravas cuarcíticas profundas del Garona sobre lecho calcáreo, tres Premiers Crus de 1855"},
    {"id": "aoc_francia_margaux", "title": "AOC Margaux: Delicadeza y Perfume", "area": "Regiones de Francia", "focus": "Las gravas más finas y arenosas del Médoc meridional, pH bajo y elegancia tánica sedosa"},
    {"id": "aoc_francia_saint_julien", "title": "AOC Saint-Julien: El Equilibrio Canónico de Burdeos", "area": "Regiones de Francia", "focus": "Meseta homogénea de grava entre Pauillac y Margaux con la mayor densidad de Crus Classés"},
    {"id": "aoc_francia_saint_estephe", "title": "AOC Saint-Estèphe: Arcillas y Frescura", "area": "Regiones de Francia", "focus": "Suelos con mayor componente de arcilla pesada que retienen agua en añadas cálidas y estructuran Merlot"},
    {"id": "aoc_francia_pomerol_plateau", "title": "AOC Pomerol y la Meseta de Arcilla Azul", "area": "Regiones de Francia", "focus": "Ausencia de clasificación formal, arcillas de esmectita con óxido de hierro (crasse de fer) y Merlot untuoso"},
    {"id": "aoc_francia_saint_emilion_grand_cru_classe", "title": "AOC Saint-Émilion: Meseta Calcárea y Cuestas", "area": "Regiones de Francia", "focus": "Caliza con fósiles de estrellas marinas (calcaire à astéries) y ensamblajes dominados por Cabernet Franc"},
    {"id": "aoc_francia_pessac_leognan", "title": "AOC Pessac-Léognan: Cuna de Haut-Brion", "area": "Regiones de Francia", "focus": "Gravas aluviales históricas al sur de Burdeos con microclima urbano templado para tintos y blancos"},
    {"id": "aoc_francia_sauternes_barsac", "title": "AOC Sauternes y Barsac: El Río Ciron y la Botrytis", "area": "Regiones de Francia", "focus": "Confluencia de aguas frías del Ciron con el Garona para nieblas otoñales, Semillon botritizado noble"},
    {"id": "aoc_francia_gevrey_chambertin", "title": "AOC Gevrey-Chambertin: Potencia de la Côte de Nuits", "area": "Regiones de Francia", "focus": "Los 9 Grands Crus (Chambertin, Clos de Bèze), calizas bajocienses y Pinot Noir musculoso"},
    {"id": "aoc_francia_vosne_romanee", "title": "AOC Vosne-Romanée: El Sancta Sanctorum", "area": "Regiones de Francia", "focus": "Romanée-Conti, La Tâche, Richebourg: inclinación este perfecta sobre caliza jurásica y textura etérea"},
    {"id": "aoc_francia_chambolle_musigny", "title": "AOC Chambolle-Musigny: Encaje y Mineralidad", "area": "Regiones de Francia", "focus": "Musigny y Bonnes-Mares sobre suelos de caliza pura con escasa arcilla superficial y perfume de violeta"},
    {"id": "aoc_francia_nuits_saint_georges", "title": "AOC Nuits-Saint-Georges", "area": "Regiones de Francia", "focus": "Frontera entre Côte de Nuits y Beaune: sector norte pedregoso vs sector sur margoso y vinos de larga guarda"},
    {"id": "aoc_francia_meursault", "title": "AOC Meursault: La Cremosidad del Chardonnay", "area": "Regiones de Francia", "focus": "Margas jurásicas oxfordianas y calizas de crinoides en Les Perrières y Les Charmes"},
    {"id": "aoc_francia_puligny_chassagne_montrachet", "title": "AOC Puligny-Montrachet y Chassagne-Montrachet", "area": "Regiones de Francia", "focus": "La mayor concentración mundial de grandes blancos secos sobre el banco de caliza batoniense"},
    {"id": "aoc_francia_chablis_premier_grand_cru", "title": "AOC Chablis: Las 7 Parcelas del Grand Cru", "area": "Regiones de Francia", "focus": "Les Clos, Vaudésir, Valmur: ladera orientada al suroeste sobre marga kimmeridgiense pura"},
    {"id": "aoc_francia_sancerre_tres_terruños", "title": "AOC Sancerre: Terres Blanches, Caillottes y Silex", "area": "Regiones de Francia", "focus": "Falla geológica que expone tiza kimmeridgiense, calizas de guijarros y pedernal de sílice"},
    {"id": "aoc_francia_pouilly_fume", "title": "AOC Pouilly-Fumé: Fuego y Mineralidad", "area": "Regiones de Francia", "focus": "Riberas orientales del Loira sobre sílex puro que aporta la nota característica de piedra de fusil"},
    {"id": "aoc_francia_vouvray_tuffeau", "title": "AOC Vouvray y la Toba Calcárea", "area": "Regiones de Francia", "focus": "Tiza porosa blanca (tuffeau) en laderas del Loira: desde secos aéreos hasta moelleux centenarios de Chenin"},
    {"id": "aoc_francia_chinon_cabernet_franc", "title": "AOC Chinon: El Cabernet Franc Rabelaisiano", "area": "Regiones de Francia", "focus": "Gravas arenosas de vega para vinos jugosos y laderas de toba calcárea para tintos de guarda"},
    {"id": "aoc_francia_saumur_champigny", "title": "AOC Saumur-Champigny", "area": "Regiones de Francia", "focus": "Lomas soleadas al sur del Loira con suelo de tiza permeable y Cabernet Franc de fruta crujiente"},
    {"id": "aoc_francia_muscadet_sevre_et_maine_sur_lie", "title": "AOC Muscadet Sèvre-et-Maine sobre Lías", "area": "Regiones de Francia", "focus": "Rocas ígneas y metamórficas del Macizo Armoricano (gneis, esquisto, gabro) y uva Melon de Bourgogne"},
    {"id": "aoc_francia_cornas", "title": "AOC Cornas: El Granito del Ródano Norte", "area": "Regiones de Francia", "focus": "Anfiteatro natural protegido del viento del norte, suelo de granito descompuesto (gore) y Syrah 100%"},
    {"id": "aoc_francia_chateauneuf_du_pape_13_variedades", "title": "AOC Châteauneuf-du-Pape y las 13 Variedades", "area": "Regiones de Francia", "focus": "Los cuatro suelos (galets roulés, arenas, calizas y arcillas rojas) y la sinfonía de Garnacha"},
    {"id": "aoc_francia_gigondas_dentelles_montmirail", "title": "AOC Gigondas y las Dentelles de Montmirail", "area": "Regiones de Francia", "focus": "Estructuras rocosas jurásicas calizas que aportan sombra matinal y frescura alpina a la Garnacha"},
    {"id": "aoc_francia_bandol_mourvedre", "title": "AOC Bandol: El Bastión de la Mourvèdre", "area": "Regiones de Francia", "focus": "Bancales de piedra marina orientados al sur frente al Mediterráneo con mínimo 50% de Mourvèdre"},
    {"id": "aoc_francia_cahors_malbec_auxerrois", "title": "AOC Cahors: El Vino Negro del Lot", "area": "Regiones de Francia", "focus": "Las tres terrazas aluviales del río Lot y la meseta caliza (causses) con Malbec autóctono"},
    {"id": "aoc_francia_madiran_tannat", "title": "AOC Madiran: El Reino del Tannat", "area": "Regiones de Francia", "focus": "Suelos arcillo-silíceos con cantos rodados (galets) y la técnica de microoxigenación de Patrick Ducournau"},
    {"id": "aoc_francia_jurancon_manseng", "title": "AOC Jurançon: Gros y Petit Manseng", "area": "Regiones de Francia", "focus": "Laderas del Pirineo atlántico, efecto foehn del viento sur y pasificación sobre la vid (passerillage)"},
    {"id": "aoc_francia_alsacia_grand_cru_51_terruños", "title": "AOC Alsace Grand Cru: Los 51 Terruños Históricos", "area": "Regiones de Francia", "focus": "Complejidad geológica mosaico bajo los Vosgos: granito de Schlossberg, caliza de Rangen, esquisto de Kastelberg"},
    {"id": "aoc_francia_champagne_montagne_reims_cote_blancs", "title": "Champagne: Montagne de Reims vs Côte des Blancs", "area": "Regiones de Francia", "focus": "Suelos de creta belemnita: Pinot Noir estructurado al norte vs pureza mineral de Chardonnay al sur"},
    {"id": "aoc_francia_champagne_vallee_marne_cote_bar", "title": "Champagne: Vallée de la Marne y Côte des Bar", "area": "Regiones de Francia", "focus": "Arcillas y arenas del Valle del Marne para Meunier vs margas kimmeridgienses del Aube para Pinot Noir"},
    {"id": "aoc_francia_jura_arbois_chateau_chalon", "title": "AOC Arbois y Château-Chalon", "area": "Regiones de Francia", "focus": "La cuna de Louis Pasteur, margas triásicas y la crianza oxidativa de Savagnin bajo levaduras indígenas"},
    {"id": "aoc_francia_savoie_chignin_bergeron", "title": "AOC Vin de Savoie: Chignin-Bergeron y Apremont", "area": "Regiones de Francia", "focus": "Desprendimiento histórico del Monte Granier (1248), calizas alpinas y variedades Jacquère y Roussanne"},
    {"id": "aoc_francia_corse_patrimonio_calvi", "title": "AOC Patrimonio y Vinos de Córcega", "area": "Regiones de Francia", "focus": "Calizas blancas de Patrimonio y granitos de Calvi para las variedades Nielluccio, Sciaccarello y Vermentinu"},
    {"id": "aoc_francia_banyuls_collioure", "title": "AOC Banyuls y Collioure: Terrazas de Esquisto sobre el Mar", "area": "Regiones de Francia", "focus": "Pirineo oriental que se sumerge en el Mediterráneo, Garnacha en soleras al aire libre (bonbonnes de cristal)"},
    {"id": "docg_italia_barolo_once_comunas", "title": "DOCG Barolo: Las Once Comunas y sus Fórmulas Geológicas", "area": "Regiones de Italia", "focus": "Margas de Sant'Agata (La Morra, Barolo) vs Areniscas de Diano (Monforte, Castiglione, Serralunga)"},
    {"id": "docg_italia_barbaresco_tres_pueblos", "title": "DOCG Barbaresco: Barbaresco, Neive y Treiso", "area": "Regiones de Italia", "focus": "Altitud moderada, mayor proximidad al río Tanaro y taninos más sedosos que Barolo"},
    {"id": "docg_italia_roero_arenas_nebbiolo_arneis", "title": "DOCG Roero: La Margen Izquierda del Tanaro", "area": "Regiones de Italia", "focus": "Arenas fósiles marinas amarillas y rocas arcillosas con Nebbiolo fragante y Arneis mineral"},
    {"id": "docg_italia_gattinara_ghemme_alto_piamonte", "title": "Gattinara y Ghemme: El Nebbiolo Volcánico del Alto Piamonte", "area": "Regiones de Italia", "focus": "El supervolcán fósil de Valsesia, suelos ácidos de pórfido y granito y Nebbiolo de gran tensión"},
    {"id": "docg_italia_amarone_della_valpolicella", "title": "DOCG Amarone della Valpolicella: Fruttai y Suelos Calizos", "area": "Regiones de Italia", "focus": "Los valles de Negrar, Marano y Fumane, calizas de Biancone y el secado de Corvina y Rondinella"},
    {"id": "docg_italia_soave_superiore_classico", "title": "DOCG Soave Superiore y el Terruño Volcánico", "area": "Regiones de Italia", "focus": "Basaltos oscuros volcánicos de Monteforte d'Alpone vs calizas de Soave para la uva Garganega"},
    {"id": "docg_italia_franciacorta_metodo_classico", "title": "DOCG Franciacorta: La Excelencia Espumosa de Lombardía", "area": "Regiones de Italia", "focus": "Anfiteatro morrénico glaciar al sur del Lago de Iseo, suelos de grava y categorías Satèn y Pas Dosé"},
    {"id": "docg_italia_chianti_classico_uga", "title": "DOCG Chianti Classico: Las 11 Unidades Geográficas Adicionales", "area": "Regiones de Italia", "focus": "Castellina, Gaiole, Radda, Greve, Panzano; contrastes de Alberese y Galestro en Sangiovese puro"},
    {"id": "docg_italia_brunello_di_montalcino", "title": "DOCG Brunello di Montalcino: Cinco Años de Crianza Canónica", "area": "Regiones de Italia", "focus": "Colina aislada protegida por el Monte Amiata, clon Sangiovese Grosso y dos años mínimos en roble"},
    {"id": "docg_italia_vino_nobile_di_montepulciano", "title": "DOCG Vino Nobile di Montepulciano", "area": "Regiones de Italia", "focus": "Areniscas y arenas pliocénicas al este de Montalcino y el clon Prugnolo Gentile"},
    {"id": "doc_italia_bolgheri_sassicaia", "title": "DOC Bolgheri y Sassicaia: El Nacimiento de los Supertoscanos", "area": "Regiones de Italia", "focus": "La franja costera de la Maremma toscana, gravas marítimas similares a Graves y Cabernet Sauvignon"},
    {"id": "docg_italia_taurasi_el_barolo_del_sur", "title": "DOCG Taurasi: El Aglianico Volcánico de Irpinia", "area": "Regiones de Italia", "focus": "Laderas apeninas a 700m de altitud en Campania, cenizas volcánicas del Vesubio y taninos indómitos"},
    {"id": "docg_italia_greco_di_tufo_fiano_avellino", "title": "DOCG Greco di Tufo y Fiano di Avellino", "area": "Regiones de Italia", "focus": "Toba calcárea rica en azufre para Greco mineral vs arcillas y cenizas volcánicas para Fiano floral"},
    {"id": "docg_italia_aglianico_del_vulture", "title": "DOCG Aglianico del Vulture Superiore", "area": "Regiones de Italia", "focus": "Laderas del volcán extinto Monte Vulture en Basilicata, tobas volcánicas y estructura monolítica"},
    {"id": "doc_italia_etna_rosso_bianco", "title": "DOC Etna: La Viticultura sobre el Volcán Activo", "area": "Regiones de Italia", "focus": "Coladas de lava de diferentes siglos, altitud de hasta 1.000m, Nerello Mascalese y Carricante"},
    {"id": "doc_italia_valle_d_aosta_viticultura_alpina", "title": "DOC Valle d'Aosta: Los Viñedos más Altos de Europa", "area": "Regiones de Italia", "focus": "Bajo el Mont Blanc a 1.200m sobre terrazas morrénicas, variedades Prié Blanc y Petit Rouge"},
    {"id": "doc_italia_trentino_alto_adige_contrastes", "title": "Alto Adige / Südtirol y Trentino", "area": "Regiones de Italia", "focus": "Dolomitas calizas, valles fluviales del Adige, pérgolas trentinas y uvas Schiava, Lagrein y Teroldego"},
    {"id": "doc_italia_collio_goriziano_ponca", "title": "DOC Collio Goriziano y Colli Orientali del Friuli: El Ponca", "area": "Regiones de Italia", "focus": "Flysch de arenisca y marga marina friulana (ponca), cuna de los mejores blancos complejos de Italia"},
    {"id": "doc_italia_vernaccia_di_san_gimignano", "title": "DOCG Vernaccia di San Gimignano: Primera DOC de Italia (1966)", "area": "Regiones de Italia", "focus": "Arcillas amarillas con fósiles marinos pliocénicos y la única DOCG blanca de la Toscana"},
    {"id": "docg_italia_conegliano_valdobbiadene_prosecco", "title": "DOCG Conegliano Valdobbiadene Prosecco Superiore", "area": "Regiones de Italia", "focus": "Colinas de pendiente extrema declaradas Patrimonio UNESCO, suelos de flysch y Glera seleccionada"},
    {"id": "doc_portugal_douro_baixo_cima_superior", "title": "DOC Douro: Las Tres Subregiones sobre Esquisto", "area": "Regiones de Europa", "focus": "Baixo Corgo (húmedo), Cima Corgo (el corazón del Oporto) y Douro Superior (cálido y seco)"},
    {"id": "doc_portugal_dao_meseta_granito", "title": "DOC Dão: La Meseta Protegida de Granito", "area": "Regiones de Europa", "focus": "Rodeada por las sierras de Estrela y Caramulo, suelos de granito meteorizado y Touriga Nacional fresca"},
    {"id": "doc_portugal_bairrada_arcillas_baga", "title": "DOC Bairrada: Barros Calcáreos y la Uva Baga", "area": "Regiones de Europa", "focus": "Influencia marítima atlántica directa, arcillas pesadas y la domesticación de los taninos de la Baga"},
    {"id": "doc_portugal_alentejo_ocho_subregiones", "title": "DOC Alentejo: De Portalegre a Reguengos", "area": "Regiones de Europa", "focus": "La sierra granítica fresca de São Mamede en Portalegre vs los llanos cálidos de esquisto del sur"},
    {"id": "doc_portugal_vinho_verde_moncao_melgaco", "title": "DOC Vinho Verde: Monção e Melgaço y el Alvarinho", "area": "Regiones de Europa", "focus": "Microclima interior del Miño protegido de vientos atlánticos directos sobre granito puro"},
    {"id": "doc_portugal_colares_arenas_pie_franco", "title": "DOC Colares: Las Arenas Inmunes a la Filoxera", "area": "Regiones de Europa", "focus": "Dunas litorales de Sintra batidas por el Atlántico, uva Ramisco plantada en zanjas profundas de arena"},
    {"id": "region_alemania_mosel_saar_ruwer", "title": "Mosel, Saar y Ruwer: Las Tres Caras del Riesling Alemán", "area": "Regiones de Europa", "focus": "El Saar gélido vs pendientes del Mittelmosel (Wehlener Sonnenuhr, Erdener Prälat) sobre pizarra azul"},
    {"id": "region_alemania_rheingau_paralelo_50", "title": "Rheingau: El Giro del Rin y las Pendientes al Sur", "area": "Regiones de Europa", "focus": "Donde el río Rin fluye de este a oeste durante 30 km, cuarcita de Taunus y el histórico Schloss Johannisberg"},
    {"id": "region_alemania_pfalz_bosque_haardt", "title": "Pfalz: La Extensión de los Vosgos y el Riesling Seco", "area": "Regiones de Europa", "focus": "La cordillera del Haardt protege de lluvias, calizas, basaltos y areniscas rojas con clima casi mediterráneo"},
    {"id": "region_alemania_rheinhessen_roter_hang", "title": "Rheinhessen y el Roter Hang de Nierstein", "area": "Regiones de Europa", "focus": "La ladera roja de arenisca pérmica rica en hierro sobre el Rin y el renacimiento de los secos de calidad"},
    {"id": "region_alemania_nahe_mosaico_geologico", "title": "Nahe: El Mosaico Geológico más Denso de Alemania", "area": "Regiones de Europa", "focus": "Más de 180 tipos de suelo en un estrecho valle: rocas volcánicas, pórfidos, calizas y pizarras"},
    {"id": "region_austria_wachau_steinfeder_federspiel_smaragd", "title": "Wachau: La Jerarquía de Madurez Natural del Danubio", "area": "Regiones de Europa", "focus": "Clasificación Vinea Wachau por alcohol natural sin chaptalización sobre terrazas de gneis Gföhl"},
    {"id": "region_austria_kamptal_kremstal_heiligenstein", "title": "Kamptal y Kremstal: El Cerro de Zöbinger Heiligenstein", "area": "Regiones de Europa", "focus": "Arenisca desértica pérmica con sedimentos volcánicos de 270 millones de años para Riesling sublime"},
    {"id": "region_austria_burgenland_neusiedlersee", "title": "Burgenland y el Lago Neusiedl: Nieblas Panónicas", "area": "Regiones de Europa", "focus": "Lago estepario de poca profundidad que genera humedad para Botrytis noble y suelos de pizarra en Leithaberg"},
    {"id": "region_hungria_tokaj_seis_variedades", "title": "Tokaj: Furmint, Hárslevelű y Sárgamuskotály", "area": "Regiones de Europa", "focus": "La cuna del primer vino botritizado documentado (1650), suelos de loess cálido y riolita volcánica"},
    {"id": "region_grecia_santorini_assyrtiko_pie_franco", "title": "Santorini: La Ceniza Volcánica y el Assyrtiko Prehistórico", "area": "Regiones de Europa", "focus": "Cepas de más de 400 años que renuevan raíces sin replantar, ausencia total de materia orgánica y acidez eléctrica"},
    {"id": "region_grecia_naoussa_amynteo_xinomavro", "title": "Naoussa y Amynteo: El Imperio del Xinomavro", "area": "Regiones de Europa", "focus": "Macedonia griega: laderas calizas y clima alpino continental para tintos de alta acidez y aromas de aceituna y tomate"},
    {"id": "region_georgia_kakheti_qvevri_8000_anos", "title": "Kakheti y los Qvevris de Georgia: 8.000 Años de Historia", "area": "Regiones de Europa", "focus": "Vasijas de arcilla enterradas con cera de abeja, contacto de 6 meses con pieles y raspón (Chacha) y Rkatsiteli"},
    {"id": "nuevo_mundo_napa_valley_rutherford_dust", "title": "Napa Valley: El Banco de Rutherford y el 'Rutherford Dust'", "area": "Nuevo Mundo", "focus": "Gravas aluviales al pie de las Mayacamas, taninos terrosos y finos característicos de Cabernet Sauvignon"},
    {"id": "nuevo_mundo_napa_valley_oakville", "title": "Napa Valley: Oakville y el Corredor Central", "area": "Nuevo Mundo", "focus": "To Kalon Vineyard, balance de nieblas marinas de San Pablo Bay y radiación solar perfecta"},
    {"id": "nuevo_mundo_napa_valley_howell_mountain", "title": "Napa Valley: Howell Mountain y los Viñedos sobre las Nieblas", "area": "Nuevo Mundo", "focus": "Viticultura a más de 600m en las Vaca Mountains, por encima de la capa de inversión marina, suelos volcánicos blancos"},
    {"id": "nuevo_mundo_napa_valley_stags_leap_district", "title": "Napa Valley: Stags Leap District y los Conos Aluviales", "area": "Nuevo Mundo", "focus": "Gravas volcánicas bajo las Stags Leap Palisades, radiación reflejada y Cabernet de tanino aterciopelado"},
    {"id": "nuevo_mundo_sonoma_russian_river_valley", "title": "Sonoma: Russian River Valley y la Niebla Pacífica", "area": "Nuevo Mundo", "focus": "Suelos aluviales de Goldridge, entrada de nieblas a través del Petaluma Gap y Pinot Noir/Chardonnay de referencia"},
    {"id": "nuevo_mundo_sonoma_coast_extreme", "title": "True Sonoma Coast y Fort Ross-Seaview", "area": "Nuevo Mundo", "focus": "Viñedos en crestas montañosas a pocos kilómetros del Océano Pacífico, clima marítimo gélido y acidez cortante"},
    {"id": "nuevo_mundo_oregon_willamette_dundee_hills", "title": "Oregon: Dundee Hills y los Suelos Rojos de Jory", "area": "Nuevo Mundo", "focus": "Basalto volcánico meteorizado rico en hierro, sombra de lluvia de las Coast Ranges y Pinot Noir elegante"},
    {"id": "nuevo_mundo_oregon_eola_amity_hills", "title": "Oregon: Eola-Amity Hills y el Viento del Van Duzer Corridor", "area": "Nuevo Mundo", "focus": "Brecha en las montañas costeras que canaliza vientos oceánicos fríos al atardecer, engrosando los hollejos"},
    {"id": "nuevo_mundo_washington_columbia_valley_red_mountain", "title": "Washington: Red Mountain y la Pendiente al Suroeste", "area": "Nuevo Mundo", "focus": "Inundaciones glaciares de Missoula, arenas eólicas sobre grava basáltica y Cabernet de gran concentración"},
    {"id": "nuevo_mundo_mendoza_gualtallary_altura", "title": "Mendoza: Gualtallary y los 1.600 Metros de Altitud", "area": "Nuevo Mundo", "focus": "Tupungato, Valle de Uco: arenas sobre gravas cubiertas de carbonato de calcio blanco y Malbec/Cabernet Franc etéreo"},
    {"id": "nuevo_mundo_mendoza_paraje_altamira", "title": "Mendoza: Paraje Altamira y el Cono Aluvial del Tunuyán", "area": "Nuevo Mundo", "focus": "Grandes rocas graníticas y calcáreas depositadas por el río, perfil mineral calcáreo y frescura tánica"},
    {"id": "nuevo_mundo_mendoza_las_compuertas_lujan", "title": "Mendoza: Las Compuertas y los Viñedos Centenarios de Luján de Cuyo", "area": "Nuevo Mundo", "focus": "1.050m a orillas del río Mendoza, cepas de pie franco de 1910 y Malbec clásico aterciopelado"},
    {"id": "nuevo_mundo_salta_cafayate_extrema_altitud", "title": "Salta: Cafayate y Molinos (Hasta 3.000m de Altitud)", "area": "Nuevo Mundo", "focus": "Los viñedos más altos del planeta: radiación UV extrema, hollejos gruesos y Torrontés aromático explosivo"},
    {"id": "nuevo_mundo_chile_casablanca_corriente_humboldt", "title": "Chile: Valle de Casablanca y la Corriente de Humboldt", "area": "Nuevo Mundo", "focus": "Nieblas matinales costeras (camanchaca), suelos de arcilla sobre granito descompuesto y Sauvignon Blanc frío"},
    {"id": "nuevo_mundo_chile_colchagua_apalta", "title": "Chile: Valle de Apalta en Colchagua", "area": "Nuevo Mundo", "focus": "Herradura montañosa protegida del viento sobre arenas graníticas: cuna de los mejores Carménère del mundo"},
    {"id": "nuevo_mundo_chile_itata_biobio_cepas_patrimoniales", "title": "Chile: Valles de Itata y Bío-Bío: Cepas Ancestrales", "area": "Nuevo Mundo", "focus": "Secano costero sin riego sobre granito y suelos volcánicos rojos: uva País y Cinsault centenarios en pie franco"},
    {"id": "nuevo_mundo_australia_barossa_valley_shiraz_centenario", "title": "Australia: Barossa Valley y las Cepas de 1843", "area": "Nuevo Mundo", "focus": "Suelos de arcilla roja y arenas profundas no filoxéricas con las cepas vivas de Shiraz más antiguas del planeta"},
    {"id": "nuevo_mundo_australia_eden_valley_riesling_altura", "title": "Australia: Eden Valley y el Riesling de Altura", "area": "Nuevo Mundo", "focus": "Colinas adyacentes a Barossa a 500m de altitud sobre esquisto y cuarzo: Riesling de lima, hueso y kerosene"},
    {"id": "nuevo_mundo_australia_mclaren_vale_geologia", "title": "Australia: McLaren Vale y la Geología de 500 Millones de Años", "area": "Nuevo Mundo", "focus": "Influencia del golfo de San Vicente, brisas marinas de la tarde y Shiraz y Garnacha de gran frescura"},
    {"id": "nuevo_mundo_australia_margaret_river_gravels", "title": "Australia: Margaret River y la Influencia del Océano Índico", "area": "Nuevo Mundo", "focus": "Península aislada en Western Australia sobre gravas lateríticas: Cabernet Sauvignon al estilo bordelés y Chardonnay"},
    {"id": "nuevo_mundo_australia_clare_valley_riesling", "title": "Australia: Clare Valley y los Callejones de Watervale y Polish Hill River", "area": "Nuevo Mundo", "focus": "Calizas rojas en Watervale vs pizarra y cuarzo en Polish Hill River para Riesling de acidez vibrante"},
    {"id": "nuevo_mundo_australia_yarra_valley_frescura", "title": "Australia: Yarra Valley y el Valle Superior", "area": "Nuevo Mundo", "focus": "Suelos rojos volcánicos y lodos aluviales en Victoria para Pinot Noir y Chardonnay de clase mundial"},
    {"id": "nuevo_mundo_nueva_zelanda_marlborough_wairau_awatere", "title": "Nueva Zelanda: Wairau Valley vs Awatere Valley en Marlborough", "area": "Nuevo Mundo", "focus": "Lecho aluvial de cantos rodados (greywacke) de Wairau vs Awatere seco y ventoso para Sauvignon Blanc punzante"},
    {"id": "nuevo_mundo_nueva_zelanda_hawkes_bay_gimblett", "title": "Nueva Zelanda: Hawke's Bay y Gimblett Gravels", "area": "Nuevo Mundo", "focus": "Antiguo cauce del río Ngaruroro: 800 hectáreas de grava profunda que retienen calor para Syrah y Burdeos blends"},
    {"id": "nuevo_mundo_sudafrica_stellenbosch_granito", "title": "Sudáfrica: Stellenbosch y las Montañas de Simonsberg y Helderberg", "area": "Nuevo Mundo", "focus": "Granitos profundamente meteorizados de 600 millones de años, brisas de False Bay y Cabernet/Pinotage de terruño"},
    {"id": "nuevo_mundo_sudafrica_swartland_revolution", "title": "Sudáfrica: Swartland y la Revolución de los Viñedos Viejos", "area": "Nuevo Mundo", "focus": "Suelos de esquisto de Riebeek Kasteel y granito de Paardeberg en secano estricto con Chenin Blanc y Syrah"},
    {"id": "nuevo_mundo_sudafrica_walker_bay_hemel_en_aarde", "title": "Sudáfrica: Hemel-en-Aarde (Cielo en la Tierra)", "area": "Nuevo Mundo", "focus": "Valle estrecho que canaliza corrientes antárticas frías sobre esquistos de Bokkeveld: Pinot Noir y Chardonnay supremos"},
    {"id": "dop_espana_valles_de_benavente", "title": "D.O.P. Valles de Benavente", "area": "Regiones de España", "focus": "Suelos aluviales, altitud media de 700m y Tempranillo/Prieto Picudo en Zamora"},
    {"id": "dop_espana_sierra_de_salamanca", "title": "D.O.P. Sierra de Salamanca", "area": "Regiones de España", "focus": "Rufete y Rufete Blanca en bancales sobre granito y pizarra en la Sierra de Francia"},
    {"id": "dop_espana_valtiendas_segovia", "title": "D.O.P. Valtiendas: Los Páramos Calizos de Segovia", "area": "Regiones de España", "focus": "Altitud superior a 900m sobre el nivel del mar, suelos cascajosos sobre lecho calcáreo y Tempranillo de maduración tardía"},
    {"id": "dop_espana_cebreros_terruños_gredos", "title": "D.O.P. Cebreros y el Macizo de Gredos", "area": "Regiones de España", "focus": "Garnachas viejas de altura (hasta 1100m), arenas graníticas y pizarras esquistosas"},
    {"id": "dop_espana_gran_canaria", "title": "D.O. Gran Canaria", "area": "Regiones de España", "focus": "Viticultura volcánica en picón, caldera de Bandama, Listán Negro y Tintilla"},
    {"id": "dop_espana_valle_de_guimar", "title": "D.O. Valle de Güímar", "area": "Regiones de España", "focus": "Vertiente sureste de Tenerife, viñedos hasta 1.400m de altitud, Listán Blanco aromático"},
    {"id": "dop_espana_uruztieta_bizkaiko_txakolina", "title": "D.O. Bizkaiko Txakolina", "area": "Regiones de España", "focus": "Clima atlántico húmedo, Hondarrabi Zuri y Hondarrabi Beltza, fermentaciones en lías y tinas de roble"},
    {"id": "dop_espana_getariako_txakolina_parras", "title": "D.O. Getariako Txakolina: El Empalizado Costero", "area": "Regiones de España", "focus": "Conducción en parral para alejar racimos de la humedad del suelo, acidez málica y carbónico natural"},
    {"id": "dop_espana_chacoli_de_alava", "title": "D.O. Arabako Txakolina", "area": "Regiones de España", "focus": "Valle de Ayala, mayor continentalidad respecto a la costa vasca y Hondarrabi Zuri Zerratia"},
    {"id": "dop_espana_plateresco_manchuela_bobal", "title": "D.O. Manchuela: El Feudo de la Bobal Centenaria", "area": "Regiones de España", "focus": "Vientos de Poniente y Levante, valles fluviales del Júcar y Cabriel, suelos calcáreo-arcillosos"},
    {"id": "aoc_francia_cotes_de_provence_subzonas", "title": "AOC Côtes de Provence: Sainte-Victoire y La Londe", "area": "Regiones de Francia", "focus": "Garnacha, Cinsault, Syrah y Rolle sobre calizas jurásicas y esquistos costeros cristalinos"},
    {"id": "aoc_francia_bandol_mourvedre_maritimo", "title": "AOC Bandol: Anfiteatros de Restanques Frente al Mediterráneo", "area": "Regiones de Francia", "focus": "Mínimo 50% Mourvèdre, suelos de areniscas y margas con fósiles marinos, crianza mínima obligatoria de 18 meses"},
    {"id": "aoc_francia_cassis_blancos_calcareos", "title": "AOC Cassis: Vinos Blancos de los Acantilados Calcáreos", "area": "Regiones de Francia", "focus": "Marsanne y Clairette sobre roca caliza blanca emergente marina, microclima protegido por el Cap Canaille"},
    {"id": "aoc_francia_bellet_colinas_niza", "title": "AOC Bellet: Los Viñedos Urbanos de Niza", "area": "Regiones de Francia", "focus": "Variedades indígenas Braquet, Fuella Nera (Folle Noire) y Rolle sobre pudingas alpinas"},
    {"id": "aoc_francia_palette_chateau_simone", "title": "AOC Palette: El Enclave Histórico de Aix-en-Provence", "area": "Regiones de Francia", "focus": "Microclima kárstico rodeado de colinas, exposición norte, más de 16 variedades históricas co-fermentadas"},
    {"id": "aoc_francia_patrimonio_corcega", "title": "AOC Patrimonio: Córcega Calcárea y Niellucciu", "area": "Regiones de Francia", "focus": "Suelos arcillocalcáreos de la cuenca de Saint-Florent, Niellucciu (Sangiovese) y Vermentino de gran mineralidad"},
    {"id": "aoc_francia_ajaccio_sciacaccarello", "title": "AOC Ajaccio: Esquistos y Granitos para la Sciacaccarello", "area": "Regiones de Francia", "focus": "Suelos graníticos degradados, aromas de maquia corsa, almendra y especias silvestres"},
    {"id": "docg_italia_barbaresco_crus_historicos", "title": "DOCG Barbaresco: Asili, Rabajà y Martinenga", "area": "Regiones de Italia", "focus": "Nebbiolo sobre margas de Sant'Agata Fossili (margas tortonianas), taninos más sedosos y afinamiento más temprano que Barolo"},
    {"id": "docg_italia_roero_arneis_arenas", "title": "DOCG Roero: Nebbiolo y Arneis sobre Areniscas Fósiles", "area": "Regiones de Italia", "focus": "Margen izquierda del río Tánaro, suelos sueltos arenosos del Plioceno, perfil aromático fragante"},
    {"id": "docg_italia_gattinara_ghemme_alto_piemonte", "title": "DOCG Gattinara y Ghemme: Nebbiolo Volcánico del Alto Piamonte", "area": "Regiones de Italia", "focus": "Spanna (Nebbiolo) sobre pórfidos volcánicos ácidos del supervolcán del Sesia, acidez electrizante"},
    {"id": "docg_italia_soave_superiore_crus_calcareos", "title": "DOCG Soave Superiore: Garganega en Terruños Basálticos de Monte Foscarino", "area": "Regiones de Italia", "focus": "Garganega y Trebbiano di Soave en suelos volcánicos oscuros e intercalaciones calcáreas de colina"},
    {"id": "docg_italia_valtellina_superiore_sforzato", "title": "DOCG Valtellina Superiore y Sfursat: El Nebbiolo de los Alpes", "area": "Regiones de Italia", "focus": "Chiavennasca cultivada en terrazas sobre roca metamórfica en el valle del Adda; técnica de appassimento para Sfursat"},
    {"id": "docg_italia_taurasi_aglianico_irpinia", "title": "DOCG Taurasi: El Barolo del Sur en Suelos Volcánicos de Campania", "area": "Regiones de Italia", "focus": "Aglianico en los Apeninos campanos, cenizas vesubianas y arcillas calcáreas, alta estructura tánica"},
    {"id": "docg_italia_fiano_di_avellino_lapilli", "title": "DOCG Fiano di Avellino: Toba Volcánica y Mineralidad Sulfurosa", "area": "Regiones de Italia", "focus": "Fiano cultivado sobre capas de piroclastos y tobas volcánicas, aromas de avellana tostada y gran capacidad de guarda"},
    {"id": "docg_italia_greco_di_tufo_azufre", "title": "DOCG Greco di Tufo: Minas de Azufre y Acidez Cortante", "area": "Regiones de Italia", "focus": "Subsuelo enriquecido en azufre fósil en torno al municipio de Tufo, estructura phenólica y acidez brillante"},
    {"id": "docg_italia_etna_contrade_lava", "title": "DOC Etna: El Mosaico de Contrade y Vides Pre-filoxéricas", "area": "Regiones de Italia", "focus": "Nerello Mascalese y Carricante sobre flujos de lava de diferentes eras geológicas (100 a 10.000 años), viticultura heroica en alberello"},
    {"id": "docg_italia_cerasuolo_di_vittoria_arena", "title": "DOCG Cerasuolo di Vittoria: La Única DOCG de Sicilia", "area": "Regiones de Italia", "focus": "Nero d'Avola (cuerpo y color) y Frappato (aroma floral y frescura) sobre arenas rojas calcáreas"},
    {"id": "vdp_alemania_grosse_lage_rheingau_mosel", "title": "Clasificación VDP Grosse Lage: Grandes Pagos Alemanes", "area": "Regiones de Centroeuropa", "focus": "Criterios estrictos de rendimiento (máx 50 hl/ha), selección manual, expresión de Einzellagen legendarios"},
    {"id": "dac_austria_wachau_steinfeder_federspiel_smaragd", "title": "Wachau DAC: Clasificación Histórica de Steinfeder a Smaragd", "area": "Regiones de Centroeuropa", "focus": "Niveles de madurez natural por Oechsle/KMW, terrazas de esquisto (Gföhl gneiss) y vientos catabáticos del bosque de Dunkelsteiner"},
    {"id": "dac_austria_kamptal_kremstal_loess", "title": "Kamptal y Kremstal DAC: Grüner Veltliner sobre Terrazas de Loess Profundo", "area": "Regiones de Centroeuropa", "focus": "El Loess eólico cuaternario frente a rocas primarias cristalinas en Heiligenstein y Gaisberg"},
    {"id": "regiones_hungria_tokaj_aszu_eszencia", "title": "Tokaj Aszú y Tokaji Eszencia: La Métrica de los Puttonyos y Botrytis", "area": "Regiones de Centroeuropa", "focus": "Furmint y Hárslevelű atacadas por Botrytis cinerea en confluencia del Bodrog y Tisza, niveles de azúcar residual >450 g/L en Eszencia"},
    {"id": "ava_usa_willamette_valley_sub_avas_jory", "title": "Willamette Valley AVA: Suelos Volcánicos Jory y Sedimentos Willakenzie", "area": "Regiones de América", "focus": "Pinot Noir en Dundee Hills, Eola-Amity Hills y Ribbon Ridge, influencia de los vientos marítimos por el corredor Van Duzer"},
    {"id": "ava_usa_walla_walla_valley_columbia", "title": "Walla Walla Valley AVA: Syrah y Cabernet en Suelos Basálticos", "area": "Regiones de América", "focus": "Lavas basálticas del Columbia River Basalt Group cubiertas de loess eólico y arenas de las inundaciones de Missoula"},
    {"id": "regiones_argentina_valle_de_uco_parajes_calcarios", "title": "Valle de Uco: Gualtallary, Paraje Altamira y San Pablo", "area": "Regiones de América", "focus": "Aluviones con gravas recubiertas de carbonato de calcio (calcáreo blanco), altitudes de 1.100 a 1.600m y Malbec de montaña"},
    {"id": "regiones_chile_limari_suelos_camanchaca", "title": "Valle del Limarí: Carbonato de Calcio y Niebla Camanchaca", "area": "Regiones de América", "focus": "Talinay y suelos ricos en conchuelas marinas fosilizadas, Chardonnay y Syrah con mineralidad salina"},
    {"id": "regiones_australia_mornington_peninsula_pinot", "title": "Mornington Peninsula: Pinot Noir y Chardonnay Marítimo de Victoria", "area": "Regiones de Oceanía", "focus": "Bañada por tres masas de agua (Port Phillip Bay, Western Port y Bass Strait), suelos de arcilla volcánica roja"},
    {"id": "regiones_sudafrica_swartland_revolution_granito", "title": "Swartland Revolution: Vides Viejas de Secano en el Paardeberg", "area": "Regiones de África", "focus": "Chenin Blanc y Syrah en vaso sobre granito descompuesto (koffieklip), mínima intervención y viticultura de secano extremo"},
]

STUDY_CARD_TOPICS = [
    # WSET 3: Factores Naturales, Regiones y Estilos (50)
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
    {"standard": "WSET3", "category": "Regiones de Alemania", "topic": "El sistema Prädikatswein: Kabinett, Spätlese, Auslese, Beerenauslese, Eiswein y Trockenbeerenauslese"},
    {"standard": "WSET3", "category": "Regiones de Alemania", "topic": "Rheingau y Pfalz: laderas orientadas al sur sobre el Rin, suelos y perfiles de Riesling"},
    {"standard": "WSET3", "category": "Regiones de Austria", "topic": "Wachau, Kamptal y Kremstal: Grüner Veltliner en terrazas fluviales y clasificación Steinfeder/Federspiel/Smaragd"},
    {"standard": "WSET3", "category": "Regiones de Sudáfrica", "topic": "Stellenbosch y Swartland: suelos graníticos antiguos, Chenin Blanc viejo y Pinotage de calidad"},
    {"standard": "WSET3", "category": "Regiones de Australia", "topic": "Barossa Valley vs Eden Valley: Shiraz potente de fondo de valle vs Riesling mineral de altura"},
    {"standard": "WSET3", "category": "Regiones de Australia", "topic": "Hunter Valley y Semillon: bajo alcohol (11%), alta acidez natural y evolución a tostados tras 10 años"},
    {"standard": "WSET3", "category": "Regiones de Nueva Zelanda", "topic": "Central Otago: la región vitivinícola más meridional del mundo y su perfil de Pinot Noir"},
    {"standard": "WSET3", "category": "Regiones de Estados Unidos", "topic": "Willamette Valley (Oregon): suelos volcánicos de Jory, influencia marina y Pinot Noir de estilo borgoñón"},
    {"standard": "WSET3", "category": "Regiones de Estados Unidos", "topic": "Columbia Valley (Washington): sombra de lluvia de las Cascades, riego por goteo y Merlot/Syrah"},
    {"standard": "WSET3", "category": "Regiones de España", "topic": "Ribera del Duero: altitud de 800m, oscilación térmica día/noche de 20°C y maduración fenólica"},
    {"standard": "WSET3", "category": "Regiones de España", "topic": "Bierzo y la uva Mencía: viñedos viejos en minifundio de ladera pizarrosa y climas atlántico-continental"},
    {"standard": "WSET3", "category": "Regiones de España", "topic": "Toro: cepas centenarias de Tinta de Toro en pie franco sobre suelos arenosos no filoxéricos"},
    {"standard": "WSET3", "category": "Regiones de Francia", "topic": "Burdeos margen izquierda vs derecha: Cabernet Sauvignon en gravas vs Merlot en arcillas"},
    {"standard": "WSET3", "category": "Regiones de Francia", "topic": "Alsacia: el efecto de barrera orográfica de los Vosgos, alta insolación y los 51 Grands Crus"},
    {"standard": "WSET3", "category": "Regiones de Francia", "topic": "Valle del Loira de este a oeste: Sancerre (Sauvignon), Vouvray (Chenin), Chinon (Cab Franc), Muscadet (Melon)"},
    {"standard": "WSET3", "category": "Regiones de Italia", "topic": "Toscana: Chianti Classico vs Brunello di Montalcino vs Bolgheri (Super Tuscan blends)"},
    {"standard": "WSET3", "category": "Regiones de Italia", "topic": "Piamonte: Nebbiolo en Barolo y Barbaresco vs Barbera d'Asti y Dolcetto d'Alba"},
    {"standard": "WSET3", "category": "Regiones de Italia", "topic": "Véneto: colinas de Soave (Garganega en suelos volcánicos) vs Valpolicella Corvina"},
    {"standard": "WSET3", "category": "Regiones de Grecia", "topic": "Santorini: poda en canasta kouloura contra vientos marinos, suelo volcánico y Assyrtiko mineral"},
    {"standard": "WSET3", "category": "Regiones de Hungría", "topic": "Tokaj-Hegyalja: confluencia de los ríos Bodrog y Tisza para nieblas de Botrytis y Furmint"},

    # CMS Deductive Tasting & Sommelier (50)
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
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata ciega de Viognier de Condrieu vs Gewürztraminer de Alsacia: textura viscosa y acidez baja"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Identificación de Garnacha de Gredos (granito y altitud) vs Garnacha de Châteauneuf-du-Pape"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Distinción de Barolo maduro vs Rioja Gran Reserva de más de 20 años: perfil tánico y color teja"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata deductiva de Torrontés de Salta vs Moscatel de Alejandría: terpenos y amargor final"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Deducción ciega de Tannat de Madiran (microoxigenado) vs Tannat de Uruguay (frutal y pulido)"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje para carnes rojas a la brasa con grasa infiltrada: polimerización tánica con saliva y grasa"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Armonía para platos con vinagretas y escabeches: por qué fallan los tintos y la solución con Manzanilla Pasada"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje molecular para chocolate amargo: vinos rancios, PX y Oporto Tawny 20 años"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje para ceviches y tiraditos de pescado blanco: acidez cítrica cortante con Sauvignon Blanc o Txakoli"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Protocolo de sustitución de copa cuando se derrama vino sobre la mantelería del cliente"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Servicio y orden de servicio en mesa según protocolo: anfitrión, señoras, caballeros y sentido horario"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Presentación de la etiqueta de la botella al comensal: postura corporal y anuncio de añada y bodega"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Identificación de notas de barniz y quitaesmaltes (acetato de etilo) en concentraciones sublegales"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Detección de contaminación por humo en el viñedo (Smoke Taint): guayacol y cresoles libres"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Deducción de crianza sobre lías (bâtonnage) vs crianza en barrica de roble nuevo en blancos"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Identificación de maceración carbónica mediante aromas de cinamato de etilo (plátano y chicle)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata de vinos envejecidos en ánfora de terracota: textura tánica granular y ausencia de vainilla"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Uso del lito de sumiller: técnicas de sujeción para no calentar la botella con la palma de la mano"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Control de goteo con corte de gota en el cuello de la botella sin accesorios plásticos"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Evaluación de la persistencia aromática (caudalías) como indicador determinante de calidad"}
,
    # ASI Global: Concurso Internacional, Servicio y Bebidas (25)
    {"standard": "ASI", "category": "Deontología de Sumiller", "topic": "Código deontológico y ética profesional en el servicio de vinos en restaurantes Michelin"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Protocolo oficial de decantación con vela de un vino tinto antiguo de más de 25 años con posos"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Clasificación de calidad del Sake según la tasa de pulido (Seimai-buai): Daiginjo vs Ginjo vs Junmai"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Temperaturas de servicio y copas adecuadas para diferentes tipos de Sake japonés"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Estilos de cerveza y fermentación: fermentación espontánea (Lambic/Gueuze) vs Ale vs Lager"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Sumillería del agua mineral: residuo seco a 180°C (TDS) y su maridaje con vinos tánicos y ácidos"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Diferencias de producción y legislación entre Tequila (100% Agave azul) y Mezcal tradicional"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Tipologías de Whisky: Single Malt escocés vs Irish Pot Still vs Kentucky Straight Bourbon"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Cognac vs Armagnac: métodos de destilación (doble alambique Charentais vs columna continua)"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Protocolo de servicio de una botella de formato Magnum (1,5 L) y Jeroboam (3 L) en mesa"},
    {"standard": "ASI", "category": "Física de la Cristalería", "topic": "Influencia del volumen de la copa y el estrechamiento de la chimenea en el desprendimiento de aromas"},
    {"standard": "ASI", "category": "Viticultura Sostenible", "topic": "Principios de la viticultura biodinámica: preparados 500 y 501, dinamización y calendario lunar"},
    {"standard": "ASI", "category": "Viticultura Sostenible", "topic": "Viticultura regenerativa: pastoreo en viñedo, cubiertas vegetales y eliminación de herbicidas"},
    {"standard": "ASI", "category": "Maridajes Clásicos", "topic": "El carro de quesos: armonías canónicas de quesos azules con vinos dulces nobles botritizados"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Servicio de puros habanos y su maridaje con vinos generosos (Oloroso, Tawny) y destilados añejos"},
    {"standard": "ASI", "category": "Fisiología Sensorial", "topic": "El receptor TRPV1 y la capsaicina: por qué el picante destruye la armonía con vinos de alto tanino y alcohol"},
    {"standard": "ASI", "category": "Fisiología Sensorial", "topic": "Efecto de la sal en el vino: supresión del amargor, reducción de la acidez percibida y realce de fruta"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Presentación canónica de la botella al comensal: postura corporal y anuncio de añada y bodega"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Inspección visual y olfativa del corcho antes de depositarlo en el platillo de servicio"},
    {"standard": "ASI", "category": "Cata de Competición", "topic": "La cuadrícula de cata en concursos internacionales de sumillería: tiempo, descriptores y nota comercial"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "El vermut y los vinos aromatizados: plantas amargas (artemisia), azúcar y ritual del aperitivo"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Sumillería del té: servicio y maridaje de tés Pu-erh, Oolong y verdes en la alta gastronomía"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Café de especialidad en sala: molienda al momento, agua filtrada y maridaje con petit fours"},
    {"standard": "ASI", "category": "Gestión de Bodega", "topic": "Sistemas de conservación de vino por copas mediante gas argón inerte y Coravin"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Resolución diplomática de quejas en mesa cuando un cliente rechaza una botella por TCA o temperatura"},

    # NUEVA SERIE MASTER: CMS Deductive Tasting & Hospitality (+50 Fichas)
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Deducción de Syrah de clima frío (Ródano Norte / Cornas) vs Shiraz de clima cálido (Barossa Valley)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Diferenciación de Cabernet Sauvignon de Napa Valley (Oakville) vs Burdeos Margen Izquierda (Pauillac)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata a ciegas de Pinot Noir: Willamette Valley (Oregon) vs Borgoña (Côte de Nuits) vs Central Otago (NZ)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Deducción de Sauvignon Blanc: Sancerre (sílex/mineral) vs Marlborough (maracuyá/espárrago) vs Pessac-Léognan (roble/Semillon)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata deductiva de Chardonnay: Chablis Premier Cru vs Meursault vs Russian River Valley (California)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Identificación de Riesling en cata ciega: Mosel (pizarra, baja graduación, azúcar residual) vs Alsacia Grand Cru (seco, cuerpo, hidrocarburo)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Chenin Blanc a ciegas: Vouvray sec vs Savennières (alta acidez, lana húmeda, membrillo) vs Swartland (cepas viejas)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Deducción de Albariño (Rías Baixas) vs Alvarinho (Vinho Verde Monção) vs Loureiro"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata ciega de Grüner Veltliner de Wachau (pimienta blanca, rábano) vs Furmint seco de Tokaj"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Diferenciación de uvas aromáticas blancas: Viognier (Condrieu) vs Gewürztraminer (Alsacia) vs Torrontés (Cafayate)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Deducción de Nebbiolo (Barolo/Barbaresco) vs Sangiovese (Brunello di Montalcino) vs Aglianico (Taurasi)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Identificación de Tempranillo: Rioja Gran Reserva clásico vs Ribera del Duero moderna vs Toro vs Douro (Tinta Roriz)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata de Garnacha: Priorat (llicorella, mineralidad férrea) vs Châteauneuf-du-Pape vs Sierra de Gredos (granito, etéreo)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata ciega de Malbec: Valle de Uco (Mendoza, altitud, violetas) vs Cahors (rústico, tanino duro, tinta)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Identificación de Cabernet Franc: Chinon / Bourgueil (hoja de tomate, grafito) vs Toscana / Bolgheri"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Deducción de Gamay de Beaujolais Cru (Moulin-à-Vent o Morgon) vs Pinot Noir de Borgoña genérica"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata ciega de Corvina de Amarone della Valpolicella vs Primitivo di Manduria: pasificación vs sobremaduración"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Identificación de Mencía de Bierzo (suelos de pizarra, fruta roja ácida, notas florales) vs Syrah de clima frío"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata ciega de Nerello Mascalese del Etna vs Nebbiolo de Piamonte vs Pinot Noir de Borgoña"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Diagnóstico de edad en vinos tintos: evolución del menisco (púrpura a teja/ámbar), pérdida de antocianos y polimerización tánica"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Diagnóstico de edad en vinos blancos: evolución del color pajizo a oro viejo/ámbar y desarrollo de aromas terciarios"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Detección de origen del roble: Roble Francés (grano fino, vainillina sutil, cedro, especias) vs Roble Americano (lactonas de coco, eneldo, grano abierto)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Identificación de fermentación con racimo entero (raspón / escobajo): notas herbales, té negro, pimienta blanca y taninos de tallo"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Deducción de crianza biológica bajo velo de flor vs crianza oxidativa: acetaldehído, frutos secos, sotolón"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata ciega de vinos fortificados: Oporto Vintage vs Oporto Tawny 20 Años vs Madeira Bual"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Diagnóstico sensorial de TCA (2,4,6-tricloroanisol) vs TBA (tribromoanisol) y su impacto en la supresión frutal"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Oxidación prematura en vinos blancos (Premox): causas químicas, falta de SO2 libre y marcadores olfativos"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Diferenciación de ácido acético (vinagre) frente a acetato de etilo (pegamento / disolvente) en la acidez volátil"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Compuestos azufrados pesados: sulfuro de hidrógeno (H2S), mercaptanos y disulfuros; cuándo es reversible y cuándo no"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Brettanomyces en detalle: 4-etilfenol (cuadra, sudor de caballo) vs 4-etilguayacol (clavo, especias) vs ácido isovalérico"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Gusto de luz (Lightstruck / Goût de lumière): foto-oxidación de riboflavina por exposición a rayos UV en botellas transparentes"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Contaminación por humo (Smoke Taint): glicósidos de guayacol y cresoles volátiles liberados por enzimas salivares"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Gusto de ratón (Mouse Taint / Goût de souris): tetrahidropiridinas en vinos naturales y su activación por pH salival alcalino"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Aroma a geranio: metabolización bacteriana del ácido sórbico en vinos dulces estabilizados"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje con alimentos amargos (alcachofas, endivias, cacao puro): por qué los taninos astringentes chocan y soluciones de sumiller"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje con platos de alta acidez cítrica y vinagres: la regla de que el vino debe igualar o superar la acidez del plato"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje con carnes grasas y ricas en colágeno (panceta, jarrete): papel de la acidez alta vs la estructura tánica limpiadora"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Efecto de la salazón sobre los taninos y la fruta: por qué el jamón ibérico o los quesos curados suavizan vinos ásperos"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Postres dulces con vinos secos: la trampa del Champagne Brut con tarta de boda y la regla del nivel de azúcar superior en la copa"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje con platos intensos en Umami (caldos de dashi, setas shiitake, trufa negra): vinos maduros con taninos polimerizados"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Comida picante y capsaicina (cocina tailandesa, mexicana): por qué el alcohol alto (>14%) y el tanino multiplican el ardor"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Armonía molecular para mariscos con alto contenido en yodo (ostras, percebes): acidez eléctrica, ausencia de roble y mineralidad marina"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Técnica de decantación con cesta y extracción de corchos frágiles o degradados con descorchador Durand o láminas Ah-So"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Termometría de servicio: rangos térmicos estrictos del CMS para espumosos, blancos ligeros, blancos con madera, tintos sutiles y tintos estructurados"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Manejo y transporte de bandeja de cristalería en sala: equilibrio, ergonomía y colocación sin ruidos"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Protocolo de atención al cliente ante la devolución de una botella dudosa o defectuosa con diplomacia de alto nivel"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Gestión del tiempo en el examen práctico de cata ciega CMS: distribución de los 4 minutos por copa"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Selección de copas según variedad y tipología: cáliz Borgoña vs Burdeos vs copa universal vs flauta tradicional"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Acondicionamiento y enjuague previo de copa (avinado) para eliminar olores a lavavajillas o celulosa"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Protocolo de apertura de vinos espumosos de alta presión sin emisión sonora y control del corcho"},

    # NUEVA SERIE MASTER: ASI Global Competition, Sommelier Floor & World Beverages (+50 Fichas)
    {"standard": "ASI", "category": "Cata de Competición", "topic": "Estructura formal de la ficha de cata ASI en finales mundiales: balance analítico, potencial de guarda y sugerencias gastronómicas precisas"},
    {"standard": "ASI", "category": "Cata de Competición", "topic": "Identificación a ciegas de destilados y licores del mundo en copa negra: graduación, materia prima base y método de destilación"},
    {"standard": "ASI", "category": "Cata de Competición", "topic": "Corrección de cartas de vino erróneas en pruebas de concurso ASI: detección de añadas imposibles, clasificaciones apócrifas y errores de AOC"},
    {"standard": "ASI", "category": "Cata de Competición", "topic": "Prueba de maridaje exprés en escenario: diseño en 8 minutos de una armonía completa para menú de 5 pases con justificación técnica"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Decantación oficial con vela cronometrada en concurso internacional: colocación de gueridón, encendido de cerilla y corte de cápsula"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Servicio ceremonial de Champagne en copa de vino blanco: llenado en dos tiempos para estabilizar espuma y temperatura"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Manejo y escanciado de botellas de gran formato (Magnum, Doble Magnum y Jeroboam) sin tocar el labio de la copa"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Protocolo de servicio a la mesa según la etiqueta ASI: orden de prelación (damas, homenajeados, caballeros y anfitrión) y movimiento horario"},
    {"standard": "ASI", "category": "Gestión de Bodega", "topic": "Condiciones climáticas de conservación en cava profesional: temperatura constante (12-14°C), higrometría (70-75%), ausencia de vibración y oscuridad"},
    {"standard": "ASI", "category": "Gestión de Bodega", "topic": "Ingeniería de la carta de vinos (Wine List Engineering): cálculo de márgenes (mark-up), rotación de existencias y prevención de referencias dormidas"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Clasificación de calidad del Sake según pulido de arroz (Seimai-buai): Junmai Daiginjo vs Ginjo vs Honjozo"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Métodos ancestrales de elaboración de Sake: Kimoto vs Yamahai (ácido láctico natural) vs Sokujo moderno"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Servicio y cristalería para Sake japonés: del choko tradicional a la copa Riedel de Daiginjo y temperaturas de servicio"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Cervezas de fermentación espontánea (Lambic, Gueuze, Kriek): levaduras salvajes, barricas centenarias y maridaje gastronómico"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Cervezas trapenses y de abadía belgas: alta densidad, azúcares candi, refermentación en botella y servicio en cáliz"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Estilos de cerveza IPA: West Coast (amargor resinoso y seco) vs New England Hazy IPA (turbidez, baja astringencia y fruta tropical)"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Sidra natural del mundo: Sagardoa vasca (escanciado en txotx) vs Sidra asturiana vs Cidre bouché normando"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Sumillería de las aguas minerales: residuo seco a 180°C (mineralización muy débil vs fuerte), balance de bicarbonatos y maridaje con acidez y taninos"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Regiones del Whisky escocés: Islay (turba, yodo, humo medicinal) vs Speyside (fruta, miel, barrica de jerez) vs Highlands"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Bourbon vs Rye Whiskey estadounidense: composición del grano (51%+ maíz vs centeno), barricas de roble virgen carbonizado y envejecimiento"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Cognac vs Armagnac: terruños (Grande Champagne vs Bas-Armagnac), destilación doble Charentais vs alambique continuo y perfiles de crianza"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Mezcal artesanal y ancestral: horneado en pozo de tierra, destilación en ollas de barro y variedades de agave silvestre (Tobalá, Tepeztate)"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Tequila 100% puro de agave: fermentación y diferencias organolépticas entre Blanco, Reposado, Añejo y Extra Añejo"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Rhum Agricole de las Antillas francesas (AOC Martinique) elaborado con jugo directo de caña vs ron industrial de melazas"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Ginebra: London Dry (sin adición de aromas tras destilación ni azúcar) vs Plymouth vs Old Tom vs Genever holandesa"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Calvados Pays d'Auge AOC (doble destilación en alambique de cobre) vs Calvados Domfrontais (mínimo 30% peras)"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Aguardientes de frutas (Eaux-de-vie): Kirsch, Poire Williams, Mirabelle y Framboise; destilación y servicio frío pero sin hielo"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Pisco peruano (destilación directa a grado sin agua, mosto verde y aromáticas) vs Pisco chileno (doble destilación y madera)"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Grappa italiana de monovarietal (Nebbiolo, Moscato) vs Orujo gallego tradicional: control del destilado y pureza de cabeza y cola"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Licores amargos y botánicos: Amaro italiano (Fernet, Montenegro, Nonino), digestivos y su función aperitiva"},
    {"standard": "ASI", "category": "Infusiones & Café", "topic": "Sumillería del té en la alta gastronomía: fermentación de hojas de té (Verde, Blanco, Oolong, Negro, Pu-erh) y sus temperaturas de infusión"},
    {"standard": "ASI", "category": "Infusiones & Café", "topic": "Protocolo de maridaje de té con quesos y carnes: astringencia de taninos de té negro vs cremosidad láctica"},
    {"standard": "ASI", "category": "Infusiones & Café", "topic": "Café de especialidad (Specialty Coffee): variedades Arábica (Geisha, Bourbon, Typica), beneficio por lavado vs natural y ratios de extracción"},
    {"standard": "ASI", "category": "Infusiones & Café", "topic": "El agua como solvente en la extracción de café: dureza total, alcalinidad y su impacto en la brillantez aromática"},
    {"standard": "ASI", "category": "Vinos Fortificados & Aromatizados", "topic": "Vinos aromatizados y Vermut: papel de las plantas amargas (Artemisia absinthium), quina, genciana y especias en sala"},
    {"standard": "ASI", "category": "Vinos Fortificados & Aromatizados", "topic": "Barolo Chinato: maceración de Nebbiolo con corteza de quina calisaya, ruibarbo y especias; servicio como vino de meditación"},
    {"standard": "ASI", "category": "Vinos Fortificados & Aromatizados", "topic": "Vinos de licor tradicionales: Banyuls, Maury, Rivesaltes y el método de mutage con alcohol para preservar azúcar natural"},
    {"standard": "ASI", "category": "Vinos Fortificados & Aromatizados", "topic": "Marsala de Sicilia: clasificaciones según envejecimiento (Fine, Superiore, Vergine, Soleras) y contenido de azúcar residual"},
    {"standard": "ASI", "category": "Vinos Fortificados & Aromatizados", "topic": "Rutherglen Muscat de Australia: uva Brown Muscat, añejamiento en barricas expuestas al calor y sistema de soleras"},
    {"standard": "ASI", "category": "Viticultura & Sostenibilidad", "topic": "Certificaciones medioambientales internacionales: Demeter (biodinámica), Biodyvin, Ecocert orgánico y normativas HVE"},
    {"standard": "ASI", "category": "Viticultura & Sostenibilidad", "topic": "Viticultura regenerativa y resiliencia climática: cubiertas vegetales permanentes, integración de ganado y captura de carbono"},
    {"standard": "ASI", "category": "Viticultura & Sostenibilidad", "topic": "Impacto de la huella de carbono en la sumillería: peso del vidrio de las botellas, transportes sostenibles y formatos alternativos"},
    {"standard": "ASI", "category": "Deontología de Sumiller", "topic": "Código deontológico internacional de la ASI: independencia frente a bodegas, confidencialidad del cliente y trato igualitario"},
    {"standard": "ASI", "category": "Deontología de Sumiller", "topic": "Gestión de alérgenos y legislación en el servicio: sulfitos (>10 mg/L), clarificantes de origen animal (albúmina, caseína) y veganismo"},
    {"standard": "ASI", "category": "Fisiología Sensorial", "topic": "Fatiga sensorial en catadores profesionales: causas neurosensoriales de adaptación olfativa y estrategias de recuperación en sala"},
    {"standard": "ASI", "category": "Fisiología Sensorial", "topic": "La interacción trigeminal en la boca: temperatura, astringencia, acidez y alcohol percibidos a través del nervio trigémino"},
    {"standard": "ASI", "category": "Física de la Cristalería", "topic": "Efecto de la composición del cristal (cristal de plomo vs cristal de titanio) en la adherencia y oxigenación del vino"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Servicio de puros habanos en alta gastronomía: conservación en humidor (70% humedad), corte limpio con guillotina y encendido sin gasolina"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Manejo del Coravin y sistemas de aguja: purga previa de oxígeno, inyección de gas argón grado alimentario y conservación posterior"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Protocolo para la gestión de mesas de grandes dignatarios o eventos de estado según los estándares de la ASI"},



    # ==========================================================================
    # NUEVA SERIE MASTER FLASHCARDS (+100 Fichas: WSET3/Diploma, CMS Master, ASI Global)
    # ==========================================================================
    {"standard": "WSET3", "category": "Cambio Climático & Viticultura", "topic": "Impacto del calentamiento global en la maduración fenólica vs azúcares y caída de ácido málico"},
    {"standard": "WSET3", "category": "Cambio Climático & Viticultura", "topic": "Estrategias de adaptación en el viñedo: orientación de hileras, aumento de altura de canopia y mallas de sombreo"},
    {"standard": "WSET3", "category": "Sistemas de Clasificación", "topic": "La clasificación VDP alemana: Gutswein, Ortswein, Erste Lage y Grosse Lage"},
    {"standard": "WSET3", "category": "Sistemas de Clasificación", "topic": "Las Unidades Geográficas Adicionales (UGA) de Chianti Classico y la categoría Gran Selezione"},
    {"standard": "WSET3", "category": "Sistemas de Clasificación", "topic": "El sistema En Primeur de Burdeos: mecánica financiera de la Place de Bordeaux y campañas de primavera"},
    {"standard": "WSET3", "category": "Enología de Precisión", "topic": "Fermentación con racimo entero (whole bunch) vs despalillado: impacto en taninos, pH y frescura"},
    {"standard": "WSET3", "category": "Enología de Precisión", "topic": "Maceración prefermentativa en frío (Cold Soak): extracción de color acuosa sin extracción alcohólica de semillas"},
    {"standard": "WSET3", "category": "Enología de Precisión", "topic": "Selección del nivel de tostado de la barrica (Ligero, Medio, Plus) y liberación de furfural, guayacol y eugenol"},
    {"standard": "WSET3", "category": "Tecnología de Cierres", "topic": "Tipos de cierre: Corcho natural, técnico microgranulado (Diam), tapón de rosca (Stelvin) y tapón de cristal (Vinolok)"},
    {"standard": "WSET3", "category": "Regiones del Nuevo Mundo", "topic": "Patagonia vitivinícola (Río Negro y Neuquén): vientos secos, alta radiación UV y Pinot Noir mineral"},
    {"standard": "WSET3", "category": "Regiones del Nuevo Mundo", "topic": "Tasmania (Coal River y Tamar Valley): clima marítimo frío extremo, acidez natural y base de espumosos"},
    {"standard": "WSET3", "category": "Regiones del Nuevo Mundo", "topic": "Washington State (Horse Heaven Hills y Red Mountain): 300 días de sol, acumulación térmica y Cabernet tánico"},
    {"standard": "WSET3", "category": "Regiones del Nuevo Mundo", "topic": "Sudáfrica (Hemel-en-Aarde): influencia antártica de la corriente de Benguela y Pinot Noir/Chardonnay de terruño"},
    {"standard": "WSET3", "category": "Regiones de Europa", "topic": "Grecia (Naoussa): clima continental montañoso y la uva Xinomavro de alta acidez y estructura similar a Nebbiolo"},
    {"standard": "WSET3", "category": "Regiones de Europa", "topic": "Portugal (Dão): meseta rodeada de montañas graníticas, uva Touriga Nacional elegante y Encruzado mineral"},
    {"standard": "WSET3", "category": "Regiones de Europa", "topic": "Italia (Etna DOC): pendientes volcánicas del estrato-volcán activo, cepas en pie franco (alberello) y Carricante"},
    {"standard": "WSET3", "category": "Regiones de Europa", "topic": "Francia (Jura): clima semicontinental riguroso, calizas del Lias y la elaboración de Savagnin y Poulsard"},
    {"standard": "WSET3", "category": "Regiones de España", "topic": "Ribeira Sacra: viticultura heroica en terrazas del Sil y Miño, suelos de pizarra y Mencía fresca"},
    {"standard": "WSET3", "category": "Regiones de España", "topic": "Canarias (Valle de la Orotava y La Geria): cordón trenzado tradicional, hoyos en lapilli volcánico y pie franco"},
    {"standard": "WSET3", "category": "Regiones de España", "topic": "Sierra de Gredos: altitud superior a 900m, arenas graníticas degradadas y Garnachas etéreas"},
    {"standard": "WSET3", "category": "Regiones de España", "topic": "Montilla-Moriles: crianza biológica natural con Pedro Ximénez sin necesidad de fortificación (15% natural)"},
    {"standard": "WSET3", "category": "Regiones de España", "topic": "Empordà: influencia de la Tramuntana como desecante fúngico y suelos de pizarra y granito"},
    {"standard": "WSET3", "category": "Vinos Espumosos", "topic": "Diferencias técnicas entre Franciacorta, Cava y Champagne: variedades autorizadas y meses mínimos en rima"},
    {"standard": "WSET3", "category": "Vinos Espumosos", "topic": "El Método Ancestral (Pét-Nat): embotellado antes de concluir la primera fermentación sin licor de tiraje"},
    {"standard": "WSET3", "category": "Vinos Fortificados", "topic": "Madeira: estilos por casta tradicional según dulzor (Sercial seco, Verdelho semisecco, Bual semidulce, Malmsey dulce)"},
    {"standard": "WSET3", "category": "Vinos Fortificados", "topic": "Palo Cortado: accidente enológico tradicional y definición normativa moderna en el Consejo Regulador"},
    {"standard": "WSET3", "category": "Química del Envejecimiento", "topic": "Evolución de los taninos condensados: hidrólisis ácida, polimerización y precipitación de posos en botella"},
    {"standard": "WSET3", "category": "Química del Envejecimiento", "topic": "Oxigenación a través del tapón: Tasa de Transmisión de Oxígeno (OTR) en diferentes cierres"},
    {"standard": "WSET3", "category": "Factores Naturales", "topic": "Aspecto y pendiente: por qué las laderas orientadas al sur maximizan la insolación en el hemisferio norte"},
    {"standard": "WSET3", "category": "Factores Naturales", "topic": "Efecto moderador de grandes masas de agua: reducción de oscilación térmica y retardo de heladas otoñales"},
    {"standard": "WSET3", "category": "Suelos & Nutrición", "topic": "Clorosis férrica en suelos calizos: bloqueo del hierro por exceso de carbonato cálcico y uso de portainjertos específicos"},
    {"standard": "WSET3", "category": "Suelos & Nutrición", "topic": "Capacidad de Intercambio Catiónico (CIC) y disponibilidad de potasio, magnesio y nitrógeno para la vid"},
    {"standard": "WSET3", "category": "Bioquímica de la Uva", "topic": "Cinética de acumulación de antocianos y descomposición del ácido málico durante el envero"},
    {"standard": "WSET3", "category": "Bioquímica de la Uva", "topic": "Los precursores aromáticos conjugados con glutatión y cisteína (tioles varietales 3MH y 3MHA)"},
    {"standard": "WSET3", "category": "Control de Calidad", "topic": "La turbidez del mosto en NTU: rango óptimo para fermentación limpia en blancos aromáticos"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Deducción a ciegas: Pomerol / Saint-Émilion (Merlot de arcilla/grava) vs Merlot de Toscana / Bolgheri"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata deductiva de Semillon de Hunter Valley: perfil cítrico punzante joven vs evolución tostada a cera de abeja a los 10 años"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Diferenciación entre Gamay de Beaujolais Cru, Mencía de Bierzo y Schiava de Alto Adige"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata comparativa a ciegas: Tannat de Madiran vs Sagrantino di Montefalco vs Petit Verdot"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Deducción ciega de Chardonnay: Yarra Valley / Mornington Peninsula vs Meursault borgoñón"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Diferenciación de Garnacha de Sierra de Gredos (granito y tensión) vs Pinot Noir de Gevrey-Chambertin"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata deductiva de Chenin Blanc: Swartland (cepas viejas y sol) vs Vouvray sec (acidez y tiza)"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Identificación de Riesling Kabinett de Mosel vs Spätlese trocken de Rheingau: azúcar residual vs extracto seco"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Anomalías estructurales en cata deductiva: alcohol alto con acidez alta en Amarone della Valpolicella"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Identificación en copa de vinos elaborados en ánfora / tinaja: textura terrosa, tanino fino en blancos orange y ausencia de roble"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Deducción ciega de Carménère chileno vs Cabernet Franc del Loira: notas de pimiento asado vs grafito y frambuesa"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata a ciegas de Fiano di Avellino vs Greco di Tufo: avellana y textura cremosa vs acidez cortante y mineralidad volcánica"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Diferenciación de Barbaresco joven vs Barolo joven: taninos pulidos y menor extracción frente a austeridad tánica"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Cata ciega de Torrontés de Salta vs Moscatel de grano menudo: perfumado terpénico sin amargor desequilibrado"},
    {"standard": "CMS", "category": "Deductive Tasting Grid", "topic": "Identificación de Syrah de Ródano Norte (Saint-Joseph / Cornas) mediante notas de aceituna negra, carne ahumada y violetas"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Detección sensorial de Tribromoanisol (TBA) procedente de maderas de bodega tratadas con fungicidas halogenados"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Diagnóstico diferencial de reducción reversible con agitación o cobre frente a mercaptanos pesados irreversibles"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Contaminación por mariquitas (Harmonia axyridis / IPMP): sabor rancio a cacahuete y espárrago crudo"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Química de la maderización y cómo distinguirla de una crianza oxidativa intencionada en vinos rancios"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Aroma a pegamento de modelismo (acetato de etilo) en combinación con ácido acético: el umbral de rechazo"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje con carnes de caza de pluma (pichón, perdiz): afinidad con notas terciarias de caza de vinos con evolución"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje con pescados grasos (atún rojo, salmón a la brasa): tintos ligeros con poco tanino o blancos con crianza sobre lías"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "La regla de la salsa en el maridaje: por qué la salsa determina el vino con mayor peso que la proteína base"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje con platos ahumados: por qué la madera tostada y la Syrah armonizan molecularmente con el humo"},
    {"standard": "CMS", "category": "Maridaje Deductivo", "topic": "Maridaje con quesos de cabra jóvenes y curados: acidez cítrica cortante de Sauvignon Blanc vs frutos secos de Amontillado"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Técnica de corte de cápsula bajo el anillo inferior (cavage) para evitar que el vino entre en contacto con el metal"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Uso del descorchador de láminas gemelas (Ah-So) en corchos reblandecidos o pegados a la pared del cuello"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Acondicionamiento térmico de emergencia en sala: uso de cubitera con agua, hielo y sal para descenso rápido"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Protocolo de cata de la primera copa por parte del sumiller antes del servicio al comensal en restaurantes 3 estrellas"},
    {"standard": "CMS", "category": "Servicio de Sala", "topic": "Manejo del carrito de destilados y protocolo de servicio de licores digestivos en copa tulipa a temperatura adecuada"},
    {"standard": "CMS", "category": "Física de la Cristalería", "topic": "La curvatura del borde de la copa y su impacto en la dirección del flujo líquido hacia el dorso o punta de la lengua"},
    {"standard": "CMS", "category": "Física de la Cristalería", "topic": "Por qué las copas sopladas a mano ultra-finas mejoran la percepción organoléptica frente al vidrio prensado grueso"},
    {"standard": "CMS", "category": "Psicología de Mesa", "topic": "Lectura psicológica del cliente y asesoramiento del vino respetando presupuestos implícitos con elegancia"},
    {"standard": "CMS", "category": "Psicología de Mesa", "topic": "Gestión de desacuerdos entre comensales al elegir vino para platos antagónicos: selección de vinos puente versátiles"},
    {"standard": "CMS", "category": "Gestión de Bodega", "topic": "Elaboración de una carta de vinos rentable: matriz Boston Consulting Group (Estrellas, Vacas, Perros e Interrogantes)"},
    {"standard": "ASI", "category": "Competición Internacional", "topic": "La prueba de identificación sensorial a ciegas en copa negra: graduación alcohólica, destilado base y origen"},
    {"standard": "ASI", "category": "Competición Internacional", "topic": "Detección de cartas de vinos manipuladas: corrección de AOC erróneas, añadas inexistentes y bodegas mal clasificadas"},
    {"standard": "ASI", "category": "Competición Internacional", "topic": "Prueba de maridaje relámpago con menú sorpresa de 5 platos: justificación de armonías en 6 minutos ante el jurado"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Protocolo de decantación con vela cronometrado: preparación del velador, limpieza de botella y trasiego continuo"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Servicio de espumosos en copa de cata amplia: por qué la flauta tradicional ha sido desterrada de los concursos ASI"},
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Protocolo de escanciado simultáneo de una botella en 12 copas con dosificación idéntica y sin retorno de gota"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Sake Awasake (Sake Espumoso de fermentación natural): normativa oficial y armonía gastronómica"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Koshu: el sake envejecido tradicional de color ámbar y notas de caramelo, setas y salsa de soja"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "Cervezas Geuze Oude: mezcla de lambics de 1, 2 y 3 años con refermentación en botella y acidez acética/láctica"},
    {"standard": "ASI", "category": "Bebidas del Mundo", "topic": "El servicio de la sidra natural en sala: métodos de escanciado y oxigenación para liberar carbónico endógeno"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Identificación de estilos de Ron: Ron de melaza estilo inglés (Navy/Jamaica) vs estilo hispano vs Rhum Agricole"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Armagnac: tipología de añadas y envejecimiento (Hors d'Âge, Vintage millésimé) en roble negro de Gascuña"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Whisky japonés: influencia del roble Mizunara (sándalo e incienso), aguas de deshielo alpino y mezclas de malta"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Pisco peruano Puro vs Acholado vs Mosto Verde: destilación discontinua en falca y reposo en recipientes inertes"},
    {"standard": "ASI", "category": "Destilados del Mundo", "topic": "Aguardientes de orujo y grappa: destilación al baño maría vs alambique tradicional y monovarietales aromáticos"},
    {"standard": "ASI", "category": "Infusiones & Café", "topic": "Té blanco Silver Needle (Bai Hao Yin Zhen): marchitamiento suave, secado al sol y maridaje con pescados delicados"},
    {"standard": "ASI", "category": "Infusiones & Café", "topic": "Té Gyokuro japonés: técnica de sombreado previo de tres semanas, riqueza en teanina y explosión de Umami"},
    {"standard": "ASI", "category": "Infusiones & Café", "topic": "Té Oolong de roca Wuyi (Da Hong Pao): oxidación media, tostado al carbón y armonía con carnes asadas"},
    {"standard": "ASI", "category": "Infusiones & Café", "topic": "Café Geisha de Panamá y Etiopía: procesos anaeróbicos, notas florales de jazmín y servicio en copa de vino"},
    {"standard": "ASI", "category": "Infusiones & Café", "topic": "El refractómetro en café de especialidad: cálculo del Total de Sólidos Disueltos (TDS) y porcentaje de extracción"},
    {"standard": "ASI", "category": "Sumillería de Aguas", "topic": "Mineralización del agua y su impacto en sala: aguas de alta salinidad y gas natural con platos cárnicos intensos"},
    {"standard": "ASI", "category": "Sumillería de Puros", "topic": "Anatomía de un cigarro puro: Capa, Capote y Tripa (Ligero, Seco, Volado) y su conservación higrométrica"},
    {"standard": "ASI", "category": "Sumillería de Puros", "topic": "Corte de puro: corte recto vs punzón (punch) vs corte en V y su impacto en la concentración de humo"},
    {"standard": "ASI", "category": "Gestión de Bodega", "topic": "Control de temperatura e higrometría en cavas de guarda: riesgo de mohos en corcho a >80% y secado a <60%"},
    {"standard": "ASI", "category": "Gestión de Bodega", "topic": "Cálculo del Beverage Cost: coste de compras vs inventario final y estrategias de reducción de mermas"},
    {"standard": "ASI", "category": "Deontología Profesional", "topic": "Código deontológico ASI: principios de honestidad comercial, neutralidad de marca y respeto a la privacidad"},
    {"standard": "ASI", "category": "Deontología Profesional", "topic": "El sumiller como embajador de la sostenibilidad: selección de productores con baja huella de carbono y regeneración"},
    {"standard": "ASI", "category": "Gestión de Conflictos", "topic": "Gestión diplomática ante mesas de estado: protocolo de seguridad alimentaria, verificación de alérgenos y etiqueta diplomática"},
    {"standard": "ASI", "category": "Gestión de Conflictos", "topic": "Resolución de derrames accidentales en sala: sustitución inmediata de cubertería, secado con muletón y calma protocolaria"},
    {"standard": "ASI", "category": "Fisiología y Salud", "topic": "El metabolismo del alcohol por la enzima alcohol deshidrogenasa (ADH) y pautas de hidratación y moderación en el servicio"},

    # --- Expansión a 1,450 Fichas: WSET Diploma, Master Sommelier y ASI World (+225) ---
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "Manejo del dosel vegetal mediante deshojado basal para optimizar la exposición solar de pirazinas y prevenir botrytis"},
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "Uso de portainjertos resistentes a sequía (110R, 140Ru) versus portainjertos reductores de vigor (Riparia Gloire)"},
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "Índice de Huglin y su correlación con la suma térmica requerida para la maduración fenólica completa"},
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "Efectos fisiológicos del estrés hídrico regulado (RDI) en la síntesis de antocianos y polifenoles en uvas tintas"},
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "Impacto de la poda tardía de invierno como estrategia de adaptación ante heladas primaverales tardías"},
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "Manejo de cubiertas vegetales permanentes versus laboreo: competencia por nitrógeno y agua en viñedos vigorosos"},
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "Mapeo de vigor mediante índice NDVI con drones para vendimias diferenciales de precisión"},
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "Técnicas de aclareo de racimos (vendimia en verde): momento óptimo en el envero y equilibrio de rendimiento"},
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "Efecto de la orientación de las hileras (Norte-Sur vs Este-Oeste) sobre el golpe de calor y la preservación de ácido málico"},
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "Fisiología del marchitamiento del racimo (waterberry / bunch stem necrosis) asociado a desequilibrios de potasio y magnesio"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Química de la reducción enológica: formación de sulfuro de hidrógeno (H2S) y mercaptanos volátiles por deficiencia de YAN"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Uso de levaduras no-Saccharomyces (Torulaspora delbrueckii, Metschnikowia pulcherrima) en bio-protección prefermentativa"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Fermentación espontánea con levaduras indígenas versus inoculación con cepas seleccionadas de Saccharomyces cerevisiae"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Maceración carbónica estricta versus semi-carbónica en Beaujolais: enzimas intracelulares y ésteres aromáticos"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Termovinificación y flash-détente: principios térmicos de extracción rápida y riesgos de pérdida de tipicidad varietal"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Microoxigenación (MOX) en vinos tintos: cinética de polimerización tanino-antociano y estabilización del color"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Estabilización tartárica mediante carboximetilcelulosa (CMC) y poliaspartato de potasio versus choque térmico en frío"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Factores que desencadenan la fermentación maloláctica en barrica: temperatura, pH, SO2 libre y cepas de Oenococcus oeni"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Composición de manoproteínas parietales de levaduras durante la crianza sobre lías finas y battonage"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Química de la oxidación enzimática (polifenol oxidasa / tirosinasa) y no enzimática (oxidación fenton mediada por hierro y cobre)"},
    {"standard": "WSET3", "category": "Regiones & Terruños", "topic": "Suelos calcáreos de Kimmeridgiense en Chablis Grand Cru versus Portlandiense en Petit Chablis"},
    {"standard": "WSET3", "category": "Regiones & Terruños", "topic": "Régimen pluviométrico y efecto sombra de lluvia de la Cordillera de los Vosgos en los viñedos de Alsacia"},
    {"standard": "WSET3", "category": "Regiones & Terruños", "topic": "Estratigrafía del suelo en la Côte d'Or: margas del Jurásico y calizas oolíticas en Côte de Nuits vs Côte de Beaune"},
    {"standard": "WSET3", "category": "Regiones & Terruños", "topic": "Los suelos de esquisto azul (Blauschiefer) en los viñedos empinados de Wehlener Sonnenuhr en Mosel"},
    {"standard": "WSET3", "category": "Regiones & Terruños", "topic": "Topoclimas y suelos volcánicos del Somló y Tokaj en Hungría: impacto en la frescura y longevidad del Furmint"},
    {"standard": "WSET3", "category": "Regiones & Terruños", "topic": "Los cantos rodados (galets roulés) en Châteauneuf-du-Pape y su función termorreguladora nocturna"},
    {"standard": "WSET3", "category": "Regiones & Terruños", "topic": "El papel del viento Mistral en el Valle del Ródano meridional: deshidratación, sanidad fúngica y estrés mecánico"},
    {"standard": "WSET3", "category": "Regiones & Terruños", "topic": "Valle de Casablanca en Chile: corriente fría de Humboldt, camanchaca costera y tipicidad del Sauvignon Blanc"},
    {"standard": "WSET3", "category": "Regiones & Terruños", "topic": "Suelos de terra rossa sobre piedra caliza en Coonawarra: drenaje, retención de agua y Cabernet Sauvignon"},
    {"standard": "WSET3", "category": "Regiones & Terruños", "topic": "Influencia del canal de Marlborough (Wairau vs Awatere Valley): temperaturas medias diurnas y perfiles herbáceos vs tropicales"},
    {"standard": "WSET3", "category": "Vinos Espumosos", "topic": "Método Tradicional: ciclo biológico de la toma de espuma en botella según la ecuación de Gay-Lussac (4 g/L de azúcar = 1 bar)"},
    {"standard": "WSET3", "category": "Vinos Espumosos", "topic": "Papel del licor de expedición (dosage) y perfiles sensoriales de Brut Nature (0-3 g/L) a Doux (>50 g/L)"},
    {"standard": "WSET3", "category": "Vinos Espumosos", "topic": "Método Ancestral (Pét-Nat): control de densidad al embotellar y ausencia de degüelle o dosage"},
    {"standard": "WSET3", "category": "Vinos Espumosos", "topic": "Método Charmat / Martinotti para Prosecco y Asti: preservación de precursores tiólicos y terpenos primarios"},
    {"standard": "WSET3", "category": "Vinos Espumosos", "topic": "Sistemas de prensado de racimo entero en Champagne (prensa Coquard): extracción de cuvée (2050L) y taille (500L)"},
    {"standard": "WSET3", "category": "Vinos Espumosos", "topic": "Cava de Guarda Superior: requisitos de envejecimiento mínimo para Reserva (18 meses) y Gran Reserva (30 meses)"},
    {"standard": "WSET3", "category": "Vinos Espumosos", "topic": "Cap Classique sudafricano: evolución en lías de un mínimo de 12 a 24 meses y variedades permitidas"},
    {"standard": "WSET3", "category": "Vinos Espumosos", "topic": "Franciacorta Satèn: presión máxima reducida a 5 bares y utilización exclusiva de uvas blancas (Blanc de Blancs)"},
    {"standard": "WSET3", "category": "Vinos Espumosos", "topic": "Impacto del descorche por chorro de hielo en el cuello de la botella (dégorgement à la volée vs par congélation)"},
    {"standard": "WSET3", "category": "Vinos Espumosos", "topic": "Evolución oxidativa posdegüelle: la reacción de Maillard estimulada por el azúcar del licor de expedición"},
    {"standard": "WSET3", "category": "Vinos Fortificados & Dulces", "topic": "Sistemas de Criaderas y Soleras en el Marco de Jerez: flujo fraccional de rocío y saca anual"},
    {"standard": "WSET3", "category": "Vinos Fortificados & Dulces", "topic": "Condiciones ecológicas para el desarrollo del velo de flor: humedad 70%, 15-20°C y graduación 15-15.5% vol"},
    {"standard": "WSET3", "category": "Vinos Fortificados & Dulces", "topic": "Porto Vintage versus Colheita versus Tawny con indicación de edad: maduración reductiva en botella vs oxidativa en pipas"},
    {"standard": "WSET3", "category": "Vinos Fortificados & Dulces", "topic": "Madeira: proceso de estufagem (calentamiento artificial a 45-50°C) versus canteiro (maduración solar en buhardillas)"},
    {"standard": "WSET3", "category": "Vinos Fortificados & Dulces", "topic": "Sauternes y Barsac: concentración de azúcares y glicerol inducida por Botrytis cinerea y microclima del río Ciron"},
    {"standard": "WSET3", "category": "Vinos Fortificados & Dulces", "topic": "Eiswein alemán y canadiense: vendimia a temperaturas mínimas de -7°C a -8°C y prensado en frío de cristales de hielo"},
    {"standard": "WSET3", "category": "Vinos Fortificados & Dulces", "topic": "Vin Doux Naturel de Rivesaltes y Banyuls: técnica de mutage sobre mosto o sobre hollejos con alcohol neutro al 96%"},
    {"standard": "WSET3", "category": "Vinos Fortificados & Dulces", "topic": "Marsala Vergine o Soleras: crianza mínima de 5 años en madera y graduación mínima de 18% sin adición de mosto cotto"},
    {"standard": "WSET3", "category": "Vinos Fortificados & Dulces", "topic": "Commandaria de Chipre: uvas Mavro y Xynisteri asoladas en esteras y crianza bajo sistema similar a solera (Mána)"},
    {"standard": "WSET3", "category": "Vinos Fortificados & Dulces", "topic": "Rutherglen Muscat: clasificación por edad (Rutherglen, Classic, Grand, Rare) y graduación de azúcares residuales (>200 g/L)"},
    {"standard": "WSET3", "category": "Sostenibilidad & Legislación", "topic": "Normativa europea de etiquetado nutricional (Reglamento UE 2021/2117): valor energético y lista de ingredientes por código QR"},
    {"standard": "WSET3", "category": "Sostenibilidad & Legislación", "topic": "Principios de biodinámica según Rudolf Steiner y certificación Demeter: preparados 500 (sílice de cuerno) y 501"},
    {"standard": "WSET3", "category": "Sostenibilidad & Legislación", "topic": "Límites máximos de anhídrido sulfuroso total (SO2) en la UE para vinos convencionales, ecológicos y biodinámicos"},
    {"standard": "WSET3", "category": "Sostenibilidad & Legislación", "topic": "Sistema de Appelations en Francia: jerarquía INAO de AOP/AOC, IGP y Vin de France"},
    {"standard": "WSET3", "category": "Sostenibilidad & Legislación", "topic": "Regulaciones de la TTB en Estados Unidos: requisito del 85% de uva procedente del AVA declarada en la etiqueta"},
    {"standard": "WSET3", "category": "Sostenibilidad & Legislación", "topic": "Indicaciones Geográficas (GI) en Australia: zonas, regiones y subregiones reguladas por Wine Australia"},
    {"standard": "WSET3", "category": "Sostenibilidad & Legislación", "topic": "Legislación de Vinos de Pago en España: requisitos de finca única, vinificación propia y trazabilidad estricta"},
    {"standard": "WSET3", "category": "Sostenibilidad & Legislación", "topic": "La mención 'Reserva' y 'Gran Reserva' en Rioja: tiempos mínimos de barrica y botella según el pliego de condiciones"},
    {"standard": "WSET3", "category": "Sostenibilidad & Legislación", "topic": "Certificaciones de huella de carbono y gestión del agua: International Wineries for Climate Action (IWCA)"},
    {"standard": "WSET3", "category": "Sostenibilidad & Legislación", "topic": "Nuevas variedades de vid resistentes a enfermedades fúngicas (PIWI) y su inclusión en las denominaciones de origen europeas"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "Evaluación del equilibrio: relación entre acidez total, concentración frutal, taninos y alcohol en boca"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "Evaluación de la persistencia aromática (caudalías): distinción entre persistencia gustativa y amargor retronasal"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "Evaluación de la complejidad: coexistencia de capas aromáticas primarias (varietales), secundarias (fermentación) y terciarias (crianza)"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "Evaluación de la tipicidad varietal y geográfica: fidelidad al perfil clásico de la cepa y al macroclima del origen"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "Potencial de envejecimiento en botella: presencia de suficiente concentración de acidez, taninos estructurados y extracto seco"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "Impacto del tipo de cierre (corcho natural de una pieza vs tapón de rosca vs microgranulado Diam) en el envejecimiento reductivo"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "Tasa de transmisión de oxígeno (OTR) de los diferentes tipos de cierres y prevención de prematura oxidación o reducción"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "Efectos del tostado de la barrica (ligero, medio, medio-plus, pesado) en la liberación de furanos, vainillina y eugenol"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "Diferencia de porosidad y aporte aromático entre roble francés (Quercus petraea/robur) y roble americano (Quercus alba)"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "Uso de recipientes de hormigón crudo y ánforas de terracota: microoxigenación pasiva sin aporte de compuestos de madera"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "Clarificación con agentes orgánicos (albúmina de huevo, cola de pescado) vs minerales (bentonita) vs vegetales (proteína de guisante)"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "Filtración por placas celulósicas versus filtración tangencial (cross-flow): impacto en la limpidez y estructura coloidal"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "Criterios para determinar la madurez óptima de la uva: madurez tecnológica (azúcares/ácidos) vs madurez fenólica (taninos/color)"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "El pH del vino como parámetro rector de la estabilidad microbiana, eficacia del SO2 y sensación táctil de frescura"},
    {"standard": "WSET3", "category": "Factores de Calidad", "topic": "Rendimientos por hectárea: correlación entre carga de yemas, vigor del viñedo y concentración de extracto seco en el mosto"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Vista", "topic": "Deducción de edad y variedad mediante la profundidad del color y la anchura del ribete acuoso (rim variation)"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Vista", "topic": "Reflejos verdosos versus pajizos versus dorados en vinos blancos: indicación de clima frío, edad o crianza en roble"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Vista", "topic": "Intensidad y color de las lágrimas (legs/tears): viscosidad debida a glicerol y porcentaje de alcohol por efecto Marangoni"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Vista", "topic": "Presencia de turbidez coloidal o partículas en suspensión: filtración no invasiva, vino natural o decantación requerida"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Vista", "topic": "Matiz teja o atejado (garnet / tawny) en vinos tintos jóvenes: uvas ricas en fenoles oxidables como Nebbiolo o Sangiovese"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Nariz", "topic": "Deducción de clima: fruta ácida y fresca (cítricos, manzana verde) vs fruta madura o compotada (fruta negra, higos, mermeladas)"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Nariz", "topic": "Marcadores de pirazinas (pimiento verde, tallo de tomate): Cabernet Franc y Sauvignon Blanc en zonas de clima moderado"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Nariz", "topic": "Marcadores de rotundona (pimienta negra y blanca recién molida): Syrah de clima frío (Ródano Norte) y Grüner Veltliner"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Nariz", "topic": "Marcador de TDN (1,1,6-trimetil-1,2-dihidronaftaleno): hidrocarburos y queroseno en Riesling maduros con crianza en botella"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Nariz", "topic": "Marcadores terpénicos (linalool, geraniol): notas florales a azahar, jazmín y uva fresca en Torrontés, Moscatel y Gewürztraminer"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Nariz", "topic": "Marcadores tiólicos (3MH, 3MHA): fruta de la pasión, pomelo rosado y boj en Sauvignon Blanc de Marlborough"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Nariz", "topic": "Marcadores de lactonas de roble (whisky lactone): coco rallado, eneldo y serrín fresco típicos de barrica de roble americano"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Nariz", "topic": "Deducción de suelo y mineralidad: pedernal (flint/gunsmoke) en Pouilly-Fumé vs piedra caliza mojada en Chablis"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Nariz", "topic": "Aromas de autólisis: brioche recién horneado, masa madre, galleta y tostadas en Champagne de largo envejecimiento"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Nariz", "topic": "Aromas botríticos: miel de acacia, orejones de albaricoque, cera de abejas y mermelada de naranja amarga"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Boca", "topic": "Sensación de tanino en encías vs lengua vs garganta: taninos de hollejo maduros y poliméricos vs taninos verdes de raspón o madera"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Boca", "topic": "Evaluación de acidez salival: salivación lateral fluida (ácido málico/tartárico) vs acidez láctica redonda y cremosa"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Boca", "topic": "Calidez del alcohol en la orofaringe: calibración precisa del porcentaje de alcohol entre 12.5% y 15.5% vol"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Boca", "topic": "Sensación de textura y cuerpo: aporte del extracto seco libre de azúcares y volumen de polisacáridos coloidales"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Boca", "topic": "Identificación de azúcar residual imperceptible (2-5 g/L): diferenciación entre dulzor verdadero y fruta madura glicérica"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Blancos", "topic": "Diferenciación a ciegas: Chablis Premier Cru vs Napa Valley Chardonnay con roble nuevo al 50%"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Blancos", "topic": "Diferenciación a ciegas: Sancerre (Sauvignon Blanc calizo) vs Marlborough Sauvignon Blanc (tioles punzantes)"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Blancos", "topic": "Diferenciación a ciegas: Mosel Riesling Kabinett (azúcar residual y acidez punzante) vs Rheingau Riesling Trocken"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Blancos", "topic": "Diferenciación a ciegas: Albariño de Rías Baixas (salinidad, flor blanca y hueso) vs Viognier de Condrieu (oleosidad baja acidez)"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Blancos", "topic": "Diferenciación a ciegas: Grüner Veltliner de Wachau (pimienta blanca, rábano) vs Pinot Gris de Alsacia (cuerpo denso, ahumado)"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Blancos", "topic": "Diferenciación a ciegas: Hunter Valley Semillon madurado en botella (cera, tostada sin madera) vs Graves Blanc con crianza"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Blancos", "topic": "Diferenciación a ciegas: Chenin Blanc de Vouvray Sec (membrillo, lanolina, acidez cortante) vs dry Furmint de Tokaj"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Blancos", "topic": "Diferenciación a ciegas: Soave Classico (Garganega, almendra amarga) vs Gavi di Gavi (Cortese, manzana y acidez cítrica)"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Blancos", "topic": "Diferenciación a ciegas: Verdicchio dei Castelli di Jesi (hierbas amargas, salitre) vs Pinot Grigio del Friuli"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Blancos", "topic": "Diferenciación a ciegas: Assyrtiko de Santorini (acidez volcánica volcánica, salmuera, pomelo) vs Chablis"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Tintos", "topic": "Diferenciación a ciegas: Borgoña Pinot Noir (Côte de Nuits) vs Oregon Willamette Valley Pinot Noir"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Tintos", "topic": "Diferenciación a ciegas: Barolo (Nebbiolo: color claro, tanino masivo, rosa y alquitrán) vs Brunello di Montalcino (Sangiovese: cereza ácida y cuero)"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Tintos", "topic": "Diferenciación a ciegas: Burdeos Margaux (Cabernet Sauvignon estructurado, cedro) vs Napa Valley Cabernet Sauvignon"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Tintos", "topic": "Diferenciación a ciegas: Ródano Norte Syrah (pimienta negra, aceituna verde, caza) vs Barossa Valley Shiraz (mora, eucalipto, vainilla)"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Tintos", "topic": "Diferenciación a ciegas: Rioja Gran Reserva (Tempranillo evolucionado, coco, cuero, eneldo) vs Chianti Classico Riserva"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Tintos", "topic": "Diferenciación a ciegas: Mendoza Malbec de altura (violeta, ciruela, tanino dulce) vs Cahors Malbec francés (rústico, tanino terroso)"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Tintos", "topic": "Diferenciación a ciegas: Chinon (Cabernet Franc: pimiento verde asado, frambuesa silvestre) vs Carmenère chileno"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Tintos", "topic": "Diferenciación a ciegas: Priorat Llicorella (Garnacha/Cariñena alcohólica y mineral) vs Châteauneuf-du-Pape"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Tintos", "topic": "Diferenciación a ciegas: Ribera del Duero (Tinto Fino denso, zarzamora, tanino firme) vs Toro (Tinta de Toro hiperconcentrada)"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Tintos", "topic": "Diferenciación a ciegas: Pinotage sudafricano (notas ahumadas, plátano tostado, zarzamora) vs Syrah de clima cálido"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "TCA (2,4,6-tricloroanisol): umbral de detección humano (1-2 ng/L) y diferenciación de moho ambiental o humedad de bodega"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Brettanomyces bruxellensis: síntesis de 4-etilfenol (sudor de caballo, establo) y 4-etilguayacol (ahumado medicinal)"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Picado acético: combinación de ácido acético (vinagre) y acetato de etilo (pegamento/quitaesmalte) por Acetobacter"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Acetaldehído: aroma a manzana oxidada y frutos secos en vinos que no han sido intencionadamente criados bajo velo"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Enfermedad de la luz (lightstruck flavor): fotólisis de riboflavina y producción de dimetildisulfuro en botellas transparentes"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Gusto a ratón (mousiness): 2-acetilpirrolina y 2-etil-tetrahidropiridina activadas por el pH neutro de la saliva retronasal"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Defecto de corcho por tribromoanisol (TBA): contaminación por biocidas bromados en palets de almacenamiento"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Geosmina: olor a tierra húmeda o remolacha infectada por Penicillium expansum en vendimias con podredumbre gris"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Aroma a geranio: reducción del sorbato de potasio por bacterias lácticas en presencia de anhídrido sulfuroso insuficiente"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Oxidación prematura en vinos blancos secos (Premox): degradación de glutatión y cierre defectuoso con entrada de O2"},
    {"standard": "CMS", "category": "Servicio de Sala de Élite", "topic": "Protocolo de apertura de vino espumoso frente a mesa de comensales: ángulo de 45 grados, rotación de base y descorche silencioso"},
    {"standard": "CMS", "category": "Servicio de Sala de Élite", "topic": "Decantación de vino tinto viejo con vela: posición del hombro de la botella, flujo continuo y detención precisa del sedimento"},
    {"standard": "CMS", "category": "Servicio de Sala de Élite", "topic": "Servicio de cata inicial al anfitrión (host tasting): dosis de 30 ml, espera de confirmación y servicio ordenado en sentido horario"},
    {"standard": "CMS", "category": "Servicio de Sala de Élite", "topic": "Temperatura de servicio óptima por estilo: espumosos (6-8°C), blancos ligeros (8-10°C), tintos de guarda (16-18°C)"},
    {"standard": "CMS", "category": "Servicio de Sala de Élite", "topic": "Uso de las tenazas de Oporto (Port tongs): calentamiento al fuego, choque térmico con agua helada y corte limpio del vidrio"},
    {"standard": "CMS", "category": "Servicio de Sala de Élite", "topic": "Procedimiento ante una queja de cliente sobre temperatura de vino tinto elevada (chilling bucket con agua, hielo y sal)"},
    {"standard": "CMS", "category": "Servicio de Sala de Élite", "topic": "Manejo de cristalería: selección de copas (Bordeaux vs Burgundy vs Zalto Universal) y pulido sin residuos de detergente"},
    {"standard": "CMS", "category": "Servicio de Sala de Élite", "topic": "Protocolo de servicio de cigarrillos y puros puros habanos: encendido con astilla de cedro y corte con guillotina de doble hoja"},
    {"standard": "CMS", "category": "Servicio de Sala de Élite", "topic": "Presentación de la etiqueta de la botella al comensal: posición del lito en la mano izquierda y orientación visible"},
    {"standard": "CMS", "category": "Servicio de Sala de Élite", "topic": "Orden de prioridad de servicio en mesa según protocolo clásico: dama anfitriona, comensales de mayor edad, anfitrión"},
    {"standard": "CMS", "category": "Destilados & Bebidas Mundiales", "topic": "Scotch Whisky: diferencias de destilación y perfil entre Islay (humo de turba, fenoles marinos) y Speyside (fruta y miel)"},
    {"standard": "CMS", "category": "Destilados & Bebidas Mundiales", "topic": "Cognac vs Armagnac: destilación en alambique charentais doble vs alambique de columna continua armagnaçais"},
    {"standard": "CMS", "category": "Destilados & Bebidas Mundiales", "topic": "Mezcal artesanal versus Tequila 100% de agave: hornos cónicos de tierra bajo leña vs autoclaves industriales de vapor"},
    {"standard": "CMS", "category": "Destilados & Bebidas Mundiales", "topic": "Sake japonés: ratio de pulido de arroz (Seimaibuai) en Ginjo (<=60%) vs Daiginjo (<=50%) y adición de alcohol (Junmai)"},
    {"standard": "CMS", "category": "Destilados & Bebidas Mundiales", "topic": "Cerveza: diferencias de fermentación entre Ale (Saccharomyces cerevisiae, fermentación alta) y Lager (S. pastorianus, baja)"},
    {"standard": "ASI", "category": "Competición Internacional ASI", "topic": "Prueba de corrección de carta de vinos con errores tramposos en añadas ficticias, DOs inexistentes y productores inventados"},
    {"standard": "ASI", "category": "Competición Internacional ASI", "topic": "Servicio simultáneo y cronometrado de un Magnum de Champagne en 15 copas idénticas sin retorno a ninguna de ellas"},
    {"standard": "ASI", "category": "Competición Internacional ASI", "topic": "Identificación de 5 destilados mundiales a ciegas en copa negra en menos de 3 minutos: origen, materia prima y alcohol"},
    {"standard": "ASI", "category": "Competición Internacional ASI", "topic": "Presentación oral en segundo idioma (inglés/francés/español) de un maridaje de menú de 5 tiempos con justificación física"},
    {"standard": "ASI", "category": "Competición Internacional ASI", "topic": "Resolución de crisis en escenario: cliente VIP que insiste en que un vino de 50 años está en mal estado por falta de fruta primaria"},
    {"standard": "ASI", "category": "Competición Internacional ASI", "topic": "Gestión de comensales con alergias graves a sulfitos o proteína de huevo: filtración tangencial y selección de vinos naturales"},
    {"standard": "ASI", "category": "Competición Internacional ASI", "topic": "Venta sugerida de vinos de alta gama (upselling) respetando escrupulosamente el perfil gustativo solicitado por la mesa"},
    {"standard": "ASI", "category": "Competición Internacional ASI", "topic": "Descripción organoléptica canónica en 90 segundos con conclusión clara: variedad, país, región, subzona, añada y calidad"},
    {"standard": "ASI", "category": "Competición Internacional ASI", "topic": "Cálculo en vivo de márgenes de beneficio (cost of sales, pour cost) y fijación de precios en carta de alta gastronomía"},
    {"standard": "ASI", "category": "Competición Internacional ASI", "topic": "Protocolo de cata de aguas minerales premium: residuo seco a 180°C, balance bicarbonato-calcio y carbonatación natural"},
    {"standard": "ASI", "category": "Maridaje Molecular & Gastronomía", "topic": "Afinidad de compuestos volátiles: maridaje por pirazinas entre Sauvignon Blanc y espárragos trigueros a la brasa"},
    {"standard": "ASI", "category": "Maridaje Molecular & Gastronomía", "topic": "Contraste de grasas saturadas: interacción entre la astringencia de taninos de Nebbiolo y las proteínas de un ossobuco"},
    {"standard": "ASI", "category": "Maridaje Molecular & Gastronomía", "topic": "El desafío del umami: maridaje de quesos curados (Parmesano/Manchego viejo) con vinos oxidativos de Jerez (Palo Cortado)"},
    {"standard": "ASI", "category": "Maridaje Molecular & Gastronomía", "topic": "Maridaje de comidas picantes (capsaicina en cocina tailandesa/mexicana): evitar taninos y optar por acidez, dulzor residual y bajo alcohol"},
    {"standard": "ASI", "category": "Maridaje Molecular & Gastronomía", "topic": "Maridaje de postres con chocolate amargo (>70% cacao): armonía por taninos y frutos secos con Oporto Vintage o Banyuls"},
    {"standard": "ASI", "category": "Maridaje Molecular & Gastronomía", "topic": "Armonía salina y yodada: ostras frescas y Manzanilla Pasada o Muscadet Sèvre et Maine sobre lías"},
    {"standard": "ASI", "category": "Maridaje Molecular & Gastronomía", "topic": "Maridaje por afinidad con alcachofas (cinarina): elección de espumosos método tradicional o vinos fortificados secos"},
    {"standard": "ASI", "category": "Maridaje Molecular & Gastronomía", "topic": "Maridaje de caza de pelo (ciervo, jabalí) y salsas reducidas: tintos maduros de Ródano Norte (Cornas) o Barolo Riserva"},
    {"standard": "ASI", "category": "Maridaje Molecular & Gastronomía", "topic": "Armonía de contraste ácido: ceviche clásico peruano de corvina y Riesling Trocken o Albariño en lías"},
    {"standard": "ASI", "category": "Maridaje Molecular & Gastronomía", "topic": "Maridaje de foie gras micuit: equilibrio de dulzor y acidez entre Sauternes botritizado o Tokaji Aszú 5 Puttonyos"},
    {"standard": "ASI", "category": "Logística & Gestión de Bodega", "topic": "Condiciones climáticas de guarda a largo plazo: 12-14°C constantes, humedad 70-75%, oscuridad y ausencia total de vibraciones"},
    {"standard": "ASI", "category": "Logística & Gestión de Bodega", "topic": "Sistemas de rotación de stock FIFO (First In, First Out) y seguimiento de añadas con curvas de ventana óptima de consumo"},
    {"standard": "ASI", "category": "Logística & Gestión de Bodega", "topic": "Almacenamiento de vinos espumosos: conservación horizontal versus vertical y tasa de intercambio gaseoso a través del corcho"},
    {"standard": "ASI", "category": "Logística & Gestión de Bodega", "topic": "Prevención de choques térmicos durante el transporte logístico internacional (uso de contenedores refrigerados reefer)"},
    {"standard": "ASI", "category": "Logística & Gestión de Bodega", "topic": "Pérdida por merma (ullage): niveles de cuello de botella aceptables en botellas de Burdeos y Borgoña según su antigüedad"},
    {"standard": "ASI", "category": "Logística & Gestión de Bodega", "topic": "Protocolo de reencorchado de vinos centenarios en bodega (château recorking) con reposición de volumen y gas inerte"},
    {"standard": "ASI", "category": "Logística & Gestión de Bodega", "topic": "Diseño de cavas climatizadas visibles en sala: cálculo de carga térmica, iluminación LED libre de UV y aislamiento acústico"},
    {"standard": "ASI", "category": "Logística & Gestión de Bodega", "topic": "Auditoría de autenticidad en subastas de vinos raros: análisis de micrograbado de etiquetas, cápsulas y sellos Prooftag"},
    {"standard": "ASI", "category": "Logística & Gestión de Bodega", "topic": "Seguro de bodega y valoración patrimonial de añadas míticas ante siniestros de inundación o rotura de compresores"},
    {"standard": "ASI", "category": "Logística & Gestión de Bodega", "topic": "Gestión del sistema Coravin: reemplazo de cápsulas de argón puro al 99.99% y cuidado de la aguja con teflón"},
    {"standard": "ASI", "category": "Bebidas Especiales & Infusiones", "topic": "Servicio ceremonial del té: diferencias de infusión y agua entre té blanco (Baihao Yinzhen) y té verde Matcha"},
    {"standard": "ASI", "category": "Bebidas Especiales & Infusiones", "topic": "Té negro fermentado Pu-erh: maduración microbiológica en cuevas de Yunnan y armonía con platos de pato asado"},
    {"standard": "ASI", "category": "Bebidas Especiales & Infusiones", "topic": "El café de especialidad en el restaurante con estrella Michelin: ratio de extracción (brew ratio) y tostado ligero varietal"},
    {"standard": "ASI", "category": "Bebidas Especiales & Infusiones", "topic": "Cata de aceites de oliva virgen extra (AOVE): amargor, picor y frutado en vaso oficial azul cobalto a 28°C"},
    {"standard": "ASI", "category": "Bebidas Especiales & Infusiones", "topic": "Destilación de ginebra botánica: maceración de enebro, cardamomo y cítricos en alambique de cobre al vacío (Rotovap)"},
    {"standard": "ASI", "category": "Bebidas Especiales & Infusiones", "topic": "Vermouth tradicional de Reus y Torino: adición de ajenjo (Artemisia absinthium), díctamo y azúcar caramelizado"},
    {"standard": "ASI", "category": "Bebidas Especiales & Infusiones", "topic": "Ron agrícola de Martinica (AOC Rhum Agricole): destilación directa de jugo puro de caña (vesou) vs melaza"},
    {"standard": "ASI", "category": "Bebidas Especiales & Infusiones", "topic": "Calvados del Pays d'Auge: doble destilación en alambique de cobre de sidra de manzanas ácidas y amargas"},
    {"standard": "ASI", "category": "Bebidas Especiales & Infusiones", "topic": "Grappa monovarietal de orujos frescos: alambique discontinuo al baño maría para destilación de uvas Moscato o Nebbiolo"},
    {"standard": "ASI", "category": "Bebidas Especiales & Infusiones", "topic": "Elaboración de cócteles clásicos en mesa de comensal: Dry Martini perfecto, balance 5:1 con vermouth dry y aceituna o twist"},
    {"standard": "ASI", "category": "Cultura y Geopolítica Enológica", "topic": "Viticultura en el Cáucaso: Georgia y el método ancestral de vinificación en tinajas Qvevri enterradas en tierra"},
    {"standard": "ASI", "category": "Cultura y Geopolítica Enológica", "topic": "El impacto del cambio climático en las regiones septentrionales: emergencia de espumosos ingleses en Sussex y Kent"},
    {"standard": "ASI", "category": "Cultura y Geopolítica Enológica", "topic": "Historia y evolución de las clasificaciones vinícolas: la Clasificación Oficial de Burdeos de 1855"},
    {"standard": "ASI", "category": "Cultura y Geopolítica Enológica", "topic": "Evolución de la viticultura en China: Ningxia Helan Mountain y el desarrollo de vinos de alta gama en climas desérticos"},
    {"standard": "ASI", "category": "Cultura y Geopolítica Enológica", "topic": "El renacimiento de los vinos de tinaja de barro en el Alentejo portugués: Vinho de Talha certificado"},
    {"standard": "ASI", "category": "Cultura y Geopolítica Enológica", "topic": "Sistemas tradicionales de conducción en el mundo: alberello en Pantelleria (patrimonio UNESCO) vs pergola trentina"},
    {"standard": "ASI", "category": "Cultura y Geopolítica Enológica", "topic": "La crisis filoxérica del siglo XIX: origen del insecto Daktulosphaira vitifoliae y salvación por injerto americano"},
    {"standard": "ASI", "category": "Cultura y Geopolítica Enológica", "topic": "Vinos de viñedos en pie franco (ungrafted): zonas arenosas de Colares (Portugal), Valle del Loira y Toro"},
    {"standard": "ASI", "category": "Cultura y Geopolítica Enológica", "topic": "La Juicio de París de 1976: cata a ciegas que posicionó a los vinos de California frente a los primeros crus de Burdeos y Borgoña"},
    {"standard": "ASI", "category": "Cultura y Geopolítica Enológica", "topic": "El renacimiento de los Vins Liquoreux de Constantia en Sudáfrica: historia del Vin de Constance desde el siglo XVIII"},
    {"standard": "ASI", "category": "Técnicas de Sala y Comunicación", "topic": "Storytelling enológico: narración precisa de la historia del productor sin caer en clichés comerciales"},
    {"standard": "ASI", "category": "Técnicas de Sala y Comunicación", "topic": "Lectura de lenguaje corporal del cliente: cuándo intervenir en la mesa y cuándo garantizar privacidad absoluta"},
    {"standard": "ASI", "category": "Técnicas de Sala y Comunicación", "topic": "Manejo de tiempos entre cocina y sala: sincronización de descorches con la llegada del plato a mesa"},
    {"standard": "ASI", "category": "Técnicas de Sala y Comunicación", "topic": "Protocolo de cata para jurados de concursos internacionales: eliminación de sesgos y calibración de panel"},
    {"standard": "ASI", "category": "Técnicas de Sala y Comunicación", "topic": "Diseño tipográfico y estructura ergonómica de una carta de vinos física y digital (organización por peso o geografía)"},
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "Manejo de podas de regeneración (Guyot-Poussard) para prevenir enfermedades de la madera de la vid (Yesca, Eutipiosis)"},
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "El papel del boro y zinc en el cuajado floral: prevención del corrimiento (coulure) y millerandage"},
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "Monitoreo del potencial hídrico foliar antes del amanecer (cámara de presión Scholander) para optimizar riego deficitario"},
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "Compostaje en viñedo y biochar: fijación de carbono estable y mejora de la capacidad de intercambio catiónico (CIC)"},
    {"standard": "WSET3", "category": "Viticultura Avanzada", "topic": "Selección masal versus clonal: conservación de variabilidad intra-varietal y resiliencia climática"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Química de las pirazinas (3-isobutil-2-metoxipirazina): degradación lumínica y umbral sensorial en partes por trillón"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Oxigenación durante la fermentación alcohólica: síntesis de esteroles y ácidos grasos insaturados por Saccharomyces"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Adición de enzimas pectolíticas: clarificación de mostos blancos y aumento del rendimiento en prensado suave"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Cinética de liberación de lactonas y elagitaninos durante los primeros 12 meses de crianza en barrica nueva"},
    {"standard": "WSET3", "category": "Enología & Química", "topic": "Estabilización de proteínas en vinos blancos: uso óptimo de bentonita cálcica vs sódica para evitar pérdidas aromáticas"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Nariz", "topic": "Deducción de crianza oxidativa: nueces tostadas, avellanas, piel de naranja confitada y toffee en Madeiras y Olorosos"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Nariz", "topic": "Deducción de maceración con hollejos en vinos blancos (Orange Wines): té negro bergamota, albaricoque seco y tanino táctil"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Boca", "topic": "Identificación de acidez volátil beneficiosa (lifted acidity) vs picado irreversible en vinos tradicionales"},
    {"standard": "CMS", "category": "Cuadrícula Deductiva: Boca", "topic": "Diferenciación táctil entre taninos astringentes desecantes y taninos calcáreos salinos de suelos de tiza o caliza"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Tintos", "topic": "Diferenciación a ciegas: Carmenère del Valle de Colchagua (pimiento rojo dulce, páprika, cacao) vs Merlot de Pomerol"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Tintos", "topic": "Diferenciación a ciegas: Amarone della Valpolicella (fruta pasa, alcohol 15.5%, chocolate) vs Ripasso della Valpolicella"},
    {"standard": "CMS", "category": "Identificación a Ciegas: Tintos", "topic": "Diferenciación a ciegas: Bandol Mourvèdre (cuero, carne curada, mora silvestre) vs Madiran Tannat"},
    {"standard": "CMS", "category": "Defectos del Vino", "topic": "Detección de mercaptanos pesados (disulfuro de dietilo, sulfuro de dimetilo) y su dificultad de reversión por aireación"},
    {"standard": "CMS", "category": "Servicio de Sala de Élite", "topic": "Manejo de botellas con corcho degradado o partido: extracción con descorchador de láminas The Durand y doble filtrado"},
    {"standard": "CMS", "category": "Servicio de Sala de Élite", "topic": "Servicio de vino dulce en copas tipo digestif (copa bordelesa pequeña o Riedel Vinum Sauternes) a 10-12°C"},
    {"standard": "ASI", "category": "Competición Internacional ASI", "topic": "Prueba de maridaje inverso: dado un vino específico y complejo (ej. Château Chalon 2012), diseñar un plato de alta cocina"},
    {"standard": "ASI", "category": "Competición Internacional ASI", "topic": "Servicio de sala bajo presión: gestión de un decantador roto accidentalmente y atención prioritaria al invitado afectado"},
    {"standard": "ASI", "category": "Maridaje Molecular & Gastronomía", "topic": "Maridaje por contraste térmico: helado de queso azul con reducción de Pedro Ximénez de 30 años"},
    {"standard": "ASI", "category": "Maridaje Molecular & Gastronomía", "topic": "Armonía con platos ahumados (salmón o anguila ahumada): Fino en rama bien frío o Whisky de Islay con turbas suaves"},
    {"standard": "ASI", "category": "Logística & Gestión de Bodega", "topic": "Plan de contingencia ante fallos del sistema HVAC en cavas subterráneas y protocolos de ventilación mecánica forzada"},
    {"standard": "ASI", "category": "Logística & Gestión de Bodega", "topic": "Sistemas de iluminación fría en bodegas históricas: protección de fotodegradación mediante filtros ámbar de 400-500 nm"},
    {"standard": "ASI", "category": "Bebidas Especiales & Infusiones", "topic": "Cata y servicio de hidromiel (mead): estilos secos versus melomel frutal y temperaturas idóneas de cata"},
    {"standard": "ASI", "category": "Bebidas Especiales & Infusiones", "topic": "Sidra de hielo (cidre de glace) de Quebec: crioextracción crioconcentrada natural a -15°C y maridaje con quesos de corteza lavada"},
    {"standard": "ASI", "category": "Cultura y Geopolítica Enológica", "topic": "La viticultura en zonas desérticas extremas: el desierto del Néguev en Israel y riego por goteo computarizado"},
    {"standard": "ASI", "category": "Cultura y Geopolítica Enológica", "topic": "Viticultura submarina: envejecimiento de botellas en jaulas sumergidas a 20-30 metros de profundidad en el Atlántico y Mediterráneo"},
]

# Variedades de Uva Mundiales y Autóctonas (180)
GRAPES_TO_ENRICH = [
    # Tintas Españolas Autóctonas y Tradicionales (45)
    "Tempranillo", "Garnacha", "Mencia", "Bobal", "Monastrell", 
    "Graciano", "Carignan", "Prieto Picudo", "Rufete", "Juan Garcia",
    "Souson", "Brancellao", "Caino Tinto", "Espadeiro", "Listan Negro",
    "Negramoll", "Baboso Negro", "Vijariego Negro", "Tintilla de Rota", "Maturana Tinta",
    "Garnacha Tintorera", "Garnacha Peluda", "Callet", "Fogoneu", "Manto Negro",
    "Mando", "Forcallat Tinta", "Moravia Agria", "Bruñal", "Gorgollassa",
    "Castets", "Beba", "Albarin Negro", "Verdejo Negro", "Carrasquin",
    "Garnatxa Fosca", "Trepat", "Sumoll", "Ull de Llebre", "Tinta de Toro",
    "Tinta del Pais", "Cencibel", "Tempranillo Peludo", "Moristel", "Parraleta",

    # Blancas Españolas Autóctonas y Tradicionales (45)
    "Albarino", "Verdejo", "Godello", "Treixadura", "Loureira",
    "Caino Blanco", "Torrontes Iberico", "Palomino Fino", "Pedro Ximenez", "Macabeo",
    "Xarello", "Parellada", "Garnacha Blanca", "Albillo Mayor", "Albillo Real",
    "Malvasia Volcanica", "Malvasia Aromatica", "Hondarrabi Zuri", "Albarin Blanco", "Dona Blanca",
    "Listan Blanco", "Vijariego Blanco", "Prensal Blanc", "Giro Ros", "Merseguera",
    "Airén", "Zalema", "Pardina", "Montua", "Cayetana Blanca",
    "Lado", "Albariño de Rias Baixas", "Gobelette", "Hondarrabi Zuri Zerratia", "Forcallat Blanca",
    "Tardana", "Tortosi", "Subirat Parent", "Malvasia de Sitges", "Moscatel de Alejandria",
    "Moscatel de Grano Menudo", "Planta Fina", "Planta Nova", "Garnacha Gris", "Marmajuelo",

    # Tintas Internacionales Emblemáticas (45)
    "Cabernet Sauvignon", "Merlot", "Pinot Noir", "Syrah", "Nebbiolo",
    "Sangiovese", "Malbec", "Cabernet Franc", "Gamay", "Mourvedre",
    "Touriga Nacional", "Touriga Franca", "Barbera", "Carmenere", "Tannat",
    "Pinotage", "Zinfandel", "Corvina", "Rondinella", "Aglianico",
    "Nero d Avola", "Nerello Mascalese", "Primitivo", "Baga", "Blaufraenkisch",
    "Zweigelt", "Saperavi", "Xinomavro", "Agiorgitiko", "Petit Verdot",
    "Dolcetto", "Molinara", "Montepulciano", "Corvinone", "Sagrantino",
    "Tinta Roriz", "Tinta Barroca", "Trincadeira", "Castelao", "Cinsault",
    "Counoise", "Teroldego", "Lagrein", "St Laurent", "Plavac Mali",

    # Blancas Internacionales Emblemáticas (45)
    "Chardonnay", "Sauvignon Blanc", "Riesling", "Chenin Blanc", "Viognier",
    "Semillon", "Gewurztraminer", "Pinot Gris", "Gruner Veltliner", "Assyrtiko",
    "Furmint", "Glera", "Marsanne", "Roussanne", "Melon de Bourgogne",
    "Savagnin", "Aligote", "Garganega", "Cortese", "Verdicchio",
    "Fiano", "Greco di Tufo", "Vermentino", "Carricante", "Moschofilero",
    "Harlevelu", "Torrontes Riojano", "Pinot Blanc", "Silvaner", "Muller-Thurgau",
    "Clairette", "Grenache Blanc", "Picpoul de Pinet", "Bourboulenc", "Mauzac",
    "Len de l El", "Petit Manseng", "Gros Manseng", "Arneis", "Pecorino",
    "Ribolla Gialla", "Friulano", "Trebbiano Toscano", "Catarratto", "Inzolia",


    # ==========================================================================
    # NUEVO CATÁLOGO DE VARIEDADES AUTÓCTONAS E HISTÓRICAS MUNDIALES (+120 Uvas)
    # ==========================================================================
    "Maturana Blanca", "Maturana Tinta", "Bruñal", "Albarín Negro", "Moravia Dulce",
    "Moravia Agria", "Forcallat Tinta", "Tortosí", "Escanyavella", "Malvasía de Sitges",
    "Callet", "Manto Negro", "Fogoneu", "Gorgollassa", "Sabro",
    "Baboso Blanco", "Gual", "Verdello", "Albillo Criollo", "Forastera Gomera",
    "Juan García", "Carrasquín", "Merenzao", "Ferrón", "Doña Blanca",
    "Lado", "Castañal", "Pedral", "Sousón", "Caíño da Terra",
    "Planta Fina", "Planta Nova", "Tardana", "Trepat", "Sumoll",
    "Mandó", "Monastrell de Alicante", "Albarín Blanco", "Airén de la Mancha", "Albillo Mayor",
    "Schiava", "Lagrein", "Teroldego", "Marzemino", "Refosco dal Peduncolo Rosso",
    "Picolit", "Ribolla Gialla", "Schiopettino", "Friulano", "Timorasso",
    "Nascetta", "Freisa", "Grignolino", "Ruché", "Pelaverga",
    "Erbaluce", "Pigato", "Rossese", "Nerello Cappuccio", "Nocera",
    "Frappato", "Gaglioppo", "Greco Nero", "Magliocco", "Susumaniello",
    "Uva di Troia", "Bombino Bianco", "Falanghina", "Coda di Volpe", "Pallagrello Nero",
    "Casavecchia", "Piedirosso", "Tintilia", "Bovale Sardo", "Cannonau",
    "Vermentino di Gallura", "Carignano del Sulcis", "Nuragus", "Vernaccia di San Gimignano", "Grechetto",
    "Savagnin", "Poulsard", "Trousseau", "Jacquère", "Altesse",
    "Mondeuse Noire", "Gringet", "Persan", "Braquet", "Folle Blanche",
    "Colombard", "Ugni Blanc", "Gros Manseng", "Petit Manseng", "Petit Courbu",
    "Arrufiac", "Fer Servadou", "Duras", "Prunelard", "Loin de l Oeil",
    "Négrette", "Sciaccarello", "Nielluccio", "Vermentinu", "Romorantin",
    "Pineau d Aunis", "Grolleau", "César", "Baco Noir", "Chasselas",
    "Furmint", "Hárslevelű", "Juhfark", "Kadarka", "Kékfrankos",
    "Blaufränkisch", "Zweigelt", "St Laurent", "Grüner Veltliner", "Roter Veltliner",
    "Neuburger", "Rotgipfler", "Zierfandler", "Plavac Mali", "Graševina",
    "Pošip", "Grk", "Teran", "Malvazija Istarska", "Vranac",
    "Saperavi", "Rkatsiteli", "Kisi", "Mtsvane", "Xinomavro",
    "Agiorgitiko", "Assyrtiko", "Moschofilero", "Malagousia", "Mavrodaphne",
    "Roditis", "Savatiano", "Vidiano", "Vilana", "Limnio",
    "Touriga Nacional", "Touriga Franca", "Tinta Roriz", "Tinta Barroca", "Tinto Cão",
    "Baga", "Trincadeira", "Castelão", "Alfrocheiro", "Jaen",
    "Vinhão", "Loureiro", "Alvarinho", "Arinto", "Antão Vaz",
    "Encruzado", "Fernão Pires", "Bical", "Cercial", "Verdelho dos Açores",
    "Sercial", "Boal", "Malvasia Fina", "Trajadura", "Avesso",

    # --- Expansión a 1,450 Fichas: Variedades Raras, Históricas y Resilientes (+150) ---
    "Aledo",
    "Albaranzeuli Bianco",
    "Albaranzeuli Nero",
    "Benedicto",
    "Bermejuela",
    "Borba",
    "Calagraño",
    "Camaralet",
    "Castellana Blanca",
    "Chasselas Doré",
    "Coira",
    "Corval",
    "Escursac",
    "Esperon de Gallo",
    "Folgasão",
    "Gouveio Real",
    "Graciano 15",
    "Hebén",
    "Jaén Blanco",
    "Legitimo Blanco",
    "Mancés de Tibés",
    "Molinera",
    "Moribel",
    "Obeidi",
    "Pardillo",
    "Parrellada",
    "Perruno",
    "Picapoll Blanc",
    "Picapoll Negre",
    "Rojal",
    "Tinta Francisca",
    "Tinta Miúda",
    "Trincadeira das Pratas",
    "Turruntés de Rioja",
    "Uva de Rey",
    "Valenci Blanc",
    "Valenci Negre",
    "Verdelho Tinto",
    "Verdil",
    "Vidadillo",
    "Abbuoto",
    "Albarola",
    "Aleatico",
    "Ancellotta",
    "Arvesiniadu",
    "Barbera Sarda",
    "Barsaglina",
    "Bellone Lazio",
    "Biancame",
    "Biancolella",
    "Bovale Grande",
    "Brugneto",
    "Calabrese",
    "Cagnulari",
    "Canaiolo Bianco",
    "Caprettone",
    "Carricante Bianco",
    "Cascitello",
    "Catalanesca",
    "Cavrara",
    "Centesimino",
    "Centesimino di Faenza",
    "Cesanese Comune",
    "Cesanese di Olevano",
    "Cococciola",
    "Coda di Pecora",
    "Colorino del Valdarno",
    "Cornalin",
    "Cordenossa",
    "Durella",
    "Enantio",
    "Famoso",
    "Fiano Minutolo",
    "Foglia Tonda",
    "Forastera",
    "Frappato di Vittoria",
    "Garganega Veronese",
    "Grechetto di Todi",
    "Greco Bianco",
    "Grignolino d'Asti",
    "Guardavalle",
    "Incrocio Manzoni 6.0.13",
    "Lacrima di Morro d'Alba",
    "Laurot",
    "Lumassina",
    "Magliocco Canino",
    "Magliocco Dolce",
    "Malbo Gentile",
    "Malvasia di Candia Aromatica",
    "Malvasia di Lipari",
    "Malvasia Puntinata",
    "Mantonico",
    "Mayolet",
    "Montuni",
    "Moscato di Scanzo",
    "Nascetta di Novello",
    "Nero Buono",
    "Neyret",
    "Nosiola",
    "Ortrugo",
    "Passerina",
    "Pecorino d'Abruzzo",
    "Pedevenda",
    "Perricone",
    "Petit Rouge",
    "Pignoletto",
    "Prié Blanc",
    "Raboso Piave",
    "Raboso Veronese",
    "Rebo",
    "Rossese di Dolceacqua",
    "Roussette d'Ayze",
    "Ruchè di Castagnole",
    "Sciaglin",
    "Sgavetta",
    "Tazzelenghe Friulano",
    "Terrano",
    "Tintilia del Molise",
    "Trebbiano d'Abruzzo",
    "Trebbiano di Soave",
    "Trebbiano Spoletino",
    "Uva Longanesi",
    "Uva Rara",
    "Verdeca",
    "Verduzzo Friulano",
    "Verduzzo Trevigiano",
    "Vespolina di Gattinara",
    "Vien de Nus",
    "Vitouska del Carso",
    "Araux",
    "Aramon Noir",
    "Arbois (Menu Pineau)",
    "Aubun",
    "Auxerrois Blanc",
    "Baco Blanc",
    "Bébian",
    "Béquignol",
    "Blanc Dame",
    "Bouchalès",
    "Bouysselet",
    "Brun Argenté",
    "Camaralet de Lasseube",
    "Castets de Bordeaux",
    "Chasan",
    "Chenanson",
    "Clairette Blanche",
    "Clairette Rose",
    "Claverie",
    "Corbeau (Douce Noire)",
    "Courbu Blanc",
]

def generate_winepedia_article(item):
    standard = item.get("standard", "WSET3")
    default_cat_es = f"{item['area']} & Terruño" if standard == "WSET3" else ("Cata Deductiva & Metodología" if standard == "CMS" else "Servicio & Protocolo de Sala")
    default_cat_en = "Enology & Terroir" if standard == "WSET3" else ("Deductive Tasting & Flaws" if standard == "CMS" else "Sommellerie & Service Protocol")
    category_es = item.get("category_es", default_cat_es)
    category_en = item.get("category_en", default_cat_en)
    badge_color = item.get("badge_color", "amber" if standard == "WSET3" else ("rose" if standard == "CMS" else "emerald"))

    prompt = f"""Genera un artículo técnico canónico para WINEp3dIA sobre '{item['title']}' ({item['area']}).
Canon de referencia: {standard}.
Enfoque: {item['focus']}.
Devuelve EXCLUSIVAMENTE un objeto JSON válido con esta estructura:
{{
  "id": "{item['id']}",
  "standard": "{standard}",
  "category_es": "{category_es}",
  "category_en": "{category_en}",
  "badge_color": "{badge_color}",
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
    print(f"   📈 Acumulado sesión : {stats['total_tokens']:,} tokens locales | Fichas nuevas: {stats['total_generated']}", flush=True)
    print(f"{sep}\n", flush=True)

# ==========================================
# CLI PARSER & TIME CONTROL
# ==========================================

def parse_schedule():
    parser = argparse.ArgumentParser(
        description="WINE³ai — Generador Autónomo Local con LM Studio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python3 scripts/overnight_worker.py                     # Inicia AHORA MISMO, termina en 3 horas
  python3 scripts/overnight_worker.py --end 06:45         # Inicia AHORA MISMO, termina a las 06:45 AM
  python3 scripts/overnight_worker.py --hours 8           # Inicia AHORA MISMO, trabaja durante 8 horas
  python3 scripts/overnight_worker.py --start 22:30 --end 06:45  # Inicia a las 22:30 y para a las 06:45 AM
        """
    )
    parser.add_argument("--start", type=str, default=None, help="Hora de inicio en formato HH:MM (por defecto: ahora mismo)")
    parser.add_argument("--end", type=str, default=None, help="Hora de fin en formato HH:MM (ej: 06:45 o 16:15)")
    parser.add_argument("--hours", type=float, default=None, help="Duración en horas (por defecto: 3 horas)")
    parser.add_argument("--indefinite", action="store_true", help="Ejecutar de forma continua e indefinida hasta detener manualmente")
    parser.add_argument("--now", action="store_true", help="Iniciar inmediatamente")
    
    args = parser.parse_args()
    now = datetime.now()

    # 1. Determinar hora de inicio
    if args.start:
        try:
            sh, sm = map(int, args.start.split(":"))
            start_dt = now.replace(hour=sh, minute=sm, second=0, microsecond=0)
            if start_dt < now - timedelta(minutes=1):
                start_dt += timedelta(days=1)
        except Exception:
            print(f"Error en formato --start '{args.start}'. Use HH:MM (ej: 22:00).")
            sys.exit(1)
    else:
        start_dt = now

    # 2. Determinar hora de fin
    if args.indefinite:
        end_dt = None
    elif args.end:
        try:
            eh, em = map(int, args.end.split(":"))
            end_dt = start_dt.replace(hour=eh, minute=em, second=0, microsecond=0)
            if end_dt <= start_dt:
                end_dt += timedelta(days=1)
        except Exception:
            print(f"Error en formato --end '{args.end}'. Use HH:MM (ej: 06:45 o 16:15).")
            sys.exit(1)
    elif args.hours is not None:
        end_dt = start_dt + timedelta(hours=args.hours)
    else:
        # Por defecto: 3 horas a partir del inicio
        end_dt = start_dt + timedelta(hours=3)

    return start_dt, end_dt

# ==========================================
# MAIN WORKER LOOP
# ==========================================

def main():
    start_dt, end_dt = parse_schedule()
    total_catalog = len(WINEPEDIA_TOPICS) + len(STUDY_CARD_TOPICS) + len(GRAPES_TO_ENRICH)

    print("\n" + "=" * 78, flush=True)
    print("🍷 WINE³ai — GENERADOR AUTÓNOMO LOCAL CON LM STUDIO (OFFLINE)", flush=True)
    print("=" * 78, flush=True)
    print(f"⏰ HORA DE INICIO           : {start_dt.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    if end_dt is None:
        print(f"🛑 FINALIZACIÓN PROGRAMADA : INDEFINIDA (Modo continuo hasta detención manual)", flush=True)
    else:
        duration_planned = end_dt - start_dt
        print(f"🛑 FINALIZACIÓN PROGRAMADA : {end_dt.strftime('%Y-%m-%d %H:%M:%S')} (Duración: {duration_planned})", flush=True)
    print(f"💻 MOTOR LOCAL             : LM Studio (http://localhost:1234/v1) · qwen/qwen3.5-9b", flush=True)
    print(f"⚡ ACELERACIÓN              : Apple Metal GPU (Inferencia Local en Mac)", flush=True)
    print(f"💰 CONSUMO EN NUBE         : 0 tokens (100% gratuito y privado)", flush=True)
    print(f"📋 CATÁLOGO DISPONIBLE     : {total_catalog} fichas en cola:", flush=True)
    print(f"   ├─ WINEp3dIA Articles   : {len(WINEPEDIA_TOPICS)} artículos enciclopédicos", flush=True)
    print(f"   ├─ Study Flashcards     : {len(STUDY_CARD_TOPICS)} fichas de examen (WSET 3, CMS, ASI)", flush=True)
    print(f"   └─ Grape Varieties      : {len(GRAPES_TO_ENRICH)} variedades de uva mundiales", flush=True)
    print("=" * 78 + "\n", flush=True)

    # Si la hora de inicio es en el futuro, esperar
    if datetime.now() < start_dt:
        wait_secs = (start_dt - datetime.now()).total_seconds()
        print(f"⏳ Esperando hasta la hora de inicio programada ({start_dt.strftime('%H:%M:%S')}, faltan {wait_secs/60:.1f} minutos)...", flush=True)
        while datetime.now() < start_dt:
            time.sleep(min(5, (start_dt - datetime.now()).total_seconds()))

    def is_time_up():
        if end_dt is None:
            return False
        return datetime.now() >= end_dt

    scheduled_end_str = end_dt.strftime('%Y-%m-%d %H:%M:%S') if end_dt else "INDEFINIDO (Detención Manual)"
    log(f"Worker running. Scheduled end: {scheduled_end_str}. Catalog: {total_catalog} items.", to_file_only=True)

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
            cutoff_msg = f"Hora de corte alcanzada ({end_dt.strftime('%H:%M:%S')}). Finalizando generador con gracia." if end_dt else "Detención solicitada."
            log(cutoff_msg)
            break

        if topic["id"] in existing_article_ids:
            continue

        start_t = time.time()
        try:
            res, usage = generate_winepedia_article(topic)
        except Exception:
            res, usage = None, {}

        elapsed = time.time() - start_t

        if res and isinstance(res, dict) and "title_es" in res:
            res["id"] = topic["id"]
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
                cutoff_msg = f"Hora de corte alcanzada ({end_dt.strftime('%H:%M:%S')}). Finalizando generador con gracia." if end_dt else "Detención solicitada."
                log(cutoff_msg)
                break

            card_id = f"card_{card_task['standard'].lower()}_{i:03d}"
            if card_id in existing_card_ids:
                continue

            start_t = time.time()
            try:
                res, usage = generate_study_card(card_task, i)
            except Exception:
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
                cutoff_msg = f"Hora de corte alcanzada ({end_dt.strftime('%H:%M:%S')}). Finalizando generador con gracia." if end_dt else "Detención solicitada."
                log(cutoff_msg)
                break

            if grape in existing_grape_names:
                continue

            start_t = time.time()
            try:
                res, usage = generate_grape_profile(grape)
            except Exception:
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
    actual_duration = now_end - start_dt

    print("\n" + "=" * 78, flush=True)
    print("🎉 GENERACIÓN NOCTURNA COMPLETADA CON ÉXITO", flush=True)
    print("=" * 78, flush=True)
    print(f"⏰ HORA DE FINALIZACIÓN       : {now_end.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print(f"⏱️ TIEMPO TOTAL TRANSCURRIDO  : {str(actual_duration).split('.')[0]}", flush=True)
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
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        local_hw = "Apple Silicon"
    else:
        local_hw = f"{platform.system()} ({platform.machine()})"

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 🍷 WINE³ai — Informe de Generación Nocturna (LM Studio)\n\n")
        f.write(f"- **Fecha y hora de finalización:** {now_end.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **Consumo de tokens en la nube:** **0 tokens** (100% inferencia local en {local_hw})\n")
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
