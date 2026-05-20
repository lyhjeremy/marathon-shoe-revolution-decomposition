"""
Scrape top 10,000m track performances from Wikipedia.

Strategy: Wikipedia's main "10,000 metres" article and the event's record
progression pages contain top-N all-time tables. Also try the 'Year' pages
in athletics for season top performances.
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


def fetch_html(title):
    url = f"https://en.wikipedia.org/wiki/{quote(title.replace(' ', '_'))}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code == 200:
            return r.text, True
        return None, False
    except Exception as e:
        print(f"  ERR fetching {title}: {e}", file=sys.stderr)
        return None, False


def parse_track_time(text):
    """Parse 10000m times: MM:SS.SS or HH:MM:SS.SS"""
    text = text.strip()
    text = re.sub(r"\[[^\]]*\]", "", text)
    text = text.replace(" ", "").replace(" ", "")
    # 26:11.00 or 26:11 or 1:01:23.4
    m = re.match(r"^(?:(\d+):)?(\d{1,2}):(\d{1,2}(?:\.\d+)?)$", text)
    if not m:
        return None
    h, mins, secs = m.groups()
    try:
        total = (int(h) if h else 0) * 3600 + int(mins) * 60 + float(secs)
        return int(round(total))
    except Exception:
        return None


def extract_date_year(text):
    """Extract a 4-digit year from a string like '7 May 2005' or '2005-05-07'."""
    m = re.search(r"\b(19|20)\d{2}\b", text or "")
    return int(m.group(0)) if m else None


def parse_tables(html, gender_hint):
    """
    Find all wikitables; extract rows with a 10000m-style time.
    gender_hint: 'M' or 'W' or None (inferred from headings).
    """
    soup = BeautifulSoup(html, "lxml")
    rows = []

    for t in soup.find_all("table", class_=re.compile(r"wikitable")):
        prev = t.find_previous(["h2", "h3", "h4"])
        section_label = prev.get_text(" ", strip=True).lower() if prev else ""
        if gender_hint:
            gender = gender_hint
        elif "women" in section_label or "female" in section_label:
            gender = "W"
        elif "men" in section_label or "male" in section_label:
            gender = "M"
        else:
            gender = None
        if gender is None:
            continue

        trs = t.find_all("tr")
        if len(trs) < 3:
            continue

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
        time_i = idx_of("time", "result", "mark", "performance")
        date_i = idx_of("date")
        venue_i = idx_of("venue", "location", "place", "city")

        if time_i is None or name_i is None:
            continue

        for tr in trs[1:]:
            cells = tr.find_all(["td", "th"])
            if len(cells) <= time_i:
                continue
            time_text = cells[time_i].get_text(" ", strip=True)
            t_sec = parse_track_time(time_text)
            if t_sec is None:
                continue
            # 10000m elite range: 26:00 (1560s) to 36:00 (2160s)
            if not (1500 <= t_sec <= 2200):
                continue
            athlete = cells[name_i].get_text(" ", strip=True)
            athlete = re.sub(r"\[[^\]]*\]", "", athlete).strip()
            if not athlete:
                continue
            nat = cells[nat_i].get_text(" ", strip=True) if nat_i is not None and nat_i < len(cells) else ""
            nat = re.sub(r"\[[^\]]*\]", "", nat).strip()
            date_txt = cells[date_i].get_text(" ", strip=True) if date_i is not None and date_i < len(cells) else ""
            venue = cells[venue_i].get_text(" ", strip=True) if venue_i is not None and venue_i < len(cells) else ""
            year = extract_date_year(date_txt)
            if year is None:
                continue
            if not (2010 <= year <= 2024):
                continue
            rows.append({
                "athlete_name": athlete,
                "gender": gender,
                "nationality": nat,
                "date": date_txt,
                "event_m": 10000,
                "finish_time_seconds": t_sec,
                "year": year,
                "venue": venue,
            })

    return rows


def main():
    all_rows = []

    targets = [
        # (page title, gender_hint)
        ("Men's 10,000 metres world record progression", "M"),
        ("Women's 10,000 metres world record progression", "W"),
        ("10,000 metres", None),
        ("2010 in athletics (track and field)", None),
        ("2011 in athletics (track and field)", None),
        ("2012 in athletics (track and field)", None),
        ("2013 in athletics (track and field)", None),
        ("2014 in athletics (track and field)", None),
        ("2015 in athletics (track and field)", None),
        ("2016 in athletics (track and field)", None),
        ("2017 in athletics (track and field)", None),
        ("2018 in athletics (track and field)", None),
        ("2019 in athletics (track and field)", None),
        ("2020 in athletics (track and field)", None),
        ("2021 in athletics (track and field)", None),
        ("2022 in athletics (track and field)", None),
        ("2023 in athletics (track and field)", None),
        ("2024 in athletics (track and field)", None),
        ("List of African 10,000 metres champions", None),
        # Olympic + Worlds finals
        ("Athletics at the 2012 Summer Olympics – Men's 10,000 metres", "M"),
        ("Athletics at the 2012 Summer Olympics – Women's 10,000 metres", "W"),
        ("Athletics at the 2016 Summer Olympics – Men's 10,000 metres", "M"),
        ("Athletics at the 2016 Summer Olympics – Women's 10,000 metres", "W"),
        ("Athletics at the 2020 Summer Olympics – Men's 10,000 metres", "M"),
        ("Athletics at the 2020 Summer Olympics – Women's 10,000 metres", "W"),
        ("Athletics at the 2024 Summer Olympics – Men's 10,000 metres", "M"),
        ("Athletics at the 2024 Summer Olympics – Women's 10,000 metres", "W"),
        ("2011 World Championships in Athletics – Men's 10,000 metres", "M"),
        ("2013 World Championships in Athletics – Men's 10,000 metres", "M"),
        ("2015 World Championships in Athletics – Men's 10,000 metres", "M"),
        ("2017 World Championships in Athletics – Men's 10,000 metres", "M"),
        ("2019 World Championships in Athletics – Men's 10,000 metres", "M"),
        ("2022 World Athletics Championships – Men's 10,000 metres", "M"),
        ("2023 World Athletics Championships – Men's 10,000 metres", "M"),
        ("2011 World Championships in Athletics – Women's 10,000 metres", "W"),
        ("2013 World Championships in Athletics – Women's 10,000 metres", "W"),
        ("2015 World Championships in Athletics – Women's 10,000 metres", "W"),
        ("2017 World Championships in Athletics – Women's 10,000 metres", "W"),
        ("2019 World Championships in Athletics – Women's 10,000 metres", "W"),
        ("2022 World Athletics Championships – Women's 10,000 metres", "W"),
        ("2023 World Athletics Championships – Women's 10,000 metres", "W"),
    ]

    for title, gender in targets:
        html, ok = fetch_html(title)
        if not ok:
            print(f"  miss: {title}")
            time.sleep(0.3)
            continue
        rows = parse_tables(html, gender_hint=gender)
        for r in rows:
            all_rows.append(r)
        print(f"  ok: {title}  +{len(rows)}")
        time.sleep(0.2)

    # Dedupe by (athlete, gender, year, time)
    seen = set()
    dedup = []
    for r in all_rows:
        key = (r["athlete_name"], r["gender"], r["year"], r["finish_time_seconds"])
        if key in seen:
            continue
        seen.add(key)
        dedup.append(r)

    out_path = os.path.join(OUT_DIR, "track_records_control.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "athlete_name", "gender", "nationality", "date",
            "event_m", "finish_time_seconds", "year", "venue"])
        writer.writeheader()
        for r in dedup:
            writer.writerow(r)
    print(f"\n{len(dedup)} unique rows -> {out_path}")


if __name__ == "__main__":
    main()
