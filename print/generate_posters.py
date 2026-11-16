import json
import re
import os

# Load grape varieties
gv_path = '/Users/jreyes13/GitHub/wine3ai/data/grape_varieties.json'
with open(gv_path, encoding='utf-8') as f:
    all_grapes = json.load(f)

# Sort by total_regions descending
all_grapes.sort(key=lambda g: -g.get('total_regions', 0))

# Colors for country bars
country_colors = {
    'Francia': '#1d4ed8', 'France': '#1d4ed8',
    'España': '#dc2626', 'Spain': '#dc2626',
    'Italia': '#059669', 'Italy': '#059669',
    'Alemania': '#d97706', 'Germany': '#d97706',
    'Hungría': '#0284c7', 'Hungary': '#0284c7',
    'Portugal': '#16a34a',
    'Austria': '#9333ea',
    'Turquía': '#b91c1c', 'Turkey': '#b91c1c',
    'Líbano': '#ea580c', 'Lebanon': '#ea580c',
    'Eslovenia': '#4f46e5', 'Slovenia': '#4f46e5',
    'Otros': '#64748b', 'Others': '#64748b', 'Rest': '#64748b'
}

def generate_top_varieties_html(lang='es'):
    top = all_grapes[:8]
    items_html = []
    
    is_es = lang == 'es'
    other_label = 'Otros' if is_es else 'Others'
    reg_label = 'DOs / Reg.' if is_es else 'Appell.'
    countries_lbl = 'países' if is_es else 'countries'

    for rank, g in enumerate(top, 1):
        name = g['name']
        color = g.get('color', 'red')
        dot_color = '#ef4444' if color == 'red' else '#ca8a04'
        total = g.get('total_regions', 0)
        c_count = g.get('countries_count', 0)
        breakdown = g.get('countries_breakdown', [])

        segments = []
        accum_pct = 0.0
        # take top 3 or 4 countries
        for c in breakdown[:4]:
            pct = c.get('percentage', 0.0)
            accum_pct += pct
            c_name = c.get('country_es' if is_es else 'country_en', c.get('country'))
            c_col = country_colors.get(c.get('country'), '#64748b')
            flag = c.get('flag', '')
            cnt = c.get('count', 0)
            segments.append(f'<div class="tseg" style="width:{pct:.1f}%;background:{c_col};" title="{c_name}: {cnt} ({pct:.1f}%)"><span>{flag} {c_name} {pct:.0f}%</span></div>')

        rem_pct = max(0.0, 100.0 - accum_pct)
        if rem_pct >= 2.0:
            rem_count = total - sum(c.get('count', 0) for c in breakdown[:4])
            rem_c_count = max(1, c_count - min(4, len(breakdown)))
            segments.append(f'<div class="tseg tseg-other" style="width:{rem_pct:.1f}%;background:#64748b;" title="{other_label} ({rem_c_count} {countries_lbl}): {rem_count}"><span>+{rem_c_count} {other_label} {rem_pct:.0f}%</span></div>')

        bar_html = ''.join(segments)
        item = f'''
        <div class="top-var-item">
          <div class="top-var-meta">
            <span class="top-var-rank">#{rank}</span>
            <span class="top-var-dot" style="background:{dot_color};"></span>
            <span class="top-var-name">{name}</span>
            <span class="top-var-total">{total} {reg_label} · {c_count} {countries_lbl}</span>
          </div>
          <div class="top-var-bar">{bar_html}</div>
        </div>'''
        items_html.append(item)

    title = "📊 VARIEDADES MÁS CULTIVADAS & PRESENCIA GLOBAL" if is_es else "📊 MOST CULTIVATED VARIETIES & GLOBAL SPREAD"
    subtitle = "Distribución porcentual por países en denominaciones oficiales" if is_es else "Share of official appellations cultivating benchmark noble grapes"

    return f'''
      <div class="box top-var">
        <h3>{title}</h3>
        <div class="top-var-sub">{subtitle}</div>
        <div class="top-var-list">
          {''.join(items_html)}
        </div>
      </div>'''

print("Generated top varieties sample length:", len(generate_top_varieties_html('es')))
