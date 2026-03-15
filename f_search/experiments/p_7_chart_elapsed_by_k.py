from f_psl.pandas.df import UDf
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
import base64
import io

matplotlib.use('Agg')


"""
===============================================================================
 Create a visual line chart of elapsed time by k for each algorithm.
-------------------------------------------------------------------------------
 Input:  distribution_elapsed_by_k.csv (output of p_6)
 Output: chart_elapsed_by_k.html (self-contained HTML with embedded chart)
===============================================================================
"""

folder = 'f:\\temp\\2026\\03\\incremental'
path_input = f'{folder}\\distribution_elapsed_by_k.csv'
path_output = f'{folder}\\chart_elapsed_by_k.html'

# Algorithm display config
algos = {
    'elapsed_agg': {'label': 'Aggregative', 'color': '#f97316'},
    'elapsed_inc': {'label': 'Incremental', 'color': '#22d3ee'},
    'elapsed_dij': {'label': 'Dijkstra', 'color': '#a78bfa'},
}


def calc_slope(ks: list, vals: list) -> float:
    """
    ====================================================================
     Calculate the linear slope (seconds per k) using least squares.
    ====================================================================
    """
    coeffs = np.polyfit(x=ks, y=vals, deg=1)
    return round(coeffs[0], 2)


def find_crossovers(df: pd.DataFrame,
                    col_x: str,
                    col_y: str) -> list[dict]:
    """
    ====================================================================
     Find crossover points between two algorithm lines.
     Returns list of dicts with k, elapsed, labels.
    ====================================================================
    """
    ks = list(df['k'])
    xs = list(df[col_x])
    ys = list(df[col_y])
    crossovers = []
    for i in range(len(ks) - 1):
        diff_curr = xs[i] - ys[i]
        diff_next = xs[i + 1] - ys[i + 1]
        # Sign change means crossover
        if diff_curr * diff_next < 0:
            # Linear interpolation
            ratio = abs(diff_curr) / (abs(diff_curr) + abs(diff_next))
            k_cross = ks[i] + ratio * (ks[i + 1] - ks[i])
            v_cross = xs[i] + ratio * (xs[i + 1] - xs[i])
            crossovers.append(dict(
                k=round(k_cross, 1),
                elapsed=round(v_cross, 1),
                col_x=col_x,
                col_y=col_y,
            ))
    return crossovers


