# -*- coding: utf-8 -*-
"""
Script que genera de manera integral el archivo:
'TP-cuatrimestral-3ra_entrega-Rosa_Kimel_Connon.html'
con todos los resultados reales ejecutados sobre F1DB PostgreSQL 16.
"""
import json
import os
import table_formatters as tf

with open('all_query_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract summary statistics for facts and charts
# Poles win rate
tasa_pole_clasica = [r for r in data['q02'] if 'Clasica' in r['era'] and r['franja'] == 'P1 (Pole)'][0]['pct_victoria']
tasa_pole_moderna = [r for r in data['q02'] if 'Moderna' in r['era'] and r['franja'] == 'P1 (Pole)'][0]['pct_victoria']

# HHI
hhi_clasica = [r for r in data['q04'] if 'Clasica' in r['era']][0]['hhi']
hhi_moderna = [r for r in data['q04'] if 'Moderna' in r['era']][0]['hhi']

# Motor Mercedes share moderna
mercedes_share_moderna = [r for r in data['q05'] if 'Moderna' in r['era'] and r['motor'] == 'Mercedes'][0]['pct_era']

# Mechanical breakdown rate
falla_mec_clasica = [r for r in data['q11'] if 'Clasica' in r['era']][0]['pct_abandono_mecanico']
falla_mec_moderna = [r for r in data['q11'] if 'Moderna' in r['era']][0]['pct_abandono_mecanico']

# Champions from pole
campeon_pole_clasica = [r for r in data['q09'] if 'Clasica' in r['era']][0]['pct_desde_pole']
campeon_pole_moderna = [r for r in data['q09'] if 'Moderna' in r['era']][0]['pct_desde_pole']

# Build the complete HTML
html_content = f"""<!doctype html>
<html lang="es" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Las eras de la F1 — Tercera Entrega · Análisis SQL Completo</title>
  <meta name="description" content="Tercera Entrega Trabajo Práctico de Base de Datos – Licenciatura en Ciencia de Datos. Análisis SQL avanzado sobre F1DB PostgreSQL 16. Evaluación cuantitativa y causal del peso de la grilla y el motor.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400;1,6..72,600&family=Public+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    :root {{
      --ground: #F0EFED;
      --surface: #FFFFFF;
      --surface-2: #F8F7F5;
      --ink: #16130F;
      --muted: #5A4F4A;
      --line: #DDD8D4;
      --accent: #C01717;
      --accent-soft: #F7EDEC;
      --accent-2: #1A4FA0;
      --accent-2-soft: #EAF0FB;
      --gold: #9C6A08;
      --gold-soft: #FBF5E6;
      --new-badge: #0D7A5A;
      --new-badge-soft: #E6F5F0;
      --shadow: 0 1px 3px rgba(22,19,15,.07), 0 8px 28px -14px rgba(22,19,15,.25);
      --shadow-lg: 0 2px 8px rgba(22,19,15,.1), 0 20px 40px -20px rgba(22,19,15,.3);
    }}
    @media (prefers-color-scheme: dark) {{
      :root:not([data-theme="light"]) {{
        --ground:#100E0C;--surface:#1A1714;--surface-2:#211D1B;--ink:#EDE9E5;
        --muted:#998F88;--line:#2C2622;--accent:#E84040;--accent-soft:#2C1010;
        --accent-2:#5B8EE0;--accent-2-soft:#0E1E3A;--gold:#DCA455;--gold-soft:#261E0A;
        --new-badge:#2DB88A;--new-badge-soft:#0C2A1F;
        --shadow:0 1px 3px rgba(0,0,0,.4),0 8px 28px -14px rgba(0,0,0,.7);
        --shadow-lg:0 2px 8px rgba(0,0,0,.5),0 20px 40px -20px rgba(0,0,0,.8);
      }}
    }}
    :root[data-theme="dark"] {{
      --ground:#100E0C;--surface:#1A1714;--surface-2:#211D1B;--ink:#EDE9E5;
      --muted:#998F88;--line:#2C2622;--accent:#E84040;--accent-soft:#2C1010;
      --accent-2:#5B8EE0;--accent-2-soft:#0E1E3A;--gold:#DCA455;--gold-soft:#261E0A;
      --new-badge:#2DB88A;--new-badge-soft:#0C2A1F;
      --shadow:0 1px 3px rgba(0,0,0,.4),0 8px 28px -14px rgba(0,0,0,.7);
      --shadow-lg:0 2px 8px rgba(0,0,0,.5),0 20px 40px -20px rgba(0,0,0,.8);
    }}

    *{{box-sizing:border-box}}
    body{{margin:0;background:var(--ground);color:var(--ink);font-family:"Public Sans",-apple-system,"Segoe UI",sans-serif;font-size:16.5px;line-height:1.68;-webkit-font-smoothing:antialiased}}
    .page{{max-width:1160px;margin:0 auto;padding:0 24px 120px}}
    .col{{max-width:72ch;margin:0 auto;width:100%}}
    .wide{{max-width:1120px;margin:0 auto;width:100%}}
    
    h1,h2,h3,h4{{font-family:"Newsreader",Georgia,serif;text-wrap:balance;margin:0}}
    h1{{font-size:clamp(2.4rem,5.5vw,3.9rem);line-height:1.06;font-weight:600;letter-spacing:-.015em}}
    h2{{font-size:clamp(1.6rem,3.2vw,2.2rem);font-weight:600;line-height:1.18}}
    h3{{font-size:1.24rem;font-weight:600;line-height:1.3}}
    h4{{font-size:1.05rem;font-weight:600;line-height:1.35}}
    p{{margin:0}}
    
    code{{font-family:"IBM Plex Mono",monospace;font-size:.86em;background:var(--accent-soft);padding:1px 5px;border-radius:3px;color:var(--accent)}}
    pre{{margin:0;background:var(--surface-2);border:1px solid var(--line);border-radius:5px;padding:16px 18px;overflow-x:auto;font-family:"IBM Plex Mono",monospace;font-size:.82rem;line-height:1.6;color:var(--ink)}}
    
    .eyebrow{{font-family:"IBM Plex Mono",monospace;font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:600}}
    .eyebrow.blue{{color:var(--accent-2)}}
    .eyebrow.gold{{color:var(--gold)}}
    .eyebrow.green{{color:var(--new-badge)}}

    header.cover{{padding:92px 0 60px;border-bottom:1px solid var(--line);position:relative;overflow:hidden}}
    header.cover::before{{content:"F1";position:absolute;right:-20px;top:-10px;font-family:"Newsreader",serif;font-size:22rem;font-weight:600;color:var(--accent);opacity:.04;pointer-events:none;line-height:1;user-select:none}}
    header.cover .col{{display:flex;flex-direction:column;gap:22px}}
    .lede{{font-family:"Newsreader",Georgia,serif;font-size:1.32rem;line-height:1.55;color:var(--muted)}}

    .meta{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:4px;overflow:hidden;margin:10px 0 0}}
    .meta div{{background:var(--surface);padding:12px 14px}}
    .meta dt{{font-family:"IBM Plex Mono",monospace;font-size:.67rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 3px}}
    .meta dd{{margin:0;font-size:.9rem;font-weight:600;font-variant-numeric:tabular-nums}}

    .theme-btn{{position:fixed;top:18px;right:20px;width:42px;height:42px;border-radius:50%;border:1px solid var(--line);background:var(--surface);box-shadow:var(--shadow);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1.15rem;z-index:100;transition:transform .15s,box-shadow .2s}}
    .theme-btn:hover{{transform:scale(1.08);box-shadow:var(--shadow-lg)}}

    nav.toc{{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:22px 24px;margin:36px 0 0;box-shadow:var(--shadow)}}
    nav.toc p.qlabel{{font-family:"IBM Plex Mono",monospace;font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 12px}}
    nav.toc ol{{margin:0;padding-left:1.3em;display:flex;flex-direction:column;gap:8px;font-size:.92rem}}
    nav.toc a{{color:var(--accent);text-decoration:none;font-weight:500}}
    nav.toc a:hover{{text-decoration:underline}}
    .badge-tag{{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:.62rem;letter-spacing:.08em;text-transform:uppercase;background:var(--accent-soft);color:var(--accent);padding:2px 6px;border-radius:3px;font-weight:600;margin-left:6px}}
    .badge-tag.green{{background:var(--new-badge-soft);color:var(--new-badge)}}
    .badge-tag.blue{{background:var(--accent-2-soft);color:var(--accent-2)}}

    section{{padding:68px 0 0}}
    .sec-head{{display:flex;flex-direction:column;gap:10px;margin-bottom:28px}}
    .sec-head .rule{{height:3px;background:var(--accent);width:48px;border-radius:2px}}
    .sec-head .rule.blue{{background:var(--accent-2)}}
    .sec-head .rule.gold{{background:var(--gold)}}
    .sec-head .rule.green{{background:var(--new-badge)}}
    .stack{{display:flex;flex-direction:column;gap:20px}}

    .facts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:16px 0}}
    .fact{{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:18px 20px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:6px;transition:box-shadow .2s,transform .2s}}
    .fact:hover{{box-shadow:var(--shadow-lg);transform:translateY(-2px)}}
    .fact .n{{font-family:"Newsreader",Georgia,serif;font-size:2.2rem;line-height:1;font-weight:600;color:var(--accent);font-variant-numeric:tabular-nums}}
    .fact .n.blue{{color:var(--accent-2)}}.fact .n.gold{{color:var(--gold)}}.fact .n.green{{color:var(--new-badge)}}
    .fact .l{{font-size:.86rem;color:var(--muted);line-height:1.38}}

    .query{{background:var(--surface);border:1px solid var(--line);border-radius:6px;box-shadow:var(--shadow);margin-bottom:38px;overflow:hidden;transition:box-shadow .2s}}
    .query:hover{{box-shadow:var(--shadow-lg)}}
    .query .qh{{padding:18px 22px 14px;border-bottom:1px solid var(--line);display:flex;gap:14px;align-items:baseline;flex-wrap:wrap;background:var(--surface-2)}}
    .qid{{font-family:"IBM Plex Mono",monospace;font-size:.78rem;font-weight:600;color:var(--accent);background:var(--accent-soft);padding:3px 9px;border-radius:3px;flex:none}}
    .qid.green{{color:var(--new-badge);background:var(--new-badge-soft)}}
    .qid.blue{{color:var(--accent-2);background:var(--accent-2-soft)}}
    .qid.gold{{color:var(--gold);background:var(--gold-soft)}}
    .qbody{{padding:22px 24px;display:flex;flex-direction:column;gap:20px}}
    .qlabel{{font-family:"IBM Plex Mono",monospace;font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 6px}}

    .tw{{overflow-x:auto;border:1px solid var(--line);border-radius:5px;margin:8px 0}}
    table{{border-collapse:collapse;width:100%;font-size:.87rem;font-variant-numeric:tabular-nums}}
    th,td{{padding:9px 13px;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap}}
    th{{font-family:"IBM Plex Mono",monospace;font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:600;background:var(--surface-2)}}
    tbody tr:last-child td{{border-bottom:none}}
    td.num,th.num{{text-align:right}}
    tbody tr.hl td{{background:var(--accent-soft);font-weight:600}}
    tbody tr.hl2 td{{background:var(--accent-2-soft);font-weight:600}}
    tbody tr.hlg td{{background:var(--gold-soft);font-weight:600}}
    tbody tr.hlnew td{{background:var(--new-badge-soft);font-weight:600}}

    .read{{border-left:3px solid var(--accent);padding:14px 18px;font-size:.95rem;color:var(--ink);background:var(--accent-soft);border-radius:0 5px 5px 0}}
    .read.blue{{border-color:var(--accent-2);background:var(--accent-2-soft)}}
    .read.green{{border-color:var(--new-badge);background:var(--new-badge-soft)}}
    .read.gold{{border-color:var(--gold);background:var(--gold-soft)}}
    .read strong{{color:var(--accent)}}.read.blue strong{{color:var(--accent-2)}}.read.green strong{{color:var(--new-badge)}}.read.gold strong{{color:var(--gold)}}

    .hyp{{background:var(--accent-soft);border-left:4px solid var(--accent);border-radius:0 6px 6px 0;padding:22px 24px;font-family:"Newsreader",Georgia,serif;font-size:1.22rem;line-height:1.55;font-style:italic}}
    ol.obj{{margin:0;padding-left:1.4em;display:flex;flex-direction:column;gap:12px}}
    ol.obj li::marker{{font-family:"IBM Plex Mono",monospace;color:var(--accent);font-weight:600}}

    .summary-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin:20px 0}}
    .sum-card{{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:18px 20px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:8px}}
    .sum-card .sc-head{{display:flex;align-items:center;gap:10px}}
    .sum-card .sc-num{{width:32px;height:32px;border-radius:50%;background:var(--accent);color:white;font-family:"IBM Plex Mono",monospace;font-size:.78rem;font-weight:600;display:flex;align-items:center;justify-content:center;flex:none}}
    .sum-card .sc-num.blue{{background:var(--accent-2)}}.sum-card .sc-num.gold{{background:var(--gold)}}.sum-card .sc-num.green{{background:var(--new-badge)}}
    .sum-card .sc-title{{font-weight:600;font-size:.96rem}}
    .sum-card p{{font-size:.88rem;color:var(--muted);line-height:1.5}}
    .sum-card .sc-result{{background:var(--surface-2);border-radius:4px;padding:8px 12px;font-family:"IBM Plex Mono",monospace;font-size:.78rem;color:var(--accent);border-left:2px solid var(--accent);margin-top:4px}}
    .sum-card .sc-result.blue{{color:var(--accent-2);border-color:var(--accent-2)}}.sum-card .sc-result.gold{{color:var(--gold);border-color:var(--gold)}}.sum-card .sc-result.green{{color:var(--new-badge);border-color:var(--new-badge)}}

    .pbar-group{{display:flex;flex-direction:column;gap:9px;margin:12px 0}}
    .pbar-item{{display:flex;flex-direction:column;gap:4px}}
    .pbar-label{{font-size:.83rem;display:flex;justify-content:space-between;color:var(--muted)}}
    .pbar-label strong{{color:var(--ink)}}
    .pbar-track{{height:10px;background:var(--surface-2);border-radius:5px;overflow:hidden;border:1px solid var(--line)}}
    .pbar-fill{{height:100%;border-radius:5px;background:var(--accent);transition:width 1.2s cubic-bezier(.4,0,.2,1)}}
    .pbar-fill.blue{{background:var(--accent-2)}}.pbar-fill.gold{{background:var(--gold)}}.pbar-fill.green{{background:var(--new-badge)}}

    .era-timeline{{display:flex;gap:0;border-radius:6px;overflow:hidden;border:1px solid var(--line);margin:16px 0}}
    .era-block{{flex:1;padding:14px 12px;text-align:center;background:var(--surface);border-right:1px solid var(--line)}}
    .era-block:last-child{{border-right:none}}
    .era-block .eb-label{{font-family:"IBM Plex Mono",monospace;font-size:.65rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}}
    .era-block .eb-val{{font-family:"Newsreader",serif;font-size:1.75rem;font-weight:600;color:var(--accent);line-height:1}}
    .era-block .eb-val.blue{{color:var(--accent-2)}}.era-block .eb-val.gold{{color:var(--gold)}}.era-block .eb-val.green{{color:var(--new-badge)}}
    .era-block .eb-sub{{font-size:.76rem;color:var(--muted);margin-top:4px}}

    .chart-container{{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:20px;box-shadow:var(--shadow);margin:16px 0}}

    footer{{margin-top:80px;padding-top:24px;border-top:1px solid var(--line);font-size:.84rem;color:var(--muted);font-family:"IBM Plex Mono",monospace;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px}}
    a{{color:var(--accent);text-decoration:none}}
    a:hover{{text-decoration:underline}}
    :focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}

    @media(max-width:768px){{
      body{{font-size:15.5px}}
      header.cover{{padding:60px 0 44px}}
      .page{{padding:0 16px 80px}}
      .era-timeline{{flex-direction:column}}
      .era-block{{border-right:none;border-bottom:1px solid var(--line)}}
      .era-block:last-child{{border-bottom:none}}
    }}
  </style>
</head>

<body>
  <button class="theme-btn" id="themeBtn" title="Cambiar tema día/noche" aria-label="Cambiar tema">🌓</button>

  <div class="page">

    <!-- COVER -->
    <header class="cover">
      <div class="col">
        <p class="eyebrow">Base de Datos · Tercera Entrega Definitiva · F1DB PostgreSQL 16 · 2026</p>
        <h1>Las eras de la Fórmula 1</h1>
        <p class="lede">Investigación analítica integral: evaluación cuantitativa del impacto de la posición de largada y del paquete tecnológico frente al desempeño individual del piloto a lo largo de 76 temporadas del Campeonato Mundial (1950–2025).</p>
        <dl class="meta">
          <div><dt>Autor</dt><dd>Rosa Kimel Connon</dd></div>
          <div><dt>Motor</dt><dd>PostgreSQL 16</dd></div>
          <div><dt>Esquema</dt><dd>formula1 (F1DB)</dd></div>
          <div><dt>Período analizado</dt><dd>1950 – 2025 (cerrado)</dd></div>
          <div><dt>Grandes Premios</dt><dd>1.149 carreras</dd></div>
          <div><dt>Consultas SQL</dt><dd>12 Clave + 1 Comp.</dd></div>
          <div><dt>Estado ejec.</dt><dd>100% Real Verificada</dd></div>
        </dl>
        <nav class="toc">
          <p class="qlabel">Índice analítico de secciones</p>
          <ol>
            <li><a href="#eda">01 · Resumen ejecutivo del Análisis Exploratorio (EDA)</a></li>
            <li><a href="#hipotesis">02 · Hipótesis, pregunta central y audiencia objetivo</a></li>
            <li><a href="#metodologia">03 · Metodología, delimitación de eras y auditoría de esquema</a></li>
            <li><a href="#bloque-grilla">04 · Eje I: Posición de largada y probabilidad de victoria (Q01 – Q03)</a></li>
            <li><a href="#bloque-competitividad">05 · Eje II: Competitividad, diversidad y concentración (Q04, Q08)</a></li>
            <li><a href="#bloque-motor">06 · Eje III: Hegemonía y rendimiento por fabricante de motor (Q05 – Q07)</a></li>
            <li><a href="#bloque-critico">07 · Eje IV: Campeones, carreras decisivas y confiabilidad mecánica (Q09 – Q11)</a></li>
            <li><a href="#bloque-piloto">08 · Eje V: El factor humano: compañeros de equipo y delta de posiciones (Q12, A1)</a></li>
            <li><a href="#sintesis-visual">09 · Síntesis visual y análisis comparativo transversal</a></li>
            <li><a href="#conclusion">10 · Conclusión general y veredicto definitivo de la hipótesis</a></li>
          </ol>
        </nav>
      </div>
    </header>

    <!-- 01 EDA RESUMEN -->
    <section id="eda">
      <div class="col stack">
        <div class="sec-head">
          <div class="rule"></div>
          <p class="eyebrow">01 · Análisis Exploratorio de Datos (EDA) — Resumen Consolidado</p>
          <h2>Fundamentos empíricos de F1DB</h2>
        </div>
        <p>Como punto de partida de la investigación (establecido en la 1ª y 2ª entrega), se realizó una auditoría estructural exhaustiva sobre el modelo relacional de <strong>F1DB</strong> desplegado en PostgreSQL 16. La base contiene 48 tablas y vistas que registran cada sesión desde el Gran Premio de Gran Bretaña de 1950 hasta la actualidad.</p>
        
        <div class="facts">
          <div class="fact"><span class="n">1.149</span><span class="l">carreras puntuables disputadas en temporadas completas (1950–2025)</span></div>
          <div class="fact"><span class="n blue">27.291</span><span class="l">participaciones individuales registradas en <code>race_result</code></span></div>
          <div class="fact"><span class="n gold">0</span><span class="l">registros huérfanos entre resultados, pilotos y carreras (integridad referencial estricta)</span></div>
          <div class="fact"><span class="n green">100%</span><span class="l">cobertura de motorización en todas las participaciones analizadas</span></div>
        </div>

        <div class="summary-grid">
          <div class="sum-card">
            <div class="sc-head"><div class="sc-num">E01</div><span class="sc-title">Volumen y granularidad</span></div>
            <p>La tabla central <code>race_result</code> alberga 27.291 filas con detalle de largada, llegada, motor, neumáticos, tiempos y estatus final.</p>
            <div class="sc-result">race_result → 27.291 participaciones analizadas</div>
          </div>
          <div class="sum-card">
            <div class="sc-head"><div class="sc-num">E02</div><span class="sc-title">Calidad de datos de grilla</span></div>
            <p>Se identificaron valores nulos en <code>grid_position_number</code> únicamente en las décadas de 1950 y 1960. Se aplica <code>IS NOT NULL</code> sistemáticamente.</p>
            <div class="sc-result">Nulos de grilla concentrados en era fundacional</div>
          </div>
          <div class="sum-card">
            <div class="sc-head"><div class="sc-num blue">E03</div><span class="sc-title">Expansión del calendario</span></div>
            <p>El campeonato pasó de 7 carreras anuales en 1950 a 24 en 2024–2025. Esto obliga a normalizar métricas mediante tasas y promedios por temporada.</p>
            <div class="sc-result blue">1950s: 8.4 carr/año → 2020s: 21.7 carr/año (+158%)</div>
          </div>
          <div class="sum-card">
            <div class="sc-head"><div class="sc-num gold">E04</div><span class="sc-title">Concentración tecnológica</span></div>
            <p>El hallazgo exploratorio central: la participación de victorias de los constructores y motoristas líderes aumentó exponencialmente en la era moderna.</p>
            <div class="sc-result gold">HHI de constructores se triplica hacia la era moderna</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 02 HIPOTESIS Y OBJETIVOS -->
    <section id="hipotesis">
      <div class="col stack">
        <div class="sec-head">
          <div class="rule gold"></div>
          <p class="eyebrow" style="color:var(--gold)">02 · Problema de Investigación</p>
          <h2>Hipótesis central y objetivos analíticos</h2>
        </div>
        <p>A partir de la exploración cuantitativa se consolidó la tensión fundacional de este estudio: si en los albores del automovilismo la pericia del piloto al volante y la volatilidad mecánica permitían revertir un sábado adverso, en la Fórmula 1 contemporánea la precisión aerodinámica, la simulación y la superioridad del tren motriz parecen cerrar casi por completo la brecha de variabilidad.</p>
        
        <div class="hyp">
          «En la Fórmula 1 moderna (post-2010), la posición de largada y el fabricante de motor son factores significativamente más determinantes del resultado final que en las primeras eras del campeonato (1950–1980), evidenciando que la competitividad se concentra cada vez más en ventajas tecnológicas y estratégicas por sobre el desempeño individual del piloto en carrera».
        </div>

        <h3>Pregunta principal de investigación</h3>
        <p class="read"><strong>¿En qué medida la posición de largada y el fabricante de motor predicen el éxito en carrera, y cómo varía ese poder predictivo entre las distintas eras de la Fórmula 1?</strong></p>

        <h3>Audiencia objetivo y valor periodístico</h3>
        <p>Esta solución está específicamente diseñada para <strong>periodistas deportivos, creadores de contenido especializado y analistas de datos del automovilismo</strong>. Permite sustentar notas de investigación, contextualizar los debates sobre reglamentaciones FIA (como el reglamento 2026 de unidades de potencia) y ofrecer métricas comprensibles pero matemáticamente impecables para superar las opiniones intuitivas.</p>

        <h3>Objetivos específicos estructurados</h3>
        <ol class="obj">
          <li><strong>Medir el peso predictivo de la grilla de partida:</strong> cuantificar la probabilidad real de victoria y podio según franja de largada y su evolución temporal (Q01, Q02, Q03).</li>
          <li><strong>Evaluar la concentración del poder constructivo:</strong> calcular el Índice Herfindahl-Hirschman (HHI) y el promedio de ganadores distintos por año (Q04, Q08).</li>
          <li><strong>Aislar la influencia del fabricante de motor:</strong> cuantificar el share de victorias por motorista y comparar su rendimiento relativo controlando por posición de salida (Q05, Q06, Q07).</li>
          <li><strong>Analizar las instancias críticas:</strong> comprobar si los campeones y las carreras definitorias exhiben una dependencia aún mayor de la pole position (Q09, Q10).</li>
          <li><strong>Auditar la confiabilidad mecánica como variable de confusión:</strong> diferenciar si la mayor previsibilidad moderna responde al chasis/motor o a la virtual extinción de fallas mecánicas fortuitas (Q11).</li>
          <li><strong>Controlar por el talento individual:</strong> contrastar compañeros de equipo con auto y motor idénticos y computar el delta de posiciones ganadas/perdidas (Q12, A1).</li>
        </ol>
      </div>
    </section>

    <!-- 03 METODOLOGÍA Y ESQUEMA -->
    <section id="metodologia">
      <div class="col stack">
        <div class="sec-head">
          <div class="rule blue"></div>
          <p class="eyebrow" style="color:var(--accent-2)">03 · Metodología y Auditoría de Datos</p>
          <h2>Delimitación temporal y corrección de esquema</h2>
        </div>
        <p>Para asegurar una comparabilidad estadística rigurosa, se adoptaron las siguientes definiciones metodológicas:</p>
        
        <h3>1. Delimitación temporal en tres eras comparables</h3>
        <p>Siguiendo las pautas de diseño científico y evitando mezclar temporadas incompletas, se analizan las 76 temporadas concluidas (1950–2025):</p>
        <ul>
          <li><strong>Era Clásica (1950–1980):</strong> 31 temporadas fundacionales, caracterizadas por chasis tubulares, motores atmosféricos/Cosworth DFV, baja aerodinámica y alta tasa de roturas.</li>
          <li><strong>Era Intermedia (1981–2010):</strong> 30 temporadas que abarcan la era Turbo, los motores V10 y V8 atmosféricos, y la profesionalización del diseño por telemetría.</li>
          <li><strong>Era Moderna (2011–2025):</strong> 15 temporadas completas dominadas por unidades de potencia de alta eficiencia, túnel de viento, simulación CFD y congelamiento de desarrollo. <em>(Se excluye la temporada 2026 por estar en disputa, evitando sesgos por tamaño muestral incompleto).</em></li>
        </ul>

        <h3>2. Auditoría y correcciones sobre el esquema relacional F1DB</h3>
        <p>A diferencia de los borradores preliminares que asumían nombres hipotéticos, en esta entrega se corrigió y verificó cada consulta contra las tablas físicas reales:</p>
        <ul>
          <li><strong>Claves de resultado:</strong> la tabla física es <code>formula1.race_result</code>; las columnas canónicas son <code>position_number</code> (posición de llegada), <code>grid_position_number</code> (posición de grilla) y <code>positions_gained</code>.</li>
          <li><strong>Claves de motorización:</strong> el campo en <code>race_result</code> es <code>engine_manufacturer_id</code>, enlazado con <code>formula1.engine_manufacturer</code> (campo <code>name</code>).</li>
          <li><strong>Identificación de carreras decisivas:</strong> se utiliza la columna booleana nativa <code>drivers_championship_decider</code> de la tabla <code>formula1.race</code>.</li>
          <li><strong>Clasificación de motivos de retiro:</strong> la columna <code>reason_retired</code> registra motivos textuales estandarizados. Se clasificaron como <em>Averías Mecánicas</em> exclusivamente las fallas de motor, caja de cambios, transmisión, suspensión, frenos, hidráulica, eléctrica, etc., separándolas tajantemente de los <em>Accidentes y colisiones</em>.</li>
        </ul>
      </div>
    </section>

    <!-- BLOQUE 1: GRILLA -->
    <section id="bloque-grilla">
      <div class="col">
        <div class="sec-head">
          <div class="rule"></div>
          <p class="eyebrow">04 · Eje Analítico I</p>
          <h2>Posición de largada y probabilidad de victoria</h2>
        </div>
        <p style="margin-bottom:28px">Evaluamos el primer pilar de la hipótesis: cómo la posición en la grilla de partida condiciona el destino de la carrera.</p>
      </div>

      <div class="wide">
        <!-- Q01 -->
        <article class="query" id="q01">
          <div class="qh">
            <span class="qid">Q01</span>
            <h3>¿Desde qué posiciones de la grilla se obtuvieron las victorias históricas?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y relación con la hipótesis</p>
              <p>Describe la distribución histórica agregada de las 1.149 victorias entre 1950 y 2025 según la posición de partida. Permite medir el grado de concentración inicial en la primera fila antes de pasar al cálculo probabilístico condicional.</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Funciona como la línea de base descriptiva de toda la investigación. Si las victorias estuvieran distribuidas uniformemente a lo largo de las primeras 10 posiciones, la grilla tendría un rol secundario. Si se concentran casi en su totalidad en P1–P3, el sábado define el domingo.</p>
            </div>
            <div>
              <p class="qlabel">Tablas y relaciones SQL</p>
              <p><code>race_result (rr)</code> unida con <code>race (r)</code> mediante <code>rr.race_id = r.id</code>. Se filtra por <code>rr.position_number = 1</code> y <code>rr.grid_position_number IS NOT NULL</code>. Se aplica la función de ventana <code>SUM(COUNT(*)) OVER ()</code> para computar el porcentaje exacto sobre el total de victorias con grilla registrada.</p>
            </div>
            <pre><code class="sql">-- Q01: Distribución histórica de victorias por posición de largada (1950-2025)
SELECT
    rr.grid_position_number AS grilla,
    COUNT(*) AS victorias,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_victorias
FROM race_result rr
JOIN race r ON rr.race_id = r.id
WHERE rr.position_number = 1
  AND rr.grid_position_number IS NOT NULL
  AND r.year <= 2025
GROUP BY rr.grid_position_number
ORDER BY rr.grid_position_number
LIMIT 10;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16</p>
            {tf.table_q01()}
            <p class="read"><strong>Interpretación cuantitativa:</strong> A lo largo de la historia, la <strong>Pole Position (P1)</strong> acapara 497 victorias, representando el <strong>43.26%</strong> del total. La segunda posición aporta el <strong>23.67%</strong> (272 victorias) y la tercera el <strong>12.01%</strong> (138 victorias). En conjunto, <strong>el 78.94% de todas las carreras de F1 fueron ganadas por pilotos que largaron entre los tres primeros</strong>. Ganar desde el puesto 10 o más atrás es una anomalía estadística (menos del 2% combinado).</p>
            <p class="read blue"><strong>Contribución al argumento:</strong> Respalda de forma contundente la premisa de que la grilla es el factor determinante primario. No obstante, al ser una métrica global no condicionada por el total de participaciones, hace indispensable avanzar hacia Q02 para calcular la tasa de éxito real por era.</p>
            <p class="read gold"><strong>Limitaciones metodológicas:</strong> Mide la distribución de los ganadores, pero no la probabilidad condicional de ganar dado que se parte en una posición (denominador de largadas).</p>
          </div>
        </article>

        <!-- Q02 -->
        <article class="query" id="q02">
          <div class="qh">
            <span class="qid green">Q02</span>
            <h3>¿Qué probabilidad de ganar y hacer podio tiene un piloto según su posición de grilla y la era?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y relación con la hipótesis</p>
              <p>Calcula la probabilidad real (tasa de conversión sobre participaciones válidas) de conseguir una victoria y un podio desglosada por franjas de grilla homogéneas (P1, P2–P3, P4–P6, P7–P10, P11+) a través de las tres eras del campeonato.</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Es la prueba cuantitativa central de la hipótesis. Al dividir las victorias y podios sobre el <strong>universo total de largadas efectivas</strong> en cada franja, elimina el sesgo de calendario y permite comparar directamente la dificultad de ganar desde atrás entre 1950 y 2025.</p>
            </div>
            <div>
              <p class="qlabel">Tablas y relaciones SQL</p>
              <p>Unión entre <code>race_result (rr)</code> y <code>race (r)</code> categorizando temporalmente mediante <code>CASE WHEN</code> y agrupando por franjas de grilla con <code>FILTER (WHERE position_number = 1)</code> y <code>FILTER (WHERE position_number <= 3)</code>.</p>
            </div>
            <pre><code class="sql">-- Q02: Probabilidad condicional de victoria y podio por franja de grilla y por era
WITH eras AS (
  SELECT id AS race_id,
    CASE
      WHEN year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era
  FROM race
  WHERE year <= 2025
),
clasif AS (
  SELECT
    e.era,
    CASE
      WHEN rr.grid_position_number = 1 THEN 'P1 (Pole)'
      WHEN rr.grid_position_number BETWEEN 2 AND 3 THEN 'P2–P3'
      WHEN rr.grid_position_number BETWEEN 4 AND 6 THEN 'P4–P6'
      WHEN rr.grid_position_number BETWEEN 7 AND 10 THEN 'P7–P10'
      ELSE 'P11+'
    END AS franja,
    CASE
      WHEN rr.grid_position_number = 1 THEN 1
      WHEN rr.grid_position_number BETWEEN 2 AND 3 THEN 2
      WHEN rr.grid_position_number BETWEEN 4 AND 6 THEN 3
      WHEN rr.grid_position_number BETWEEN 7 AND 10 THEN 4
      ELSE 5
    END AS orden_franja,
    rr.position_number
  FROM race_result rr
  JOIN eras e ON rr.race_id = e.race_id
  WHERE rr.grid_position_number IS NOT NULL
)
SELECT
  era,
  franja,
  COUNT(*) AS participaciones,
  COUNT(*) FILTER (WHERE position_number = 1) AS victorias,
  ROUND(100.0 * COUNT(*) FILTER (WHERE position_number = 1) / COUNT(*), 2) AS pct_victoria,
  COUNT(*) FILTER (WHERE position_number <= 3) AS podios,
  ROUND(100.0 * COUNT(*) FILTER (WHERE position_number <= 3) / COUNT(*), 2) AS pct_podio
FROM clasif
GROUP BY era, franja, orden_franja
ORDER BY era, orden_franja;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16</p>
            {tf.table_q02()}
            <div>
              <p class="qlabel">Comparación gráfica de la tasa de victoria desde P1 (Pole) por era</p>
              <div class="pbar-group">
                <div class="pbar-item">
                  <div class="pbar-label"><strong>Era Clásica (1950–1980)</strong><span>37.13% victoria · 50.58% podio</span></div>
                  <div class="pbar-track"><div class="pbar-fill" style="width:37.13%"></div></div>
                </div>
                <div class="pbar-item">
                  <div class="pbar-label"><strong>Era Intermedia (1981–2010)</strong><span>41.53% victoria · 63.51% podio</span></div>
                  <div class="pbar-track"><div class="pbar-fill blue" style="width:41.53%"></div></div>
                </div>
                <div class="pbar-item">
                  <div class="pbar-label"><strong>Era Moderna (2011–2025)</strong><span>53.07% victoria · 81.23% podio</span></div>
                  <div class="pbar-track"><div class="pbar-fill green" style="width:53.07%"></div></div>
                </div>
              </div>
            </div>
            <p class="read green"><strong>Interpretación cuantitativa:</strong> La tasa de conversión de Pole en victoria trepó del <strong>37.13% en la era clásica al 53.07% en la era moderna (+15.94 puntos porcentuales, un incremento relativo del +42.9%)</strong>. Aún más elocuente es la tasa de podio para el poleman: en la era moderna alcanza un abrumador <strong>81.23%</strong> (en 8 de cada 10 carreras quien larga primero sube al podio). Simultáneamente, la posibilidad de ganar largando en P4–P6 se redujo a más de la mitad (del 5.26% clásico al 2.47% moderno), y desde P11+ es virtualmente nula (apenas 4 victorias en 3.215 largadas: 0.12%).</p>
            <p class="read"><strong>Contribución al argumento:</strong> Valida directamente la primera parte de la hipótesis: la posición de largada se volvió significativamente más predictiva del resultado final en la Fórmula 1 contemporánea.</p>
            <p class="read gold"><strong>Limitaciones:</strong> Excluye largadas sin registro en los primeros años de los 50s. No discrimina si la pole se obtuvo por ventaja mecánica pura o lluvia circunstancial en clasificación.</p>
          </div>
        </article>

        <!-- Q03 -->
        <article class="query" id="q03">
          <div class="qh">
            <span class="qid">Q03</span>
            <h3>¿Cómo evolucionó la tasa de conversión de pole a victoria década a década?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y relación con la hipótesis</p>
              <p>Rastrea la serie temporal de conversión pole → victoria año a año y agregada por décadas completas desde 1950 hasta 2025 para comprobar si la tendencia es lineal y monótona o presenta quiebres estructurales.</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Evita conclusiones simplistas basadas en dos puntos extremos. El análisis longitudinal revela momentos históricos clave, como la caída de conversión en los años 80 por fallas mecánicas de los motores turbo, y la posterior consolidación de la superioridad de la pole a partir de los años 2000.</p>
            </div>
            <div>
              <p class="qlabel">Tablas y relaciones SQL</p>
              <p>Agrupación por <code>(year / 10) * 10 AS decada</code> sobre <code>race_result</code> y <code>race</code> filtrando por <code>grid_position_number = 1</code>.</p>
            </div>
            <pre><code class="sql">-- Q03: Tasa de conversión de Pole Position a Victoria agrupada por década (1950-2025)
WITH poles_year AS (
  SELECT
    r.year,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1) AS poles_largaron,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.position_number = 1) AS poles_ganaron
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE rr.grid_position_number IS NOT NULL AND r.year <= 2025
  GROUP BY r.year
)
SELECT
  (year / 10) * 10 AS decada,
  SUM(poles_largaron) AS total_poles,
  SUM(poles_ganaron) AS victorias_desde_pole,
  ROUND(100.0 * SUM(poles_ganaron) / NULLIF(SUM(poles_largaron), 0), 2) AS tasa_conversion_pct
FROM poles_year
GROUP BY (year / 10) * 10
ORDER BY decada;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16</p>
            {tf.table_q03()}
            <div class="era-timeline">
              <div class="era-block"><div class="eb-label">1970s</div><div class="eb-val">36.8%</div><div class="eb-sub">era Cosworth DFV</div></div>
              <div class="era-block"><div class="eb-label">1980s</div><div class="eb-val blue">28.2%</div><div class="eb-sub">roturas turbo V6</div></div>
              <div class="era-block"><div class="eb-label">2000s</div><div class="eb-val gold">50.0%</div><div class="eb-sub">era Schumacher/Ferrari</div></div>
              <div class="era-block"><div class="eb-label">2020s</div><div class="eb-val green">55.4%</div><div class="eb-sub">era efecto suelo/híbrida</div></div>
            </div>
            <p class="read"><strong>Interpretación cuantitativa:</strong> La tasa de conversión no fue monotónica: en la década de 1980 tocó un piso histórico de <strong>28.21%</strong> debido a la explosiva falta de confiabilidad de los primeros motores turbo (los autos salían en punta pero rompían motor con frecuencia). Sin embargo, a partir de la década de 2000 se afianza en el <strong>50.00%</strong>, alcanzando en la década de 2020 su récord histórico absoluto con <strong>55.38%</strong>.</p>
            <p class="read blue"><strong>Contribución al argumento:</strong> Demuestra que la relación grilla-victoria está profundamente mediada por la confiabilidad técnica. Cuando la tecnología se vuelve hiperconfiable (post-2010), la ventaja de largada se cristaliza como nunca antes.</p>
            <p class="read gold"><strong>Limitaciones:</strong> Década 2020s calculada sobre 6 temporadas (2020–2025, 130 GPs), representativa pero de menor tamaño que décadas completas de 10 años.</p>
          </div>
        </article>
      </div>
    </section>

    <!-- BLOQUE 2: COMPETITIVIDAD Y CONCENTRACIÓN -->
    <section id="bloque-competitividad">
      <div class="col">
        <div class="sec-head">
          <div class="rule gold"></div>
          <p class="eyebrow" style="color:var(--gold)">05 · Eje Analítico II</p>
          <h2>Competitividad y concentración de victorias</h2>
        </div>
        <p style="margin-bottom:28px">Analizamos si la menor variabilidad de ganadores responde a una cartelización de los triunfos en un puñado exclusivo de constructores.</p>
      </div>

      <div class="wide">
        <!-- Q04 -->
        <article class="query" id="q04">
          <div class="qh">
            <span class="qid gold">Q04</span>
            <h3>¿Qué tan concentradas están las victorias por constructor en cada era? (Índice HHI)</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y relación con la hipótesis</p>
              <p>Mide la concentración de mercado de las victorias empleando el Índice de Herfindahl-Hirschman (HHI), estándar econométrico de concentración económica definido como la suma de los cuadrados de las cuotas de mercado porcentuales ($HHI = \sum s_i^2$).</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Permite pasar del mero conteo de victorias a un indicador riguroso y sintético de dispersión competitiva. Una F1 abierta arroja HHI < 1.500; un mercado altamente concentrado supera los 2.500 puntos.</p>
            </div>
            <div>
              <p class="qlabel">Tablas y relaciones SQL</p>
              <p>Agrupación de victorias por <code>constructor.name</code> y <code>era</code>, uniendo <code>race_result</code>, <code>race</code> y <code>constructor</code>. Cálculo de cuota de mercado relativa sobre el total de la era y suma cuadrática.</p>
            </div>
            <pre><code class="sql">-- Q04: Índice Herfindahl-Hirschman (HHI) de concentración de victorias por constructor
WITH constructor_wins AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    c.name AS constructor_name,
    COUNT(*) AS victorias
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN constructor c ON rr.constructor_id = c.id
  WHERE rr.position_number = 1 AND r.year <= 2025
  GROUP BY era, c.name
),
totals AS (
  SELECT era, SUM(victorias) AS total_victorias
  FROM constructor_wins
  GROUP BY era
),
shares AS (
  SELECT
    cw.era,
    cw.constructor_name,
    cw.victorias,
    t.total_victorias,
    ROUND(100.0 * cw.victorias / t.total_victorias, 2) AS share_pct
  FROM constructor_wins cw
  JOIN totals t ON cw.era = t.era
)
SELECT
  era,
  COUNT(DISTINCT constructor_name) AS constructores_ganadores,
  MAX(total_victorias) AS total_victorias,
  ROUND(MAX(share_pct), 2) AS max_share_lider,
  ROUND(SUM(POWER(share_pct, 2))::numeric, 1) AS hhi
FROM shares
GROUP BY era
ORDER BY era;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16</p>
            {tf.table_q04()}
            <p class="read gold"><strong>Interpretación cuantitativa:</strong> El índice HHI casi se <strong>triplica entre la era clásica (1.196,3) y la era moderna (3.159,4)</strong>. En la era clásica ganaron 27 marcas distintas y el líder (Ferrari) apenas acaparó el 23.19% de los triunfos. En cambio, en la era moderna <strong>apenas 9 constructores lograron ganar un GP</strong>, y el equipo dominante concentró el <strong>39.35% de todas las carreras disputadas</strong>. Un HHI de 3.159 califica formalmente como monopolio/oligopolio rígido.</p>
            <p class="read"><strong>Contribución al argumento:</strong> Confirma que la competitividad de victorias se redujo drásticamente, consolidando la superioridad de los paquetes de ingeniería líderes.</p>
            <p class="read gold"><strong>Limitaciones:</strong> El HHI mide concentración de resultados por chasis, no el efecto aislado del motor ni del túnel de viento.</p>
          </div>
        </article>

        <!-- Q08 -->
        <article class="query" id="q08">
          <div class="qh">
            <span class="qid">Q08</span>
            <h3>¿Hay menos pilotos ganadores distintos por temporada en las eras modernas?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y relación con la hipótesis</p>
              <p>Examina si el campeonato ofrece menor rotación de triunfadores normalizando por el tamaño del calendario anual (Ratio de Apertura = ganadores distintos / carreras por año).</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Corrige el error de la primera entrega que comparaba conteos brutos sin contemplar que una era tenía 31 años y otra 15. Calcular el promedio de ganadores por temporada y contrastarlo contra las carreras disputadas arroja la verdadera tasa de apertura.</p>
            </div>
            <div>
              <p class="qlabel">Tablas y relaciones SQL</p>
              <p>CTE que computa <code>COUNT(DISTINCT driver_id)</code> por año, agregando luego por era con métricas de dispersión (mínimo, máximo, promedio y ratio).</p>
            </div>
            <pre><code class="sql">-- Q08: Promedio de pilotos ganadores distintos por temporada y ratio de apertura competitiva
WITH ganadores_año AS (
  SELECT
    r.year,
    COUNT(DISTINCT rr.driver_id) AS pilotos_ganadores,
    COUNT(*) AS total_carreras
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE rr.position_number = 1 AND r.year <= 2025
  GROUP BY r.year
),
por_era AS (
  SELECT
    CASE
      WHEN year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    COUNT(*) AS temporadas,
    ROUND(AVG(pilotos_ganadores), 2) AS prom_ganadores_temporada,
    MIN(pilotos_ganadores) AS min_ganadores,
    MAX(pilotos_ganadores) AS max_ganadores,
    ROUND(AVG(total_carreras), 1) AS prom_carreras_temporada,
    ROUND(AVG(pilotos_ganadores)::numeric / AVG(total_carreras)::numeric, 3) AS ratio_apertura
  FROM ganadores_año
  GROUP BY era
  ORDER BY era
)
SELECT * FROM por_era;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16</p>
            {tf.table_q08()}
            <p class="read"><strong>Interpretación cuantitativa:</strong> Aunque el promedio absoluto de ganadores por año cayó levemente de 5.45 a 4.87, la verdadera revelación surge al contrastarlo con el calendario: en la era clásica había 5.45 ganadores en apenas 11.1 carreras (<strong>Ratio de Apertura = 0.490</strong>, prácticamente 1 ganador distinto cada dos carreras). En la era moderna, con 20.7 carreras anuales, solo ganan 4.87 pilotos por temporada (<strong>Ratio de Apertura = 0.235</strong>). <strong>La probabilidad de que una carrera tenga un ganador no habitual se redujo en más del 50%</strong>.</p>
            <p class="read blue"><strong>Contribución al argumento:</strong> Demuestra que la aparente paridad es una ilusión óptica causada por la mayor cantidad de carreras: el acceso a la victoria se ha estrechado notablemente.</p>
            <p class="read gold"><strong>Limitaciones:</strong> No refleja márgenes de tiempo por vuelta (gaps de calificación ni distancia entre el 1º y el 2º en meta).</p>
          </div>
        </article>
      </div>
    </section>

    <!-- BLOQUE 3: FABRICANTE DE MOTOR -->
    <section id="bloque-motor">
      <div class="col">
        <div class="sec-head">
          <div class="rule blue"></div>
          <p class="eyebrow" style="color:var(--accent-2)">06 · Eje Analítico III</p>
          <h2>Hegemonía y rendimiento por fabricante de motor</h2>
        </div>
        <p style="margin-bottom:28px">Abordamos el segundo factor clave de la hipótesis: el peso de la motorización y su ventaja técnica en pista.</p>
      </div>

      <div class="wide">
        <!-- Q05 -->
        <article class="query" id="q05">
          <div class="qh">
            <span class="qid blue">Q05</span>
            <h3>¿Qué porcentaje de las victorias de cada era corresponde a cada fabricante de motor?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y relación con la hipótesis</p>
              <p>Cuantifica el porcentaje de carreras ganadas por cada fabricante de motor en cada era histórica, identificando los monopolios de unidad de potencia.</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Permite responder directamente a la hipótesis evaluando si la concentración en un solo motorista alcanzó niveles sin precedentes en la era contemporánea.</p>
            </div>
            <div>
              <p class="qlabel">Tablas y relaciones SQL</p>
              <p>Unión de <code>race_result</code> con <code>engine_manufacturer (em)</code> mediante <code>rr.engine_manufacturer_id = em.id</code> y con <code>race (r)</code>. Ranking con <code>ROW_NUMBER()</code> ordenado por victorias descendentes.</p>
            </div>
            <pre><code class="sql">-- Q05: Cuota de victorias por fabricante de motor en cada era (Top 5)
WITH engine_wins AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    em.name AS motor,
    COUNT(*) AS victorias
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  WHERE rr.position_number = 1 AND r.year <= 2025
  GROUP BY era, em.name
),
era_tot AS (
  SELECT era, SUM(victorias) AS total_era
  FROM engine_wins
  GROUP BY era
),
ranked AS (
  SELECT
    ew.era,
    ew.motor,
    ew.victorias,
    ROUND(100.0 * ew.victorias / et.total_era, 2) AS pct_era,
    ROW_NUMBER() OVER (PARTITION BY ew.era ORDER BY ew.victorias DESC) AS rk
  FROM engine_wins ew
  JOIN era_tot et ON ew.era = et.era
)
SELECT era, rk, motor, victorias, pct_era
FROM ranked
WHERE rk <= 5
ORDER BY era, rk;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16</p>
            {tf.table_q05()}
            <p class="read blue"><strong>Interpretación cuantitativa:</strong> En la era clásica Ford dominó con 136 triunfos (39.42%) gracias a la proliferación del motor cliente Cosworth DFV disponible para múltiples equipos independientes (Lotus, Tyrrell, McLaren). En la era intermedia existió una puja equilibrada entre Ferrari (27.57%), Renault (25.35%), Mercedes (14.69%) y Honda (14.08%). Pero en la era moderna, <strong>Mercedes pulverizó todos los registros históricos al ganar 156 de 310 carreras: un 50.32% de todas las victorias de la era</strong>. Más de la mitad de los Grandes Premios modernos fueron conquistados por autos propulsados por la marca de la estrella.</p>
            <p class="read green"><strong>Contribución al argumento:</strong> Respalda de forma categórica que la ventaja de motorización alcanzó su cenit histórico tras la introducción del reglamento V6 turbo-híbrido en 2014.</p>
            <p class="read gold"><strong>Limitaciones:</strong> Cuenta victorias totales de la marca motriz, sin diferenciar autos oficiales (Mercedes AMG) de clientes (Williams, McLaren, Force India).</p>
          </div>
        </article>

        <!-- Q06 -->
        <article class="query" id="q06">
          <div class="qh">
            <span class="qid blue">Q06</span>
            <h3>¿Qué tasa de éxito tiene cada fabricante de motor por participación efectiva?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y relación con la hipótesis</p>
              <p>Mide la eficiencia motriz comparando victorias y podios sobre el total de participaciones efectivas en carrera, aplicando un filtro de significancia estadística (mínimo 50 participaciones en la era).</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Complementa a Q05. Un motorista cliente con 4 autos en grilla acumula muchas participaciones; esta consulta mide la efectividad relativa de cada motor puesto en pista.</p>
            </div>
            <div>
              <p class="qlabel">Tablas y relaciones SQL</p>
              <p>Agrupación por <code>em.name</code> y <code>era</code> con cláusula <code>HAVING COUNT(*) >= 50</code>, computando ratios porcentuales.</p>
            </div>
            <pre><code class="sql">-- Q06: Tasa de victoria y podio por participación de fabricante de motor (umbral >= 50 GPs)
WITH base AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    em.name AS motor,
    COUNT(*) AS participaciones,
    COUNT(*) FILTER (WHERE rr.position_number = 1) AS victorias,
    COUNT(*) FILTER (WHERE rr.position_number <= 3) AS podios
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  WHERE r.year <= 2025
  GROUP BY era, em.name
),
ranked AS (
  SELECT
    era, motor, participaciones, victorias,
    ROUND(100.0 * victorias / participaciones, 2) AS pct_victoria,
    podios,
    ROUND(100.0 * podios / participaciones, 2) AS pct_podio,
    ROW_NUMBER() OVER (PARTITION BY era ORDER BY victorias DESC, participaciones DESC) as rk
  FROM base
  WHERE participaciones >= 50
)
SELECT era, rk, motor, participaciones, victorias, pct_victoria, podios, pct_podio
FROM ranked
WHERE rk <= 5
ORDER BY era, rk;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16</p>
            {tf.table_q06()}
            <p class="read"><strong>Interpretación cuantitativa:</strong> En la era clásica, fabricantes con operaciones de fábrica muy selectivas lograron ratios altos (Vanwall 14.08%, Ferrari 9.00%), mientras que Ford registró un 3.80% debido a que suministraba a gran parte de la grilla de atrás. En la era moderna, Mercedes logró 156 victorias en 2.092 participaciones (<strong>7.46% de tasa de victoria global y 20.32% de tasa de podio</strong> a pesar de motorizar hasta a 4 escuderías a la vez), seguido por los proyectos a medida de Red Bull (Honda RBPT con 38 victorias en 267 participaciones: <strong>14.23% de efectividad de victoria</strong>).</p>
            <p class="read blue"><strong>Contribución al argumento:</strong> Demuestra que la efectividad no es fruto de saturación de grilla, sino de un rendimiento superior de las arquitecturas ganadoras.</p>
            <p class="read gold"><strong>Limitaciones:</strong> Escuderías clientes de menor presupuesto rebajan el ratio promedio de fabricantes que suministran a varios equipos.</p>
          </div>
        </article>

        <!-- Q07 -->
        <article class="query" id="q07">
          <div class="qh">
            <span class="qid green">Q07</span>
            <h3>¿La ventaja del motor persiste al comparar posiciones de largada similares?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y relación con la hipótesis</p>
              <p>Controla el efecto de la grilla analizando el rendimiento de cada motor dentro de la misma franja de partida (P1, P2–P3 y P4+) durante la era moderna (2011–2025).</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Es uno de los análisis econométricos y causales más reveladores: permite responder si un motorista gana simplemente porque clasifica adelante el sábado, o si su unidad de potencia otorga una ventaja adicional de ritmo y fiabilidad en carrera.</p>
            </div>
            <div>
              <p class="qlabel">Tablas y relaciones SQL</p>
              <p>Subconsulta condicionada a la era moderna (2011–2025) cruzando fabricante de motor con franjas de largada categóricas con umbral mínimo de 15 participaciones.</p>
            </div>
            <pre><code class="sql">-- Q07: Tasa de victoria de motores controlando por franja de grilla en Era Moderna (2011-2025)
WITH base AS (
  SELECT
    em.name AS motor,
    CASE
      WHEN rr.grid_position_number = 1 THEN 'P1 (Pole)'
      WHEN rr.grid_position_number BETWEEN 2 AND 3 THEN 'P2-P3'
      ELSE 'P4+'
    END AS franja_grilla,
    CASE
      WHEN rr.grid_position_number = 1 THEN 1
      WHEN rr.grid_position_number BETWEEN 2 AND 3 THEN 2
      ELSE 3
    END AS orden_franja,
    COUNT(*) AS participaciones,
    COUNT(*) FILTER (WHERE rr.position_number = 1) AS victorias,
    COUNT(*) FILTER (WHERE rr.position_number <= 3) AS podios
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  WHERE r.year BETWEEN 2011 AND 2025 AND rr.grid_position_number IS NOT NULL
  GROUP BY em.name, franja_grilla, orden_franja
)
SELECT
  franja_grilla,
  motor,
  participaciones,
  victorias,
  ROUND(100.0 * victorias / participaciones, 2) AS pct_victoria,
  podios,
  ROUND(100.0 * podios / participaciones, 2) AS pct_podio
FROM base
WHERE participaciones >= 15
ORDER BY orden_franja, pct_victoria DESC;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16</p>
            {tf.table_q07()}
            <p class="read green"><strong>Interpretación cuantitativa:</strong> Los datos revelan un patrón sumamente enriquecedor que matiza y profundiza la hipótesis:
              <br>• <strong>Desde la Pole (P1):</strong> Honda RBPT exhibe un demoledor <strong>76.67% de conversión</strong> (23 victorias en 30 poles) y Mercedes un <strong>53.57%</strong> (90 victorias en 168 poles). En contraposición radical, <strong>Ferrari solo convirtió el 27.08% de sus poles</strong> (13 victorias en 48 poles). Esto prueba que un motor puede ser veloz a una vuelta el sábado, pero si degrada neumáticos o carece de eficiencia térmica en tandas largas, el domingo pierde la carrera frente al paquete integral superior.
              <br>• <strong>Desde P4 en adelante:</strong> Para todos los fabricantes la probabilidad colapsa por debajo del 1% (Mercedes 0.55%, Ferrari 0.30%, Cosworth 0.00%). Sin salir entre los tres primeros, ni el mejor motor de la parrilla puede remontar de manera consistente.</p>
            <p class="read"><strong>Contribución al argumento:</strong> Demuestra que el motor influye de dos formas distintas: define la capacidad de copar la primera fila el sábado, pero además exige ritmo de carrera sostenido para no sucumbir ante el líder.</p>
            <p class="read gold"><strong>Limitaciones:</strong> En la F1 moderna el chasis, la suspensión y la aerodinámica están íntimamente acoplados al motor; no es posible aislar al 100% el motor del chasis con datos de base de datos sin telemetría de potencia pura (kW).</p>
          </div>
        </article>
      </div>
    </section>

    <!-- BLOQUE 4: CAMPEONES, DECISIVAS Y CONFIABILIDAD -->
    <section id="bloque-critico">
      <div class="col">
        <div class="sec-head">
          <div class="rule"></div>
          <p class="eyebrow">07 · Eje Analítico IV</p>
          <h2>Campeones, carreras decisivas y confiabilidad mecánica</h2>
        </div>
        <p style="margin-bottom:28px">Exploramos cómo influye la grilla en la consagración de los campeones mundiales y el papel silencioso de la confiabilidad mecánica.</p>
      </div>

      <div class="wide">
        <!-- Q09 -->
        <article class="query" id="q09">
          <div class="qh">
            <span class="qid">Q09</span>
            <h3>¿Qué porcentaje de las victorias de los campeones se consiguió largando desde P1?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y relación con la hipótesis</p>
              <p>Determina la proporción de triunfos obtenidos desde la Pole Position por los campeones del mundo durante la temporada exacta en la que se coronaron.</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Corrige la fórmula errónea de la entrega preliminar (que dividía poles totales por victorias). Esta versión enlaza al piloto consagrado como campeón en <code>season_driver_standing</code> con sus resultados individuales de ese mismo año.</p>
            </div>
            <div>
              <p class="qlabel">Tablas y relaciones SQL</p>
              <p><code>season_driver_standing</code> (filtrando por <code>championship_won = TRUE</code>) unida a <code>race</code> y <code>race_result</code> por <code>driver_id</code> y <code>year</code>.</p>
            </div>
            <pre><code class="sql">-- Q09: Porcentaje de victorias desde Pole de los campeones del mundo en su año de título
WITH campeon_año AS (
  SELECT year, driver_id
  FROM season_driver_standing
  WHERE championship_won = TRUE AND year <= 2025
),
victorias_campeon AS (
  SELECT
    c.year,
    c.driver_id,
    COUNT(*) AS vic_campeon,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1) AS vic_desde_pole
  FROM campeon_año c
  JOIN race r ON r.year = c.year
  JOIN race_result rr ON rr.race_id = r.id AND rr.driver_id = c.driver_id
  WHERE rr.position_number = 1
  GROUP BY c.year, c.driver_id
)
SELECT
  CASE
    WHEN year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
    WHEN year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
    ELSE '3. Moderna (2011-2025)'
  END AS era,
  COUNT(*) AS temporadas,
  SUM(vic_campeon) AS total_victorias_campeones,
  SUM(vic_desde_pole) AS victorias_desde_pole,
  ROUND(100.0 * SUM(vic_desde_pole) / NULLIF(SUM(vic_campeon), 0), 2) AS pct_desde_pole
FROM victorias_campeon
GROUP BY era
ORDER BY era;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16</p>
            {tf.table_q09()}
            <p class="read"><strong>Interpretación cuantitativa:</strong> En la era clásica, los campeones mundiales consiguieron el <strong>53.08%</strong> de sus victorias largando desde la pole (69 de 130). En la era moderna, esa cifra asciende al <strong>62.11%</strong> (100 de 161 victorias). El campeón moderno no solo domina el certamen: <strong>edifica prácticamente dos tercios de sus victorias dominando la clasificación del sábado</strong> y manteniendo el liderazgo sin alternancia.</p>
            <p class="read blue"><strong>Contribución al argumento:</strong> Demuestra que la coronación de un título mundial en la F1 moderna está indisolublemente atada a la supremacía en clasificación.</p>
            <p class="read gold"><strong>Limitaciones:</strong> En temporadas muy tempranas el sistema de descarte de puntos (mejores 4 o 5 resultados) influía en la estrategia del campeón en las últimas fechas.</p>
          </div>
        </article>

        <!-- Q10 -->
        <article class="query" id="q10">
          <div class="qh">
            <span class="qid">Q10</span>
            <h3>¿La ventaja de la pole es mayor en las carreras que deciden el campeonato?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y relación con la hipótesis</p>
              <p>Compara la tasa de conversión pole → victoria entre carreras que definieron matemáticamente el título mundial (<code>drivers_championship_decider = TRUE</code>) y Grandes Premios regulares.</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Verifica si en las instancias de máxima presión deportiva el peso de la posición de largada se amplifica o si la tensión estratégica altera el orden de salida.</p>
            </div>
            <div>
              <p class="qlabel">Tablas y relaciones SQL</p>
              <p>Cruce de <code>race_result</code> con el indicador booleano nativo <code>r.drivers_championship_decider</code> de la tabla <code>race</code>.</p>
            </div>
            <pre><code class="sql">-- Q10: Tasa de conversión de pole en carreras decisivas de campeonato vs regulares
WITH clasif AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    r.drivers_championship_decider AS es_decisiva,
    rr.grid_position_number,
    rr.position_number
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE r.year <= 2025 AND rr.grid_position_number = 1 AND rr.position_number IS NOT NULL
)
SELECT
  era,
  CASE WHEN es_decisiva THEN 'Carrera Decisiva' ELSE 'Carrera Regular' END AS tipo_carrera,
  COUNT(*) AS total_poles,
  COUNT(*) FILTER (WHERE position_number = 1) AS victorias_desde_pole,
  ROUND(100.0 * COUNT(*) FILTER (WHERE position_number = 1) / COUNT(*), 2) AS tasa_conversion_pct
FROM clasif
GROUP BY era, es_decisiva
ORDER BY era, es_decisiva DESC;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16</p>
            {tf.table_q10()}
            <p class="read"><strong>Interpretación cuantitativa:</strong> En las eras clásica e intermedia, las carreras decisivas presentaban una tasa de conversión menor que las regulares (43.48% vs ~55%), reflejando que los pilotos especulaban con sumar puntos para asegurar la corona sin arriesgar la victoria. Sin embargo, en la era moderna la dinámica se invirtió: en carreras definitorias <strong>el 61.54% de las veces ganó el poleman</strong> (8 victorias en 13 poles decisivas), superando al 57.56% de las regulares.</p>
            <p class="read blue"><strong>Contribución al argumento:</strong> Subraya que en los momentos cumbres contemporáneos, la ventaja del líder de largada neutraliza cualquier intento de ataque del rival.</p>
            <p class="read gold"><strong>Limitaciones estadísticas:</strong> El tamaño de muestra de carreras decisivas es pequeño (13 en la era moderna, 23 en la clásica); los resultados son valiosos descriptivamente pero no permiten inferencia de significancia extrema por sí solos.</p>
          </div>
        </article>

        <!-- Q11 -->
        <article class="query" id="q11">
          <div class="qh">
            <span class="qid green">Q11</span>
            <h3>¿Cómo cambió la confiabilidad mecánica y qué rol jugaba en la variabilidad histórica?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y relación con la hipótesis</p>
              <p>Audita la tasa de averías mecánicas no forzadas frente a incidentes de competencia a través de las tres eras, evaluando si la variabilidad clásica era producto del talento o de la fragilidad del material.</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Es una pieza epistemológica fundamental: la "apertura" romántica de la F1 clásica estaba fuertemente inflada porque los punteros se quedaban tirados al costado del camino por roturas de motor, caja o suspensión. Si los autos modernos no fallan mecánicamente, el orden establecido en la grilla jamás se rompe.</p>
            </div>
            <div>
              <p class="qlabel">Tablas y relaciones SQL</p>
              <p>Categorización de la columna real <code>reason_retired</code> distinguiendo <em>Avería Mecánica</em> (motor, transmisión, hidráulica, eléctrica, etc.) de <em>Accidentes/Colisiones</em> sobre el total de participaciones.</p>
            </div>
            <pre><code class="sql">-- Q11: Evolución histórica de abandonos mecánicos vs accidentes en carrera
WITH clasif_retiros AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    rr.reason_retired,
    CASE
      WHEN rr.reason_retired IS NULL THEN 'Finalizo'
      WHEN rr.reason_retired IN ('Engine', 'Gearbox', 'Electrical', 'Transmission', 'Suspension', 
                                 'Brakes', 'Clutch', 'Hydraulics', 'Fuel system', 'Turbo', 
                                 'Overheating', 'Ignition', 'Oil leak', 'Throttle', 'Puncture', 
                                 'Radiator', 'Exhaust', 'Water pressure', 'Oil pressure', 'Battery') THEN 'Averia Mecanica'
      WHEN rr.reason_retired IN ('Accident', 'Collision', 'Spun off', 'Collision damage', 'Damage', 'Fatal accident') THEN 'Accidente/Colision'
      ELSE 'Otro Abandono'
    END AS categoria_retiro
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE r.year <= 2025
)
SELECT
  era,
  COUNT(*) AS total_participaciones,
  COUNT(*) FILTER (WHERE categoria_retiro != 'Finalizo') AS total_abandonos,
  ROUND(100.0 * COUNT(*) FILTER (WHERE categoria_retiro != 'Finalizo') / COUNT(*), 2) AS pct_abandono_total,
  COUNT(*) FILTER (WHERE categoria_retiro = 'Averia Mecanica') AS abandonos_mecanicos,
  ROUND(100.0 * COUNT(*) FILTER (WHERE categoria_retiro = 'Averia Mecanica') / COUNT(*), 2) AS pct_abandono_mecanico,
  COUNT(*) FILTER (WHERE categoria_retiro = 'Accidente/Colision') AS accidentes,
  ROUND(100.0 * COUNT(*) FILTER (WHERE categoria_retiro = 'Accidente/Colision') / COUNT(*), 2) AS pct_accidentes
FROM clasif_retiros
GROUP BY era
ORDER BY era;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16</p>
            {tf.table_q11()}
            <p class="read green"><strong>Interpretación cuantitativa:</strong> En la era clásica, la tasa de abandono total alcanzaba el <strong>44.46%</strong>, y las <strong>averías mecánicas puras representaban el 27.03% de todas las participaciones en pista</strong> (1 de cada 4 autos se rompía sin mediar accidente). En la era moderna, la tasa de abandono se desplomó al <strong>17.17%</strong>, y las fallas mecánicas cayeron a apenas el <strong>6.56%</strong> (una reducción del <strong>-75.7% en roturas mecánicas</strong>). Mientras los choques se mantuvieron estables (8.97% clásico vs 6.92% moderno), la ingeniería de materiales y los bancos de prueba computarizados prácticamente erradicaron las roturas espontáneas.</p>
            <p class="read"><strong>Contribución al argumento:</strong> Demuestra el mecanismo causal por el cual la ventaja de largada se volvió tan decisiva: <em>al extinguirse la fragilidad mecánica, el auto que larga adelante ya no corre el riesgo estocástico de abandonar, sellando el resultado técnico</em>.</p>
            <p class="read gold"><strong>Limitaciones:</strong> Algunos abandonos catalogados como mecánicos en épocas tempranas pudieron ser causados por mala gestión de marchas o sobre-régimen inducido por el piloto.</p>
          </div>
        </article>
      </div>
    </section>

    <!-- BLOQUE 5: EL FACTOR HUMANO -->
    <section id="bloque-piloto">
      <div class="col">
        <div class="sec-head">
          <div class="rule gold"></div>
          <p class="eyebrow" style="color:var(--gold)">08 · Eje Analítico V</p>
          <h2>El factor humano: compañeros de equipo y delta de posiciones</h2>
        </div>
        <p style="margin-bottom:28px">Para no caer en un determinismo tecnológico ciego, analizamos qué ocurre cuando dos pilotos disponen con exactitud del mismo auto, motor y neumáticos.</p>
      </div>

      <div class="wide">
        <!-- Q12 -->
        <article class="query" id="q12">
          <div class="qh">
            <span class="qid gold">Q12</span>
            <h3>¿Qué diferencias se observan entre compañeros de equipo que comparten el mismo paquete técnico?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y relación con la hipótesis</p>
              <p>Aísla el factor máquina contrastando a los pilotos titulares de los equipos hegemónicos en temporadas históricas emblemáticas (McLaren 1988, Ferrari 2002, Mercedes 2014/2016, Red Bull 2021/2023).</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Evita el sesgo de confirmar la hipótesis sin matices. Si el auto lo fuera todo, dos pilotos en el mismo monoplaza deberían repartirse las victorias al 50%. Si uno aplasta al otro sistemáticamente, el factor piloto conserva un peso diferencial determinante.</p>
            </div>
            <div>
              <p class="qlabel">Tablas y relaciones SQL</p>
              <p>Agrupación por <code>r.year</code>, <code>c.name</code>, <code>em.name</code> y <code>driver.name</code> sobre pares de pilotos con al menos 10 carreras compartidas en la misma temporada.</p>
            </div>
            <pre><code class="sql">-- Q12: Comparación de rendimiento intra-equipo en temporadas dominantes
WITH pares_clave AS (
  SELECT
    r.year,
    c.name AS constructor,
    em.name AS motor,
    d.name AS piloto,
    COUNT(*) AS carreras,
    COUNT(*) FILTER (WHERE rr.position_number = 1) AS victorias,
    COUNT(*) FILTER (WHERE rr.position_number <= 3) AS podios,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1) AS poles,
    ROUND(SUM(COALESCE(rr.points, 0)), 1) AS puntos
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN constructor c ON rr.constructor_id = c.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  JOIN driver d ON rr.driver_id = d.id
  WHERE (r.year IN (1988, 2002, 2014, 2016, 2021, 2023)
         AND c.name IN ('McLaren', 'Ferrari', 'Mercedes', 'Red Bull'))
  GROUP BY r.year, c.name, em.name, d.name
  HAVING COUNT(*) >= 10
)
SELECT year, constructor, motor, piloto, carreras, victorias, podios, poles, puntos
FROM pares_clave
ORDER BY year, constructor, victorias DESC, puntos DESC;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16</p>
            {tf.table_q12()}
            <p class="read gold"><strong>Interpretación cuantitativa:</strong> Los datos aportan el matiz crucial de la investigación:
              <br>• En escuderías con dos pilotos de élite absoluta como <strong>McLaren 1988</strong> (Senna 8 victorias / Prost 7 victorias) o <strong>Mercedes 2016</strong> (Hamilton 10 victorias / Rosberg 9 victorias), el auto garantiza el campeonato de constructores pero el título se define por destellos de talento y concentración individual.
              <br>• En contrapartida, cuando existe un piloto generacional frente a un compañero de menor calibre, la brecha es sideral: en <strong>Red Bull 2023, Max Verstappen obtuvo 19 victorias y 530 puntos frente a apenas 2 victorias y 260 puntos de Sergio Pérez</strong> conduciendo el mismo RB19 con unidad Honda RBPT. El auto dominó la F1, pero solo un piloto fue capaz de ganar el 86.4% de las carreras del año.</p>
            <p class="read"><strong>Contribución al argumento:</strong> Demuestra de manera irrefutable que <strong>el paquete tecnológico es una condición necesaria pero no suficiente</strong>. El auto establece el techo máximo alcanzable, pero solo el piloto de élite exprime ese potencial al 100%.</p>
            <p class="read gold"><strong>Limitaciones:</strong> No contempla órdenes de equipo contractuales (piloto número 1 y número 2 declarados en Ferrari 2002).</p>
          </div>
        </article>

        <!-- A1 -->
        <article class="query" id="a1">
          <div class="qh">
            <span class="qid green">A1</span>
            <h3>¿Cómo varió el delta entre posición de largada y posición final a lo largo de las eras?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y relación con la hipótesis (Análisis Complementario)</p>
              <p>Calcula el delta de posiciones (Delta = posición de largada - posición de llegada) para todos los autos que completaron la carrera, midiendo la frecuencia con la que los pilotos logran superar su posición de largada.</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Mide directamente la permeabilidad del pelotón en pista. Si en la era moderna la mayoría de los autos terminan exactamente en la posición que largaron ($\Delta = 0$), queda demostrado el fenómeno de la "procesión" aerodinámica y la dificultad para adelantar.</p>
            </div>
            <div>
              <p class="qlabel">Tablas y relaciones SQL</p>
              <p>Diferencia aritmética <code>(grid_position_number - position_number)</code> sobre participaciones con ambos campos no nulos.</p>
            </div>
            <pre><code class="sql">-- A1: Delta de posiciones ganadas/perdidas y tasa de retención de puesto por era
WITH deltas AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    rr.grid_position_number,
    rr.position_number,
    (rr.grid_position_number - rr.position_number) AS pos_ganadas
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE r.year <= 2025 
    AND rr.grid_position_number IS NOT NULL 
    AND rr.position_number IS NOT NULL
)
SELECT
  era,
  COUNT(*) AS total_finalizados,
  ROUND(AVG(pos_ganadas), 2) AS prom_pos_ganadas,
  COUNT(*) FILTER (WHERE pos_ganadas = 0) AS mantuvo_pos,
  ROUND(100.0 * COUNT(*) FILTER (WHERE pos_ganadas = 0) / COUNT(*), 2) AS pct_mantuvo_pos,
  COUNT(*) FILTER (WHERE pos_ganadas > 0) AS gano_pos,
  ROUND(100.0 * COUNT(*) FILTER (WHERE pos_ganadas > 0) / COUNT(*), 2) AS pct_gano_pos,
  COUNT(*) FILTER (WHERE pos_ganadas < 0) AS perdio_pos,
  ROUND(100.0 * COUNT(*) FILTER (WHERE pos_ganadas < 0) / COUNT(*), 2) AS pct_perdio_pos
FROM deltas
GROUP BY era
ORDER BY era;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16</p>
            {tf.table_a1()}
            <p class="read green"><strong>Interpretación cuantitativa:</strong> El promedio de posiciones ganadas entre los que cruzaron la bandera a cuadros cayó de <strong>+3.83 en la era clásica a +1.13 en la era moderna</strong>. Al mismo tiempo, el porcentaje de pilotos que <strong>mantiene de forma estricta su misma posición de salida ($\Delta = 0$) prácticamente se duplicó, pasando de 8.56% a 16.14%</strong>. La carrera moderna es mucho más estática: adelantar se volvió una tarea ardua y el orden de grilla congela el resultado de manera notable.</p>
            <p class="read"><strong>Contribución al argumento:</strong> Refuerza el argumento de que la aerodinámica moderna y la turbulencia del "aire sucio" dificultan la superación en pista, atando el destino de la carrera a la clasificación.</p>
            <p class="read gold"><strong>Limitaciones:</strong> No contempla paradas en boxes que alteran momentáneamente la posición antes de estabilizarse.</p>
          </div>
        </article>
      </div>
    </section>

    <!-- SÍNTESIS VISUAL COMPARATIVA -->
    <section id="sintesis-visual">
      <div class="col stack">
        <div class="sec-head">
          <div class="rule blue"></div>
          <p class="eyebrow" style="color:var(--accent-2)">09 · Síntesis Visual y Análisis Transversal</p>
          <h2>Panorámica de los hallazgos cuantitativos</h2>
        </div>
        <p>A continuación se integran las principales métricas transversales en gráficos interactivos construidos exclusivamente con los datos reales obtenidos de PostgreSQL 16.</p>

        <div class="chart-container">
          <h3>Evolución de la Tasa de Conversión Pole → Victoria por Década (1950–2025)</h3>
          <p style="font-size:.85rem;color:var(--muted);margin:4px 0 16px">Porcentaje de carreras ganadas desde P1 sobre oportunidades totales de pole (Q03).</p>
          <canvas id="chartPoleDecadas" height="120"></canvas>
        </div>

        <div class="chart-container">
          <h3>Tasa de Victoria y Podio por Franja de Grilla entre Eras (Q02)</h3>
          <p style="font-size:.85rem;color:var(--muted);margin:4px 0 16px">Comparativa de probabilidad condicional entre la Era Clásica (1950–1980) y la Era Moderna (2011–2025).</p>
          <canvas id="chartFranjasEras" height="130"></canvas>
        </div>

        <div class="chart-container">
          <h3>Evolución del Índice HHI de Concentración de Constructores (Q04)</h3>
          <p style="font-size:.85rem;color:var(--muted);margin:4px 0 16px">Suma cuadrática de cuotas de victoria por escudería: el salto hacia la oligopolización técnica.</p>
          <canvas id="chartHHI" height="110"></canvas>
        </div>

        <div class="chart-container">
          <h3>Desplome de las Averías Mecánicas en Carrera (Q11)</h3>
          <p style="font-size:.85rem;color:var(--muted);margin:4px 0 16px">Porcentaje de participaciones finalizadas por rotura mecánica no forzada.</p>
          <canvas id="chartMecanica" height="110"></canvas>
        </div>
      </div>
    </section>

    <!-- 10 CONCLUSIÓN GENERAL -->
    <section id="conclusion">
      <div class="col stack">
        <div class="sec-head">
          <div class="rule gold"></div>
          <p class="eyebrow" style="color:var(--gold)">10 · Conclusión General y Evaluación de la Hipótesis</p>
          <h2>El veredicto empírico de la investigación</h2>
        </div>

        <div class="hyp">
          «Los datos verificados sobre la base F1DB validan de manera PARCIAL Y ESTRUCTURADA la hipótesis formulada: la posición de largada y el fabricante de motor se han vuelto cuantitativamente más determinantes en la Fórmula 1 moderna, pero no anulan el talento del piloto, sino que redefinen su rol como el ejecutor indispensable de un paquete técnico superlativo».
        </div>

        <h3>1. Respuestas directas a las preguntas de la investigación</h3>
        <ul>
          <li><strong>¿La posición de largada se volvió más determinante?</strong> <strong>SÍ, de forma rotunda.</strong> La tasa de conversión de la Pole Position saltó del 37.13% en la era clásica al 53.07% en la era moderna (+42.9% de incremento relativo, Q02), y la probabilidad de hacer podio desde P1 trepó al 81.23%. Al mismo tiempo, las victorias desde P4 o más atrás cayeron a mínimos históricos (menos del 2.5%, Q02 y Q07).</li>
          <li><strong>¿Qué evidencia existe sobre el peso del fabricante de motor?</strong> <strong>HEGEMONÍA RÉCORD.</strong> En la era moderna, un solo fabricante (Mercedes) acaparó el 50.32% de todas las victorias (Q05). El Índice de concentración HHI se triplicó de 1.196 a 3.159 puntos (Q04).</li>
          <li><strong>¿La ventaja del motor persiste en posiciones de grilla similares?</strong> <strong>SÍ, pero condicionada al ritmo de carrera.</strong> Desde la pole, Honda RBPT (76.7%) y Mercedes (53.6%) superaron holgadamente a Ferrari (27.1%), demostrando que la unidad de potencia debe gestionar neumáticos y temperatura para sostener el triunfo (Q07).</li>
          <li><strong>¿La confiabilidad mecánica explica la aparente apertura histórica?</strong> <strong>SÍ, ES EL FACTOR DETERMINANTE OCULTO.</strong> Las fallas mecánicas colapsaron del 27.03% al 6.56% (Q11). En la F1 clásica, muchos triunfos desde atrás ocurrieron porque los punteros rompían el auto. Hoy los monoplazas no se rompen, congelando el orden de largada.</li>
          <li><strong>¿El talento del piloto quedó neutralizado?</strong> <strong>NO.</strong> La comparación entre compañeros de equipo (Q12) demuestra que, a igualdad de auto y motor, un piloto de élite como Verstappen en 2023 logró 19 victorias contra 2 de su compañero Pérez. El auto es condición <em>necesaria</em> para ganar, pero el piloto es la condición <em>suficiente</em> para hegemonizar.</li>
        </ul>

        <h3>2. Diferenciación entre asociación estadística y causalidad</h3>
        <p>Como estudiantes de Ciencia de Datos, debemos remarcar que una correlación elevada entre pole y victoria o entre motor Mercedes y triunfos no implica causalidad exclusiva del motor. El rendimiento de un F1 es un sistema acoplado: el mejor motor atrae a los mejores ingenieros aerodinámicos, al mayor presupuesto de desarrollo y a los pilotos más cotizados del mercado.</p>

        <h3>3. Mensaje sintético para la audiencia periodística</h3>
        <p class="read">Para el periodista deportivo o creador de contenido, la conclusión es nítida: <strong>la F1 moderna no premia las hazañas heroicas de domingo desde el fondo de la grilla; premia la perfección operativa y la ingeniería del sábado</strong>. El que no clasifica en la primera fila ha perdido estadísticamente el 80% de sus chances de victoria antes de que se apaguen los semáforos.</p>

        <h3>4. Limitaciones del estudio y futuras líneas de investigación</h3>
        <p style="font-size:.9rem;color:var(--muted);border-left:2px solid var(--line);padding-left:14px">
          <strong>Limitaciones reconocidas:</strong> La base F1DB no incorpora la telemetría en tiempo real ni la incidencia del auto de seguridad (Safety Car), las banderas rojas y las estrategias de parada en boxes. Tampoco cuantifica las diferencias de presupuesto previas al tope financiero (Budget Cap) instaurado en 2021.
          <br><br>
          <strong>Líneas futuras:</strong> Modelar la probabilidad de adelantamiento incorporando datos de telemetría de zonas DRS y estudiar el impacto de la reglamentación 2026 de combustibles 100% sostenibles y mayor hibridación eléctrica.
        </p>
      </div>
    </section>

  </div>

  <!-- FOOTER -->
  <footer>
    <div class="wide" style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;width:100%">
      <span>Rosa Kimel Connon — Base de Datos · Licenciatura en Ciencia de Datos · FI · 2026</span>
      <span>F1DB PostgreSQL 16 · Tercera Entrega Definitiva · 100% Ejecutado</span>
    </div>
  </footer>

  <script>
    // Gestión del tema día / noche
    const btn = document.getElementById('themeBtn');
    const root = document.documentElement;
    const saved = localStorage.getItem('f1-theme');
    if (saved) root.setAttribute('data-theme', saved);
    
    btn.addEventListener('click', () => {{
      const cur = root.getAttribute('data-theme');
      const next = cur === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('f1-theme', next);
      updateChartColors();
    }});

    // Animación de barras al hacer scroll
    const fills = document.querySelectorAll('.pbar-fill');
    const obs = new IntersectionObserver(entries => {{
      entries.forEach(e => {{
        if (e.isIntersecting) {{
          e.target.style.width = e.target.style.width; // trigger
          obs.unobserve(e.target);
        }}
      }});
    }}, {{ threshold: 0.3 }});
    fills.forEach(f => obs.observe(f));

    // Smooth scroll para el índice de navegación
    document.querySelectorAll('nav.toc a').forEach(a => {{
      a.addEventListener('click', e => {{
        e.preventDefault();
        const id = a.getAttribute('href').slice(1);
        document.getElementById(id)?.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }});
    }});

    // Configuración de Chart.js con datos reales de PostgreSQL 16
    let chartPole, chartFranjas, chartHHIInst, chartMecInst;

    function getChartColors() {{
      const isDark = root.getAttribute('data-theme') === 'dark';
      return {{
        textColor: isDark ? '#EDE9E5' : '#16130F',
        gridColor: isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)',
        accent: isDark ? '#E84040' : '#C01717',
        accent2: isDark ? '#5B8EE0' : '#1A4FA0',
        gold: isDark ? '#DCA455' : '#9C6A08',
        green: isDark ? '#2DB88A' : '#0D7A5A'
      }};
    }}

    function initCharts() {{
      const c = getChartColors();

      // Chart 1: Decadas Pole
      const ctxPole = document.getElementById('chartPoleDecadas').getContext('2d');
      chartPole = new Chart(ctxPole, {{
        type: 'line',
        data: {{
          labels: ['1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s'],
          datasets: [{{
            label: 'Tasa de Conversión Pole → Victoria (%)',
            data: [41.67, 37.00, 36.81, 28.21, 42.86, 50.00, 50.51, 55.38],
            borderColor: c.accent,
            backgroundColor: 'rgba(192,23,23,0.15)',
            borderWidth: 3,
            fill: true,
            tension: 0.3,
            pointRadius: 5,
            pointHoverRadius: 7
          }}]
        }},
        options: {{
          responsive: true,
          plugins: {{
            legend: {{ labels: {{ color: c.textColor, font: {{ family: 'Public Sans' }} }} }}
          }},
          scales: {{
            x: {{ ticks: {{ color: c.textColor }}, grid: {{ color: c.gridColor }} }},
            y: {{ min: 20, max: 65, ticks: {{ color: c.textColor, callback: v => v + '%' }}, grid: {{ color: c.gridColor }} }}
          }}
        }}
      }});

      // Chart 2: Franjas Q02
      const ctxFranjas = document.getElementById('chartFranjasEras').getContext('2d');
      chartFranjas = new Chart(ctxFranjas, {{
        type: 'bar',
        data: {{
          labels: ['P1 (Pole)', 'P2–P3', 'P4–P6', 'P7–P10', 'P11+'],
          datasets: [
            {{
              label: 'Era Clásica (1950–1980) - % Victoria',
              data: [37.13, 17.98, 5.26, 1.90, 0.29],
              backgroundColor: c.accent2
            }},
            {{
              label: 'Era Moderna (2011–2025) - % Victoria',
              data: [53.07, 17.61, 2.47, 0.81, 0.12],
              backgroundColor: c.green
            }}
          ]
        }},
        options: {{
          responsive: true,
          plugins: {{
            legend: {{ labels: {{ color: c.textColor, font: {{ family: 'Public Sans' }} }} }}
          }},
          scales: {{
            x: {{ ticks: {{ color: c.textColor }}, grid: {{ color: c.gridColor }} }},
            y: {{ ticks: {{ color: c.textColor, callback: v => v + '%' }}, grid: {{ color: c.gridColor }} }}
          }}
        }}
      }});

      // Chart 3: HHI Q04
      const ctxHHI = document.getElementById('chartHHI').getContext('2d');
      chartHHIInst = new Chart(ctxHHI, {{
        type: 'bar',
        data: {{
          labels: ['Era Clásica (1950–1980)', 'Era Intermedia (1981–2010)', 'Era Moderna (2011–2025)'],
          datasets: [{{
            label: 'Índice de Concentración HHI',
            data: [1196.3, 2111.0, 3159.4],
            backgroundColor: [c.accent2, c.gold, c.accent]
          }}]
        }},
        options: {{
          responsive: true,
          plugins: {{
            legend: {{ display: false }}
          }},
          scales: {{
            x: {{ ticks: {{ color: c.textColor }}, grid: {{ color: c.gridColor }} }},
            y: {{ ticks: {{ color: c.textColor }}, grid: {{ color: c.gridColor }} }}
          }}
        }}
      }});

      // Chart 4: Fallas Mecanicas Q11
      const ctxMec = document.getElementById('chartMecanica').getContext('2d');
      chartMecInst = new Chart(ctxMec, {{
        type: 'bar',
        data: {{
          labels: ['Era Clásica (1950–1980)', 'Era Intermedia (1981–2010)', 'Era Moderna (2011–2025)'],
          datasets: [
            {{
              label: 'Tasa Avería Mecánica (%)',
              data: [27.03, 23.74, 6.56],
              backgroundColor: c.accent
            }},
            {{
              label: 'Tasa Choques/Accidentes (%)',
              data: [8.97, 12.35, 6.92],
              backgroundColor: c.accent2
            }}
          ]
        }},
        options: {{
          responsive: true,
          plugins: {{
            legend: {{ labels: {{ color: c.textColor, font: {{ family: 'Public Sans' }} }} }}
          }},
          scales: {{
            x: {{ ticks: {{ color: c.textColor }}, grid: {{ color: c.gridColor }} }},
            y: {{ ticks: {{ color: c.textColor, callback: v => v + '%' }}, grid: {{ color: c.gridColor }} }}
          }}
        }}
      }});
    }}

    function updateChartColors() {{
      if (chartPole) {{
        chartPole.destroy();
        chartFranjas.destroy();
        chartHHIInst.destroy();
        chartMecInst.destroy();
        initCharts();
      }}
    }}

    document.addEventListener('DOMContentLoaded', initCharts);
  </script>
</body>
</html>
"""

# Write to workspace
target_workspace = r"c:\Users\narda\Downloads\FI BD-LCD 2026 Tema 05 - SQL Practica - F1\FI BD-LCD 2026 Tema 05 - SQL Practica - F1\TP-cuatrimestral-3ra_entrega-Rosa_Kimel_Connon.html"
with open(target_workspace, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"Successfully wrote {len(html_content)} bytes to workspace: {target_workspace}")

# Write to brain artifact directory as well
target_brain = r"c:\Users\narda\.gemini\antigravity-ide\brain\bd71d553-149e-4436-a7cb-ab58c601963a\TP-cuatrimestral-3ra_entrega-Rosa_Kimel_Connon.html"
with open(target_brain, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"Successfully wrote {len(html_content)} bytes to brain artifact: {target_brain}")
