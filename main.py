import requests
from bs4 import BeautifulSoup
import random
import re
import csv
import time

def extract_country(text):
    m = re.search(r"\(([^)]+)\)$", text)
    return m.group(1) if m else None

TOTAL_COUNTRIES = 237
YEAR = 2026

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; holiday-scraper/1.0)",
    "Accept-Language": "en,en-US;q=0.9"
}

class_to_heading = {
    "co1": "Public Holidays",
    "co2": "Local Holidays",
    "co3": "Unknown Events",
    "co4": "Typical Non Working Days",
}

output_file = "holidays_2026.csv"

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Country", "Holiday Type", "Date", "Holiday Name"])

    for COUNTRY in range(1, TOTAL_COUNTRIES + 1):
        url = f"https://www.timeanddate.com/calendar/?year={YEAR}&country={COUNTRY}"
        print(f"Processing country id {COUNTRY} -> {url}")

        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"  Skipping country id {COUNTRY}: request failed ({e})")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        country_name = extract_country(soup.find(id="ct1").find("h1").get_text())

        tables = soup.find_all("table", class_="cht lpad")

        if not tables:
            print(f"  No tables with class 'cht lpad' for country id {COUNTRY}, skipping")
            time.sleep(1)
            continue

        # Prepare result buckets
        grouped_rows = {heading: [] for heading in class_to_heading.values()}

        for table in tables:
            for tr in table.find_all("tr"):
                tds = tr.find_all("td")
                if not tds:
                    continue

                first_td = tds[0]

                # Only process rows where first TD has a span
                span = first_td.find("span")
                if not span:
                    continue

                # Identify which coX class is present
                span_classes = span.get("class", [])
                co_class = next((c for c in span_classes if c in class_to_heading), None)
                if not co_class:
                    continue

                heading = class_to_heading[co_class]

                # Clean text from each cell
                cells_text = [td.get_text(" ", strip=True) for td in tds]
                grouped_rows[heading].append(cells_text)    
    
        for group_name, holidays in grouped_rows.items():
            for row in holidays:
                date = row[0]
                name = row[1]
                
                writer.writerow([country_name, group_name, date, name])
        
        time.sleep(random.uniform(1, 3))

print(f"CSV written to {output_file}")