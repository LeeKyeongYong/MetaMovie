import ast
import json
import os
import random

from flask_cors import CORS,cross_origin
from numpy import deprecate
from flask import Flask, request, jsonify, render_template
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from recommendation.algorithm_poc01 import do_recommendation, get_movie_image, do_recommendation_01
from recommendation.algorithm_poc02 import *

from vod_common.crawling_value import CrawlingValueDB
from vod_common.movie_info import MovieInfo
from vod_common.ontology import Ontology
from vod_common.ontology_pool import OntologyPool
from vod_common.percent_encoder import percent_decode
from vod_common.vod_pool_info import get_result_dict, make_key
from vod_common.user import UserValueDB
from vod_common.util.util_movies import get_random_movie_by_genre
from utils.util_making_user_data import MakingUserData

# by dh to use local file
from recommendation.algorithm_poc01 import *
# from algorithm_std import *
app = Flask(__name__)


"""
1차 PoC
"""


# @app.route('/vod_recommendation', methods=['GET', 'POST'])
@app.route('/recommendation01', methods=['GET'])
def add_message():

    # TODO 선택영화 이외에 추천할 영화의 개수
    movie_number = 5

    # TODO 파라미터추출 > 추천 알고리즘 함수 결과 반환
    get_params = request.args.to_dict() # get_params {'movieName': '디워'}
    select_movie_name = str(get_params['movie_name']) # vod html에서 선택한 영화제목 :  디워
    recommendation_result = do_recommendation(select_movie_name) # 영화추천 함수 결과값
    # print(recommendation_result)
    # print("[do_recommendation 리턴값(추천영화목록)]")
    # print(type(recommendation_result)) # 데이터 프레임
    # print(recommendation_result.head()) # 상위 5개만 추출(테스트용)

    # TODO 추천된 모든 영화중 상위 항목만 추출
    movie_info_dataframe_ranking = recommendation_result.iloc[:movie_number+1] # 추천 영화 정보중 상위랭크만 추출, 데이터프레임(선택영화포함)
    movie_info_dict_ranking = movie_info_dataframe_ranking.to_dict('records') # dict으로 개별 영화 정보 전부 추출

    # TODO 상위항목의 영화명만 추출 > 선택영화와 추천영화를 구분
    movie_name_list_ranking = movie_info_dataframe_ranking['movie_name'].tolist() # 영화명만 따로 추출
    movie_name_list_ranking_str = list(map(str, movie_name_list_ranking)) # 영화명이 숫자인 예외상황이 있기 때문에 문자열로 바꿔줌

    # TODO 영화 포스터 이미지 가져오기
    movie_name_list_ranking_url = get_movie_image(movie_name_list_ranking_str)

    # TODO (각 영화별 온톨로지 정렬을 위해)추천영화 정보에서 영화명을 지우고 key, value가 tuple로 들어있는 리스트 객체로 변환
    list_movie_values_sorted = []
    for dict_each in movie_info_dict_ranking:
        del(dict_each['movie_name']) # 영화명을 지우고 온톨로지 백분율데이터만 남긴다(영화명과 인덱스를 공유함)
        sort_tuple_each = sorted(dict_each.items(), key=lambda x: x[1], reverse=True) # 내림차순 정렬
        list_movie_values_sorted.append(sort_tuple_each)

    # TODO 시각화 파일 만들기(평소엔 주석처리-새로운 영화가 추가 됐을시 update룰 위해 주석 해제)
    #visualization(movie_name_list_ranking, list_movie_values_sorted)

    # NOTE 서비스용 - 3/16 이후 쓰지 않음
    # @deprecate
    # return render_template('result.html', select_name=select_movie_name, select_url=movie_name_list_ranking_url[0], movie=movie_name_list_ranking_str[1:], movie_url=movie_name_list_ranking_url[1:])

    # TODO 로컬용
    # for movie_name in movie_name_list_ranking_str:

    # NOTE 2022/03/16~
    movie_recommedation_json = {"movieChoice" : movie_name_list_ranking_str[0], "movieChoiceImg": movie_name_list_ranking_url[0],"movieRecommedation" : movie_name_list_ranking_str[1:], "movieRecommedationImg": movie_name_list_ranking_url[1:]}
    print(movie_recommedation_json)
    return movie_recommedation_json
    
    #return render_template('result_local.html', select_name=select_movie_name, select_url=movie_name_list_ranking_url[0], movie=movie_name_list_ranking_str[1:], movie_url=movie_name_list_ranking_url[1:])
    #return movie_recommedation_json


"""
2차 PoC
"""

