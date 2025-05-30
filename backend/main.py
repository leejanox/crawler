# FastAPI 서버 (API)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import get_ranking, get_all_posts, get_posts_by_board , get_ranking_date

app = FastAPI()

origins = [
    "http://localhost:5000",
]

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ranking")
def get_ranking_api():
    return get_ranking(limit=10)

@app.get("/ranking/date")
def get_ranking_date_api():
    return get_ranking_date(limit=10)

@app.get("/posts")
def get_all_posts_api():
    return get_all_posts(limit=50)

@app.get("/posts/{board}")
def get_posts_by_board_api(board: str = None):
    if board is None:
        return get_all_posts(limit=50)
    else:
        return get_posts_by_board(board)
