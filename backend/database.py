import sqlite3
import os
import json
from .config import settings

def get_db_connection():
    os.makedirs(os.path.dirname(settings.DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Users & Roles
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('public', 'researcher', 'editor', 'admin')),
        hashed_password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 2. Expeditions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expeditions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expedition_number TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        year INTEGER NOT NULL,
        region TEXT NOT NULL,
        objectives TEXT NOT NULL,
        description TEXT NOT NULL,
        season TEXT,
        leader TEXT,
        status TEXT DEFAULT 'Completed'
    )
    ''')
    
    # 3. Research Stations
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS research_stations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        region TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        elevation INTEGER,
        year_established INTEGER NOT NULL,
        operational_status TEXT NOT NULL,
        current_weather TEXT,
        description TEXT NOT NULL,
        image_url TEXT
    )
    ''')
    
    # 4. Researchers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS researchers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        institution TEXT NOT NULL,
        designation TEXT,
        specialization TEXT,
        email TEXT,
        expeditions_joined TEXT
    )
    ''')
    
    # 5. Publications
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS publications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        authors TEXT NOT NULL,
        year INTEGER NOT NULL,
        journal TEXT NOT NULL,
        doi TEXT,
        abstract TEXT NOT NULL,
        region TEXT NOT NULL,
        expedition_id INTEGER,
        keywords TEXT,
        citation_count INTEGER DEFAULT 0,
        download_url TEXT,
        FOREIGN KEY (expedition_id) REFERENCES expeditions(id)
    )
    ''')
    
    # 6. Datasets
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        creator TEXT NOT NULL,
        year INTEGER NOT NULL,
        region TEXT NOT NULL,
        variables TEXT NOT NULL,
        format TEXT NOT NULL,
        size_mb REAL NOT NULL,
        expedition_id INTEGER,
        download_url TEXT,
        sample_data_json TEXT,
        FOREIGN KEY (expedition_id) REFERENCES expeditions(id)
    )
    ''')
    
    # 7. Reports
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        expedition_id INTEGER,
        year INTEGER NOT NULL,
        author TEXT NOT NULL,
        summary TEXT NOT NULL,
        full_text TEXT NOT NULL,
        region TEXT NOT NULL,
        file_url TEXT,
        pages_count INTEGER DEFAULT 1,
        FOREIGN KEY (expedition_id) REFERENCES expeditions(id)
    )
    ''')
    
    # 8. Media
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS media (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('photo', 'video', 'drone', 'satellite')),
        url TEXT NOT NULL,
        thumbnail_url TEXT,
        caption TEXT,
        expedition_id INTEGER,
        station_id INTEGER,
        tags TEXT,
        date_captured TEXT,
        transcript TEXT,
        FOREIGN KEY (expedition_id) REFERENCES expeditions(id),
        FOREIGN KEY (station_id) REFERENCES research_stations(id)
    )
    ''')
    
    # 9. Institutional Activities
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS institutional_activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        institution TEXT NOT NULL,
        description TEXT NOT NULL,
        outcomes TEXT,
        media_url TEXT
    )
    ''')
    
    # 10. Embeddings (Vector Search)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource_type TEXT NOT NULL,
        resource_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        chunk_index INTEGER NOT NULL,
        chunk_text TEXT NOT NULL,
        vector_json TEXT NOT NULL,
        metadata_json TEXT
    )
    ''')
    
    # 11. AI Conversations & Messages
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ai_conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT UNIQUE NOT NULL,
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ai_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        sources_json TEXT,
        confidence_score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 12. Outreach Generated Content
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS generated_content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_type TEXT NOT NULL,
        source_id INTEGER NOT NULL,
        source_title TEXT NOT NULL,
        channel TEXT NOT NULL,
        title TEXT NOT NULL,
        content_body TEXT NOT NULL,
        hashtags TEXT,
        target_audience TEXT,
        status TEXT NOT NULL DEFAULT 'Draft' CHECK(status IN ('Draft', 'Pending_Review', 'Approved', 'Rejected', 'Scheduled', 'Published')),
        created_by TEXT DEFAULT 'POLAR AI',
        reviewer_id INTEGER,
        reviewer_name TEXT,
        review_notes TEXT,
        scheduled_at TEXT,
        published_at TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 13. Content Reviews
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS content_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content_id INTEGER NOT NULL,
        reviewer_id INTEGER,
        reviewer_name TEXT,
        action TEXT NOT NULL,
        comments TEXT,
        reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (content_id) REFERENCES generated_content(id)
    )
    ''')
    
    # 14. Quiz Questions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quiz_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        question TEXT NOT NULL,
        options_json TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        explanation TEXT NOT NULL,
        source_document TEXT NOT NULL,
        difficulty TEXT DEFAULT 'Medium'
    )
    ''')
    
    # 15. Audit Logs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        user_role TEXT,
        action TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        entity_id TEXT,
        details TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database tables initialized successfully.")