@app.route('/get_random_movie', methods=['GET'])
def get_random_movie():
    print('\n\nget_random_movie')
    get_params = request.args.to_dict()
    print(get_params)

    # pool_index : 0 ,1 default 0
    # pool_type : n ,g default n
    page = 0
    try :
        pool_index = get_params['pool_index']
        pool_type = get_params['pool_type']
        count = get_params['count']
        page = get_params['page']
    except:
        print('Error')


    movieInfo = MovieInfo(pool_index, pool_type)
    ret_list_ids, ret_list_names, ret_list_imgs = movieInfo.get_random_movie_info_cnt(count)
    #ret_list_ids, ret_list_names, ret_list_imgs = movieInfo.get_movie_info_cnt(page, count)

    ret_json = { "movie_ids": ret_list_ids, "movie_names" : ret_list_names, "movie_imgs": ret_list_imgs}
    return ret_json 


@app.route('/movie/get', methods=['GET'])
def movie_get():
    print('\n\nmovie_get')

    pool_index = request.args.get('pool_index', default='6')
    pool_type = request.args.get('pool_type', default='n')
    page = request.args.get('page', default=0)
    count = request.args.get('count', default=20)
    lang = request.args.get('lang', default='ko')

    movieInfo = MovieInfo(pool_index, pool_type, lang)
    ret_list_ids, ret_list_names, ret_list_imgs = movieInfo.get_movie_info_cnt(count, page)

    ret_json = {"movie_ids": ret_list_ids, "movie_names": ret_list_names, "movie_imgs": ret_list_imgs}
    return ret_json 


@app.route('/movie/similarity', methods=['GET'])
def movie_similarity():
    print('\n\nmovie_similarity')

    pool_index = request.args.get('pool_index', default='6')
    pool_type = request.args.get('pool_type', default='n')
    movie_ids = request.args.get('movie_ids', default=None).split(',')
    lang = request.args.get('lang', default='ko')

    otlgValueDB = CrawlingValueDB(pool_index, pool_type)
    if (otlgValueDB.db_connect()):
        otlgValueDB.create_table(0)
    else:
        otlgValueDB.db_close()
        print('Error, DB Connection')    

    movieInfo = MovieInfo(pool_index, pool_type, lang)
    # ontology = Ontology(pool_index, lang)
    ontologyPool = OntologyPool(pool_index, lang)

    # 각 영화의 속성, 장르, 감독, 배우 데이터
    ret_movie_info_list = []
    for movie_id in movie_ids:
        movie_id = int(movie_id)
        movie_name = movieInfo.get_movie_name(movie_id)
        print('\n', movie_id, movie_name)

        otlg_pct_value = otlgValueDB.db_get_ontology_value_list(1, movie_id)
        print('otlg_pct_value', otlg_pct_value)
        # otlg_str = ontology.get_all_list()
        otlg_str = ontologyPool.db_get_true_ontology()

        otlg_name_val_dict = {}
        # for idx, otlg_val in enumerate(otlg_str):
        #     otlg_name_val_dict[otlg_val] = otlg_pct_value[idx]
        otlg_name_val_dict = otlgValueDB.db_get_ontology_value_list(1, movie_id)

        # reverse sort by value
        otlg_name_val_dict = dict(reversed(sorted(otlg_name_val_dict.items(), key=lambda item: item[1])))
        print('check', otlg_name_val_dict)

        ret_list_genres = movieInfo.get_movie_genres(movie_id)
        if lang == 'en':
            # ret_list_genres = ontology.get_otlg_str_en(ret_list_genres)
            ret_list_genres = ontologyPool.db_get_otlg_ko_to_en(ret_list_genres)

        ret_list_directors = movieInfo.get_movie_directors(movie_id)
        
        # 배우의 경우 목록이 너무 긴 영화도 있어, 임의로 5명까지 자름
        ret_list_actors = movieInfo.get_movie_actors(movie_id)

        # 다음 키워드들 임시로 출력에서만 제거. 추후 수정 예정
        if lang == 'ko':
            except_otlg = ['기자', '서울', '외계인', '학교', '다양한']
        else:
            except_otlg = ['reporter', 'Seoul', 'school', 'various']
        ret_list_otlg = []
        for otlg_text, property_val in otlg_name_val_dict.items():
            if otlg_text not in (ret_list_genres + except_otlg):
                ret_list_otlg.append(str(otlg_text))
                if len(set(ret_list_otlg)) == 10:
                    break

        ret_movie_info = {movie_name: {"ontology": ret_list_otlg, "genre": ret_list_genres, "director": ret_list_directors, "actor": ret_list_actors}}
        ret_movie_info_list.append(ret_movie_info)
        print(ret_movie_info_list)

    # get similarity
    if len(movie_ids) == 1:
        ret_val = {"info": ret_movie_info_list}
    elif len(movie_ids) == 2:
        std_simil_val, ext_simil_val, cos_simil_val = get_movie_similarity(pool_index, pool_type, movie_ids[0], movie_ids[1])
        simil_vals = get_more_movie_similarity(pool_index, pool_type, movie_ids[0], movie_ids[1])
        ret_val = {"ext_similarity": ext_simil_val,
                   "std_similarity": std_simil_val,
                   "cos_similarity": cos_simil_val,
                   "similarity_adj": simil_vals[0],
                   "similarity_era": simil_vals[1],
                   "similarity_genre": simil_vals[2],
                   "similarity_otlg": simil_vals[3],
                   "similarity_place": simil_vals[4],
                   "info": ret_movie_info_list}

    print('\n', ret_val)
    return ret_val

