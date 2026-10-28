"""
Generate the short HTML report at web/index.html with all figures
embedded as base64 data URIs. Fonts and color tokens come from ../assets/family.css.
"""
import base64
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
FIG_DIR = os.path.join(PROJECT_DIR, 'outputs', 'figures')
IMG_DIR = os.path.join(PROJECT_DIR, 'data', 'images')
SUMMARY_PATH = os.path.join(PROJECT_DIR, 'outputs', 'analysis_summary.json')
OUT_PATH = os.path.join(PROJECT_DIR, 'web', 'index.html')

# Ledger "road" family. Tokens and fonts come from ../assets/family.css.
REPORT_CSS = """
* { box-sizing:border-box; border-radius:0; }
body { margin:0; background:var(--paper); color:var(--ink); font-family:var(--font-head); line-height:1.65;
       border-top:6px solid var(--signal-2); }
a { color:var(--signal); }
a:hover { color:var(--ink); }
:focus-visible { outline:2px solid var(--signal); outline-offset:3px; }
.bar { display:block; background:var(--ink); color:var(--paper); text-align:center; padding:10px 18px;
       font:600 14.5px/1.45 var(--font-body); text-decoration:none; }
.bar:hover { color:var(--paper); text-decoration:underline; }
.container { max-width:760px; margin:0 auto; padding:30px 22px 80px; }
.crumb { font:400 12.5px/1.4 var(--font-mono); text-transform:uppercase; letter-spacing:.08em; color:var(--ink-2);
         border-bottom:1px solid var(--rule); padding-bottom:10px; margin:0 0 26px; }
.crumb a { color:var(--ink-2); }
h1 { font:700 clamp(40px,7vw,68px)/.95 var(--font-display); text-transform:uppercase; letter-spacing:-.005em; margin:0 0 14px; }
.sub { font-family:var(--font-body); color:var(--ink-2); font-size:16px; margin:0 0 6px; }
h2 { font:700 clamp(28px,4.2vw,38px)/1.02 var(--font-display); text-transform:uppercase; margin:52px 0 14px; }
h3 { font:600 22px/1.1 var(--font-display); text-transform:uppercase; letter-spacing:.02em; color:var(--signal-2); margin:28px 0 6px; }
p { font-size:17.5px; margin:0 0 16px; }
p.small { font-family:var(--font-body); font-size:14px; color:var(--ink-2); }
.lead { font-size:19.5px; margin:26px 0 0; }
ul { padding-left:1.2em; } li { margin:0 0 8px; font-size:17px; }
figure { margin:30px 0; }
figure img { width:100%; height:auto; display:block; border:1px solid var(--rule); background:var(--panel); }
figure.photo img { border:0; }
figcaption { font-family:var(--font-body); font-size:14px; color:var(--ink-2); margin-top:9px; }
table { width:100%; border-collapse:collapse; }
b, strong { color:var(--ink); }
code { font-family:var(--font-mono); font-size:.86em; background:var(--panel); padding:.1em .35em; border:1px solid var(--rule); }
pre { background:var(--panel); color:var(--ink); border:1px solid var(--rule); padding:16px 18px; overflow-x:auto;
      font-family:var(--font-mono); font-size:13.5px; line-height:1.55; }
.headline { border-top:2px solid var(--ink); border-bottom:2px solid var(--ink); padding:18px 0; margin:30px 0; }
.headline .label { font:400 12.5px/1.4 var(--font-mono); text-transform:uppercase; letter-spacing:.1em; color:var(--ink-2); }
.headline .big { font:700 clamp(56px,10vw,88px)/1 var(--font-display); color:var(--signal); text-transform:uppercase; }
.headline .ci { font:400 14.5px/1.4 var(--font-mono); color:var(--ink-2); margin-top:6px; }
.framework-row { display:grid; grid-template-columns:1fr 90px 120px; gap:14px; align-items:baseline;
                 padding:12px 0; border-bottom:1px solid var(--rule); font-family:var(--font-body); }
.framework-row .label-cell { font-size:15px; }
.framework-row .est { font:700 24px/1 var(--font-display); text-align:right; }
.framework-row .ci { font:400 14px/1.3 var(--font-mono); color:var(--ink-2); text-align:right; }
.framework-row.pooled { border-bottom:2px solid var(--ink); }
.framework-row.pooled .est { color:var(--signal); }
.footer { margin-top:56px; padding-top:22px; border-top:1px solid var(--rule); font-family:var(--font-body); }
.footer p { font-size:14px; color:var(--ink-2); }
.footer a { color:var(--ink-2); }
@media (max-width:640px) {
  .framework-row { grid-template-columns:1fr 1fr; }
  .framework-row .label-cell { grid-column:1 / -1; }
  .framework-row .est { text-align:left; }
}
"""


