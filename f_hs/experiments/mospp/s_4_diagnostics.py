"""
===============================================================================
 Script: experiment-adequacy diagnostics for `s_3` nested CSVs.

 Answers the methodology questions documented in
 `2026/05/22/mospp_session.md` ("Methodology — sample size &
 diversity"): is the 25-map × 20-k sample enough? Is the
 k=10..200 range wide enough? Do conclusions need per-domain
 stratification? What is the honest effective N once
 intra-cluster correlation is acknowledged?
-------------------------------------------------------------------------------
 Seven diagnostics, all computed on an existing nested
 `astar_inc_nested__*.csv` (no new experiments). Each consumes
 the same long-format DataFrame (one row per (map, k) stage,
 columns include `domain` / `map` / `m` + counter / mem /
 elapsed metrics).

 (1) Per-domain summaries
       For each (domain, metric), summary stats (n, mean,
       median, p25, p75, p90, max) over the per-map endpoint
       (the cumulative value at the chain's last k).
 (2) Per-chain Δ_k saturation
       Δ_k = row[k] − row[k-10] per (map, metric, k).
       Saturation verdict: mean Δ over k ∈ {180,190,200} vs
       k ∈ {20,30,40}. < 10 % ⇒ k-range adequate.
 (3) Cross-map cumulative-mean
       Per metric, take the per-map endpoint values; randomly
       shuffle R=200 times; for each shuffle compute the
       running mean for N = 1..n_maps. Report mean and std of
       running means across shuffles. Verdict: smallest N
       where σ_N / |μ_max| < 5 % is the stability point.
 (4) Intra-cluster ρ + effective N
       Per (map, metric), lag-1 autocorrelation across the
       k-stages. Mean ρ across maps gives the design-effect
       N_eff = N_total / (1 + (m−1)·ρ) — the honest
       independent-sample count behind the 500-row table.
 (5) Variance decomposition (η²)
       Fraction of variance in per-map endpoint explained by
       `domain`. > 0.5 ⇒ per-domain reporting mandatory.
 (6) Half-split consistency
       R random splits of the n_maps into two equal halves;
       median / p75 of |mean(half A) − mean(half B)| relative
       to the full-sample mean. Robust ⇒ < 5 %.
 (7) Bootstrap-CI extrapolation
       Bootstrap 95 % CI half-width on the mean at current N
       (B=2000 resamples). Extrapolate to N' = current × {1,
       2, 4, 10, 20} via the textbook CLT 1/√N rule:
         `hw(N') = hw(n) · √(n / N')`.
       Compute `n_required` — the smallest N at which the
       predicted half-width ≤ 5 % · |μ|. The headline answer
       to "do I need another 500 in-distribution maps?".
-------------------------------------------------------------------------------
 Inputs  (Drive)
   `Experiments/MOSPP/astar_inc_nested__*.csv` — the nested
   per-(map,k) CSV produced by `s_3`.

 Outputs (Drive)
   `Experiments/MOSPP/diagnostics/{stem}__report.md`
       Markdown summary with verdicts and small tables (1, 4,
       5, 6, 7). The headline read.
   `Experiments/MOSPP/diagnostics/{stem}__deltas.csv`
       Long-format Δ_k: (domain, map, metric, k, delta). Feeds
       per-chain saturation plots.
   `Experiments/MOSPP/diagnostics/{stem}__cumulative_mean.csv`
       Per (metric, N): mean_of_running_means,
       std_of_running_means, std_rel_to_final. Feeds cross-map
       saturation plots.
   `Experiments/MOSPP/diagnostics/{stem}__ci_extrapolation.csv`
       Per (metric, mult): N, hw_absolute, hw_relative,
       n_required. Feeds the "how much more data?" curve.

 Run:
   `python -m f_hs.experiments.mospp.s_4_diagnostics`
   (set `path_drive_csv_in` / `metrics` / `R` in `__main__`).
===============================================================================
"""
import os
import tempfile
import logging
from typing import Iterable

import numpy as np
import pandas as pd

from f_log import setup_log, get_log
from f_google.services.drive import Drive


setup_log(sink='console', level=logging.INFO)
_log = get_log(__name__)


# ── Defaults ────────────────────────────────────────────────────────────────

