"""
================================================================
 Unit tests for `report_render` -- the pure render functions of
 the MOSPP BPMX-depth report. Pins the subtle, correctness-
 critical logic that has silently confused readers before:
 the mean-of-ratios `pct_bpmx_lifts`, the uniform `elapsed_*`
 table format, the magnitude-tiered `fmt_cell`, and the
 coincident-curve merge. No I/O -- all inputs are inline.
================================================================
"""
import numpy as np
import pandas as pd

from f_hs.experiments.mospp import report_render as R
from f_hs.experiments.mospp import report_spec as S


def test_fmt_cell() -> None:
    """
    ========================================================================
     `fmt_cell` is magnitude-tiered: >=1000 comma-int, >=100 int,
     >=1 two-decimal, <1 three-sig-fig; 0 and non-finite special.
    ========================================================================
    """
    assert R.fmt_cell(285235.4) == '285,235'
    assert R.fmt_cell(160.7) == '161'
    assert R.fmt_cell(14.99) == '14.99'
    assert R.fmt_cell(0.0234) == '0.0234'
    assert R.fmt_cell(0) == '0'
    assert R.fmt_cell(float('inf')) == '—'


def test_fmt_value_elapsed_is_uniform_two_decimal() -> None:
    """
    ========================================================================
     `elapsed_*` cells are uniform 2-decimal regardless of
     magnitude -- a time table must not mix `119` with `78.33`.
    ========================================================================
    """
    assert R.fmt_value('elapsed_total', 118.783) == '118.78'
    assert R.fmt_value('elapsed_total', 78.3327) == '78.33'
    # contrast: the generic formatter would integer-ize >=100
    assert R.fmt_cell(118.783) == '119'


def test_fmt_value_pct_suffix() -> None:
    """
    ========================================================================
     `pct_*` cells append a LaTeX percent sign; other metrics
     delegate to `fmt_cell` unchanged.
    ========================================================================
    """
    assert R.fmt_value('pct_bpmx_lifts', 16.9971) == r'17.00\%'
    assert R.fmt_value('cnt_expanded', 285235.4) == '285,235'


def test_should_log_decade_rule() -> None:
    """
    ========================================================================
     Log-y only when the positive dynamic range exceeds one
     decade (max/min > 10); fewer than two positives -> linear.
    ========================================================================
    """
    assert R.should_log(np.array([1.0, 100.0])) is True
    assert R.should_log(np.array([1.0, 9.0])) is False
    assert R.should_log(np.array([0.0, 5.0])) is False


def test_heat_hex_endpoints() -> None:
    """
    ========================================================================
     `heat_hex` maps t=0 -> green (smallest), t=0.5 -> yellow,
     t=1 -> red (largest), per the Excel 3-color convention.
    ========================================================================
    """
    g = '{:02X}{:02X}{:02X}'.format(*S._HEAT_GREEN)
    y = '{:02X}{:02X}{:02X}'.format(*S._HEAT_YELLOW)
    r = '{:02X}{:02X}{:02X}'.format(*S._HEAT_RED)
    assert R.heat_hex(0.0) == g
    assert R.heat_hex(0.5) == y
    assert R.heat_hex(1.0) == r


def test_heat_cell_constant_column_unshaded() -> None:
    """
    ========================================================================
     A flat column (vmax == vmin) carries no signal -> no shade;
     otherwise vmin shades green, vmax shades red.
    ========================================================================
    """
    assert R.heat_cell(5.0, 5.0, 5.0) == ''
    assert R.heat_cell(1.0, 1.0, 9.0).endswith(
        '{' + R.heat_hex(0.0) + '}')
    assert R.heat_cell(9.0, 1.0, 9.0).endswith(
        '{' + R.heat_hex(1.0) + '}')


