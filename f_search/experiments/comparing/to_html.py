import logging
import csv
import statistics
from collections import defaultdict
from f_log import setup_log


def load_csv(path: str) -> list[dict[str, str]]:
    """
    ========================================================================
     Load the comparison CSV into a list of dicts.
    ========================================================================
    """
    logging.info(f'Loading CSV from {path}')
    with open(path, 'r') as f:
        rows = list(csv.DictReader(f))
    logging.info(f'Loaded {len(rows)} rows')
    return rows


def _ratio(fwd: float, bwd: float) -> float:
    """
    ========================================================================
     Return fwd/bwd ratio. >1 means backward is better.
    ========================================================================
    """
    if bwd == 0:
        return 0.0
    return fwd / bwd


def _pct_saved(fwd: float, bwd: float) -> float:
    """
    ========================================================================
     Percent of explored states saved by backward vs forward.
     Positive = backward saves, negative = forward saves.
    ========================================================================
    """
    if fwd == 0:
        return 0.0
    return (fwd - bwd) / fwd * 100


def _bucket(value: float, edges: list[float]) -> str:
    """
    ========================================================================
     Assign value to a bucket defined by edges.
    ========================================================================
    """
    for i in range(len(edges) - 1):
        if value < edges[i + 1]:
            return f'{edges[i]}-{edges[i+1]}'
    return f'{edges[-1]}+'


def _build_analysis(rows: list[dict]) -> dict:
    """
    ========================================================================
     Build all analysis groups from raw CSV rows.
    ========================================================================
    """
    # Parse numeric fields
    parsed = []
    for r in rows:
        fwd = int(r['forward_explored'])
        bwd = int(r['backward_explored'])
        d = {
            'domain': r['domain'],
            'map': r['map'],
            'grid_cells': int(r['grid_cells']),
            'k': int(r['k']),
            'avg_dist_start_goals': float(r['avg_dist_start_goals']),
            'norm_dist_start_goals':
                float(r['norm_dist_start_goals']),
            'norm_dist_between_goals':
                float(r['norm_dist_between_goals']),
            'fwd': fwd,
            'bwd': bwd,
            'ratio': _ratio(fwd, bwd),
            'pct_saved': _pct_saved(fwd, bwd),
            'fwd_elapsed': float(r['forward_elapsed']),
            'bwd_elapsed': float(r['backward_elapsed']),
        }
        parsed.append(d)

    analysis = {}

    # 1. By domain
    analysis['by_domain'] = _group_stats(parsed, key='domain')

    # 2. By grid size (buckets)
    size_edges = [0, 1000, 5000, 20000, 100000, 500000]
    for d in parsed:
        d['size_bucket'] = _bucket(d['grid_cells'], size_edges)
    analysis['by_grid_size'] = _group_stats(parsed, key='size_bucket')

    # 3. By k
    analysis['by_k'] = _group_stats(parsed, key='k')

    # 4. By norm_dist_start_goals (buckets)
    nd_edges = [0, 0.5, 1, 2, 5, 10]
    for d in parsed:
        d['nd_sg_bucket'] = _bucket(
            d['norm_dist_start_goals'], nd_edges)
    analysis['by_norm_dist_sg'] = _group_stats(
        parsed, key='nd_sg_bucket')

    # 5. By norm_dist_between_goals (buckets)
    for d in parsed:
        d['nd_gg_bucket'] = _bucket(
            d['norm_dist_between_goals'], nd_edges)
    analysis['by_norm_dist_gg'] = _group_stats(
        parsed, key='nd_gg_bucket')

    # 6. By avg_dist_start_goals (buckets)
    dist_edges = [0, 50, 100, 200, 500, 1000]
    for d in parsed:
        d['dist_sg_bucket'] = _bucket(
            d['avg_dist_start_goals'], dist_edges)
    analysis['by_dist_sg'] = _group_stats(
        parsed, key='dist_sg_bucket')

    # 7. Chart data: values with winner labels for histograms
    chart_values = []
    for d in parsed:
        if d['bwd'] < d['fwd']:
            winner = 'bwd'
        elif d['fwd'] < d['bwd']:
            winner = 'fwd'
        else:
            winner = 'tie'
        d['winner'] = winner
        chart_values.append(d)
    analysis['chart_values'] = chart_values

    # 8. Scatter plot data
    scatter_k = [(d['k'], d['ratio'], d['winner'])
                 for d in parsed]
    scatter_nd_sg = [(d['norm_dist_start_goals'], d['ratio'],
                      d['winner']) for d in parsed]
    scatter_nd_gg = [(d['norm_dist_between_goals'], d['ratio'],
                      d['winner']) for d in parsed]
    analysis['scatter_k'] = scatter_k
    analysis['scatter_nd_sg'] = scatter_nd_sg
    analysis['scatter_nd_gg'] = scatter_nd_gg

    # 9. Pct saved values for distribution histogram
    analysis['pct_saved_values'] = [d['pct_saved'] for d in parsed]

    # 10. Top 20 where forward wins most
    top_fwd = sorted(parsed, key=lambda d: d['pct_saved'])[:20]
    analysis['top_forward_wins'] = top_fwd

    # 8. Top 20 where backward wins most
    top_bwd = sorted(parsed, key=lambda d: -d['pct_saved'])[:20]
    analysis['top_backward_wins'] = top_bwd

    # 12. Overall summary
    ratios = [d['ratio'] for d in parsed]
    pcts = [d['pct_saved'] for d in parsed]
    n_bwd_wins = sum(1 for d in parsed if d['bwd'] < d['fwd'])
    n_fwd_wins = sum(1 for d in parsed if d['fwd'] < d['bwd'])
    n_ties = sum(1 for d in parsed if d['fwd'] == d['bwd'])
    analysis['summary'] = {
        'total': len(parsed),
        'backward_wins': n_bwd_wins,
        'forward_wins': n_fwd_wins,
        'ties': n_ties,
        'mean_ratio': statistics.mean(ratios) if ratios else 0,
        'median_ratio': statistics.median(ratios) if ratios else 0,
        'mean_pct_saved': statistics.mean(pcts) if pcts else 0,
        'median_pct_saved': statistics.median(pcts) if pcts else 0,
    }

    return analysis


