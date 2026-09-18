# Kanoon office directory dataset

`kanoon_agencies.sqlite3` is the recommended database file. It contains one table, `kanoon_agencies`, with 418 records obtained from the public Kanoon agency directory on 2026-09-18.

Columns:

- `province`: province selected on the official directory
- `city`: city/area derived from the office title; the source does not expose a distinct city field
- `office_name`: office title exactly as published
- `address`: published address
- `phone_numbers`: published phone number or numbers
- `source_url`: official per-province source page
- `retrieved_at_utc`: collection timestamp

The equivalent `kanoon_agencies.csv` and `kanoon_agencies.json` exports have the same fields. Refresh the files with:

```powershell
.\.venv\Scripts\python.exe scripts\scrape_kanoon_agencies.py
```

Source: https://www.kanoon.ir/City/Agencies
