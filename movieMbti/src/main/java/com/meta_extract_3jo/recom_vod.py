from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib import parse
import pandas as pd
import numpy as np
import faiss
import json

from sentence_transformers import SentenceTransformer


app = Flask(__name__)
CORS(app)

# 사전 훈련된 모델 불러옴
model = SentenceTransformer('jhgan/ko-sroberta-multitask')
model.eval()

# 영화 키워드 데이터 불러오기
movie_keywords_df = pd.read_csv('./moviedata_keywords_df.csv')
movie_keywords_df = movie_keywords_df[["movie_seq", "movie_keywords"]]

# 영화줄거리 임베딩 데이터 불러오기
movie_content_emb_df = pd.read_csv('./moviedata_content_emb.csv')

@app.route("/recom_vod", methods=['POST'])
def recom_vod() :

    # json 데이터 확인
    print(request.is_json)
    # json 데이터 변환 및 value값 추출
    json_movie_seq = request.get_json()
    print(json_movie_seq['movie_seq'])
    movie_seq = int(json_movie_seq['movie_seq'])
    print(type(movie_seq))

    # 영화시퀀스에 해당하는 키워드 추출
    movie_keywords = movie_keywords_df[movie_keywords_df["movie_seq"]== movie_seq]["movie_keywords"].item()
    movie_keywords = movie_keywords.replace(',', " ")
    print(movie_keywords)
    
    # 벡터 차원정의
    movie_content_emb_index = faiss.IndexFlatL2(768)
    # 영화별 줄거리 벡터 유사도 계산
    movie_content_emb_index.add(np.ascontiguousarray(movie_content_emb_df.iloc[:, -768:].values.astype(np.float32)))

    # 키워드 워드임베딩
    movie_keywords_vec = model.encode(movie_keywords)
    # 차원 형태 변경
    movie_keywords_vec = np.expand_dims(movie_keywords_vec, axis=0)
    # 키워드와 가까운 거리값(distances)과 인덱스값(indeices) SEARCH_NUM(5)개 추출
    movie_content_emb_distances, movie_content_emb_indices = movie_content_emb_index.search(movie_keywords_vec, 5)
    # 키워드와 유사한 영화시퀀스와 제목 추출
    sel_movie_cotent = movie_content_emb_df[['movie_seq', 'movie_title']].iloc[movie_content_emb_indices[0]]
    sel_movie_cotent['distance'] = movie_content_emb_distances[0]
    # 추천영화 키워드 추출
    recom_vod_seq = sel_movie_cotent["movie_seq"].to_list()
    if movie_seq in recom_vod_seq :
        recom_vod_seq.remove(movie_seq)
    else :
        recom_vod_seq.pop(-1)
    print(recom_vod_seq)
    # 딕셔너리 타입으로 수정
    recom_vod_seq_json = {'status': True, 'movie_seq': recom_vod_seq}
    
    # json타입 리턴
    return jsonify(recom_vod_seq_json)

if __name__ == '__main__' :
    app.run(debug=False, host="127.0.0.1", port=5000)