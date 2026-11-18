import json
import os
import subprocess

# 1. Load data
with open('/Users/jreyes13/GitHub/wine3ai/data/grape_varieties.json', encoding='utf-8') as f:
    all_grapes = json.load(f)
all_grapes.sort(key=lambda g: -g.get('total_regions', 0))

country_colors = {
    'Francia': '#1d4ed8', 'France': '#1d4ed8',
    'España': '#dc2626', 'Spain': '#dc2626',
    'Italia': '#059669', 'Italy': '#059669',
    'Alemania': '#d97706', 'Germany': '#d97706',
    'Hungría': '#0284c7', 'Hungary': '#0284c7',
    'Portugal': '#16a34a',
    'Austria': '#9333ea',
    'Suiza': '#e11d48', 'Switzerland': '#e11d48',
    'Grecia': '#0891b2', 'Greece': '#0891b2',
    'Croacia': '#4338ca', 'Croatia': '#4338ca',
    'Eslovenia': '#4f46e5', 'Slovenia': '#4f46e5',
    'Eslovaquia': '#6366f1', 'Slovakia': '#6366f1',
    'República Checa': '#7c3aed', 'Czech Republic': '#7c3aed',
    'Rumanía': '#b45309', 'Romania': '#b45309',
    'Bulgaria': '#047857',
    'Moldavia': '#0f766e', 'Moldova': '#0f766e',
    'Georgia': '#be123c',
    'Armenia': '#b91c1c',
    'Turquía': '#991b1b', 'Turkey': '#991b1b',
    'Líbano': '#ea580c', 'Lebanon': '#ea580c',
    'Chipre': '#0284c7', 'Cyprus': '#0284c7',
    'Estados Unidos': '#2563eb', 'USA': '#2563eb',
    'Argentina': '#0284c7',
    'Chile': '#be123c',
    'Otros': '#64748b', 'Others': '#64748b'
}

country_short = {
    'Francia': 'FRA', 'France': 'FRA',
    'España': 'ESP', 'Spain': 'ESP',
    'Italia': 'ITA', 'Italy': 'ITA',
    'Alemania': 'DEU', 'Germany': 'DEU',
    'Hungría': 'HUN', 'Hungary': 'HUN',
    'Portugal': 'PRT',
    'Austria': 'AUT',
    'Suiza': 'CHE', 'Switzerland': 'CHE',
    'Grecia': 'GRC', 'Greece': 'GRC',
    'Croacia': 'HRV', 'Croatia': 'HRV',
    'Eslovenia': 'SVN', 'Slovenia': 'SVN',
    'Eslovaquia': 'SVK', 'Slovakia': 'SVK',
    'República Checa': 'CZE', 'Czech Republic': 'CZE',
    'Rumanía': 'ROU', 'Romania': 'ROU',
    'Bulgaria': 'BGR',
    'Moldavia': 'MDA', 'Moldova': 'MDA',
    'Georgia': 'GEO',
    'Armenia': 'ARM',
    'Turquía': 'TUR', 'Turkey': 'TUR',
    'Líbano': 'LBN', 'Lebanon': 'LBN',
    'Chipre': 'CYP', 'Cyprus': 'CYP'
}

def format_grape_name(raw_name, lang='es'):
    is_es = lang == 'es'
    if 'Garnacha' in raw_name or 'Grenache' in raw_name:
        if 'blanc' in raw_name.lower():
            return 'Garnacha Blanca' if is_es else 'Grenache Blanc'
        return 'Garnacha (Grenache)' if is_es else 'Grenache / Garnacha'
    if 'Monastrell' in raw_name or 'Mourvèdre' in raw_name:
        return 'Monastrell (Mourvèdre)' if is_es else 'Mourvèdre / Monastrell'
    if 'Macabeo' in raw_name or 'Viura' in raw_name:
        return 'Macabeo / Viura' if is_es else 'Macabeo (Viura)'
    if 'Welschriesling' in raw_name or 'Graševina' in raw_name:
        return 'Welschriesling / Graševina' if is_es else 'Welschriesling'
    return raw_name

