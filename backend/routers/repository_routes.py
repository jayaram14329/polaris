from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional, List
import json
from ..database import get_db_connection
from ..auth import get_current_user

router = APIRouter(prefix="/repository", tags=["Polar Knowledge Repository"])

@router.get("/summary")
def get_repository_summary():
    conn = get_db_connection()
    expeditions_count = conn.execute("SELECT COUNT(*) FROM expeditions").fetchone()[0]
    publications_count = conn.execute("SELECT COUNT(*) FROM publications").fetchone()[0]
    datasets_count = conn.execute("SELECT COUNT(*) FROM datasets").fetchone()[0]
    reports_count = conn.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    media_count = conn.execute("SELECT COUNT(*) FROM media").fetchone()[0]
    stations_count = conn.execute("SELECT COUNT(*) FROM research_stations").fetchone()[0]
    activities_count = conn.execute("SELECT COUNT(*) FROM institutional_activities").fetchone()[0]
    conn.close()
    
    return {
        "expeditions": expeditions_count,
        "publications": publications_count,
        "datasets": datasets_count,
        "reports": reports_count,
        "media": media_count,
        "stations": stations_count,
        "activities": activities_count,
        "total_assets": expeditions_count + publications_count + datasets_count + reports_count + media_count + activities_count
    }

@router.get("/expeditions")
def list_expeditions(region: Optional[str] = None, year: Optional[int] = None):
    conn = get_db_connection()
    query = "SELECT * FROM expeditions WHERE 1=1"
    params = []
    if region and region.lower() != "all":
        query += " AND LOWER(region) = LOWER(?)"
        params.append(region)
    if year:
        query += " AND year = ?"
        params.append(year)
    query += " ORDER BY year DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.get("/expeditions/{id}")
def get_expedition_detail(id: int):
    conn = get_db_connection()
    expedition = conn.execute("SELECT * FROM expeditions WHERE id = ?", (id,)).fetchone()
    if not expedition:
        conn.close()
        raise HTTPException(status_code=404, detail="Expedition not found")
    
    reports = conn.execute("SELECT id, title, year, author, summary, pages_count, file_url FROM reports WHERE expedition_id = ?", (id,)).fetchall()
    datasets = conn.execute("SELECT id, title, format, size_mb, variables, download_url FROM datasets WHERE expedition_id = ?", (id,)).fetchall()
    publications = conn.execute("SELECT id, title, authors, journal, year, doi, download_url FROM publications WHERE expedition_id = ?", (id,)).fetchall()
    media = conn.execute("SELECT id, title, type, url, thumbnail_url, caption FROM media WHERE expedition_id = ?", (id,)).fetchall()
    conn.close()
    
    res = dict(expedition)
    res["reports"] = [dict(r) for r in reports]
    res["datasets"] = [dict(d) for d in datasets]
    res["publications"] = [dict(p) for p in publications]
    res["media"] = [dict(m) for m in media]
    return res

@router.get("/publications")
def list_publications(region: Optional[str] = None, year: Optional[int] = None, search: Optional[str] = None):
    conn = get_db_connection()
    query = "SELECT * FROM publications WHERE 1=1"
    params = []
    if region and region.lower() != "all":
        query += " AND LOWER(region) = LOWER(?)"
        params.append(region)
    if year:
        query += " AND year = ?"
        params.append(year)
    if search:
        query += " AND (title LIKE ? OR abstract LIKE ? OR keywords LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    query += " ORDER BY year DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.get("/datasets")
def list_datasets(region: Optional[str] = None, year: Optional[int] = None):
    conn = get_db_connection()
    query = "SELECT id, title, description, creator, year, region, variables, format, size_mb, expedition_id, download_url FROM datasets WHERE 1=1"
    params = []
    if region and region.lower() != "all":
        query += " AND LOWER(region) = LOWER(?)"
        params.append(region)
    if year:
        query += " AND year = ?"
        params.append(year)
    query += " ORDER BY year DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.get("/datasets/{id}/preview")
def get_dataset_preview(id: int):
    conn = get_db_connection()
    ds = conn.execute("SELECT * FROM datasets WHERE id = ?", (id,)).fetchone()
    conn.close()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    sample_data = json.loads(ds["sample_data_json"]) if ds["sample_data_json"] else []
    res = dict(ds)
    res["sample_data"] = sample_data
    return res

@router.get("/reports")
def list_reports(region: Optional[str] = None, year: Optional[int] = None):
    conn = get_db_connection()
    query = "SELECT id, title, expedition_id, year, author, summary, region, file_url, pages_count FROM reports WHERE 1=1"
    params = []
    if region and region.lower() != "all":
        query += " AND LOWER(region) = LOWER(?)"
        params.append(region)
    if year:
        query += " AND year = ?"
        params.append(year)
    query += " ORDER BY year DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.get("/reports/{id}")
def get_report_detail(id: int):
    conn = get_db_connection()
    r = conn.execute("SELECT * FROM reports WHERE id = ?", (id,)).fetchone()
    conn.close()
    if not r:
        raise HTTPException(status_code=404, detail="Report not found")
    return dict(r)

@router.get("/media")
def list_media(type: Optional[str] = None, tag: Optional[str] = None):
    conn = get_db_connection()
    query = "SELECT * FROM media WHERE 1=1"
    params = []
    if type and type.lower() != "all":
        query += " AND type = ?"
        params.append(type.lower())
    if tag:
        query += " AND tags LIKE ?"
        params.append(f"%{tag}%")
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.get("/activities")
def list_activities():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM institutional_activities ORDER BY date DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
