"""
A vulnerable FastAPI application with multiple security issues
"""
import os
import sqlite3
import subprocess
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Depends, Request
from pydantic import BaseModel

# Global variables
API_KEY = "sk-1234567890abcdef1234567890abcdef"
DB_PASSWORD = "admin123"  # Hardcoded credential
SECRET_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFkbWluIiwiaWF0IjoxNTE2MjM5MDIyfQ"

app = FastAPI(title="Vulnerable API Example")


class User(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    role: str = "user"


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None


# Database connection - insecure connection handling
def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
async def root():
    return {"message": "Welcome to the Vulnerable API"}


# SQL Injection vulnerability
@app.get("/users/search")
async def search_users(username: str):
    conn = get_db_connection()
    # Vulnerable SQL query - direct string interpolation
    query = f"SELECT * FROM users WHERE username LIKE '%{username}%'"
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        users = [{"id": row["id"], "username": row["username"], "email": row["email"]} for row in results]
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()


# Command injection vulnerability
@app.get("/system/ping")
async def ping_host(host: str):
    try:
        # Vulnerable command injection
        cmd = f"ping -c 4 {host}"
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return {"output": output.decode()}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Command execution error: {str(e)}")


# Path traversal vulnerability
@app.get("/files/get")
async def get_file(filename: str):
    try:
        # Vulnerable path traversal
        with open(filename, "r") as file:
            content = file.read()
        return {"filename": filename, "content": content}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")


# Insecure direct object reference
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # No authorization check
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {"id": user["id"], "username": user["username"], "email": user["email"], "role": user["role"]}
    raise HTTPException(status_code=404, detail="User not found")


# Broken authentication
@app.post("/login")
async def login(username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Insecure authentication - passwords stored in plaintext
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {"message": "Login successful", "token": "insecure-jwt-token-without-expiration"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")


# Missing rate limiting
@app.post("/users/create")
async def create_user(user: UserCreate):
    # No rate limiting check
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if username exists, but vulnerable to timing attacks
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Store password in plaintext
    cursor.execute(
        "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
        (user.username, user.password, user.email, "user")
    )
    conn.commit()
    
    user_id = cursor.lastrowid
    conn.close()
    
    return {"id": user_id, "username": user.username, "message": "User created successfully"}


# Excessive data exposure
@app.get("/admin/users")
async def get_all_users(api_key: str = Query(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    # Exposes sensitive data including password hashes
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    
    return [dict(user) for user in users]


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