def _group_stats(rows: list[dict],
                 key: str) -> list[dict]:
    """
    ========================================================================
     Group rows by key and compute aggregate stats per group.
    ========================================================================
    """
    groups = defaultdict(list)
    for r in rows:
        groups[r[key]].append(r)
    result = []
    for group_key in sorted(groups.keys(), key=str):
        items = groups[group_key]
        n = len(items)
        ratios = [d['ratio'] for d in items]
        pcts = [d['pct_saved'] for d in items]
        fwd_total = sum(d['fwd'] for d in items)
        bwd_total = sum(d['bwd'] for d in items)
        n_bwd_wins = sum(1 for d in items if d['bwd'] < d['fwd'])
        n_fwd_wins = sum(1 for d in items if d['fwd'] < d['bwd'])
        result.append({
            'group': str(group_key),
            'n': n,
            'fwd_total': fwd_total,
            'bwd_total': bwd_total,
            'mean_ratio': round(statistics.mean(ratios), 3),
            'median_ratio': round(statistics.median(ratios), 3),
            'mean_pct_saved': round(statistics.mean(pcts), 2),
            'median_pct_saved': round(statistics.median(pcts), 2),
            'backward_wins': n_bwd_wins,
            'forward_wins': n_fwd_wins,
            'bwd_win_pct': round(n_bwd_wins / n * 100, 1),
        })
    return result


