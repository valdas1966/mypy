"""
===============================================================================
 Script: regenerate `Reports/MOSPP.tex` -> Experimental Results
 section with a MULTI-CONFIG comparison.

 Reads each config's nested CSV from Drive (one CSV per
 (rule_bpmx, depth_bpmx, depth_prop) trio), aggregates, and
 emits:

   - ONE PGFPlots groupplots figure with one panel per
     non-trivial counter; each panel carries N curves, one
     per config, color-coded along a gradient (gray for the
     BPMX-off baseline; light-to-dark blue for the rule=1
     depth ladder).
   - ONE booktabs table per non-trivial counter: rows are
     configs, columns are 5 domains + an overall column;
     each cell is the mean across the 5 maps of that domain
     at k = k_max.

 Missing CSVs are skipped with a warning (so the script can
 run incrementally as configs come in).

 After splicing the section into `Reports/MOSPP.tex` it
 compiles via `tectonic`, uploads `.tex` + `.pdf` to Drive,
 and pushes a sanitized `.tex` to the Overleaf `MOSPP`
 project (`f_overleaf` upload is ASCII-only --
 box-drawing chars in comments are replaced).

 Run:
   PYTHONPATH=/mnt/f/mypy \
   python f_hs/experiments/mospp/s_5_gen_report.py
===============================================================================
"""
import os
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

from f_google.services.drive import Drive
from f_overleaf import OverLeaf


PATH_TEX_DRIVE = 'Reports/MOSPP.tex'
PATH_PDF_DRIVE = 'Reports/MOSPP.pdf'
OVERLEAF_PROJECT = 'MOSPP'
OVERLEAF_FILE = 'MOSPP.tex'


# ── Configs to compare (order = legend / table-row order) ───────────────────
# Color gradient: gray baseline + light→dark blue for rule_1 depth ladder.
CONFIGS = [
    {'tag':   'rule_none',
     'label': r'rule=none ($d{=}\infty$)',
     'csv':   ('Experiments/MOSPP/'
               'astar_inc_nested__rule_none__bpmx_inf__prop_0.csv'),
     'color': '808080'},
    {'tag':   'rule_1__d_1',
     'label': r'rule=1, $d{=}1$',
     'csv':   ('Experiments/MOSPP/'
               'astar_inc_nested__rule_1__bpmx_1__prop_0.csv'),
     'color': 'A6CEE3'},
    {'tag':   'rule_1__d_2',
     'label': r'rule=1, $d{=}2$',
     'csv':   ('Experiments/MOSPP/'
               'astar_inc_nested__rule_1__bpmx_2__prop_0.csv'),
     'color': '6FB0DA'},
    {'tag':   'rule_1__d_3',
     'label': r'rule=1, $d{=}3$',
     'csv':   ('Experiments/MOSPP/'
               'astar_inc_nested__rule_1__bpmx_3__prop_0.csv'),
     'color': '3F95D3'},
    {'tag':   'rule_1__d_4',
     'label': r'rule=1, $d{=}4$',
     'csv':   ('Experiments/MOSPP/'
               'astar_inc_nested__rule_1__bpmx_4__prop_0.csv'),
     'color': '1F77B4'},
    {'tag':   'rule_1__d_5',
     'label': r'rule=1, $d{=}5$',
     'csv':   ('Experiments/MOSPP/'
               'astar_inc_nested__rule_1__bpmx_5__prop_0.csv'),
     'color': '1A5A8C'},
    {'tag':   'rule_1__d_inf',
     'label': r'rule=1, $d{=}\infty$',
     'csv':   ('Experiments/MOSPP/'
               'astar_inc_nested__rule_1__bpmx_inf__prop_0.csv'),
     'color': '0F2A48'},
]

COUNTER_GROUPS = [
    ('Search',      ['cnt_expanded', 'cnt_generated']),
    ('Propagation', ['cnt_prop_attempts', 'cnt_prop_lifts',
                     'cnt_prop_waves']),
    ('BPMX',        ['cnt_bpmx_attempts', 'cnt_bpmx_lifts',
                     'cnt_bpmx_depth']),
    ('Heuristic',   ['cnt_h_search']),
    ('Frontier',    ['cnt_push', 'cnt_pop', 'cnt_decrease']),
    ('Reuse',       ['cnt_cache_hits_at_init']),
    ('Memory',      ['mem_open', 'mem_closed', 'mem_cache',
                     'mem_bounds', 'mem_total']),
    ('Time',        ['elapsed_total', 'elapsed_search',
                     'elapsed_update']),
]

