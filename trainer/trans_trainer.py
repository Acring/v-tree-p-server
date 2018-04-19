import os

import requests
import re
import csv

"""
翻译训练器
根据相应的词库去Vocabulary抓取相应的翻译

英英互译: Vocabulary
"""


class TransTrainer:

    def __init__(self, lex_name):
        self.lex_name = lex_name  # lexicon 词库地址

    def run(self):
        with open(os.path.join('..', 'lexicon', self.lex_name)) as f:
            f_csv = csv.reader(f)
            for row in enumerate(f_csv):
                word = row[2]

    @staticmethod
    def _get_short(html, word):
        """
        获取词的简介
        :param html: 爬取下的HTML
        :param word: 搜索的词，用于替换
        :return: string 词的简介
        """
        p = re.findall('<p class="short">(.*?)</p>', html)
        if not len(p):
            return None

        clean_i = re.compile(r'(<i>.*?</i>)')
        short = re.sub(clean_i, word, p[0])

        return short

    @staticmethod
    def _get_long(html, word):
        """
        获取词的长介绍
        :param html: 爬取下的HTML
        :param word: 搜索的词，用于替换
        :return: string 词的长介绍
        """
        p = re.findall('<p class="long">(.*?)</p>', html)
        if not len(p):
            return None

        clean_i = re.compile(r'(<i>.*?</i>)')
        long = re.sub(clean_i, word, p[0])

        return long


if __name__ == '__main__':
    trans_trainer = TransTrainer('COCA20000.csv')
    trans_trainer.run()