def test_pct_bpmx_lifts_is_mean_of_ratios() -> None:
    """
    ========================================================================
     `pct_bpmx_lifts` is a PER-ROW rate (lifts/attempts), so the
     across-map mean is the unweighted mean-of-ratios -- which
     deliberately differs from the size-weighted ratio-of-means.
     0/0 rows -> 0%. This is the property that confused the
     report (charted pct != charted-lifts / charted-attempts).
    ========================================================================
    """
    df = pd.DataFrame({
        'cnt_bpmx_lifts':    [50.0, 10.0, 0.0],
        'cnt_bpmx_attempts': [100.0, 1000.0, 0.0],
    })
    out = R.add_derived_columns(df.copy())

    per_row = out['pct_bpmx_lifts'].tolist()
    expected = [50.0, 1.0, 0.0]
    assert per_row == expected

    mean_of_ratios = float(out['pct_bpmx_lifts'].mean())
    ratio_of_means = (df['cnt_bpmx_lifts'].sum()
                      / df['cnt_bpmx_attempts'].sum() * 100.0)
    assert round(mean_of_ratios, 2) == 17.0
    assert round(ratio_of_means, 2) == 5.45
    assert abs(mean_of_ratios - ratio_of_means) > 1.0


def test_coincident_groups_merges_identical_series() -> None:
    """
    ========================================================================
     Configs with a bit-identical (k -> value) series are merged
     into one curve group; a distinct series stays its own group.
    ========================================================================
    """
    used = [{'tag': 'a', 'label': 'depth=0'},
            {'tag': 'b', 'label': 'depth=1'},
            {'tag': 'c', 'label': 'depth=2'}]
    rows = []
    for tag, vals in [('a', [1.0, 2.0]), ('b', [1.0, 2.0]),
                      ('c', [9.0, 8.0])]:
        for m, v in zip([10, 20], vals):
            rows.append({'config': tag, 'm': m, 'cnt_expanded': v})
    per_kc = pd.DataFrame(rows)

    groups = R._coincident_groups(per_kc, 'cnt_expanded', used)
    expected = [[0, 1], [2]]
    assert groups == expected

    label = R._group_label(groups[0], used)
    assert label == 'depth=0/1'


def test_build_insight_boxed_and_rule_fallback() -> None:
    """
    ========================================================================
     `build_insight` renders a numbered `sentences` list inside
     the lightblue `insights` box from
     `_INSIGHT_ITEMS[rule][metric]`; an uncurated (rule, counter)
     -- e.g. rule_3 before its data lands -- falls back to the
     rule-agnostic `_COUNTER_NEUTRAL` one-liner.
    ========================================================================
    """
    box = R.build_insight('cnt_expanded')            # default rule1
    assert r'\begin{insights}' in box
    assert r'\begin{sentences}' in box
    assert R._INSIGHT_ITEMS['rule1']['cnt_expanded'][0] in box
    fallback = R.build_insight('cnt_expanded', rule_key='rule3')
    assert r'\begin{insights}' in fallback
    assert R._COUNTER_NEUTRAL['cnt_expanded'] in fallback


def test_build_single_figure_externalizes_plot() -> None:
    """
    ========================================================================
     The line chart is EXTERNALIZED to dodge Overleaf's compile
     timeout: the figure float \\includegraphics-es `fig_<metric>`
     (no inline axis), and the returned standalone source is a
     self-contained `standalone` doc carrying the PGFPlots axis +
     the per-config color definitions it references.
    ========================================================================
    """
    used = [{'tag': 'a', 'label': 'depth=0', 'color': '6BAED6'},
            {'tag': 'b', 'label': 'depth=1', 'color': '4292C6'}]
    rows = []
    for tag, vals in [('a', [10.0, 20.0]), ('b', [5.0, 8.0])]:
        for m, v in zip([10, 20], vals):
            rows.append({'config': tag, 'm': m, 'cnt_expanded': v})
    per_kc = pd.DataFrame(rows)

    figure, (name, standalone) = R.build_single_figure(
        'cnt_expanded', per_kc, used)

    assert name == 'fig_cnt_expanded'
    # Float references the externalized PDF, not an inline plot.
    assert r'\includegraphics{fig_cnt_expanded}' in figure
    assert r'\begin{axis}' not in figure
    # Standalone is self-contained and carries the plot.
    assert r'\documentclass[border=3pt]{standalone}' in standalone
    assert r'\begin{axis}' in standalone
    assert r'\addplot' in standalone
    # cfgcolor defs travel into the standalone preamble.
    assert r'\definecolor{cfgcolor0}{HTML}{6BAED6}' in standalone


