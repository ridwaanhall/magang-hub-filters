"""CLI wrapper to scrape MagangHub vacancies and save pages as JSON files.

Each page is saved as `<page>.json` inside the target directory. The scraper
stops when a page returns `data: []`.

Example:
    python scripts/scrape_and_save.py --save-dir data/prov_33 --kode_provinsi 33
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional

# When running this script directly from the repository root (for example:
# `python scripts/scrape_and_save.py`), ensure the project root is on
# sys.path so `maganghub_client` can be imported without installing the
# package into the environment.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from maganghub_client.scraper import VacanciesScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Scrape MagangHub vacancies and save pages as JSON files")
    p.add_argument("--save-dir", required=True, help="Directory to save page JSON files")
    p.add_argument("--start-page", type=int, default=1, help="Start page (default: 1)")
    p.add_argument("--limit", type=int, default=100, help="Items per page (default: 100)")
    p.add_argument("--kode_provinsi", type=int, required=True, help="Province code to filter")
    p.add_argument("--max-pages", type=int, default=None, help="Maximum pages to fetch (optional)")
    p.add_argument("--delay", type=float, default=0.0, help="Delay (seconds) between requests")

    args = p.parse_args(argv)

    save_dir = Path(args.save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    scraper = VacanciesScraper()
    try:
        pages_saved = scraper.scrape_all(
            save_dir=str(save_dir),
            start_page=args.start_page,
            limit=args.limit,
            kode_provinsi=args.kode_provinsi,
            max_pages=args.max_pages,
            delay=args.delay,
        )
    except Exception as exc:
        logger.exception("Scrape failed: %s", exc)
        return 2

    logger.info("Completed scraping. Pages saved: %s", pages_saved)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
