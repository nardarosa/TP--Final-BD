# -*- coding: utf-8 -*-
"""
Formateadores de tablas HTML para la Tercera Entrega Mejorada:
'TP-cuatrimestral-3ra_entrega-Rosa_Kimel_Connon.html'
Incorpora todas las correcciones metodológicas y tests econométricos.
"""
import json

with open('all_query_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def table_q01():
    rows = ""
    for r in data['q01'][:10]:
        g = r['grilla']
        vic = r['victorias']
        pct = r['pct_victorias']
        hl = ' class="hl"' if str(g) == '1' else (' class="hl2"' if str(g) in ['2', '3'] else '')
        rows += f"<tr{hl}><td class=\"num\">P{g}</td><td class=\"num\">{vic}</td><td class=\"num\">{pct}%</td></tr>\n"
    return f"""<div class="tw"><table>
<thead><tr><th class="num">Posición de largada (Grilla)</th><th class="num">Victorias históricas (1950–2025)</th><th class="num">% sobre victorias con grilla conocida</th></tr></thead>
<tbody>
{rows}</tbody></table></div>"""

def table_q02():
    rows = ""
    for r in data['q02']:
        era = r['era']
        fr = r['franja']
        part = r['participaciones']
        vic = r['victorias']
        pct_vic = r['pct_victoria']
        pod = r['podios']
        pct_pod = r['pct_podio']
        hl = ' class="hlnew"' if 'Moderna' in era and fr == 'P1 (Pole)' else (' class="hl"' if fr == 'P1 (Pole)' else '')
        rows += f"<tr{hl}><td>{era}</td><td><strong>{fr}</strong></td><td class=\"num\">{part}</td><td class=\"num\">{vic}</td><td class=\"num\"><strong>{pct_vic}%</strong></td><td class=\"num\">{pod}</td><td class=\"num\">{pct_pod}%</td></tr>\n"
    return f"""<div class="tw"><table>
<thead><tr><th>Era del Campeonato</th><th>Franja de Grilla</th><th class="num">Participaciones válidas</th><th class="num">Victorias</th><th class="num">Tasa Victoria (%)</th><th class="num">Podios</th><th class="num">Tasa Podio (%)</th></tr></thead>
<tbody>
{rows}</tbody></table></div>"""

def table_q03_crossover():
    rows = ""
    for r in data['q03_crossover']:
        dec = r['decada']
        pol = r['total_poles']
        vic = r['victorias_pole']
        tasa_bruta = r['tasa_conversion_pole']
        pct_ab_pole = r['pct_abandono_poleman']
        tasa_cond = r['tasa_conversion_si_termina']
        falla_mec = r['pct_falla_mecanica_global']
        hl = ' class="hl"' if str(dec) == '1980' else (' class="hlnew"' if str(dec) in ['2010', '2020'] else '')
        rows += f"""<tr{hl}>
<td>Década de {dec}s</td>
<td class="num">{pol}</td>
<td class="num">{vic}</td>
<td class="num"><strong>{tasa_bruta}%</strong></td>
<td class="num">{pct_ab_pole}%</td>
<td class="num"><strong>{tasa_cond}%</strong></td>
<td class="num">{falla_mec}%</td>
</tr>\n"""
    return f"""<div class="tw"><table>
<thead><tr>
<th>Década</th>
<th class="num">Poles Totales</th>
<th class="num">Victorias Pole</th>
<th class="num">Tasa Conversión Bruta (%)</th>
<th class="num">Abandono del Poleman (%)</th>
<th class="num">Tasa Conversión si Termina (%)</th>
<th class="num">Roturas Mecánicas Globales (%)</th>
</tr></thead>
<tbody>
{rows}</tbody></table></div>"""

def table_q04_annual():
    rows = ""
    for r in data['q04_annual_hybrid']:
        era = r['era']
        temp = r['temporadas']
        prom_c = r['prom_constructores_ganadores']
        prom_sh = r['prom_share_lider_anual']
        prom_hhi = r['prom_hhi_anual']
        min_hhi = r['min_hhi_anual']
        max_hhi = r['max_hhi_anual']
        hl = ' class="hlnew"' if 'Hibrida' in era else ''
        rows += f"""<tr{hl}>
<td>{era}</td>
<td class="num">{temp}</td>
<td class="num"><strong>{prom_c}</strong></td>
<td class="num">{prom_sh}%</td>
<td class="num"><strong>{prom_hhi}</strong></td>
<td class="num">{min_hhi} – {max_hhi}</td>
</tr>\n"""
    return f"""<div class="tw"><table>
<thead><tr>
<th>Era (Corte Híbrido 2014)</th>
<th class="num">Temporadas</th>
<th class="num">Prom. Constructores Ganadores / Año</th>
<th class="num">Share Promedio Constructor Líder</th>
<th class="num">HHI Promedio Anual (Longitud Invariante)</th>
<th class="num">Rango HHI (Mín–Máx)</th>
</tr></thead>
<tbody>
{rows}</tbody></table></div>"""

def table_q05_rebadged():
    rows = ""
    for r in data['q05_rebadged']:
        era = r['era']
        rk = r['rk']
        mot = r['familia_motor']
        vic = r['victorias']
        pct = r['pct_era']
        hl = ' class="hlnew"' if 'Hibrida' in era and rk == 1 else (' class="hl2"' if 'Hibrida' in era and rk == 2 else '')
        rows += f"<tr{hl}><td>{era}</td><td class=\"num\">#{rk}</td><td><strong>{mot}</strong></td><td class=\"num\">{vic}</td><td class=\"num\"><strong>{pct}%</strong></td></tr>\n"
    return f"""<div class="tw"><table>
<thead><tr><th>Era (Con corte 2014)</th><th class="num">Rank</th><th>Familia de Motor (Unificada por Rebadging)</th><th class="num">Victorias</th><th class="num">% sobre victorias de la era</th></tr></thead>
<tbody>
{rows}</tbody></table></div>"""

def table_q06_rebadged():
    rows = ""
    for r in data['q06_rebadged']:
        era = r['era']
        rk = r['rk']
        mot = r['familia_motor']
        part = r['participaciones']
        vic = r['victorias']
        pct_vic = r['pct_victoria']
        pod = r['podios']
        pct_pod = r['pct_podio']
        hl = ' class="hlnew"' if 'Moderna' in era and rk == 1 else (' class="hl2"' if 'Moderna' in era and rk == 2 else '')
        rows += f"<tr{hl}><td>{era}</td><td class=\"num\">#{rk}</td><td><strong>{mot}</strong></td><td class=\"num\">{part}</td><td class=\"num\">{vic}</td><td class=\"num\"><strong>{pct_vic}%</strong></td><td class=\"num\">{pod}</td><td class=\"num\">{pct_pod}%</td></tr>\n"
    return f"""<div class="tw"><table>
<thead><tr><th>Era</th><th class="num">Rank</th><th>Familia de Motor (Rebadging Mapeado)</th><th class="num">Participaciones (≥50)</th><th class="num">Victorias</th><th class="num">Tasa Victoria (%)</th><th class="num">Podios</th><th class="num">Tasa Podio (%)</th></tr></thead>
<tbody>
{rows}</tbody></table></div>"""

def table_q07_works_client():
    rows = ""
    for r in data['q07_works_vs_customer']:
        mot = r['familia_motor']
        tipo = r['tipo_equipo']
        part = r['participaciones']
        vic = r['victorias']
        pct_vic = r['pct_victoria_total']
        pol = r['poles']
        v_pol = r['vic_desde_pole']
        conv = f"{r['conversion_pole_pct']}%" if r['conversion_pole_pct'] is not None else "—"
        hl = ' class="hlnew"' if 'Oficial' in tipo and mot in ['Mercedes', 'Honda / RBPT'] else (' class="hl"' if 'Oficial' in tipo else '')
        rows += f"""<tr{hl}>
<td><strong>{mot}</strong></td>
<td>{tipo}</td>
<td class="num">{part}</td>
<td class="num"><strong>{vic}</strong></td>
<td class="num"><strong>{pct_vic}%</strong></td>
<td class="num">{pol}</td>
<td class="num">{v_pol}</td>
<td class="num"><strong>{conv}</strong></td>
</tr>\n"""
    return f"""<div class="tw"><table>
<thead><tr>
<th>Familia de Motor</th>
<th>Estatus del Equipo</th>
<th class="num">Participaciones</th>
<th class="num">Victorias</th>
<th class="num">Tasa Victoria Total (%)</th>
<th class="num">Poles Obtenidas</th>
<th class="num">Victorias desde Pole</th>
<th class="num">Conversión Pole → Victoria (%)</th>
</tr></thead>
<tbody>
{rows}</tbody></table></div>"""

def table_q08_improved():
    rows = ""
    for r in data['q08_hybrid']:
        era = r['era']
        temp = r['temporadas']
        prom_g = r['prom_ganadores_temporada']
        prom_c = r['prom_carreras']
        prom_sh = r['prom_share_max_ganador']
        prom_hhi = r['prom_hhi_pilotos']
        min_hhi = r['min_hhi_pilotos']
        max_hhi = r['max_hhi_pilotos']
        hl = ' class="hlnew"' if 'Hibrida' in era else ''
        rows += f"""<tr{hl}>
<td>{era}</td>
<td class="num">{temp}</td>
<td class="num">{prom_g}</td>
<td class="num">{prom_c}</td>
<td class="num"><strong>{prom_sh}%</strong></td>
<td class="num"><strong>{prom_hhi}</strong></td>
<td class="num">{min_hhi} – {max_hhi}</td>
</tr>\n"""
    return f"""<div class="tw"><table>
<thead><tr>
<th>Era (Corte Híbrido 2014)</th>
<th class="num">Temporadas</th>
<th class="num">Prom. Ganadores / Año</th>
<th class="num">Prom. GPs / Año</th>
<th class="num">% Victorias del Máximo Ganador Anual</th>
<th class="num">HHI Pilotos Promedio (Concentración)</th>
<th class="num">Rango HHI Pilotos</th>
</tr></thead>
<tbody>
{rows}</tbody></table></div>"""

def table_q09():
    rows = ""
    for r in data['q09']:
        era = r['era']
        temp = r['temporadas']
        tot_v = r['total_victorias_campeones']
        v_pol = r['victorias_desde_pole']
        pct = r['pct_desde_pole']
        hl = ' class="hlnew"' if 'Moderna' in era else ''
        rows += f"<tr{hl}><td>{era}</td><td class=\"num\">{temp}</td><td class=\"num\">{tot_v}</td><td class=\"num\">{v_pol}</td><td class=\"num\"><strong>{pct}%</strong></td></tr>\n"
    return f"""<div class="tw"><table>
<thead><tr><th>Era</th><th class="num">Temporadas completas</th><th class="num">Victorias totales de los campeones</th><th class="num">Victorias obtenidas desde Pole (P1)</th><th class="num">% Victorias del campeón desde Pole</th></tr></thead>
<tbody>
{rows}</tbody></table></div>"""

def table_q10_conditional():
    rows = ""
    for r in data['q10_conditional']:
        era = r['era']
        pol = r['total_poles']
        vic = r['victorias']
        c_bruta = r['conversion_bruta_pct']
        ci_b = r['ci_bruta_95']
        ab_pol = r['abandonos_poleman']
        pct_ab = r['pct_abandono_poleman']
        fin = r['poles_terminaron']
        vic_fin = r['victorias_si_termina']
        c_fin = r['conversion_si_termina_pct']
        ci_f = r['ci_si_termina_95']
        hl = ' class="hlnew"' if 'Moderna' in era else ''
        rows += f"""<tr{hl}>
<td>{era}</td>
<td class="num">{pol}</td>
<td class="num">{vic}</td>
<td class="num"><strong>{c_bruta}%</strong> <small>{ci_b}</small></td>
<td class="num">{ab_pol} ({pct_ab}%)</td>
<td class="num">{fin}</td>
<td class="num"><strong>{c_fin}%</strong> <small>{ci_f}</small></td>
</tr>\n"""
    return f"""<div class="tw"><table>
<thead><tr>
<th>Era</th>
<th class="num">Poles Totales</th>
<th class="num">Victorias Pole</th>
<th class="num">Conversión Bruta [% IC 95%]</th>
<th class="num">Abandonos Poleman (%)</th>
<th class="num">Poleman Cruzó Meta</th>
<th class="num">Conversión Condicional si Termina [% IC 95%]</th>
</tr></thead>
<tbody>
{rows}</tbody></table></div>"""

def table_q11_audited():
    rows = ""
    for r in data['q11_audited']:
        era = r['era']
        tot_part = r['total_participaciones']
        tot_ab = r['total_abandonos']
        pct_ab = r['pct_abandono_total']
        ab_mec = r['abandonos_mecanicos']
        pct_mec = r['pct_abandono_mecanico']
        ci_mec = r['ci_mecanica_95']
        acc = r['accidentes']
        pct_acc = r['pct_accidentes']
        otros = r['otros_abandonos']
        pct_otros = r['pct_otros']
        hl = ' class="hlnew"' if 'Moderna' in era else ''
        rows += f"""<tr{hl}>
<td>{era}</td>
<td class="num">{tot_part}</td>
<td class="num">{tot_ab} ({pct_ab}%)</td>
<td class="num"><strong>{ab_mec}</strong></td>
<td class="num"><strong>{pct_mec}%</strong> <small>{ci_mec}</small></td>
<td class="num">{acc} ({pct_acc}%)</td>
<td class="num">{otros} ({pct_otros}%)</td>
</tr>\n"""
    return f"""<div class="tw"><table>
<thead><tr>
<th>Era</th>
<th class="num">Participaciones</th>
<th class="num">Abandonos Totales (%)</th>
<th class="num">Averías Mecánicas (Auditoría Moderna)</th>
<th class="num">Tasa Falla Mecánica [% IC 95%]</th>
<th class="num">Accidentes / Choques (%)</th>
<th class="num">Otros Abandonos (%)</th>
</tr></thead>
<tbody>
{rows}</tbody></table></div>"""

def table_q12_systematic():
    rows = ""
    for r in data['q12_systematic']:
        era = r['era']
        par = r['parejas_analizadas']
        br_pts = r['prom_brecha_puntos_pct']
        sh_vic = r['prom_share_vic_lider_pareja']
        diff_pts = r['prom_diff_puntos_absoluta']
        hl = ' class="hlnew"' if 'Moderna' in era else ''
        rows += f"""<tr{hl}>
<td>{era}</td>
<td class="num"><strong>{par} parejas</strong></td>
<td class="num"><strong>{br_pts}%</strong></td>
<td class="num"><strong>{sh_vic}%</strong></td>
<td class="num">{diff_pts} pts</td>
</tr>\n"""
    return f"""<div class="tw"><table>
<thead><tr>
<th>Era</th>
<th class="num">Parejas Titulares Analizadas (≥10 GPs compartidos)</th>
<th class="num">Brecha Relativa Promedio Puntos (|P1-P2| / Total)</th>
<th class="num">% Victorias Acaparadas por el Líder del Equipo</th>
<th class="num">Diferencia Absoluta Promedio de Puntos</th>
</tr></thead>
<tbody>
{rows}</tbody></table></div>"""

def table_q12_duels():
    selected = [
        ('1988', 'McLaren', 'Honda', 'Ayrton Senna', 16, 8, 11, 13, 90.0, 'Alain Prost', 7, 14, 2, 87.0),
        ('2002', 'Ferrari', 'Ferrari', 'Michael Schumacher', 17, 11, 17, 7, 144.0, 'Rubens Barrichello', 4, 10, 3, 77.0),
        ('2014', 'Mercedes', 'Mercedes', 'Lewis Hamilton', 19, 11, 16, 7, 384.0, 'Nico Rosberg', 5, 15, 11, 317.0),
        ('2016', 'Mercedes', 'Mercedes', 'Lewis Hamilton', 21, 10, 17, 12, 380.0, 'Nico Rosberg', 9, 16, 8, 385.0),
        ('2021', 'Red Bull', 'Honda', 'Max Verstappen', 22, 10, 18, 10, 395.5, 'Sergio Pérez', 1, 5, 0, 190.0),
        ('2023', 'Red Bull', 'Honda RBPT', 'Max Verstappen', 22, 19, 21, 12, 530.0, 'Sergio Pérez', 2, 9, 2, 260.0)
    ]
    rows = ""
    for y, team, mot, d1, gps, v1, pod1, pol1, pts1, d2, v2, pod2, pol2, pts2 in selected:
        rows += f"""<tr>
<td><strong>{y}</strong></td>
<td>{team}</td>
<td>{mot}</td>
<td><strong>{d1}</strong></td>
<td class="num">{gps}</td>
<td class="num"><strong>{v1}</strong></td>
<td class="num">{pod1}</td>
<td class="num">{pol1}</td>
<td class="num">{pts1}</td>
<td>{d2}</td>
<td class="num"><strong>{v2}</strong></td>
<td class="num">{pod2}</td>
<td class="num">{pol2}</td>
<td class="num">{pts2}</td>
</tr>\n"""
    return f"""<div class="tw"><table>
<thead><tr>
<th>Año</th><th>Equipo</th><th>Motor</th>
<th>Piloto 1 (Líder)</th><th class="num">GPs</th><th class="num">Vic 1</th><th class="num">Pod 1</th><th class="num">Pole 1</th><th class="num">Pts 1</th>
<th>Piloto 2</th><th class="num">Vic 2</th><th class="num">Pod 2</th><th class="num">Pole 2</th><th class="num">Pts 2</th>
</tr></thead>
<tbody>
{rows}</tbody></table></div>"""

def table_a1():
    rows = ""
    for r in data['a1']:
        era = r['era']
        tot = r['total_finalizados']
        prom = r['prom_pos_ganadas']
        mant = r['mantuvo_pos']
        pct_mant = r['pct_mantuvo_pos']
        gano = r['gano_pos']
        pct_gano = r['pct_gano_pos']
        perd = r['perdio_pos']
        pct_perd = r['pct_perdio_pos']
        hl = ' class="hlnew"' if 'Moderna' in era else ''
        rows += f"<tr{hl}><td>{era}</td><td class=\"num\">{tot}</td><td class=\"num\"><strong>{prom}</strong></td><td class=\"num\">{mant} ({pct_mant}%)</td><td class=\"num\">{gano} ({pct_gano}%)</td><td class=\"num\">{perd} ({pct_perd}%)</td></tr>\n"
    return f"""<div class="tw"><table>
<thead><tr><th>Era</th><th class="num">Pilotos que cruzaron meta</th><th class="num">Δ Promedio Posiciones Ganadas</th><th class="num">Mantuvo Posición (Δ=0)</th><th class="num">Ganó Posiciones (Δ>0)</th><th class="num">Perdió Posiciones (Δ<0)</th></tr></thead>
<tbody>
{rows}</tbody></table></div>"""

def table_logit_model():
    rows = ""
    for r in data['logit_results']:
        var = r['variable']
        b = r['coef']
        se = r['std_err']
        z = r['z_stat']
        p = r['p_value']
        or_val = r['odds_ratio']
        hl = ' class="hlnew"' if 'Interacción' in var or 'Pole' in var else ''
        rows += f"""<tr{hl}>
<td><strong>{var}</strong></td>
<td class="num">{b}</td>
<td class="num">{se}</td>
<td class="num">{z}</td>
<td class="num"><strong>{p}</strong></td>
<td class="num"><strong>{or_val}</strong></td>
</tr>\n"""
    return f"""<div class="tw"><table>
<thead><tr>
<th>Variable Predictora en el Modelo Logit</th>
<th class="num">Coeficiente (β)</th>
<th class="num">Error Estándar</th>
<th class="num">Estadístico z</th>
<th class="num">Valor p</th>
<th class="num">Odds Ratio (OR = e^β)</th>
</tr></thead>
<tbody>
{rows}</tbody></table></div>"""
