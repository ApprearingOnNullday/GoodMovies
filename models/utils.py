import jieba
import logging
from models.config import *
import os
import pickle

jieba.setLogLevel(logging.INFO)

# 停用词表
def get_stopwords():
    stopwords1 = [line.strip() for line in open(CN_STOPWORDS_PATH,encoding="utf-8").readlines()]
    stopwords2 = [line.strip() for line in open(HIT_STOPWORDS_PATH, encoding="utf-8").readlines()]
    stopwords3 = [line.strip() for line in open(BAIDU_STOPWORDS_PATH, encoding="utf-8").readlines()]
    stopwords4 = [line.strip() for line in open(SCU_STOPWORDS_PATH, encoding="utf-8").readlines()]
    stopwords_others = ["•","\n"]
    stopwords = stopwords1 + stopwords2 + stopwords3 + stopwords4 + stopwords_others
    return stopwords

# 分词&去停用词
def text_cut(text):
    words = []
    # 加载停用词
    stopwords = get_stopwords()
    # jieba搜索引擎分词模式lcut
    for word in jieba.lcut_for_search(text):
        if word not in stopwords:
            words.append(word)
    return words

# 以二进制形式缓存到文件
def dump_cache(object, path):
    pickle.dump(object, open(path, "wb"))

# 从文件中读取内容
def load_cache(path):
    return pickle.load(open(path, "rb"))

if __name__ == '__main__':
    # print(text_cut("我爱北京的天安门。"))
    # print(get_stopwords())
    # dump_cache(({'a':1}, [{'b':2}]), './data/cache/test.pkl')
    print(load_cache("./data/cache/test.pkl"))