# Counters intentionally hidden from the report (author choice).
# These would otherwise be auto-included (non-trivial across some
# configs) but the user has chosen to omit them. Listed under
# "Omitted (excluded by author choice)" in the setup paragraph.
_EXCLUDED_COUNTERS: set[str] = {
    'cnt_h_search',
    'cnt_push',
    'cnt_pop',
    'cnt_generated',
    'mem_cache',
    'mem_bounds',
    'elapsed_search',
}


# ── Helpers ─────────────────────────────────────────────────────────────────

def tex_esc(s: str) -> str:
    """Escape underscores for LaTeX text."""
    return s.replace('_', r'\_')


def fmt_cell(v) -> str:
    """Compact numeric formatting for table cells."""
    try:
        v = float(v)
    except (TypeError, ValueError):
        return str(v)
    if not np.isfinite(v):
        return '—'
    if v == 0:
        return '0'
    a = abs(v)
    if a >= 1e5:
        return f'{v:.2e}'
    if a >= 100:
        return f'{v:.0f}'
    if a >= 1:
        return f'{v:.2f}'
    return f'{v:.3g}'


def should_log(values: np.ndarray) -> bool:
    pos = values[values > 0]
    if len(pos) < 2:
        return False
    return float(pos.max()) / float(pos.min()) > 10.0


# ── Load + aggregate ────────────────────────────────────────────────────────

def load_configs(drive: Drive,
                 configs: list[dict],
                 work: Path) -> tuple[pd.DataFrame, list[dict]]:
    """
    ========================================================================
     Download each available CSV; combine into one DataFrame
     with a `config` column carrying the tag. Skip missing
     CSVs with a warning. Return (df, configs_used).
    ========================================================================
    """
    frames = []
    used = []
    for cfg in configs:
        if not drive.is_exists(path=cfg['csv']):
            print(f"  MISSING — skip {cfg['tag']}: {cfg['csv']}")
            continue
        local = work / (cfg['tag'] + '.csv')
        drive.download(path_src=cfg['csv'], path_dest=str(local))
        d = pd.read_csv(local)
        d['config'] = cfg['tag']
        frames.append(d)
        used.append(cfg)
        print(f"  OK     — {cfg['tag']} ({len(d):,} rows)")
    if not frames:
        raise RuntimeError('No CSVs found on Drive.')
    return pd.concat(frames, ignore_index=True), used


def metric_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns
            if c.startswith(('cnt_', 'mem_', 'elapsed_'))]


# ── Figure (multi-config, one panel per counter) ────────────────────────────

def panel_addplots(per_kc: pd.DataFrame,
                   metric: str,
                   used: list[dict]) -> str:
    """One \\addplot per config (color-coded by named color)."""
    lines = []
    for idx, cfg in enumerate(used):
        sub = (per_kc[per_kc['config'] == cfg['tag']]
               .sort_values('m'))
        coords = ' '.join(
            f'({int(k)},{float(v):.6g})'
            for k, v in zip(sub['m'], sub[metric]))
        lines.append(
            rf"\addplot[color=cfgcolor{idx}, "
            rf"mark=*, mark size=1.0pt, very thick] "
            rf"coordinates {{{coords}}};")
    return '\n'.join(lines)


def color_definitions(used: list[dict]) -> str:
    """`\\definecolor{cfgcolorN}{HTML}{RRGGBB}` for every config.
    Named refs are the safe xcolor syntax (inline `{HTML,...}`
    is rejected by xcolor's color-name parser)."""
    return '\n'.join(
        rf"\definecolor{{cfgcolor{idx}}}{{HTML}}{{{cfg['color']}}}"
        for idx, cfg in enumerate(used))


