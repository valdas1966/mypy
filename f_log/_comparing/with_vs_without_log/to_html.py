import csv
from pathlib import Path


_DIR = Path(__file__).parent
_CSV = _DIR / 'results.csv'
_HTML = _DIR / 'results.html'


def _read_csv() -> list[dict]:
    with open(_CSV) as f:
        return list(csv.DictReader(f))


def _ratio(a: float, b: float) -> str:
    if b == 0:
        return 'n/a'
    return f'{a / b:.1f}x'


def _build_html(rows: list[dict]) -> str:
    # ── Table rows: elapsed times ──
    time_rows = ''
    for r in rows:
        n = int(r['iterations'])
        time_rows += (
            f'<tr>'
            f'<td class="iter">{n:,}</td>'
            f'<td class="no-log">{r["no_log"]}</td>'
            f'<td class="disabled">{r["disabled"]}</td>'
            f'<td class="console">{r["console"]}</td>'
            f'<td class="file">{r["file"]}</td>'
            f'</tr>\n'
        )

    # ── Table rows: overhead ratios ──
    ratio_rows = ''
    for r in rows:
        n = int(r['iterations'])
        no = float(r['no_log'])
        dis = float(r['disabled'])
        con = float(r['console'])
        fil = float(r['file'])
        ratio_rows += (
            f'<tr>'
            f'<td class="iter">{n:,}</td>'
            f'<td class="no-log">baseline</td>'
            f'<td class="disabled">{_ratio(dis, no)}</td>'
            f'<td class="console">{_ratio(con, dis)}</td>'
            f'<td class="file">{_ratio(fil, con)}</td>'
            f'</tr>\n'
        )

    # ── Bar chart rows ──
    bar_rows = ''
    for r in rows:
        n = int(r['iterations'])
        no = float(r['no_log'])
        dis = float(r['disabled'])
        con = float(r['console'])
        fil = float(r['file'])
        max_val = fil
        def pct(v: float) -> float:
            return max((v / max_val) * 100, 0.5)
        bar_rows += f'''\
<tr>
  <td class="iter">{n:,}</td>
  <td>
    <div class="bar-group">
      <div class="bar no-log-bar"
           style="width:{pct(no):.1f}%">
        <span>{r["no_log"]}s</span>
      </div>
      <div class="bar disabled-bar"
           style="width:{pct(dis):.1f}%">
        <span>{r["disabled"]}s</span>
      </div>
      <div class="bar console-bar"
           style="width:{pct(con):.1f}%">
        <span>{r["console"]}s</span>
      </div>
      <div class="bar file-bar"
           style="width:{pct(fil):.1f}%">
        <span>{r["file"]}s</span>
      </div>
    </div>
  </td>
</tr>
'''

    # ── Averages for insights ──
    avg_dis_vs_no = sum(
        float(r['disabled']) / max(float(r['no_log']), 1e-9)
        for r in rows
    ) / len(rows)
    avg_con_vs_dis = sum(
        float(r['console']) / max(float(r['disabled']), 1e-9)
        for r in rows
    ) / len(rows)
    avg_fil_vs_con = sum(
        float(r['file']) / max(float(r['console']), 1e-9)
        for r in rows
    ) / len(rows)
    avg_fil_vs_no = sum(
        float(r['file']) / max(float(r['no_log']), 1e-9)
        for r in rows
    ) / len(rows)

    return f'''\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Logging Performance Results</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  background: #0f0f1a; color: #ccc;
  font-family: 'Consolas','Fira Code',monospace;
  padding: 28px 36px; line-height: 1.6;
}}
h1 {{
  color: #00d4ff; font-size: 22px;
  border-bottom: 2px solid #00d4ff;
  padding-bottom: 8px; margin-bottom: 6px;
}}
.subtitle {{
  color: #666; font-size: 12px; margin-bottom: 28px;
}}
h2 {{
  color: #00d4ff; font-size: 16px;
  margin: 28px 0 12px 0;
  border-left: 3px solid #00d4ff;
  padding-left: 10px;
}}
table {{
  border-collapse: collapse; width: 100%;
  max-width: 750px; margin-bottom: 8px;
}}
th {{
  background: #16213e; color: #00d4ff;
  padding: 9px 12px; text-align: right;
  border-bottom: 2px solid #00d4ff;
  font-size: 12px;
}}
th:first-child {{ text-align: left; }}
td {{
  padding: 7px 12px; text-align: right;
  border-bottom: 1px solid #1a1a3a;
  font-size: 12px;
}}
.iter {{
  text-align: left; color: #888;
  font-weight: bold;
}}
tr:hover {{ background: #16213e; }}
.no-log    {{ color: #6bcb77; }}
.disabled  {{ color: #ffd93d; }}
.console   {{ color: #ff9f43; }}
.file      {{ color: #ff6b6b; }}

/* Bar chart */
.bar-table {{ max-width: 750px; }}
.bar-table td {{ vertical-align: top; padding: 6px 12px; }}
.bar-table td:last-child {{ width: 85%; }}
.bar-group {{ display: flex; flex-direction: column; gap: 3px; }}
.bar {{
  height: 20px; border-radius: 3px;
  display: flex; align-items: center;
  padding-left: 6px; min-width: 60px;
  font-size: 11px; color: #fff;
  transition: width 0.3s;
}}
.bar span {{ white-space: nowrap; }}
.no-log-bar    {{ background: #6bcb77; }}
.disabled-bar  {{ background: #ffd93d; color: #222; }}
.console-bar   {{ background: #ff9f43; }}
.file-bar      {{ background: #ff6b6b; }}

/* Insights */
.insights {{
  max-width: 750px;
  background: #16213e;
  border: 1px solid #2a2a5a;
  border-radius: 6px;
  padding: 18px 22px;
  margin-top: 24px;
}}
.insights h2 {{
  margin: 0 0 12px 0;
  border: none; padding: 0;
}}
.insights ul {{
  list-style: none; padding: 0;
}}
.insights li {{
  padding: 5px 0;
  border-bottom: 1px solid #1a1a3a;
  font-size: 13px;
}}
.insights li:last-child {{ border: none; }}
.tag {{
  display: inline-block; padding: 1px 8px;
  border-radius: 3px; font-size: 11px;
  font-weight: bold; margin-right: 6px;
}}
.tag-safe  {{ background: #6bcb77; color: #111; }}
.tag-warn  {{ background: #ffd93d; color: #111; }}
.tag-danger {{ background: #ff6b6b; color: #fff; }}
.rec {{
  max-width: 750px;
  background: #1a2a1a;
  border: 1px solid #3a5a3a;
  border-radius: 6px;
  padding: 18px 22px;
  margin-top: 16px;
  font-size: 13px;
}}
.rec h2 {{
  margin: 0 0 10px 0;
  border: none; padding: 0;
  color: #6bcb77;
}}
.rec code {{
  background: #0f0f1a; padding: 2px 6px;
  border-radius: 3px; color: #ffd93d;
}}
</style>
</head>
<body>

<h1>Logging Performance: 4 Methods Compared</h1>
<div class="subtitle">
  Measuring overhead of log.debug() with 2+2 computation
  per iteration
</div>

<h2>Elapsed Time (seconds)</h2>
<table>
<tr>
  <th>Iterations</th>
  <th>No-Log</th>
  <th>Disabled</th>
  <th>Console</th>
  <th>File</th>
</tr>
{time_rows}</table>

<h2>Overhead Ratio (vs previous tier)</h2>
<table>
<tr>
  <th>Iterations</th>
  <th>No-Log</th>
  <th>Disabled / No-Log</th>
  <th>Console / Disabled</th>
  <th>File / Console</th>
</tr>
{ratio_rows}</table>

<h2>Visual Comparison</h2>
<table class="bar-table">
<tr>
  <th>Iterations</th>
  <th>Elapsed (proportional bars)</th>
</tr>
{bar_rows}</table>

<div class="insights">
  <h2>Key Findings</h2>
  <ul>
    <li>
      <span class="tag tag-safe">SAFE</span>
      <strong>Disabled vs No-Log:</strong>
      ~{avg_dis_vs_no:.0f}x overhead.
      Having <code>log.debug()</code> calls with logging
      disabled adds negligible cost.
    </li>
    <li>
      <span class="tag tag-warn">MODERATE</span>
      <strong>Console vs Disabled:</strong>
      ~{avg_con_vs_dis:.0f}x overhead.
      Active console logging adds significant cost
      due to string formatting and stream I/O.
    </li>
    <li>
      <span class="tag tag-danger">HEAVY</span>
      <strong>File vs Console:</strong>
      ~{avg_fil_vs_con:.0f}x overhead.
      File logging with rotation is the most expensive
      due to synchronous disk writes.
    </li>
    <li>
      <span class="tag tag-danger">TOTAL</span>
      <strong>File vs No-Log:</strong>
      ~{avg_fil_vs_no:,.0f}x total overhead.
      File logging is orders of magnitude slower
      than code without any logging.
    </li>
  </ul>
</div>

<div class="rec">
  <h2>Recommendations</h2>
  <p>
    1. <strong>Keep your log statements</strong> in the code.
       With <code>setup(enabled=False)</code>, the overhead
       is minimal (~{avg_dis_vs_no:.0f}x) and not worth
       stripping calls from hot paths.<br><br>
    2. <strong>Use <code>DEBUG</code> level wisely.</strong>
       In production, set level to <code>WARNING</code>
       or higher. Messages below the level threshold are
       skipped before formatting — near-zero cost.<br><br>
    3. <strong>Prefer console over file</strong> when possible.
       Console sink is ~{avg_fil_vs_con:.0f}x faster than
       file sink. Pipe stdout to a file externally
       if you need persistence.<br><br>
    4. <strong>For high-throughput loops</strong>,
       disable logging or guard with
       <code>if log.isEnabledFor(DEBUG)</code> to avoid
       even the function-call overhead.
  </p>
</div>

</body>
</html>'''


rows = _read_csv()
html = _build_html(rows=rows)
_HTML.write_text(data=html, encoding='utf-8')
print(f'\033[32mHTML saved: {_HTML}\033[0m')
