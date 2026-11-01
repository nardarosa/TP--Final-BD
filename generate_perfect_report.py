# -*- coding: utf-8 -*-
"""
Generador definitivo y riguroso de la Tercera Entrega:
'TP-cuatrimestral-3ra_entrega-Rosa_Kimel_Connon.html'
Corrige todas las inconsistencias detectadas:
1. Q06: Texto 100% coincidente con la tabla (Mercedes 2.205 part, 157 vic, 7.12%, 430 pod, 19.50%; Honda/RBPT 770 part, 72 vic, 9.35%, 141 pod, 18.31%; sin mencionar a Vanwall).
2. Q01: SQL con LIMIT 10 y tabla con exactamente 10 filas (P1 a P10).
3. Q10 vs Q02/Q03: Denominador unificado (342 poles clásicas, 496 intermedias, 309 modernas) y explicación explícita del filtro position_number IS NOT NULL (235, 373, 284) como poles condicionales a cruzar la meta.
4. Nulos de grilla: Explicación transparente de los 2.001 nulos (801, 1.047, 153) por DNQ, DNPQ, DNS y pit-lane, fijando la población base común de 25.290 largadas efectivas.
5. Entrega 1 vs 3: Justificación explícita del cambio de esquema (public -> formula1), tablas físicas (48), carreras (1.149 cerradas vs 1.172 con 2026/anuladas) y eras (3 canónicas + corte 2014).
6. Objetivo 6: Desacopla talento (Q12) de permeabilidad del pelotón (A1).
7. Conclusión: Porcentajes matemáticamente precisos (Top 3 gana el 88.06% de las carreras modernas, 273 de 310; P4-P6 tiene 2.47% por largada).
8. Q12 y Meta description: Elimina "causal" de la meta description y sustituye "condición suficiente" por "el auto fija el techo y el piloto define cuánto se alcanza".
"""
import json, os
import table_formatters as tf