@app.route('/otlg/search', methods=['GET'])
def otlg_search():
    print('\n\notlg_search')

    pool_index = request.args.get('pool_index', default='6')
    pool_type = request.args.get('pool_type', default='n')
    keyword = request.args.get('keyword', default=None)
    lang = request.args.get('lang', default='ko')

    # print(keyword)
    # otlg = Ontology(pool_index, lang)
    ontologyPool = OntologyPool(pool_index, lang)
    
    # result_otlg_search = otlg.search(keyword, lang)
    result_otlg_search = ontologyPool.db_get_similar_ontology(keyword)
    print('result_otlg_search:', result_otlg_search)
    
    # ret_json = {"search_result_otlg": result_otlg_search}
    ret_json = {"search_result_otlg": result_otlg_search, "search_result_sim_otlg": []}
    
    return ret_json 


@app.route('/movie/search', methods=['GET'])
def movie_search():
    print('\n\nmovie_search')

    get_params = request.args.to_dict()
    print(get_params)
    
    try :
        pool_index = get_params['pool_index']
        pool_type = get_params['pool_type']
        keyword = get_params['keyword']
        lang = get_params['lang']
    except:
        print('Error')

    # print(keyword)
    movieInfo = MovieInfo(pool_index, pool_type, lang)
    
    search_movie_ids = movieInfo.search_movie(keyword)
    # search_movie_ids = movieInfo.search_movie("겨울")

    movie_info_list = []
    # for id in search_movie_ids:
        # print(id)
    id_list, name_list, image_list = movieInfo.get_movie_info(search_movie_ids)
    for i in range(len(id_list)):
        movie_info_list.append({"movie_id":id_list[i], "movie_name":name_list[i]})
        
        # ret_movies.append(movieInfo.get_movie_info(id))

    print(movie_info_list)
    ret_json = { "search_result_movie": movie_info_list}
    
    return ret_json

