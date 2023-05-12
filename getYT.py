import requests
import re
import json

def getResponse(url):
    headers = {}
    cookie = {}
    response = requests.get(url)
    with open('getResponse.txt', 'a', encoding="utf-8") as f:
        f.truncate(0)
        f.write("清空過了")
        f.write(response.text)
    # print('回傳結果：')
    return response.text
def textProcess(t):
    m = re.search('"url":".*?"', t)
    print (m)

if __name__ == '__main__':
    #要前往的頁面
    url = 'https://www.youtube.com/watch?v=qru0X91U4qQ'
    t = getResponse(url)
    textProcess(t)