def build_chart_image(df: pd.DataFrame,
                      all_crossovers: list[dict]) -> str:
    """
    ====================================================================
     Build the matplotlib chart and return as base64 PNG string.
    ====================================================================
    """
    ks = list(df['k'])
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    # Plot lines
    for col, cfg in algos.items():
        vals = list(df[col])
        slope = calc_slope(ks=ks, vals=vals)
        ax.plot(ks, vals,
                color=cfg['color'],
                linewidth=2.5,
                marker='o',
                markersize=7,
                label=f'{cfg["label"]}  (slope: {slope} s/k)')
    # Annotate crossovers
    for c in all_crossovers:
        label_x = algos[c['col_x']]['label']
        label_y = algos[c['col_y']]['label']
        ax.annotate(
            f'{label_x} \u2194 {label_y}\nk={c["k"]}',
            xy=(c['k'], c['elapsed']),
            xytext=(c['k'], c['elapsed'] - 25),
            fontsize=10,
            color='#f85149',
            fontfamily='monospace',
            fontweight='bold',
            ha='center',
            arrowprops=dict(arrowstyle='->',
                            color='#f85149',
                            lw=1.5),
            bbox=dict(boxstyle='round,pad=0.4',
                      facecolor='#1c1c1c',
                      edgecolor='#f85149',
                      alpha=0.9))
    # Style axes
    ax.set_xlabel('k (Number of Goals)',
                  color='#e6edf3', fontsize=13)
    ax.set_ylabel('Elapsed Time (seconds)',
                  color='#e6edf3', fontsize=13)
    ax.tick_params(colors='#8b949e', labelsize=11)
    ax.set_xticks(ks)
    ax.grid(True, color='#21262d', linewidth=0.5)
    for spine in ax.spines.values():
        spine.set_color('#30363d')
    ax.legend(fontsize=12,
              facecolor='#161b22',
              edgecolor='#30363d',
              labelcolor='#e6edf3',
              loc='upper left')
    plt.tight_layout()
    # Encode to base64
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150,
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def build_html(df: pd.DataFrame) -> str:
    """
    ====================================================================
     Build self-contained HTML with embedded matplotlib chart.
    ====================================================================
    """
    ks = list(df['k'])
    # Find crossovers between all pairs
    pairs = [('elapsed_agg', 'elapsed_inc'),
             ('elapsed_agg', 'elapsed_dij'),
             ('elapsed_inc', 'elapsed_dij')]
    all_crossovers = []
    for col_x, col_y in pairs:
        all_crossovers.extend(
            find_crossovers(df=df, col_x=col_x, col_y=col_y)
        )
    # Build chart image
    img_b64 = build_chart_image(df=df,
                                all_crossovers=all_crossovers)
    # Build insights table rows
    insight_rows = ''
    for col, cfg in algos.items():
        vals = list(df[col])
        slope = calc_slope(ks=ks, vals=vals)
        v_min = round(min(vals), 1)
        v_max = round(max(vals), 1)
        ratio = round(v_max / v_min, 1) if v_min > 0 else 'N/A'
        insight_rows += f"""
        <tr>
          <td style="color:{cfg['color']};
                     font-weight:700">{cfg['label']}</td>
          <td>{slope} s/k</td>
          <td>{v_min}s</td>
          <td>{v_max}s</td>
          <td>{ratio}x</td>
        </tr>"""
    crossover_rows = ''
    if all_crossovers:
        for c in all_crossovers:
            label_x = algos[c['col_x']]['label']
            label_y = algos[c['col_y']]['label']
            crossover_rows += f"""
        <tr>
          <td>{label_x} &harr; {label_y}</td>
          <td>k = {c['k']}</td>
          <td>{c['elapsed']}s</td>
        </tr>"""
    else:
        crossover_rows = """
        <tr>
          <td colspan="3" style="color:#8b949e">
            No crossovers detected in this range
          </td>
        </tr>"""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Elapsed Time by K — Algorithm Comparison</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #0d1117;
    color: #e6edf3;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    padding: 30px 40px;
  }}
  h1 {{
    font-size: 32px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 4px;
    letter-spacing: -0.5px;
  }}
  .subtitle {{
    text-align: center;
    font-size: 15px;
    color: #8b949e;
    margin-bottom: 24px;
  }}
  .chart-container {{
    text-align: center;
    margin-bottom: 30px;
  }}
  .chart-container img {{
    max-width: 100%;
    border-radius: 12px;
    border: 1px solid #30363d;
  }}
  .section-title {{
    font-size: 22px;
    font-weight: 800;
    margin: 30px 0 12px;
    letter-spacing: -0.3px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    background: #161b22;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #30363d;
    margin-bottom: 20px;
  }}
  th {{
    background: #1c2129;
    padding: 12px 14px;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #8b949e;
    text-align: left;
    border-bottom: 1px solid #30363d;
  }}
  td {{
    padding: 10px 14px;
    font-size: 14px;
    border-bottom: 1px solid #21262d;
    font-variant-numeric: tabular-nums;
  }}
  tr:last-child td {{ border-bottom: none; }}
  .tables {{ display: flex; gap: 24px; }}
  .tables > div {{ flex: 1; }}
</style>
</head>
<body>
<h1>Distribution of Elapsed Time by K</h1>
<p class="subtitle">
  Mean elapsed time per algorithm, grouped by number of goals (k)
</p>
<div class="chart-container">
  <img src="data:image/png;base64,{img_b64}"
       alt="Elapsed Time by K">
</div>
<div class="tables">
  <div>
    <p class="section-title">Algorithm Slopes</p>
    <table>
      <tr>
        <th>Algorithm</th>
        <th>Slope</th>
        <th>Min</th>
        <th>Max</th>
        <th>Growth</th>
      </tr>
      {insight_rows}
    </table>
  </div>
  <div>
    <p class="section-title">Crossover Points</p>
    <table>
      <tr>
        <th>Algorithms</th>
        <th>At K</th>
        <th>Elapsed</th>
      </tr>
      {crossover_rows}
    </table>
  </div>
</div>
</body>
</html>"""
    return html


def main() -> None:
    df = UDf.read(path=path_input)
    html = build_html(df=df)
    with open(path_output, mode='w') as f:
        f.write(html)


if __name__ == '__main__':
    main()
