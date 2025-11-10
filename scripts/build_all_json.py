"""Build a combined `all.json` from per-page JSON files saved by the scraper.

The script looks for `<n>.json` files in the target directory (numeric prefix),
loads them, extracts `data` lists, concatenates them, and writes `all.json`.

Example:
    python scripts/build_all_json.py --dir data/prov_33
"""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


def discover_page_files(directory: Path) -> List[Path]:
    """Return a sorted list of page JSON files by numeric filename.

    Accepts files like `1.json`, `2.json`, `10.json`. Ignores `all.json`.
    """
    files = []
    for p in directory.glob("*.json"):
        if p.name == "all.json":
            continue
        # attempt to parse numeric basename
        try:
            base = p.stem
            int(base)
            files.append(p)
        except Exception:
            # skip files that aren't named as numbers
            continue
    # sort by numeric stem
    files.sort(key=lambda x: int(x.stem))
    return files


def load_page_data(path: Path) -> Optional[List[Dict[str, Any]]]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            j = json.load(fh)
    except Exception as exc:
        logger.error("Failed to load %s: %s", path, exc)
        return None

    if isinstance(j, dict) and isinstance(j.get("data"), list):
        return j.get("data")
    if isinstance(j, list):
        return j
    logger.warning("File %s does not contain a `data` list; skipping.", path)
    return None


def build_all(directory: Path) -> Dict[str, Any]:
    page_files = discover_page_files(directory)
    logger.info("Found %d page files in %s", len(page_files), directory)

    all_items: List[Dict[str, Any]] = []
    pages_info = []

    for p in page_files:
        items = load_page_data(p)
        if items is None:
            continue
        pages_info.append({"file": p.name, "count": len(items)})
        all_items.extend(items)

    meta = {"pages": pages_info, "total_items": len(all_items)}
    return {"data": all_items, "meta": meta}


def write_all(directory: Path, payload: Dict[str, Any]) -> Path:
    out = directory / "all.json"
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    logger.info("Wrote combined all.json -> %s", out)
    return out


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Build combined all.json from page JSON files")
    parser.add_argument("--dir", required=False, default="data", help="Directory containing page JSON files (default: data)")
    args = parser.parse_args(argv)

    directory = Path(args.dir)
    if not directory.exists() or not directory.is_dir():
        logger.error("Directory does not exist: %s", directory)
        return 2

    payload = build_all(directory)
    write_all(directory, payload)
    logger.info("Combined total items: %s", payload.get("meta", {}).get("total_items"))
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    raise SystemExit(main())
