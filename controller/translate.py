import hashlib
import random

import requests

https_url = "https://openapi.youdao.com/api"  # Api的https地址
app_key = "7e7bda78ce50ca93"  # 应用ID
secret_key = "MKtBIvokcWPawPa0eBazUPBYb9VYoq3h"  # 应用密钥
api_docs = "http://ai.youdao.com/docs/api.s#"  # 有道翻译api和说明文档
language = {  # 语言转换表
    "zh-CHS": "中文",
    "ja": "日文",
    "EN": "英文",
    "ko": "韩语",
    "fr": "法语",
    "ru": "俄语",
    "pt": "葡萄牙",
    "es": "西班牙文"
}


# 生成md5签名
def to_sign(q, salt):
    """
    签名要进行UTF-8编码(否则中文无法翻译)
    :param q: 翻译文本
    :param salt: 随机数
    :return: sign: md5签名
    """
    sign = app_key + q + salt + secret_key
    m = hashlib.md5()
    m.update(sign.encode('utf-8'))
    sign = m.hexdigest()
    return sign


# 生成api_url
def get_api_url(sign, salt, q="Hello World", from_lan="auto", to_lan="auto"):
    api_url = "{}?q={}&sign={}&from={}&to={}&appKey={}&salt={}".format(https_url, q, sign, from_lan, to_lan, app_key, salt)
    return api_url


def traslate(word):
    salt = str(random.randint(12345, 56789))
    sign = to_sign(salt=salt, q=word)
    api_url = get_api_url(q=word, sign=sign, salt=salt, from_lan='auto', to_lan='auto')
    translation = requests.get(api_url)
    print(translation.json())
    if not translation:
        return None
    return translation.json()
