import os
import argparse

import numpy as np
import pandas as pd
from tqdm import tqdm
import faiss

from sentence_transformers import SentenceTransformer

from konlpy.tag import Kkma, Komoran, Okt, Mecab, Hannanum, Twitter
from khaiii import KhaiiiApi

from flask import Flask
from flask import request


app = Flask(__name__)
api = KhaiiiApi()

# 시드값을 고정해두지 않았기에 유사도 측정에 있어서 미세한 차이가 존재할 수 있음
PLOT_TOP_K = 20
EMB_SIZE = 768
SEARCH_NUM = 10


class khaiii_morph_analyzer:
    def __init__(self):
        self.khaiii_api = KhaiiiApi()

    def analyzing_text(self, input_data):
        morphs_list = []
        analyzed_text = self.khaiii_api.analyze(input_data)
        for word in analyzed_text:
            for morph in word.morphs:
                morphs_list.append((morph.lex, morph.tag))
        return morphs_list

    def nouns(self, input_data):
        nouns_list = []
        analyzed = self.analyzing_text(input_data)
        for token, morph_tag in analyzed:
            if morph_tag in ['NNP', 'NNG', 'NNB', 'NP']:    # 수사는 제외
                nouns_list.append(token)
        return nouns_list


# 메타데이터를 입력 받아 추천영화 출력
@app.route("/recom_vod", methods=['POST'])
def recom_vod():
    '''
    {
    "input": "겨울,자매, 언니,눈, 엘사"
    }
    '''
    print(request.is_json)
    #print(request.json)
    params = request.get_json()
    #params = request.get_json()
    print('-', params)
    print(params['input'])

    movie_cds = ["1234","1234","1234","1234"]
    '''
    output
    {'status': True, 'movie_cd': [1,2,3,4]}
    '''
    ret_json = {'status': 'true', 'movie_cds': movie_cds}
    print(ret_json)
    return ret_json


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # 데모 모드 선택
    parser.add_argument('--demo_mode', type=str, default='none') # on, off

    # 형태소 분석기 선택
    # mec, okt, kkm, kom, han, twi, kha
    parser.add_argument('--sel_tokenizer', type=str, default='kha')


    # 모델 선택
    # https://github.com/jhgan00/ko-sentence-transformers
    # ko-sroberta-multitask
    # ko-sbert-multitask
    # ko-sroberta-base-nli
    # ko-sbert-nli
    # ko-sroberta-sts
    # ko-sbert-sts
    parser.add_argument('--model_name', type=str, default='ko-sroberta-multitask')

    args = parser.parse_args()


    # 사전 훈련된 모델 불러옴
    model = SentenceTransformer('jhgan/{}'.format(args.model_name))
    model.eval()


    # 형태소 분석기 선택
    tokenizer_dic = {'mec':Mecab(), 'okt':Okt(), 'kkm':Kkma(), 'kom':Komoran(), 'han':Hannanum(), 'twi':Twitter(), 'kha':khaiii_morph_analyzer()}
    morph_tokenizer = tokenizer_dic[args.sel_tokenizer]

    if args.demo_mode == 'off':
        # 영화데이터 불러오기
        movie_info_df = pd.read_csv('./moviedata_keywords_df.csv')
        movie_info_df = movie_info_df[['movie_seq', 'movie_title', 'movie_content']]
        # 영화 줄거리 추출
        movie_content_list = movie_info_df.loc[:,'movie_content'].to_list()
        # 임베딩 데이터프레임 생성
        movie_content_emb_df = pd.DataFrame(columns = ['movie_content_emb_{}'.format(num) for num in range(EMB_SIZE)])

        # 영화 줄거리 벡터화
        for movie_content in tqdm(movie_content_list, desc=f'영화 {len(movie_content_list)}개 줄거리 벡터화') :
            # 영화 줄거리 태그 삭제
            movie_content = movie_content.replace("<br/>", " ").replace("\'", " ")
            # 영화 줄거리 문자열 변환
            movie_content = ' '.join(movie_content)
            # 영화 줄거리 워드임베딩(768개)
            movie_content_emb = model.encode(movie_content)
            # 데이터프레임에 데이터 추가
            movie_content_emb_df.loc[len(movie_content_emb_df)] = [vec_num for vec_num in movie_content_emb.tolist()]
        # 데이터 저장
        movie_content_emb_df = pd.concat([movie_info_df, movie_content_emb_df], axis=1)
        movie_content_emb_df.to_csv("moviedata_content_emb.csv", index=False, encoding='utf-8')

    elif args.demo_mode == 'on':
        # 영화줄거리 임베딩 데이터 불러오기
        movie_content_emb_df = pd.read_csv('./moviedata_content_emb.csv')
        # 벡터 차원정의
        movie_content_emb_index = faiss.IndexFlatL2(EMB_SIZE)
        # 영화별 줄거리 벡터 유사도 계산
        movie_content_emb_index.add(np.ascontiguousarray(movie_content_emb_df.iloc[:, -EMB_SIZE:].values.astype(np.float32)))

        while True:
            try:
                #time.sleep(0.5)
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print()
                # 키워드 입력
                user_input = input("입력해주세요 : ")
                user_input = str(user_input)

                # 키워드 입력 대신 quit 입력시 종료
                if user_input == 'quit':
                    break
                
                # 키워드 워드임베딩
                user_input_vec = model.encode(user_input)
                # 차원 형태 변경
                user_input_vec = np.expand_dims(user_input_vec, axis=0)
                # 키워드와 가까운 거리값(distances)과 인덱스값(indeices) SEARCH_NUM(10)개 추출
                movie_content_emb_distances, movie_content_emb_indices = movie_content_emb_index.search(user_input_vec, SEARCH_NUM)
                # 키워드와 유사한 영화시퀀스와 제목 추출
                sel_movie_cotent = movie_content_emb_df[['movie_seq', 'movie_title']].iloc[movie_content_emb_indices[0]]
                sel_movie_cotent['distance'] = movie_content_emb_distances[0]


                print() 
                print('===================== 영화 추천 ======================================')
                print(sel_movie_cotent)
                print() 
                print()
                
            except:
                print("ERROR : ", user_input)

            else:
                print('pass')
                pass
    else :
        print('demo_mode를 on 혹은 off 로 실행해주세요')
        pass
        
    print('done')