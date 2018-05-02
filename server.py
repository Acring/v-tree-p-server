from gensim import corpora
from flask import *
from gensim import models
import os
import logging
from werkzeug.datastructures import Headers
from controller.translate import traslate
from flask_script import Manager

test_model = None
test_dictionary = None


class MyResponse(Response):

    def __init__(self, response=None, **kwargs):
        kwargs['headers'] = ''
        headers = kwargs.get('headers')
        # 跨域控制
        origin = ('Access-Control-Allow-Origin', '*')
        methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
        if headers:
            headers.add(origin)
            headers.add(methods)
        else:
            headers = Headers([origin, methods])
        kwargs['headers'] = headers
        super(MyResponse, self).__init__(response, **kwargs)

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(MyResponse, cls).force_type(rv, environ)

app = Flask(__name__)
manager = Manager(app)
app.config['JSON_AS_ASCII'] = False
app.response_class = MyResponse


@app.route('/')
def hello_vtree():
    return 'Hello V-Tree'


@app.route('/test/word/similar', methods=['GET'])
def req_test_model():
    """
    查询测试训练模型返回对应的相似度
    """
    global test_model

    word = request.args.get('word')
    if not word:
        return 'no word to query'
    if test_model:
        try:
            data = test_model.wv.most_similar(word, topn=10)
            return {'code': 1000, 'data': data}
        except Exception as e:
            return {'code': 1001, 'msg': '单词未收录:{}'.format(e)}
    return {'code': 404, 'msg': '测试模型为空'}


@app.route('/test/word/info', methods=['GET'])
def req_test_dic():
    """
    查询词的出现频率
    :return:
    """

    word = request.args.get('word')
    global test_dictionary
    try:
        word_index = test_dictionary.token2id[word]
        count = test_dictionary.dfs[word_index]

        data = {
            'index': word_index,
            'count': count,
            'freq': test_dictionary.dfs[word_index] / test_dictionary.num_docs
        }
        return {'code': 1000, 'data': data}
    except Exception as e:
        return {'code': 1001, 'msg': '单词不存在:{}'.format(e)}


@app.route('/test/word/trans', methods=['GET'])
def req_test_trans():
    """
    查询词的意思
    :return:
    """
    word = request.args.get('word')
    fb = traslate(word)
    return {'code': 1000, 'data': fb}


def load_test_model(model_name):
    """
    加载测试模型
    """
    global test_model
    logging.info('loading model')
    try:
        test_model = models.Word2Vec.load(os.path.join('.', 'model', model_name))
        print(test_model)
    except Exception as e:
        logging.error("加载模型失败:{}".format(e))
        return


def load_test_dic(dic_name):
    """
    加载测试词库
    """
    global test_dictionary
    logging.info('loading dictionary')
    try:
        test_dictionary = corpora.Dictionary.load(os.path.join('.', 'dictionary', dic_name))
        print(test_dictionary)
    except Exception as e:
        logging.error("加载词库失败:{}".format(e))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    load_test_model('sub')
    load_test_dic('test')
    manager.run()
    app.run(debug=True)
