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
    {"id": "pasteurizacion_flash_vs_filtracion", "title": "Estabilización Microbiológica: Filtración Tangencial vs Lenticular", "area": "Enología", "focus": "Porosidad en micras, retención de levaduras y bacterias sin despojar coloides protectores"},
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
    {"id": "asi_sommelier_conflict_spoilage_resolution", "standard": "ASI", "area": "Sumillería & Sala", "title": "Resolución de Disconformidad por Vino Defectuoso en Sala", "focus": "Validación cortés sin discusión, retirada inmediata de la botella y sugerencia de alternativa óptima"}

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
    {"standard": "ASI", "category": "Servicio de Sala", "topic": "Resolución diplomática de quejas en mesa cuando un cliente rechaza una botella por TCA o temperatura"}

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
    "Ribolla Gialla", "Friulano", "Trebbiano Toscano", "Catarratto", "Inzolia"
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
    parser.add_argument("--end", type=str, default=None, help="Hora de fin en formato HH:MM (ej: 06:45 o 07:00)")
    parser.add_argument("--hours", type=float, default=None, help="Duración en horas (por defecto: 3 horas)")
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
    if args.end:
        try:
            eh, em = map(int, args.end.split(":"))
            end_dt = start_dt.replace(hour=eh, minute=em, second=0, microsecond=0)
            if end_dt <= start_dt:
                end_dt += timedelta(days=1)
        except Exception:
            print(f"Error en formato --end '{args.end}'. Use HH:MM (ej: 06:45).")
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
    duration_planned = end_dt - start_dt

    print("\n" + "=" * 78, flush=True)
    print("🍷 WINE³ai — GENERADOR AUTÓNOMO LOCAL CON LM STUDIO (OFFLINE)", flush=True)
    print("=" * 78, flush=True)
    print(f"⏰ HORA DE INICIO           : {start_dt.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
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
        return datetime.now() >= end_dt

    log(f"Worker running. Scheduled end: {end_dt.strftime('%Y-%m-%d %H:%M:%S')}. Catalog: {total_catalog} items.", to_file_only=True)

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
            log(f"Hora de corte alcanzada ({end_dt.strftime('%H:%M:%S')}). Finalizando generador con gracia.")
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
                log(f"Hora de corte alcanzada ({end_dt.strftime('%H:%M:%S')}). Finalizando generador con gracia.")
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
                log(f"Hora de corte alcanzada ({end_dt.strftime('%H:%M:%S')}). Finalizando generador con gracia.")
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