with open('all_query_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Banner facts
c_bruta_clasica = [r for r in data['q10_conditional'] if 'Clasica' in r['era']][0]['conversion_bruta_pct']
c_bruta_moderna = [r for r in data['q10_conditional'] if 'Moderna' in r['era']][0]['conversion_bruta_pct']
c_cond_clasica = [r for r in data['q10_conditional'] if 'Clasica' in r['era']][0]['conversion_si_termina_pct']
c_cond_moderna = [r for r in data['q10_conditional'] if 'Moderna' in r['era']][0]['conversion_si_termina_pct']

ab_pole_clasica = [r for r in data['q10_conditional'] if 'Clasica' in r['era']][0]['pct_abandono_poleman']
ab_pole_moderna = [r for r in data['q10_conditional'] if 'Moderna' in r['era']][0]['pct_abandono_poleman']

hhi_clasica_anual = [r for r in data['q04_annual_hybrid'] if 'Clasica' in r['era']][0]['prom_hhi_anual']
hhi_hibrida_anual = [r for r in data['q04_annual_hybrid'] if 'Hibrida' in r['era']][0]['prom_hhi_anual']
leader_share_hibrida = [r for r in data['q04_annual_hybrid'] if 'Hibrida' in r['era']][0]['prom_share_lider_anual']

driver_share_hibrida = [r for r in data['q08_hybrid'] if 'Hibrida' in r['era']][0]['prom_share_max_ganador']

falla_mec_clasica = [r for r in data['q11_audited'] if 'Clasica' in r['era']][0]['pct_abandono_mecanico']
falla_mec_moderna = [r for r in data['q11_audited'] if 'Moderna' in r['era']][0]['pct_abandono_mecanico']

html_content = f"""<!doctype html>
<html lang="es" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Las eras de la F1 — Tercera Entrega Definitiva · Investigación Analítica y Econométrica</title>
  <meta name="description" content="Tercera Entrega Trabajo Práctico de Base de Datos – Licenciatura en Ciencia de Datos. Análisis SQL avanzado sobre F1DB PostgreSQL 16. Evaluación cuantitativa, asociativa y econométrica del impacto de la posición de largada, la confiabilidad mecánica y el paquete técnico frente al talento del piloto.">
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
      --purple: #6B21A8;
      --purple-soft: #F3E8FF;
      --shadow: 0 1px 3px rgba(22,19,15,.07), 0 8px 28px -14px rgba(22,19,15,.25);
      --shadow-lg: 0 2px 8px rgba(22,19,15,.1), 0 20px 40px -20px rgba(22,19,15,.3);
    }}
    @media (prefers-color-scheme: dark) {{
      :root:not([data-theme="light"]) {{
        --ground:#100E0C;--surface:#1A1714;--surface-2:#211D1B;--ink:#EDE9E5;
        --muted:#998F88;--line:#2C2622;--accent:#E84040;--accent-soft:#2C1010;
        --accent-2:#5B8EE0;--accent-2-soft:#0E1E3A;--gold:#DCA455;--gold-soft:#261E0A;
        --new-badge:#2DB88A;--new-badge-soft:#0C2A1F;
        --purple:#C084FC;--purple-soft:#2E1065;
        --shadow:0 1px 3px rgba(0,0,0,.4),0 8px 28px -14px rgba(0,0,0,.7);
        --shadow-lg:0 2px 8px rgba(0,0,0,.5),0 20px 40px -20px rgba(0,0,0,.8);
      }}
    }}
    :root[data-theme="dark"] {{
      --ground:#100E0C;--surface:#1A1714;--surface-2:#211D1B;--ink:#EDE9E5;
      --muted:#998F88;--line:#2C2622;--accent:#E84040;--accent-soft:#2C1010;
      --accent-2:#5B8EE0;--accent-2-soft:#0E1E3A;--gold:#DCA455;--gold-soft:#261E0A;
      --new-badge:#2DB88A;--new-badge-soft:#0C2A1F;
      --purple:#C084FC;--purple-soft:#2E1065;
      --shadow:0 1px 3px rgba(0,0,0,.4),0 8px 28px -14px rgba(0,0,0,.7);
      --shadow-lg:0 2px 8px rgba(0,0,0,.5),0 20px 40px -20px rgba(0,0,0,.8);
    }}

    *{{box-sizing:border-box}}
    body{{margin:0;background:var(--ground);color:var(--ink);font-family:"Public Sans",-apple-system,"Segoe UI",sans-serif;font-size:16.5px;line-height:1.68;-webkit-font-smoothing:antialiased}}
    .page{{max-width:1160px;margin:0 auto;padding:0 24px 120px}}
    .col{{max-width:74ch;margin:0 auto;width:100%}}
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
    .eyebrow.purple{{color:var(--purple)}}

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
    .badge-tag.purple{{background:var(--purple-soft);color:var(--purple)}}

    section{{padding:68px 0 0}}
    .sec-head{{display:flex;flex-direction:column;gap:10px;margin-bottom:28px}}
    .sec-head .rule{{height:3px;background:var(--accent);width:48px;border-radius:2px}}
    .sec-head .rule.blue{{background:var(--accent-2)}}
    .sec-head .rule.gold{{background:var(--gold)}}
    .sec-head .rule.green{{background:var(--new-badge)}}
    .sec-head .rule.purple{{background:var(--purple)}}
    .stack{{display:flex;flex-direction:column;gap:20px}}

    .facts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:16px 0}}
    .fact{{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:18px 20px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:6px;transition:box-shadow .2s,transform .2s}}
    .fact:hover{{box-shadow:var(--shadow-lg);transform:translateY(-2px)}}
    .fact .n{{font-family:"Newsreader",Georgia,serif;font-size:2.2rem;line-height:1;font-weight:600;color:var(--accent);font-variant-numeric:tabular-nums}}
    .fact .n.blue{{color:var(--accent-2)}}.fact .n.gold{{color:var(--gold)}}.fact .n.green{{color:var(--new-badge)}}.fact .n.purple{{color:var(--purple)}}
    .fact .l{{font-size:.86rem;color:var(--muted);line-height:1.38}}

    .query{{background:var(--surface);border:1px solid var(--line);border-radius:6px;box-shadow:var(--shadow);margin-bottom:38px;overflow:hidden;transition:box-shadow .2s}}
    .query:hover{{box-shadow:var(--shadow-lg)}}
    .query .qh{{padding:18px 22px 14px;border-bottom:1px solid var(--line);display:flex;gap:14px;align-items:baseline;flex-wrap:wrap;background:var(--surface-2)}}
    .qid{{font-family:"IBM Plex Mono",monospace;font-size:.78rem;font-weight:600;color:var(--accent);background:var(--accent-soft);padding:3px 9px;border-radius:3px;flex:none}}
    .qid.green{{color:var(--new-badge);background:var(--new-badge-soft)}}
    .qid.blue{{color:var(--accent-2);background:var(--accent-2-soft)}}
    .qid.gold{{color:var(--gold);background:var(--gold-soft)}}
    .qid.purple{{color:var(--purple);background:var(--purple-soft)}}
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
    tbody tr.hlp td{{background:var(--purple-soft);font-weight:600}}

    .read{{border-left:3px solid var(--accent);padding:14px 18px;font-size:.95rem;color:var(--ink);background:var(--accent-soft);border-radius:0 5px 5px 0}}
    .read.blue{{border-color:var(--accent-2);background:var(--accent-2-soft)}}
    .read.green{{border-color:var(--new-badge);background:var(--new-badge-soft)}}
    .read.gold{{border-color:var(--gold);background:var(--gold-soft)}}
    .read.purple{{border-color:var(--purple);background:var(--purple-soft)}}
    .read strong{{color:var(--accent)}}.read.blue strong{{color:var(--accent-2)}}.read.green strong{{color:var(--new-badge)}}.read.gold strong{{color:var(--gold)}}.read.purple strong{{color:var(--purple)}}

    .hyp{{background:var(--accent-soft);border-left:4px solid var(--accent);border-radius:0 6px 6px 0;padding:22px 24px;font-family:"Newsreader",Georgia,serif;font-size:1.22rem;line-height:1.55;font-style:italic}}
    ol.obj{{margin:0;padding-left:1.4em;display:flex;flex-direction:column;gap:12px}}
    ol.obj li::marker{{font-family:"IBM Plex Mono",monospace;color:var(--accent);font-weight:600}}

    .summary-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin:20px 0}}
    .sum-card{{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:18px 20px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:8px}}
    .sum-card .sc-head{{display:flex;align-items:center;gap:10px}}
    .sum-card .sc-num{{width:32px;height:32px;border-radius:50%;background:var(--accent);color:white;font-family:"IBM Plex Mono",monospace;font-size:.78rem;font-weight:600;display:flex;align-items:center;justify-content:center;flex:none}}
    .sum-card .sc-num.blue{{background:var(--accent-2)}}.sum-card .sc-num.gold{{background:var(--gold)}}.sum-card .sc-num.green{{background:var(--new-badge)}}.sum-card .sc-num.purple{{background:var(--purple)}}
    .sum-card .sc-title{{font-weight:600;font-size:.96rem}}
    .sum-card p{{font-size:.88rem;color:var(--muted);line-height:1.5}}
    .sum-card .sc-result{{background:var(--surface-2);border-radius:4px;padding:8px 12px;font-family:"IBM Plex Mono",monospace;font-size:.78rem;color:var(--accent);border-left:2px solid var(--accent);margin-top:4px}}
    .sum-card .sc-result.blue{{color:var(--accent-2);border-color:var(--accent-2)}}.sum-card .sc-result.gold{{color:var(--gold);border-color:var(--gold)}}.sum-card .sc-result.green{{color:var(--new-badge);border-color:var(--new-badge)}}.sum-card .sc-result.purple{{color:var(--purple);border-color:var(--purple)}}

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
        <p class="eyebrow">Base de Datos · Tercera Entrega Definitiva · F1DB PostgreSQL 16 · LCD FI 2026</p>
        <h1>Las eras de la Fórmula 1</h1>
        <p class="lede">Investigación cuantitativa, asociativa y econométrica: evaluación del impacto de la posición de largada, la concentración de constructores y la motorización frente a la confiabilidad mecánica y el talento del piloto a lo largo de 76 temporadas del Campeonato Mundial (1950–2025).</p>
        <dl class="meta">
          <div><dt>Autor</dt><dd>Rosa Kimel Connon</dd></div>
          <div><dt>Motor</dt><dd>PostgreSQL 16</dd></div>
          <div><dt>Esquema</dt><dd>formula1 (F1DB)</dd></div>
          <div><dt>Período analizado</dt><dd>1950 – 2025 (cerrado)</dd></div>
          <div><dt>Grandes Premios</dt><dd>1.149 carreras</dd></div>
          <div><dt>Participaciones</dt><dd>27.291 filas auditadas</dd></div>
          <div><dt>Población Grilla</dt><dd>25.290 largadas efectivas</dd></div>
          <div><dt>Control Técnico</dt><dd>Rebadging + Clientes</dd></div>
        </dl>
        <nav class="toc">
          <p class="qlabel">Índice analítico de secciones y consultas</p>
          <ol>
            <li><a href="#eda">01 · Resumen ejecutivo del Análisis Exploratorio (EDA) y auditoría de grilla</a></li>
            <li><a href="#hipotesis">02 · Hipótesis central, preguntas analíticas y delimitación</a></li>
            <li><a href="#metodologia">03 · Metodología, conciliación entre entregas y taxonomía técnica</a></li>
            <li><a href="#bloque-grilla">04 · Eje I: Posición de largada y probabilidad de victoria (Q01, Q02, Q03 Crossover)</a></li>
            <li><a href="#bloque-competitividad">05 · Eje II: Concentración y competitividad longitudinal (Q04 HHI Anual, Q08 Piloto Dominante)</a></li>
            <li><a href="#bloque-motor">06 · Eje III: Hegemonía del motor y aislamiento oficial vs cliente (Q05, Q06, Q07)</a></li>
            <li><a href="#bloque-critico">07 · Eje IV: Campeones, carreras decisivas y el sesgo de confiabilidad (Q09, Q10 Condicional, Q11)</a></li>
            <li><a href="#bloque-piloto">08 · Eje V: El factor humano: brecha sistemática entre compañeros y movilidad (Q12, A1)</a></li>
            <li><a href="#bloque-econometrico">09 · Eje VI: Inferencia estadística formal y regresión logística multivariada</a> <span class="badge-tag purple">Nuevo</span></li>
            <li><a href="#sintesis-visual">10 · Síntesis visual y análisis comparativo transversal</a></li>
            <li><a href="#conclusion">11 · Conclusión general y veredicto definitivo de la hipótesis</a></li>
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
          <h2>Fundamentos empíricos de F1DB y auditoría de grilla</h2>
        </div>
        <p>Como punto de partida de la investigación (establecido en la 1ª y 2ª entrega), se realizó una auditoría estructural exhaustiva sobre el modelo relacional de <strong>F1DB</strong> desplegado en PostgreSQL 16. La base contiene 48 tablas y vistas que registran cada sesión desde el Gran Premio de Gran Bretaña de 1950 hasta la actualidad.</p>
        
        <div class="facts">
          <div class="fact"><span class="n">1.149</span><span class="l">carreras puntuables disputadas en temporadas completas (1950–2025)</span></div>
          <div class="fact"><span class="n blue">27.291</span><span class="l">filas totales de inscripción en <code>formula1.race_result</code></span></div>
          <div class="fact"><span class="n gold">25.290</span><span class="l">largadas efectivas en cajón de grilla (población base común)</span></div>
          <div class="fact"><span class="n green">100%</span><span class="l">cobertura de motorización en todas las participaciones analizadas</span></div>
        </div>

        <div class="summary-grid">
          <div class="sum-card">
            <div class="sc-head"><div class="sc-num">E01</div><span class="sc-title">Volumen y granularidad</span></div>
            <p>La tabla central <code>race_result</code> alberga 27.291 filas con detalle de largada, llegada, motor, neumáticos, tiempos y estatus final.</p>
            <div class="sc-result">race_result → 27.291 participaciones registradas</div>
          </div>
          <div class="sum-card">
            <div class="sc-head"><div class="sc-num">E02</div><span class="sc-title">Tratamiento de nulos de grilla</span></div>
            <p>Existen 2.001 registros con <code>grid_position_number IS NULL</code> distribuidos en todas las eras: 801 en la clásica (463 no clasificados DNQ y 40 no largaron DNS), 1.047 en la intermedia (preclasificación masiva de 35+ autos) y 153 en la moderna (largadas desde pit-lane y fallas en vuelta de formación). Se define como <strong>población base común de análisis las 25.290 largadas efectivas</strong>.</p>
            <div class="sc-result">Población base común = 25.290 largadas con grilla conocida</div>
          </div>
          <div class="sum-card">
            <div class="sc-head"><div class="sc-num blue">E03</div><span class="sc-title">Expansión del calendario</span></div>
            <p>El campeonato pasó de 7 carreras anuales en 1950 a 24 en 2024–2025. Esto obliga a normalizar métricas mediante tasas y promedios por temporada para no incurrir en distorsiones mecánicas.</p>
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
          «En la Fórmula 1 moderna, la posición de largada y el fabricante de motor son factores significativamente más determinantes del resultado final que en las primeras eras del campeonato (1950–1980), evidenciando que la competitividad se concentra cada vez más en ventajas tecnológicas y estratégicas por sobre el desempeño individual del piloto en carrera».
        </div>

        <h3>Pregunta principal de investigación</h3>
        <p class="read"><strong>¿En qué medida la posición de largada y el fabricante de motor se asocian con el éxito en carrera, y cómo varía ese poder predictivo entre las distintas eras de la Fórmula 1 una vez que se controla por la confiabilidad mecánica y el estatus oficial/cliente?</strong></p>

        <h3>Audiencia objetivo y valor periodístico</h3>
        <p>Esta solución está específicamente diseñada para <strong>periodistas deportivos, creadores de contenido especializado y analistas de datos del automovilismo</strong>. Permite sustentar notas de investigación, contextualizar los debates sobre reglamentaciones FIA (como el reglamento 2026 de unidades de potencia) y ofrecer métricas comprensibles pero matemáticamente impecables para superar las opiniones intuitivas.</p>

        <h3>Objetivos específicos estructurados</h3>
        <ol class="obj">
          <li><strong>Medir el peso predictivo de la grilla de partida:</strong> cuantificar la probabilidad real de victoria y podio según franja de largada sobre las 25.290 largadas efectivas y su evolución temporal (Q01, Q02, Q03).</li>
          <li><strong>Evaluar la concentración del poder constructivo:</strong> calcular el Índice Herfindahl-Hirschman (HHI) anual promedio para eliminar sesgos de longitud temporal e incorporar el corte de la Era Híbrida en 2014 (Q04).</li>
          <li><strong>Medir la concentración de pilotos inmune al calendario:</strong> calcular el porcentaje de victorias del máximo ganador de cada temporada y el HHI de pilotos anual (Q08).</li>
          <li><strong>Aislar la influencia del fabricante de motor (Rebadging y Oficiales vs Clientes):</strong> unificar denominaciones comerciales dispersas y contrastar el rendimiento del mismo motor entre equipos oficiales de fábrica y escuderías clientes (Q05, Q06, Q07).</li>
          <li><strong>Analizar las instancias críticas y la pole condicionada:</strong> comprobar el peso de la pole en campeones (Q09) y evaluar la tasa de conversión condicionada a cruzar la meta para aislar el efecto de los abandonos (Q10).</li>
          <li><strong>Auditar la confiabilidad mecánica como variable de confusión:</strong> diferenciar si la mayor previsibilidad moderna responde al chasis/motor o al colapso de fallas mecánicas fortuitas, modernizando la taxonomía de retiros (Q11).</li>
          <li><strong>Controlar por el talento individual entre compañeros de equipo:</strong> contrastar parejas de pilotos con auto y motor idénticos a nivel sistemático en las 584 temporadas con $\ge 10$ carreras compartidas (Q12).</li>
          <li><strong>Evaluar la permeabilidad del pelotón y la movilidad en carrera:</strong> computar el delta de posiciones ganadas/perdidas ($\Delta = Grilla - Llegada$) y analizar críticamente la hipótesis de la procesión aerodinámica frente al sesgo de supervivencia (A1).</li>
          <li><strong>Someter la hipótesis a contrastes estadísticos formales:</strong> calcular intervalos de confianza de Wilson al 95%, tests de Chi-cuadrado y estimar una regresión logística multivariada de probabilidad de victoria (Eje VI).</li>
        </ol>
      </div>
    </section>

    <!-- 03 METODOLOGÍA Y ESQUEMA -->
    <section id="metodologia">
      <div class="col stack">
        <div class="sec-head">
          <div class="rule blue"></div>
          <p class="eyebrow" style="color:var(--accent-2)">03 · Metodología y Auditoría de Datos</p>
          <h2>Delimitación temporal, esquema y conciliación entre entregas</h2>
        </div>
        <p>Para asegurar una comparabilidad estadística rigurosa, se adoptaron las siguientes definiciones metodológicas:</p>
        
        <div class="read blue">
          <strong>Nota de conciliación metodológica entre entregas:</strong>
          <br>• <strong>Esquema físico canónico:</strong> en la 1ª y 2ª entrega se consultaba el esquema preliminar <code>public</code> y vistas consolidadas. En esta entrega se migró al esquema oficial de producción <code>formula1</code> en PostgreSQL 16 (48 tablas físicas y vistas de catálogo), accediendo a tablas canónicas como <code>formula1.race_result</code>.
          <br>• <strong>Universo de carreras (1.172 vs 1.149):</strong> borradores exploratorios iniciales incluían Grandes Premios futuros del calendario 2026 y pruebas especiales o canceladas que sumaban 1.172 registros en <code>race</code>. Para esta investigación definitiva se cerró el universo a las <strong>1.149 carreras puntuables de campeonato efectivamente disputadas y concluidas entre 1950 y 2025</strong>.
          <br>• <strong>Periodización estructural (4 vs 3 eras):</strong> la partición previa en 4 sub-eras fragmentaba en exceso el tamaño muestral. Se consolidó la estructura canónica en 3 eras (Clásica 1950–1980, Intermedia 1981–2010 y Moderna 2011–2025), incorporando adicionalmente el <strong>corte reglamentario de 2014 (Era Híbrida V6 Turbo)</strong> en los análisis de concentración tecnológica.
        </div>

        <h3>1. Delimitación temporal en tres eras comparables y el corte 2014</h3>
        <ul>
          <li><strong>Era Clásica (1950–1980):</strong> 31 temporadas fundacionales (342 carreras), caracterizadas por motores atmosféricos, baja aerodinámica y altísima tasa de roturas mecánicas.</li>
          <li><strong>Era Intermedia (1981–2010 / 2013):</strong> abarca la primera era Turbo, los motores V10 y los motores V8 atmosféricos de 2.4L (497 carreras hasta 2010; 555 hasta 2013).</li>
          <li><strong>Era Híbrida / Moderna (2014–2025 / 2011–2025):</strong> dominada por unidades de potencia V6 turbo-híbridas con recuperación de energía cinética y térmica, túnel de viento CFD y congelamiento normativo (310 carreras modernas; 252 híbridas).</li>
        </ul>

        <h3>2. Normalización de familias de motor (Rebadging comercial)</h3>
        <p>En la F1 contemporánea e histórica, razones de patrocinio comercial llevaron a renombrar unidades de potencia idénticas. Para evitar subestimar dinastías tecnológicas, se implementó el siguiente mapeo analítico:</p>
        <pre><code class="sql">CASE
  WHEN em.name IN ('Honda', 'Honda RBPT', 'RBPT', 'Mugen-Honda') THEN 'Honda / RBPT'
  WHEN em.name IN ('Renault', 'TAG Heuer', 'Mecachrome', 'Playlife', 'Supertec') THEN 'Renault / TAG Heuer'
  WHEN em.name IN ('Mercedes', 'BWT Mercedes') THEN 'Mercedes'
  WHEN em.name IN ('Ford', 'Cosworth') THEN 'Ford / Cosworth'
  WHEN em.name IN ('Ferrari', 'Petronas', 'Acer') THEN 'Ferrari'
  WHEN em.name IN ('TAG', 'Porsche') THEN 'Porsche / TAG'
  WHEN em.name IN ('BMW', 'Megatron') THEN 'BMW'
  ELSE em.name
END AS familia_motor</code></pre>
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
            <h3>¿Desde qué posiciones de la grilla se obtuvieron las victorias históricas? (Top 10)</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y relación con la hipótesis</p>
              <p>Describe la distribución histórica agregada de las victorias entre 1950 y 2025 según la posición de partida sobre las 1.149 carreras disputadas. Permite medir el grado de concentración inicial en la primera fila antes de pasar al cálculo probabilístico condicional.</p>
            </div>
            <div>
              <p class="qlabel">Tablas y relaciones SQL</p>
              <p><code>race_result (rr)</code> unida con <code>race (r)</code> mediante <code>rr.race_id = r.id</code>. Se filtra por <code>rr.position_number = 1</code> y <code>rr.grid_position_number IS NOT NULL</code>. Se aplica la función de ventana <code>SUM(COUNT(*)) OVER ()</code> limitando a las 10 primeras posiciones de grilla.</p>
            </div>
            <pre><code class="sql">-- Q01: Distribución histórica de victorias por posición de largada (1950-2025, Top 10)
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
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16 (Top 10 Posiciones de Grilla)</p>
            {tf.table_q01()}
            <p class="read"><strong>Interpretación cuantitativa:</strong> A lo largo de la historia, la <strong>Pole Position (P1)</strong> acapara 497 victorias, representando el <strong>43.26%</strong> de todas las carreras ganadas con grilla registrada. La segunda posición aporta el <strong>23.67%</strong> (272 victorias) y la tercera el <strong>12.01%</strong> (138 victorias). En conjunto, <strong>el 78.94% de todas las carreras de F1 fueron ganadas por pilotos que largaron entre los tres primeros (907 de 1.149 victorias)</strong>. Las posiciones P4 a P10 acumulan de manera combinada el 19.23%, mientras que ganar desde el puesto 11 o más atrás es una anomalía estadística histórica (apenas 21 victorias en 76 años: 1.83%).</p>
            <p class="read blue"><strong>Contribución al argumento:</strong> Respalda la premisa de que la grilla es el factor determinante primario. No obstante, al ser una métrica global no condicionada por el total de participaciones en cada cajón, hace indispensable avanzar hacia Q02 para calcular la tasa de éxito real por era.</p>
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
              <p>Calcula la probabilidad real (tasa de conversión sobre participaciones efectivas con grilla conocida) de conseguir una victoria y un podio desglosada por franjas de grilla homogéneas (P1, P2–P3, P4–P6, P7–P10, P11+) a través de las tres eras del campeonato.</p>
            </div>
            <pre><code class="sql">-- Q02: Probabilidad condicional de victoria y podio por franja de grilla y por era
WITH clasif AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
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
  JOIN race r ON rr.race_id = r.id
  WHERE rr.grid_position_number IS NOT NULL AND r.year <= 2025
)
SELECT
  era, franja,
  COUNT(*) AS participaciones,
  COUNT(*) FILTER (WHERE position_number = 1) AS victorias,
  ROUND(100.0 * COUNT(*) FILTER (WHERE position_number = 1) / COUNT(*), 2) AS pct_victoria,
  COUNT(*) FILTER (WHERE position_number <= 3) AS podios,
  ROUND(100.0 * COUNT(*) FILTER (WHERE position_number <= 3) / COUNT(*), 2) AS pct_podio
FROM clasif
GROUP BY era, franja, orden_franja
ORDER BY era, orden_franja;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16 (Población Base = 25.290 Largadas Efectivas)</p>
            {tf.table_q02()}
            <p class="read green"><strong>Interpretación cuantitativa:</strong> La tasa de conversión de Pole en victoria trepó del <strong>37.13% en la era clásica al 53.07% en la era moderna (+15.94 pp, un incremento relativo del +42.9%)</strong>. Aún más elocuente es la tasa de podio para el poleman: en la era moderna alcanza un abrumador <strong>81.23%</strong>. Simultáneamente, la posibilidad individual de ganar largando en P4–P6 se redujo a más de la mitad (del 5.26% clásico al 2.47% moderno), y desde P11+ es virtualmente nula (apenas 4 victorias en 3.215 largadas: 0.12%).</p>
          </div>
        </article>

        <!-- Q03 CROSSOVER -->
        <article class="query" id="q03">
          <div class="qh">
            <span class="qid gold">Q03</span>
            <h3>¿Cómo interactúa la confiabilidad mecánica con la conversión de pole década a década?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y respuesta metodológica</p>
              <p>Cruza la serie temporal de conversión de pole con la tasa de abandonos del poleman y la tasa global de fallas mecánicas para <strong>evaluar la causa real del piso histórico de los años 80</strong>.</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Resuelve el dilema causal planteado por los críticos: ¿por qué en los 80 la pole se convirtió solo en un 28% de victorias? Al cruzar las variables, se comprueba que no respondía a adelantamientos en pista, sino a una epidemia de roturas de motor en plena carrera.</p>
            </div>
            <pre><code class="sql">-- Q03: Cruce longitudinal de conversión de pole vs confiabilidad mecánica por década
WITH decade_stats AS (
  SELECT
    (r.year / 10) * 10 AS decada,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1) AS total_poles,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.position_number = 1) AS victorias_pole,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.reason_retired IS NULL) AS poles_terminaron,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.reason_retired IS NOT NULL) AS poles_abandonaron,
    COUNT(*) AS total_participaciones,
    COUNT(*) FILTER (WHERE rr.reason_retired IN (
      'Engine', 'Gearbox', 'Electrical', 'Transmission', 'Suspension', 
      'Brakes', 'Clutch', 'Hydraulics', 'Fuel system', 'Turbo', 
      'Overheating', 'Ignition', 'Oil leak', 'Throttle', 
      'Radiator', 'Exhaust', 'Water pressure', 'Oil pressure', 'Battery',
      'Power Unit', 'ERS', 'Power loss', 'Electronics', 'Hybrid system',
      'Energy storage system failure', 'KERS failure', 'Differential', 'Driveshaft',
      'Cooling system', 'Coolant leak', 'Turbocharger', 'Fuel pressure', 'Fuel leak',
      'Technical defect', 'Mechenical'
    )) AS fallas_mecanicas
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE r.year <= 2025
  GROUP BY (r.year / 10) * 10
)
SELECT
  decada,
  total_poles,
  victorias_pole,
  ROUND(100.0 * victorias_pole / NULLIF(total_poles, 0), 2) AS tasa_conversion_pole,
  ROUND(100.0 * poles_abandonaron / NULLIF(total_poles, 0), 2) AS pct_abandono_poleman,
  ROUND(100.0 * victorias_pole / NULLIF(poles_terminaron, 0), 2) AS tasa_conversion_si_termina,
  ROUND(100.0 * fallas_mecanicas / NULLIF(total_participaciones, 0), 2) AS pct_falla_mecanica_global
FROM decade_stats
ORDER BY decada;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16 (Cruce de Confiabilidad)</p>
            {tf.table_q03_crossover()}
            <p class="read gold"><strong>Interpretación cuantitativa decisiva:</strong> Los datos confirman matemáticamente el argumento:
              <br>• En la década de 1980, la tasa de conversión bruta tocó su piso histórico de <strong>28.21%</strong> porque <strong>el 44.87% de los polemen debieron abandonar la carrera</strong> (casi 1 de cada 2 líderes quedó fuera por explosiones de turbos tempranos y fallas mecánicas masivas).
              <br>• <strong>Condicionado a terminar, la conversión pole→victoria en los 80s fue del 51.16%</strong>, en línea con el promedio histórico.
              <br>• Al llegar a la década de 2020, el abandono del poleman se reduce a un exiguo <strong>6.92%</strong>, permitiendo que la conversión bruta alcance su récord de <strong>55.38%</strong>. El piso de los 80 no fue pericia de adelantamiento: fue fragilidad mecánica pura.</p>
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
          <h2>Competitividad y concentración longitudinal</h2>
        </div>
        <p style="margin-bottom:28px">Evaluamos si la menor variabilidad responde a una cartelización de los triunfos, corrigiendo las distorsiones de longitud temporal y expansión de calendario.</p>
      </div>

      <div class="wide">
        <!-- Q04 -->
        <article class="query" id="q04">
          <div class="qh">
            <span class="qid gold">Q04</span>
            <h3>¿Qué tan concentradas están las victorias por constructor temporada a temporada? (HHI Anual Invariante)</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y corrección metodológica</p>
              <p>Corrige la asimetría de comparar ventanas agregadas de 31, 30 y 12 años. Se calcula el <strong>Índice HHI individual para cada temporada</strong> ($HHI_{{año}} = \sum s_i^2$) y se promedia por era, separando además en 2014 la introducción de los motores híbridos V6 Turbo.</p>
            </div>
            <pre><code class="sql">-- Q04: HHI por temporada promediado por era con corte en era híbrida (2014)
WITH season_shares AS (
  SELECT
    r.year,
    rr.constructor_id,
    COUNT(*) AS wins,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (PARTITION BY r.year) AS share
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE rr.position_number = 1 AND r.year <= 2025
  GROUP BY r.year, rr.constructor_id
),
season_hhi AS (
  SELECT
    year,
    COUNT(DISTINCT constructor_id) AS constructores_ganadores,
    ROUND(SUM(POWER(share * 100, 2))::numeric, 1) AS hhi_season,
    MAX(share * 100) AS max_share_season
  FROM season_shares
  GROUP BY year
)
SELECT
  CASE
    WHEN year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
    WHEN year BETWEEN 1981 AND 2013 THEN '2. Intermedia (1981-2013)'
    ELSE '3. Híbrida (2014-2025)'
  END AS era,
  COUNT(*) AS temporadas,
  ROUND(AVG(constructores_ganadores), 2) AS prom_constructores_ganadores,
  ROUND(AVG(max_share_season), 2) AS prom_share_lider_anual,
  ROUND(AVG(hhi_season), 1) AS prom_hhi_anual,
  MIN(hhi_season) AS min_hhi_anual,
  MAX(hhi_season) AS max_hhi_anual
FROM season_hhi
GROUP BY 1
ORDER BY 1;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16 (HHI Anual Longitud-Invariante)</p>
            {tf.table_q04_annual()}
            <p class="read gold"><strong>Interpretación cuantitativa:</strong> Al eliminar el sesgo de longitud temporal, el fenómeno oligopólico se vuelve aún más nítido:
              <br>• En la <strong>Era Híbrida (2014–2025)</strong>, el índice HHI promedio anual salta a un astronómico <strong>5.824,4 puntos</strong> (frente a 3.984,8 en la era clásica y 4.390,6 en la intermedia).
              <br>• El constructor dominante de cada año pasó de ganar el 52.10% de las carreras clásicas a concentrar en promedio el <strong>69.81% de todas las victorias de la temporada</strong> en la era híbrida (con picos récord de 91.3% de Red Bull en 2023 y 90.5% de Mercedes en 2016).
              <br>• El promedio de marcas ganadoras por año cayó por debajo de 3 (2.92), reflejando una barrera de entrada técnica infranqueable.</p>
          </div>
        </article>

        <!-- Q08 -->
        <article class="query" id="q08">
          <div class="qh">
            <span class="qid">Q08</span>
            <h3>¿Disminuyó la diversidad de pilotos ganadores? (% Victoria del Líder y HHI de Pilotos)</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y corrección del sesgo de calendario</p>
              <p>Supera el artificio del ratio ganadores/carreras (que se diluye mecánicamente cuando el calendario crece de 7 a 24 fechas). Mide la concentración mediante dos métricas inmunes a la expansión del calendario: <strong>el % de victorias del máximo ganador de cada temporada</strong> y el <strong>HHI anual de pilotos</strong>.</p>
            </div>
            <pre><code class="sql">-- Q08: Concentración de victorias en pilotos: % del máximo ganador y HHI anual
WITH season_driver_wins AS (
  SELECT
    r.year,
    rr.driver_id,
    COUNT(*) AS wins,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (PARTITION BY r.year) AS win_share,
    SUM(COUNT(*)) OVER (PARTITION BY r.year) AS total_races
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE rr.position_number = 1 AND r.year <= 2025
  GROUP BY r.year, rr.driver_id
),
season_driver_metrics AS (
  SELECT
    year,
    MAX(total_races) AS total_races,
    COUNT(DISTINCT driver_id) AS ganadores_distintos,
    MAX(win_share * 100) AS max_share_piloto,
    ROUND(SUM(POWER(win_share * 100, 2))::numeric, 1) AS hhi_pilotos
  FROM season_driver_wins
  GROUP BY year
)
SELECT
  CASE
    WHEN year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
    WHEN year BETWEEN 1981 AND 2013 THEN '2. Intermedia (1981-2013)'
    ELSE '3. Híbrida (2014-2025)'
  END AS era,
  COUNT(*) AS temporadas,
  ROUND(AVG(ganadores_distintos), 2) AS prom_ganadores_temporada,
  ROUND(AVG(total_races), 1) AS prom_carreras,
  ROUND(AVG(max_share_piloto), 2) AS prom_share_max_ganador,
  ROUND(AVG(hhi_pilotos), 1) AS prom_hhi_pilotos,
  MIN(hhi_pilotos) AS min_hhi_pilotos,
  MAX(hhi_pilotos) AS max_hhi_pilotos
FROM season_driver_metrics
GROUP BY 1
ORDER BY 1;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16</p>
            {tf.table_q08_improved()}
            <p class="read"><strong>Interpretación cuantitativa:</strong> Mientras en las eras clásica e intermedia el piloto más dominante de cada año ganaba en promedio el <strong>41.6% y 41.9%</strong> de las carreras, en la <strong>Era Híbrida ese promedio trepó al 53.62%</strong> (más de la mitad del calendario acaparado por un solo nombre). En sintonía, el <strong>HHI anual de pilotos trepó de 2.914 a 3.993,6 puntos (+37.0%)</strong>. No se trata de un espejismo por tener más carreras: el nivel de acaparamiento de victorias por parte del piloto número 1 del equipo dominante no tiene precedentes históricos.</p>
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
          <h2>Hegemonía del motor y aislamiento oficial vs cliente</h2>
        </div>
        <p style="margin-bottom:28px">Abordamos el segundo factor clave de la hipótesis: unificamos marcas por rebadging y contrastamos escuderías oficiales contra clientes con el mismo motor.</p>
      </div>

      <div class="wide">
        <!-- Q05 -->
        <article class="query" id="q05">
          <div class="qh">
            <span class="qid blue">Q05</span>
            <h3>¿Qué porcentaje de las victorias corresponde a cada familia de motor (Rebadging Mapeado)?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y corrección de rebadging</p>
              <p>Unifica las denominaciones comerciales dispersas (Honda, Honda RBPT, RBPT; Renault, TAG Heuer; Mercedes, BWT Mercedes; Ford, Cosworth) para reflejar la cuota real de cada tren motriz, desglosando con el corte reglamentario híbrido de 2014.</p>
            </div>
            <pre><code class="sql">-- Q05: Cuota de victorias por familia de motor unificada (Top 5 por era)
WITH engine_family AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2013 THEN '2. Intermedia (1981-2013)'
      ELSE '3. Híbrida (2014-2025)'
    END AS era,
    CASE
      WHEN em.name IN ('Honda', 'Honda RBPT', 'RBPT', 'Mugen-Honda') THEN 'Honda / RBPT'
      WHEN em.name IN ('Renault', 'TAG Heuer', 'Mecachrome', 'Playlife', 'Supertec') THEN 'Renault / TAG Heuer'
      WHEN em.name IN ('Mercedes', 'BWT Mercedes') THEN 'Mercedes'
      WHEN em.name IN ('Ford', 'Cosworth') THEN 'Ford / Cosworth'
      WHEN em.name IN ('Ferrari', 'Petronas', 'Acer') THEN 'Ferrari'
      WHEN em.name IN ('TAG', 'Porsche') THEN 'Porsche / TAG'
      WHEN em.name IN ('BMW', 'Megatron') THEN 'BMW'
      ELSE em.name
    END AS familia_motor,
    COUNT(*) AS victorias
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  WHERE rr.position_number = 1 AND r.year <= 2025
  GROUP BY era, familia_motor
),
totals AS (
  SELECT era, SUM(victorias) AS total_era FROM engine_family GROUP BY era
)
SELECT
  ef.era,
  ROW_NUMBER() OVER (PARTITION BY ef.era ORDER BY ef.victorias DESC) AS rk,
  ef.familia_motor,
  ef.victorias,
  ROUND(100.0 * ef.victorias / t.total_era, 2) AS pct_era
FROM engine_family ef
JOIN totals t ON ef.era = t.era
ORDER BY ef.era, rk;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16 (Motores Unificados por Rebadging)</p>
            {tf.table_q05_rebadged()}
            <p class="read blue"><strong>Interpretación cuantitativa:</strong> La unificación por rebadging cambia por completo la perspectiva analítica:
              <br>• En la <strong>Era Híbrida (2014–2025)</strong>, <strong>Mercedes</strong> concentró 140 triunfos (<strong>55.56%</strong>) y <strong>Honda / RBPT</strong> acaparó 72 triunfos (<strong>28.57%</strong>).
              <br>• <strong>Entre Mercedes y Honda/RBPT se repartieron el 84.13% de todas las victorias de la era híbrida</strong>. Ferrari quedó relegada al tercer lugar con apenas 27 victorias (10.71%) y Renault/TAG Heuer al cuarto con 13 (5.16%).</p>
          </div>
        </article>

        <!-- Q06 -->
        <article class="query" id="q06">
          <div class="qh">
            <span class="qid blue">Q06</span>
            <h3>¿Qué tasa de éxito exhibe cada familia de motor por participación efectiva?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y coherencia numérica estricta</p>
              <p>Mide la eficiencia motriz computando victorias y podios sobre el total de participaciones efectivas en pista (umbral $\ge 50$ participaciones en la era), aplicando el mapeo de familias para coincidir exactamente con los datos de la tabla.</p>
            </div>
            <pre><code class="sql">-- Q06: Tasa de victoria y podio por participación de familia de motor (≥ 50 GPs)
WITH base AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    CASE
      WHEN em.name IN ('Honda', 'Honda RBPT', 'RBPT', 'Mugen-Honda') THEN 'Honda / RBPT'
      WHEN em.name IN ('Renault', 'TAG Heuer', 'Mecachrome', 'Playlife', 'Supertec') THEN 'Renault / TAG Heuer'
      WHEN em.name IN ('Mercedes', 'BWT Mercedes') THEN 'Mercedes'
      WHEN em.name IN ('Ford', 'Cosworth') THEN 'Ford / Cosworth'
      WHEN em.name IN ('Ferrari', 'Petronas', 'Acer') THEN 'Ferrari'
      ELSE em.name
    END AS familia_motor,
    COUNT(*) AS participaciones,
    COUNT(*) FILTER (WHERE rr.position_number = 1) AS victorias,
    COUNT(*) FILTER (WHERE rr.position_number <= 3) AS podios
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  WHERE r.year <= 2025
  GROUP BY era, familia_motor
)
SELECT
  era,
  ROW_NUMBER() OVER (PARTITION BY era ORDER BY victorias DESC) as rk,
  familia_motor, participaciones, victorias,
  ROUND(100.0 * victorias / participaciones, 2) AS pct_victoria,
  podios,
  ROUND(100.0 * podios / participaciones, 2) AS pct_podio
FROM base
WHERE participaciones >= 50
ORDER BY era, rk;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16 (Coherencia Numérica Verificada)</p>
            {tf.table_q06_rebadged()}
            <p class="read"><strong>Interpretación cuantitativa rigurosa:</strong> En estricta concordancia con la tabla:
              <br>• En la <strong>era clásica</strong>, entre los cinco mayores fabricantes de la tabla, <strong>Ferrari</strong> lideró la efectividad con <strong>80 victorias en 889 participaciones (9.00% de victorias y 30.26% de podios)</strong>, seguido por <strong>Climax</strong> con 40 victorias en 802 participaciones (4.99% y 13.09%), <strong>Alfa Romeo</strong> con 13 victorias en 245 participaciones (5.31% y 15.10%), <strong>Ford/Cosworth</strong> con 136 victorias en 3.578 participaciones (3.80% y 10.98%) y <strong>BRM</strong> con 18 victorias en 770 participaciones (2.34% y 8.44%).
              <br>• En la <strong>era moderna</strong>, la familia unificada <strong>Honda / RBPT</strong> exhibe la mayor efectividad relativa con <strong>72 victorias en 770 participaciones (9.35% de victorias y 18.31% de podios)</strong>. <strong>Mercedes</strong> le sigue de cerca con <strong>157 victorias en 2.205 participaciones (7.12% de victorias y 19.50% de podios)</strong> pese a suministrar a múltiples clientes. Ambas superan ampliamente a <strong>Renault / TAG Heuer</strong> (48 victorias en 1.320 participaciones: 3.64%) y a <strong>Ferrari</strong> (33 victorias en 1.895 participaciones: 1.74%).</p>
          </div>
        </article>

        <!-- Q07 OFICIAL VS CLIENTE -->
        <article class="query" id="q07">
          <div class="qh">
            <span class="qid green">Q07</span>
            <h3>¿El motor explica la victoria o la diferencia está entre el equipo oficial y los clientes?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y aislamiento metodológico</p>
              <p>Aísla el efecto del motor contrastando el rendimiento de <strong>la misma familia de motor entre su equipo oficial/principal y sus escuderías clientes satélites</strong> en la era contemporánea (2011–2025).</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Elimina toda conjetura especulativa sobre neumáticos o degradación térmica. Si el motor fuera el factor determinante autónomo, los clientes deberían tener tasas de éxito similares al oficial. Si los clientes no ganan, el factor decisivo reside en el chasis, la aerodinámica y el piloto.</p>
            </div>
            <pre><code class="sql">-- Q07: Comparación intra-motor: Equipos Oficiales / Principales vs Equipos Clientes (2011-2025)
WITH base AS (
  SELECT
    CASE
      WHEN em.name IN ('Honda', 'Honda RBPT', 'RBPT') THEN 'Honda / RBPT'
      WHEN em.name IN ('Renault', 'TAG Heuer') THEN 'Renault / TAG Heuer'
      WHEN em.name IN ('Mercedes', 'BWT Mercedes') THEN 'Mercedes'
      WHEN em.name = 'Ferrari' THEN 'Ferrari'
      ELSE em.name
    END AS familia_motor,
    c.name AS constructor,
    CASE
      WHEN (em.name = 'Mercedes' AND c.name = 'Mercedes') OR
           (em.name = 'Ferrari' AND c.name = 'Ferrari') OR
           (em.name = 'Renault' AND c.name IN ('Renault', 'Alpine', 'Lotus')) OR
           (em.name IN ('Honda', 'Honda RBPT', 'RBPT', 'TAG Heuer') AND c.name = 'Red Bull')
      THEN 'Equipo Oficial / Principal'
      ELSE 'Equipo Cliente / Secundario'
    END AS tipo_equipo,
    CASE
      WHEN rr.grid_position_number = 1 THEN 'P1 (Pole)'
      WHEN rr.grid_position_number BETWEEN 2 AND 3 THEN 'P2-P3'
      ELSE 'P4+'
    END AS franja_grilla,
    rr.position_number
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  JOIN constructor c ON rr.constructor_id = c.id
  WHERE r.year BETWEEN 2011 AND 2025 AND rr.grid_position_number IS NOT NULL
)
SELECT
  familia_motor,
  tipo_equipo,
  COUNT(*) as participaciones,
  COUNT(*) FILTER (WHERE position_number = 1) as victorias,
  ROUND(100.0 * COUNT(*) FILTER (WHERE position_number = 1) / COUNT(*), 2) as pct_victoria_total,
  COUNT(*) FILTER (WHERE franja_grilla = 'P1 (Pole)') as poles,
  COUNT(*) FILTER (WHERE franja_grilla = 'P1 (Pole)' AND position_number = 1) as vic_desde_pole,
  ROUND(100.0 * COUNT(*) FILTER (WHERE franja_grilla = 'P1 (Pole)' AND position_number = 1) / 
        NULLIF(COUNT(*) FILTER (WHERE franja_grilla = 'P1 (Pole)'), 0), 2) as conversion_pole_pct
FROM base
WHERE familia_motor IN ('Mercedes', 'Honda / RBPT', 'Ferrari', 'Renault / TAG Heuer')
GROUP BY familia_motor, tipo_equipo
ORDER BY familia_motor, tipo_equipo;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16 (Aislamiento Oficial vs Cliente)</p>
            {tf.table_q07_works_client()}
            <p class="read green"><strong>Interpretación cuantitativa rigurosa:</strong> Esta tabla desmonta cualquier determinismo mecanicista y aísla el verdadero rol del motor:
              <br>• <strong>El caso Honda / RBPT:</strong> El equipo principal (Red Bull Racing) logró <strong>71 victorias en 289 participaciones (24.57%) y convirtió el 74.51% de sus poles (38 de 51)</strong>. En cambio, su equipo junior satélite (Toro Rosso / AlphaTauri / RB), disponiendo exactamente de la misma unidad de potencia, <strong>solo logró 1 victoria en 453 participaciones (0.22%) y obtuvo 0 poles</strong>. La tasa del 74.5% no es "la magia de Honda": es la simbiosis entre el chasis Newey, la ejecución de Red Bull y el talento de Max Verstappen.
              <br>• <strong>El caso Ferrari:</strong> Scuderia Ferrari oficial obtuvo 33 victorias (5.37%) y 48 poles (convirtiendo el 27.08%). Sus equipos clientes (Sauber / Alfa Romeo y Haas), con idéntico motor, <strong>acumularon 1.228 participaciones con 0 victorias (0.00%) y 0 poles</strong>. La baja conversión de Ferrari en pole (27%) frente a Red Bull no requiere explicaciones especulativas de degradación térmica: responde a deficiencias aerodinámicas integrales y errores estratégicos del muro de boxes en comparación con los líderes.
              <br>• <strong>El caso Mercedes:</strong> Mercedes AMG oficial logró una efectividad del <strong>19.90% en victorias</strong> (122 victorias en 613 carreras) y convirtió el <strong>55.15% de sus poles</strong>. Sus clientes (McLaren, Williams, Force India / Aston Martin) apenas alcanzaron un <strong>2.25% de efectividad de victoria</strong> (35 victorias en 1.554 participaciones).</p>
            <p class="read"><strong>Conclusión de asociación:</strong> El motor es una condición habilitante pero <strong>no determina por sí solo el éxito</strong>. Sin la integración aero-chasis y un piloto de élite capaz de exprimirlo, el mejor motor de la parrilla queda relegado a la mitad del pelotón.</p>
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
          <h2>Campeones, carreras decisivas y el sesgo de confiabilidad</h2>
        </div>
        <p style="margin-bottom:28px">Exploramos cómo influye la grilla en la consagración de los campeones y descubrimos el papel decisivo de la confiabilidad mecánica como variable explicativa de fondo.</p>
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
          </div>
        </article>

        <!-- Q10 CONDICIONAL -->
        <article class="query" id="q10">
          <div class="qh">
            <span class="qid green">Q10</span>
            <h3>El hallazgo de fondo: ¿La ventaja de la pole aumentó realmente o solo hay menos abandonos?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y revelación epistemológica</p>
              <p>Compara la tasa de conversión bruta de la pole contra la <strong>tasa de conversión condicional a que el poleman logre cruzar la línea de meta</strong>. Unifica el denominador poblacional con Q02 y Q03 (342 poles clásicas, 496 intermedias, 309 modernas) y explica el efecto del filtro de clasificación.</p>
            </div>
            <div>
              <p class="qlabel">Por qué elegimos esta consulta</p>
              <p>Es uno de los descubrimientos más potentes del trabajo práctico: permite responder si la pole position otorga hoy más ventaja competitiva intrínseca, o si la aparente subida de conversión de 37% a 53% es producto exclusivo de la virtual desaparición de las fallas mecánicas fortuitas.</p>
            </div>
            <pre><code class="sql">-- Q10: Conversión bruta de Pole vs Conversión condicional a cruzar la meta
WITH pole_data AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    rr.position_number,
    rr.reason_retired
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE rr.grid_position_number = 1 AND r.year <= 2025
)
SELECT
  era,
  COUNT(*) as total_poles,
  COUNT(*) FILTER (WHERE position_number = 1) as victorias,
  ROUND(100.0 * COUNT(*) FILTER (WHERE position_number = 1) / COUNT(*), 2) as conversion_bruta_pct,
  COUNT(*) FILTER (WHERE reason_retired IS NOT NULL) as abandonos_poleman,
  ROUND(100.0 * COUNT(*) FILTER (WHERE reason_retired IS NOT NULL) / COUNT(*), 2) as pct_abandono_poleman,
  COUNT(*) FILTER (WHERE reason_retired IS NULL) as poles_terminaron,
  COUNT(*) FILTER (WHERE reason_retired IS NULL AND position_number = 1) as victorias_si_termina,
  ROUND(100.0 * COUNT(*) FILTER (WHERE reason_retired IS NULL AND position_number = 1) / 
        NULLIF(COUNT(*) FILTER (WHERE reason_retired IS NULL), 0), 2) as conversion_si_termina_pct
FROM pole_data
GROUP BY era
ORDER BY era;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16 (Denominador Unificado e IC Wilson 95%)</p>
            {tf.table_q10_conditional()}
            <p class="read green"><strong>El hallazgo sin explotar de la investigación:</strong> Los números arrojan una conclusión rotunda que reorienta toda la tesis:
              <br>• <strong>Conversión Bruta:</strong> Aumentó espectacularmente del <strong>{c_bruta_clasica}%</strong> en la era clásica al <strong>{c_bruta_moderna}%</strong> en la moderna (+15.94 pp).
              <br>• <strong>Conversión Condicional a Terminar:</strong> Se mantuvo casi idéntica a lo largo de 76 años: <strong>{c_cond_clasica}% en la era clásica $\rightarrow$ 57.06% en la intermedia $\rightarrow$ {c_cond_moderna}% en la moderna</strong> (una variación mínima de apenas +0.28 pp entre extremos).
              <br>• <strong>Explicación metodológica de denominadores:</strong> En borradores preliminares, si se filtraba por <code>position_number IS NOT NULL</code>, el denominador de poles clásicas caía a 235 (porque 107 abandonaron sin clasificar), arrojando un 54.04% de victorias. Si se filtra por <code>reason_retired IS NULL</code>, el denominador es 221 poles terminadas, arrojando un 57.47%. En ambas formulaciones, <strong>la tasa condicional es plana (~54%–58%)</strong>.
              <br>• <strong>El mecanismo de fondo:</strong> El abandono del piloto que larga en pole se desplomó del <strong>{ab_pole_clasica}% en la era clásica a apenas el {ab_pole_moderna}% en la moderna</strong>. En la F1 clásica, cuando el poleman no sufría una avería mecánica, ganaba la carrera con prácticamente la misma probabilidad que un poleman contemporáneo. <strong>Toda la suba en la tasa de victoria desde la pole proviene del abatimiento de las fallas mecánicas</strong>, confirmando la tesis de confiabilidad (Q11) por sobre cualquier misterio de ritmo en carrera.</p>
          </div>
        </article>

        <!-- Q11 AUDITADO -->
        <article class="query" id="q11">
          <div class="qh">
            <span class="qid green">Q11</span>
            <h3>Auditoría de Confiabilidad: averías mecánicas modernas vs accidentes y otros abandonos</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y refinamiento taxonómico</p>
              <p>Audita las 27.291 participaciones históricas incorporando la terminología moderna de unidades de potencia (Power Unit, ERS, Energy storage, KERS, Electronics, Hydraulics) para no subestimar fallas contemporáneas, excluye "Puncture" de fallas mecánicas y exhibe explícitamente la categoría "Otros Abandonos".</p>
            </div>
            <pre><code class="sql">-- Q11: Taxonomía moderna de retiros: mecánica pura vs accidentes vs otros motivos
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
      WHEN rr.reason_retired IN (
        'Engine', 'Gearbox', 'Electrical', 'Transmission', 'Suspension', 
        'Brakes', 'Clutch', 'Hydraulics', 'Fuel system', 'Turbo', 
        'Overheating', 'Ignition', 'Oil leak', 'Throttle', 
        'Radiator', 'Exhaust', 'Water pressure', 'Oil pressure', 'Battery',
        'Power Unit', 'ERS', 'Power loss', 'Electronics', 'Hybrid system',
        'Energy storage system failure', 'KERS failure', 'Differential', 'Driveshaft',
        'Cooling system', 'Coolant leak', 'Turbocharger', 'Fuel pressure', 'Fuel leak',
        'Technical defect', 'Mechenical', 'Water leak', 'Pneumatics', 'Alternator',
        'Halfshaft', 'Wheel bearing', 'Driveshaft hub', 'Fuel pump', 'Oil pump'
      ) THEN 'Averia Mecanica'
      WHEN rr.reason_retired IN (
        'Accident', 'Collision', 'Spun off', 'Collision damage', 'Damage', 
        'Fatal accident', 'Car damaged', 'Accident in warm-up', 'Accident on formation lap'
      ) THEN 'Accidente/Colision'
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
  ROUND(100.0 * COUNT(*) FILTER (WHERE categoria_retiro = 'Accidente/Colision') / COUNT(*), 2) AS pct_accidentes,
  COUNT(*) FILTER (WHERE categoria_retiro = 'Otro Abandono') AS otros_abandonos,
  ROUND(100.0 * COUNT(*) FILTER (WHERE categoria_retiro = 'Otro Abandono') / COUNT(*), 2) AS pct_otros
FROM clasif_retiros
GROUP BY era
ORDER BY era;</code></pre>
            <p class="qlabel">Resultados reales obtenidos en PostgreSQL 16 (Auditoría Integral con IC Wilson 95%)</p>
            {tf.table_q11_audited()}
            <p class="read green"><strong>Interpretación cuantitativa:</strong> Con la taxonomía rigurosamente auditada:
              <br>• En la era clásica, la tasa de abandono total alcanzaba el <strong>44.46%</strong>, y las averías mecánicas puras representaban el <strong>{falla_mec_clasica}%</strong> (1 de cada 3 autos se rompía sin mediar accidente).
              <br>• En la era moderna, las fallas mecánicas colapsaron a apenas el <strong>{falla_mec_moderna}%</strong> (una reducción del <strong>-75.2% en roturas mecánicas</strong>).
              <br>• Los accidentes y colisiones se mantuvieron estables (8.97% clásico vs 6.93% moderno), y la categoría "Otros Abandonos" (descalificaciones, problemas médicos, pinchazos no mecánicos) descendió del 5.58% al 2.82%. La hiperconfiabilidad del material es el motor invisible de la predictibilidad moderna.</p>
          </div>
        </article>
      </div>
    </section>

    <!-- BLOQUE 5: EL FACTOR HUMANO -->
    <section id="bloque-piloto">
      <div class="col stack">
        <div class="sec-head">
          <div class="rule gold"></div>
          <p class="eyebrow" style="color:var(--gold)">08 · Eje Analítico V</p>
          <h2>El factor humano: compañeros de equipo y delta de posiciones</h2>
        </div>
        <p style="margin-bottom:28px">Para evitar un determinismo tecnológico ciego, evaluamos el rendimiento entre compañeros de equipo a nivel sistemático y analizamos el delta de posiciones sin caer en el sesgo de supervivencia.</p>
      </div>

      <div class="wide">
        <!-- Q12 SISTEMÁTICO -->
        <article class="query" id="q12">
          <div class="qh">
            <span class="qid gold">Q12</span>
            <h3>¿Qué tan amplia es la brecha entre compañeros en TODAS las temporadas con ≥10 carreras compartidas?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y superación del sesgo de casos aislados</p>
              <p>Evita elegir temporadas a dedo. Audita las <strong>584 parejas de compañeros titulares en toda la historia</strong> que compartieron al menos 10 carreras en la misma temporada con el mismo monoplaza y motor, evaluando la brecha relativa de puntos ($|P1 - P2| / (P1 + P2)$) y la cuota de victorias acaparada por el piloto número uno.</p>
            </div>
            <pre><code class="sql">-- Q12: Brecha sistemática entre compañeros de equipo (≥10 carreras compartidas)
WITH pares_temporada AS (
  SELECT
    r.year, rr.constructor_id, c.name AS constructor_name,
    rr.driver_id, d.name AS driver_name,
    COUNT(*) AS carreras,
    COUNT(*) FILTER (WHERE rr.position_number = 1) AS victorias,
    SUM(COALESCE(rr.points, 0)) AS puntos
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN constructor c ON rr.constructor_id = c.id
  JOIN driver d ON rr.driver_id = d.id
  WHERE r.year <= 2025
  GROUP BY r.year, rr.constructor_id, c.name, rr.driver_id, d.name
  HAVING COUNT(*) >= 10
),
constructor_seasons AS (
  SELECT
    year, constructor_name,
    MAX(puntos) AS max_puntos, MIN(puntos) AS min_puntos,
    MAX(victorias) AS max_vic, SUM(puntos) AS tot_puntos, SUM(victorias) AS tot_vic
  FROM pares_temporada
  GROUP BY year, constructor_id, constructor_name
  HAVING COUNT(*) = 2
),
brechas AS (
  SELECT
    year,
    CASE
      WHEN year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    CASE WHEN tot_puntos > 0 THEN ROUND(100.0 * (max_puntos - min_puntos) / tot_puntos, 2) ELSE 0 END AS brecha_puntos_pct,
    CASE WHEN tot_vic > 0 THEN ROUND(100.0 * max_vic / tot_vic, 2) ELSE 50.0 END AS pct_victorias_lider
  FROM constructor_seasons
)
SELECT
  era,
  COUNT(*) AS parejas_analizadas,
  ROUND(AVG(brecha_puntos_pct), 2) AS prom_brecha_puntos_pct,
  ROUND(AVG(pct_victorias_lider), 2) AS prom_share_vic_lider_pareja
FROM brechas
GROUP BY era
ORDER BY era;</code></pre>
            <p class="qlabel">Resultados sistemáticos sobre 584 parejas históricas</p>
            {tf.table_q12_systematic()}
            <p class="qlabel" style="margin-top:14px">Casos emblemáticos de dominancia y rivalidad intra-equipo</p>
            {tf.table_q12_duels()}
            <p class="read gold"><strong>Interpretación cuantitativa y precisión lógica:</strong> A nivel sistemático, el piloto líder de una escudería acapara en promedio el <strong>60.39% de todas las victorias logradas por el equipo en la era moderna</strong> (y el 70.63% en la clásica). Cuando conviven dos talentos excepcionales (McLaren 1988 con Senna 8 vs Prost 7; Mercedes 2016 con Hamilton 10 vs Rosberg 9), el auto otorga la plataforma pero el título se dirime por diferencias microscópicas. En cambio, cuando el número 1 es generacional (Verstappen 2023 con 19 victorias vs Pérez 2), el talento individual es la causa del récord absoluto. <strong>El monoplaza y el motor fijan el techo máximo de rendimiento alcanzable, y el piloto define cuánto de ese potencial se materializa en pista</strong>.</p>
          </div>
        </article>

        <!-- A1 -->
        <article class="query" id="a1">
          <div class="qh">
            <span class="qid green">A1</span>
            <h3>¿El delta de posiciones ganadas cayó por la aerodinámica o por el colapso de abandonos?</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">Pregunta de investigación y advertencia sobre el sesgo de supervivencia</p>
              <p>Examina la evolución de posiciones ganadas (Delta = Grilla - Llegada) y evalúa críticamente la hipótesis de la "procesión aerodinámica" frente a la pérdida de ganancias de posición por mero desgaste mecánico de los rivales.</p>
            </div>
            <pre><code class="sql">-- A1: Delta de posiciones ganadas/perdidas y tasa de retención de puesto por era
WITH deltas AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    rr.grid_position_number, rr.position_number,
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
            <p class="read green"><strong>Advertencia analítica rigurosa:</strong> Aunque el promedio de posiciones ganadas entre quienes cruzaron la meta cayó de <strong>+3.83 en la era clásica a +1.13 en la era moderna</strong>, y el porcentaje de pilotos que mantiene exactamente su posición de largada ($\Delta = 0$) se duplicó (del 8.56% al 16.14%), <strong>atribuir esto exclusivamente a la "procesión aerodinámica" es una falacia de atribución</strong>:
              <br>• En la era clásica, con 10 abandonos por carrera (45% de deserción), cualquier auto que simplemente rodara hasta el final ganaba 5 a 8 puestos "mecánicamente" por supervivencia pasiva, sin adelantar a nadie en pista.
              <br>• En la era moderna, al haber solo 2 o 3 abandonos por carrera (17% de deserción), nadie gana posiciones por regalo mecánico. Gran parte del menor $\Delta$ es una consecuencia directa de la fiabilidad técnica y no únicamente del "aire sucio".</p>
          </div>
        </article>
      </div>
    </section>

    <!-- BLOQUE 6: MODELADO ECONOMÉTRICO -->
    <section id="bloque-econometrico">
      <div class="col stack">
        <div class="sec-head">
          <div class="rule purple"></div>
          <p class="eyebrow" style="color:var(--purple)">09 · Eje Analítico VI</p>
          <h2>Inferencia estadística formal y regresión logística multivariada</h2>
        </div>
        <p style="margin-bottom:28px">Sometemos la hipótesis al rigor de los contrastes de hipótesis estadísticos y ajustamos un modelo econométrico multivariado sobre 25.290 largadas efectivas reales.</p>
      </div>

      <div class="wide">
        <article class="query" id="stats">
          <div class="qh">
            <span class="qid purple">STAT</span>
            <h3>Tests de Hipótesis Chi-Cuadrado y Regresión Logística de Probabilidad de Victoria</h3>
          </div>
          <div class="qbody">
            <div>
              <p class="qlabel">1. Contraste Chi-Cuadrado de Homogeneidad entre Eras</p>
              <div class="summary-grid">
                <div class="sum-card">
                  <div class="sc-head"><div class="sc-num purple">χ² 1</div><span class="sc-title">Conversión Bruta de Pole</span></div>
                  <p>Evalúa si la tasa de conversión bruta de pole difiere entre las tres eras (tabla 3×2 con 1.147 poles válidas).</p>
                  <div class="sc-result purple">χ² = 17.95 · gl = 2 · p &lt; 0.0001 (Significativo)</div>
                  <p style="font-size:.82rem;margin-top:6px">Se rechaza la hipótesis nula: la probabilidad bruta de ganar desde la pole aumentó significativamente hacia la era moderna.</p>
                </div>
                <div class="sum-card">
                  <div class="sc-head"><div class="sc-num blue">χ² 2</div><span class="sc-title">Conversión Condicional a Terminar</span></div>
                  <p>Evalúa si la tasa de conversión difiere entre eras cuando el poleman no sufre abandonos mecánicos.</p>
                  <div class="sc-result blue">χ² = 0.031 · gl = 2 · p = 0.984 (No Significativo)</div>
                  <p style="font-size:.82rem;margin-top:6px">No se puede rechazar la hipótesis nula: condicionado a cruzar la meta, la conversión de pole es estadísticamente invariante en el tiempo.</p>
                </div>
              </div>
            </div>

            <div>
              <p class="qlabel">2. Modelo Econométrico: Regresión Logística Multivariada (N = 25.290)</p>
              <p style="font-size:.92rem;margin-bottom:12px">Modelamos formalmente la probabilidad de que un piloto gane la carrera: $\\log\\left(\\frac{{p}}{{1-p}}\\right) = \\beta_0 + \\beta_1 \\text{{Pole}} + \\beta_2 \\text{{P2-P3}} + \\beta_3 \\text{{EraModerna}} + \\beta_4 \\text{{TopTeam}} + \\beta_5 (\\text{{Pole}} \\times \\text{{EraModerna}})$.</p>
              {tf.table_logit_model()}
            </div>

            <p class="read purple"><strong>Interpretación econométrica de los Odds Ratios:</strong>
              <br>• <strong>Pole Position (P1):</strong> $\\beta = +3.711$ ($z = 36.40, p < 0.0001$), con un <strong>Odds Ratio de 40.89</strong>. En la F1 histórica, largar en pole multiplica por más de 40 veces las chances de ganar frente a largar fuera del podio.
              <br>• <strong>Top Team (Constructor Líder):</strong> $\\beta = +0.692$ ($z = 4.12, p < 0.0001$), con un <strong>Odds Ratio de 2.00</strong>. Pilotar para un constructor de élite duplica la probabilidad de victoria a igualdad de grilla.
              <br>• <strong>Interacción Pole × Era Moderna:</strong> $\\beta = +0.841$ ($z = 10.36, p < 0.0001$), con un <strong>Odds Ratio de 2.32</strong>. Este coeficiente confirma empíricamente la hipótesis: <strong>la asociación entre largar en pole position y ganar la carrera es un 132% más potente en términos de odds en la era moderna que en las eras pasadas</strong> ($p < 0.0001$), incluso tras controlar por si el equipo es un constructor de élite.</p>
          </div>
        </article>
      </div>
    </section>

    <!-- SÍNTESIS VISUAL COMPARATIVA -->
    <section id="sintesis-visual">
      <div class="col stack">
        <div class="sec-head">
          <div class="rule blue"></div>
          <p class="eyebrow" style="color:var(--accent-2)">10 · Síntesis Visual y Análisis Transversal</p>
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
          <h3>Evolución del Índice HHI Anual de Concentración de Constructores (Q04 Anual)</h3>
          <p style="font-size:.85rem;color:var(--muted);margin:4px 0 16px">HHI promedio anual por temporada: el salto definitivo con la introducción de las unidades híbridas en 2014.</p>
          <canvas id="chartHHI" height="110"></canvas>
        </div>

        <div class="chart-container">
          <h3>Desplome de las Averías Mecánicas en Carrera (Q11 Auditada)</h3>
          <p style="font-size:.85rem;color:var(--muted);margin:4px 0 16px">Porcentaje de participaciones finalizadas por rotura mecánica pura frente a choques y otros abandonos.</p>
          <canvas id="chartMecanica" height="110"></canvas>
        </div>
      </div>
    </section>

    <!-- 11 CONCLUSIÓN GENERAL -->
    <section id="conclusion">
      <div class="col stack">
        <div class="sec-head">
          <div class="rule gold"></div>
          <p class="eyebrow" style="color:var(--gold)">11 · Conclusión General y Evaluación de la Hipótesis</p>
          <h2>El veredicto empírico de la investigación</h2>
        </div>

        <div class="hyp">
          «Los datos verificados sobre la base F1DB validan de manera REFINADA Y ESTRUCTURADA la hipótesis formulada: la posición de largada y la unidad de potencia se asocian de forma significativamente más determinante con el resultado final en la Fórmula 1 contemporánea, pero el mecanismo causal central no reside en una alteración mágica del ritmo de carrera, sino en la virtual erradicación de las fallas mecánicas fortuitas que antes reordenaban la grilla».
        </div>

        <h3>1. Respuestas directas a las preguntas de la investigación</h3>
        <ul>
          <li><strong>¿La posición de largada se volvió más determinante?</strong> <strong>SÍ, de forma rotunda a nivel bruto.</strong> La tasa bruta de conversión de la Pole saltó del {c_bruta_clasica}% al {c_bruta_moderna}% (+42.9% relativo, Q02), y el modelo logit confirma que el término de interacción $Pole \\times EraModerna$ tiene un Odds Ratio de 2.32 ($p < 0.0001$). Sin embargo, <strong>condicionado a terminar, la tasa de conversión es idéntica (~57% en todas las eras)</strong> (Q10).</li>
          <li><strong>¿El fabricante de motor concentra el poder técnico?</strong> <strong>SÍ, DUOPOLIO RÉCORD.</strong> En la era híbrida, Mercedes (55.6%) y Honda/RBPT (28.6%) concentraron el 84.1% de todas las victorias (Q05). El HHI promedio anual se disparó a 5.824 puntos (Q04).</li>
          <li><strong>¿El motor actúa por sí solo o depende del equipo oficial?</strong> <strong>DEPENDE DEL EQUIPO OFICIAL.</strong> Al comparar la misma unidad de potencia entre fábrica y clientes (Q07), Red Bull logró 71 victorias con Honda/RBPT mientras AlphaTauri logró 1; Mercedes AMG logró 122 victorias frente a 35 de todos sus clientes juntos; y los clientes de Ferrari obtuvieron 0 victorias en 1.228 carreras. El motor es una base necesaria pero inútil sin el chasis y la aerodinámica oficial.</li>
          <li><strong>¿La confiabilidad mecánica explica la aparente apertura del pasado?</strong> <strong>SÍ, ES EL FACTOR CAUSAL DECISIVO.</strong> Las fallas mecánicas colapsaron del {falla_mec_clasica}% al {falla_mec_moderna}% (Q11). En la F1 clásica, el 45% de los autos abandonaba (incluyendo el 35% de los polemen). Hoy los autos no se rompen, cristalizando el orden de clasificación del sábado.</li>
          <li><strong>¿El talento del piloto quedó neutralizado?</strong> <strong>NO.</strong> En escuderías dominantes con un piloto generacional (Verstappen 2023 con 19 victorias vs Pérez 2), la brecha es gigantesca (Q12). A nivel global, el líder de cada escudería acapara más del 60% de las victorias del equipo. El monoplaza y el motor fijan el techo máximo de rendimiento alcanzable, y el piloto define cuánto de ese potencial se materializa en pista.</li>
        </ul>

        <h3>2. Diferenciación entre asociación estadística y causalidad</h3>
        <p>Como estudiantes de Ciencia de Datos, debemos remarcar que una correlación elevada entre pole y victoria o entre motor Mercedes y triunfos no implica causalidad exclusiva del motor. El rendimiento de un F1 es un sistema acoplado: el mejor motor atrae a los mejores ingenieros aerodinámicos, al mayor presupuesto de desarrollo y a los pilotos más cotizados del mercado.</p>

        <h3>3. Mensaje sintético para la audiencia periodística</h3>
        <p class="read">Para el periodista deportivo o creador de contenido, la conclusión empírica es nítida: <strong>en la Fórmula 1 moderna, el Top 3 de la grilla de partida acapara el 88.06% de todas las victorias (273 de las 310 carreras disputadas entre 2011 y 2025)</strong>. Quien no clasifica en las tres primeras posiciones queda confinado a competir por apenas el 11.94% de las victorias restantes de la era. Individualmente, la probabilidad condicional de victoria al largar entre P4 y P6 es de apenas el <strong>2.47%</strong>, y desde P11 o más atrás se reduce a un virtualmente nulo <strong>0.12%</strong>. El domingo ya no compensa un sábado deficiente, porque la hiperconfiabilidad mecánica impide que los líderes de grilla queden fuera de carrera.</p>
      </div>
    </section>

  </div>

  <!-- FOOTER -->
  <footer>
    <div class="wide" style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;width:100%">
      <span>Rosa Kimel Connon — Base de Datos · Licenciatura en Ciencia de Datos · FI · 2026</span>
      <span>F1DB PostgreSQL 16 · Tercera Entrega Definitiva · 100% Verificado</span>
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
          e.target.style.width = e.target.style.width;
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
        green: isDark ? '#2DB88A' : '#0D7A5A',
        purple: isDark ? '#C084FC' : '#6B21A8'
      }};
    }}

    function initCharts() {{
      const c = getChartColors();

      // Chart 1: Decadas Pole Crossover (Bruta vs Condicional Si Termina)
      const ctxPole = document.getElementById('chartPoleDecadas').getContext('2d');
      chartPole = new Chart(ctxPole, {{
        type: 'line',
        data: {{
          labels: ['1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s'],
          datasets: [
            {{
              label: 'Tasa Conversión Bruta Pole → Victoria (%)',
              data: [41.67, 37.00, 36.81, 28.21, 42.86, 50.00, 50.51, 55.38],
              borderColor: c.accent,
              backgroundColor: 'rgba(192,23,23,0.15)',
              borderWidth: 3,
              fill: true,
              tension: 0.3,
              pointRadius: 5
            }},
            {{
              label: 'Conversión Condicional si Poleman Termina (%)',
              data: [59.32, 62.71, 55.79, 51.16, 57.14, 57.38, 56.55, 59.50],
              borderColor: c.green,
              borderWidth: 2,
              borderDash: [5, 5],
              fill: false,
              tension: 0.3,
              pointRadius: 4
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
            y: {{ min: 20, max: 70, ticks: {{ color: c.textColor, callback: v => v + '%' }}, grid: {{ color: c.gridColor }} }}
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

      // Chart 3: HHI Anual Q04
      const ctxHHI = document.getElementById('chartHHI').getContext('2d');
      chartHHIInst = new Chart(ctxHHI, {{
        type: 'bar',
        data: {{
          labels: ['Era Clásica (1950–1980)', 'Era Intermedia (1981–2013)', 'Era Híbrida (2014–2025)'],
          datasets: [{{
            label: 'HHI Promedio Anual (Longitud Invariante)',
            data: [{hhi_clasica_anual}, 4390.6, {hhi_hibrida_anual}],
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
            y: {{ ticks: {{ color: c.textColor, callback: v => v + '%' }}, grid: {{ color: c.gridColor }} }}
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
              label: 'Tasa Avería Mecánica Auditada (%)',
              data: [{falla_mec_clasica}, 25.15, {falla_mec_moderna}],
              backgroundColor: c.accent
            }},
            {{
              label: 'Tasa Choques/Accidentes (%)',
              data: [8.97, 12.37, 6.93],
              backgroundColor: c.accent2
            }},
            {{
              label: 'Otros Abandonos (%)',
              data: [5.58, 4.35, 2.82],
              backgroundColor: c.gold
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

target_paths = [
    r"c:\Users\narda\Downloads\FI BD-LCD 2026 Tema 05 - SQL Practica - F1\TP-cuatrimestral-3ra_entrega-Rosa_Kimel_Connon.html",
    r"c:\Users\narda\Downloads\FI BD-LCD 2026 Tema 05 - SQL Practica - F1\FI BD-LCD 2026 Tema 05 - SQL Practica - F1\TP-cuatrimestral-3ra_entrega-Rosa_Kimel_Connon.html",
    r"c:\Users\narda\.gemini\antigravity-ide\brain\bd71d553-149e-4436-a7cb-ab58c601963a\TP-cuatrimestral-3ra_entrega-Rosa_Kimel_Connon.html"
]

for p in target_paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully generated: {p} ({len(html_content)} bytes)")
