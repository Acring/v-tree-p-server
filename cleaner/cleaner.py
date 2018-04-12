#! coding=utf-8
import os
import nltk
import logging
import bz2file
import re
from nltk.tokenize import word_tokenize
"""
对原始语料库进行数据清理
"""


class TextIterator:
    """
    纯文本文件的读取并返回
    """
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        filename = os.path.join('..', 'raw', self.filename)
        for line in open(filename, 'r', encoding='utf-8'):
            yield line


class WikiIterator:
    """
    维基百科文件夹读取并返回
    """
    file_limit = 100  # 读取的文件数限制 3G

    count = 0
    dirname = 'enwiki'

    def __iter__(self):  # 找到enwiki文件夹下的
        dirname = os.path.join('..', 'raw', self.dirname)
        for root, dirs, files in os.walk(dirname):
            if self.count >= self.file_limit:  # 训练文件数量限制，1个文件1M
                break
            for filename in files:
                if self.count >= self.file_limit:  # 训练文件数量限制，1个文件1M
                    break
                file_path = os.path.join(root, filename)
                self.count += 1
                logging.info('at files {}'.format(self.count))
                for line in open(file_path, 'r', encoding='utf-8'):
                    yield Cleaner.wiki_cleaner(line)


class Cleaner:
    """
    数据清理
    """
    @staticmethod
    def wiki_cleaner(line):

        def clean_html(raw_html):  # 清除纯HTML中的<标签>
            cleaner = re.compile('<.*?>')
            cleantext = re.sub(cleaner, ' ', raw_html)
            return cleantext
        """
        维基百科文件夹清理
        """
        sline = line.strip()
        if sline != '':
            rline = clean_html(sline)
            tokenized = word_tokenize(rline)
            sentence = [word.lower() for word in tokenized if word.isalpha()]
            return sentence
        return []


