import pandas as pd
from models.config import *
from models.model import *
from models.utils import *
import os

# todo:后期为优化检索处理速度可以搞一个缓存
def compute_tfiwf_save():
    corpus = [] # 语料库列表
    # 读每个文件，构建语料库
    for i in range(1, 251, 1):
        file_path = os.path.join(CORPUS_PATH, f"top{i}.txt")
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # 读取文件全部内容
            corpus.append(content)  # 将内容添加到列表中
    model = TfiwfModel()
    model.load_corpus(corpus)
    model.compute_tfiwf_value()
    # 获取属性
    iwf_dict = model.iwf_dict
    tfiwf_list = model.tfiwf_list
    # 缓存文件
    dump_cache((corpus, iwf_dict, tfiwf_list), CACHE_PATH)
    # # 返回语料库、iwf_dict以及计算的tfiwf值list
    # return corpus, model.compute_iwf_value(), model.compute_tfiwf_value()

if __name__ == '__main__':
    # corpus, iwf_dict, tfiwf_value_list = compute_tfiwf_save()
    # print(corpus)
    # print(iwf_dict)
    # print(tfiwf_value_list)
    compute_tfiwf_save()