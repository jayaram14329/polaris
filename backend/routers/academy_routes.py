from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import json
from backend.database import get_db_connection
from ai.quiz_generator import PolarQuizGenerator

router = APIRouter(prefix="/academy", tags=["Polar Academy & Student Learning"])

class QuizEvaluateRequest(BaseModel):
    answers: Dict[int, str]

@router.get("/milestones")
def get_expedition_milestones():
    milestones = [
        {
            "year": 1981,
            "title": "First Indian Antarctic Expedition",
            "leader": "Dr. S. Z. Qasim",
            "region": "Antarctica",
            "description": "Historic landing of Indian scientists in Antarctica aboard MV Polar Circle. Initiated continuous Indian high-latitude research.",
            "impact": "India recognized as a key player in the Antarctic Treaty system.",
            "badge": "Historic Milestone"
        },
        {
            "year": 1983,
            "title": "Establishment of Dakshin Gangotri",
            "leader": "3rd Indian Antarctic Expedition",
            "region": "Antarctica",
            "description": "India's first permanent research base built in ice-covered Queen Maud Land in record time of one polar season.",
            "impact": "Inaugurated year-round wintering observations.",
            "badge": "First Permanent Base"
        },
        {
            "year": 1989,
            "title": "Commissioning of Maitri Station",
            "leader": "8th Indian Antarctic Expedition",
            "region": "Antarctica (Schirmacher Oasis)",
            "description": "Second permanent base built on the rocky, ice-free Schirmacher Oasis adjacent to Lake Priyadarshini.",
            "impact": "Active continuous year-round laboratory running for over 35 years.",
            "badge": "Active Wintering Station"
        },
        {
            "year": 2008,
            "title": "India Enters the Arctic: Himadri Station",
            "leader": "NCPOR Arctic Scientific Team",
            "region": "Arctic (Ny-Ålesund, Svalbard)",
            "description": "Inauguration of Himadri, India's permanent Arctic research observatory in the international science village of Svalbard.",
            "impact": "Expanded Indian polar mandate to the Boreal Arctic realm.",
            "badge": "Arctic Expansion"
        },
        {
            "year": 2012,
            "title": "State-of-the-Art Bharati Station",
            "leader": "31st Indian Antarctic Expedition",
            "region": "Antarctica (Larsemann Hills)",
            "description": "Commissioning of Bharati, an aerodynamic architectural marvel elevated on stilts with minimal environmental footprint.",
            "impact": "Expanded Indian research into East Antarctica, Prydz Bay, and deep oceanography.",
            "badge": "Modern Polar Laboratory"
        },
        {
            "year": 2014,
            "title": "Deployment of IndARC Underwater Observatory",
            "leader": "NCPOR Ocean Sciences Division",
            "region": "Arctic (Kongsfjorden Fjord)",
            "description": "India's first multi-sensor underwater moored observatory anchored at 192m depth in the freezing Arctic fjord.",
            "impact": "Continuous round-the-year marine water column telemetry.",
            "badge": "Deep Ocean Mooring"
        },
        {
            "year": 2024,
            "title": "44th Indian Antarctic Expedition & Maitri II Planning",
            "leader": "Dr. S. K. Roy / NCPOR",
            "region": "Antarctica",
            "description": "Prydz Bay acoustic sea-ice monitoring, deep firn coring, and foundational site surveys for the next-generation Maitri II base.",
            "impact": "Next-decade sustainable science roadmap under the Indian Antarctic Act 2022.",
            "badge": "Active Mission (2024-26)"
        }
    ]
    return milestones

@router.get("/quizzes")
def get_quiz_questions(topic: Optional[str] = None):
    conn = get_db_connection()
    query = "SELECT * FROM quiz_questions"
    params = []
    if topic and topic.lower() != "all":
        query += " WHERE LOWER(topic) LIKE ?"
        params.append(f"%{topic.lower()}%")
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    quizzes = []
    for r in rows:
        q = dict(r)
        q["options"] = json.loads(q["options_json"]) if q["options_json"] else []
        quizzes.append(q)
    return quizzes

@router.post("/quizzes/evaluate")
def evaluate_quiz(req: QuizEvaluateRequest):
    conn = get_db_connection()
    rows = conn.execute("SELECT id, question, correct_answer, explanation, source_document FROM quiz_questions").fetchall()
    conn.close()
    
    q_map = {r["id"]: dict(r) for r in rows}
    
    score = 0
    total = len(req.answers)
    breakdown = []
    
    for q_id, user_ans in req.answers.items():
        if q_id in q_map:
            q_info = q_map[q_id]
            is_correct = (user_ans.strip().lower() == q_info["correct_answer"].strip().lower())
            if is_correct:
                score += 1
            breakdown.append({
                "question_id": q_id,
                "question": q_info["question"],
                "user_answer": user_ans,
                "correct_answer": q_info["correct_answer"],
                "is_correct": is_correct,
                "explanation": q_info["explanation"],
                "source_document": q_info["source_document"]
            })
            
    pct = round((score / total) * 100, 1) if total > 0 else 0
    return {
        "score": score,
        "total": total,
        "percentage": pct,
        "badge_awarded": "Polar Cadet" if pct < 60 else ("Polar Researcher" if pct < 85 else "Master Polar Explorer"),
        "breakdown": breakdown
    }
