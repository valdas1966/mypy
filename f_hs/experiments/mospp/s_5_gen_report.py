"""
===============================================================================
 Script: regenerate `Reports/MOSPP.tex` -> Experimental Results
 section with a MULTI-CONFIG comparison.

 Reads each config's nested CSV from Drive (one CSV per
 (rule_bpmx, depth_bpmx, depth_prop) trio), aggregates, and
 emits one subsection per non-trivial counter, each
 containing:

   - a curated semantic description of the counter +
     data-driven min/max observation at k = k_max,
   - a single-axis PGFPlots line chart (N config-colored
     curves) of the per-(config, k) mean across all 25 maps,
   - a booktabs per-domain mean table at k = k_max.

 `pct_bpmx_lifts = cnt_bpmx_lifts / cnt_bpmx_attempts` is
 added as a derived per-row counter so the BPMX hit-rate
 surfaces alongside attempts/lifts.

 Missing CSVs are skipped with a warning (so the script can
 run incrementally as configs come in).

 Each line chart / toy grid is EXTERNALIZED: rendered to a
 standalone `fig_<metric>.pdf` (and `fig_toy.pdf`) up front,
 then \\includegraphics-ed by the main doc. This keeps PGFPlots
 off the main -- and Overleaf -- compile path (10 inline axes
 were overrunning Overleaf's compile timeout; the same doc
 builds in ~2.5s under `tectonic` locally).

 After splicing the section into `Reports/MOSPP.tex` it
 compiles via `tectonic`, uploads `.tex` + `.pdf` to Drive
 (the `.pdf` embeds the figures, so Drive stays a 2-file
 artifact -- the loose `fig_*.pdf` live only in the work dir
 and on Overleaf, which needs them to recompile), and pushes a
 sanitized `.tex` + the `fig_*.pdf` set to the Overleaf `MOSPP`
 project (`f_overleaf` text upload is ASCII-only --
 box-drawing chars in comments are replaced).

 Run:
   PYTHONPATH=/mnt/f/mypy \
   python f_hs/experiments/mospp/s_5_gen_report.py
===============================================================================
"""
import shutil
import subprocess
import tempfile
from pathlib import Path

import pandas as pd

from f_google.services.drive import Drive
from f_overleaf import OverLeaf

from f_hs.experiments.mospp.report_spec import (
    RULE_SECTIONS, K_TABLE, _EXCLUDED_COUNTERS,
)
from f_hs.experiments.mospp.report_render import (
    add_derived_columns, metric_columns, build_section,
    sanitize_ascii,
)


PATH_TEX_DRIVE = 'Reports/MOSPP.tex'
PATH_PDF_DRIVE = 'Reports/MOSPP.pdf'
OVERLEAF_PROJECT = 'MOSPP'
OVERLEAF_FILE = 'MOSPP.tex'

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


# ── Main ────────────────────────────────────────────────────────────────────

