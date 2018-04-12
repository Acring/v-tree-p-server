#! coding=utf-8


"""
词典训练器
"""
import os

import logging
from gensim import corpora
from cleaner.cleaner import WikiIterator, TextIterator


class DicTrainer:
    main_dic = corpora.Dictionary()

    def __init__(self, iterator):
        self.iterator = iterator

    def wiki_trainer(self):
        dic = None
        documents = []
        document = []
        count = 0
        for line in self.iterator:
            if not len(line):
                continue
            if len(line) == 1:
                if document:
                    documents.append(document)
                    document = []
                document.append(line[0])
            if len(line) != 1:
                document.extend(line)
            if len(documents) == 10:
                count += 1
                logging.info('at documents #{}'.format(count * 10))
                dic = corpora.Dictionary(documents)
                self.main_dic.merge_with(dic)
                documents = []
        self.main_dic.save(os.path.join('..', 'dictionary', 'enwiki'))

    def test_trainer(self):
        dic = corpora.Dictionary()
        documents = []
        count = 0
        for line in self.iterator:
            documents.append(line.split(" "))
            if len(documents) == 10:
                count += 1
                print('document #{}', count * 10)
                new_dic = corpora.Dictionary(documents)
                dic.merge_with(new_dic)
                documents = []

        dic.save(os.path.join('..', 'dictionary', 'test'))


def train_test():
    iterator = TextIterator('wiki_chinese_preprocessed.simplied.txt')
    trainer = DicTrainer(iterator)
    trainer.test_trainer()


def train_wiki():
    iterator = WikiIterator()
    trainer = DicTrainer(iterator)
    trainer.wiki_trainer()


def test_wiki():
    dic = corpora.Dictionary.load(os.path.join('..', 'dictionary', 'test'))
    print(len(dic))
    # 按词出现文档的次个数对词进行排序
    while True:
        word = input()

        # 获取某个词的id
        id = dic.token2id[word]
        print('id:{}'.format(id))

        # 用id获取某个词
        print(dic[id])

        # 用id获取几个文档中出现过这个词
        print(dic.dfs[id])
        print(dic.dfs[id]/len(dic))

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    test_wiki()