# Headline metrics — small enough to read at a glance, broad
# enough to cover the experiment's main axes (work / reuse /
# wall time / memory).
_DEFAULT_METRICS: tuple[str, ...] = (
    'cnt_expanded',
    'cnt_cache_hits_at_init',
    'elapsed_total',
    'mem_total',
)
# Within-chain saturation tolerance: late-Δ / early-Δ ratio.
_SAT_TOL_REL = 0.10
# Cross-map cumulative-mean stability tolerance:
# σ_N / |μ_max| < CROSS_TOL ⇒ stable.
_CROSS_TOL_REL = 0.05
# Half-split robustness tolerance: median |Δ| / mean < ε ⇒ robust.
_HALF_TOL_REL = 0.05
# Shufflings for stochastic diagnostics (cumulative-mean,
# half-split). 200 is plenty for 25 maps; cheap.
_R_SHUFFLES = 200
# Bootstrap resamples for the CI half-width at current N
# (Diagnostic 7). 2000 is the textbook default for 95% CI.
_BOOTSTRAP_B = 2000
# Target relative CI half-width for the "how many more maps?"
# verdict in Diagnostic 7 (5 % of |μ|).
_TARGET_REL_CI = 0.05
# Multipliers (× current N) for the CI-extrapolation table:
# current → 2× → 4× → 10× → 20×. The 1/√N rule shrinks the CI
# by √(mult) at each step.
_EXTRAPOLATION_MULTIPLIERS: tuple[int, ...] = (1, 2, 4, 10, 20)
_RANDOM_SEED = 0


# ── Domain inference from Moving AI grid names ──────────────────────────────

def _infer_domain(grid_name: str) -> str:
    """
    ========================================================================
     Map a Moving AI grid_name to its domain bucket. Idempotent
     fallback when the CSV's `domain` column is empty (the
     experiment writes `getattr(problem.grid, 'domain', '')`,
     which is empty for these grids).
    ========================================================================
    """
    n = grid_name
    if 'room_' in n:
        return 'rooms'
    if n.startswith('maze512'):
        return 'maze512'
    if n.startswith('random512'):
        return 'random512'
    if n in ('Berlin_2_1024', 'London_1_1024', 'Moscow_1_1024',
             'NewYork_0_1024', 'Paris_0_1024'):
        return 'cities'
    # Moving AI Dragon Age maps: short name ending in 'd'
    # (brc503d, den000d, hrt000d, lak405d, ost100d).
    if n.endswith('d') and len(n) <= 8:
        return 'dragon_age'
    return 'unknown'


def _ensure_domain(df: pd.DataFrame) -> pd.DataFrame:
    """
    ========================================================================
     Ensure `df['domain']` carries a non-empty Moving AI bucket
     for every row. Overrides empty / missing values via
     `_infer_domain(map)`.
    ========================================================================
    """
    df = df.copy()
    if 'domain' not in df.columns:
        df['domain'] = ''
    df['domain'] = df['domain'].fillna('').astype(str)
    empty = df['domain'] == ''
    if empty.any():
        df.loc[empty, 'domain'] = df.loc[empty, 'map'].map(_infer_domain)
    return df


# ── Per-chain endpoint extractor (shared by several diagnostics) ────────────

def _endpoints(df: pd.DataFrame) -> pd.DataFrame:
    """
    ========================================================================
     One row per map: the last stage (max m) of each chain.
     The cumulative value at the chain's endpoint is the
     natural per-map summary number.
    ========================================================================
    """
    return df.sort_values('m').groupby('map', as_index=False).tail(1).copy()


# ── (1) Per-domain summaries ────────────────────────────────────────────────

def _diag_per_domain(df: pd.DataFrame,
                     metrics: Iterable[str]) -> pd.DataFrame:
    """
    ========================================================================
     For each (domain, metric), summary stats over per-map
     endpoint values.
    ========================================================================
    """
    end = _endpoints(df)
    rows = []
    for metric in metrics:
        for dom, grp in end.groupby('domain'):
            v = grp[metric].astype(float).to_numpy()
            rows.append({
                'metric': metric,
                'domain': dom,
                'n_maps': int(len(v)),
                'mean':   float(np.mean(v)),
                'median': float(np.median(v)),
                'p25':    float(np.percentile(v, 25)),
                'p75':    float(np.percentile(v, 75)),
                'p90':    float(np.percentile(v, 90)),
                'max':    float(np.max(v)),
            })
    return pd.DataFrame(rows)


# ── (2) Per-chain Δ_k saturation ────────────────────────────────────────────

def _diag_deltas(df: pd.DataFrame,
                 metrics: Iterable[str]) -> pd.DataFrame:
    """
    ========================================================================
     Δ_k = row[k] − row[k-10] per (map, metric, k). Long-format
     output: domain, map, metric, k, delta.
    ========================================================================
    """
    rows = []
    for (dom, mp), grp in df.groupby(['domain', 'map']):
        grp = grp.sort_values('m').reset_index(drop=True)
        ks = grp['m'].astype(int).to_numpy()
        for metric in metrics:
            vals = grp[metric].astype(float).to_numpy()
            for i in range(1, len(vals)):
                rows.append({
                    'domain': dom, 'map': mp, 'metric': metric,
                    'k':      int(ks[i]),
                    'delta':  float(vals[i] - vals[i - 1]),
                })
    return pd.DataFrame(rows)