#@app.route('/selected_movie/get', methods=['GET'])
@app.route('/movie/info', methods=['GET'])
def movie_info():
    print('\n\nmovie_info')

    pool_index = request.args.get('pool_index', default='6')
    pool_type = request.args.get('pool_type', default='n')
    movie_id = int(request.args.get('movie_id', default=None))
    lang = request.args.get('lang', default='ko')

    otlgValueDB = CrawlingValueDB(pool_index, pool_type)
    if (otlgValueDB.db_connect()):
        otlgValueDB.create_table(0)
    else:
        otlgValueDB.db_close()
        print('Error, DB Connection')

    movieInfo = MovieInfo(pool_index, pool_type, lang)
    # ontology = Ontology(pool_index, lang)
    ontologyPool = OntologyPool(pool_index, lang)

    print('\nmovie id', movie_id, 'name:', movieInfo.get_movie_name(movie_id))

    #ret_otlg_str_list = otlgValueDB.db_get_ontology_pct_key_value_list(movie_id, 100)
    #print('otlg top5', ret_otlg_str_list)

    otlg_pct_value = otlgValueDB.db_get_ontology_value_list(1, movie_id)
    otlg_name_val_dict = otlgValueDB.db_get_ontology_value_list(1, movie_id)
    # otlg_str = ontology.get_all_list()
    # otlg_type = ontology.get_all_type_list()
    otlg_str = ontologyPool.db_get_true_ontology()
    otlg_type = ontologyPool.db_get_true_type()
    otlg_name_type_dict = ontologyPool.db_get_true_ontology_type()

    # make data with otlg name, value
    # 임시조건
    if lang == 'ko':
        except_otlg = ['기자', '서울', '외계인', '학교', '다양한']
    else:
        except_otlg = ['reporter', 'Seoul', 'school', 'various']
    # otlg_name_val_dict = {}
    # for idx, otlg_val in enumerate(otlg_str):
    #     # if otlg_pct_value[idx] > 0.5:
    #     # 속성 상세페이지에서 속성값이 1.0 이상인 속성만 표출되도록 변경
    #     if otlg_pct_value[idx] > 1.0:
    #         if otlg_val not in except_otlg:
    #             otlg_name_val_dict[otlg_val] = otlg_pct_value[idx]
    #         else:
    #             # print("임시", otlg_val, otlg_pct_value[idx])
    #             pass
    #     else:
    #         #print('Value is too low. Ignore', otlg_val, otlg_pct_value[idx])
    #         pass
    # 변경 후 버전
    print(len(otlg_name_val_dict.keys()))
    # todo: 1000번을 for문으로 도는 것보다 조건에 맞는 애들만 append해서 끝내는 게 빠를듯. 팀장님 피드백. 수정 필요
    # for key, value in list(otlg_name_val_dict.items()):
    #     # if (value < 1.0) or (key in except_otlg):
    #         del(otlg_name_val_dict[key])
    print(len(otlg_name_val_dict.keys()), otlg_name_val_dict)

    # reverse sort by value
    otlg_name_val_dict = dict(reversed(sorted(otlg_name_val_dict.items(), key=lambda item: item[1])))
    print('\n\notlg value\n', otlg_name_val_dict)
    except_otlg = ['영화', '개봉', '감독', '출연', '영상', '시간', '스토리', '내용', '자신', '마지막', '시작', '세상',
                   '관객', '제작', '완벽', '주인공', '캐릭터', '극장', '장면', '기억', '예고편', '연출', '친구', '결국',
                   '세계', '탄생', '이야기', '연기', '매력', '배우', '흥행', '국내', '경험', '순간', '최고', '과정',
                   '영화관', '효과', '문제', '현실', '남자', '여자', '기록', '기술', '선택', '거대', '사진',
                   '대한민국', '걱정', '현장', '거부', '노력', '인기', '행복', '여성', '중요', '관계', '공감',
                   '목숨', '공격', '공간', '바람', '촬영', '실패', '최악', '러브', '스타', '제안', '수상', '대상',
                   '인생', '화제', '재미', '유명', '유일', '성공', '문화', '운영', '해리',]

    cnt = 0
    for key, value in list(otlg_name_val_dict.items()):
        # if key in except_otlg:
            # del(otlg_name_val_dict[key])
        # else:
        cnt += 1 
        if (cnt > 20):
            del(otlg_name_val_dict[key])
    ret_list_genres = movieInfo.get_movie_genres(movie_id)

    # make data with otlg name, type
    # otlg_name_type_dict = {}
    # for idx, otlg_val in enumerate(otlg_str):
    #     # print(idx, otlg_val, 'type:', otlg_type[idx], 'val:', otlg_pct_value[idx])
    #     otlg_name_type_dict[otlg_val] = otlg_type[idx]
    # print('\n\notlg_name_type_dict\n', otlg_name_type_dict)

    if lang == 'en':
        # ret_list_genres = ontology.get_otlg_str_en(ret_list_genres)
        ret_list_genres = ontologyPool.db_get_otlg_ko_to_en(ret_list_genres)

    ret_list_directors = movieInfo.get_movie_directors(movie_id)
    # 배우의 경우 목록이 너무 긴 영화도 있어, 임의로 5명까지 자름
    ret_list_actors = movieInfo.get_movie_actors(movie_id)

    # add type info
    otlg_ret_list = []
    for otlg_text, property_val in otlg_name_val_dict.items():
        if otlg_text not in ret_list_genres:
            otlg_name_type_val = {}
            otlg_text = otlg_text.replace(' ', '')
            if str(otlg_name_type_dict[otlg_text]) == 'None':
                otlg_name_type_val[otlg_text] = ['0', property_val]
            else:
                otlg_name_type_val[otlg_text] = [str(otlg_name_type_dict[otlg_text]), property_val]
            otlg_ret_list.append(otlg_name_type_val)

    print('\n\notlg ret value\n', otlg_ret_list)

    ret_movie_info = {"movie_name": movieInfo.get_movie_name(movie_id),
                      "movie_img": movieInfo.get_movie_img(movie_id),
                      "ontology": otlg_ret_list,
                      "genre": ret_list_genres,
                      "director": ret_list_directors,
                      "actor": ret_list_actors
                      }

    print('\n', ret_movie_info)
    return ret_movie_info


@app.route('/movie/similar_movie', methods=['GET'])
def movie_similar_movie():
    print('\n\nmovie_similar_movie')

    pool_index = request.args.get('pool_index', default='6')
    pool_type = request.args.get('pool_type', default='n')
    movie_id = int(request.args.get('movie_id', default=None))
    lang = request.args.get('lang', default='ko')
    # print(pool_index, pool_type, movie_id)

    movieInfo = MovieInfo(pool_index, pool_type, lang)

    similar_movie_df = do_recommendation_01(pool_index, pool_type, movie_id, 7)
    similar_movie_ids = similar_movie_df['movie_id'].values.tolist()
    similar_movie_val = similar_movie_df['diff_val'].values.tolist()

    ret_movie_info = {'movies': []}

    for idx in range(len(similar_movie_ids)):
        for_append = {'movie_id': int(), "movie_name": str(), "movie_img": str(), "similarity": int()}
        id = similar_movie_ids[idx]
        for_append['movie_id'] = id
        for_append['movie_name'] = movieInfo.get_movie_name(id)
        for_append['movie_img'] = movieInfo.get_movie_img(id)
        for_append['similarity'] = round(100-(similar_movie_val[idx]*100), 2)
        ret_movie_info['movies'].append(for_append)

    print('\n', ret_movie_info)

    return ret_movie_info


