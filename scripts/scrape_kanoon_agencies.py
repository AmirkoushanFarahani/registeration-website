"""Build CSV, JSON and SQLite datasets from Kanoon's public agency directory."""
import csv
import json
import re
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.kanoon.ir/City/Agencies'
OUTPUT_DIR = Path(__file__).resolve().parents[1] / 'data'
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; student-registration-directory/1.0)'}

def clean(value):
    return ' '.join(value.stripped_strings) if value else ''

def city_from_office_name(name):
    """The source gives an office/area label, not a separate city field."""
    city = re.sub(r'\s*[\(（].*?[\)）]\s*', ' ', name)
    city = re.sub(r'\s+(پسران|دختران|خواهران|برادران)\s*$', '', city)
    return re.sub(r'\s+', ' ', city).strip()

def get_provinces(session):
    response = session.get(BASE_URL, params={'state': 1}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return [(option['value'], clean(option)) for option in soup.select('#StateCode option[value]') if option['value']]

def scrape_province(session, state_code, province, retrieved_at):
    response = session.get(BASE_URL, params={'state': state_code}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    agencies = []
    for item in soup.select('#Cities .list-group-item'):
        heading = item.select_one('h4')
        if not heading:
            continue
        office_name = clean(heading)
        agencies.append({
            'province': province,
            'city': city_from_office_name(office_name),
            'office_name': office_name,
            'address': clean(item.select_one('p.list-group-item-text')),
            'phone_numbers': clean(item.select_one('span.pull-left')),
            'source_url': f'{BASE_URL}?state={state_code}',
            'retrieved_at_utc': retrieved_at,
        })
    return agencies

def write_outputs(rows):
    OUTPUT_DIR.mkdir(exist_ok=True)
    columns = ['province', 'city', 'office_name', 'address', 'phone_numbers', 'source_url', 'retrieved_at_utc']
    with (OUTPUT_DIR / 'kanoon_agencies.csv').open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    with (OUTPUT_DIR / 'kanoon_agencies.json').open('w', encoding='utf-8') as file:
        json.dump(rows, file, ensure_ascii=False, indent=2)
    database = sqlite3.connect(OUTPUT_DIR / 'kanoon_agencies.sqlite3')
    database.execute('DROP TABLE IF EXISTS kanoon_agencies')
    database.execute('''CREATE TABLE kanoon_agencies (
        id INTEGER PRIMARY KEY, province TEXT NOT NULL, city TEXT NOT NULL,
        office_name TEXT NOT NULL, address TEXT, phone_numbers TEXT,
        source_url TEXT NOT NULL, retrieved_at_utc TEXT NOT NULL
    )''')
    database.executemany(
        '''INSERT INTO kanoon_agencies
           (province, city, office_name, address, phone_numbers, source_url, retrieved_at_utc)
           VALUES (:province, :city, :office_name, :address, :phone_numbers, :source_url, :retrieved_at_utc)''', rows)
    database.commit()
    database.close()

def main():
    retrieved_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    session = requests.Session()
    session.headers.update(HEADERS)
    rows = []
    for state_code, province in get_provinces(session):
        agencies = scrape_province(session, state_code, province, retrieved_at)
        print(f'state {state_code}: {len(agencies)} offices')
        rows.extend(agencies)
        time.sleep(0.4)
    write_outputs(rows)
    print(f'Wrote {len(rows)} offices from {len({row["province"] for row in rows})} provinces to {OUTPUT_DIR}')
    print(f'Missing addresses: {sum(not row["address"] for row in rows)}')
    print(f'Missing phone values: {sum(not row["phone_numbers"] for row in rows)}')

if __name__ == '__main__':
    main()
