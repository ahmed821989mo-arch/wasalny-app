# ملف قاعدة البيانات - وصلني سيدي سالم
import sqlite3
import os

# اسم ملف قاعدة البيانات
DB_PATH = os.path.join(os.path.dirname(__file__), "wasalny.db")

# متغيرات عامة للاتصال بقاعدة البيانات
con = None
cur = None

def init():
    """تهيئة الاتصال بقاعدة البيانات"""
    global con, cur
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    cur = con.cursor()
    print(f"✅ Database initialized at: {DB_PATH}")