@app.route('/movie_name/info', methods=['GET'])
def movie_id_by_name():
    """ 고대결과로 받은 영화 이름을 인자로 받아서, 영화이름으로 영화의 id값 조회 """
    keys = request.args.get('keys')
    pool_index = request.args.get('pool_index', default='6')
    pool_type = request.args.get('pool_type', default='n')
    lang = request.args.get('lang', default='ko')
    movieInfo = MovieInfo(pool_index, pool_type, lang)
    print("before keys:", keys)
    keys = percent_decode(keys)
    keys = keys.replace('[', '')
    keys = keys.replace(']', '')
    keys = keys.split(', ')
    print("keys:", keys)

    movie_ids = []
    movie_names = []
    for movie_name in keys:
        movie_name = movie_name.replace('^',',')
        updated_movie_name = movie_name.replace(' ','')
        print('movie_name:', updated_movie_name)
        movie_id = movieInfo.get_movie_id(updated_movie_name)
        print('movie_id:', movie_id)
        movie_ids.append(movie_id)
        movie_names.append(movie_name)
    ret_movie_info = {
        "movie_ids": movie_ids,
        "movie_names": movie_names
                      }
    return ret_movie_info

@app.route('/user/rating', methods=['GET'])
def user_rating():
    print('\n\nuser_rating')
    user_id = request.args.get('user_id')
    movie_id = request.args.get('movie_id')
    score = request.args.get('score')
    print('user_id', user_id, 'movie_id', movie_id, 'score', score)
    ret_json = {"ret": "", "msg": None}

    userDB = UserValueDB()
    # 위에서 connection OK 여부 확인하고
    if userDB.db_status == True:
        userDB.db_insert_rating_value(user_id, movie_id, score)
        ret_json["ret"] = True
    else:
        ret_json["ret"] = False
        ret_json["msg"] = "DB가 연결되지 않습니다."
    userDB.db_close()
    return ret_json


@app.route('/user/rating/get_score', methods=['GET'])
def user_rating_get_score():
    print('\n\nuser_rating_get_score')

    user_id = request.args.get('user_id')
    movie_id = request.args.get('movie_id')
    print('user_id', user_id, 'movie_id', movie_id)
    ret_json = {"ret": "", "msg": None, "score": int()}

    userDB = UserValueDB()
    # 위에서 connection OK 여부 확인하고
    if userDB.db_status == True:
        existence = userDB.db_check_existence_rating_value(user_id, movie_id)
    else:
        ret_json["ret"] = False
        ret_json["msg"] = "DB가 연결되지 않습니다."

    if existence == True:
        score = userDB.db_get_rating_value(user_id, movie_id)
        print('score', score)
        ret_json["ret"] = True
        ret_json["score"] = int(score)
    else:
        ret_json["ret"] = True
        ret_json["score"] = int(0)
    userDB.db_close()

    return ret_json

'''
@app.route('/movie/info2', methods=['GET'])
def movie_info2():
    print('\n\nmovie_info2')

    pool_index = request.args.get('pool_index', default='4')
    pool_type = request.args.get('pool_type', default='n')
    movie_id = int(request.args.get('movie_id', default=None))

    # for banana
    path = f'/opt/svc_vod_recommendation/vod_recommendation/data/ontology_src/movie_{str(movie_id)}'
    # for local
    # path = f'../data/ontology_src/movie_{str(movie_id)}'

    res_adj = []
    res_noun = []
    # 소스 폴더가 이미 있을 때만
    if os.path.isdir(path) == True:
        for file in os.listdir(path):
            with open(os.path.join(path, file), 'r') as f:
                text = f.read()
                # print(text)
                adj = pos_text_adj(text)
                res_adj.extend(adj)
                noun = pos_text_noun(text)
                res_noun.extend(noun)
    freq_adj = most_frequency(res_adj)
    freq_noun = most_frequency(res_noun)
    print("freq_adj", freq_adj)
    print("freq_noun", freq_noun)

    ret_word = {movie_id: [freq_adj, freq_noun]}
    return ret_word
'''