def img_data_uri(path):
    if not os.path.exists(path):
        return ''
    ext = os.path.splitext(path)[1].lower().lstrip('.')
    mime = {'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg'}.get(ext, 'image/png')
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    return f'data:{mime};base64,{b64}'


def main():
    with open(SUMMARY_PATH) as f:
        s = json.load(f)
    f1 = s['framework1_did']
    f2 = s['framework2_within_athlete']
    f3 = s['framework3_cohort_survival']
    pool = s['pooled']

    figs = {
        f'fig{i}': img_data_uri(os.path.join(FIG_DIR, fname))
        for i, fname in enumerate([
            'fig1_sub210_frequency_by_year.png',
            'fig2_did_track_vs_road.png',
            'fig3_within_athlete_paired.png',
            'fig4_cohort_survival.png',
            'fig5_framework_comparison.png',
            'fig6_decomposition_pie.png',
            'fig7_sensitivity.png',
            'fig8_brand_adoption_timeline.png',
        ], start=1)
    }
    hero = img_data_uri(os.path.join(IMG_DIR, 'hero_marathon_runners.jpg'))
    vaporfly_cut = img_data_uri(os.path.join(IMG_DIR, 'vaporfly_cutaway.png'))
    kipchoge = img_data_uri(os.path.join(IMG_DIR, 'kipchoge_berlin.jpg'))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>How much of the post-2017 marathon speed-up is the shoe? Short report</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="A three-framework decomposition of elite marathon improvement, 2010 to 2024. Pooled shoe contribution: {pool['pooled_estimate_seconds']:.0f} seconds.">
<link rel="stylesheet" href="../assets/family.css">
<style>{REPORT_CSS}</style>
</head>
<body>
<a class="bar" href="../overview/" data-overview-link>Read the full writeup&nbsp;&rarr;</a>

<div class="container">
<p class="crumb"><a href="../">The shoe decomposition</a> &middot; short report</p>
<h1>How much of the post-2017 marathon speed-up is the shoe?</h1>
<p class="sub">A three-framework decomposition of elite marathon improvement, 2010&ndash;2024. Jeremy Lee, May 2026. Updated 28 October 2026: 106 wheelchair and handcycle results the scraper had read as running times are now excluded, which moved the pooled estimate from 67 s to {pool['pooled_estimate_seconds']:.0f} s.</p>

<figure class="photo">
  <img src="{hero}" alt="The lead pack of runners on the road at the 2011 Berlin Marathon">
  <figcaption>Berlin Marathon 2011, before the carbon-plated era. Photo by Mr.choppers, CC-BY-SA 3.0, Wikimedia Commons.</figcaption>
</figure>

<p class="lead">Nike&rsquo;s Vaporfly 4% went on general sale in 2017, and elite marathon times dropped quickly after it. This report asks how many seconds of that drop the shoe accounts for, using 1,802 elite running performances and three methods that control for different things.</p>

<div class="headline">
  <div class="label">Pooled shoe contribution</div>
  <div class="big">{pool['pooled_estimate_seconds']:.0f} seconds</div>
  <div class="ci">95% CI {pool['pooled_ci_low']:.0f}&ndash;{pool['pooled_ci_high']:.0f} s &middot; about {pool['pooled_estimate_seconds'] / 75:.1f}% of a 2:05 marathon</div>
