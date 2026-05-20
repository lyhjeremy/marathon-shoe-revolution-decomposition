"""
Materialize notebooks/shoe_revolution_decomposition.ipynb that reproduces
the analysis end-to-end with prose interleaved between code cells.
"""
import json
import os

import nbformat as nbf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
NB_PATH = os.path.join(PROJECT_DIR, 'notebooks', 'shoe_revolution_decomposition.ipynb')


def md(s):
    return nbf.v4.new_markdown_cell(s)


def code(s):
    return nbf.v4.new_code_cell(s)


def main():
    nb = nbf.v4.new_notebook()
    cells = []

    cells.append(md("""# How Much of the Post-2017 Marathon Revolution Is the Shoe?

**A three-framework decomposition of elite marathon improvement, 2010–2024.**

*Jeremy Lee · May 2026 · [github.com/lyhjeremy/marathon-shoe-revolution-decomposition](https://github.com/lyhjeremy/marathon-shoe-revolution-decomposition)*

This notebook reproduces the analysis cell-by-cell. The same numbers and figures appear in the formal writeup at `writeup.md` and the PDF report in `reports/`."""))

    cells.append(md("""## 1. Setup

Load the three frameworks and helper functions from `src/analysis.py`. We use matplotlib's Agg backend for headless rendering."""))

    cells.append(code("""import sys, os
sys.path.insert(0, os.path.abspath('../src'))
import analysis
from analysis import (
    load_data, derive_athlete_career_arcs,
    framework1_did, framework2_within_athlete, framework3_cohort_survival,
    synthesize, time_str,
)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
plt.rcParams['savefig.dpi'] = 200  # screen-friendly; src/analysis.py uses 400 for files
"""))

    cells.append(md("""## 2. Load the four source CSVs

- `data/elite_marathon_times.csv` (1,908 rows scraped from major-marathon Wikipedia tables)
- `data/track_records_control.csv` (27 rows, sparse — see writeup §9)
- `data/shoe_timeline.csv` (hand-compiled, 19 rows)
- `data/athlete_career_arcs.csv` (derived)"""))

    cells.append(code("""data = load_data()
marathon = data['marathon']
track    = data['track']
timeline = data['timeline']
arcs     = data['arcs']

print(f"Marathon: {len(marathon):,} rows ({marathon['year'].min()}–{marathon['year'].max()})")
print(f"Track:    {len(track):,} rows ({track['year'].min()}–{track['year'].max()})")
print(f"Timeline: {len(timeline):,} rows")
if arcs is None:
    print("Career arcs: not yet derived — building now …")
    arcs = derive_athlete_career_arcs(marathon)
print(f"Career arcs: {len(arcs)} athletes")
"""))

    cells.append(md("""## 3. Quick look at the marathon data

Top-30 median time per year, per gender. This is the cohort signal that drives Framework 3."""))

    cells.append(code("""def top30_median(g):
    return g.nsmallest(min(30, len(g)), 'finish_time_seconds')['finish_time_seconds'].median()

med = (marathon.groupby(['year','gender']).apply(top30_median)
        .unstack(fill_value=np.nan))
med['M_str'] = med['M'].apply(lambda s: time_str(s) if not np.isnan(s) else '—')
med['W_str'] = med['W'].apply(lambda s: time_str(s) if not np.isnan(s) else '—')
med[['M','W','M_str','W_str']].round(0)
"""))

    cells.append(md("""## 4. Framework 1 — Difference-in-Differences

Road marathon improvement minus track 10,000m improvement, computed per gender on top-30 medians. Bootstrap CI from 1,000 marathon-row resamples."""))

    cells.append(code("""s1, ctx1 = framework1_did(marathon, track, n=30)
print(f"Shoe contribution (DiD): {s1['shoe_contribution_seconds']:.0f} s")
print(f"95% CI: [{s1['ci_low']:.0f}, {s1['ci_high']:.0f}]")
print(f"Placebo DiD: {s1['placebo_did_seconds']:.1f} s (should be near zero)")
print(f"\\nGender breakdown:")
for g, r in s1['by_gender'].items():
    print(f"  {g}: road improvement {-r['road_delta']:.0f} s ({r['road_pct']:.2f}%), "
          f"track improvement {-r['trk_delta']:.0f} s ({r['trk_pct']:.2f}%), "
          f"shoe contribution {r['shoe_contribution_seconds']:.0f} s")
print(f"\\nNote: {s1['note']}")
"""))

    cells.append(md("""## 5. Framework 2 — Within-athlete paired pre/post

Median of per-athlete (post mean minus pre mean) across the n=17 cohort that raced ≥2 elites in both eras."""))

    cells.append(code("""s2, arcs_used = framework2_within_athlete(arcs)
print(f"n athletes: {s2['n_athletes']}")
print(f"Method:     {s2['delta_method']}")
print(f"Median delta:  {s2['median_delta_seconds']:.0f} s (post mean − pre mean)")
print(f"Mean delta:    {s2['mean_delta_seconds']:.0f} s")
print(f"% improved:    {s2['pct_improved']:.0f}%")
print(f"Paired t-test: t={s2['paired_t']:.2f}, p={s2['paired_p']:.3f}")
print(f"Shoe contribution: {s2['shoe_contribution_seconds']:.0f} s")
print(f"95% CI: [{-s2['ci_high']:.0f}, {-s2['ci_low']:.0f}]")
"""))

    cells.append(md("""## 6. Framework 3 — Cohort survival / depth

Annual sub-2:10 (men) and sub-2:25 (women) counts; changepoint detection; cohort-improvement shoe attribution (55% share)."""))

    cells.append(code("""s3, ctx3 = framework3_cohort_survival(marathon)
print(f"Changepoint year: {s3['changepoint_year']}")
print(f"Sub-2:10 men:  {s3['sub_m_pre_mean']:.1f}/yr pre → {s3['sub_m_post_mean']:.1f}/yr post")
print(f"Sub-2:25 women: {s3['sub_w_pre_mean']:.1f}/yr pre → {s3['sub_w_post_mean']:.1f}/yr post")
print(f"\\nRaw cohort improvement: {s3['raw_cohort_improvement_seconds']:.0f} s")
print(f"Shoe-attributed (55%):   {s3['shoe_contribution_seconds']:.0f} s")
print(f"95% CI: [{s3['ci_low']:.0f}, {s3['ci_high']:.0f}]")
"""))

    cells.append(md("""## 7. Cross-framework synthesis

Inverse-CI-width-weighted pool of the three estimates."""))

    cells.append(code("""pool = synthesize([s1, s2, s3])
print(f"Pooled shoe contribution: {pool['pooled_estimate_seconds']:.0f} s")
print(f"95% CI: [{pool['pooled_ci_low']:.0f}, {pool['pooled_ci_high']:.0f}]")
print(f"As % of 2:05 marathon: {pool['pooled_estimate_seconds']/(2*3600+5*60)*100:.2f}%")
print()
print("Individual framework estimates:")
for k, v in pool['framework_estimates'].items():
    print(f"  {k:18}  {v:6.0f} s")
"""))

    cells.append(md("""## 8. Render the eight figures

All figures save to `outputs/figures/` at 400 DPI."""))

    cells.append(code("""import importlib
importlib.reload(analysis)
from analysis import (
    fig1_sub210_frequency, fig2_did_track_vs_road, fig3_within_athlete_paired,
    fig4_cohort_survival, fig5_framework_comparison, fig6_decomposition,
    fig7_sensitivity, fig8_brand_adoption, OUTPUT_DIR,
)
fig1_sub210_frequency(marathon, os.path.join(OUTPUT_DIR, 'fig1_sub210_frequency_by_year.png'))
fig2_did_track_vs_road(marathon, track, os.path.join(OUTPUT_DIR, 'fig2_did_track_vs_road.png'))
fig3_within_athlete_paired(arcs_used, os.path.join(OUTPUT_DIR, 'fig3_within_athlete_paired.png'))
fig4_cohort_survival(marathon, os.path.join(OUTPUT_DIR, 'fig4_cohort_survival.png'))
fig5_framework_comparison([s1, s2, s3], pool, os.path.join(OUTPUT_DIR, 'fig5_framework_comparison.png'))
fig6_decomposition(pool, os.path.join(OUTPUT_DIR, 'fig6_decomposition_pie.png'))
fig7_sensitivity(marathon, track, arcs, os.path.join(OUTPUT_DIR, 'fig7_sensitivity.png'))
fig8_brand_adoption(timeline, os.path.join(OUTPUT_DIR, 'fig8_brand_adoption_timeline.png'))
print('All 8 figures written.')
"""))

    cells.append(md("""## 9. Display the headline figure inline

The forest plot of three framework estimates and the pooled value."""))

    cells.append(code("""from IPython.display import Image, display
display(Image(os.path.join(OUTPUT_DIR, 'fig5_framework_comparison.png')))
"""))

    cells.append(md("""## 10. Sub-threshold frequencies"""))

    cells.append(code("""display(Image(os.path.join(OUTPUT_DIR, 'fig1_sub210_frequency_by_year.png')))
"""))

    cells.append(md("""## 11. Reproducibility

This notebook can be regenerated by running `python src/build_notebook.py` from the repo root. The analysis itself can be rerun with `python src/analysis.py`. Both PDF reports and both DOCX reports regenerate from `python src/generate_pdf.py` and `python src/generate_docx.py`. The self-contained HTML article rebuilds from `python src/generate_html.py`.

For methodology, sensitivity analysis, and limitations, see the full [writeup.md](../writeup.md)."""))

    nb.cells = cells
    os.makedirs(os.path.dirname(NB_PATH), exist_ok=True)
    with open(NB_PATH, 'w') as f:
        nbf.write(nb, f)
    print(f"Notebook written: {NB_PATH}  ({len(cells)} cells)")


if __name__ == '__main__':
    main()
