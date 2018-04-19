#! coding=utf-8


"""
词典训练器
"""
import csv
import os

import logging
from gensim import corpora
from iterator.iterator import WikiIterator, TextIterator
from pyecharts import Line


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
            logging.debug(line)
            documents.append(line)
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
            documents.append(line)
            if len(documents) == 10:
                count += 1
                print('document #{}', count * 10)
                new_dic = corpora.Dictionary(documents)
                dic.merge_with(new_dic)
                documents = []

        dic.save(os.path.join('..', 'dictionary', 'test'))


def train_test():
    iterator = TextIterator('wiki_chinese_preprocessed.simplied.txt', 'COCA20000.csv')
    trainer = DicTrainer(iterator)
    trainer.test_trainer()


def train_wiki():
    iterator = WikiIterator(lex_name='COCA20000.csv')
    trainer = DicTrainer(iterator)
    trainer.wiki_trainer()


def test_wiki():
    dic = corpora.Dictionary().load(os.path.join('..', 'dictionary', 'enwiki'))

    print(len(dic))
    # 按词出现文档的次个数对词进行排序
    while True:

        word = input()
        try:
            # 获取某个词的id
            id = dic.token2id[word]
            print('id:{}'.format(id))

            # 用id获取某个词
            print(dic[id])

            # 用id获取几个文档中出现过这个词
            print(dic.dfs[id])
            print(dic.dfs[id]/dic.num_docs)
        except KeyError as e:
            print('不存在单词: {}'.format(e))


def test_by_lexicon(lex_name, dic_name):
    with open(os.path.join('..', 'lexicon', lex_name)) as f:
        dic = corpora.Dictionary.load(os.path.join('..', 'dictionary', dic_name))
        f_csv = csv.reader(f)

        for row in f_csv:
            word = row[1]
            try:
                wid = dic.token2id[word]
                print('id:{}, word:{}, dfs:{}, freq:{}'.format(wid, word, dic.dfs[wid], dic.dfs[wid]/dic.num_docs))
            except KeyError as e:
                print('word: {} 未被统计到'.format(word))

        # for x in dic:
        #     print(dic[x])


def chart_by_lexicon(lex_name, dic_name, title):
    with open(os.path.join('..', 'lexicon', lex_name)) as f:
        dic = corpora.Dictionary.load(os.path.join('..', 'dictionary', dic_name))
        f_csv = csv.reader(f)
        sorted_dic = sorted(dic.dfs.items(), key=lambda x: x[1], reverse=True)[1000:2000]
        line = Line(title)
        line.add("词频分布", [dic[word[0]] for word in sorted_dic], [word[1]/dic.num_docs for word in sorted_dic], is_smooth=True)
        line.render(os.path.join('..', 'charts', title+'.html'))

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    test_by_lexicon('COCA20000.csv', 'enwiki')