def build_top_chart_html(lang='es'):
    is_es = lang == 'es'
    top = all_grapes[:30]
    col1_items = []
    col2_items = []
    
    other_label = 'Otros' if is_es else 'Others'
    reg_label = 'DOs'
    p_label = 'p.' if is_es else 'c.'
    countries_lbl = 'países' if is_es else 'countries'

    for rank, g in enumerate(top, 1):
        name = format_grape_name(g['name'], lang)
        color = g.get('color', 'red')
        dot_color = '#ef4444' if color == 'red' else '#ca8a04'
        total = g.get('total_regions', 0)
        c_count = g.get('countries_count', 0)
        breakdown = g.get('countries_breakdown', [])

        segments = []
        accum_pct = 0.0
        max_slices = 3 if len(breakdown) > 3 else len(breakdown)
        for c in breakdown[:max_slices]:
            pct = c.get('percentage', 0.0)
            accum_pct += pct
            c_name = c.get('country_es' if is_es else 'country_en', c.get('country'))
            c_code = country_short.get(c.get('country'), c_name[:3].upper())
            c_col = country_colors.get(c.get('country'), '#64748b')
            flag = c.get('flag', '')
            cnt = c.get('count', 0)
            
            # Segment text calibrated for ~145mm column
            if pct >= 30:
                txt = f"{flag} {c_code} {pct:.0f}%"
            elif pct >= 16:
                txt = f"{flag} {pct:.0f}%"
            elif pct >= 8:
                txt = f"{flag}"
            else:
                txt = ""
                
            segments.append(f'<div class="tseg" style="width:{pct:.1f}%;background:{c_col};" title="{c_name}: {cnt} {reg_label} ({pct:.1f}%)"><span>{txt}</span></div>')

        rem_pct = max(0.0, 100.0 - accum_pct)
        if rem_pct >= 2.0:
            rem_count = total - sum(c.get('count', 0) for c in breakdown[:max_slices])
            rem_c_count = max(1, c_count - max_slices)
            other_txt = f"+{rem_c_count} ({rem_pct:.0f}%)" if rem_pct >= 20 else (f"+{rem_c_count}" if rem_pct >= 10 else "")
            segments.append(f'<div class="tseg tseg-other" style="width:{rem_pct:.1f}%;background:#64748b;" title="{other_label} ({rem_c_count} {countries_lbl}): {rem_count}"><span>{other_txt}</span></div>')

        bar_html = ''.join(segments)
        item_html = f'''
        <div class="top-var-item">
          <div class="top-var-meta">
            <div class="top-var-left">
              <span class="top-var-rank">#{rank}</span>
              <span class="top-var-dot" style="background:{dot_color};"></span>
              <span class="top-var-name" title="{name}">{name}</span>
            </div>
            <span class="top-var-total"><b>{total}</b> {reg_label} · {c_count}{p_label}</span>
          </div>
          <div class="top-var-bar">{bar_html}</div>
        </div>'''
        
        if rank <= 15:
            col1_items.append(item_html)
        else:
            col2_items.append(item_html)

    title = "📊 TOP 30 VARIEDADES MÁS CULTIVADAS & PRESENCIA GLOBAL" if is_es else "📊 TOP 30 MOST CULTIVATED VARIETIES & GLOBAL SPREAD"
    subtitle = "Presencia en denominaciones de origen oficiales (DOs / AOCs / DOCGs) y desglose por países" if is_es else "Share of official protected appellations (DOs / AOCs / DOCGs) and country breakdown"

    return f'''
      <div class="box top-var">
        <h3>{title}</h3>
        <div class="top-var-sub">{subtitle}</div>
        <div class="top-var-grid">
          <div class="top-var-col">
            {''.join(col1_items)}
          </div>
          <div class="top-var-col">
            {''.join(col2_items)}
          </div>
        </div>
      </div>'''

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="__LANG__">
<head>
<meta charset="UTF-8">
<title>__PAGE_TITLE__</title>
<style>
  /* DIN-A0 apaisado: 1189 x 841 mm. Todo en mm => PDF vectorial a escala 1:1 */
  @page { size: 1189mm 841mm; margin: 0; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body {
    width: 1189mm; height: 841mm;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #0f172a;
    background: #fbf8f3;
    overflow: hidden;
  }
  .poster {
    width: 1189mm; height: 841mm;
    padding: 12mm 14mm 10mm 14mm;
    display: grid;
    grid-template-rows: 56mm 1fr 12mm;
    gap: 5mm;
  }

  /* ---------- HEADER ---------- */
  .head {
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: 1.6mm solid #5E1C37; padding-bottom: 4mm;
  }
  .brand { display: flex; align-items: center; gap: 7mm; }
  .brand-logo-wrap { display: flex; align-items: center; gap: 4mm; }
  .brand-logo-img { width: 34mm; height: 34mm; object-fit: contain; }
  .brand-logo { font-size: 28mm; font-weight: 900; color: #B08D4B; letter-spacing: -1.2mm; line-height: 1; }
  .brand-logo sup { font-size: 16mm; color: #B08D4B; font-weight: 900; }
  .brand-logo .ai { font-size: 16mm; color: #5E1C37; font-weight: 900; background: rgba(94, 28, 55, 0.12); padding: 1mm 3.5mm; border-radius: 2mm; border: 0.6mm solid rgba(94, 28, 55, 0.4); margin-left: 2.5mm; }
  .title-block h1 { font-size: 18mm; font-weight: 900; letter-spacing: -0.4mm; line-height: 1.05; color: #0f172a; }
  .title-block p { font-size: 6.2mm; color: #334155; font-weight: 500; margin-top: 1.8mm; }
  .head-formula { text-align: right; }
  .formula { font-size: 13.5mm; font-weight: 900; color: #0f172a; }
  .formula span { color: #B08D4B; }
  .formula-sub { font-size: 4.8mm; color: #475569; font-weight: 600; margin-top: 1.2mm; line-height: 1.35; }

  /* ---------- BODY ---------- */
  .body { display: grid; grid-template-columns: 1fr 310mm; gap: 8mm; min-height: 0; }

  .table-grid {
    display: grid;
    grid-template-columns: 14mm 54mm repeat(9, 1fr);
    grid-template-rows: 14mm 42mm repeat(9, 1fr);
    gap: 2.2mm;
    min-height: 0;
  }
  .wband {
    border-radius: 2mm; color: #fff; font-weight: 900; font-size: 5.6mm;
    display: flex; align-items: center; justify-content: center; letter-spacing: 0.4mm;
  }
  .cband {
    border-radius: 2mm; color: #fff; font-weight: 900; font-size: 5.2mm;
    writing-mode: vertical-rl; transform: rotate(180deg);
    display: flex; align-items: center; justify-content: center; letter-spacing: 0.4mm;
  }
  .corner {
    border: 0.5mm dashed #94a3b8; border-radius: 2mm;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    font-size: 4.4mm; font-weight: 900; color: #334155; text-align: center; line-height: 1.3;
  }
  .ghead {
    background: #fff; border-radius: 2.2mm; border-top: 2.8mm solid var(--c);
    padding: 2.2mm 2.4mm; display: flex; flex-direction: column; justify-content: flex-start;
    box-shadow: 0 0 0 0.35mm #cbd5e1 inset;
  }
  .ghead .gnum { font-size: 4.2mm; font-weight: 900; color: var(--c); }
  .ghead .gtitle { font-size: 4.8mm; font-weight: 800; line-height: 1.15; margin-top: 0.8mm; color: #0f172a; }
  .ghead .gsub { font-size: 3.3mm; color: #475569; line-height: 1.25; margin-top: 0.8mm; }

  .phead {
    background: #fff; border-radius: 2.2mm; border-left: 2.8mm solid var(--c);
    padding: 1.8mm 2.2mm; display: flex; flex-direction: column; justify-content: center;
    box-shadow: 0 0 0 0.35mm #cbd5e1 inset;
  }
  .phead .pnum { font-size: 4.4mm; font-weight: 900; color: var(--c); }
  .phead .picon { font-size: 9mm; line-height: 1.15; margin: 0.5mm 0; }
  .phead .pname { font-size: 4.6mm; font-weight: 800; line-height: 1.15; color: #0f172a; }
  .phead .pbadge { font-size: 3.5mm; color: #475569; font-weight: 600; margin-top: 0.6mm; }

  .tile {
    position: relative; background: #fff; border-radius: 2.4mm;
    border: 0.6mm solid var(--c); border-top-width: 2.4mm;
    padding: 1.8mm 2.2mm 1.6mm 2.2mm;
    display: flex; flex-direction: column; justify-content: space-between;
    overflow: hidden;
  }
  .tile::after {
    content: ""; position: absolute; inset: 0; background: var(--c); opacity: 0.05; pointer-events: none;
  }
  .t-top { display: flex; justify-content: space-between; align-items: baseline; font-weight: 800; }
  .t-z { font-size: 7.2mm; color: #b45309; line-height: 1; font-weight: 900; }
  .t-origin { font-size: 4.2mm; color: #334155; font-weight: 700; white-space: nowrap; }
  .t-mass { font-size: 4.2mm; color: #0f172a; font-weight: 800; background: #f1f5f9; border: 0.25mm solid #cbd5e1; border-radius: 1mm; padding: 0.2mm 1mm; }
  .t-symbol { font-size: 26mm; font-weight: 900; text-align: center; line-height: 0.95; color: var(--c); letter-spacing: -0.5mm; margin: 0.2mm 0; }
  .t-name { font-size: 5.2mm; font-weight: 900; text-align: center; color: #0f172a; line-height: 1.1;
            letter-spacing: -0.15mm; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .t-val { display: flex; justify-content: center; gap: 1.2mm; margin-top: 0.6mm; }
  .vb { font-size: 3.8mm; font-weight: 800; border-radius: 1mm; padding: 0.3mm 1mm; border: 0.3mm solid; }
  .vb.ac { color: #0369a1; border-color: #38bdf8; background: #f0f9ff; }
  .vb.tn { color: #b91c1c; border-color: #f87171; background: #fef2f2; }
  .vb.cp { color: #b45309; border-color: #fbbf24; background: #fffbeb; }
  .vb.az { color: #7e22ce; border-color: #c084fc; background: #faf5ff; }
  .t-aromas { display: flex; justify-content: center; gap: 1.8mm; font-size: 4mm; color: #334155; font-weight: 800; margin-top: 0.6mm; }
  .t-aromas span { white-space: nowrap; }
  .t-chem { font-size: 3.1mm; color: #64748b; font-weight: 500; text-align: center; font-style: italic; line-height: 1.15;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 0.3mm; }

  /* ---------- SIDEBAR (Designer-optimized 0-gap vertical fill) ---------- */
  .side {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: 4.5mm;
    min-height: 0;
  }
  .box {
    background: #fff;
    border-radius: 3.4mm;
    padding: 4.4mm 5.2mm;
    box-shadow: 0 0 0 0.4mm #cbd5e1 inset;
  }
  .box h3 {
    font-size: 5.6mm;
    font-weight: 900;
    color: #7f1d1d;
    margin-bottom: 2.2mm;
    letter-spacing: 0.3mm;
  }
  
  /* Box 1: Anatomy (1:1 scale sample tile) */
  .anat { display: grid; grid-template-columns: 82mm 1fr; gap: 5.5mm; align-items: center; }
  .anat .tile { height: 75mm; --c: #b91c1c; }
  .anat ol { list-style: none; font-size: 4.6mm; line-height: 1.48; color: #1e293b; }
  .anat li { margin-bottom: 1.6mm; }
  .anat li:last-child { margin-bottom: 0; }
  .anat li b { color: #0f172a; font-weight: 800; }
  .num { display: inline-flex; width: 5.4mm; height: 5.4mm; border-radius: 50%; background: #f59e0b; color: #fff;
         font-size: 3.5mm; font-weight: 900; align-items: center; justify-content: center; margin-right: 1.4mm; }

  /* Box 2: Top 30 Varieties Stacked Bar Chart */
  .top-var { padding: 4.4mm 5.2mm; }
  .top-var-sub { font-size: 3.7mm; color: #475569; font-weight: 600; margin-top: -1.2mm; margin-bottom: 3.2mm; }
  .top-var-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5.5mm; }
  .top-var-col { display: flex; flex-direction: column; gap: 2.3mm; }
  .top-var-item { display: flex; flex-direction: column; gap: 0.8mm; }
  .top-var-meta { display: flex; justify-content: space-between; align-items: baseline; }
  .top-var-left { display: flex; align-items: center; gap: 1.5mm; min-width: 0; overflow: hidden; }
  .top-var-rank { font-size: 4.2mm; font-weight: 900; color: #b45309; width: 7.6mm; flex-shrink: 0; }
  .top-var-dot { width: 3.5mm; height: 3.5mm; border-radius: 50%; flex-shrink: 0; }
  .top-var-name { font-size: 4.2mm; font-weight: 800; color: #0f172a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .top-var-total { font-size: 3.5mm; color: #475569; white-space: nowrap; margin-left: 1.5mm; flex-shrink: 0; }
  .top-var-total b { color: #0f172a; font-weight: 800; }
  .top-var-bar { display: flex; height: 6.2mm; border-radius: 1.4mm; overflow: hidden; background: #e2e8f0; font-size: 3.1mm; font-weight: 800; color: #fff; line-height: 6.2mm; }
  .tseg { display: flex; align-items: center; justify-content: center; overflow: hidden; white-space: nowrap; padding: 0 1mm; text-overflow: ellipsis; }
  .tseg span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

  /* Box 3: Climates */
  .clim-row { display: flex; gap: 3.2mm; align-items: flex-start; margin-bottom: 2.4mm; font-size: 4.3mm; line-height: 1.38; color: #1e293b; }
  .clim-row:last-child { margin-bottom: 0; }
  .clim-row .sw { flex: 0 0 6.8mm; height: 6.8mm; border-radius: 1.5mm; margin-top: 0.3mm; }
  .clim-row b { color: #0f172a; font-weight: 800; }

  /* Box 4: Aromas 54 Index */
  .aromas-cols { column-count: 2; column-gap: 6.5mm; font-size: 4.4mm; line-height: 1.66; color: #1e293b; }
  .aromas-cols .fam { font-weight: 900; color: #7f1d1d; font-size: 4.9mm; margin-top: 1.8mm; margin-bottom: 0.6mm; break-after: avoid; }
  .aromas-cols .fam:first-child { margin-top: 0; }
  .aromas-cols .ar { margin-bottom: 0.4mm; }
  .aromas-cols .ar b { display: inline-block; min-width: 7.2mm; color: #b45309; font-weight: 800; }
  .aromas-cols .ar i { color: #64748b; font-size: 3.5mm; font-weight: 500; }

  /* Box 5: Dynasties */
  .dyn-card { font-size: 4.4mm; line-height: 1.44; color: #1e293b; margin-bottom: 2.4mm; padding: 3mm 4mm; background: #f8fafc; border-radius: 1.8mm; border-left: 2mm solid #f59e0b; }
  .dyn-card:last-of-type { margin-bottom: 0; }
  .dyn-card.d-pinot { border-left-color: #ca8a04; }
  .dyn-card.d-cab { border-left-color: #991b1b; }
  .dyn-card.d-sav { border-left-color: #0ea5e9; }
  .dyn-card.d-iber { border-left-color: #dc2626; }
  .dyn-card b { color: #0f172a; font-weight: 800; }
  .dyn-note { font-size: 3.5mm; color: #64748b; font-style: italic; margin-top: 2mm; }

  /* ---------- FOOTER ---------- */
  .foot { display: flex; justify-content: space-between; align-items: center; font-size: 4.2mm; color: #475569; font-weight: 600;
          border-top: 0.6mm solid #cbd5e1; padding-top: 2.5mm; }
  .foot b { color: #7f1d1d; font-weight: 800; }
</style>
</head>
<body>
<div class="poster">
  <header class="head">
    <div class="brand">
      <div class="brand-logo-wrap">
        <img class="brand-logo-img" src="../assets/logo.svg" alt="WINE³ai" />
        <div class="brand-logo">WINE<sup>³</sup><span class="ai">ai</span></div>
      </div>
      <div class="title-block">
        <h1>__H1_TITLE__</h1>
        <p>__H1_SUB__</p>
      </div>
    </div>
    <div class="head-formula">
      <div class="formula">__FORMULA_HEAD__</div>
      <div class="formula-sub">__FORMULA_SUB__</div>
    </div>
  </header>

  <section class="body">
    <div class="table-grid" id="grid"></div>

    <aside class="side">
      <div class="box">
        <h3>__ANAT_TITLE__</h3>
        <div class="anat">
          <div class="tile">
            <div class="t-top"><span class="t-z">5</span><span class="t-origin">🇪🇸 74 DOs</span><span class="t-mass">4.0</span></div>
            <div class="t-symbol" style="font-size:24mm !important;">Te</div>
            <div class="t-name">Tempranillo</div>
            <div class="t-val"><span class="vb ac">Ac 3</span><span class="vb tn">Tn 4</span><span class="vb cp">Cp 4</span></div>
            <div class="t-aromas"><span>🍒 13</span><span>🪵 52</span><span>🌿 35</span></div>
            <div class="t-chem">Beta-damascenona, Ciclona</div>
          </div>
          <ol>
            __ANAT_LIST__
          </ol>
        </div>
      </div>

      __TOP_CHART__

      <div class="box climates">
        <h3>__CLIMATES_TITLE__</h3>
        __CLIMATES_BODY__
      </div>

      <div class="box aromas-box">
        <h3>__AROMAS_TITLE__</h3>
        <div class="aromas-cols" id="aromas"></div>
      </div>

      <div class="box dyn">
        <h3>__DYN_TITLE__</h3>
        __DYN_BODY__
      </div>
    </aside>
  </section>

  <footer class="foot">
    <div>__FOOT_LEFT__</div>
    <div>__FOOT_RIGHT__<span id="ed"></span></div>
  </footer>
</div>

<script src="../data/aromas_nez_du_vin.js"></script>
<script src="../data/periodic_table_grapes.js"></script>
<script src="../data/grape_varieties.js"></script>
<script>
(function () {
  const LANG = "__LANG__";
  const isEs = LANG === "es";
  const D = window.PERIODIC_TABLE_DATA;
  const AR = window.AROMAS_NEZ_DU_VIN || [];
  const GV = window.GRAPE_VARIETIES_DATA || [];
  const grid = document.getElementById('grid');
  const climateCol = { C1: '#0ea5e9', C2: '#10b981', C3: '#f59e0b' };
  const macroCol = { W1: '#ca8a04', W2: '#991b1b', W3: '#7c3aed' };
  const add = (cls, col, row, html, style) => {
    const d = document.createElement('div');
    d.className = cls; d.style.gridColumn = col; d.style.gridRow = row;
    if (style) Object.assign(d.style, style);
    d.innerHTML = html; grid.appendChild(d); return d;
  };
  const flagFor = (c) => {
    const m = { 'españa':'🇪🇸','spain':'🇪🇸','francia':'🇫🇷','france':'🇫🇷','italia':'🇮🇹','italy':'🇮🇹','portugal':'🇵🇹',
      'alemania':'🇩🇪','germany':'🇩🇪','austria':'🇦🇹','grecia':'🇬🇷','greece':'🇬🇷','georgia':'🇬🇪','hungría':'🇭🇺',
      'hungary':'🇭🇺','croacia':'🇭🇷','argentina':'🇦🇷','chile':'🇨🇱','estados unidos':'🇺🇸','usa':'🇺🇸' };
    const k = (c || '').toLowerCase();
    for (const key in m) if (k.includes(key)) return m[key];
    return '🍇';
  };

  // Corner + macro bands
  add('corner', '1 / 3', '1 / 3', '__CORNER_TEXT__');
  D.macroCategories.forEach((m, i) => {
    const title = isEs ? m.title_es : m.title_en;
    add('wband', `${3 + i * 3} / span 3`, '1', title, { background: macroCol[m.id] });
  });
  D.macroClimates.forEach((c, i) => {
    const title = (isEs ? c.title_es : c.title_en).split(',')[0];
    add('cband', '1', `${3 + i * 3} / span 3`, title, { background: climateCol[c.id] });
  });

  // Group headers
  D.groups.forEach(g => {
    const title = isEs ? g.title_es : g.title_en;
    const sub = isEs ? g.subtitle_es : g.subtitle_en;
    const el = add('ghead', `${g.group + 2}`, '2',
      `<div class="gnum">G${g.group} · ${g.macro}</div><div class="gtitle">${title}</div><div class="gsub">${sub}</div>`);
    el.style.setProperty('--c', g.color);
  });

  // Period headers
  (D.periods || []).forEach(p => {
    const name = isEs ? p.climate_es : p.climate_en;
    const badge = isEs ? p.badge_es : p.badge_en;
    const el = add('phead', '2', `${p.period + 2}`,
      `<div class="pnum">P${p.period} · ${p.macro}</div><div class="picon">${p.icon}</div><div class="pname">${name}</div><div class="pbadge">${badge}</div>`);
    el.style.setProperty('--c', climateCol[p.macro]);
  });

  // Tiles
  D.elements.forEach(el => {
    const g = D.groups.find(x => x.group === el.group);
    const gv = GV.find(x => x.id === el.id || x.name.toLowerCase() === el.name.toLowerCase());
    let origin = flagFor(el.country);
    const regSuffix = isEs ? 'DOs' : 'DOs';
    if (gv && gv.countries_breakdown && gv.countries_breakdown.length) {
      origin = `${gv.countries_breakdown[0].flag || origin} ${gv.total_regions} ${regSuffix}`;
    }
    const ac = el.acidity || 3, body = el.body || Math.round(el.atomicMass);
    let val;
    if (el.color === 'red') {
      val = `<span class="vb ac">Ac ${ac}</span><span class="vb tn">Tn ${el.tannin || 3}</span><span class="vb cp">Cp ${body}</span>`;
    } else if (el.group === 9 || (el.sweetness && el.sweetness > 2)) {
      val = `<span class="vb ac">Ac ${ac}</span><span class="vb az">Az ${el.sweetness || 4}</span><span class="vb cp">Cp ${body}</span>`;
    } else {
      val = `<span class="vb ac">Ac ${ac}</span><span class="vb cp">Cp ${body}</span>`;
    }
    const aromas = (el.aroma_ids || []).slice(0, 3).map(n => {
      const a = AR.find(x => x.number === n); return a ? `<span>${a.icon} ${n}</span>` : '';
    }).join('');
    const chem = (el.key_compounds || '').split(',').slice(0, 2).join(', ');
    const t = add('tile', `${el.group + 2}`, `${el.period + 2}`, `
      <div class="t-top"><span class="t-z">${el.atomicNumber}</span><span class="t-origin">${origin}</span><span class="t-mass">${el.atomicMass.toFixed(1)}</span></div>
      <div class="t-symbol">${el.symbol}</div>
      <div class="t-name">${el.name}</div>
      <div class="t-val">${val}</div>
      <div class="t-aromas">${aromas}</div>
      <div class="t-chem">${chem}</div>`);
    t.style.setProperty('--c', g ? g.color : '#64748b');
  });

  // Aroma index
  const fams = isEs ? [
    ['fruity', '🍏 Frutales (1–23)'], ['floral', '🌸 Florales (24–29)'],
    ['vegetal_spicy', '🌿 Vegetales & Especiados (30–44)'], ['animal', '👞 Animales (45–47)'],
    ['roasted', '🪵 Tostados & Torrefactos (48–54)']
  ] : [
    ['fruity', '🍏 Fruity Notes (1–23)'], ['floral', '🌸 Floral Notes (24–29)'],
    ['vegetal_spicy', '🌿 Vegetal & Spicy Notes (30–44)'], ['animal', '👞 Animal Notes (45–47)'],
    ['roasted', '🪵 Roasted & Smoky Notes (48–54)']
  ];

  const box = document.getElementById('aromas');
  box.innerHTML = fams.map(([k, label]) =>
    `<div class="fam">${label}</div>` +
    AR.filter(a => a.family === k).map(a => {
      const aName = isEs ? a.name_es : (a.name_en || a.name_es);
      return `<div class="ar"><b>${a.number}</b>${a.icon} ${aName} <i>${(a.molecule || '').split(',')[0]}</i></div>`;
    }).join('')
  ).join('');

  const dateLocale = isEs ? 'es-ES' : 'en-US';
  document.getElementById('ed').textContent = new Date().toLocaleDateString(dateLocale, { month: 'long', year: 'numeric' });
  document.body.setAttribute('data-ready', '1');
})();
</script>
</body>
</html>"""

def generate_poster_html(lang='es'):
    is_es = lang == 'es'
    top_chart = build_top_chart_html(lang)

    page_title = "Tabla Periódica del Vino WINE³ai — Póster DIN-A0" if is_es else "The Periodic Table of Wine WINE³ai — DIN-A0 Poster"
    h1_title = "Tabla Periódica del Vino &amp; Terruño" if is_es else "The Periodic Table of Wine &amp; Terroir"
    h1_sub = "81 variedades de uva ordenadas por estilo (columnas) y clima (filas) · calibradas con los 54 aromas de <i>Le Nez du Vin</i>" if is_es else "81 grape varieties arranged by style (columns) and climate (rows) · calibrated with the 54 aromas of <i>Le Nez du Vin</i>"
    formula_head = "3 Estilos <span>×</span> 3 Climas <span>×</span> 9 = 81" if is_es else "3 Styles <span>×</span> 3 Climates <span>×</span> 9 = 81"
    formula_sub = ("W¹ Blancos · W² Tintos · W³ Método &amp; Singulares<br>C¹ Fresco/Atlántico · C² Templado/Continental · C³ Cálido/Mediterráneo"
                   if is_es else
                   "W¹ Whites · W² Reds · W³ Method &amp; Heritage Terroir<br>C¹ Cool/Atlantic · C² Temperate/Continental · C³ Warm/Mediterranean")
    corner_text = "ESTILO →<br>╲<br>↓ CLIMA" if is_es else "STYLE →<br>╲<br>↓ CLIMATE"

    anat_title = "🔬 ANATOMÍA ENOLÓGICA DE CADA CASILLA" if is_es else "🔬 OENOLOGICAL ANATOMY OF EACH TILE"
    anat_list = ("""
            <li><span class="num">1</span><b>Nº atómico (Z 1–81):</b> posición ordinal única en la matriz cartesiana 9×9.</li>
            <li><span class="num">2</span><b>Origen + DOs:</b> país de origen y total de denominaciones oficiales protegidas.</li>
            <li><span class="num">3</span><b>Masa (A 1.0–5.0):</b> cuerpo, densidad, extracto seco y peso táctil en boca.</li>
            <li><span class="num">4</span><b>Símbolo:</b> abreviatura mnemotécnica de 2 letras en formato atómico destacado.</li>
            <li><span class="num">5</span><b>Valencias (1–5):</b> <b>Ac</b> acidez · <b>Tn</b> tanino · <b>Cp</b> cuerpo/crianza · <b>Az</b> azúcar residual.</li>
            <li><span class="num">6</span><b>Aromas:</b> descriptores olfativos dominantes de <i>Le Nez du Vin</i> (ver índice numerado).</li>
    """ if is_es else """
            <li><span class="num">1</span><b>Atomic No. (Z 1–81):</b> unique ordinal position in the 9×9 Cartesian matrix.</li>
            <li><span class="num">2</span><b>Origin + DOs:</b> country flag and total number of official protected appellations.</li>
            <li><span class="num">3</span><b>Mass (A 1.0–5.0):</b> body, density, dry extract, and palate weight.</li>
            <li><span class="num">4</span><b>Symbol:</b> 2-letter mnemonic chemical symbol in bold atomic display.</li>
            <li><span class="num">5</span><b>Valences (1–5):</b> <b>Ac</b> acidity · <b>Tn</b> tannin · <b>Cp</b> body/aging · <b>Az</b> residual sweetness.</li>
            <li><span class="num">6</span><b>Aromas:</b> dominant aroma descriptors from <i>Le Nez du Vin</i> (see numbered index).</li>
    """)

    climates_title = "🌍 FILAS = CLIMA · COLUMNAS = ESTILO" if is_es else "🌍 ROWS = CLIMATE · COLUMNS = STYLE"
    climates_body = ("""
        <div class="clim-row"><span class="sw" style="background:#0ea5e9"></span><span><b>C¹ Fresco, Atlántico &amp; Alpino (P1–P3):</b> acidez cortante, ciclo vegetativo largo, tensión mineral, graduación moderada y gran frescura.</span></div>
        <div class="clim-row"><span class="sw" style="background:#10b981"></span><span><b>C² Templado &amp; Continental (P4–P6):</b> riberas fluviales, mesetas centrales y valles de acusada oscilación térmica día/noche.</span></div>
        <div class="clim-row"><span class="sw" style="background:#f59e0b"></span><span><b>C³ Cálido, Mediterráneo &amp; Volcánico (P7–P9):</b> insolación plena, suelos de lava y esquisto, asoleo, crianza biológica de flor y soleras.</span></div>
        <div class="clim-row"><span class="sw" style="background:linear-gradient(90deg,#ca8a04,#991b1b,#7c3aed)"></span><span><b>G1–G3 Blancos · G4–G6 Tintos · G7–G9 Singulares:</b> Espumosos nobles, Rosados/Ancestrales y Generosos/Dulces de guarda.</span></div>
    """ if is_es else """
        <div class="clim-row"><span class="sw" style="background:#0ea5e9"></span><span><b>C¹ Cool, Atlantic &amp; Alpine (P1–P3):</b> high acid tension, extended ripening cycle, mineral drive, moderate alcohol, and crispness.</span></div>
        <div class="clim-row"><span class="sw" style="background:#10b981"></span><span><b>C² Temperate &amp; Continental (P4–P6):</b> river basins, plateau mesetas, and pronounced diurnal temperature shifts.</span></div>
        <div class="clim-row"><span class="sw" style="background:#f59e0b"></span><span><b>C³ Warm, Mediterranean &amp; Volcanic (P7–P9):</b> abundant sun, volcanic lava &amp; schist, raisining, biological flor aging, and secular soleras.</span></div>
        <div class="clim-row"><span class="sw" style="background:linear-gradient(90deg,#ca8a04,#991b1b,#7c3aed)"></span><span><b>G1–G3 Whites · G4–G6 Reds · G7–G9 Special:</b> Noble Sparkling, Rosé/Skin-Contact, and Fortified/Noble Sweet.</span></div>
    """)

    aromas_title = "👃 ÍNDICE SENSORIAL DE AROMAS · LE NEZ DU VIN (54)" if is_es else "👃 SENSORY AROMA INDEX · LE NEZ DU VIN (54)"
    dyn_title = "🧬 LAS GRANDES DINASTÍAS GENÉTICAS (VIVC)" if is_es else "🧬 MAJOR GENETIC DYNASTIES (VIVC)"
    dyn_body = ("""
        <div class="dyn-card d-pinot"><b>👑 Dinastía Borgoñona (Pinot Noir × Gouais Blanc):</b> Chardonnay · Gamay · Aligoté · Melon de Bourgogne</div>
        <div class="dyn-card d-cab"><b>👑 Dinastía Bordelesa (Cabernet Franc):</b> Cabernet Sauvignon (× Sauvignon Blanc) · Merlot (× Magdeleine Noire) · Carmenère (× Gros Cabernet)</div>
        <div class="dyn-card d-sav"><b>👑 Dinastía Savagnin / Traminer:</b> Sauvignon Blanc · Grüner Veltliner · Verdejo y Godello (hermanas biológicas, × Castellana Blanca)</div>
        <div class="dyn-card d-iber"><b>👑 Dinastías Ibéricas Ancestrales:</b> Tempranillo (Albillo Mayor × Benedicto) · Hebén (madre morisca de Pedro Ximénez y Macabeo)</div>
        <p class="dyn-note">Pedigríes certificados por marcadores moleculares de ADN (SSR) · Vitis International Variety Catalogue (Julius Kühn-Institut)</p>
    """ if is_es else """
        <div class="dyn-card d-pinot"><b>👑 Burgundian Dynasty (Pinot Noir × Gouais Blanc):</b> Chardonnay · Gamay · Aligoté · Melon de Bourgogne</div>
        <div class="dyn-card d-cab"><b>👑 Bordeaux Dynasty (Cabernet Franc):</b> Cabernet Sauvignon (× Sauvignon Blanc) · Merlot (× Magdeleine Noire) · Carmenère (× Gros Cabernet)</div>
        <div class="dyn-card d-sav"><b>👑 Savagnin / Traminer Dynasty:</b> Sauvignon Blanc · Grüner Veltliner · Verdejo &amp; Godello (biological siblings, × Castellana Blanca)</div>
        <div class="dyn-card d-iber"><b>👑 Ancient Iberian Patriarchs:</b> Tempranillo (Albillo Mayor × Benedicto) · Hebén (Moorish matriarch of Pedro Ximénez &amp; Macabeo)</div>
        <p class="dyn-note">Pedigrees certified by molecular SSR DNA markers · Vitis International Variety Catalogue (Julius Kühn-Institut)</p>
    """)

    foot_left = ("<b>WINE³ai</b> — Proyecto abierto geoespacial y vitícola · <span style='color:#5E1C37;font-weight:900;'>wine3ai.jreyes13.net</span>"
                 if is_es else
                 "<b>WINE³ai</b> — Open Geospatial &amp; Viticultural Project · <span style='color:#5E1C37;font-weight:900;'>wine3ai.jreyes13.net</span>")
    foot_right = ("Fuentes: Consejos Reguladores Oficiales, VIVC (Julius Kühn-Institut), Jean Lenoir — <i>Le Nez du Vin</i> · Edición: "
                  if is_es else
                  "Sources: Official Regulatory Councils, VIVC (Julius Kühn-Institut), Jean Lenoir — <i>Le Nez du Vin</i> · Edition: ")

    html = HTML_TEMPLATE
    replacements = {
        '__LANG__': lang,
        '__PAGE_TITLE__': page_title,
        '__H1_TITLE__': h1_title,
        '__H1_SUB__': h1_sub,
        '__FORMULA_HEAD__': formula_head,
        '__FORMULA_SUB__': formula_sub,
        '__CORNER_TEXT__': corner_text,
        '__ANAT_TITLE__': anat_title,
        '__ANAT_LIST__': anat_list,
        '__TOP_CHART__': top_chart,
        '__CLIMATES_TITLE__': climates_title,
        '__CLIMATES_BODY__': climates_body,
        '__AROMAS_TITLE__': aromas_title,
        '__DYN_TITLE__': dyn_title,
        '__DYN_BODY__': dyn_body,
        '__FOOT_LEFT__': foot_left,
        '__FOOT_RIGHT__': foot_right,
    }

    for k, v in replacements.items():
        html = html.replace(k, v)

    return html

# Write ES, EN and default
es_html = generate_poster_html('es')
en_html = generate_poster_html('en')

print_dir = '/Users/jreyes13/GitHub/WINE3ai/print'
es_html_path = os.path.join(print_dir, 'poster_a0_es.html')
en_html_path = os.path.join(print_dir, 'poster_a0_en.html')
def_html_path = os.path.join(print_dir, 'poster_a0.html')

with open(es_html_path, 'w', encoding='utf-8') as f:
    f.write(es_html)

with open(en_html_path, 'w', encoding='utf-8') as f:
    f.write(en_html)

with open(def_html_path, 'w', encoding='utf-8') as f:
    f.write(es_html)

print("Generated HTML posters successfully.")

# Generate PDFs via Google Chrome headless
chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if os.path.exists(chrome_bin):
    es_pdf = os.path.join(print_dir, 'WINE3ai_Tabla_Periodica_A0_ES.pdf')
    en_pdf = os.path.join(print_dir, 'WINE3ai_Periodic_Table_A0_EN.pdf')
    def_pdf = os.path.join(print_dir, 'WINE3ai_Tabla_Periodica_A0.pdf')

    print("Rendering ES PDF via Chrome headless...")
    subprocess.run([
        chrome_bin, '--headless=new', '--disable-gpu',
        '--run-all-compositor-stages-before-draw',
        '--no-pdf-header-footer',
        f'--print-to-pdf={es_pdf}',
        f'file://{es_html_path}'
    ], check=True)

    print("Rendering EN PDF via Chrome headless...")
    subprocess.run([
        chrome_bin, '--headless=new', '--disable-gpu',
        '--run-all-compositor-stages-before-draw',
        '--no-pdf-header-footer',
        f'--print-to-pdf={en_pdf}',
        f'file://{en_html_path}'
    ], check=True)

    import shutil
    shutil.copyfile(es_pdf, def_pdf)
    print("PDF generation complete: ES, EN, and default A0 vector PDFs created.")
