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
import subprocess
import tempfile
from pathlib import Path

import pandas as pd

from f_google.services.drive import Drive
from f_overleaf import OverLeaf

from f_hs.experiments.mospp.report_spec import (
    CONFIGS, K_TABLE, _EXCLUDED_COUNTERS,
)
from f_hs.experiments.mospp.report_render import (
    add_derived_columns, metric_columns, build_section,
    splice, sanitize_ascii,
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

def main(push_drive: bool = True,
         push_overleaf: bool = True) -> None:
    drive = Drive.Factory.valdas()
    work = Path(tempfile.mkdtemp(prefix='mospp_s5_', dir='/tmp'))
    print(f'work dir: {work}')

    print('downloading CSVs ...')
    df, used = load_configs(drive=drive, configs=CONFIGS, work=work)
    df = add_derived_columns(df)
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
    overall = at_max.groupby('config')[metric_cols].mean().reset_index()
    k_values = [k for k in K_TABLE if k <= k_max]

    print('building section ...')
    section, figures = build_section(
        df=df, per_kc=per_kc, overall=overall,
        used=used, metric_cols=metric_cols, nontrivial=nontrivial,
        omitted_user=omitted_user, k_values=k_values, k_max=k_max)

    # Externalized figures: compile each PGFPlots/TikZ figure to a
    # standalone PDF in the work dir BEFORE the main compile, so the
    # main doc only \includegraphics them (no PGFPlots on the main --
    # or Overleaf -- compile path; that is what blew the timeout).
    print(f'rendering {len(figures)} externalized figures ...')
    for name, src in figures:
        (work / f'{name}.tex').write_text(src, encoding='utf-8')
        subprocess.run(['tectonic', f'{name}.tex'],
                       check=True, cwd=str(work))
        print(f'  OK     — {name}.pdf')

    print('downloading MOSPP.tex + splicing ...')
    tex_path = work / 'MOSPP.tex'
    drive.download(path_src=PATH_TEX_DRIVE,
                   path_dest=str(tex_path))
    tex = tex_path.read_text(encoding='utf-8')
    tex = splice(tex, section)
    tex_path.write_text(tex, encoding='utf-8')

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
        # Refresh externalized figures: drop any stale fig_*.pdf
        # (a counter dropping out of the report would otherwise
        # leave an orphan), then upload the current set so Overleaf
        # \includegraphics-es PDFs instead of re-running PGFPlots.
        existing = project.list_files()
        for f in existing:
            if f.startswith('fig_') and f.endswith('.pdf'):
                project.delete_file(path=f)
        for name, _ in figures:
            project.upload_file(path_src=str(work / f'{name}.pdf'),
                                path_dest=f'{name}.pdf')
        print(f'  pushed {len(figures)} figures')
        project.set_root_doc(name=OVERLEAF_FILE)
        if 'main.tex' in existing:
            project.delete_file(path='main.tex')
        print(f'  pushed: {OVERLEAF_PROJECT}/{OVERLEAF_FILE}')

    print('done.')


if __name__ == '__main__':
    main(push_drive=True, push_overleaf=True)
