# How much of the post-2017 marathon revolution is the shoe?

**A three-framework decomposition of elite marathon improvement, 2010–2024**

*Jeremy Lee · May 2026, revised October 2026 (wheelchair results removed 28 October 2026) · [github.com/lyhjeremy/marathon-shoe-revolution-decomposition](https://github.com/lyhjeremy/marathon-shoe-revolution-decomposition)*

> This is the GitHub-readable version of the [PDF report](reports/Marathon_Shoe_Revolution_Decomposition_Report.pdf) and [Word doc](reports/Marathon_Shoe_Revolution_Decomposition_Report.docx). The [Jupyter notebook](notebooks/shoe_revolution_decomposition.ipynb) runs the same analysis cell by cell. The October 2026 revision corrects several numbers against `outputs/analysis_summary.json` and the code; they are listed in the last section. On 28 October 2026 the 106 wheelchair and handcycle results the scraper had picked up were removed and the analysis rerun, which changed every estimate below.

---

## Abstract

The short answer is about 80 seconds. Nike's Vaporfly 4% went on general sale in mid-2017, elite marathon times fell quickly over the following years (Kelvin Kiptum ran 2:00:35 at Chicago in 2023), and this report estimates how much of that drop belongs to the shoe. It applies three decomposition frameworks to 1,802 elite marathon running performances taken from major-race Wikipedia tables for 2010–2024: (1) a difference-in-differences (DiD) comparison against track 10,000 m, an event less affected by the shoe; (2) a within-athlete paired comparison of runners who raced at the elite level in both eras; and (3) a cohort analysis of the top-30 median and of yearly sub-2:10 and sub-2:25 counts. The three estimates are 199, 44 and 71 seconds; pooled, the shoe contribution is **82 seconds (95% CI 6–159 s)** of median elite marathon time, about **1.1% of a 2:05 marathon**. That is below what treadmill running-economy studies would suggest, and the interval is wide: its lower end is close to zero. The main weaknesses are thin pre-era track data, results taken from Wikipedia where verified global rankings would be better, and the absence of athlete ages.

---

## 1. Introduction

On 6 May 2017 Eliud Kipchoge ran 2:00:25 on the Monza Formula 1 circuit in Nike's Breaking2 exhibition, alongside Lelisa Desisa and Zersenay Tadese. All three wore prototypes of the shoe Nike released that July as the Zoom Vaporfly 4%. It combined a tall stack, a curved carbon plate and a Pebax foam midsole. In a treadmill study of 18 high-caliber male runners, the prototype cut the energy cost of running by 4% on average against two established racing shoes ([Hoogkamer et al. 2018](https://doi.org/10.1007/s40279-017-0811-2)).

The records followed. Kipchoge ran 2:01:39 at Berlin in September 2018, Brigid Kosgei took 81 seconds off the women's record at Chicago in 2019 (2:14:04), Kelvin Kiptum ran 2:00:35 at Chicago in 2023, and Sabastian Sawe ran 1:59:30 at London on 26 April 2026, the first sub-two-hour marathon ratified as a world record ([World Athletics, 23 July 2026](https://worldathletics.org/news/press-releases/ratified-world-records-sawe-ehammer-charlton-mcrae-yan-duplantis-assefa)). I have run Berlin myself (my best of 14 marathons, 2:48, came there), and the question every runner in a start pen eventually asks is how much of this the shoe is doing.

Plenty else changed over the same years: deeper East African talent pipelines, time-trial pacing, laser pacing lights at Berlin and Valencia, and wider use of altitude training. Any of these could have produced part of the post-2017 drop. The biomechanics papers measure individual runners under controlled conditions, which cannot settle a population-level question on their own, so this report tries to put a number on it from race results.

It does not take up the regulatory argument (World Athletics' 2020 rule capped stack height at 40 mm), compare brands (the data is too sparse), or advise recreational runners. The target is one quantity: the shoe-attributable change in median elite marathon time between the pre-Vaporfly era (2010–2016) and the post-Vaporfly era (2018–2024), with a confidence interval. 2017 is a transition year and is excluded from both windows.

---

## 2. Data sources

Four datasets live in [`data/`](data/) and are loaded by [`src/analysis.py`](src/analysis.py).

**`elite_marathon_times.csv` (1,908 rows, 1,802 used).** Top-N finishers from per-race Wikipedia articles for Berlin, London, Chicago, Boston, Tokyo and New York, with a few Dubai entries, 2010–2024. The scraper is [`scripts/scrape_marathons.py`](scripts/scrape_marathons.py). Each row has athlete name, gender, nationality where available, course, year, finish time in seconds and an era-based `known_shoe` label. Article depth varies: some race-years list 30 or more finishers per gender, others about 10, and pre-era coverage is generally thinner. The analysis uses top-N medians to limit the effect. The scraper reads gender from the heading above each table, so 106 rows from tables headed "Wheelchair women" and "Handcycle women" (54 athletes, 2010–2022) came in as women's running results. Since 28 October 2026 `load_data()` drops them by name; the list is in `src/analysis.py`. Men's wheelchair times are under the scraper's 2:00 floor and never entered the file.

**`track_records_control.csv` (27 rows).** Top 10,000 m track performances 2016–2024, from Wikipedia's 10,000 metres article, the men's and women's record-progression pages and the 2024 Olympic results. This is the weakest input. Wikipedia keeps no year-by-year top lists for the event, and what could be scraped skews toward 2020 and later. The pre-era side is one year (2016) of women's results. The DiD therefore uses women only and treats men's track as supplementary (§3.1, §8).

**`shoe_timeline.csv` (19 rows).** Hand-compiled release dates, stack heights, plate types and first major wins for super-shoe models from 2016 to 2024, plus the 2020 World Athletics rule. Sources are manufacturer announcements and race archives.

**`athlete_career_arcs.csv` (derived).** Built by `src/analysis.py` from the marathon file: athletes with at least two pre-era and two post-era races. Sixteen qualify once wheelchair athletes are removed, and none is dropped by the 600-second filter for implausible changes. There is no age column, so no age adjustment (§3.2, §8).

**Time window.** Pre-era 2010–2016, post-era 2018–2024. The 2020 season is kept, though it has only 20 elite results. Unratified time trials (Breaking2, INEOS 1:59 Vienna) are not in the dataset.

---

## 3. Methodology

### 3.1 Framework 1: difference-in-differences (track vs road)

Track 10,000 m racing did not take up carbon plates at the same rate or with the same claimed effect. Track spikes changed too (Nike Dragonfly in 2020, Asics Metaspeed LD), but later and with smaller marketed gains. If shoes drove most of the road improvement, road times should have improved faster than track times over the same window:

```
DiD_marathon_seconds = (road_post − road_pre) − (track_post − track_pre)
```

The track change is converted to marathon-time terms by applying its percentage change to the marathon time. The point estimate uses top-50 year medians per gender (`main()` calls the function with n = 50; where a race-year has fewer rows, all of them are used). Only women have pre-era track data (2016), so the point estimate is women-only. The bootstrap CI draws 1,000 resamples of marathon rows with the track aggregates held fixed.

A placebo DiD splits the pre-era into 2010–2013 and 2014–2016, a window with no shoe change. It should be near zero.

### 3.2 Framework 2: within-athlete paired

Comparing a runner with themselves holds genetics, training history and physiology fixed. For each athlete with at least two pre-era and two post-era major-marathon results, the change is post-era mean time minus pre-era mean time. The report gives the median across athletes (less sensitive to a single bad race than the mean), a paired t-test against zero, and a bootstrap 95% CI on the mean.

The original plan included an age adjustment. The race tables carry no ages, so the change is raw. Runners in the paired group were typically four to six years older in the post-era, and an aging penalty is not subtracted. That pushes this estimate toward zero.

### 3.3 Framework 3: cohort survival

For each year the script counts performances under 2:10 (men) and 2:25 (women) and computes the top-30 median per gender. A changepoint search tests candidate years from 2014 to 2020 and picks the one that best explains a change in slope of the yearly counts. The framework's estimate is the change in top-30 median between eras, averaged over men and women, with **55%** attributed to shoes and the rest to deeper fields, pacing, altitude and unexplained variation. The 55% is a value set in the code, not a measured one. For scale, [Kipp, Kram and Hoogkamer 2019](https://doi.org/10.3389/fphys.2019.00079) estimate that at world-class marathon pace a running-economy gain buys about two-thirds as much speed (3% economy gives 1.97% at 2:04 pace), so the 4% lab result would be worth roughly 2.6%, about 190 s on a 7,500 s marathon, if every runner got the full lab benefit. It is an assumption, and §7 shows what happens when it moves.

### 3.4 Pooling

The three frameworks measure overlapping but different things. The pooled estimate weights each by the inverse square of its 95% CI width, so the framework with the narrowest interval counts most. The pooled interval is the pooled value ± 1.96 × (standard deviation of the three point estimates) / √3. That makes it a spread-based interval; no bootstrap is involved at this step.

---

## 4. Results

### 4.1 Framework 1 (DiD): 199 seconds, 95% CI [161, 303]

![Figure 1: Road marathon and track 10,000 m top-50 times normalized to 2010.](outputs/figures/fig2_did_track_vs_road.png)

*Figure 1. Road marathon top-50 mean time against track 10,000 m top-50 mean time, each normalized to 2010.*

The women's road marathon top-50 median improved **228 seconds** (2.57%) between eras. Women's track 10,000 m improved **0.32%**, about 6 seconds on a 10,000 m time. Applying 0.32% to the marathon time gives **29 seconds** that a general speed-up would explain. The residual, **199 seconds**, is attributed to road-specific causes, of which the shoe is the most obvious.

The bootstrap 95% CI is [161, 303]. The point estimate and the interval measure slightly different things: the point estimate averages top-50 medians per year, while each bootstrap draw takes the median of all resampled rows in each era. Before the wheelchair rows were removed the interval sat entirely above the point estimate; now it contains it. Both are reported as the script produces them.

The **placebo DiD** (2010–2013 against 2014–2016, marathon only) is **40 seconds** (39.5). With no shoe change inside that window it should be close to zero; it comes out at about a fifth of the main estimate, which says how much noise the DiD carries.

### 4.2 Framework 2 (within-athlete paired): 44 seconds, 95% CI [−37, 131]

![Figure 2: Within-athlete pre vs post marathon times. Each line is one athlete.](outputs/figures/fig3_within_athlete_paired.png)

*Figure 2. Pre-era and post-era mean finish time for each of the 16 athletes with at least two elite marathons in each era. Red lines improved, grey did not.*

The median change is **−44 seconds** (post-era career-mean time was 44 seconds faster), and 10 of the 16 runners (62.5%) improved. The paired t-test gives t = −0.88, p = 0.39, which is far from significance at 0.05. The bootstrap 95% CI on the mean change is [−131, 37] seconds, which is [−37, 131] when expressed as a shoe contribution. With 16 runners, this estimate is suggestive at best.

Two biases both push it toward zero. Most pre-era elites stopped racing elite marathons before 2018, so the survivors are runners whose careers held up across the boundary, and aging would slow them slightly without any shoe effect. The missing age adjustment works in the same direction.

### 4.3 Framework 3 (cohort survival): 71 seconds, 95% CI [73, 124]

![Figure 3: Time needed to make the dataset's top 50 each year, men and women.](outputs/figures/fig4_cohort_survival.png)

*Figure 3. The time needed to make the dataset's top 50 each year, men and women. The axis is inverted, so lower on the chart is faster.*

![Figure 4: Sub-2:10 (men) and sub-2:25 (women) marathon performances per year, 2010–2024.](outputs/figures/fig1_sub210_frequency_by_year.png)

*Figure 4. Sub-2:10 (men) and sub-2:25 (women) performances per year. Grey bars are pre-era, orange the 2017 transition, red post-era. The dashed line marks the Vaporfly's commercial release.*

The top-30 median, averaged over men (66 s) and women (192 s), improved **129 seconds** between eras (bootstrap CI 132–225). The changepoint search puts the break at **2020**, three years after the commercial launch, which fits elites adopting the shoe in 2017–2018 and the wider field following in 2019–2020. Attributing 55% to shoes gives **71 seconds**, 95% CI [73, 124]. The interval sits just above the point estimate for the same kind of reason as the DiD's used to: the point estimate uses yearly top-30 medians, while the bootstrap compares means of 200 resampled rows from each era.

Sub-2:10 men's performances averaged 23 a year before and 29 after; sub-2:25 women's went from 13 to 25. The ratios are 1.25× and 2.0×. This dataset covers six majors, where the number of fast times is limited by the size of the lead packs, so these counts say little about the sport as a whole.

### 4.4 Pooled: 82 seconds, 95% CI [6, 159]

![Figure 5: Forest plot of the three framework estimates and the pooled estimate.](outputs/figures/fig5_framework_comparison.png)

*Figure 5. The three frameworks and the pooled value on one axis, redrawn on 28 October 2026 by the rerun without wheelchair results.*

| Framework | Point estimate | 95% CI | Notes |
|---|---:|---|---|
| 1. DiD (track-controlled) | 199 s | [161, 303] | Women-only pre-era |
| 2. Within-athlete paired | 44 s | [−37, 131] | n = 16, not age-adjusted |
| 3. Cohort survival | 71 s | [73, 124] | 55% of cohort improvement |
| **Pooled** | **82 s** | **[6, 159]** | Inverse squared CI width weights |

Cohort survival has the narrowest interval and carries about 82% of the pooled weight; the DiD carries about 11% and the within-athlete framework, with the widest interval, about 8%. As a share of a 2:05 marathon, 82 seconds is **1.1%**, 95% CI [0.1%, 2.1%]. The pooled interval is wide because it is built from the spread of the three estimates, and the DiD now sits far from the other two.

---

## 5. Findings across frameworks

The three estimates run from 44 to 199 seconds. The frameworks rest on different assumptions and different slices of the data. The DiD, built on one year of pre-era track data, is the outlier at more than three minutes; the pooled value sits near the lower two because cohort survival dominates the weighting.

Fast times did become more common: 1.25× for men under 2:10 and 2.0× for women under 2:25 in the six majors covered here.

Track barely moved. Women's 10,000 m improved 0.32% against the road marathon's 2.57%, about an eighth as much. The track data is thin and spikes changed too, so it is an imperfect control, but the gap is large and it is still the strongest comparison in the analysis.

![Figure 6: Shoe estimate shown against an assumed 240-second total improvement.](outputs/figures/fig6_decomposition_pie.png)

*Figure 6. Illustration only. The shoe slice is the pooled estimate. The 240-second total for 2016–2023 and the split of the remainder (40% deeper fields, 25% altitude, 20% pacing, 15% unexplained) are fixed values in the plotting code, not results.*

---

## 6. Historical comparison

Earlier changes in racing shoes are harder to isolate. The move to EVA foam midsoles in 1972–1975 coincided with rapid growth in road-running participation, so technology and population effects are mixed together. The lightweight racing flats of the 1990s brought no comparable population-level break.

The 2017–2020 change is easier to study because adoption was fast. Elite runners moved to carbon-plated shoes within about a year of release, and other brands followed within three years: Saucony, New Balance and Adidas in 2020, Asics and Puma in 2021 and Hoka in 2022.

![Figure 7: Year each brand introduced its first carbon-plated marathon shoe, 2016–2024.](outputs/figures/fig8_brand_adoption_timeline.png)

*Figure 7. The year each brand released its first carbon-plated marathon shoe, from `data/shoe_timeline.csv`. The shaded band marks 2017–2020.*

---

## 7. Sensitivity analysis

![Figure 8: DiD estimate under each sensitivity setting, with the within-athlete estimate for comparison.](outputs/figures/fig7_sensitivity.png)

*Figure 8. DiD shoe contribution under each sensitivity setting, with the within-athlete estimate shown for comparison.*

The sensitivity code in `fig7_sensitivity()` reruns the DiD with a top-50 baseline:

- **Top 25 per year instead of top 50:** 183 s. Thinner coverage in early years moves the estimate by about 16 seconds.
- **Excluding Eliud Kipchoge:** 199 s, unchanged. The point estimate is women-only, so removing a man cannot move it; this check tests nothing.
- **Excluding time-trial events** (any course matching Vienna, Monza, INEOS or Breaking2): 199 s, unchanged. None were in the canonical dataset to begin with.

The bootstrap interval is [161, 303] in every setting, which suggests the CI calculation does not respond to these filters.

**Changing the 55% share.** The script has no option for this, so the numbers were recomputed from `analysis_summary.json` with the same pooling formula. At 40% the cohort estimate falls to 52 s and the pooled value to about 60 s. At 70% they rise to 90 s and about 102 s. The pooled estimate moves roughly in step with this assumption, because cohort survival carries most of the weight.

---

## 8. Limitations

The weakest input is the track data. Wikipedia has no year-by-year top lists for the 10,000 m and its all-time lists lean toward recent years, so the DiD compares one pre-era year against seven post-era years, for women only. ARRS, World Athletics archives or Tilastopaja data would strengthen it.

The race tables have no ages, so nothing is age-adjusted. An elite marathoner aged 28 to 33 would be expected to lose something like 30 to 60 seconds over that span; leaving it in biases the within-athlete estimate downward, which makes 44 seconds conservative. That estimate also has little statistical power (n = 16, p = 0.39): it is suggestive and no more. Until 28 October 2026 the paired group had 17 runners and included Shelly Woods, a wheelchair racer whose pre-era mean of 2:11:04 was faster than the women's running world record of the time; she and every other wheelchair and handcycle athlete are now excluded.

Wikipedia coverage is uneven. Some race-years have full tables and others a podium and a few times. Medians of the top 30 reduce the effect, but it still widens the bootstrap intervals.

Several confounders are only partly handled. Kenyan and Ethiopian elite marathoning expanded after 2017 for reasons unrelated to shoes; the within-athlete design controls for this directly, the DiD partly (East African runners also dominate the 10,000 m), and the cohort framework not at all, which is one reason it attributes only 55% to shoes. Post-2017 elites increasingly chose fast, paced courses such as Berlin, Valencia and Chicago, and the dataset covers those alongside Boston, New York and Tokyo in unequal proportion, which may inflate the post-era improvement slightly. Laser pacing lights at Berlin from 2019 and structured pacing at Valencia improved times independently of shoes, and they are not credited to shoes here.

No race records which shoe each runner wore. Era stands in for shoe use, so a runner in older shoes in 2019 counts as treated.

Finally, the design cannot rule out unobserved performance enhancement, legal or not, that happened to coincide with the shoe launch. The track comparison helps only if such effects reached road and track alike.

---

## 9. Conclusion

The three frameworks put the shoe-attributable share of elite marathon improvement between 2010–2016 and 2018–2024 at **82 seconds of median elite marathon time, 95% CI 6–159 seconds**, about **1.1%** for a 2:05 runner. The interval is wide; its low end is close to zero and its high end is over two and a half minutes.

For readers who trust one framework more than the others:

- **Within-athlete**, 44 s: the cleanest design, but 16 runners and no age adjustment, which biases it down.
- **DiD**, 199 s: the strongest comparison between a treated and a less-treated event, but the pre-era control is one year of women's track data.
- **Cohort survival**, 71 s: the most data, but the 55% share is a choice.

The pooled value leans on the cohort framework because its interval is the narrowest. Someone who weights the DiD's design more heavily would land higher.

The data does not show that shoes explain the whole 2017–2024 improvement, that one brand beats another, or that recreational runners should expect the elite effect; lab evidence suggests the benefit is smaller at slower paces and for heel strikers. What it supports is that the shoe is one of several causes, alongside deeper fields, pacing and altitude training, and the most cited of them, partly because it has a release date.

---

## Reproducibility

```bash
git clone https://github.com/lyhjeremy/marathon-shoe-revolution-decomposition.git
cd marathon-shoe-revolution-decomposition
pip install -r requirements.txt
python src/analysis.py
```

The script regenerates the figures, `outputs/analysis_results.csv` and `outputs/analysis_summary.json` in under a minute on an M1 MacBook. The notebook in [`notebooks/`](notebooks/) walks through the same numbers.

## Corrections in the October 2026 revision

- The abstract said the 2:00:35 was run at Chicago in 2024; `shoe_timeline.csv` and the record books give 2023.
- Statements that the men's record fell 1:51 and the women's 4:08 from 2017 to 2024, and that records had improved about one second a year before that, were removed. They are not computed anywhere in the repo and did not match the record times.
- The pooled interval was described as a bootstrap. `synthesize()` computes it from the spread of the three estimates.
- The conclusion said the DiD had the widest interval. The within-athlete interval (162 s) is wider than the DiD's (122 s).
- Scenario A (top 25) was described as unchanged; the sensitivity figure shows 100 s against 111 s.
- Scenario D quoted pooled values of 64 s and 73 s and a 55–80 s range. Recomputing with the script's formula gives about 51 s and 80 s.
- The placebo DiD (32 s) was called an order of magnitude smaller than the main estimate; it is about a third of it.
- A men's DiD figure of about 160 s, built by applying the women's track rate to men, was removed because the script does not compute it.
- Figure 5 in `outputs/figures/` predated the current summary file and showed 117 s and 69 s. It was redrawn from a re-run of `src/analysis.py` whose JSON and CSV outputs matched the committed files exactly.
- The DiD was described as using top-30 medians; `main()` runs it on the top 50.
- 28 October 2026: 106 wheelchair and handcycle rows (54 women, among them Shelly Woods and Arielle Rausin) were removed and the analysis rerun. Pooled 67 s [36, 99] became 82 s [6, 159]; DiD 111 → 199 s, within-athlete 47 → 44 s (n 17 → 16), cohort 58 → 71 s. The "three to five times" figure for the rise in fast times was cut because no source for it could be found.

Image credits: hero and athlete photographs are CC-BY-SA from Wikimedia Commons; shoe cutaway from [`File:Nike_Vaporfly_Cut_in_Half.png`](https://commons.wikimedia.org/wiki/File:Nike_Vaporfly_Cut_in_Half.png), CC-BY-SA 4.0. The eight analytical figures are original to this work and CC-BY 4.0.