def test_diff_annotations_label_is_x_multiplier() -> None:
    """
    ========================================================================
     The k=100/200 gap label is a `Nx` multiplier (ratio of the two
     highest lines), never a percentage -- so it is unambiguous
     about direction and cannot disagree with a caption's framing.
    ========================================================================
    """
    used = [{'tag': 'a', 'label': 'depth=0'},
            {'tag': 'b', 'label': 'depth=1'}]
    rows = []
    # top line 'a' = 2x the second line 'b' at both annotated k.
    for tag, val in [('a', 200.0), ('b', 100.0)]:
        for k in (100, 200):
            rows.append({'config': tag, 'm': k, 'cnt_expanded': val})
    per_kc = pd.DataFrame(rows)

    out = R._diff_annotations(per_kc, 'cnt_expanded', used, is_log=False)
    assert r'2.00$\times$' in out
    assert r'\%' not in out
    # The d= line-id tag no longer rides on the gap span -- it now
    # lives once at the line's left start (see _start_labels).
    assert 'd=0' not in out


def test_start_labels_only_when_gap_and_placed_at_start() -> None:
    """
    ========================================================================
     Line-id tags are decided at the MIDDLE k (=100) and drawn at
     the line's left START (k=10): the topmost line is always
     tagged; a lower line only when it sits >=1.1x below the line
     immediately above it at the middle k.
    ========================================================================
    """
    used = [{'tag': 'a', 'label': 'depth=0'},
            {'tag': 'b', 'label': 'depth=1'},
            {'tag': 'c', 'label': 'depth=2'}]
    series = {
        'a': {10: 30.0, 100: 300.0, 200: 600.0},
        'b': {10: 29.0, 100: 290.0, 200: 580.0},
        'c': {10: 20.0, 100: 200.0, 200: 400.0},
    }
    rows = [{'config': tag, 'm': k, 'cnt_expanded': v}
            for tag, kv in series.items() for k, v in kv.items()]
    per_kc = pd.DataFrame(rows)

    out = R._start_labels(per_kc, 'cnt_expanded', used, is_log=False)
    # d=0 top -> tagged; d=2 is 290/200 = 1.45x below its neighbour
    # -> tagged; d=1 is only 300/290 = 1.03x below d=0 -> not.
    assert 'd=0' in out
    assert 'd=2' in out
    assert 'd=1' not in out
    # Tags sit at the LEFT start (k=10) at each line's start value,
    # never at the middle/right k.
    assert r'(axis cs:10,30)' in out
    assert r'(axis cs:10,20)' in out
    assert r'(axis cs:100,' not in out


def test_start_labels_merge_coincident_into_one_tag() -> None:
    """
    ========================================================================
     Coincident configs share one curve, so they carry one combined
     start tag (e.g. d=0/1), not one per config.
    ========================================================================
    """
    used = [{'tag': 'a', 'label': 'depth=0'},
            {'tag': 'b', 'label': 'depth=1'},
            {'tag': 'c', 'label': 'depth=2'}]
    series = {
        'a': {10: 30.0, 100: 300.0, 200: 600.0},
        'b': {10: 30.0, 100: 300.0, 200: 600.0},
        'c': {10: 20.0, 100: 200.0, 200: 400.0},
    }
    rows = [{'config': tag, 'm': k, 'cnt_expanded': v}
            for tag, kv in series.items() for k, v in kv.items()]
    per_kc = pd.DataFrame(rows)

    out = R._start_labels(per_kc, 'cnt_expanded', used, is_log=False)
    assert 'd=0/1' in out
    assert 'd=2' in out
