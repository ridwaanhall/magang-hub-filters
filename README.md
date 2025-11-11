# MagangHub Advanced Filters — scraper, merger, and search toolkit for vacancies

An OOP Python client and command-line tools to
scrape the MagangHub public vacancies API, persist raw page JSON (each
file contains an ISO UTC `_scraped_at` timestamp), merge saved pages into
a single file, and run powerful local searches. Key features include a
resilient `requests`-based scraper, a merger for numeric page files,
structured filters (e.g. `--nama_kabupaten`, `--program_studi`,
`--posisi`, `--deskripsi_posisi`), a government-postings filter
(`--gov` with `0|1|2` semantics), free-text deep search, and optional
JSON export with helper fields such as `_applicants_per_slot` and
`_acceptance_prob`.

## What is included

- `maganghub_client/` — client, models, scraper and search utilities.
- `scripts/scrape_and_save.py` — paginate the API and save each page as `1.json`, `2.json`, ...
- `scripts/build_all_json.py` — merge numbered page files into one `all.json` (optional)
- `scripts/run.py` — structured and free-text search over saved pages
- `data/` — where scraped page folders live (e.g. `data/prov_33/1.json`)

## Quick workflow

1. Scrape pages from MagangHub and save them locally.
2. (Optional) Merge page files into a single `all.json` for convenience.
3. Use `scripts/run.py` to search, filter, sort and export matches.

## Prerequisites

- Python 3.8+
- (Recommended) Virtual environment

## Install

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\activate   # PowerShell / cmd
python -m pip install -r requirements.txt
```

## Scrape (save pages)

Use the scraper to fetch pages and write them into a folder such as `data/prov_33`.

Single-line example (PowerShell / bash):

```bash
python scripts/scrape_and_save.py --save-dir data/prov_33 --kode_provinsi 33
```

## Important options

- `--save-dir` (required): directory to write pages
- `--start-page`: default 1
- `--limit`: items per page (default 100)
- `--max-pages`: optional cap
- `--delay`: politeness delay between requests

## Merge pages (unrecommend)

Combine numeric page files into `all.json`.

Single-line example:

```bash
python scripts/build_all_json.py --dir data/prov_33
```

## Search saved pages

`scripts/run.py` supports both free-text and structured searches.

Structured filters (examples):

- `--nama_kabupaten` — space-separated tokens (OR within field). Prefixes like `KAB.` / `KOTA` are removed for matching.
- `--program_studi` — tokens matched against program titles parsed from `program_studi`.
- `--posisi` — tokens matched against the `posisi` (title).
- `--deskripsi_posisi` — tokens matched in job description (and related fields).
- `--gov` — government filter: `1` = government postings only, `0` = non-government only, `2` = both (default).
- `--dir all` — search every province folder under `data/`.
- `--out` — write matched items to a JSON file (adds helper fields `_applicants_per_slot` and `_acceptance_prob`).

By default structured filters are combined with logical AND (an item must match every provided structured filter). Within a field tokens act as OR (match any). `--mode and|or` applies to free-text `--deep` queries.

## One-line examples (single line per shell)

- Bash / PowerShell (search Hukum vacancies in Surakarta or Boyolali, government postings, sorted by acceptance desc):

```bash
python scripts/run.py --dir all --nama_kabupaten "surakarta boyolali" --program_studi "hukum" --gov 1 --accept desc
```

- Windows cmd (same command in cmd.exe):

```cmd
python scripts\run.py --dir all --nama_kabupaten "surakarta boyolali" --program_studi "hukum" --gov 1 --accept desc
```

## Explanation of the example

- `--dir all`: search all `data/` subfolders (each province folder)
- `--nama_kabupaten "surakarta boyolali"`: match either location token (cleaned, case-insensitive)
- `--program_studi "hukum"`: match program titles containing "hukum"
- `--gov 1`: only include vacancies with government agency information
- `--accept desc`: sort results by estimated acceptance probability (descending)

## Free-text search example

Search across multiple fields in one string (tokens split by whitespace):

```bash
python scripts/run.py --dir data/prov_33 --deep "python backend yogyakarta" --mode or
```

## Output columns and saved fields

- Displayed columns: posisi, perusahaan, kabupaten, kuota, terdaftar, accept%
- `accept%` is computed as: min(1.0, jumlah_kuota / (jumlah_terdaftar + 1))
- Saved JSON (when using `--out`) includes `_applicants_per_slot` and `_acceptance_prob` per item.

## Troubleshooting & tips

- Run scripts from the project root and activate your virtualenv to avoid `ModuleNotFoundError` for `maganghub_client`.
- If a search returns zero results, try removing one structured filter or using fewer tokens, or run a free-text `--deep` query to inspect matches.
- If you want looser structured logic, ask to add a `--struct-mode` flag (OR vs AND across structured filters) or a `--show-matches` debug option.

## Developer notes

- `maganghub_client/search.py` implements `VacancySearch` and `search_deep` (tokenized search and program_studi parsing).
- `maganghub_client/scraper.py` writes an ISO `_scraped_at` timestamp into saved page JSON files.
- The HTTP client uses `requests.Session` with retries for robustness.

## Next steps / optional improvements

- Add fuzzy matching (typo tolerance) using `rapidfuzz`.
- Add CSV/Excel export or an option to include the scrape timestamp in filenames.
- Add unit tests for search filters and scraper behavior.

## License & attribution

This project consumes MagangHub's public API (Kementerian Ketenagakerjaan). Use data responsibly and comply with any API terms.

If you want a shorter quickstart or a maintainer-focused README, tell me which audience and I will produce a trimmed variant.
