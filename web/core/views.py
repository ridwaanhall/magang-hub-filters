from pathlib import Path
from typing import List

from django.shortcuts import render

from maganghub_client.search import VacancySearch


"""Path to the repository `data/` directory. Use parents[2] because this
module lives at <repo>/web/core/views.py and the repo root is two levels up.
"""
DATA_ROOT = Path(__file__).resolve().parents[2] / "data"


def filter_view(request):
	"""Render a simple filter page that reuses VacancySearch.

	Query parameters:
	- q: search query (tokens separated by whitespace)
	- prov: province folder name (e.g. prov_33 or prov_34). default: prov_33 if exists
	- mode: 'and' or 'or' (default 'and')
	- limit: integer limit for results (optional)
	"""
	q = request.GET.get("q", "").strip()
	prov = request.GET.get("prov") or "prov_33"
	mode = request.GET.get("mode") or "and"
	limit = request.GET.get("limit")
	try:
		limit_val = int(limit) if limit else None
	except Exception:
		limit_val = None

	# determine data dir
	data_dir = DATA_ROOT / prov
	results: List[dict] = []
	error = None
	if q:
		try:
			vs = VacancySearch(data_dir)
			results = vs.search_deep(q, limit=limit_val, mode=mode)
		except Exception as exc:
			error = str(exc)

	# list available provinces under data
	prov_choices = []
	try:
		for p in (DATA_ROOT).iterdir():
			if p.is_dir() and p.name.startswith("prov_"):
				prov_choices.append(p.name)
	except Exception:
		prov_choices = []

	context = {
		"query": q,
		"prov": prov,
		"mode": mode,
		"limit": limit or "",
		"results": results,
		"error": error,
		"prov_choices": sorted(prov_choices),
	}
	return render(request, "core/filter.html", context)
