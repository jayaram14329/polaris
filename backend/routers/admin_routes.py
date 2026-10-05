from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List
from ..database import get_db_connection

router = APIRouter(prefix="/admin", tags=["Admin & Analytics Dashboard"])

@router.get("/analytics")
def get_admin_analytics():
    conn = get_db_connection()
    
    # 1. Total counts
    expeditions_count = conn.execute("SELECT COUNT(*) FROM expeditions").fetchone()[0]
    publications_count = conn.execute("SELECT COUNT(*) FROM publications").fetchone()[0]
    datasets_count = conn.execute("SELECT COUNT(*) FROM datasets").fetchone()[0]
    media_count = conn.execute("SELECT COUNT(*) FROM media").fetchone()[0]
    pending_reviews_count = conn.execute("SELECT COUNT(*) FROM generated_content WHERE status = 'Pending_Review'").fetchone()[0]
    published_count = conn.execute("SELECT COUNT(*) FROM generated_content WHERE status = 'Published'").fetchone()[0]
    
    # 2. Resources by Year
    pub_years = conn.execute("SELECT year, COUNT(*) as count FROM publications GROUP BY year ORDER BY year ASC").fetchall()
    resources_by_year = [{"year": r["year"], "publications": r["count"]} for r in pub_years]
    
    # 3. Expeditions by Region
    exp_regions = conn.execute("SELECT region, COUNT(*) as count FROM expeditions GROUP BY region").fetchall()
    expeditions_by_region = [{"region": r["region"], "count": r["count"]} for r in exp_regions]
    
    # 4. Outreach status breakdown
    outreach_stats = conn.execute("SELECT status, COUNT(*) as count FROM generated_content GROUP BY status").fetchall()
    outreach_by_status = [{"status": r["status"], "count": r["count"]} for r in outreach_stats]
    
    conn.close()
    
    return {
        "kpi_cards": {
            "expeditions": expeditions_count,
            "publications": publications_count,
            "datasets": datasets_count,
            "media_assets": media_count,
            "pending_reviews": pending_reviews_count,
            "published_outreach": published_count
        },
        "charts": {
            "resources_by_year": resources_by_year,
            "expeditions_by_region": expeditions_by_region,
            "outreach_by_status": outreach_by_status
        }
    }

@router.get("/audit-logs")
def get_audit_logs(limit: int = 50):
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