def main(rules: list[str] | None = None,
         push_overleaf: bool = True) -> None:
    """
    ===========================================================================
     Generate the experimental sections as an `\\input`-split
     report (no splice): one file per BPMX rule
     (rule1/rule2/rule3/cascade.tex) that the human-owned
     `report/main.tex` `\\input`s. The generator never touches
     main.tex; git is the source of truth.

     `rules`: which rules' FIGURES to (re)compile (e.g.
     `['rule2']`); None = all rendered. The per-rule .tex files
     are always rewritten (instant); only the requested rules'
     figures are recompiled, the rest are reused from the
     persistent fig cache (and stay on Overleaf). That is what
     makes a single-rule update touch one file + its figures
     instead of regenerating the whole report.
    ===========================================================================
    """
    report_dir = Path(__file__).resolve().parent / 'report'
    fig_dir = Path('/tmp/mospp_figs')
    fig_dir.mkdir(parents=True, exist_ok=True)
    drive = Drive.Factory.valdas()
    work = Path(tempfile.mkdtemp(prefix='mospp_s5_', dir='/tmp'))
    print(f'work {work} | report {report_dir} | figs {fig_dir}')

    # 1. Download every UNIQUE CSV once (baseline shared by all
    #    rule sections). Missing CSVs are skipped.
    print('downloading CSVs ...')
    frames: dict[str, pd.DataFrame] = {}
    seen: set[str] = set()
    for sec in RULE_SECTIONS:
        for c in sec['configs']:
            if c['tag'] in seen:
                continue
            seen.add(c['tag'])
            if not drive.is_exists(path=c['csv']):
                print(f"  MISSING — {c['tag']}")
                continue
            local = work / (c['tag'] + '.csv')
            drive.download(path_src=c['csv'], path_dest=str(local))
            d = pd.read_csv(local)
            d['config'] = c['tag']
            frames[c['tag']] = d
            print(f"  OK     — {c['tag']} ({len(d):,} rows)")
    if not frames:
        raise RuntimeError('No CSVs found on Drive.')

    # 2. Build each rule's section -> write report/<key>.tex. A
    #    rule renders only when >=1 of its depth CSVs is present.
    print('writing per-rule section files ...')
    fig_specs: dict[str, str] = {}
    rendered: list[str] = []
    for sec in RULE_SECTIONS:
        used = [c for c in sec['configs'] if c['tag'] in frames]
        if not [c for c in used if c['tag'] != 'rule_none']:
            print(f"  skip '{sec['key']}' — no depth CSVs")
            continue
        df = add_derived_columns(
            pd.concat([frames[c['tag']] for c in used],
                      ignore_index=True))
        metric_cols = metric_columns(df)
        nontrivial = ({m for m in metric_cols
                       if float(df[m].astype(float).max()) > 0}
                      - _EXCLUDED_COUNTERS)
        k_max = int(df['m'].max())
        per_kc = (df.groupby(['config', 'm'])[metric_cols]
                  .mean().reset_index())
        k_values = [k for k in K_TABLE if k <= k_max]
        sec_tex, sec_figs = build_section(
            per_kc=per_kc, used=used, nontrivial=nontrivial,
            k_values=k_values, rule_key=sec['key'],
            section_title=sec['title'])
        (report_dir / f"{sec['key']}.tex").write_text(
            sec_tex + '\n', encoding='utf-8')
        for name, src in sec_figs:
            fig_specs[name] = src
        rendered.append(sec['key'])
        print(f"  wrote report/{sec['key']}.tex ({len(sec_figs)} figs)")
    if not rendered:
        raise RuntimeError('No rule sections had depth data.')

    main_tex = report_dir / 'main.tex'
    if not main_tex.exists():
        raise FileNotFoundError(
            f'{main_tex} missing — the human-owned main.tex '
            f'(preamble + sections 1-2 + the \\input list) must exist.')

    # 3. Compile figures — SELECTIVE. `rules=None` -> all rendered;
    #    else only the listed rules' figures (the rest are reused
    #    from the persistent cache + Overleaf).
    todo = set(rules) if rules is not None else set(rendered)
    to_build = [(n, s) for n, s in fig_specs.items()
                if any(n.startswith(f'fig_{k}_') for k in todo)]
    print(f'compiling {len(to_build)} figures (rules={sorted(todo)}) ...')
    for name, src in to_build:
        (work / f'{name}.tex').write_text(src, encoding='utf-8')
        subprocess.run(['tectonic', f'{name}.tex'],
                       check=True, cwd=str(work))
        shutil.copy(work / f'{name}.pdf', fig_dir / f'{name}.pdf')
        print(f'  OK     — {name}.pdf')

    # 4. Validate: compile main.tex with every rendered rule's
    #    figures (from the persistent cache).
    val = Path(tempfile.mkdtemp(prefix='mospp_val_', dir='/tmp'))
    shutil.copy(main_tex, val / 'main.tex')
    for key in rendered:
        shutil.copy(report_dir / f'{key}.tex', val / f'{key}.tex')
    missing = [n for n in fig_specs
               if not (fig_dir / f'{n}.pdf').exists()]
    if missing:
        raise RuntimeError(
            'figure cache incomplete — run once with rules=None: '
            f'{missing[:5]}')
    for name in fig_specs:
        shutil.copy(fig_dir / f'{name}.pdf', val / f'{name}.pdf')
    print('compiling main.tex (validation) ...')
    subprocess.run(['tectonic', 'main.tex'], check=True, cwd=str(val))
    print(f'  pdf: {(val / "main.pdf").stat().st_size:,} bytes')

    # 5. Push the \input-split report to Overleaf (multi-file):
    #    main.tex + each rendered rule file + ONLY the (re)built
    #    figures (others stay on Overleaf).
    if push_overleaf:
        print('pushing to Overleaf ...')
        proj = OverLeaf.Factory.valdas()[OVERLEAF_PROJECT]

        def _up(path: str, p: Path) -> None:
            txt, _ = sanitize_ascii(p.read_text(encoding='utf-8'))
            if any(ord(c) > 127 for c in txt):
                raise ValueError(f'non-ASCII in {path}')
            proj.create_file(path=path, text=txt)

        _up('main.tex', main_tex)
        for key in rendered:
            _up(f'{key}.tex', report_dir / f'{key}.tex')
        for name, _ in to_build:
            proj.upload_file(path_src=str(fig_dir / f'{name}.pdf'),
                             path_dest=f'{name}.pdf')
        proj.set_root_doc('main.tex')
        if 'MOSPP.tex' in proj.list_files():
            proj.delete_file(path='MOSPP.tex')
        print(f'  pushed main.tex + {len(rendered)} rule files + '
              f'{len(to_build)} figs; root=main.tex')
    print('done.')


if __name__ == '__main__':
    import sys
    # `python s_5_gen_report.py`              -> recompile ALL figures.
    # `python s_5_gen_report.py rule2`        -> recompile only rule2's
    #                                            figures (others reused);
    #                                            every .tex is rewritten.
    main(rules=sys.argv[1:] or None)
