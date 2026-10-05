from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from backend.database import get_db_connection
from ai.outreach_generator import OutreachStudioGenerator
from backend.auth import get_current_user

router = APIRouter(prefix="/outreach", tags=["POLARIS Outreach Studio"])

class GenerateRequest(BaseModel):
    source_type: str # 'report', 'dataset', 'publication', 'activity'
    source_id: int
    channel: str # 'Website Article', 'Instagram', 'LinkedIn', 'Student Explanation', 'X / Twitter'

class ReviewRequest(BaseModel):
    action: str # 'approve', 'reject'
    reviewer_name: Optional[str] = "Dr. S. Sharma (Chief Science Editor)"
    review_notes: Optional[str] = None

class ScheduleRequest(BaseModel):
    scheduled_at: str

@router.post("/generate")
def generate_outreach_content(req: GenerateRequest):
    conn = get_db_connection()
    source_title = "Polar Research Resource"
    source_content = ""
    
    if req.source_type.lower() == "report":
        r = conn.execute("SELECT title, summary, full_text FROM reports WHERE id = ?", (req.source_id,)).fetchone()
        if r:
            source_title = r["title"]
            source_content = r["summary"] or r["full_text"][:300]
    elif req.source_type.lower() == "dataset":
        d = conn.execute("SELECT title, description FROM datasets WHERE id = ?", (req.source_id,)).fetchone()
        if d:
            source_title = d["title"]
            source_content = d["description"]
    elif req.source_type.lower() == "publication":
        p = conn.execute("SELECT title, abstract FROM publications WHERE id = ?", (req.source_id,)).fetchone()
        if p:
            source_title = p["title"]
            source_content = p["abstract"]
    
    draft = OutreachStudioGenerator.generate_draft(
        source_type=req.source_type,
        source_title=source_title,
        source_content=source_content,
        channel=req.channel
    )
    
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO generated_content (source_type, source_id, source_title, channel, title, content_body, hashtags, target_audience, status, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Draft', ?)
    ''', (req.source_type, req.source_id, source_title, req.channel, draft["title"], draft["content_body"], draft["hashtags"], draft["target_audience"], draft["created_by"]))
    
    new_id = cursor.lastrowid
    
    cursor.execute('''
        INSERT INTO audit_logs (user_name, user_role, action, entity_type, entity_id, details)
        VALUES (?, 'researcher', 'OUTREACH_DRAFT_GENERATED', 'OUTREACH_STUDIO', ?, ?)
    ''', ("Researcher / POLAR AI", str(new_id), f"Generated draft for {req.channel}: {draft['title']}"))
    
    conn.commit()
    conn.close()
    
    draft["id"] = new_id
    return draft

@router.get("/queue")
def list_outreach_queue(status: Optional[str] = None):
    conn = get_db_connection()
    query = "SELECT * FROM generated_content WHERE 1=1"
    params = []
    if status and status.lower() != "all":
        query += " AND LOWER(status) = LOWER(?)"
        params.append(status)
    query += " ORDER BY id DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.post("/submit-for-review/{id}")
def submit_for_review(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE generated_content SET status = 'Pending_Review' WHERE id = ?", (id,))
    cursor.execute('''
        INSERT INTO audit_logs (user_name, user_role, action, entity_type, entity_id, details)
        VALUES (?, 'researcher', 'SUBMITTED_FOR_REVIEW', 'OUTREACH_STUDIO', ?, 'Draft submitted for Editor Verification')
    ''', ("Researcher", str(id)))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Draft submitted to editorial queue for verification"}

@router.post("/review/{id}")
def review_outreach_content(id: int, req: ReviewRequest):
    new_status = "Approved" if req.action.lower() == "approve" else "Rejected"
    reviewer = req.reviewer_name or "Science Editor"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE generated_content
        SET status = ?, reviewer_name = ?, review_notes = ?
        WHERE id = ?
    ''', (new_status, reviewer, req.review_notes, id))
    
    cursor.execute('''
        INSERT INTO content_reviews (content_id, reviewer_name, action, comments)
        VALUES (?, ?, ?, ?)
    ''', (id, reviewer, new_status, req.review_notes or "Editor decision executed"))
    
    cursor.execute('''
        INSERT INTO audit_logs (user_name, user_role, action, entity_type, entity_id, details)
        VALUES (?, 'editor', 'HUMAN_EDITORIAL_DECISION', 'OUTREACH_STUDIO', ?, ?)
    ''', (reviewer, str(id), f"Content {new_status} by Editor: {req.review_notes or 'No notes'}"))
    
    conn.commit()
    conn.close()
    
    return {"status": "success", "new_status": new_status, "reviewer": reviewer}

@router.post("/schedule/{id}")
def schedule_outreach_content(id: int, req: ScheduleRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE generated_content SET status = 'Scheduled', scheduled_at = ? WHERE id = ?", (req.scheduled_at, id))
    cursor.execute('''
        INSERT INTO audit_logs (user_name, user_role, action, entity_type, entity_id, details)
        VALUES (?, 'editor', 'CONTENT_SCHEDULED', 'OUTREACH_STUDIO', ?, ?)
    ''', ("Editor", str(id), f"Scheduled for {req.scheduled_at}"))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Content scheduled for {req.scheduled_at}"}

@router.post("/publish/{id}")
def publish_outreach_content(id: int):
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE generated_content SET status = 'Published', published_at = ? WHERE id = ?", (now_str, id))
    cursor.execute('''
        INSERT INTO audit_logs (user_name, user_role, action, entity_type, entity_id, details)
        VALUES (?, 'editor', 'CONTENT_PUBLISHED', 'OUTREACH_STUDIO', ?, 'Content published to MoES/NCPOR channels')
    ''', ("Editor", str(id)))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Content successfully published"}