def _saturation_verdicts(deltas: pd.DataFrame,
                         metrics: Iterable[str],
                         tol: float) -> dict:
    """
    ========================================================================
     Per metric, fraction of maps where Δ_k saturates: mean Δ
     at k ∈ {180,190,200} is < `tol` × mean Δ at k ∈
     {20,30,40}. Handles missing tail (when a chain is short)
     by skipping that map.
    ========================================================================
    """
    verdicts = {}
    early_ks = np.array([20, 30, 40])
    late_ks = np.array([180, 190, 200])
    for metric in metrics:
        sub = deltas[deltas['metric'] == metric]
        n_sat = 0
        n_total = 0
        per_map: dict[str, float] = {}
        for mp, grp in sub.groupby('map'):
            ks = grp['k'].astype(int).to_numpy()
            d = grp['delta'].astype(float).to_numpy()
            e_mask = np.isin(ks, early_ks)
            l_mask = np.isin(ks, late_ks)
            if not e_mask.any() or not l_mask.any():
                continue
            early = float(np.mean(d[e_mask]))
            late = float(np.mean(d[l_mask]))
            if abs(early) < 1e-12:
                ratio = 0.0
            else:
                ratio = late / early
            per_map[mp] = ratio
            n_total += 1
            if abs(ratio) < tol:
                n_sat += 1
        verdicts[metric] = {
            'n_saturated': n_sat,
            'n_total':     n_total,
            'frac':        (n_sat / n_total) if n_total else 0.0,
            'per_map':     per_map,
        }
    return verdicts


# ── (3) Cross-map cumulative-mean ───────────────────────────────────────────

def _diag_cumulative_mean(df: pd.DataFrame,
                          metrics: Iterable[str],
                          R: int = _R_SHUFFLES,
                          seed: int = _RANDOM_SEED) -> pd.DataFrame:
    """
    ========================================================================
     Cross-map saturation diagnostic. For each metric, take the
     per-map endpoint, shuffle R times, build running means for
     N = 1..n_maps. Report mean / std across shuffles per N,
     plus the std relative to the full-sample mean (the
     stability metric).
    ========================================================================
    """
    end = _endpoints(df)
    rng = np.random.default_rng(seed)
    rows = []
    for metric in metrics:
        per_map = end[metric].astype(float).to_numpy()
        n = len(per_map)
        curves = np.zeros((R, n))
        for r in range(R):
            order = rng.permutation(n)
            shuffled = per_map[order]
            curves[r] = np.cumsum(shuffled) / np.arange(1, n + 1)
        mu = curves.mean(axis=0)
        sd = curves.std(axis=0)
        denom = abs(mu[-1]) if mu[-1] != 0 else 1.0
        for i in range(n):
            rows.append({
                'metric':                  metric,
                'N':                       int(i + 1),
                'mean_of_running_means':   float(mu[i]),
                'std_of_running_means':    float(sd[i]),
                'std_rel_to_final':        float(sd[i] / denom),
            })
    return pd.DataFrame(rows)


