# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time
# from imp import reload

# reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '665d9b1112ef69e7' #您的应用ID
APP_SECRET = 'LZtqtbJMdpEGr12zu2KbUxoEOLYoNA0F'#您的应用密钥


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


#官方幫助說明
#https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html
def connect(txt):
    q = txt #待输入的文字

    data = {} 
    data['from'] = 'ja'#源语言
    data['to'] = 'zh-CHT'#目标语言
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET #簽名字串
    sign = encrypt(signStr) 
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    # data['vocabId'] = "您的用户词表ID"

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        millis = int(round(time.time() * 1000))
        filePath = "D:/myProject/GitHub/garyusu" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
    else:
        return response.json()['translation']

def write():
    with open("D:/myProject/GitHub/garyusu/garyusu_Github/test.txt", 'a+', encoding="utf-8") as f:
        readF = f.readlines()
        print(readF)
        # for line in f.readline():
            # readline = line.strip() #刪除頭尾空白字符
            # connect(readline) #回傳翻譯好的字串
            # print(type(line))
            # print(line)
            # f.write() #寫入

if __name__ == '__main__':
    write()