def _render_histogram(title: str,
                      values: list[float],
                      edges: list[float],
                      xlabel: str) -> str:
    """
    ========================================================================
     Render an SVG histogram of values bucketed by edges.
     Each bar is split: green = backward wins, red = forward wins.
    ========================================================================
    """
    # Bucket the values
    buckets = defaultdict(lambda: {'bwd': 0, 'fwd': 0, 'tie': 0})
    for v, winner in values:
        label = _bucket(v, edges)
        buckets[label][winner] += 1
    # Build ordered labels
    labels = []
    for i in range(len(edges) - 1):
        labels.append(f'{edges[i]}-{edges[i+1]}')
    labels.append(f'{edges[-1]}+')
    # Filter to labels that have data
    labels = [lb for lb in labels if lb in buckets]
    if not labels:
        return ''
    max_count = max(
        buckets[lb]['bwd'] + buckets[lb]['fwd'] + buckets[lb]['tie']
        for lb in labels)
    if max_count == 0:
        return ''
    # SVG dimensions
    w = 600
    bar_h = 28
    gap = 4
    left = 100
    right = 40
    chart_w = w - left - right
    h = len(labels) * (bar_h + gap) + 60
    bars = ''
    for i, lb in enumerate(labels):
        y = i * (bar_h + gap) + 10
        b = buckets[lb]
        total = b['bwd'] + b['fwd'] + b['tie']
        # Label
        bars += (f'<text x="{left - 8}" y="{y + bar_h // 2 + 4}"'
                 f' text-anchor="end" fill="#cbd5e1"'
                 f' font-size="11">{lb}</text>')
        # Backward bar (green)
        bw = b['bwd'] / max_count * chart_w
        bars += (f'<rect x="{left}" y="{y}" width="{bw}"'
                 f' height="{bar_h}" fill="#34d399" rx="2"/>')
        # Tie bar (gray)
        tw = b['tie'] / max_count * chart_w
        bars += (f'<rect x="{left + bw}" y="{y}" width="{tw}"'
                 f' height="{bar_h}" fill="#64748b" rx="2"/>')
        # Forward bar (red)
        fw = b['fwd'] / max_count * chart_w
        bars += (f'<rect x="{left + bw + tw}" y="{y}"'
                 f' width="{fw}" height="{bar_h}"'
                 f' fill="#fb7185" rx="2"/>')
        # Count label
        bars += (f'<text x="{left + bw + tw + fw + 4}"'
                 f' y="{y + bar_h // 2 + 4}" fill="#94a3b8"'
                 f' font-size="11">{total}</text>')
    # X-axis label
    bars += (f'<text x="{left + chart_w // 2}" y="{h - 5}"'
             f' text-anchor="middle" fill="#94a3b8"'
             f' font-size="11">{xlabel}</text>')
    # Legend
    ly = h - 45
    bars += (f'<rect x="{left}" y="{ly}" width="12"'
             f' height="12" fill="#34d399" rx="2"/>')
    bars += (f'<text x="{left + 16}" y="{ly + 10}"'
             f' fill="#cbd5e1" font-size="11">Backward wins</text>')
    bars += (f'<rect x="{left + 120}" y="{ly}" width="12"'
             f' height="12" fill="#fb7185" rx="2"/>')
    bars += (f'<text x="{left + 136}" y="{ly + 10}"'
             f' fill="#cbd5e1" font-size="11">Forward wins</text>')
    bars += (f'<rect x="{left + 240}" y="{ly}" width="12"'
             f' height="12" fill="#64748b" rx="2"/>')
    bars += (f'<text x="{left + 256}" y="{ly + 10}"'
             f' fill="#cbd5e1" font-size="11">Tie</text>')
    return f'''<section>
<h2>{title}</h2>
<svg width="{w}" height="{h}" style="background:var(--panel);
  border-radius:6px;padding:8px;margin:.5rem 0;">
{bars}
</svg>
</section>'''