def build_figure(per_kc: pd.DataFrame,
                 nontrivial: set[str],
                 used: list[dict]) -> str:
    panels: list[tuple[str, str]] = []
    for _, metrics in COUNTER_GROUPS:
        for m in metrics:
            if m in nontrivial:
                panels.append((m, m))
    n = len(panels)
    n_cols = 3
    n_rows = (n + n_cols - 1) // n_cols

    blocks = []
    for idx, (_, metric) in enumerate(panels):
        vals = per_kc[metric].astype(float).to_numpy()
        ymode = 'ymode=log,' if should_log(vals) else ''
        # Add legend on the first panel only.
        legend_cmd = ''
        legend_attr = ''
        if idx == 0:
            entries = ', '.join(cfg['label'] for cfg in used)
            legend_attr = (
                r'legend style={font=\tiny, fill=white, '
                r'fill opacity=0.9, draw=secgray, '
                r'at={(0.02,0.98)}, anchor=north west}, '
                r'legend cell align=left,'
            )
            legend_cmd = f'\n\\legend{{{entries}}}'
        data = panel_addplots(per_kc, metric, used)
        blocks.append(
            f'\\nextgroupplot[title={{\\texttt{{{tex_esc(metric)}}}}}, '
            f'{ymode} {legend_attr}]\n{data}{legend_cmd}')

    body = '\n'.join(blocks)
    color_defs = color_definitions(used)
    return rf"""{color_defs}
\begin{{figure}}[H]
\centering
\begin{{tikzpicture}}
\pgfplotsset{{
    every axis/.append style={{
        width=5.8cm, height=4.4cm,
        xlabel={{$k$}},
        grid=both,
        tick label style={{font=\scriptsize}},
        label style={{font=\scriptsize}},
        title style={{font=\small, yshift=-2pt}},
        every axis plot/.append style={{line width=0.9pt}},
    }}
}}
\begin{{groupplot}}[
    group style={{group size={n_cols} by {n_rows},
                  horizontal sep=1.55cm,
                  vertical sep=1.30cm}},
]
{body}
\end{{groupplot}}
\end{{tikzpicture}}
\caption{{\textbf{{Per-counter means vs.~$k$.}}\\
Each panel = one counter; each curve = one BPMX config (rule
+ cascade depth); $y$ is the arithmetic mean across all
25~maps (5 maps $\times$ 5 domains) at the given~$k$; log-$y$
where the dynamic range exceeds one order of magnitude.}}
\end{{figure}}
"""


# ── Tables (one per counter) ────────────────────────────────────────────────

def build_table_for_metric(per_dom: pd.DataFrame,
                           overall: pd.DataFrame,
                           used: list[dict],
                           metric: str,
                           domains: list[str],
                           k_max: int) -> str:
    head = ' & '.join(
        ['config']
        + [rf'\textbf{{{tex_esc(d)}}}' for d in domains]
        + [r'\textbf{overall}']
    )
    rows = []
    for cfg in used:
        cells = []
        for d in domains:
            mask = ((per_dom['config'] == cfg['tag'])
                    & (per_dom['domain'] == d))
            v = (float(per_dom.loc[mask, metric].iloc[0])
                 if mask.any() else 0.0)
            cells.append(fmt_cell(v))
        ov_mask = overall['config'] == cfg['tag']
        ov = (float(overall.loc[ov_mask, metric].iloc[0])
              if ov_mask.any() else 0.0)
        cells.append(fmt_cell(ov))
        rows.append(rf'  {cfg["label"]} & ' + ' & '.join(cells) + r' \\')
    n_cols = len(domains) + 2
    align = 'l' + 'r' * (n_cols - 1)
    return rf"""\begin{{table}}[H]
\centering
\caption{{\textbf{{\texttt{{{tex_esc(metric)}}} --- per-domain mean
at $k={k_max}$.}}\\Rows are BPMX configs; columns are the 5 Moving-AI
domains plus an overall mean across all 25~maps.}}
\small
\setlength{{\tabcolsep}}{{4pt}}
\begin{{tabular}}{{{align}}}
\toprule
{head} \\
\midrule
{chr(10).join(rows)}
\bottomrule
\end{{tabular}}
\end{{table}}
"""


# ── Section assembly ────────────────────────────────────────────────────────

