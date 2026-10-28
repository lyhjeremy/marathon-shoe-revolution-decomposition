---
title: "I tried to work out how much of the marathon revolution is the shoe"
description: "Three frameworks, 1,802 elite races and one long-running argument. The answer came out at about 80 seconds."
author: "Jeremy Lee"
date: 2026-05-20
tags: [marathon, super-shoes, vaporfly, running, data-analysis, python, side-project]
---

![A pack of elite marathon runners on the road](./data/images/hero_marathon_runners.jpg)
*Berlin Marathon 2011. Photo by Mr.choppers, CC-BY-SA 3.0, Wikimedia Commons; full credits at the end.*

## The argument that never ends

Spend enough time around runners and you will watch the same thread play out.

Someone posts that Kelvin Kiptum ran 2:00:35. Someone replies that it doesn't count because the shoes did it. A third person says the shoes are worth 1% and the rest is training. A fourth links a paper that measured a 4% running-economy gain on a treadmill. Someone points out that treadmills aren't races. Someone says shoes aren't doping, someone else says of course they are, and the thread dies without an answer.

I had the same question. I have run 14 marathons, the fastest a 2:48 at Berlin, and over those years road marathon records were falling faster than I could remember them falling. I wanted to know how much of that was the shoe.

As far as I could find, nobody had tried to bound it with population data. The biomechanics papers tested individual runners on treadmills. Athletes said different things depending, in part, on who sponsored them. There was no number for the shoe's share across the elite field.

So I collected the data.

## The question

**Of the elite marathon improvement between the pre-Vaporfly era (2010–2016) and the post-Vaporfly era (2018–2024), how many seconds come from the shoe?**

That is narrower than "do shoes work?" (the lab evidence says yes) or "should they be banned?" (a question about values). It has a before, an after, a unit and room for a confidence interval.

I didn't want to rest the answer on one method, so I built three:

- **Difference-in-differences.** Compare road marathon improvement with track 10,000 m improvement over the same years. Track racing took up carbon plates later and with smaller claimed gains. If shoes drove the road improvement, road should have improved faster than track, and the gap is the shoe's share.
- **Within-athlete paired.** Find runners who raced elite marathons in both eras. Comparing a runner with themselves cancels genetics, training history and physiology.
- **Cohort survival.** Count sub-2:10 (men) and sub-2:25 (women) performances per year, find the year the trend breaks, and attribute a share of the change in the top-30 median to shoes.

I expected three different answers. What I wanted to know was whether they would be in the same range.

## What I found

*Updated 28 October 2026: the first version of this analysis counted 106 wheelchair and handcycle results as running times and put the answer at 67 seconds. With them removed it is 82.*

**Shoes account for about 82 seconds of elite marathon improvement, 95% CI 6–159 seconds**, roughly 1.1% of a 2:05 marathon. The three frameworks gave 44, 71 and 199 seconds. They disagree, and the interval is wide, but none of them reaches five minutes.

![Forest plot of three framework estimates](./outputs/figures/fig5_framework_comparison.png)
*The three frameworks on one axis, in seconds of shoe-attributable improvement. The interval drawn for cohort survival sits just above its point estimate, because the bootstrap computes a different statistic from the point estimate (see the full report).*

Three things surprised me.

**The number is lower than the lab number.** The 4% in the Vaporfly's name comes from [Hoogkamer et al. 2018](https://doi.org/10.1007/s40279-017-0811-2): in 18 high-caliber male runners on a treadmill, the prototype cut the energy cost of running by 4% on average against two established racing shoes. That is economy, not race time. [Kipp, Kram and Hoogkamer 2019](https://doi.org/10.3389/fphys.2019.00079) estimate that at world-class marathon pace an economy gain buys about two-thirds as much speed, so 4% would be worth roughly 2.6% if every runner got the full lab benefit. My pooled 1.1% is well under that. The rest of the post-2017 improvement comes from deeper East African fields, better pacing, altitude training and race craft.

**The track control was messier than I hoped.** Track 10,000 m times did improve: Cheptegei ran 26:11 in 2020 and Chebet 28:54 in 2024. They improved much less than the road marathon, though. Women's track improved about 0.3% between eras; the women's road marathon top-50 median improved about 2.6%. That eight-to-one gap is the strongest single piece of evidence in the project. Something road-specific changed, and the shoe is the most obvious road-specific change.

**The within-athlete group is tiny.** I expected 80 to 150 runners who raced majors in both 2010–2016 and 2018–2024. After requiring at least two races on each side and removing wheelchair racers, there were 16. Most pre-Vaporfly elites had retired, moved to ultras or been injured by 2018. The ones who stayed are a survivor group with unusually durable careers. Their median change is 44 seconds faster after the Vaporfly, but the paired t-test gives p = 0.39. With a sample that small, a weak result says more about the sample than about the effect. The race tables carry no ages, so I couldn't correct for these runners being several years older in the second era. An age correction would push the shoe estimate up.