</div>

<h2>The question</h2>

<p>Of the elite marathon improvement between the pre-Vaporfly era (2010&ndash;2016) and the post-Vaporfly era (2018&ndash;2024), how much, in seconds, comes from the shoe? 2017 is a transition year and sits in neither window.</p>

<p>No single method answers that cleanly, so the analysis runs three and compares them.</p>

<h3>Framework 1: difference-in-differences</h3>
<p>Road marathon improvement minus track 10,000 m improvement over the same window, with the track change rescaled to marathon time. Track racing did not take up carbon plates at the same rate, so anything that sped up both events cancels out.</p>

<h3>Framework 2: within-athlete paired</h3>
<p>Athletes with at least two elite marathons in each era. Comparing a runner with themselves holds genetics and training history fixed. The race tables carry no ages, so the change is not age-adjusted.</p>

<h3>Framework 3: cohort survival</h3>
<p>Counts of sub-2:10 (men) and sub-2:25 (women) performances per year, a changepoint search on those counts, and the shift in the top-30 median between eras, of which 55% is attributed to shoes.</p>

<h2>The three estimates</h2>

<figure>
  <img src="{figs['fig5']}" alt="Forest plot of the three framework estimates and the pooled value, with the within-athlete interval crossing zero and the difference-in-differences interval far to the right">
  <figcaption>The three frameworks and the pooled value on one axis. Pooled: {pool['pooled_estimate_seconds']:.0f} s [{pool['pooled_ci_low']:.0f}, {pool['pooled_ci_high']:.0f}].</figcaption>
</figure>

<div class="framework-row">
  <div class="label-cell"><b>Framework 1.</b> Difference-in-differences (road vs track, women-only pre-era)</div>
  <div class="est">{f1['shoe_contribution_seconds']:.0f} s</div>
  <div class="ci">[{f1['ci_low']:.0f}, {f1['ci_high']:.0f}]</div>
</div>
<div class="framework-row">
  <div class="label-cell"><b>Framework 2.</b> Within-athlete paired (n={f2['n_athletes']}, p={f2['paired_p']:.2f})</div>
  <div class="est">{f2['shoe_contribution_seconds']:.0f} s</div>
  <div class="ci">[{f2['ci_low']:.0f}, {f2['ci_high']:.0f}]</div>
</div>
<div class="framework-row">
  <div class="label-cell"><b>Framework 3.</b> Cohort survival (changepoint {f3['changepoint_year']})</div>
  <div class="est">{f3['shoe_contribution_seconds']:.0f} s</div>
  <div class="ci">[{f3['ci_low']:.0f}, {f3['ci_high']:.0f}]</div>
</div>
<div class="framework-row pooled">
  <div class="label-cell"><b>Pooled</b> (weighted by inverse squared CI width)</div>
  <div class="est">{pool['pooled_estimate_seconds']:.0f} s</div>
  <div class="ci">[{pool['pooled_ci_low']:.0f}, {pool['pooled_ci_high']:.0f}]</div>
</div>

<p class="small">The cohort-survival interval lies just above its point estimate because the point uses year medians and the bootstrap resamples row means. Both are reported as computed.</p>

<h2>Fast times became more common, women&rsquo;s most of all</h2>

<figure>
  <img src="{figs['fig1']}" alt="Bar charts of sub-2:10 men's and sub-2:25 women's marathon performances per year, 2010 to 2024, higher after 2017">
  <figcaption>Sub-2:10 (men) and sub-2:25 (women) performances per year in the dataset. The dashed line is the Vaporfly&rsquo;s commercial release.</figcaption>
</figure>

<p>The pre-era averaged <b>{f3['sub_m_pre_mean']:.0f} sub-2:10 men&rsquo;s performances per year</b> across the major-marathon dataset and the post-era averaged <b>{f3['sub_m_post_mean']:.0f}</b>, a {f3['sub_m_post_mean'] / f3['sub_m_pre_mean']:.2f}&times; rise. Women under 2:25 went from {f3['sub_w_pre_mean']:.0f} a year to {f3['sub_w_post_mean']:.0f}, {f3['sub_w_post_mean'] / f3['sub_w_pre_mean']:.1f}&times;. At the majors the count is capped by the size of the lead packs, so these ratios understate the change across the sport.</p>

