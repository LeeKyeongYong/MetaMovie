import os
import argparse

import numpy as np
import pandas as pd
from tqdm import tqdm

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

#from konlpy.tag import Kkma, Komoran, Okt, Mecab, Hannanum, Twitter
from khaiii import KhaiiiApi

# 시드값을 고정해두지 않았기에 유사도 측정에 있어서 미세한 차이가 존재할 수 있음



# 입력받은 줄거리와 키워드를 벡터로 변환하고 서로간 유사도를 계산 및 정렬하는 함수
def get_text_keywords_cosine_similarity(input_model, input_text, input_keyword_list, top_k=-1):
    
    # 입력받은 줄거리 벡터화
    sentence_emb = input_model.encode(input_text)
    sentence_emb = np.expand_dims(sentence_emb, axis=0)

    # 입력받은 키워드 벡터화
    keyword_emb_arr = input_model.encode(input_keyword_list)

    # 줄거리 벡터와 키워드 벡터간 유사도 계산
    cos_value_list = cosine_similarity(sentence_emb, keyword_emb_arr)

    # 각 키워드와 대응되는 유사도 저장
    output_df = pd.DataFrame({
            'keyword': input_keyword_list,
            'cosine_score':cos_value_list[0]
            })

    # 유사도 기준으로 키워드 정렬
    output_df = output_df.sort_values(by='cosine_score', ascending=False)
    
    # 상위 top_k 개의 키워드 추출
    sel_keyword_df = output_df.iloc[:top_k]

    return sel_keyword_df

