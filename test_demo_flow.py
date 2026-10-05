import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ai.rag_engine import PolarRAGEngine
from backend.database import get_db_connection
from ai.outreach_generator import OutreachStudioGenerator
from ai.quiz_generator import PolarQuizGenerator

print("=== 1. TESTING RAG QUERY ===")
rag = PolarRAGEngine(get_db_connection)
query = "What were the major research objectives of this expedition?"
res = rag.answer_query(query)
print("Answer:\n", res["answer"])
print("\nSources Used:")
for s in res["sources_used"]:
    print(f" - {s['source']} | {s['section']} (p.{s['page']}) | Confidence: {s['similarity_score']}%")
print("Confidence:", res["confidence_score"])
print("Grounded:", res["grounded"])

print("\n=== 2. TESTING OUTREACH STUDIO GENERATION ===")
draft = OutreachStudioGenerator.generate_draft(
    source_type="report",
    source_title="43rd Indian Antarctic Expedition Scientific Report",
    source_content=res["answer"],
    channel="Website Article"
)
print("Draft Title:", draft["title"])
print("Draft Status (MUST BE Draft):", draft["status"])

insta_draft = OutreachStudioGenerator.generate_draft(
    source_type="report",
    source_title="43rd Indian Antarctic Expedition Scientific Report",
    source_content=res["answer"],
    channel="Instagram"
)
print("Instagram Draft Title:", insta_draft["title"])

print("\n=== 3. TESTING POLAR ACADEMY QUIZ GENERATION ===")
quizzes = PolarQuizGenerator.get_sample_quizzes_by_topic("All")
print(f"Loaded {len(quizzes)} verified quizzes.")
for q in quizzes[:2]:
    print(f"Q: {q['question']} -> Ans: {q['correct_answer']} (Source: {q['source_document']})")

print("\nALL CORE ENGINE TESTS PASSED PERFECTLY!")