def build_section(df: pd.DataFrame,
                  per_kc: pd.DataFrame,
                  per_dom: pd.DataFrame,
                  overall: pd.DataFrame,
                  used: list[dict],
                  metric_cols: list[str],
                  nontrivial: set[str],
                  omitted_user: list[str],
                  domains: list[str],
                  k_max: int) -> str:
    cfg_lines = ', '.join(cfg['label'] for cfg in used)
    setup = rf"""\section{{Experimental Results --- BPMX depth ladder}}

\paragraph{{Setup.}} \texttt{{AStarIncMOSPP}} compared across
{len(used)}~BPMX configs ({cfg_lines}); shared:
\texttt{{depth\_prop=0}}, \texttt{{order\_starts='given'}},
\texttt{{carry\_cache=True}}, \texttt{{carry\_bounds=False}}.
Problem set: 500~OMSPP instances ($=$ 5~domains $\times$
5~maps $\times$ 20~$k$-values $\in
\{{10, 20, \ldots, 200\}}$, Moving~AI grids), flipped to
MOSPP via \texttt{{ProblemSPP.flipped()}}. CSVs are
nested-chain output: each row is the cumulative counter
state after $k$ starts on its map.
"""
    omitted_zero = sorted(set(metric_cols)
                          - nontrivial
                          - set(omitted_user))
    if omitted_zero:
        setup += (rf"""
\paragraph{{Omitted (uniformly zero across every config).}}
""" + ', '.join(rf'\texttt{{{tex_esc(m)}}}' for m in omitted_zero)
                  + '.\n')
    if omitted_user:
        setup += (rf"""
\paragraph{{Omitted (excluded by author choice).}}
""" + ', '.join(rf'\texttt{{{tex_esc(m)}}}' for m in omitted_user)
                  + '.\n')

    fig = build_figure(per_kc, nontrivial, used)

    table_blocks = []
    for _, metrics in COUNTER_GROUPS:
        for m in metrics:
            if m in nontrivial:
                table_blocks.append(
                    build_table_for_metric(
                        per_dom=per_dom, overall=overall,
                        used=used, metric=m,
                        domains=domains, k_max=k_max))

    tables = '\n\n'.join(table_blocks)
    return '\n\n'.join([
        setup,
        r'\paragraph{Per-counter line charts (means across all 25 maps).}',
        fig,
        r'\paragraph{Per-counter tables (means at $k=k_{\max}$, per domain).}',
        tables,
    ])


# ── Splice into MOSPP.tex ───────────────────────────────────────────────────

def splice(tex: str, new_section: str) -> str:
    # 1. Add pgfplots packages if missing.
    pkg_block = ('\\usepackage{pgfplots}\n'
                 '\\pgfplotsset{compat=1.18}\n'
                 '\\usepgfplotslibrary{groupplots}\n')
    if r'\usepackage{pgfplots}' not in tex:
        tex = tex.replace(
            '\\usepackage{float}',
            '\\usepackage{float}\n' + pkg_block,
            1)
    # 2. Add the mandatory \me / \you block if missing.
    me_block = (
        '\n% -- Author annotations (draft only) --\n'
        '\\newif\\ifdraft\\drafttrue\n'
        '\\newcommand{\\me}[1]{%\n'
        '    \\ifdraft\\textcolor{red}{\\textbf{[me:\\,#1]}}\\fi%\n'
        '}\n'
        '\\newcommand{\\you}[1]{%\n'
        '    \\ifdraft\\textcolor{blue}{\\textbf{[you:\\,#1]}}\\fi%\n'
        '}\n'
    )
    if '\\newcommand{\\me}' not in tex:
        tex = tex.replace(
            '\\begin{document}',
            me_block + '\n\\begin{document}',
            1)
    # 3. Idempotent: strip the prior "Experimental Results"
    #    section if present, then insert the new one before
    #    \end{document}.
    for marker in (
            r'\section{Experimental Results --- BPMX depth ladder}',
            r'\section{Experimental Results}'):
        if marker in tex:
            i = tex.index(marker)
            j = tex.index('\\end{document}', i)
            tex = tex[:i] + tex[j:]
            break
    tex = tex.replace(
        '\\end{document}',
        new_section + '\n\n\\end{document}',
        1)
    return tex