# Khaiii api를 다른 일반적인 형태소 분석기과 같이 사용하기 위한 클래스
class khaiii_morph_analyzer:
    def __init__(self):
        self.khaiii_api = KhaiiiApi()

    # 다른 형태소 분석기의 pos 함수 구현
    def pos(self, input_data):
        morphs_list = []
        analyzed_text = self.khaiii_api.analyze(input_data)
        for word in analyzed_text:
            for morph in word.morphs:
                morphs_list.append((morph.lex, morph.tag))
        return morphs_list

    # 다른 형태소 분석기의 nouns 함수 구현
    def nouns(self, input_data):
        nouns_list = []
        analyzed = self.pos(input_data)
        for token, morph_tag in analyzed:
            if morph_tag in ['NNP', 'NNG', 'NNB', 'NP']:    # 수사는 제외
                nouns_list.append(token)
        return nouns_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # 데모 모드 선택
    parser.add_argument('--demo_mode', type=str, default='none')    # on, off

    # 형태소 분석기 선택
    # mec, okt, kkm, kom, han, twi, kha
    # 현재 다른 형태소 분석기는 주석처리 상태, 사용하려는 경우 상단 주석 처리된 konlpy 패키지 import 문을 주석 해제하면 사용가능
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
    
    # 추출하고자 하는 최대 키워드 수 설정
    parser.add_argument('--TOP_K', type=int, default=-1)

    # 데이터 경로
    parser.add_argument('--movie_data_path', type=str, default='./ontology_src')

    args = parser.parse_args()


    # 사전 훈련된 모델 불러옴
    model = SentenceTransformer('jhgan/{}'.format(args.model_name))
    model.eval()



    # 형태소 분석기 선택
    # 현재 다른 형태소 분석기는 주석처리 상태, 사용하려는 경우 하단 토크나이저 사전 주석 처리를 해제하고 다른 토크나이저 사전을 주석 처리시 사용 가능
    #tokenizer_dic = {'mec':Mecab(), 'okt':Okt(), 'kkm':Kkma(), 'kom':Komoran(), 'han':Hannanum(), 'twi':Twitter(), 'kha':khaiii_morph_analyzer()}
    tokenizer_dic = {'kha':khaiii_morph_analyzer()} # 토크나이저 사전

    morph_tokenizer = tokenizer_dic[args.sel_tokenizer]

    movie_folder_list = os.listdir(args.movie_data_path)



    # demo_mode on 인 경우 입력한 영화의 줄거리 데이터의 키워드 추출 및 유사도 계산 작업 시작
    # demo_mode off 인 경우 ontology_src 내부 모든 영화 줄거리 데이터의 키워드 추출 및 유사도 계산 작업 시작

    # demo_mode on
    if args.demo_mode == 'on':
        
        # 영화 목록 및 대응되는 영화 번호 데이터 로드
        movie_info_df = pd.read_csv('./movie_info_base_202211011116.csv')
        movie_info_df = movie_info_df[['moviecd', 'movienm']]

        while True:
            try:
                
                # 영화명 입력
                user_input = input("영화 이름을 입력해주세요 : ")
                user_input = str(user_input)

                # 영화명 입력 대신 quit 입력시 종료
                if user_input == 'quit':
                    break

                # 입력한 영화명이 영화 목록에 존재하지 않는 경우 에러처리 후 재입력
                try:
                    movie_folder_name = str(movie_info_df[movie_info_df['movienm'] == user_input]['moviecd'].item())
                except:
                    print('입력하신 키워드의 영화는 존재하지 않습니다')
                    print('다른 영화 이름을 입력해주세요')
                    print()
                    continue

                # 입력한 영화명의 영화 데이터가 존재하지 않는 경우 에러처리 후 재입력
                try:
                    movie_folder_path = args.movie_data_path + '/movie_{}/'.format(movie_folder_name)
                    movie_data_list = os.listdir(movie_folder_path)
                except:
                    print('해당 영화 데이터는 존재하지 않습니다')
                    print('다른 영화 이름을 입력해주세요')
                    print()
                    continue

                # 영화 줄거리 데이터 로드
                if any('plot' in plot_name for plot_name in movie_data_list):
                    try:
                        plot_text = pd.read_csv(movie_folder_path + 'plot.txt', header=None)
                    except:
                        continue

                # 데모 결과를 저장할 movie_keyword_weighting_demo 폴더와 영화 번호 - 영화명으로 구성된 폴더 생성
                os.makedirs('./output/movie_keyword_weighting_demo/{}_{}/movie_{}-{}'.format(args.model_name, args.sel_tokenizer, movie_folder_name, user_input), exist_ok=True)

                # 영화 줄거리에서 키워드 추출
                try:
                    # 영화 줄거리를 한줄의 string으로 변환
                    plot_text = ' '.join(map(str, plot_text.values.tolist()[0]))

                    # 영화 줄거리의 키워드 목록 추출 - 현재 코드는 수사를 제외한 명사만 추출
                    plot_keyword_list = morph_tokenizer.nouns(plot_text)
                    plot_keyword_list = list(set(plot_keyword_list))

                    # 영화 줄거리와 키워드간 유사도 계산 및 상위 유사 키워드 추출
                    plot_keyword_cos_val_df = get_text_keywords_cosine_similarity(model, plot_text, plot_keyword_list, args.TOP_K)

                    # 추출된 키워드 및 유사도 데이터 저장
                    plot_keyword_cos_val_df.to_csv('./output/movie_keyword_weighting_demo/{}_{}/movie_{}-{}/{}-plot_keyword_cos_val.csv'.format(args.model_name, args.sel_tokenizer, movie_folder_name, user_input, user_input), encoding="utf-8-sig")

                except:
                    continue

                print()
                print('========================= 줄거리 키워드 검색 =================================')
                print(plot_keyword_cos_val_df)
                print()

                print('search_{}_keyword_done'.format(user_input))
                print()
                print()
                print()

            except:
                pass

    # demo_mode off
    elif args.demo_mode == 'off':

        # 각 영화별 영화 키워드 및 유사도 추출
        for movie_folder_name in tqdm(movie_folder_list):
            movie_folder_path = args.movie_data_path + '/{}/'.format(movie_folder_name)
            movie_data_list = os.listdir(movie_folder_path)

            # 영화 줄거리 데이터 존재 확인
            if any('plot' in plot_name for plot_name in movie_data_list):

                # 영화 줄거리 데이터 로드
                try:
                    plot_text = pd.read_csv(movie_folder_path + 'plot.txt', header=None)
                except:
                    continue

                # 해당 영화 키워드 및 유사도 데이터 저장 폴더 생성
                os.makedirs('./output/movie_keyword_weighting/{}_{}/{}'.format(args.model_name, args.sel_tokenizer, movie_folder_name), exist_ok=True)

                # 영화 줄거리에서 키워드 추출
                try:
                    # 영화 줄거리를 한줄의 string으로 변환
                    plot_text = ' '.join(map(str, plot_text.values.tolist()[0]))

                    # 영화 줄거리의 키워드 목록 추출 - 현재 코드는 수사를 제외한 명사만 추출
                    plot_keyword_list = morph_tokenizer.nouns(plot_text)
                    plot_keyword_list = list(set(plot_keyword_list))

                    # 영화 줄거리와 키워드간 유사도 계산 및 상위 유사 키워드 추출
                    plot_keyword_cos_val_df = get_text_keywords_cosine_similarity(model, plot_text, plot_keyword_list)

                    # 추출된 키워드 및 유사도 데이터 저장
                    plot_keyword_cos_val_df.to_csv('./output/movie_keyword_weighting/{}_{}/{}/{}-plot_keyword_cos_val.csv'.format(args.model_name, args.sel_tokenizer, movie_folder_name, movie_folder_name), encoding="utf-8-sig")

                except:
                    continue
    
    else:
        print('demo_mode를 on 혹은 off 로 실행해주세요')
        pass


    print('done')