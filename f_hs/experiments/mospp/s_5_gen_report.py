"""
===============================================================================
 Script: regenerate `Reports/MOSPP.tex` -> Experimental Results
 section with a MULTI-CONFIG comparison.

 Reads each config's by-k aggregate from Drive `Results/agg/`
 (one `*_by_k.csv` per (rule_bpmx, depth_bpmx, depth_prop)
 trio, produced by `s_4` -- already one row per (config, k)
 with every metric meaned across the 25 maps and the derived
 `pct_bpmx_lifts` baked in). `s_4` is the single aggregation
 authority; this script no longer downloads the raw per-map
 CSVs or re-aggregates -- it tags, concatenates, and renders.
 Emits one subsection per non-trivial counter, each
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

 NO PC TRACES. The generator writes nothing into the repo:
 `report/main.tex` (the human-owned `\\input` host) is READ-ONLY;
 every generated artifact -- per-rule `.tex`, figure
 `.tex`/`.pdf`, downloaded aggregates, compiled `main.pdf` --
 lives in ONE `/tmp` scratch dir that is wiped on exit. Outputs
 land only on:
   - Overleaf `MOSPP`: sanitized `main.tex` + rule `.tex` +
     the `fig_*.pdf` set (`f_overleaf` upload is ASCII-only --
     box-drawing chars in comments are replaced), and
   - Drive `Reports/`: the compiled `MOSPP.pdf` + the `\\input`
     bundle (`MOSPP.tex` + each rule `.tex`), kept recompilable.
 No persistent figure cache -> every figure is rebuilt per run.

 Run (reads s_4 aggregates from Drive + compiles + pushes):
   PYTHONPATH=/Users/eyalberkovich/mypy \
   python f_hs/experiments/mospp/s_5_gen_report.py [--no-push]
===============================================================================
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

from f_google.services.drive import Drive
from f_overleaf import OverLeaf

from f_hs.experiments.mospp.report_spec import (
    RULE_SECTIONS, K_TABLE, _EXCLUDED_COUNTERS,
)
from f_hs.experiments.mospp.report_render import (
    metric_columns, build_section, sanitize_ascii,
)


def _tectonic_bin() -> str:
    """
    ========================================================================
     Resolve the `tectonic` executable robustly. `subprocess`
     inherits the launcher's PATH -- which, when the script is
     run from an IDE or a non-base conda env (e.g. `mypy`), often
     EXCLUDES the conda-base `bin/` where tectonic is installed.
     Try PATH first (`shutil.which`), then the usual installs:
     this env, conda base (`envs/<x>/.. -> base`), cargo,
     homebrew. Fail with an actionable message if none exist.
    ========================================================================
    """
    exe = shutil.which('tectonic')
    if exe:
        return exe
    prefix = Path(sys.prefix)
    candidates = [
        prefix / 'bin' / 'tectonic',                  # this env
        prefix.parent.parent / 'bin' / 'tectonic',    # conda base
        Path.home() / '.cargo' / 'bin' / 'tectonic',  # cargo
        Path('/opt/homebrew/bin/tectonic'),           # brew (arm)
        Path('/usr/local/bin/tectonic'),              # brew (intel)
    ]
    for c in candidates:
        if c.is_file():
            return str(c)
    raise FileNotFoundError(
        'tectonic not found on PATH or in the usual locations. '
        'Install it (e.g. `conda install -n mypy -c conda-forge '
        'tectonic`) or add it to PATH.')


PATH_TEX_DRIVE = 'Reports/MOSPP.tex'
PATH_PDF_DRIVE = 'Reports/MOSPP.pdf'
OVERLEAF_PROJECT = 'MOSPP'
OVERLEAF_FILE = 'MOSPP.tex'

# ── Main ────────────────────────────────────────────────────────────────────

def main(push_overleaf: bool = True) -> None:
    """
    ===========================================================================
     Generate the experimental sections as an `\\input`-split
     report (no splice): one file per BPMX rule
     (rule1/rule2/rule3/cascade.tex) that the human-owned
     `report/main.tex` `\\input`s.

     **No PC traces.** The generator NEVER writes into the repo:
     `report/main.tex` is the only repo file and it is READ-ONLY
     (the human-owned source). Every generated artifact -- the
     per-rule `.tex`, the figure `.tex`/`.pdf`, the downloaded
     aggregates, the compiled `main.pdf` -- lives in a single
     `/tmp` scratch dir that is WIPED on exit (success or error).
     Outputs go only to **Overleaf** (`.tex` sources + figure
     PDFs) and **Drive** (`Reports/MOSPP.{tex,pdf}` + rule
     `.tex`). Nothing is left on disk.

     Because nothing is cached between runs, EVERY figure is
     recompiled each run (the prior selective-recompile cache is
     gone -- the trade for leaving no trace). `push_overleaf` is
     the only knob; Drive upload always happens.
    ===========================================================================
    """
    report_dir = Path(__file__).resolve().parent / 'report'
    main_tex_src = report_dir / 'main.tex'
    if not main_tex_src.exists():
        raise FileNotFoundError(
            f'{main_tex_src} missing — the human-owned main.tex '
            f'(preamble + sections 1-2 + the \\input list) must exist.')
    tectonic = _tectonic_bin()        # fail fast before any Drive work
    drive = Drive.Factory.valdas()
    # Single scratch dir under /tmp -- every generated artifact
    # lives here and the whole dir is wiped in `finally`. Nothing
    # is ever written into the repo / PC.
    work = Path(tempfile.mkdtemp(prefix='mospp_s5_', dir='/tmp'))
    print(f'scratch {work} (wiped on exit) | main.tex {main_tex_src}')
    try:
        # 1. Download every UNIQUE by-k aggregate once (baseline
        #    shared by all rule sections). Missing aggregates are
        #    skipped -- run `s_4` first if a config is absent.
        print('downloading s_4 by-k aggregates ...')
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
            raise RuntimeError(
                'No by-k aggregates on Drive — run s_4 first.')

        # 2. Build each rule's section -> write work/<key>.tex (NOT
        #    the repo). A rule renders only when >=1 depth CSV is
        #    present.
        print('writing per-rule section files (to scratch) ...')
        fig_specs: dict[str, str] = {}
        rendered: list[str] = []
        for sec in RULE_SECTIONS:
            used = [c for c in sec['configs'] if c['tag'] in frames]
            if not [c for c in used if c['tag'] != 'rule_none']:
                print(f"  skip '{sec['key']}' — no depth CSVs")
                continue
            # The frames are already `s_4` by-k aggregates: one row
            # per (config, k), every metric meaned, `pct_bpmx_lifts`
            # baked in. Tagged with `config` on load -> the concat
            # IS `per_kc`. No re-aggregation / derived step here.
            per_kc = pd.concat([frames[c['tag']] for c in used],
                               ignore_index=True)
            metric_cols = metric_columns(per_kc)
            nontrivial = ({m for m in metric_cols
                           if float(per_kc[m].astype(float).max()) > 0}
                          - _EXCLUDED_COUNTERS)
            k_max = int(per_kc['m'].max())
            k_values = [k for k in K_TABLE if k <= k_max]
            sec_tex, sec_figs = build_section(
                per_kc=per_kc, used=used, nontrivial=nontrivial,
                k_values=k_values, rule_key=sec['key'],
                section_title=sec['title'])
            (work / f"{sec['key']}.tex").write_text(
                sec_tex + '\n', encoding='utf-8')
            for name, src in sec_figs:
                fig_specs[name] = src
            rendered.append(sec['key'])
            print(f"  wrote {sec['key']}.tex ({len(sec_figs)} figs)")
        if not rendered:
            raise RuntimeError('No rule sections had depth data.')

        # 3. Compile EVERY figure into the scratch dir (no
        #    persistent cache -> all rebuilt each run).
        print(f'compiling {len(fig_specs)} figures ...')
        for name, src in fig_specs.items():
            (work / f'{name}.tex').write_text(src, encoding='utf-8')
            subprocess.run([tectonic, f'{name}.tex'],
                           check=True, cwd=str(work))
            print(f'  OK     — {name}.pdf')

        # 4. Compile main.tex in the scratch dir (main + rule files
        #    + figure PDFs all co-located). main.tex is COPIED in,
        #    never edited in the repo.
        shutil.copy(main_tex_src, work / 'main.tex')
        print('compiling main.tex ...')
        subprocess.run([tectonic, 'main.tex'],
                       check=True, cwd=str(work))
        pdf = work / 'main.pdf'
        print(f'  pdf: {pdf.stat().st_size:,} bytes')

        # 5. Push the \input-split report to Overleaf: main.tex +
        #    every rendered rule file + every figure PDF.
        if push_overleaf:
            print('pushing to Overleaf ...')
            # `with` -> the Overleaf session is closed on block exit
            # (success or error). Each file op's realtime socket is
            # also closed at the source (ProjectOverLeaf._root), so
            # no phantom online 'me' viewers are left behind.
            with OverLeaf.Factory.valdas() as ol:
                proj = ol[OVERLEAF_PROJECT]

                def _up(path: str, p: Path) -> None:
                    txt, _ = sanitize_ascii(
                        p.read_text(encoding='utf-8'))
                    if any(ord(c) > 127 for c in txt):
                        raise ValueError(f'non-ASCII in {path}')
                    proj.create_file(path=path, text=txt)

                _up('main.tex', main_tex_src)
                for key in rendered:
                    _up(f'{key}.tex', work / f'{key}.tex')
                for name in fig_specs:
                    proj.upload_file(
                        path_src=str(work / f'{name}.pdf'),
                        path_dest=f'{name}.pdf')
                proj.set_root_doc('main.tex')
                if 'MOSPP.tex' in proj.list_files():
                    proj.delete_file(path='MOSPP.tex')
            print(f'  pushed main.tex + {len(rendered)} rule files + '
                  f'{len(fig_specs)} figs; root=main.tex '
                  f'(session closed)')

        # 6. Upload the compiled report to Drive: the self-contained
        #    PDF + the \input bundle (main.tex + rule files), so
        #    Reports/ stays recompilable. main.tex from the repo
        #    source; rule files from scratch.
        print('uploading to Drive ...')
        drive.upload(path_src=str(pdf), path_dest=PATH_PDF_DRIVE)
        drive.upload(path_src=str(main_tex_src), path_dest=PATH_TEX_DRIVE)
        for key in rendered:
            drive.upload(path_src=str(work / f'{key}.tex'),
                         path_dest=f'Reports/{key}.tex')
        print(f'  {PATH_PDF_DRIVE} + {PATH_TEX_DRIVE} + '
              f'{len(rendered)} rule .tex')
        print('done.')
    finally:
        # Leave NO trace: wipe the scratch dir + any legacy fig
        # cache from the pre-"no-PC-traces" design.
        shutil.rmtree(work, ignore_errors=True)
        legacy = Path('/tmp/mospp_figs')
        if legacy.exists():
            shutil.rmtree(legacy, ignore_errors=True)
        print(f'cleaned scratch {work}')


if __name__ == '__main__':
    # `python s_5_gen_report.py`            -> Overleaf + Drive.
    # `python s_5_gen_report.py --no-push`  -> Drive only (skip the
    #                                          Overleaf push; safe
    #                                          first look that can't
    #                                          overwrite Overleaf).
    main(push_overleaf='--no-push' not in sys.argv)