def _render_pct_histogram(title: str,
                          pcts: list[float]) -> str:
    """
    ========================================================================
     Render an SVG histogram of % saved distribution.
    ========================================================================
    """
    edges = [-50, -20, -10, -5, 0, 5, 10, 20, 50, 100]
    counts = defaultdict(int)
    for p in pcts:
        counts[_bucket(p, edges)] += 1
    # Build bucket labels with their low-edge values
    all_labels = []
    for i in range(len(edges) - 1):
        all_labels.append((f'{edges[i]}-{edges[i+1]}', edges[i]))
    all_labels.append((f'{edges[-1]}+', edges[-1]))
    all_labels = [(lb, low) for lb, low in all_labels
                  if counts.get(lb, 0)]
    if not all_labels:
        return ''
    max_count = max(counts[lb] for lb, _ in all_labels)
    if max_count == 0:
        return ''
    w = 600
    bar_h = 24
    gap = 4
    left = 100
    right = 40
    chart_w = w - left - right
    h = len(all_labels) * (bar_h + gap) + 40
    bars = ''
    for i, (lb, low) in enumerate(all_labels):
        y = i * (bar_h + gap) + 10
        c = counts[lb]
        bw = c / max_count * chart_w
        # Color: negative = forward better (red), positive = backward
        color = '#34d399' if low >= 0 else '#fb7185'
        bars += (f'<text x="{left - 8}" y="{y + bar_h // 2 + 4}"'
                 f' text-anchor="end" fill="#cbd5e1"'
                 f' font-size="10">{lb}%</text>')
        bars += (f'<rect x="{left}" y="{y}" width="{bw}"'
                 f' height="{bar_h}" fill="{color}" rx="2"/>')
        bars += (f'<text x="{left + bw + 4}"'
                 f' y="{y + bar_h // 2 + 4}" fill="#94a3b8"'
                 f' font-size="10">{c}</text>')
    return f'''<section>
<h2>{title}</h2>
<ol><li>Green = backward saves explored states, Red = forward saves.</li>
<li>X-axis: number of problems in each % saved bucket.</li></ol>
<svg width="{w}" height="{h}" style="background:var(--panel);
  border-radius:6px;padding:8px;margin:.5rem 0;">
{bars}
</svg>
</section>'''


def _render_scatter(title: str,
                    points: list[tuple[float, float, str]],
                    xlabel: str,
                    ylabel: str) -> str:
    """
    ========================================================================
     Render an SVG scatter plot. Points are (x, y, winner).
     winner: 'bwd' = green, 'fwd' = red, 'tie' = gray.
    ========================================================================
    """
    if not points:
        return ''
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    if x_max == x_min:
        x_max = x_min + 1
    if y_max == y_min:
        y_max = y_min + 1
    w, h = 600, 350
    left, right, top, bottom = 60, 20, 20, 40
    cw = w - left - right
    ch = h - top - bottom
    colors = {'bwd': '#34d399', 'fwd': '#fb7185', 'tie': '#64748b'}
    dots = ''
    for x, y, winner in points:
        sx = left + (x - x_min) / (x_max - x_min) * cw
        sy = top + ch - (y - y_min) / (y_max - y_min) * ch
        c = colors.get(winner, '#64748b')
        dots += (f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="3"'
                 f' fill="{c}" opacity="0.7"/>')
    # Axes labels
    dots += (f'<text x="{left + cw // 2}" y="{h - 5}"'
             f' text-anchor="middle" fill="#94a3b8"'
             f' font-size="11">{xlabel}</text>')
    dots += (f'<text x="12" y="{top + ch // 2}"'
             f' text-anchor="middle" fill="#94a3b8"'
             f' font-size="11"'
             f' transform="rotate(-90,12,{top + ch // 2})">'
             f'{ylabel}</text>')
    # Axis ticks
    for frac in [0, 0.25, 0.5, 0.75, 1.0]:
        xv = x_min + frac * (x_max - x_min)
        sx = left + frac * cw
        dots += (f'<text x="{sx:.0f}" y="{top + ch + 15}"'
                 f' text-anchor="middle" fill="#64748b"'
                 f' font-size="9">{xv:.1f}</text>')
        yv = y_min + frac * (y_max - y_min)
        sy = top + ch - frac * ch
        dots += (f'<text x="{left - 5}" y="{sy:.0f}"'
                 f' text-anchor="end" fill="#64748b"'
                 f' font-size="9">{yv:.1f}</text>')
    # Reference line at y=1 (ratio) if applicable
    if y_min < 1 < y_max and 'ratio' in ylabel.lower():
        ref_y = top + ch - (1 - y_min) / (y_max - y_min) * ch
        dots += (f'<line x1="{left}" y1="{ref_y:.0f}"'
                 f' x2="{left + cw}" y2="{ref_y:.0f}"'
                 f' stroke="#fbbf24" stroke-dasharray="4"'
                 f' opacity="0.5"/>')
        dots += (f'<text x="{left + cw + 2}" y="{ref_y:.0f}"'
                 f' fill="#fbbf24" font-size="9">ratio=1</text>')
    # Legend
    ly = 8
    dots += (f'<circle cx="{left}" cy="{ly}" r="4"'
             f' fill="#34d399"/>')
    dots += (f'<text x="{left + 8}" y="{ly + 4}"'
             f' fill="#cbd5e1" font-size="10">Bwd wins</text>')
    dots += (f'<circle cx="{left + 80}" cy="{ly}" r="4"'
             f' fill="#fb7185"/>')
    dots += (f'<text x="{left + 88}" y="{ly + 4}"'
             f' fill="#cbd5e1" font-size="10">Fwd wins</text>')
    return f'''<section>
<h2>{title}</h2>
<svg width="{w}" height="{h}" style="background:var(--panel);
  border-radius:6px;padding:8px;margin:.5rem 0;">
{dots}
</svg>
</section>'''


