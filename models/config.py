import os

BASE_PATH = os.path.dirname(__file__)

BAIDU_STOPWORDS_PATH = os.path.join(BASE_PATH, r'data\stopwords\baidu_stopwords.txt')
CN_STOPWORDS_PATH = os.path.join(BASE_PATH, r'data\stopwords\cn_stopwords.txt')
HIT_STOPWORDS_PATH = os.path.join(BASE_PATH, r'data\stopwords\hit_stopwords.txt')
SCU_STOPWORDS_PATH = os.path.join(BASE_PATH, r'data\stopwords\scu_stopwords.txt')

CORPUS_PATH = os.path.join(BASE_PATH, r'data\movie_info')
# CACHE_PATH = os.path.join(BASE_PATH, r'data\tfidf_cache.pkl')