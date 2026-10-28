# How much of the marathon revolution is the shoe?

Carbon-plated "super shoes" took about a minute off median elite marathon time. This repo reaches that figure three separate ways, from 1,908 elite marathon performances between 2010 and 2024, and pools the three.

[Live site](https://lyhjeremy.github.io/marathon-shoe-revolution-decomposition/) · [Write-up](https://lyhjeremy.github.io/marathon-shoe-revolution-decomposition/overview/) · [Full report](writeup.md) · [Narrative article](https://lyhjeremy.github.io/marathon-shoe-revolution-decomposition/article.html) · [PDF](reports/Marathon_Shoe_Revolution_Decomposition_Report.pdf)

Design and copy follow [these standards](https://github.com/lyhjeremy/lyhjeremy/blob/main/DESIGN_STANDARDS.md).

## Results

| Framework | Shoe contribution | 95% CI |
|---|---:|---|
| Difference-in-differences (road vs track 10,000 m) | 111 s | [131, 253] |
| Within-athlete paired (n = 17) | 47 s | [−25, 137] |
| Cohort survival (55% attribution share) | 58 s | [46, 111] |
| **Pooled** | **67 s** | **[36, 99]** |

- 67 seconds is about 0.9% of a 2:05 marathon.
- Sub-2:10 (men) and sub-2:25 (women) performances per year rose 1.25× and 1.39× after 2017 in this dataset, against the three to five times often quoted.
- Women's road marathon top-30 median improved 1.59% between eras; women's track 10,000 m improved 0.32%.

Values come from [`outputs/analysis_summary.json`](outputs/analysis_summary.json).

![Sub-2:10 men's and sub-2:25 women's marathon performances per year, 2010 to 2024, modestly higher after 2017](outputs/figures/fig1_sub210_frequency_by_year.png)

## Method

The comparison is the pre-Vaporfly era (2010–2016) against the post-Vaporfly era (2018–2024), with 2017 left out as a transition year.

1. **Difference-in-differences.** Road marathon improvement in the top-30 median minus track 10,000 m improvement, rescaled to marathon time. Bootstrap CI from 1,000 resamples, plus a placebo split inside the pre-era (32 s).
2. **Within-athlete paired.** Runners with at least two elite marathons in each era; median change in career-mean time, paired t-test (t = −1.17, p = 0.26) and bootstrap CI. Not age-adjusted, because the source tables have no ages.
3. **Cohort survival.** Yearly counts of sub-2:10 and sub-2:25 performances, a slope-change changepoint search (break at 2020), and the shift in the top-30 median between eras with 55% attributed to shoes.

The pooled estimate weights each framework by the inverse square of its CI width. Its interval is the pooled value ± 1.96 × the standard deviation of the three estimates / √3.

Stack: Python, pandas, NumPy, SciPy, matplotlib, seaborn; ReportLab and python-docx for the reports.

## How to run

```bash
git clone https://github.com/lyhjeremy/marathon-shoe-revolution-decomposition.git
cd marathon-shoe-revolution-decomposition
pip install -r requirements.txt
python src/analysis.py        # figures, results CSV and JSON summary, under a minute
```

Rebuild the reports and notebook:

```bash
python src/generate_pdf.py
python src/generate_docx.py
python src/generate_html.py   # short report at web/index.html
python src/build_notebook.py
```

Re-scrape the source data (about three minutes):

```bash
python scripts/scrape_marathons.py
python scripts/scrape_track.py
```

## Repository layout

| Path | Contents |
|---|---|
| `data/` | `elite_marathon_times.csv` (1,908 rows), `track_records_control.csv` (27 rows), `shoe_timeline.csv` (19 hand-compiled rows), `athlete_career_arcs.csv` (derived), CC-BY-SA photos |
| `scripts/` | Wikipedia scrapers for marathon and track results |
| `src/` | Analysis, plus PDF, DOCX, HTML and notebook builders |
| `outputs/` | Eight figures, `analysis_results.csv`, `analysis_summary.json` |
| `notebooks/` | The analysis cell by cell |
| `reports/` | Full PDF and Word report |
| `web/` | Short HTML report with matching PDF and DOCX |
| `overview/` | Write-up page on the live site |

## Data sources

| Dataset | Source | Coverage |
|---|---|---|
| Elite marathon times | Wikipedia race-result tables: Berlin, London, Chicago, Boston, Tokyo, New York, some Dubai | 2010–2024, 1,908 rows |
| 10,000 m track | [Wikipedia 10,000 metres](https://en.wikipedia.org/wiki/10,000_metres) and record-progression pages | 2016–2024, 27 rows |
| Shoe timeline | Manufacturer announcements and race archives | 2016–2024, hand-compiled |
| Biomechanics | [Hoogkamer et al. 2018](https://doi.org/10.1007/s40279-017-0811-2), Senefeld et al. 2023 | Literature |

## Limitations

- The track control is thin: 27 rows, with one pre-era year (2016) for women and none for men. The difference-in-differences estimate rests on it.
- The difference-in-differences CI lies entirely above its point estimate, because the point uses year medians and the bootstrap resamples row means.
- The within-athlete sample is 17 runners, the result is not significant, and there is no age adjustment.
- The 55% shoe share in the cohort framework is an assumption. At 40% and 70% the cohort estimate is 42 s and 74 s, and the pooled value about 51 s and 80 s (recomputed from the summary file; the script has no switch for it).
- No race records which shoe anyone wore, so era stands in for shoe use.
- `outputs/figures/fig5_framework_comparison.png` is from an earlier run and shows 117 s for the difference-in-differences and 69 s pooled; the JSON summary and every page use 111 s and 67 s.

## License

[MIT](LICENSE) © 2026 Jeremy Lee. The eight analytical figures are CC-BY 4.0; photo credits are in [`article.md`](article.md#image-credits).
