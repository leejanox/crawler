from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import datetime
import glob
from typing import Optional

app = FastAPI(debug=True)

# CORS 설정
origins = [
    "http://localhost:5000",
    "http://localhost:3000",
    "http://127.0.0.1:5000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/posts/rank")
def rank_all(
    date: str = Query(default=None, description="날짜 형식: YYYYMMDD"),
    order: str = Query(default='desc', enum=['desc', 'asc'], description="정렬 방식"),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1),
    menu: Optional[str] = Query(default=None, description="csv 파일 이름 (예: cook82)"),
    search: Optional[str] = Query(default=None, description="검색어(제목)")
):
    if date is None:
        date = datetime.datetime.today().strftime('%Y%m%d')

    folder_path = os.path.join(r'D:\Kimgoeun\crawler\backend', f'cafe_crawler_{date}')
    if not os.path.exists(folder_path):
        return {"error": "해당 날짜 폴더가 존재하지 않습니다.", "date": date}

    all_csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
    if not all_csv_files:
        return {"error": "CSV 파일이 존재하지 않습니다.", "date": date}

    dfs = []
    for file_path in all_csv_files:
        site = os.path.splitext(os.path.basename(file_path))[0]
        if menu and site != menu:
            continue
        try:
            df = pd.read_csv(file_path)
            df['site'] = site
            dfs.append(df)
        except Exception as e:
            print(f"파일 읽기 실패: {file_path}, 에러: {e}")

    if not dfs:
        return {"error": f"{menu}에 해당하는 유효한 데이터가 없습니다." if menu else "유효한 데이터가 없습니다."}

    merged_df = pd.concat(dfs, ignore_index=True)

    # 조회수 숫자형 변환
    merged_df['조회수'] = pd.to_numeric(merged_df['조회수'], errors='coerce').fillna(0).astype(int)

    # 제목 전처리 (공백 제거)
    merged_df['제목'] = merged_df['제목'].astype(str).str.strip()

    # 검색어 필터링
    if search:
        merged_df = merged_df[merged_df['제목'].str.contains(search, case=False, na=False)]

    # 조회수 높은 순 정렬
    merged_df.sort_values(by='조회수', ascending=False, inplace=True)

    # 제목 기준 중복 제거
    merged_df.drop_duplicates(subset=['제목'], keep='first', inplace=True)
    # 번호 기준 중복 제거
    merged_df = merged_df.drop_duplicates(subset=['번호'], keep='first')

    # 요청된 정렬 순서(order)에 맞춰 다시 정렬
    sorted_df = merged_df.sort_values(by='조회수', ascending=(order == 'asc'))

    # 페이지네이션
    total_pages = (len(sorted_df) + size - 1) // size
    if page > total_pages and total_pages != 0:
        return {"error": "존재하지 않는 페이지입니다.", "page": page, "total_pages": total_pages}

    start_idx = (page - 1) * size
    end_idx = start_idx + size
    page_data = sorted_df.iloc[start_idx:end_idx]

    # 게시판별 그룹화
    grouped = {}
    for _, row in page_data.iterrows():
        board = row['게시판']
        row_dict = row.to_dict()
        grouped.setdefault(board, []).append(row_dict)

    return {
        "date": date,
        "menu": menu,
        "posts": grouped,
        "total_pages": total_pages,
        "current_page": page
    }
