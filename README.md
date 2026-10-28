# How much of the marathon revolution is the shoe?

Carbon-plated "super shoes" took about 73 seconds off median elite marathon time, with a wide interval (−4 to 150 s). This repo reaches that figure three separate ways, from 1,802 elite marathon running performances between 2010 and 2024, and pools the three.

*Updated 28 October 2026: the scraped data held 106 wheelchair and handcycle results, which are now excluded. Every estimate below comes from the rerun; the pooled value was 67 s [36, 99] before. Later the same day the bootstrap was fixed to resample the same statistic as each estimate, which moved the pooled value from 82 s [6, 159] to 73 s [−4, 150].*

[Live site](https://lyhjeremy.github.io/marathon-shoe-revolution-decomposition/) · [Write-up](https://lyhjeremy.github.io/marathon-shoe-revolution-decomposition/overview/) · [Full report](writeup.md) · [Narrative article](https://lyhjeremy.github.io/marathon-shoe-revolution-decomposition/article.html) · [PDF](reports/Marathon_Shoe_Revolution_Decomposition_Report.pdf)

Design and copy follow [these standards](https://github.com/lyhjeremy/lyhjeremy/blob/main/DESIGN_STANDARDS.md).

## Results

| Framework | Shoe contribution | 95% CI |
|---|---:|---|
| Difference-in-differences (road vs track 10,000 m) | 199 s | [83, 338] |
| Within-athlete paired (n = 16) | 44 s | [−62, 121] |
| Cohort survival (55% attribution share) | 71 s | [58, 98] |
| **Pooled** | **73 s** | **[−4, 150]** |

- 73 seconds is about 1.0% of a 2:05 marathon. For scale, the lab result behind the Vaporfly's name is a 4% cut in the energy cost of running against two established racing shoes ([Hoogkamer et al. 2018](https://doi.org/10.1007/s40279-017-0811-2)), and at elite marathon pace an economy gain buys only about two-thirds as much speed ([Kipp, Kram and Hoogkamer 2019](https://doi.org/10.3389/fphys.2019.00079)).
- Sub-2:10 (men) and sub-2:25 (women) performances per year rose 1.25× and 2.0× after 2017 in this dataset.
- Women's road marathon top-50 median improved 2.57% between eras; women's track 10,000 m improved 0.32%.

Values come from [`outputs/analysis_summary.json`](outputs/analysis_summary.json).

![Sub-2:10 men's and sub-2:25 women's marathon performances per year, 2010 to 2024: the men's yearly count is about a quarter higher after 2017 and the women's about twice as high](outputs/figures/fig1_sub210_frequency_by_year.png)

## Method

The comparison is the pre-Vaporfly era (2010–2016) against the post-Vaporfly era (2018–2024), with 2017 left out as a transition year. Wheelchair and handcycle results are dropped in `load_data()`: the scraper reads gender from the heading above each Wikipedia table, so tables headed "Wheelchair women" and "Handcycle women" had come in as running results.

1. **Difference-in-differences.** Road marathon improvement in the top-50 median minus track 10,000 m improvement, rescaled to marathon time. Bootstrap CI from 1,000 resamples of results within each year, plus a placebo split inside the pre-era (40 s).
2. **Within-athlete paired.** Runners with at least two elite marathons in each era; median change in career-mean time, paired t-test (t = −0.88, p = 0.39) and a bootstrap CI over athletes. Not age-adjusted, because the source tables have no ages.
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
| `data/` | `elite_marathon_times.csv` (1,908 rows, 106 of them wheelchair or handcycle and excluded), `track_records_control.csv` (27 rows), `shoe_timeline.csv` (19 hand-compiled rows), `athlete_career_arcs.csv` (derived), CC-BY-SA photos |
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
| Elite marathon times | Wikipedia race-result tables: Berlin, London, Chicago, Boston, Tokyo, New York, some Dubai | 2010–2024, 1,908 rows (1,802 running) |
| 10,000 m track | [Wikipedia 10,000 metres](https://en.wikipedia.org/wiki/10,000_metres) and record-progression pages | 2016–2024, 27 rows |
| Shoe timeline | Manufacturer announcements and race archives | 2016–2024, hand-compiled |
| Biomechanics | [Hoogkamer et al. 2018](https://doi.org/10.1007/s40279-017-0811-2), [Kipp et al. 2019](https://doi.org/10.3389/fphys.2019.00079), Senefeld et al. 2023 | Literature |

## Limitations

- The track control is thin: 27 rows, with one pre-era year (2016) for women and none for men. The difference-in-differences estimate rests on it.
- 28 October 2026: the bootstrap now resamples the same statistic as the estimate.
- The within-athlete sample is 16 runners, the result is not significant, and there is no age adjustment.
- The 55% shoe share in the cohort framework is an assumption. At 40% and 70% the cohort estimate is 52 s and 90 s, and the pooled value about 53 s and 91 s (recomputed from the summary file; the script has no switch for it).
- No race records which shoe anyone wore, so era stands in for shoe use.
- Wheelchair entries are excluded by a name list built from the source pages' table headings (54 athletes). A future re-scrape would need the list checked again.

## License

[MIT](LICENSE) © 2026 Jeremy Lee. The eight analytical figures are CC-BY 4.0; photo credits are in [`article.md`](article.md#image-credits).
