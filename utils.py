import pymysql

from models.config import *
from models.utils import *
from models.model import *
import numpy as np

# 模糊搜索
def fuzzy_search(searchText, topK = 6):
    # 分割检索词
    words = text_cut(searchText)
    # 获得电影语料库、iwf_dict和tfiwf_list
    corpus = []  # 语料库列表
    # 读每个文件，构建语料库
    # for i in range(1, 251, 1):
    #     file_path = os.path.join(CORPUS_PATH, f"top{i}.txt")
    #     with open(file_path, 'r', encoding='utf-8') as file:
    #         content = file.read()  # 读取文件全部内容
    #         corpus.append(content)  # 将内容添加到列表中
    # model = TfiwfModel()
    # model.load_corpus(corpus)
    # # iwf_dict
    # iwf_dict = model.compute_iwf_value()
    # # tfiwf_list
    # tfiwf_list = model.compute_tfiwf_value()
    # 从缓存cache文件中加载:1.语料库列表 2.语料库中所有词的iwf值 3.每篇文档的tfiwf_list
    corpus, iwf_dict, tfiwf_list = load_cache(CACHE_PATH)
    # 筛选检索词中在iwf_dict中的词
    words = [word for word in words if word in iwf_dict.keys()]
    # todo：倒排索引，这步之后去倒排索引中找words在哪些文档中出现
    score_list = []
    # 得到用户检索词于每一篇文档（共250篇）的得分，在score_list中存放
    for tfiwf in tfiwf_list:
        score_list.append(sum([tfiwf.get(word, 0) for word in words]))
    # np.argsort方法得到排序后的索引值(若需要倒序从大到小排序需要用[::-1]) e.g.[7,2,9]用argsort排序后得到[1,0,2]
    # 根据搜索词相关度排序
    ids = [id for id in np.argsort(score_list)[::-1] if score_list[id]!=0]
    # 返回索引值&对应文本内容
    if(len(ids)<topK):
        # return ids[:len(ids)], [corpus[id] for id in ids[:len(ids)]]
        return ids[:len(ids)]
    else:
        # return ids[:topK], [corpus[id] for id in ids[:topK]]
        return ids[:topK]


if __name__ == '__main__':
    ids = fuzzy_search("校园爱情")
    print(ids)
    # 索引值全部+1，方便在数据库中搜索
    ids = [x + 1 for x in ids]
    # 将ids列表中的元素转换为字符串，并用逗号分隔
    ids_str = ', '.join(map(str, ids))
    # 查询对应电影的所有信息
    # 1.连接mysql
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="1234", charset='utf8', db='movies')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 2.发送指令
    sql = ("SELECT * FROM tb_movie WHERE id IN (%s)")
    data = [ids_str]
    cursor.execute(sql,data)
    movie_list = cursor.fetchall()
    print(movie_list)
    # 3.关闭连接
    cursor.close()
    conn.close()