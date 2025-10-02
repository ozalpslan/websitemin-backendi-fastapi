from fastapi import FastAPI
import sqlite3
from sqlite3 import Connection

DB_PATH = "site_data.db"

def get_db() -> Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

app = FastAPI()

# ---------------------------
# API Endpoints
# ---------------------------
@app.get("/about/timeline")
def get_timeline():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT year, title, description AS desc FROM timeline ORDER BY year DESC")
    data = [dict(row) for row in c.fetchall()]
    conn.close()
    return data

@app.get("/about/certificates")
def get_certificates():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT id, title, issuer, year, description, important 
        FROM certificates 
        ORDER BY important DESC, year DESC
    """)
    data = [dict(row) for row in c.fetchall()]
    conn.close()
    return data

@app.get("/projects")
def get_projects():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT title, description, link, important FROM projects ORDER BY important DESC, id ASC")
    projects = [dict(row) for row in c.fetchall()]
    conn.close()
    return projects