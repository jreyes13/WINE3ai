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
import argparse
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
