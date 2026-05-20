"""
Scrape elite marathon top-N results from Wikipedia race pages.
Targets: 6 major marathons × 15 years × top-20 men/women = ~3,600 row potential.
Writes to data/elite_marathon_times.csv.
"""
import csv
import os
import re
import sys
import time
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

OUT_DIR = "/Users/jeremylee/My Drive/7. Data Projects/Project 9 Marathon Shoe Revolution Decomposition/marathon-shoe-revolution-decomposition/data"
HEADERS = {
    "User-Agent": "MarathonShoeResearch/1.0 (academic research; lyhjeremy@github)"
}

# Map of (course_slug -> list of (page_title_template, year)). Template uses {year}.
RACE_PAGES = {
    "berlin":   "{year} Berlin Marathon",
    "london":   "{year} London Marathon",
    "chicago":  "{year} Chicago Marathon",
    "boston":   "{year} Boston Marathon",
    "tokyo":    "{year} Tokyo Marathon",
    "nyc":      "{year} New York City Marathon",
    "valencia": "{year} Valencia Marathon",
    "frankfurt":"{year} Frankfurt Marathon",
    "amsterdam":"{year} Amsterdam Marathon",
    "rotterdam":"{year} Rotterdam Marathon",
    "dubai":    "{year} Dubai Marathon",
    "seoul":    "{year} Seoul Marathon",
}

YEARS = list(range(2010, 2025))


def fetch_html(title):
    """Fetch a Wikipedia article HTML. Returns (html_text, found_bool)."""
    url = f"https://en.wikipedia.org/wiki/{quote(title.replace(' ', '_'))}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            return r.text, True
        return None, False
    except Exception as e:
        print(f"  ERR fetching {title}: {e}", file=sys.stderr)
        return None, False


def parse_time(text):
    """Convert various marathon-time strings (h:mm:ss, hh:mm:ss, m:ss with leading hour zero) to seconds."""
    text = text.strip()
    text = re.sub(r"\[[^\]]*\]", "", text)  # strip footnotes
    text = text.replace(" ", "").replace(" ", "")
    # Common patterns: 2:01:39, 2:01:39.5, 2.01.39
    m = re.match(r"^(\d+)[:.](\d{1,2})[:.](\d{1,2}(?:\.\d+)?)$", text)
    if not m:
        return None
    h, mins, secs = m.groups()
    try:
        total = int(h) * 3600 + int(mins) * 60 + float(secs)
        return int(round(total))
    except Exception:
        return None


def parse_race_page(html, course, year):
    """Return list of dicts: {athlete_name, gender, nationality, finish_time_seconds, ...}"""
    if not html:
        return []
    soup = BeautifulSoup(html, "lxml")
    rows = []

    # Find tables that look like results tables. Heuristic: look for tables that
    # contain at least one cell with a marathon-time-shaped string (2:something).
    tables = soup.find_all("table", class_=re.compile(r"wikitable"))
    for t in tables:
        # Get all rows
        trs = t.find_all("tr")
        if len(trs) < 3:
            continue
        # Header row: try to detect gender section ("Men", "Women") from preceding h2/h3
        # We'll determine gender by inspecting parent h2/h3 immediately before the table.
        prev = t.find_previous(["h2", "h3", "h4"])
        section_label = prev.get_text(" ", strip=True).lower() if prev else ""
        if "women" in section_label:
            gender = "W"
        elif "men" in section_label and "women" not in section_label:
            gender = "M"
        else:
            gender = None  # we'll skip indeterminate tables

        if gender is None:
            continue

        # Identify column indices by header
        header_cells = [c.get_text(" ", strip=True).lower() for c in trs[0].find_all(["th", "td"])]
        if not header_cells:
            continue

        def idx_of(*candidates):
            for i, h in enumerate(header_cells):
                for c in candidates:
                    if c in h:
                        return i
            return None

        name_i = idx_of("athlete", "name", "runner")
        nat_i = idx_of("nationality", "country", "nation")
        time_i = idx_of("time", "result")
        if time_i is None:
            continue

        for tr in trs[1:]:
            cells = tr.find_all(["td", "th"])
            if len(cells) < 3:
                continue
            time_cell = cells[time_i].get_text(" ", strip=True) if time_i < len(cells) else ""
            t_sec = parse_time(time_cell)
            if t_sec is None:
                continue
            # Sanity range for elite marathon: 2:00 to 2:45
            if not (7200 <= t_sec <= 9900):
                continue
            athlete = cells[name_i].get_text(" ", strip=True) if name_i is not None and name_i < len(cells) else ""
            athlete = re.sub(r"\[[^\]]*\]", "", athlete).strip()
            if not athlete:
                continue
            nat = cells[nat_i].get_text(" ", strip=True) if nat_i is not None and nat_i < len(cells) else ""
            nat = re.sub(r"\[[^\]]*\]", "", nat).strip()
            # Nat is often "United Kingdom" or just a flag template; normalize to IOC-ish if obvious
            nat_short = nat[:3].upper() if nat else ""
            rows.append({
                "athlete_name": athlete,
                "gender": gender,
                "nationality": nat,
                "course": course,
                "year": year,
                "finish_time_seconds": t_sec,
            })

    return rows


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "elite_marathon_times.csv")
    seen_pages = 0
    total_rows = 0
    all_rows = []

    for course, template in RACE_PAGES.items():
        for year in YEARS:
            title = template.format(year=year)
            html, ok = fetch_html(title)
            seen_pages += 1
            if not ok:
                print(f"  miss: {title}")
                time.sleep(0.4)
                continue
            rows = parse_race_page(html, course, year)
            for r in rows:
                r["date"] = ""  # not parsed
                r["age_at_race"] = ""
                # Era-based shoe label
                if year <= 2016:
                    r["known_shoe"] = "pre_vaporfly"
                elif year == 2017:
                    r["known_shoe"] = "vaporfly_4"  # transition year
                elif year == 2018:
                    r["known_shoe"] = "vaporfly_4"
                elif year == 2019:
                    r["known_shoe"] = "vaporfly_next"
                elif year >= 2020:
                    r["known_shoe"] = "super_shoe_unknown_brand"
                else:
                    r["known_shoe"] = ""
                all_rows.append(r)
            total_rows += len(rows)
            print(f"  ok: {title}  +{len(rows)} rows")
            time.sleep(0.2)

    # Dedupe by (athlete_name, course, year, finish_time_seconds)
    seen = set()
    dedup = []
    for r in all_rows:
        key = (r["athlete_name"], r["course"], r["year"], r["finish_time_seconds"])
        if key in seen:
            continue
        seen.add(key)
        dedup.append(r)

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "athlete_name", "gender", "nationality", "date", "course",
            "finish_time_seconds", "year", "age_at_race", "known_shoe"])
        writer.writeheader()
        for r in dedup:
            writer.writerow(r)

    print(f"\nDONE. {seen_pages} pages tried, {total_rows} raw rows, {len(dedup)} unique rows -> {out_path}")


if __name__ == "__main__":
    main()
