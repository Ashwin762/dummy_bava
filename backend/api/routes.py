import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api", tags=["jobs"])

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "mock_jobs.json"
EXPORT_DIR = BASE_DIR / "export"


class SearchRequest(BaseModel):
	query: str = Field(default="", description="Search keyword for role, skill, or company")
	company: str | None = Field(default=None, description="Optional company filter")
	location: str | None = Field(default=None, description="Optional location filter")
	internship_only: bool = Field(default=False, description="Only include internships")
	limit: int = Field(default=20, ge=1, le=100)


def build_response(data: Any, message: str = "ok", success: bool = True) -> dict:
	return {"success": success, "message": message, "data": data}


def load_jobs() -> list[dict[str, Any]]:
	if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
		return []

	with DATA_FILE.open("r", encoding="utf-8") as file:
		loaded = json.load(file)
	return loaded if isinstance(loaded, list) else []


def apply_filters(
	jobs: list[dict[str, Any]],
	query: str = "",
	company: str | None = None,
	location: str | None = None,
	internship_only: bool = False,
) -> list[dict[str, Any]]:
	query_l = query.lower().strip()
	company_l = company.lower().strip() if company else None
	location_l = location.lower().strip() if location else None

	filtered: list[dict[str, Any]] = []
	for job in jobs:
		title = str(job.get("title", "")).lower()
		company_name = str(job.get("company", "")).lower()
		job_location = str(job.get("location", "")).lower()
		skills = " ".join(job.get("skills", [])) if isinstance(job.get("skills"), list) else ""
		haystack = f"{title} {company_name} {job_location} {skills.lower()}"

		if query_l and query_l not in haystack:
			continue
		if company_l and company_l != company_name:
			continue
		if location_l and location_l not in job_location:
			continue
		if internship_only and not bool(job.get("is_internship", False)):
			continue

		filtered.append(job)

	return filtered


@router.get("/jobs")
def get_jobs(
	company: str | None = None,
	location: str | None = None,
	internship_only: bool = False,
	limit: int = Query(default=50, ge=1, le=200),
) -> dict:
	jobs = load_jobs()
	filtered = apply_filters(
		jobs,
		company=company,
		location=location,
		internship_only=internship_only,
	)
	payload = {"count": len(filtered[:limit]), "total": len(filtered), "jobs": filtered[:limit]}
	return build_response(payload, message="jobs fetched")


@router.post("/search")
def search_jobs(request: SearchRequest) -> dict:
	jobs = load_jobs()
	filtered = apply_filters(
		jobs,
		query=request.query,
		company=request.company,
		location=request.location,
		internship_only=request.internship_only,
	)
	payload = {
		"count": len(filtered[: request.limit]),
		"total": len(filtered),
		"jobs": filtered[: request.limit],
	}
	return build_response(payload, message="search complete")


@router.get("/export")
def get_export_info() -> dict:
	jobs = load_jobs()
	available_files = [path.name for path in EXPORT_DIR.glob("*") if path.is_file()] if EXPORT_DIR.exists() else []
	payload = {
		"supported_formats": ["csv", "xlsx"],
		"jobs_available": len(jobs),
		"export_files": available_files,
	}
	return build_response(payload, message="export metadata fetched")
