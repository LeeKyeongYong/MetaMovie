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
SEARCH_NUM = 20


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

def get_recommend_movie(user_input):
    try:
        user_input_vec = model.encode(user_input)
        user_input_vec = np.expand_dims(user_input_vec, axis=0)

        #print('plot_text_emb_index',plot_text_emb_index)
        plot_text_emb_distances, plot_text_emb_indices = plot_text_emb_index.search(user_input_vec, SEARCH_NUM)
        #print('plot_text_emb_distances',plot_text_emb_distances)
        print('--', plot_text_emb_indices[0])

        sel_movie_plot_text = plot_text_emb_df[['movie_title', 'movie_code']].iloc[plot_text_emb_indices[0]]
        sel_movie_plot_text['distance'] = plot_text_emb_distances[0]

        print('===================== plot_text ======================================')
        print(type(sel_movie_plot_text))
        print(sel_movie_plot_text)

    
        #ret_movies = sel_movie_plot_text.values.tolist()
        
        # df to dictionary
        ret_movies = sel_movie_plot_text.to_dict('records')

        return ret_movies

    except:
        print("ERROR : ", user_input)

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
    
    input = params['input']
    #print(input, type(input))
    user_input = ' '.join(input)
    print('user input str',user_input)

    #input = "겨울 크리스마스 눈"
    ret = get_recommend_movie(user_input)


    return ret 




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    # 데모 모드 선택
    parser.add_argument('--demo_mode', type=str, default='on') # on, off

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
    
    # 데이터 경로
    parser.add_argument('--movie_data_path', type=str, default='./ontology_src')

    args = parser.parse_args()

    print ('\ninit vod recommendation model...')
    model = SentenceTransformer('jhgan/{}'.format(args.model_name))
    model.eval()

    # 형태소 분석기 선택
    tokenizer_dic = {'mec':Mecab(), 'okt':Okt(), 'kkm':Kkma(), 'kom':Komoran(), 'han':Hannanum(), 'twi':Twitter(), 'kha':khaiii_morph_analyzer()}
    morph_tokenizer = tokenizer_dic[args.sel_tokenizer]

    movie_folder_list = os.listdir(args.movie_data_path)

    if args.demo_mode == 'off':
        os.makedirs('./output/movie_embedding/{}_{}'.format(args.model_name, args.sel_tokenizer), exist_ok=True)

        plot_text_emb_df = pd.DataFrame(columns=['movie_title', 'movie_code', 'movie_plot'] + ['movie_plot_emb_{}'.format(num) for num in range(EMB_SIZE)])

        movie_info_df = pd.read_csv('./movie_info_base_202211011116.csv')
        movie_info_df = movie_info_df[['moviecd', 'movienm']]

        for movie_folder_name in tqdm(movie_folder_list):
            movie_folder_path = args.movie_data_path + '/{}/'.format(movie_folder_name)
            movie_data_list = os.listdir(movie_folder_path)

            if any('plot' in plot_name for plot_name in movie_data_list):
                try:
                    plot_text = pd.read_csv(movie_folder_path + 'plot.txt', header=None)
                except:
                    continue


                try:

                    # 영화 줄거리 벡터화
                    plot_text = ' '.join(map(str, plot_text.values.tolist()[0]))
                    plot_text_emb = model.encode(plot_text)

                    movie_title = movie_info_df[movie_info_df['moviecd']==int(movie_folder_name.split('_')[-1])]['movienm'].item()

                    # 영화 줄거리 벡터화
                    plot_text_emb_df.loc[len(plot_text_emb_df)] = [movie_title, movie_folder_name, plot_text] + [vec_num for vec_num in plot_text_emb.tolist()]

                except:
                    continue

        plot_text_emb_df.to_csv('./output/movie_embedding/{}_{}/plot_text_emb.csv'.format(args.model_name, args.sel_tokenizer), encoding="utf-8-sig")


    elif args.demo_mode == 'svc':

        os.makedirs('./output/movie_recommendation/{}_{}'.format(args.model_name, args.sel_tokenizer), exist_ok=True)

        print('loading plot embedding data...')
        plot_text_emb_df = pd.read_csv('./output/movie_embedding/{}_{}/plot_text_emb.csv'.format(args.model_name, args.sel_tokenizer), index_col=0)

        plot_text_emb_index = faiss.IndexFlatL2(EMB_SIZE)
        plot_text_emb_index.add(np.ascontiguousarray(plot_text_emb_df.iloc[:, -EMB_SIZE:].values.astype(np.float32)))

        # start service
        print ('\nstart service...')
        app.run(host='0.0.0.0', port=8888, debug=True)

    elif args.demo_mode == 'on':
        os.makedirs('./output/movie_recommendation/{}_{}'.format(args.model_name, args.sel_tokenizer), exist_ok=True)

        print('loading plot embedding data...')
        plot_text_emb_df = pd.read_csv('./output/movie_embedding/{}_{}/plot_text_emb.csv'.format(args.model_name, args.sel_tokenizer), index_col=0)

        plot_text_emb_index = faiss.IndexFlatL2(EMB_SIZE)
        plot_text_emb_index.add(np.ascontiguousarray(plot_text_emb_df.iloc[:, -EMB_SIZE:].values.astype(np.float32)))


        while True:
            try:
                #time.sleep(0.5)
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print()
                user_input = input("입력해주세요 : ")
                user_input = str(user_input)

                if user_input == 'quit':
                    break

                user_input_vec = model.encode(user_input)
                user_input_vec = np.expand_dims(user_input_vec, axis=0)

                plot_text_emb_distances, plot_text_emb_indices = plot_text_emb_index.search(user_input_vec, SEARCH_NUM)
                sel_movie_plot_text = plot_text_emb_df[['movie_title', 'movie_code']].iloc[plot_text_emb_indices[0]]
                sel_movie_plot_text['distance'] = plot_text_emb_distances[0]


                print() 
                print('===================== plot_text ======================================')
                print(sel_movie_plot_text)
                print() 
                print()

                search_result_path = './output/movie_recommendation/{}_{}/input_{}'.format(args.model_name, args.sel_tokenizer, user_input)
                os.makedirs(search_result_path, exist_ok=True)
                sel_movie_plot_text.to_csv(search_result_path + '/sel_movie_by_plot_text.csv', encoding="utf-8-sig")

            except:
                print("ERROR : ", user_input)

    else:
        print('pass')
        pass

        
    print('done')
