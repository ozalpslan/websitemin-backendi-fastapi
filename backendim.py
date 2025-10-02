from fastapi import FastAPI
import sqlite3
from sqlite3 import Connection
from contextlib import asynccontextmanager

DB_PATH = "site_data.db"

# ---------------------------
# Helper fonksiyonlar
# ---------------------------
def get_db() -> Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_timeline():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS timeline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year TEXT,
            title TEXT,
            description TEXT
        )
    """)
    conn.commit()
    c.execute("SELECT COUNT(*) as count FROM timeline")
    if c.fetchone()["count"] == 0:
        c.executemany(
            "INSERT INTO timeline (year, title, description) VALUES (?, ?, ?)",
            [
                ("2025", "Kişisel React Web Sitesi", "React, FastAPI, AWS EC2 ve Docker kullanarak CV ve portfolyo geliştirdim."),
                ("2024", "Arabam.com Fiyat Tahmini", "Scraping + ML pipeline"),
                ("2023", "İTÜ Deep Learning Datathon", "CNN modelleriyle şehir yapısı tahmini")
            ]
        )
        conn.commit()
    conn.close()

def init_certificates():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            year TEXT,
            issuer TEXT,
            description TEXT,
            important INTEGER
        )
    """)
    conn.commit()
    c.execute("SELECT COUNT(*) as count FROM certificates")
    if c.fetchone()["count"] == 0:
        c.executemany(
            "INSERT INTO certificates (title, year, issuer, description, important) VALUES (?, ?, ?, ?, ?)",
            [
                ("AWS Certified Cloud Practitioner", "2025", "Amazon Web Services",
                 "EC2, S3, RDS, Lambda, VPC, IAM gibi temel AWS servislerinde yetkinlik. Cloud uygulamalarını tasarlama, güvenlik ve maliyet optimizasyonu deneyimi.", 1),
                ("AI Engineer for Data Scientists Associate", "2025", "DataCamp",
                 "Python ile veri hazırlama, modelleme ve görselleştirme. MLOps ve LLMOps kavramlarına giriş, ETL/ELT pipeline hazırlama.", 1),
                ("Full-Stack Web Development Bootcamp", "2025", "Dr. Angela Yu (Udemy)",
                 "HTML, CSS, Bootstrap, JavaScript, React, Node.js, Express.js, PostgreSQL ile web uygulamaları geliştirme. Git & GitHub ile proje yönetimi.", 1),
                ("Advanced Excel Certificate", "2025", "BilgeAdam",
                 "Excel formülleri, pivot tablolar, dashboardlar ve makrolar ile ileri seviye analizler.", 0),
                ("Python Bootcamp", "2024", "Akbank",
                 "OOP, sınıflar, dosya işlemleriyle özel Python kütüphane sistemi geliştirme deneyimi.", 0),
                ("Geleceği Yazanlar 401", "2024", "Turkcell",
                 "Python’da veri yapıları, algoritmalar, nesne yönelimli programlama ve dosya işlemleri temelleri.", 0)
            ]
        )
        conn.commit()
    conn.close()

def init_projects():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            link TEXT,
            important INTEGER
        )
    """)
    conn.commit()
    c.execute("SELECT COUNT(*) as count FROM projects")
    if c.fetchone()["count"] == 0:
        c.executemany(
            "INSERT INTO projects (title, description, link, important) VALUES (?, ?, ?, ?)",
            [
                ("Kişisel React Web Sitesi",
                 "React, FastAPI, AWS EC2 ve Docker kullanarak CV ve portfolyo için geliştirdiğim web sitesi.",
                 "https://github.com/ozalpslan/websitesi", 1),
                ("Streamlit Çalışmaları",
                 "Streamlit ile yaptığım küçük ML/AI projeleri ve denemeler.",
                 "https://github.com/ozalpslan/streamlit", 0),
                ("Arabam.com Fiyat Tahmini",
                 "Araç verilerini scrape edip temizledim, ML modelleriyle fiyat tahmini pipeline kurdum.",
                 "https://github.com/ozalpslan/Araba-Deger-Tahmini-Projesi", 1),
                ("Ses Kaydı & Transkripsiyon Sistemi",
                 "Türkçe sesleri yazıya döken ve BART modeli ile özetleyen Python tabanlı LLM projesi.",
                 "https://github.com/ozalpslan/Audio-Transcriber-and-Summerizer", 1),
                ("Katıldığım Yarışmalar",
                 "İTÜ Deep Learning Datathon (CNN), YTÜ ML Datathon (XGBoost), OBSS AI Intern (Image Captioning).",
                 "https://github.com/ozalpslan/Katildigim-Yarismalar", 1),
                ("Leetcode Çalışmaları",
                 "Algoritma & problem çözme alıştırmaları. JavaScript/Python çözümleri.",
                 "https://github.com/ozalpslan/Leetcode", 0),
                ("Kredi Riski Analizi",
                 "Derin öğrenme yöntemleriyle kredi riski tahmini modeli geliştirdim.",
                 "https://github.com/ozalpslan/Derin-ogrenme-ile-kredi-riski-analizi", 0),
                ("Ev Fiyat Tahmini",
                 "Neural Networks ile ev fiyat tahmin modeli (HousePricingPredict).",
                 "https://github.com/ozalpslan/HousePricingPredict", 0),
                ("Akbank Python Bootcamp Projesi",
                 "OOP tabanlı Python kütüphane sistemi geliştirdiğim proje.",
                 "https://github.com/ozalpslan/Akbank-python-bootcamp-projesi", 0)
            ]
        )
        conn.commit()
    conn.close()

# ---------------------------
# Lifespan event
# ---------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_timeline()
    init_certificates()
    init_projects()
    yield
    # Shutdown (gerekirse)

app = FastAPI(lifespan=lifespan)

# ---------------------------
# API Endpoints
# ---------------------------
@app.get("/api/about/timeline")
def get_timeline():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT year, title, description AS desc FROM timeline ORDER BY year DESC")
    data = [dict(row) for row in c.fetchall()]
    conn.close()
    return data

@app.get("/api/about/certificates")
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

@app.get("/api/projects")
def get_projects():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT title, description, link, important FROM projects ORDER BY important DESC, id ASC")
    projects = [dict(row) for row in c.fetchall()]
    conn.close()
    return projects