def _render_group_table(title: str,
                        group_col: str,
                        groups: list[dict]) -> str:
    """
    ========================================================================
     Render an HTML table for a group analysis.
    ========================================================================
    """
    rows_html = ''
    for g in groups:
        # Color the pct_saved cell
        pct = g['mean_pct_saved']
        if pct > 5:
            color = 'var(--good)'
        elif pct < -5:
            color = 'var(--bad)'
        else:
            color = 'var(--muted)'
        rows_html += f'''<tr>
<td>{g['group']}</td><td>{g['n']}</td>
<td>{g['fwd_total']:,}</td><td>{g['bwd_total']:,}</td>
<td>{g['mean_ratio']}</td><td>{g['median_ratio']}</td>
<td style="color:{color}">{g['mean_pct_saved']}%</td>
<td>{g['median_pct_saved']}%</td>
<td>{g['backward_wins']}</td><td>{g['forward_wins']}</td>
<td>{g['bwd_win_pct']}%</td>
</tr>'''
    return f'''<section>
<h2>{title}</h2>
<table>
<tr><th>{group_col}</th><th>N</th>
<th>Fwd Total</th><th>Bwd Total</th>
<th>Mean Ratio</th><th>Med Ratio</th>
<th>Mean % Saved</th><th>Med % Saved</th>
<th>Bwd Wins</th><th>Fwd Wins</th>
<th>Bwd Win %</th></tr>
{rows_html}
</table>
<ol>
<li>Ratio = fwd_explored / bwd_explored (&gt;1 means backward better).</li>
<li>% Saved = (fwd - bwd) / fwd * 100 (positive = backward saves).</li>
</ol>
</section>'''


def _render_top_table(title: str,
                      subtitle: str,
                      items: list[dict]) -> str:
    """
    ========================================================================
     Render an HTML table for top N cases.
    ========================================================================
    """
    rows_html = ''
    for d in items:
        pct = d['pct_saved']
        if pct > 5:
            color = 'var(--good)'
        elif pct < -5:
            color = 'var(--bad)'
        else:
            color = 'var(--muted)'
        rows_html += f'''<tr>
<td>{d['domain']}</td><td>{d['map'][:30]}</td>
<td>{d['grid_cells']:,}</td><td>{d['k']}</td>
<td>{d['norm_dist_start_goals']}</td>
<td>{d['norm_dist_between_goals']}</td>
<td>{d['fwd']:,}</td><td>{d['bwd']:,}</td>
<td>{round(d['ratio'], 3)}</td>
<td style="color:{color}">{round(pct, 1)}%</td>
</tr>'''
    return f'''<section>
<h2>{title}</h2>
<ol><li>{subtitle}</li></ol>
<table>
<tr><th>Domain</th><th>Map</th><th>Cells</th><th>k</th>
<th>Norm Dist SG</th><th>Norm Dist GG</th>
<th>Fwd Expl</th><th>Bwd Expl</th>
<th>Ratio</th><th>% Saved</th></tr>
{rows_html}
</table>
</section>'''


