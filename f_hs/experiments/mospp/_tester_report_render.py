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


def test_build_insight_minmax_observation() -> None:
    """
    ========================================================================
     `build_insight` appends a data-driven min/max observation at
     k_max; a uniform-value metric gets the description only.
    ========================================================================
    """
    used = [{'tag': 'a', 'label': 'depth=0'},
            {'tag': 'b', 'label': 'depth=1'}]
    overall = pd.DataFrame({
        'config': ['a', 'b'],
        'cnt_expanded': [285235.0, 146114.0],
    })
    insight = R.build_insight('cnt_expanded', overall, used, k_max=200)
    assert R._COUNTER_INFO['cnt_expanded'] in insight
    assert 'min $= 146,114$ (depth=1)' in insight
    assert 'max $= 285,235$ (depth=0)' in insight