<h2>Track 10,000 m improved far less</h2>

<figure>
  <img src="{figs['fig2']}" alt="Road marathon and track 10,000 metre times normalized to 2010, with the road line falling further after 2017">
  <figcaption>Road marathon top-50 mean against track 10,000 m top-50 mean, each normalized to 2010.</figcaption>
</figure>

<p>Track times did improve: Cheptegei ran 26:11 in 2020 and Chebet 28:54 in 2024. Across the eras the women&rsquo;s track numbers moved about <b>{f1['by_gender']['W']['trk_pct']:.1f}%</b> while the women&rsquo;s road marathon top-50 median moved about <b>{f1['by_gender']['W']['road_pct']:.1f}%</b>. That gap, roughly eight to one, is the main evidence for something road-specific, and the shoe is the most obvious road-specific change. The track control is thin, though: 27 performances, and only 2016 on the pre-era side.</p>

<h2>What it adds up to</h2>

<p>The shoe accounts for about a minute and a half of elite marathon time, close to 1%, with a wide interval. That is well short of the 4% running-economy gain measured on a treadmill (<a href="https://doi.org/10.1007/s40279-017-0811-2">Hoogkamer et al. 2018</a>). Running economy is not race time: at elite marathon pace an economy gain buys about two-thirds as much speed (<a href="https://doi.org/10.3389/fphys.2019.00079">Kipp et al. 2019</a>). Deeper East African fields, pace-controlled races and altitude training also changed over the same years. The shoe gets most of the credit in public argument partly because it has a release date.</p>

<figure>
  <img src="{figs['fig6']}" alt="Ring chart splitting an assumed 240 seconds of improvement into the shoe estimate and four other slices">
  <figcaption>Only the shoe slice comes from this study. The 240-second total and the split of the remainder are fixed assumptions in the plotting code, for illustration.</figcaption>
</figure>

<h2>Limits</h2>
<ul>
  <li>The track control has 27 rows, and its pre-era side is one year of women&rsquo;s results. Framework 1 is the weakest of the three for that reason.</li>
  <li>The within-athlete sample is {f2['n_athletes']} runners and the paired t-test is not significant (p = {f2['paired_p']:.2f}).</li>
  <li>The 55% shoe share in Framework 3 is a modeling choice, not an estimate.</li>
  <li>Era stands in for shoe use. Nobody&rsquo;s footwear is recorded per race.</li>
</ul>

<h2>Reproduce</h2>

<pre>git clone https://github.com/lyhjeremy/marathon-shoe-revolution-decomposition.git
cd marathon-shoe-revolution-decomposition
pip install -r requirements.txt
python src/analysis.py</pre>

<p>Under a minute on an M1 MacBook. The <a href="../reports/Marathon_Shoe_Revolution_Decomposition_Report.pdf">PDF report</a> has the sensitivity analysis and full limitations; the notebook in <code>notebooks/</code> reproduces every number cell by cell.</p>

<div class="footer">
  <p>Code, data and method: <a href="https://github.com/lyhjeremy/marathon-shoe-revolution-decomposition">github.com/lyhjeremy/marathon-shoe-revolution-decomposition</a> &middot; <a href="../">project page</a> &middot; <a href="../overview/">full write-up</a></p>
  <p>Photo: Berlin Marathon 2011 by Mr.choppers, CC-BY-SA 3.0 via Wikimedia Commons. Analytical figures are original to this work and CC-BY 4.0. Code MIT &copy; 2026 Jeremy Lee.</p>
</div>

</div>
</body>
</html>"""

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    size_mb = os.path.getsize(OUT_PATH) / 1024 / 1024
    print(f"  HTML saved: {OUT_PATH}  ({size_mb:.2f} MB)")


if __name__ == '__main__':
    main()
