from models.utils import *
from models.model import *

if __name__ == '__main__':
    # 测试tfiwf模型
    model = TfiwfModel()
    corpus = [
        '我爱北京天安门',
        '天安门上太阳升'
    ]
    model.load_corpus(corpus)
    model.compute_tfiwf_value()
    print(model.all_words)
    print(model.vocab)
    print(model.corpus_words)
    print(model.tflist)
    print(model.iwf_dict)
    print(model.tfiwf_list)