@app.route('/otlg/recommendation', methods=['GET'])
def otlg_recommendation():
    '''
    속성, 장르, 배우, 감독 선택했을 때 파라미터로 받아서 속성 값 계산 후 영화 정보 return함
    :return: ret_json = {"recommend_result": [
                         {"친구+액션+시리즈": [{name:"","image":"","movie_id":"","otlg":[ ],"otlg_val":[ ]},]},
                         {"친구": [{name:"","image":"","movie_id":"","otlg":[ ],"otlg_val":[ ]},]}
                         ]}
    '''
    print('\n\nurl otlg_recommendation', request.args)

    pool_index = request.args.get('pool_index', default='6')
    pool_type = request.args.get('pool_type', default='n')
    lang = request.args.get('lang', default='ko')
    movie_ids = request.args.get('movie_ids', default='').split(',')
    ontologies = request.args.get('ontologies', default='').split(',')
    genres = request.args.get('genres', default='').split(',')
    directors = request.args.get('directors', default='').split(',')
    actors = request.args.get('actors', default='').split(',')

    ontologies = set(ontologies + genres)
    ontologies = [i for i in list(ontologies) if i != ""]
    staff = set(directors + actors)
    staff = [i for i in list(staff) if i != ""]
    print("ontologies", ontologies, "staff", staff)

    movieInfo = MovieInfo(pool_index, pool_type, lang)
    # ontology = Ontology(pool_index, lang)
    ontologyPool = OntologyPool(pool_index, lang)
    otlgValueDB = CrawlingValueDB(pool_index, pool_type)
    if (otlgValueDB.db_connect()):
        otlgValueDB.create_table(0)
    else:
        otlgValueDB.db_close()
        print('Error, DB Connection')

    # otlg_str = ontology.get_all_list()
    otlg_str = ontologyPool.db_get_true_ontology()
    otlg_pct_value_all = otlgValueDB.db_get_ontology_value_all(1)
    # otlg_pct_value_all = otlgValueDB.db_get_ontology_pct_all(1)
    otlg_value_all = []
    movie_ids_all = []
    for movie_id, pct_value in otlg_pct_value_all:
        movie_ids_all.append(movie_id)
        # otlg_value_all.append({otlg_str[i]: pct_value[i] for i in range(len(pct_value))})
        otlg_value_all.append(ast.literal_eval(pct_value))

    # 1. 선택된 staff(배우+감독)로 movie_id 거르기
    otlg_value = []
    movie_ids_by_staff = []
    if len(staff) >= 1:
        filtered_movie_ids = movieInfo.get_ids_by_staff(staff)
    else:
        filtered_movie_ids = []

    for id in filtered_movie_ids:
        otlg_pct_value = otlgValueDB.db_get_ontology_value(1, id)
        if otlg_pct_value:
            otlg_pct_value = ast.literal_eval(otlg_pct_value[0][0])
            movie_ids_by_staff.append(id)
            # otlg_value.append({otlg_str[i]: otlg_pct_value[i] for i in range(len(otlg_pct_value))})
            otlg_value.append(otlg_pct_value)

    ret_json = {"recommend_result": []}
    # 2. ontology 정보와 1번의 staff로 선정된 movie_id 로 최종 영화 선정 후 return
    # 배우, 장르만 선택하고 속성, 장르는 선택하지 않았을 때
    if len(ontologies) == 0:
        key = make_key(staff=staff)
        if len(movie_ids_by_staff) == 0:
            ret_json['recommend_result'].append({key: []})
            return ret_json
        else:
            df_recommendation_result_dict = {key: []}
            ret_list_movie_id, ret_list_names, ret_list_imgs = movieInfo.get_movie_info(movie_ids_by_staff)
            for i in range(len(ret_list_movie_id)):
                return_movie = {"movie_id": str(ret_list_movie_id[i]), "name": ret_list_names[i], "image": ret_list_imgs[i]}
                df_recommendation_result_dict[key].append(return_movie)
            ret_json['recommend_result'].append(df_recommendation_result_dict)
            return ret_json
    # 속성, 장르가 선택되었을 때
    else:
        # 배우, 감독을 선택했지만 조건에 맞는 movie_id는 없을 때
        if len(movie_ids_by_staff) == 0 and len(staff) >= 1:
            key1 = make_key(staff=staff, ontologies=ontologies)
            key2 = make_key(staff=staff)
            ret_json['recommend_result'].extend([{key1: []}, {key2: []}])
        # 배우, 감독으로 movie_id 있을 때
        elif len(movie_ids_by_staff) >= 1:
            print("==== result with STAFF", staff, "MOVIE", movie_ids_by_staff)
            # do_recommendation_otlg -> check_gap 옵션 추가 가능
            # (1: gap으로 2차 정렬함, 0: 2차 정렬 없이 수치 간 합으로 1차 정렬만 함), 디폴트=1)
            key = make_key(staff=staff, ontologies=ontologies)
            if len(ontologies) >= 2:
                key_otlg = make_key(staff=staff, ontologies=ontologies, start_idx=1)
                df_recommendation_result = do_recommendation_otlg(ontologies, otlg_value, movie_ids_by_staff, movie_ids, key_otlg)
            else:
                df_recommendation_result = do_recommendation_otlg(ontologies, otlg_value, movie_ids_by_staff, movie_ids)
            df_recommendation_result_dict = get_result_dict(df_recommendation_result, key, movieInfo)
            ret_json['recommend_result'].append(df_recommendation_result_dict)

            key = make_key(staff=staff)
            df_recommendation_result_dict = get_result_dict(movie_ids_by_staff, key, movieInfo, 0)
            ret_json['recommend_result'].append(df_recommendation_result_dict)

        # 배우, 감독 선택 안 했을 때
        key = make_key(ontologies=ontologies)
        df_recommendation_result = do_recommendation_otlg(ontologies, otlg_value_all, movie_ids_all, movie_ids, key)
        df_recommendation_result_dict = get_result_dict(df_recommendation_result, key, movieInfo)
        ret_json['recommend_result'].append(df_recommendation_result_dict)

        # 속성, 장르를 여러 개 선택했을 경우 각 온톨로지 별로 데이터 추가
        if len(ontologies) >= 2:
            for otlg in ontologies:
                df_recommendation_result = do_recommendation_otlg([otlg], otlg_value_all, movie_ids_all, movie_ids)
                df_recommendation_result_dict = get_result_dict(df_recommendation_result, otlg, movieInfo)
                ret_json['recommend_result'].append(df_recommendation_result_dict)

        print('==== result ret_json:\n')
        print(ret_json)
        return ret_json