def generate_html(analysis: dict, path_html: str) -> None:
    """
    ========================================================================
     Generate the insights HTML file.
    ========================================================================
    """
    s = analysis['summary']

    summary_html = f'''<section>
<h2>Overall Summary</h2>
<ol>
<li>Total problems: <strong>{s['total']}</strong></li>
<li>Backward wins: <strong>{s['backward_wins']}</strong>
 ({round(s['backward_wins']/s['total']*100, 1)}%)</li>
<li>Forward wins: <strong>{s['forward_wins']}</strong>
 ({round(s['forward_wins']/s['total']*100, 1)}%)</li>
<li>Ties: <strong>{s['ties']}</strong></li>
<li>Mean fwd/bwd ratio: <strong>{round(s['mean_ratio'], 3)}</strong>
 (median: {round(s['median_ratio'], 3)})</li>
<li>Mean % saved by backward:
 <strong>{round(s['mean_pct_saved'], 2)}%</strong>
 (median: {round(s['median_pct_saved'], 2)}%)</li>
</ol>
</section>'''

    sections = [
        summary_html,
        _render_group_table('By Domain', 'Domain',
                            analysis['by_domain']),
        _render_group_table('By Grid Size (cells)', 'Size Bucket',
                            analysis['by_grid_size']),
        _render_group_table('By k (Number of Goals)', 'k',
                            analysis['by_k']),
        _render_group_table('By Avg Distance Start-Goals',
                            'Dist Bucket',
                            analysis['by_dist_sg']),
        _render_group_table('By Normalized Dist Start-Goals',
                            'Norm Dist %',
                            analysis['by_norm_dist_sg']),
        _render_group_table('By Normalized Dist Between Goals',
                            'Norm Dist %',
                            analysis['by_norm_dist_gg']),
        _render_top_table('Top 20: Forward Wins Most',
                          'Cases where forward explores fewer states'
                          ' than backward (negative % saved).',
                          analysis['top_forward_wins']),
        _render_top_table('Top 20: Backward Wins Most',
                          'Cases where backward explores fewer states'
                          ' than forward (positive % saved).',
                          analysis['top_backward_wins']),
        # Charts
        _render_pct_histogram(
            'Distribution of % Saved (Backward vs Forward)',
            analysis['pct_saved_values']),
        _render_histogram(
            'Wins by k (Number of Goals)',
            [(d['k'], d['winner'])
             for d in analysis['chart_values']],
            [2, 3, 5, 8, 12, 20],
            'k'),
        _render_histogram(
            'Wins by Grid Size (cells)',
            [(d['grid_cells'], d['winner'])
             for d in analysis['chart_values']],
            [0, 1000, 5000, 20000, 100000, 500000],
            'Grid Cells'),
        _render_histogram(
            'Wins by Norm Dist Start-Goals',
            [(d['norm_dist_start_goals'], d['winner'])
             for d in analysis['chart_values']],
            [0, 0.5, 1, 2, 5, 10],
            'Norm Dist SG (%)'),
        _render_histogram(
            'Wins by Norm Dist Between Goals',
            [(d['norm_dist_between_goals'], d['winner'])
             for d in analysis['chart_values']],
            [0, 0.5, 1, 2, 5, 10],
            'Norm Dist GG (%)'),
        _render_scatter(
            'k vs Ratio (fwd/bwd)',
            analysis['scatter_k'],
            'k', 'Ratio (fwd/bwd)'),
        _render_scatter(
            'Norm Dist Start-Goals vs Ratio',
            analysis['scatter_nd_sg'],
            'Norm Dist SG (%)', 'Ratio (fwd/bwd)'),
        _render_scatter(
            'Norm Dist Between Goals vs Ratio',
            analysis['scatter_nd_gg'],
            'Norm Dist GG (%)', 'Ratio (fwd/bwd)'),
    ]

    # Filter out empty sections (charts with no data)
    sections = [s for s in sections if s]

    toc_items = ''
    for i, sec in enumerate(sections):
        # Extract title from <h2>
        start = sec.find('<h2>') + 4
        end = sec.find('</h2>')
        title = sec[start:end]
        sec_id = f'sec-{i}'
        sections[i] = sec.replace(
            '<section>', f'<section id="{sec_id}">', 1)
        toc_items += f'<li><a href="#{sec_id}">{title}</a></li>\n'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Forward vs Backward — Insights</title>
