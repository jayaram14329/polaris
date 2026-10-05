from fastapi import APIRouter, Query
from typing import Optional, List
import json
from backend.database import get_db_connection
from ai.rag_engine import embedder

router = APIRouter(prefix="/search", tags=["Global & Multimodal Search"])

@router.get("/global")
def global_search(
    q: Optional[str] = Query(None, description="Search keyword or semantic query"),
    region: Optional[str] = None,
    year: Optional[int] = None,
    resource_type: Optional[str] = None
):
    conn = get_db_connection()
    results = {
        "reports": [],
        "datasets": [],
        "publications": [],
        "stations": [],
        "media": []
    }
    
    query_str = q.lower().strip() if q else ""
    
    # 1. Reports Search
    if not resource_type or resource_type.lower() in ["all", "reports", "report"]:
        rep_sql = "SELECT id, title, year, author, summary, region, file_url FROM reports WHERE 1=1"
        rep_params = []
        if query_str:
            rep_sql += " AND (LOWER(title) LIKE ? OR LOWER(summary) LIKE ? OR LOWER(full_text) LIKE ?)"
            rep_params.extend([f"%{query_str}%", f"%{query_str}%", f"%{query_str}%"])
        if region and region.lower() != "all":
            rep_sql += " AND LOWER(region) = LOWER(?)"
            rep_params.append(region)
        if year:
            rep_sql += " AND year = ?"
            rep_params.append(year)
        rep_rows = conn.execute(rep_sql, rep_params).fetchall()
        results["reports"] = [dict(r) for r in rep_rows]

    # 2. Datasets Search
    if not resource_type or resource_type.lower() in ["all", "datasets", "dataset"]:
        ds_sql = "SELECT id, title, description, creator, year, region, variables, format, size_mb, download_url FROM datasets WHERE 1=1"
        ds_params = []
        if query_str:
            ds_sql += " AND (LOWER(title) LIKE ? OR LOWER(description) LIKE ? OR LOWER(variables) LIKE ?)"
            ds_params.extend([f"%{query_str}%", f"%{query_str}%", f"%{query_str}%"])
        if region and region.lower() != "all":
            ds_sql += " AND LOWER(region) = LOWER(?)"
            ds_params.append(region)
        if year:
            ds_sql += " AND year = ?"
            ds_params.append(year)
        ds_rows = conn.execute(ds_sql, ds_params).fetchall()
        results["datasets"] = [dict(d) for d in ds_rows]

    # 3. Publications Search
    if not resource_type or resource_type.lower() in ["all", "publications", "papers"]:
        pub_sql = "SELECT id, title, authors, year, journal, doi, abstract, region, keywords, download_url FROM publications WHERE 1=1"
        pub_params = []
        if query_str:
            pub_sql += " AND (LOWER(title) LIKE ? OR LOWER(abstract) LIKE ? OR LOWER(keywords) LIKE ?)"
            pub_params.extend([f"%{query_str}%", f"%{query_str}%", f"%{query_str}%"])
        if region and region.lower() != "all":
            pub_sql += " AND LOWER(region) = LOWER(?)"
            pub_params.append(region)
        if year:
            pub_sql += " AND year = ?"
            pub_params.append(year)
        pub_rows = conn.execute(pub_sql, pub_params).fetchall()
        results["publications"] = [dict(p) for p in pub_rows]

    # 4. Stations Search
    if not resource_type or resource_type.lower() in ["all", "stations"]:
        st_sql = "SELECT id, code, name, region, latitude, longitude, operational_status, description FROM research_stations WHERE 1=1"
        st_params = []
        if query_str:
            st_sql += " AND (LOWER(name) LIKE ? OR LOWER(code) LIKE ? OR LOWER(description) LIKE ?)"
            st_params.extend([f"%{query_str}%", f"%{query_str}%", f"%{query_str}%"])
        if region and region.lower() != "all":
            st_sql += " AND LOWER(region) LIKE ?"
            st_params.append(f"%{region.lower()}%")
        st_rows = conn.execute(st_sql, st_params).fetchall()
        results["stations"] = [dict(s) for s in st_rows]

    # 5. Media Search
    if not resource_type or resource_type.lower() in ["all", "media", "photos", "videos"]:
        med_sql = "SELECT id, title, type, url, thumbnail_url, caption, tags FROM media WHERE 1=1"
        med_params = []
        if query_str:
            med_sql += " AND (LOWER(title) LIKE ? OR LOWER(caption) LIKE ? OR LOWER(tags) LIKE ? OR LOWER(COALESCE(transcript, '')) LIKE ?)"
            med_params.extend([f"%{query_str}%", f"%{query_str}%", f"%{query_str}%", f"%{query_str}%"])
        med_rows = conn.execute(med_sql, med_params).fetchall()
        results["media"] = [dict(m) for m in med_rows]

    conn.close()
    
    total_found = sum(len(v) for v in results.values())
    return {
        "query": q,
        "total_results": total_found,
        "results": results
    }

@router.get("/media")
def search_media_multimodal(q: str = Query(..., description="Natural language media query")):
    conn = get_db_connection()
    q_words = [w.lower() for w in q.split() if len(w) > 2]
    
    rows = conn.execute("SELECT id, title, type, url, thumbnail_url, caption, tags, transcript FROM media").fetchall()
    conn.close()
    
    scored = []
    for r in rows:
        text_corpus = f"{r['title']} {r['caption']} {r['tags']} {r['transcript'] or ''}".lower()
        score = 0.0
        for w in q_words:
            if w in text_corpus:
                score += 1.0
        
        if "penguin" in q.lower() and "penguin" in text_corpus:
            score += 2.0
        if "station" in q.lower() and "station" in text_corpus:
            score += 1.5
        if "ice core" in q.lower() and "ice core" in text_corpus:
            score += 2.0
        if "video" in q.lower() and r["type"] == "video":
            score += 1.5
            
        if score > 0 or not q_words:
            m_dict = dict(r)
            m_dict["relevance_score"] = round(score, 2)
            scored.append(m_dict)
            
    scored.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
    return scored
