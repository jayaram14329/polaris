from fastapi import APIRouter, HTTPException
import json
from ..database import get_db_connection

router = APIRouter(prefix="/stations", tags=["Research Stations & Polar Map"])

@router.get("")
def list_stations():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM research_stations").fetchall()
    conn.close()
    
    result = []
    for r in rows:
        st = dict(r)
        st["weather"] = json.loads(st["current_weather"]) if st["current_weather"] else {}
        result.append(st)
    return result

@router.get("/{code}")
def get_station_detail(code: str):
    conn = get_db_connection()
    st = conn.execute("SELECT * FROM research_stations WHERE UPPER(code) = UPPER(?)", (code,)).fetchone()
    if not st:
        conn.close()
        raise HTTPException(status_code=404, detail="Station not found")
    
    st_id = st["id"]
    # Get related media
    media = conn.execute("SELECT id, title, type, url, thumbnail_url, caption FROM media WHERE station_id = ?", (st_id,)).fetchall()
    
    # Get related expeditions based on region
    region_kw = "Antarctica" if "antarctica" in st["region"].lower() else "Arctic"
    expeditions = conn.execute("SELECT id, expedition_number, name, year, region, status FROM expeditions WHERE region = ? ORDER BY year DESC", (region_kw,)).fetchall()
    
    # Get related datasets
    datasets = conn.execute("SELECT id, title, format, size_mb, download_url FROM datasets WHERE region = ?", (region_kw,)).fetchall()
    
    conn.close()
    
    res = dict(st)
    res["weather"] = json.loads(res["current_weather"]) if res["current_weather"] else {}
    res["media"] = [dict(m) for m in media]
    res["related_expeditions"] = [dict(e) for e in expeditions]
    res["related_datasets"] = [dict(d) for d in datasets]
    return res
