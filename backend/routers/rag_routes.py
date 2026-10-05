from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json
import uuid
from backend.database import get_db_connection
from ai.rag_engine import PolarRAGEngine

router = APIRouter(prefix="/ai", tags=["POLAR AI & RAG Assistant"])
rag_engine = PolarRAGEngine(get_db_connection)

class AIQueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    user_id: Optional[int] = None

@router.post("/query")
def ask_polar_ai(req: AIQueryRequest):
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    sess_id = req.session_id or str(uuid.uuid4())
    
    # Execute RAG Retrieval and Grounding
    result = rag_engine.answer_query(req.query)
    
    # Store Conversation in DB for audit and session continuity
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO ai_conversations (session_id, user_id) VALUES (?, ?)", (sess_id, req.user_id))
    
    # Store User Message
    cursor.execute("INSERT INTO ai_messages (session_id, role, content) VALUES (?, 'user', ?)", (sess_id, req.query))
    
    # Store AI Answer with Sources
    sources_str = json.dumps(result.get("sources_used", []))
    cursor.execute('''
        INSERT INTO ai_messages (session_id, role, content, sources_json, confidence_score)
        VALUES (?, 'assistant', ?, ?, ?)
    ''', (sess_id, result["answer"], sources_str, result["confidence_score"]))
    
    # Audit log entry
    cursor.execute('''
        INSERT INTO audit_logs (user_name, user_role, action, entity_type, entity_id, details)
        VALUES (?, ?, 'AI_RAG_QUERY', 'AI_ASSISTANT', ?, ?)
    ''', ("Public / Researcher", "User", sess_id, f"Query: {req.query[:60]}... | Grounded: {result['grounded']}"))
    
    conn.commit()
    conn.close()
    
    return {
        "session_id": sess_id,
        "answer": result["answer"],
        "confidence_score": result["confidence_score"],
        "sources_used": result["sources_used"],
        "grounded": result["grounded"]
    }

@router.get("/history/{session_id}")
def get_session_history(session_id: str):
    conn = get_db_connection()
    messages = conn.execute("SELECT id, role, content, sources_json, confidence_score, created_at FROM ai_messages WHERE session_id = ? ORDER BY id ASC", (session_id,)).fetchall()
    conn.close()
    
    history = []
    for m in messages:
        msg = dict(m)
        msg["sources"] = json.loads(msg["sources_json"]) if msg["sources_json"] else []
        history.append(msg)
    return history