def _cross_map_verdicts(cum_mean: pd.DataFrame,
                        metrics: Iterable[str],
                        tol: float) -> dict:
    """
    ========================================================================
     Per metric, smallest N where `std_rel_to_final < tol` —
     and stays so for the rest of the curve. Reports the
     stability N, plus rel-σ at half (a useful comparator).
    ========================================================================
    """
    verdicts = {}
    for metric in metrics:
        sub = (cum_mean[cum_mean['metric'] == metric]
               .sort_values('N').reset_index(drop=True))
        Ns = sub['N'].astype(int).to_numpy()
        rels = sub['std_rel_to_final'].astype(float).to_numpy()
        n_max = int(Ns[-1]) if len(Ns) else 0
        stable_n: int | None = None
        for i in range(len(rels)):
            if rels[i:].max() < tol:
                stable_n = int(Ns[i])
                break
        rel_half = float(rels[max(0, n_max // 2 - 1)]) if n_max else 0.0
        verdicts[metric] = {
            'stable_at_N': stable_n,
            'n_max':       n_max,
            'rel_at_half': rel_half,
        }
    return verdicts


# ── (4) Intra-cluster ρ + effective N ───────────────────────────────────────

def _diag_intra_cluster_rho(df: pd.DataFrame,
                            metrics: Iterable[str]) -> pd.DataFrame:
    """
    ========================================================================
     Lag-1 autocorrelation across the k-stages of each chain,
     averaged over maps → ρ per metric. Design-effect:
       N_eff = N_total / (1 + (m − 1) · ρ).
     m = mean chain length (rows per map).
    ========================================================================
    """
    n_total = int(len(df))
    n_maps = int(df['map'].nunique())
    m_per = (n_total / n_maps) if n_maps else 1.0
    rows = []
    for metric in metrics:
        rhos = []
        for _, grp in df.groupby('map'):
            v = grp.sort_values('m')[metric].astype(float).to_numpy()
            if len(v) < 2:
                continue
            if np.std(v) == 0:
                rhos.append(1.0)
                continue
            v0 = v[:-1]; v1 = v[1:]
            r = float(np.corrcoef(v0, v1)[0, 1])
            rhos.append(1.0 if np.isnan(r) else r)
        mean_rho = float(np.mean(rhos)) if rhos else 0.0
        rho_eff = max(0.0, mean_rho)
        n_eff = n_total / (1.0 + (m_per - 1.0) * rho_eff)
        rows.append({
            'metric':         metric,
            'mean_rho_lag1':  mean_rho,
            'n_total':        n_total,
            'n_maps':         n_maps,
            'rows_per_map':   float(m_per),
            'n_eff':          float(n_eff),
            'design_effect':  (n_total / n_eff) if n_eff > 0 else float('inf'),
        })
    return pd.DataFrame(rows)


# ── (5) Variance decomposition (η² for domain) ──────────────────────────────

def _diag_variance_decomposition(df: pd.DataFrame,
                                 metrics: Iterable[str]) -> pd.DataFrame:
    """
    ========================================================================
     η² = SS_between_domain / SS_total on per-map endpoint
     values. Fraction of variance explained by domain.
       > 0.5 ⇒ domain dominates (per-domain reporting MANDATORY).
       0.2 – 0.5 ⇒ moderate (per-domain helpful).
       < 0.2 ⇒ weak (domain not the main axis).
    ========================================================================
    """
    end = _endpoints(df)
    rows = []
    for metric in metrics:
        v = end[metric].astype(float).to_numpy()
        if len(v) == 0:
            continue
        grand = float(np.mean(v))
        ss_total = float(np.sum((v - grand) ** 2))
        ss_between = 0.0
        within_vars = []
        for _, grp in end.groupby('domain'):
            g = grp[metric].astype(float).to_numpy()
            ng = len(g)
            if ng == 0:
                continue
            ss_between += ng * (float(np.mean(g)) - grand) ** 2
            within_vars.append(float(np.var(g, ddof=1)) if ng > 1 else 0.0)
        eta2 = (ss_between / ss_total) if ss_total > 0 else 0.0
        rows.append({
            'metric':                    metric,
            'eta_squared_domain':        float(eta2),
            'mean_within_domain_var':    float(np.mean(within_vars))
                                          if within_vars else 0.0,
            'ss_total':                  ss_total,
            'ss_between_domain':         ss_between,
        })
    return pd.DataFrame(rows)


# ── (6) Half-split consistency ──────────────────────────────────────────────

def _diag_half_split(df: pd.DataFrame,
                     metrics: Iterable[str],
                     R: int = _R_SHUFFLES,
                     seed: int = _RANDOM_SEED) -> pd.DataFrame:
    """
    ========================================================================
     R random equal-half splits of the n_maps. For each split,
     |mean(half A) − mean(half B)|. Report median / p75 / p95,
     and relative to the full-sample mean.
    ========================================================================
    """
    end = _endpoints(df)
    rng = np.random.default_rng(seed)
    rows = []
    for metric in metrics:
        per_map = end[metric].astype(float).to_numpy()
        n = len(per_map)
        half = n // 2
        if half == 0:
            continue
        diffs = np.zeros(R)
        for r in range(R):
            order = rng.permutation(n)
            a = float(np.mean(per_map[order[:half]]))
            b = float(np.mean(per_map[order[half:half * 2]]))
            diffs[r] = abs(a - b)
        full_mean = float(np.mean(per_map))
        denom = abs(full_mean) if full_mean != 0 else 1.0
        rows.append({
            'metric':           metric,
            'median_abs_diff':  float(np.median(diffs)),
            'p75_abs_diff':     float(np.percentile(diffs, 75)),
            'p95_abs_diff':     float(np.percentile(diffs, 95)),
            'median_rel':       float(np.median(diffs) / denom),
            'p75_rel':          float(np.percentile(diffs, 75) / denom),
            'full_mean':        full_mean,
        })
    return pd.DataFrame(rows)


# ── (7) Bootstrap-CI extrapolation ──────────────────────────────────────────

def _bootstrap_ci_half_width(values: np.ndarray,
                             B: int,
                             alpha: float,
                             rng: np.random.Generator) -> float:
    """
    ========================================================================
     Percentile-bootstrap 95 % CI half-width on the mean.
     Resamples `values` with replacement B times, takes the
     2.5 / 97.5 quantiles of the resampled means, returns
     half the spread.
    ========================================================================
    """
    n = len(values)
    if n < 2:
        return 0.0
    means = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, n)
        means[b] = float(values[idx].mean())
    lo = float(np.quantile(means, alpha / 2.0))
    hi = float(np.quantile(means, 1.0 - alpha / 2.0))
    return (hi - lo) / 2.0


def _diag_ci_extrapolation(df: pd.DataFrame,
                           metrics: Iterable[str],
                           B: int = _BOOTSTRAP_B,
                           target_rel: float = _TARGET_REL_CI,
                           seed: int = _RANDOM_SEED
                           ) -> pd.DataFrame:
    """
    ========================================================================
     For each metric:
       - Take per-map endpoint values (n maps).
       - Bootstrap-resample with replacement (B times) to get
         the 95 % CI half-width on the mean at current n.
       - Extrapolate to hypothetical N' via the textbook CLT
         1/√N rule:  hw(N') = hw(n) · √(n / N').
       - Compute `n_required`: smallest N such that
         predicted hw(N) ≤ target_rel · |μ|, i.e.
           N_req = n · (hw_now / (target_rel · |μ|))².

     **In-distribution assumption.** The 1/√N extrapolation
     assumes additional maps are drawn from the SAME
     population (here: the Moving-AI 2D-grid mix —
     `rooms ∪ maze512 ∪ random512 ∪ dragon_age ∪ cities`).
     Maps from a new regime (3D grids, weighted graphs,
     time-dependent costs, etc.) are outside the diagnostic's
     reach.
    ========================================================================
    """
    end = _endpoints(df)
    rng = np.random.default_rng(seed)
    rows = []
    for metric in metrics:
        vals = end[metric].astype(float).to_numpy()
        n = len(vals)
        mu = float(np.mean(vals))
        denom = abs(mu) if mu != 0 else 1.0
        hw_now = _bootstrap_ci_half_width(
            vals, B=B, alpha=0.05, rng=rng)
        target_hw = target_rel * abs(mu)
        if hw_now > 0.0 and target_hw > 0.0:
            n_required = int(np.ceil(
                n * (hw_now / target_hw) ** 2))
        else:
            # Either degenerate variance (hw_now == 0) or
            # near-zero mean (target_hw == 0) — no meaningful
            # extrapolation; report current N as sufficient.
            n_required = n
        for mult in _EXTRAPOLATION_MULTIPLIERS:
            N_pred = mult * n
            hw_pred = hw_now * float(np.sqrt(n / N_pred))
            rows.append({
                'metric':       metric,
                'mult':         int(mult),
                'N':            int(N_pred),
                'n_current':    int(n),
                'mu':           mu,
                'hw_absolute':  float(hw_pred),
                'hw_relative':  float(hw_pred / denom),
                'target_rel':   float(target_rel),
                'n_required':   int(n_required),
            })
    return pd.DataFrame(rows)


# ── Markdown report ─────────────────────────────────────────────────────────

def _fmt(x: float) -> str:
    """
    ========================================================================
     Compact float formatting for table cells: %g for very
     small/large, fixed otherwise. Keeps tables readable across
     metrics that range across orders of magnitude.
    ========================================================================
    """
    if x == 0.0:
        return '0'
    if abs(x) >= 1000 or abs(x) < 0.01:
        return f'{x:.3g}'
    return f'{x:.3f}'


def _format_report(csv_stem: str,
                   df: pd.DataFrame,
                   metrics: Iterable[str],
                   per_domain: pd.DataFrame,
                   sat_verdicts: dict,
                   cross_verdicts: dict,
                   rho: pd.DataFrame,
                   var_decomp: pd.DataFrame,
                   half: pd.DataFrame,
                   ci_extrap: pd.DataFrame) -> str:
    """
    ========================================================================
     Build the Markdown diagnostic report (sections 1–7 + a
     bottom-line summary).
    ========================================================================
    """
    n_rows = int(len(df))
    n_maps = int(df['map'].nunique())
    n_doms = int(df['domain'].nunique())
    dom_counts = dict(df.drop_duplicates('map')['domain']
                       .value_counts().items())
    L: list[str] = []
    L.append(f'# s_3 diagnostics — `{csv_stem}`')
    L.append('')
    L.append(f'**Rows:** {n_rows:,}  '
             f'**Maps:** {n_maps}  '
             f'**Domains:** {n_doms}  '
             f'**Per-domain map counts:** {dom_counts}')
    L.append('')
    L.append('---')
    L.append('')

    # 1 — per-domain summaries (one block per metric)
    L.append('## 1. Per-domain summaries (per-map endpoint)')
    L.append('')
    for metric in metrics:
        sub = (per_domain[per_domain['metric'] == metric]
               .sort_values('domain'))
        if sub.empty:
            continue
        L.append(f'### `{metric}`')
        L.append('')
        L.append('| domain | n | mean | median | p25 | p75 | p90 | max |')
        L.append('|---|---|---|---|---|---|---|---|')
        for _, row in sub.iterrows():
            L.append(
                f'| {row["domain"]} | {int(row["n_maps"])} | '
                f'{_fmt(row["mean"])} | {_fmt(row["median"])} | '
                f'{_fmt(row["p25"])} | {_fmt(row["p75"])} | '
                f'{_fmt(row["p90"])} | {_fmt(row["max"])} |')
        L.append('')

    # 2 — per-chain Δ_k saturation
    L.append('## 2. Per-chain Δ_k saturation')
    L.append('')
    L.append(f'**Criterion:** `mean(Δ at k∈{{180,190,200}}) / '
             f'mean(Δ at k∈{{20,30,40}}) < {_SAT_TOL_REL}` ⇒ '
             f'k-range adequate on that map.')
    L.append('')
    L.append('| metric | saturated maps | verdict |')
    L.append('|---|---|---|')
    for metric in metrics:
        v = sat_verdicts.get(metric, {})
        if not v:
            continue
        frac = v['frac']
        verdict = ('k-range **adequate** ✓' if frac >= 0.8 else
                   'k-range **borderline**' if frac >= 0.5 else
                   'k-range **narrow** ✗')
        L.append(f'| `{metric}` | {v["n_saturated"]} / '
                 f'{v["n_total"]} ({frac:.0%}) | {verdict} |')
    L.append('')

    # 3 — cross-map saturation
    L.append('## 3. Cross-map cumulative-mean saturation')
    L.append('')
    L.append(f'**Criterion:** smallest N where '
             f'`σ_N / |μ_max| < {_CROSS_TOL_REL}` and stays '
             f'so. R = {_R_SHUFFLES} shufflings.')
    L.append('')
    L.append('| metric | stable_at_N | rel σ at N≈half | verdict |')
    L.append('|---|---|---|---|')
    for metric in metrics:
        v = cross_verdicts.get(metric, {})
        if not v:
            continue
        sn = v['stable_at_N']
        nm = v['n_max']
        if sn is None:
            verdict = '**unstable** at N_max ✗'
            sn_str = '—'
        elif sn <= 0.6 * nm:
            verdict = 'comfortable margin ✓'
            sn_str = str(sn)
        elif sn <= 0.85 * nm:
            verdict = 'modest margin'
            sn_str = str(sn)
        else:
            verdict = 'tight — saturates only near N_max'
            sn_str = str(sn)
        L.append(f'| `{metric}` | {sn_str} / {nm} | '
                 f'{v["rel_at_half"]:.2%} | {verdict} |')
    L.append('')

    # 4 — intra-cluster ρ + effective N
    L.append('## 4. Intra-cluster ρ + effective N')
    L.append('')
    L.append('Honest sample count after design-effect '
             '`N_eff = N / (1 + (m−1)·ρ)` (m = rows per map).')
    L.append('')
    L.append('| metric | ρ (lag-1) | N_naïve | N_eff | design effect |')
    L.append('|---|---|---|---|---|')
    for _, row in rho.iterrows():
        L.append(f'| `{row["metric"]}` | {row["mean_rho_lag1"]:.3f} | '
                 f'{int(row["n_total"])} | {row["n_eff"]:.1f} | '
                 f'{row["design_effect"]:.1f}× |')
    L.append('')

    # 5 — variance decomposition
    L.append('## 5. Variance decomposition — η² for domain')
    L.append('')
    L.append('| metric | η²_domain | strength | reporting verdict |')
    L.append('|---|---|---|---|')
    for _, row in var_decomp.iterrows():
        eta2 = float(row['eta_squared_domain'])
        if eta2 > 0.5:
            strength = 'strong'
            verdict = '**per-domain MANDATORY** ✓'
        elif eta2 > 0.2:
            strength = 'moderate'
            verdict = 'per-domain helpful'
        else:
            strength = 'weak'
            verdict = 'domain not a primary axis'
        L.append(f'| `{row["metric"]}` | {eta2:.3f} | '
                 f'{strength} | {verdict} |')
    L.append('')

    # 6 — half-split consistency
    L.append(f'## 6. Half-split consistency (R = {_R_SHUFFLES})')
    L.append('')
    L.append('| metric | median \\|Δ\\| / mean | p75 \\|Δ\\| / mean | verdict |')
    L.append('|---|---|---|---|')
    for _, row in half.iterrows():
        rel = float(row['median_rel'])
        if rel < _HALF_TOL_REL:
            verdict = 'robust ✓'
        elif rel < 3 * _HALF_TOL_REL:
            verdict = 'borderline'
        else:
            verdict = 'fragile ✗'
        L.append(f'| `{row["metric"]}` | {rel:.2%} | '
                 f'{float(row["p75_rel"]):.2%} | {verdict} |')
    L.append('')

    # 7 — Bootstrap-CI extrapolation
    L.append(f'## 7. Bootstrap-CI extrapolation '
             f'(target ±{_TARGET_REL_CI:.0%}, '
             f'B = {_BOOTSTRAP_B})')
    L.append('')
    L.append('**In-distribution sampling assumption:** the new '
             'maps are drawn from the same Moving-AI 2D-grid '
             'mix (`rooms ∪ maze512 ∪ random512 ∪ dragon_age '
             '∪ cities`). Extrapolation uses the textbook CLT '
             '1/√N rule: `hw(N\') = hw(n) · √(n / N\')`.')
    L.append('')
    for metric in metrics:
        sub = (ci_extrap[ci_extrap['metric'] == metric]
               .sort_values('N').reset_index(drop=True))
        if sub.empty:
            continue
        mu = float(sub.iloc[0]['mu'])
        n_cur = int(sub.iloc[0]['n_current'])
        n_req = int(sub.iloc[0]['n_required'])
        # Verdict — how much extra data to reach target.
        if n_req <= n_cur:
            verdict = (f'**current N={n_cur} already meets '
                       f'±{_TARGET_REL_CI:.0%}** ✓')
        elif n_req <= 2 * n_cur:
            verdict = ('**doubling sufficient** to meet target')
        elif n_req <= 4 * n_cur:
            verdict = ('**~4×** more maps needed')
        elif n_req <= 20 * n_cur:
            ratio = max(2, n_req // n_cur)
            verdict = (f'**~{ratio}×** more maps needed')
        else:
            verdict = (f'**very noisy** — N ≈ {n_req} for '
                       f'±{_TARGET_REL_CI:.0%} (current design '
                       f'may not support that precision)')
        L.append(f'### `{metric}`  μ = {_fmt(mu)}, '
                 f'N to reach ±{_TARGET_REL_CI:.0%}: '
                 f'**{n_req}**')
        L.append('')
        L.append('| N | mult × current | 95 % CI half-width | rel. to μ |')
        L.append('|---|---|---|---|')
        for _, row in sub.iterrows():
            marker = ' ← current' if int(row['N']) == n_cur else ''
            L.append(f'| {int(row["N"])}{marker} | '
                     f'{int(row["mult"])}× | '
                     f'±{_fmt(float(row["hw_absolute"]))} | '
                     f'±{float(row["hw_relative"]):.2%} |')
        L.append('')
        L.append(f'Verdict: {verdict}.')
        L.append('')

    # Bottom-line summary
    L.append('## Bottom line')
    L.append('')
    n_eff_summary = rho['n_eff'].mean() if not rho.empty else float('nan')
    sat_frac_summary = (np.mean([sat_verdicts[m]['frac']
                                  for m in metrics
                                  if m in sat_verdicts])
                        if any(m in sat_verdicts for m in metrics)
                        else 0.0)
    eta2_summary = (var_decomp['eta_squared_domain'].mean()
                    if not var_decomp.empty else 0.0)
    L.append(f'- **Effective N** (averaged across metrics): '
             f'{n_eff_summary:.1f} (naïve {n_rows}).')
    L.append(f'- **k-range adequacy** (saturated-map fraction, '
             f'averaged): {sat_frac_summary:.0%}.')
    L.append(f'- **Domain effect** (mean η²): {eta2_summary:.2f} — '
             f'{"per-domain reporting MANDATORY" if eta2_summary > 0.5 else ("per-domain helpful" if eta2_summary > 0.2 else "domain weak")}.')
    # CI-extrapolation: median N_required across metrics gives
    # the headline "do I need more in-distribution maps?" answer.
    if not ci_extrap.empty:
        per_metric = (ci_extrap.drop_duplicates('metric')
                      .set_index('metric'))
        n_req_median = int(np.median(
            per_metric['n_required'].astype(int).to_numpy()))
        n_cur_any = int(per_metric['n_current'].iloc[0])
        if n_req_median <= n_cur_any:
            ci_verdict = (f'current N={n_cur_any} ALREADY MEETS '
                          f'±{_TARGET_REL_CI:.0%} CI')
        else:
            mult = max(2, n_req_median // n_cur_any)
            ci_verdict = (f'need ≈ {n_req_median} maps total '
                          f'(~{mult}× more) for ±{_TARGET_REL_CI:.0%} CI')
        L.append(f'- **In-distribution adequacy** (Diagnostic 7, '
                 f'median across metrics): {ci_verdict}.')
    L.append('')
    L.append('See sections 1–7 above for per-metric detail '
             'and the three derived CSVs (`__deltas.csv`, '
             '`__cumulative_mean.csv`, `__ci_extrapolation.csv`) '
             'for plotting.')
    L.append('')
    return '\n'.join(L)


# ── Public API ──────────────────────────────────────────────────────────────

def diagnose(path_drive_csv_in: str,
             dir_drive_out: str = 'Experiments/MOSPP/diagnostics',
             metrics: tuple[str, ...] = _DEFAULT_METRICS,
             R: int = _R_SHUFFLES,
             seed: int = _RANDOM_SEED) -> None:
    """
    ========================================================================
     Download `path_drive_csv_in`, run the 6 diagnostics, write
     the Markdown report + two long-format CSVs (deltas,
     cumulative-mean curves) to `dir_drive_out/`.

     Output filenames derive from the input CSV stem:
       {stem}__report.md
       {stem}__deltas.csv
       {stem}__cumulative_mean.csv
    ========================================================================
    """
    drive = Drive.Factory.valdas()
    stem = os.path.splitext(os.path.basename(path_drive_csv_in))[0]
    _log.info(f'diagnostics: input = {path_drive_csv_in}')
    _log.info(f'diagnostics: stem = {stem}')

    fd_in, path_in = tempfile.mkstemp(suffix='.csv')
    os.close(fd_in)
    fd_md, path_md = tempfile.mkstemp(suffix='.md')
    os.close(fd_md)
    fd_d, path_deltas = tempfile.mkstemp(suffix='.csv')
    os.close(fd_d)
    fd_c, path_cum = tempfile.mkstemp(suffix='.csv')
    os.close(fd_c)
    fd_e, path_ci = tempfile.mkstemp(suffix='.csv')
    os.close(fd_e)
    try:
        drive.download(path_src=path_drive_csv_in, path_dest=path_in)
        df = pd.read_csv(path_in)
        df = _ensure_domain(df)
        # Filter metrics to those present.
        present = [m for m in metrics if m in df.columns]
        missing = [m for m in metrics if m not in df.columns]
        if missing:
            _log.warning(f'metrics absent from CSV (skipped): {missing}')
        if not present:
            raise ValueError(
                f'no requested metrics found in CSV; '
                f'columns are: {list(df.columns)}')
        _log.info(f'loaded {len(df):,} rows, '
                  f'{df["map"].nunique()} maps, '
                  f'{df["domain"].nunique()} domains; '
                  f'metrics = {present}')

        # Run the 7 diagnostics.
        _log.info('(1) per-domain summaries')
        per_domain = _diag_per_domain(df, present)
        _log.info('(2) per-chain Δ_k')
        deltas = _diag_deltas(df, present)
        sat_v = _saturation_verdicts(deltas, present, _SAT_TOL_REL)
        _log.info(f'(3) cross-map cumulative-mean (R={R})')
        cum = _diag_cumulative_mean(df, present, R=R, seed=seed)
        cross_v = _cross_map_verdicts(cum, present, _CROSS_TOL_REL)
        _log.info('(4) intra-cluster ρ + effective N')
        rho = _diag_intra_cluster_rho(df, present)
        _log.info('(5) variance decomposition (η²)')
        var_dec = _diag_variance_decomposition(df, present)
        _log.info(f'(6) half-split consistency (R={R})')
        half = _diag_half_split(df, present, R=R, seed=seed)
        _log.info(f'(7) bootstrap-CI extrapolation '
                  f'(B={_BOOTSTRAP_B}, target ±{_TARGET_REL_CI:.0%})')
        ci_extrap = _diag_ci_extrapolation(
            df, present, B=_BOOTSTRAP_B,
            target_rel=_TARGET_REL_CI, seed=seed)

        # Write report + derived CSVs.
        report = _format_report(
            csv_stem=stem, df=df, metrics=present,
            per_domain=per_domain, sat_verdicts=sat_v,
            cross_verdicts=cross_v, rho=rho,
            var_decomp=var_dec, half=half,
            ci_extrap=ci_extrap)
        with open(path_md, 'w') as f:
            f.write(report)
        deltas.to_csv(path_deltas, index=False)
        cum.to_csv(path_cum, index=False)
        ci_extrap.to_csv(path_ci, index=False)

        # Upload to Drive.
        out_md = f'{dir_drive_out}/{stem}__report.md'
        out_d = f'{dir_drive_out}/{stem}__deltas.csv'
        out_c = f'{dir_drive_out}/{stem}__cumulative_mean.csv'
        out_e = f'{dir_drive_out}/{stem}__ci_extrapolation.csv'
        drive.upload(path_src=path_md, path_dest=out_md)
        drive.upload(path_src=path_deltas, path_dest=out_d)
        drive.upload(path_src=path_cum, path_dest=out_c)
        drive.upload(path_src=path_ci, path_dest=out_e)
        _log.info(f'uploaded:')
        _log.info(f'  {out_md}')
        _log.info(f'  {out_d}')
        _log.info(f'  {out_c}')
        _log.info(f'  {out_e}')
    finally:
        for p in (path_in, path_md, path_deltas, path_cum, path_ci):
            if os.path.exists(p):
                os.unlink(p)


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Point at any `s_3` nested CSV on Drive; each run produces
    # one report + two derived CSVs in `dir_drive_out`.
    path_drive_csv_in = (
        'Experiments/MOSPP/'
        'astar_inc_nested__rule_1__bpmx_inf__prop_0.csv')
    diagnose(
        path_drive_csv_in=path_drive_csv_in,
        dir_drive_out='Experiments/MOSPP/diagnostics',
        metrics=_DEFAULT_METRICS,
        R=_R_SHUFFLES,
        seed=_RANDOM_SEED,
    )
    _log.info('--- done ---')
