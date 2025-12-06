import pdfkit
import time
import random

config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe") 

YEAR = 2025
OUTPUT_DIR = "./output"  # change if you want a subfolder like "calendars"
SKIP_COUNTRIES = {22, 23}

options = {
    "page-size": "A4",
    "encoding": "UTF-8",
    "quiet": "",
    # Extra safety to force English
    "custom-header": [
        ("Accept-Language", "en,en-US;q=0.9"),
    ],
}

for country in range(1, 142):
    if country in SKIP_COUNTRIES:
        print(f"Skipping country {country}")
        continue

    url = (
        "https://www.timeanddate.com/calendar/print.html"
        f"?year={YEAR}&country={country}&cols=3&df=1&lang=en"
    )

    filename = f"{OUTPUT_DIR}/calendar_{YEAR}_country_{country:03d}.pdf"

    print(f"Generating PDF for country {country}: {url}")

    try:
        pdfkit.from_url(url, filename, options=options, configuration=config)
        print(f"  ✔ Saved as {filename}")
    except Exception as e:
        print(f"  ✖ Failed for country {country}: {e}")

    time.sleep(random.uniform(1, 2))
