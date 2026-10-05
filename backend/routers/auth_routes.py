from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from ..database import get_db_connection
from ..auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    role: Optional[str] = "public"

@router.post("/login")
def login(req: LoginRequest):
    conn = get_db_connection()
    user = conn.execute("SELECT id, username, email, full_name, role, hashed_password FROM users WHERE username = ? OR email = ?",
                        (req.username, req.username)).fetchone()
    conn.close()
    
    if not user or not verify_password(req.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username/email or password")
    
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"]
        }
    }

@router.get("/me")
def get_me(current_user: Optional[dict] = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return current_user

@router.post("/register")
def register(req: RegisterRequest):
    conn = get_db_connection()
    existing = conn.execute("SELECT id FROM users WHERE username = ? OR email = ?", (req.username, req.email)).fetchone()
    if existing:
        conn.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already registered")
    
    hashed = hash_password(req.password)
    assigned_role = req.role if req.role in ['public', 'researcher'] else 'public'
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, email, full_name, role, hashed_password)
        VALUES (?, ?, ?, ?, ?)
    ''', (req.username, req.email, req.full_name, assigned_role, hashed))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    token = create_access_token(data={"sub": req.username, "role": assigned_role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": new_id,
            "username": req.username,
            "email": req.email,
            "full_name": req.full_name,
            "role": assigned_role
        }
    }
