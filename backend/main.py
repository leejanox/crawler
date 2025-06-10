from fastapi import FastAPI
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import datetime
import glob

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
    date:str = Query(default=None, description="날짜 형식: YYYYMMDD"),
    order:str = Query(default='desc', enum=['desc', 'asc'], description="정렬 방식: desc(내림차순), asc(오름차순)"),
    page:int = Query(default=1, ge=1, description="페이지 번호"),
    size:int = Query(default=20, ge=1, description="페이지 크기")
):
    if date is None:    
        date = datetime.datetime.today().strftime('%Y%m%d')
    # 파일 경로 지정
    #folder_path = r'D:\goeun\2_1\bigdata\crawler\backend\cafe_crawler_{date}'
    folder_path = os.path.join(r'D:\goeun\2_1\bigdata\crawler\backend', f'cafe_crawler_{date}')


    # 파일 존재 여부 확인
    if not os.path.exists(folder_path):
        return {"error": "파일이 존재하지 않습니다."}
    
    all_csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
    if not all_csv_files:
        return {"error": "csv 파일이 존재하지 않습니다."}
    
    # 모든 csv 파일 읽기
    dfs = []
    for file_path in all_csv_files:
        site = os.path.splitext(os.path.basename(file_path))[0]
        df = pd.read_csv(file_path)
        df['site'] = site
        dfs.append(df)
    
    # 모든 데이터프레임 결합
    merged_df = pd.concat(dfs, ignore_index=True)
    
    # 조회수 기준 정렬
    merged_df['조회수']= pd.to_numeric(merged_df['조회수'],errors='coerce').fillna(0).astype(int)
    if order == 'desc':
        rank_desc = merged_df.sort_values(by='조회수', ascending=False) # 내림차순
    else:
        rank_desc = merged_df.sort_values(by='조회수', ascending=True) # 오름차순

    # 페이지 계산
    total_pages = (len(rank_desc) + size - 1) // size
    if page > total_pages:
        return {"error": "존재하지 않는 페이지입니다."}
    
    # 페이지 데이터 추출
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    page_data = rank_desc.iloc[start_idx:end_idx] 
    grouped = {}

    for _, row in page_data.iterrows():
        board = row['게시판']
        row_dict = row.to_dict()
        grouped.setdefault(board, []).append(row_dict)

    return {
        "date": date,
        "posts": grouped,
        "total_pages": total_pages,
        "current_page": page
    }


# @app.get("/posts/{date}/{menu}")
# def read_posts(date:str = None, menu:str = None,):
#     if date is None:
#         date = datetime.datetime.today().strftime('%Y%m%d')

#     # 파일 경로 지정
#     folder_path = r'D:\goeun\2_1\bigdata\crawler\backend\cafe_crawler_{date}'
#     file_path = os.path.join(folder_path, f'{menu}.csv')

#     # 파일 존재 여부 확인
#     if not os.path.exists(file_path):
#         return {"error": "파일이 존재하지 않습니다."}
        
#     # 파일 읽기
#     df = pd.read_csv(file_path)

#     return df.to_dict(orient='records')

# @app.get("/posts/search")
# def search_posts(date:str = None, menu:str = None, search:str = None):
#     if date is None:
#         date = datetime.datetime.today().strftime('%Y%m%d')

#     # 파일 경로 지정
#     folder_path = r'D:\goeun\2_1\bigdata\crawler\backend\cafe_crawler_{date}'
#     file_path = os.path.join(folder_path, f'{menu}.csv')

#     # 파일 존재 여부 확인
#     if not os.path.exists(file_path):
#         return {"error": "파일이 존재하지 않습니다."}
    
#     # 파일 읽기
#     df = pd.read_csv(file_path)

#     # 검색 조건 적용
#     if search:
#         df = df[df['제목'].str.contains(search)]

#     return df.to_dict(orient='records')



