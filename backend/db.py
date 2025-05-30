# SQLite 저장 / 조회 유틸
import sqlite3
from typing import Optional

def get_connection():
    return sqlite3.connect("db.sqlite3")

# sort
def get_ranking_view(limit: int = 10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM crawler ORDER BY view DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    
    return [{
        "board": row[0],
        "i": row[1],
        "title": row[2],
        "writer": row[3],
        "date": row[4],
        "view": row[5]
    } for row in rows]
    
def get_ranking_date(limit: int = 10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM crawler ORDER BY date DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    
    return [{
        "board": row[0],
        "i": row[1],
        "title": row[2],
        "writer": row[3],
        "date": row[4],
        "view": row[5]
    } for row in rows]


# select
def get_all_posts(limit: int = 50):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM crawler ORDER BY date DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    
    return [{
        "board": row[0],
        "i": row[1],
        "title": row[2],
        "writer": row[3],
        "date": row[4],
        "view": row[5]
    } for row in rows]
    
def get_posts_by_board(board: str):
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM crawler WHERE board = ? ORDER BY date DESC LIMIT ?", (board, limit))
    rows = cur.fetchall()
    conn.close()
    
    return [{
        "board": row[0],
        "i": row[1],
        "title": row[2],
        "writer": row[3],
        "date": row[4],
        "view": row[5]
    } for row in rows]
    
# search
def search_posts(keyword: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM crawler WHERE title LIKE ? ORDER BY date DESC", ('%' + keyword + '%',))
    rows = cur.fetchall()
    conn.close()
    
    return [{
        "board": row[0],
        "i": row[1],
        "title": row[2],
        "writer": row[3],
        "date": row[4],
        "view": row[5]
    } for row in rows]



'''
1. Render에 백엔드 배포

2. GitHub에 backend 폴더 푸시

3. https://render.com 접속 → Web Service 생성

4. GitHub에서 해당 레포 선택

5. startCommand:

6. bash
uvicorn main:app --host 0.0.0.0 --port 10000

7. 무료 플랜 선택 후 배포
'''