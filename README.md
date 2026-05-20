# How Much of the Post-2017 Marathon Revolution Is the Shoe?

A three-framework decomposition of elite marathon performance improvement from 2010–2024, isolating the contribution of carbon-plated "super shoes."

📊 **[Read the full writeup →](writeup.md)** &nbsp;·&nbsp; 📝 [Narrative article](article.md) &nbsp;·&nbsp; 📄 [PDF report](reports/Marathon_Shoe_Revolution_Decomposition_Report.pdf) &nbsp;·&nbsp; 📘 [Word doc](reports/Marathon_Shoe_Revolution_Decomposition_Report.docx) &nbsp;·&nbsp; 📓 [Notebook](notebooks/shoe_revolution_decomposition.ipynb) &nbsp;·&nbsp; 🌐 [HTML article](web/index.html)

---

## What this is

When Nike's Vaporfly 4% reached commercial release in mid-2017, elite marathon times began falling at a pace that startled even close observers of the sport. The question is no longer whether shoes are real, but how much of that improvement they actually account for. This project applies three independent decomposition frameworks to ~1,900 elite marathon performances 2010–2024:

1. **Difference-in-Differences (DiD)** — road marathon improvement vs track 10,000m as a less-affected control
2. **Within-athlete paired** — same-athlete pre/post-era delta, controlling for genetics, training, physiology
3. **Cohort survival** — distributional shift in the top-30 elite cohort, with a 55% shoe-attribution share

Plus historical comparison, four robustness scenarios, and an honest accounting of limitations.

## Headline findings

- **Pooled shoe contribution: 67 seconds (95% CI 36–99 s)** in median elite marathon time, equivalent to **~0.9% of a 2:05 marathon**
- The within-athlete framework is the most conservative (47 s, wide CI). The DiD is the highest (111 s, women-only on pre-side). All three frameworks agree on order of magnitude.
- **Sub-2:10 (men) and sub-2:25 (women) frequencies rose 1.25–1.4× post-2017** — substantial but smaller than the 3–5× cited in popular running press
- **Track 10,000m did improve too (~0.3%) but markedly less than road marathon (~1.6%)**, supporting the shoe story
- Changepoint detection places the cohort-survival structural break at **2020**, consistent with broad-cohort adoption following elite adoption in 2017–2018

Full methodology, statistical tests, sensitivity analysis, and limitations in [`writeup.md`](writeup.md).

## Repository structure

```
marathon-shoe-revolution-decomposition/
├── data/                              # Four source CSVs + image assets
│   ├── elite_marathon_times.csv       # 1,908 rows scraped from 6 major-marathon Wikipedia tables, 2010–2024
│   ├── track_records_control.csv      # 27 rows of 10,000m performances 2016–2024 (sparse — see writeup §9)
│   ├── shoe_timeline.csv              # Hand-compiled super-shoe release dates and milestones
│   ├── athlete_career_arcs.csv        # Derived: 17 athletes with ≥2 pre and ≥2 post elite marathons
│   └── images/                        # CC-BY-SA reference photos
├── notebooks/                         # Jupyter notebook reproducing the analysis end-to-end
├── src/                               # Python source for analysis, PDF, DOCX, HTML
├── outputs/                           # Generated 400-DPI figures and results CSV
├── reports/                           # PDF and Word versions of the formal writeup
├── web/                               # Self-contained HTML article + matching short-form PDF/DOCX
├── writeup.md                         # Full report in markdown — renders on GitHub
├── article.md                         # Narrative blog version, looser voice
├── README.md                          # This file
├── LICENSE                            # MIT
└── requirements.txt
```

## Reproducing the analysis

```bash
git clone https://github.com/lyhjeremy/marathon-shoe-revolution-decomposition.git
cd marathon-shoe-revolution-decomposition
pip install -r requirements.txt
python src/analysis.py
```

Wall-clock time: under 60 seconds on an M1 MacBook. The analysis script regenerates all 8 figures, both writeup-supporting CSVs, and the full JSON results summary.

To rebuild the PDF/DOCX/HTML deliverables:

```bash
python src/generate_pdf.py
python src/generate_docx.py
python src/generate_html.py
python src/build_notebook.py
```

To re-scrape the source data (idempotent, takes ~3 minutes):

```bash
python scripts/scrape_marathons.py
python scripts/scrape_track.py
```

Or open [`notebooks/shoe_revolution_decomposition.ipynb`](notebooks/shoe_revolution_decomposition.ipynb) in Jupyter / VS Code and run all cells.

## Data sources

| Dataset | Source | Coverage |
|---------|--------|----------|
| Elite marathon times | Wikipedia race-result tables (Berlin, London, Chicago, Boston, Tokyo, NYC, Dubai) | 2010–2024, 1,908 rows |
| 10,000m track | [Wikipedia 10,000 metres](https://en.wikipedia.org/wiki/10,000_metres) + record progression pages | 2016–2024, 27 rows |
| Shoe release timeline | Manufacturer announcements + race archives | 2016–2024, hand-compiled |
| Vaporfly biomechanics | [Hoogkamer et al. 2018](https://doi.org/10.1007/s40279-017-0811-2), Senefeld et al. 2023 | Lab/literature |

## License

MIT — see [LICENSE](LICENSE). Image attributions are listed in [`article.md`](article.md#image-credits). All eight analytical figures (`outputs/figures/`) are CC-BY 4.0.

## Author

Jeremy Lee — [github.com/lyhjeremy](https://github.com/lyhjeremy)