@app.route('/user_otlg/recommendation', methods=['GET'])
def user_otlg_recommendation():
    '''
    사용자 취향 영화에서 최상위 온톨로지 2개 추출, 유사영화 2편 추출하여 리턴
    :return: ret_json = {"status": bool(),
                        "recommend_result": [
                         {"ontology": ['마블', '로맨스', '애니메이션', ...]},
                         {"movies": ['12345', '23456', ...]}
                         ],
                         "error_msg": ""}
    '''
    print('\n\nurl user_otlg_recommendation', request.args)

    user_id = request.args.get('user_id', default='ko')
    ret_json = {"status": "", "recommend_result": [{"ontology": []}, {"movies": []}], "error_msg": ""}

    user_db = UserValueDB()
    make_user_data = MakingUserData()

    user_val = user_db.db_get_user_value(user_id)
    print(f"user {user_id}'s value in DB:", user_val)
    movie_ids = user_val[-3]

    if movie_ids and movie_ids != '[]' and type(movie_ids) == str:
        movie_ids = movie_ids.replace('[', '')
        movie_ids = movie_ids.replace(']', '')
        if bool(movie_ids.strip()) == True:
            movie_ids = movie_ids.split(',')
            ontology = make_user_data.get_ontology(movie_ids)
            ontology_set = set()
            ret_ontology = []
            for otlg, val in ontology:
                if otlg not in ontology_set:
                    ontology_set.add(otlg)
                    ret_ontology.append([otlg, val])
                    print('ret_ontology', ret_ontology)
                else:
                    index = [ret_ontology.index(a) for a in ret_ontology if otlg in a][0]
                    ret_ontology[index][1] += val
            ret_json['status'] = "True"
            ret_json["recommend_result"][0]['ontology'] = ret_ontology
            ret_json["recommend_result"][1]['movies'] = make_user_data.recommend_movie_by_userdata(movie_ids, ontology)['movies']
            print("\nret_json:", ret_json)
            return ret_json
    else:
        print("ERROR, 사용자 취향의 영화를 불러올 수 없습니다.")
        ret_json['status'] = "False"
        ret_json['error_msg'] = "사용자 취향의 영화를 불러올 수 없습니다."
        return ret_json


@app.route('/user/login', methods=['POST'])
def user_login():
    print('\n\nuser_login')
    user_id = request.args.get('user_id')
    passwd = request.args.get('passwd')
    print('user_id', user_id, 'password', passwd)
    ret_json = {"ret": "", "msg": None}

    userDB = UserValueDB()
    # 위에서 connection OK 여부 확인하고
    if userDB.db_status == True:
        exists = userDB.db_check_existence_user_value(user_id)
    else:
        exists = False
        ret_json["msg"] = "DB가 연결되지 않습니다."

    if exists == str(True):
        ret_json["ret"] = True
    elif exists == str(False):
        ret_json["ret"] = False
        ret_json["msg"] = "등록된 아이디가 없습니다."
    userDB.db_close()
    print("ret_json", ret_json)

    return ret_json