![Within-athlete paired pre vs post](./outputs/figures/fig3_within_athlete_paired.png)
*Each line is one of the 16 runners who raced elite marathons in both eras. Red lines got faster, grey didn't. Most got faster, and the interval on the average is wide.*

## The frequency story

The plainest chart is the count of fast performances per year.

![Sub-2:10 and sub-2:25 marathon performances per year, 2010–2024](./outputs/figures/fig1_sub210_frequency_by_year.png)
*Top: men's sub-2:10. Bottom: women's sub-2:25. Grey is pre-Vaporfly, orange the 2017 transition, red post. The dashed line is the Vaporfly launch.*

Before the Vaporfly, my six-major dataset averaged 23 sub-2:10 men's performances a year. Afterwards it averaged 29, a 1.25× rise. Women under 2:25 went from 13 a year to 25, about twice as many. At the six majors the number of fast finishers is limited by the size of the lead packs, so these counts understate how much the field as a whole sped up.

What moved a lot was the median of the top 30, which dropped by 66 seconds for men and 192 seconds for women between eras. Framework 3 is built on that number.

## The data, and its limits

The original plan was to use ARRS (Association of Road Racing Statisticians) and World Athletics for verified top-100 lists per year. ARRS blocked me after one request, and the World Athletics pages are rendered in JavaScript and needed headless-browser scraping I didn't have time for. I fell back to Wikipedia race-result tables for six major marathons.

That gave 1,908 rows, with names, times and races. The scraper read gender from the heading above each table, so 106 of those rows came from "Wheelchair women" and "Handcycle women" tables; I missed that until October 2026 and the analysis now drops them, leaving 1,802 running performances. Depth varies by year: 107 finishers across the dataset in 2011, 157 in 2017 and 20 in 2020. The track 10,000 m data is worse, 27 rows, all from 2016 on. The difference-in-differences is in effect one pre-era year (2016) against seven post-era years, for women only. There is no men's pre-era track data at all.

The [full report](https://github.com/lyhjeremy/marathon-shoe-revolution-decomposition/blob/main/writeup.md) documents all of this. Better data from ARRS or Tilastopaja would tighten the intervals, and I don't know how far it would move the headline.

## What this means for a recreational runner

Probably less than you'd hope. The lab evidence for recreational runners is mixed: forefoot strikers at faster paces gain more, heel strikers at moderate paces gain less. If you run four-hour marathons and read that the shoes are worth 12 minutes, I'd discount that heavily. The plate and foam are tuned for elite mechanics and elite speeds.

For elite racing, the shoe is about a minute and a half of a two-hour marathon, give or take a lot. The rest comes from everything else that changed over the same years.

![Shoe estimate against an assumed 240-second total](./outputs/figures/fig6_decomposition_pie.png)
*An illustration, not a result. The shoe slice is this study's pooled estimate. The 240-second total for 2016–2023 and the split of the remainder are fixed assumptions in the plotting code.*

## Reproducibility

The repo is [github.com/lyhjeremy/marathon-shoe-revolution-decomposition](https://github.com/lyhjeremy/marathon-shoe-revolution-decomposition).

```bash
git clone https://github.com/lyhjeremy/marathon-shoe-revolution-decomposition.git
cd marathon-shoe-revolution-decomposition
pip install -r requirements.txt
python src/analysis.py
```

It runs in under a minute. The notebook in `notebooks/` walks through the same numbers with notes between cells, the [full report](https://github.com/lyhjeremy/marathon-shoe-revolution-decomposition/blob/main/writeup.md) has the statistical detail, and the PDF is in [`reports/`](reports/). If you find a bug, open an issue or a pull request.

## Image credits

- **Hero image:** Berlin Marathon 2011 by [Mr.choppers](https://commons.wikimedia.org/wiki/File:Berlin_Marathon_2011.JPG), CC-BY-SA 3.0
- **Vaporfly cutaway:** [User:Hpvpzgrpv](https://commons.wikimedia.org/wiki/File:Nike_Vaporfly_Cut_in_Half.png), CC-BY-SA 4.0
- **Vaporfly Next:** [User:ChoyByHK](https://commons.wikimedia.org/wiki/File:HK_clothing_NIKE_brand_Vaporfly_Next_sneakers_white_n_silver_shoes_October_2022_Px3_05.jpg), CC-BY-SA 4.0
- **Athlete photograph:** Berlin-Marathon 2015 Runners by a Wikimedia Commons contributor, CC-BY-SA

The eight analytical figures are original to this work and CC-BY 4.0.