def sanitize_ascii(text: str) -> tuple[str, dict[str, int]]:
    """ASCII-only sanitizer for Overleaf upload."""
    counts = {c: text.count(c) for c in ['─', '═']}
    text = text.replace('─', '-').replace('═', '=')
    return text, counts


# ── Main ────────────────────────────────────────────────────────────────────

def main(push_drive: bool = True,
         push_overleaf: bool = True) -> None:
    drive = Drive.Factory.valdas()
    work = Path(tempfile.mkdtemp(prefix='mospp_s5_', dir='/tmp'))
    print(f'work dir: {work}')

    print('downloading CSVs ...')
    df, used = load_configs(drive=drive, configs=CONFIGS, work=work)
    metric_cols = metric_columns(df)
    nontrivial_all = {m for m in metric_cols
                      if float(df[m].astype(float).max()) > 0}
    omitted_user = sorted(nontrivial_all & _EXCLUDED_COUNTERS)
    nontrivial = nontrivial_all - _EXCLUDED_COUNTERS
    domains = sorted(df['domain'].astype(str).unique())
    k_max = int(df['m'].max())
    print(f'  {len(used)} configs, {len(domains)} domains, '
          f'{len(metric_cols)} metrics '
          f'({len(nontrivial_all)} non-trivial, '
          f'{len(omitted_user)} excluded by author, '
          f'{len(nontrivial)} active); '
          f'k_max = {k_max}')

    print('aggregating ...')
    per_kc = (df.groupby(['config', 'm'])[metric_cols]
              .mean().reset_index())
    at_max = df[df['m'] == k_max]
    per_dom = (at_max.groupby(['config', 'domain'])[metric_cols]
               .mean().reset_index())
    overall = at_max.groupby('config')[metric_cols].mean().reset_index()

    print('building section ...')
    section = build_section(
        df=df, per_kc=per_kc, per_dom=per_dom, overall=overall,
        used=used, metric_cols=metric_cols, nontrivial=nontrivial,
        omitted_user=omitted_user, domains=domains, k_max=k_max)

    print('downloading MOSPP.tex + splicing ...')
    tex_path = work / 'MOSPP.tex'
    drive.download(path_src=PATH_TEX_DRIVE,
                   path_dest=str(tex_path))
    tex = tex_path.read_text()
    tex = splice(tex, section)
    tex_path.write_text(tex)

    print('compiling via tectonic ...')
    subprocess.run(['tectonic', str(tex_path)],
                   check=True, cwd=str(work))
    pdf_path = tex_path.with_suffix('.pdf')
    print(f'pdf size: {pdf_path.stat().st_size:,} bytes')

    if push_drive:
        print('uploading to Drive ...')
        drive.upload(path_src=str(tex_path),
                     path_dest=PATH_TEX_DRIVE)
        drive.upload(path_src=str(pdf_path),
                     path_dest=PATH_PDF_DRIVE)
        print(f'  {PATH_TEX_DRIVE}')
        print(f'  {PATH_PDF_DRIVE}')

    if push_overleaf:
        print('pushing to Overleaf ...')
        overleaf = OverLeaf.Factory.valdas()
        if OVERLEAF_PROJECT not in overleaf:
            project = overleaf.create_project(name=OVERLEAF_PROJECT)
            print(f'  created Overleaf project {OVERLEAF_PROJECT!r} '
                  f'(key={project.key})')
        else:
            project = overleaf[OVERLEAF_PROJECT]
            print(f'  reusing Overleaf project {OVERLEAF_PROJECT!r} '
                  f'(key={project.key})')
        sanitized, sc = sanitize_ascii(tex)
        if any(ord(c) > 127 for c in sanitized):
            raise ValueError(
                'sanitized text still has non-ASCII; abort')
        print(f'  sanitized chars: {sc}')
        project.create_file(path=OVERLEAF_FILE, text=sanitized)
        project.set_root_doc(name=OVERLEAF_FILE)
        if 'main.tex' in project.list_files():
            project.delete_file(path='main.tex')
        print(f'  pushed: {OVERLEAF_PROJECT}/{OVERLEAF_FILE}')

    print('done.')


if __name__ == '__main__':
    main(push_drive=True, push_overleaf=True)