@app.route('/user/signup/get_id', methods=['GET'])
def user_signup_get_id():
    print('\n\nuser_signup_get_id')
    color = ['red', 'yellow', 'green', 'blue', 'black', 'white', 'gray', 'orange',
             'blue', 'cyan', 'violet', 'pink', 'brown', 'grape', 'indigo', 'teal', 'lime']
    animal = ['lion', 'elephant', 'penguin', 'dog', 'kitten', 'cat', 'wolf', 'dolphin', 'tiger',
              'octopus', 'bear', 'rabbit', 'puppies', 'fox', 'deer', 'owl', 'meerkat', 'panda']
    ret_json = {"ret": "", "msg": None, "id": ""}
    userDB = UserValueDB()

    if userDB.db_status == True:
        while True:
            random_id = str(random.sample(color, 1)[0]) + '_' + str(random.sample(animal, 1)[0]) + '_' + str([random.randrange(1, 100)][0])
            exists = userDB.db_check_existence_user_value(random_id)
            if exists == str(False):
                ret_json["ret"] = True
                ret_json['id'] = random_id
                break
    else:
        ret_json["ret"] = False
        ret_json["msg"] = "DB가 연결되지 않습니다."
    userDB.db_close()
    print("ret_json", ret_json)

    return ret_json


@app.route('/user/signup', methods=['POST'])
def user_signup():
    print('\n\nuser_signup')
    user_id = request.args.get('user_id')
    passwd = request.args.get('passwd')
    age = request.args.get('age', default='')
    gender = request.args.get('gender', default='')
    print('user_id', user_id, 'password', passwd)
    ret_json = {"ret": "", "msg": None}

    userDB = UserValueDB()
    # 위에서 connection OK 여부 확인하고
    if userDB.db_status == True:
        exists = userDB.db_check_existence_user_value(user_id)
    else:
        ret_json["ret"] = False
        ret_json["msg"] = "DB가 연결되지 않습니다."

    if exists == str(False):
        userDB.db_insert_user_value(user_id, passwd, age=age, gender=gender)
        ret_json["ret"] = True
    elif exists == str(True):
        ret_json["ret"] = False
        ret_json["msg"] = "아이디가 이미 등록되어 있습니다.\n다른 아이디를 입력해주세요."
    userDB.db_close()
    print("ret_json", ret_json)
    return ret_json


@app.route("/user/taste/get_movies", methods=["GET"])
def user_taste_get_movies():
    print('\n\nuser_taste_get_movies')
    cnt = request.args.get('count', default=20)
    original_ids = request.args.get('movie_ids', default=[])
    pool_index = request.args.get('pool_index', default='6')
    pool_type = request.args.get('pool_type', default='n')
    lang = request.args.get('lang', default='ko')

    movie_ids = get_random_movie_by_genre(int(cnt), original_ids)
    movieInfo = MovieInfo(pool_index, pool_type, lang)
    ret_list_movie_id, ret_list_names, ret_list_imgs = movieInfo.get_movie_info(movie_ids)
    get_movies_result = {"movie_ids": ret_list_movie_id, "movie_names": ret_list_names, "movie_imgs": ret_list_imgs}

    return get_movies_result


@app.route("/user/taste/update", methods=["GET"])
def user_taste_update():
    print('\n\nuser_taste_update')
    user_id = request.args.get('user_id')
    movie_ids = request.args.get('movie_ids', default=[]).split(',')
    scores = request.args.get('scores', default=[]).split(',')
    print('user_id:', user_id, 'movie_ids:', movie_ids)
    ret_json = {"ret": "", "msg": None}

    userDB = UserValueDB()
    # 위에서 connection OK 여부 확인하고
    if userDB.db_status == True:
        existence = userDB.db_check_existence_user_value(user_id)
    else:
        ret_json["ret"] = False
        ret_json["msg"] = "DB가 연결되지 않습니다."

    if existence == str(True):
        original_data = userDB.db_get_user_value(user_id)[-1]
        print("original_data", type(original_data), original_data)
        if original_data != '[]':
            original_data = original_data.replace('[', '')
            original_data = original_data.replace(']', '')
            movie_ids_total = movie_ids
            if bool(original_data.strip()) == True:
                original_data = original_data.split(',')
                movie_ids_total.extend(original_data)
        else:
            movie_ids_total = movie_ids
        print("movie_ids_total", movie_ids_total)
        movie_ids_total = list(map(int, movie_ids_total))
        if scores:
            userDB.db_insert_rating_value(user_id, movie_ids_total, scores)
        userDB.db_update_movie_ids(user_id, movie_ids=movie_ids_total)
        ret_json["ret"] = True
    userDB.db_close()
    return ret_json


# 메타데이터 랜덤하게 뽑아서 반환하는 함수
@app.route("/random-metadata", methods=["GET"])
def random_metadata():
    from vod_common.ontology_pool import get_random_meta
    ret_json = {'status': False, 'metaList': []}

    meta_list = get_random_meta()

    if len(meta_list) > 0:
        ret_json["status"] = True
    ret_json["metaList"] = meta_list
    print('json>>>', ret_json)
    return ret_json


if __name__ == '__main__':
    CORS(app)
    app.run(host='localhost', port='8888', debug=True)
