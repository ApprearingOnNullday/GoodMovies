import math
from models.utils import text_cut

class TfiwfModel():
    def __init__(self):
        self.all_words = []     # 语料库所有单词的list
        self.vocab = set()      # 语料库所有单词的set（去重）
        self.corpus_words = []  # 二维的list，每个文档中分完的所有词为一个list
        self.tflist = []        # 一个list，list中每个元素为一个词典，key：单词，value：tf值
        self.iwf_dict = {}      # 语料库中所有词的iwf值，key：词，value：iwf值
        self.tfiwf_list = []    # 一个list，list中每个元素为一个词典，key：单词，value：tfiwf值

    # 参数corpus: 语料库，一个list，每个元素为一个文档中的所有内容
    def load_corpus(self, corpus):
        for text in corpus:
            words = text_cut(text)  # 调用分词&去停用词的text_cut函数
            self.all_words += words
            self.vocab.update(words)
            self.corpus_words.append(words)

    # 计算tf值
    def compute_tf_value(self):
        self.tflist = []    # 一个list，list中每个元素为一个词典，key：单词，value：tf值
        # 每篇文档
        for words in self.corpus_words:
            tf_dict = {}
            # 文档中的每个词
            for word in words:
                tf_dict[word] = words.count(word) / len(words)
            self.tflist.append(tf_dict)

    # 计算iwf值(log(语料库中所有词的个数/某个词在整个语料库中出现的次数))
    def compute_iwf_value(self):
        self.iwf_dict = {}
        N = len(self.all_words)
        for word in self.vocab:
            num = self.all_words.count(word)
            self.iwf_dict[word] = math.log(N/num)
        return self.iwf_dict

    # 计算tfiwf值
    def compute_tfiwf_value(self):
        self.compute_tf_value()
        self.compute_iwf_value()
        self.tfiwf_list = []
        for tf in self.tflist:
            tfiwf = {}
            for word, tfval in tf.items():
                tfiwf[word] = tfval * self.iwf_dict[word]
            self.tfiwf_list.append(tfiwf)
        return self.tfiwf_list