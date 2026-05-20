"""
Generate a self-contained HTML article at web/index.html with all figures
embedded as base64 data URIs. Drop-in deployable (no external assets).
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
<title>How Much of the Post-2017 Marathon Revolution Is the Shoe?</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="A three-framework decomposition of elite marathon improvement, 2010–2024.">
<style>
:root {{
    --text:#1a1a2e; --soft:#555; --muted:#888;
    --men:#2563eb; --women:#dc2626; --alt:#059669;
    --bg:#fafaf7; --card:#fff; --rule:#e5e2da;
}}
* {{ box-sizing:border-box; }}
body {{
    margin:0; padding:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
    background:var(--bg); color:var(--text); line-height:1.6;
}}
.hero {{
    width:100%; height:380px; background:#222 center/cover no-repeat;
    background-image:url('{hero}');
    position:relative;
}}
.hero::after {{
    content:""; position:absolute; inset:0;
    background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,.7) 100%);
}}
.hero-text {{
    position:relative; z-index:1; height:100%;
    max-width:880px; margin:0 auto; padding:0 28px;
    display:flex; flex-direction:column; justify-content:flex-end; padding-bottom:34px;
    color:#fff;
}}
.hero-text h1 {{ font-family:Georgia,serif; font-size:38px; line-height:1.15; margin:0 0 12px 0; }}
.hero-text .sub {{ font-size:17px; opacity:.92; max-width:640px; }}
.hero-text .byline {{ margin-top:14px; font-size:14px; opacity:.85; font-style:italic; }}
.container {{ max-width:760px; margin:0 auto; padding:48px 28px 80px; }}
h2 {{ font-family:Georgia,serif; font-size:26px; margin:48px 0 12px; color:var(--text); }}
h3 {{ font-family:Georgia,serif; font-size:18px; margin:32px 0 8px; color:var(--text); }}
p {{ font-size:17px; margin:0 0 16px; }}
.lead {{ font-size:19px; color:var(--soft); margin-bottom:28px; }}
figure {{ margin:36px 0; }}
figure img {{ width:100%; height:auto; border-radius:8px; box-shadow:0 1px 3px rgba(0,0,0,.06); }}
figcaption {{ font-size:14px; color:var(--muted); font-style:italic; text-align:center; margin-top:10px; }}
blockquote {{
    border-left:4px solid var(--women); margin:24px 0; padding:14px 22px;
    background:var(--card); border-radius:0 8px 8px 0; font-size:18px; font-style:italic;
}}
table {{
    width:100%; border-collapse:collapse; margin:28px 0; font-size:15px;
    background:var(--card); border-radius:8px; overflow:hidden;
    box-shadow:0 1px 3px rgba(0,0,0,.05);
}}
th {{ background:var(--text); color:#fff; padding:11px 14px; text-align:left; font-weight:600; }}
td {{ padding:10px 14px; border-bottom:1px solid var(--rule); }}
tr:last-child td {{ border-bottom:none; }}
tr:nth-child(even) td {{ background:#f8f6f0; }}
b, strong {{ color:var(--text); }}
.code, code {{
    background:#f3eee3; padding:2px 6px; border-radius:4px; font-family:"SF Mono",Consolas,monospace; font-size:14px;
}}
pre {{
    background:var(--text); color:#f8f8f2; padding:18px 22px; border-radius:8px; overflow-x:auto;
    font-family:"SF Mono",Consolas,monospace; font-size:14px; line-height:1.5;
}}
.headline {{
    background:var(--card); border-left:6px solid var(--women); padding:22px 26px;
    margin:32px 0; border-radius:0 8px 8px 0;
    box-shadow:0 1px 3px rgba(0,0,0,.05);
}}
.headline .big {{ font-size:34px; font-weight:bold; font-family:Georgia,serif; color:var(--women); }}
.headline .label {{ color:var(--soft); font-size:14px; text-transform:uppercase; letter-spacing:.05em; margin-bottom:6px; }}
.headline .ci {{ color:var(--soft); font-size:15px; margin-top:6px; }}
.framework-row {{
    display:grid; grid-template-columns:1fr 110px 160px; gap:16px;
    padding:14px 0; border-bottom:1px solid var(--rule);
}}
.framework-row:last-child {{ border-bottom:none; }}
.framework-row .est {{ font-weight:bold; font-size:18px; color:var(--text); text-align:right; }}
.framework-row .ci {{ color:var(--muted); font-size:14px; text-align:right; }}
.framework-row .label-cell {{ font-size:15px; }}
.framework-row.pooled {{ background:#f8f6f0; padding:18px 14px; border-radius:6px; border-bottom:none; }}
.framework-row.pooled .est {{ color:var(--women); }}
.footer {{
    margin-top:60px; padding-top:30px; border-top:2px solid var(--rule);
    font-size:14px; color:var(--muted);
}}
.footer a {{ color:var(--soft); }}
@media (max-width:640px) {{
    .hero {{ height:280px; }}
    .hero-text h1 {{ font-size:28px; }}
    .container {{ padding:32px 20px 60px; }}
    .framework-row {{ grid-template-columns:1fr 1fr; }}
}}
</style>
</head>
<body>

<div class="hero">
  <div class="hero-text">
    <h1>How Much of the Post-2017 Marathon Revolution Is the Shoe?</h1>
    <div class="sub">A three-framework decomposition of elite marathon improvement, 2010–2024.</div>
    <div class="byline">Jeremy Lee · May 2026</div>
  </div>
</div>

<div class="container">

<p class="lead">When Nike's Vaporfly 4% reached commercial release in mid-2017, elite marathon times began falling at a pace that startled even close observers of the sport. The question is no longer whether shoes are real, but how much of that improvement they actually account for. Three frameworks, 1,908 elite races, one stubborn question.</p>

<div class="headline">
  <div class="label">Pooled shoe contribution</div>
  <div class="big">{pool['pooled_estimate_seconds']:.0f} seconds</div>
  <div class="ci">95% CI {pool['pooled_ci_low']:.0f}–{pool['pooled_ci_high']:.0f} s · roughly 0.9% of a 2:05 marathon</div>
</div>

<h2>What I was actually trying to answer</h2>

<p>The question I picked is empirical and bounded: <b>of the total elite marathon time improvement between the pre-Vaporfly era (2010–2016) and the post-Vaporfly era (2018–2024), how much, in seconds, is attributable to the shoe?</b></p>

<p>I refused to pick one framework. Instead I built three independent decompositions and asked whether they agreed.</p>

<h3>Framework 1 — Difference-in-Differences</h3>
<p>Compare road marathon improvement to track 10,000m improvement over the same window. Track racing did not adopt carbon plates at the same rate. If shoes are the dominant cause of road improvement, road should have improved faster than track. The difference is the shoe-attributable share.</p>

<h3>Framework 2 — Within-athlete paired</h3>
<p>Find athletes who raced elites in both eras. The same person's pre-vs-post delta cancels genetics, training history, physiology. Whatever's left is non-genetic, mostly the shoe.</p>

<h3>Framework 3 — Cohort survival</h3>
<p>Count sub-2:10 (men) and sub-2:25 (women) performances per year. Find the changepoint. Attribute a share of the cohort improvement to shoes.</p>

<h2>The three estimates</h2>

<figure>
  <img src="{figs['fig5']}" alt="Forest plot comparing the three framework estimates and the pooled value">
  <figcaption>Three frameworks plotted on the same x-axis (seconds of shoe-attributable marathon improvement). The within-athlete is the most conservative; the DiD is the highest. The pooled estimate sits between them.</figcaption>
</figure>

<div class="framework-row">
  <div class="label-cell"><b>Framework 1.</b> Difference-in-Differences (track vs road)</div>
  <div class="est">{f1['shoe_contribution_seconds']:.0f} s</div>
  <div class="ci">[{f1['ci_low']:.0f}, {f1['ci_high']:.0f}]</div>
</div>
<div class="framework-row">
  <div class="label-cell"><b>Framework 2.</b> Within-athlete paired (n={f2['n_athletes']}, p={f2['paired_p']:.2f})</div>
  <div class="est">{f2['shoe_contribution_seconds']:.0f} s</div>
  <div class="ci">[{-f2['ci_high']:.0f}, {-f2['ci_low']:.0f}]</div>
</div>
<div class="framework-row">
  <div class="label-cell"><b>Framework 3.</b> Cohort survival (changepoint = {f3['changepoint_year']})</div>
  <div class="est">{f3['shoe_contribution_seconds']:.0f} s</div>
  <div class="ci">[{f3['ci_low']:.0f}, {f3['ci_high']:.0f}]</div>
</div>
<div class="framework-row pooled">
  <div class="label-cell"><b>Pooled estimate</b> (inverse-CI-width weighted)</div>
  <div class="est">{pool['pooled_estimate_seconds']:.0f} s</div>
  <div class="ci">[{pool['pooled_ci_low']:.0f}, {pool['pooled_ci_high']:.0f}]</div>
</div>

<h2>The frequency story</h2>

<figure>
  <img src="{figs['fig1']}" alt="Sub-2:10 (men) and sub-2:25 (women) marathon performance counts per year">
  <figcaption>Sub-2:10 (men) and sub-2:25 (women) marathon performances per year. Grey is pre-Vaporfly, red is post. The 2017 transition year is orange. The Vaporfly launch is the dashed line.</figcaption>
</figure>

<p>The pre-era averaged <b>23 sub-2:10 men's performances per year</b> across our six-major dataset; the post-era averaged <b>29</b>. That's a 1.25× increase, not the 3–5× quoted in popular running press. The difference between my number and the popular figure isn't disagreement — it's scope. The 3–5× figure comes from including mid-tier marathons where shoe-driven improvement is more visible in the middle ranks.</p>

<h2>Track 10,000m didn't move the same way</h2>

<figure>
  <img src="{figs['fig2']}" alt="Road marathon and track 10,000m improvements 2010-2024">
  <figcaption>Road marathon top-50 mean time vs track 10,000m top-50 mean time, normalized to 2010 baseline. The road curve diverges sharply after 2017; the track curve doesn't.</figcaption>
</figure>

<p>Track 10,000m did improve — Cheptegei's 26:11 in 2020, Chebet's 28:54 in 2024. Just less than the road marathon did. The post-era times improved <b>~0.3%</b>. The road marathon top-30 median improved <b>~1.6%</b> over the same window. That ratio — roughly 5× — is the cleanest causal lever in the analysis.</p>

<h2>What this means</h2>

<figure>
  <img src="{figs['fig6']}" alt="Decomposition of total 2016 to 2023 elite improvement">
  <figcaption>Indicative decomposition of the ~240 seconds of total elite improvement between 2016 and 2023. The shoe slice is grounded in this study's pooled estimate; the other slices are post-hoc carve-ups based on running-stats literature.</figcaption>
</figure>

<p>Shoes account for measurable, statistically credible improvement in elite marathon times. The contribution is real but smaller than headline framings suggest — <b>around 1% of marathon time, not 4%</b>. The remaining improvement comes from deeper African talent pipelines, pacing improvements, altitude training, and race-craft. Shoes are the most-cited cause because they are the most discrete and dateable, not because they are the largest cause.</p>

<blockquote>Shoes are the most-cited cause not because they are the largest single cause, but because they are the most discrete and dateable one.</blockquote>

<h2>Reproducing this</h2>

<pre>git clone https://github.com/lyhjeremy/marathon-shoe-revolution-decomposition.git
cd marathon-shoe-revolution-decomposition
pip install -r requirements.txt
python src/analysis.py</pre>

<p>Wall-clock time: under 60 seconds on an M1 MacBook. The full PDF report (with sensitivity analysis and limitations) is in <code>reports/</code>. The Jupyter notebook reproduces every number cell-by-cell.</p>

<div class="footer">
  <p>Full code, data, and methodology at <a href="https://github.com/lyhjeremy/marathon-shoe-revolution-decomposition">github.com/lyhjeremy/marathon-shoe-revolution-decomposition</a></p>
  <p>Hero photograph: Berlin Marathon 2011 by Mr.choppers, CC-BY-SA 3.0 via Wikimedia Commons. All analytical figures are original to this work and CC-BY 4.0.</p>
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