<style>
:root {{
  --bg: #0b0f14;
  --panel: #111827;
  --panel2: #0f172a;
  --text: #f8fafc;
  --muted: #cbd5e1;
  --faint: #94a3b8;
  --border: #334155;
  --accent: #60a5fa;
  --accent2: #a78bfa;
  --good: #34d399;
  --warn: #fbbf24;
  --bad: #fb7185;
  --code-bg: #0a1220;
}}
*, *::before, *::after {{ box-sizing: border-box;
  margin: 0; padding: 0; }}
body {{ font-family: 'Segoe UI', system-ui, sans-serif;
  background: var(--bg); color: var(--text);
  line-height: 1.6; display: flex; }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}

nav {{ position: sticky; top: 0; width: 260px;
  height: 100vh; overflow-y: auto; padding: 1.5rem 1rem;
  border-right: 2px solid var(--border);
  background: var(--panel2); flex-shrink: 0; }}
nav h2 {{ font-size: .85rem; text-transform: uppercase;
  letter-spacing: .08em; color: var(--faint);
  margin-bottom: .75rem; }}
nav ol {{ list-style: none; counter-reset: toc; }}
nav li {{ counter-increment: toc; margin-bottom: .4rem; }}
nav li::before {{ content: counter(toc) ". ";
  color: var(--faint); font-size: .8rem; }}
nav a {{ font-size: .85rem; }}

main {{ flex: 1; max-width: 1100px; padding: 2rem 2.5rem; }}
h1 {{ font-size: 1.6rem; margin-bottom: .25rem; }}
.path {{ color: var(--faint); font-size: .85rem;
  margin-bottom: 2rem; }}
h2 {{ font-size: 1.15rem; color: var(--accent);
  margin: 2rem 0 .75rem;
  border-bottom: 2px solid var(--border);
  padding-bottom: .35rem; }}
section {{ margin-bottom: 2rem; }}
ol {{ padding-left: 1.4rem; margin: .5rem 0; }}
li {{ margin-bottom: .35rem; color: var(--muted); }}
strong {{ color: var(--text); }}

table {{ width: 100%; border-collapse: collapse;
  margin: .75rem 0; font-size: .8rem; }}
th {{ text-align: left; color: var(--faint);
  border-bottom: 2px solid var(--border);
  padding: .4rem .5rem; white-space: nowrap; }}
td {{ border-bottom: 1px solid var(--border);
  padding: .35rem .5rem; color: var(--muted); }}
tr:hover td {{ background: var(--panel); }}

@media (max-width: 800px) {{
  body {{ flex-direction: column; }}
  nav {{ position: static; width: 100%; height: auto;
    border-right: none;
    border-bottom: 2px solid var(--border); }}
}}
</style>
</head>
<body>

<nav>
<h2>Contents</h2>
<ol>
{toc_items}
</ol>
</nav>

<main>
<h1>Forward vs Backward — Insights</h1>
<div class="path">Generated from forward_vs_backward.csv</div>

{''.join(sections)}

<footer style="margin-top:2rem;padding-top:1rem;
  border-top:1px solid var(--border);
  color:var(--faint);font-size:.75rem;">
  Generated 2026-03-07.
</footer>
</main>
</body>
</html>'''

    with open(path_html, 'w', encoding='utf-8') as f:
        f.write(html)
    logging.info(f'Wrote insights HTML to {path_html}')


"""
===============================================================================
 Main - Read comparison CSV and generate insights HTML.
-------------------------------------------------------------------------------
 Input: forward_vs_backward.csv
 Output: forward_vs_backward.html
===============================================================================
"""

setup_log()

dir_exp = 'f:\\temp\\2026\\03\\Exp Depth'
path_csv = f'{dir_exp}\\forward_vs_backward.csv'
path_html = f'{dir_exp}\\forward_vs_backward.html'

rows = load_csv(path=path_csv)
analysis = _build_analysis(rows)
generate_html(analysis=analysis, path_html=path_html)
