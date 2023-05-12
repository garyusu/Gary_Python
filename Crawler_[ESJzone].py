import requests  #用於get請求
from bs4 import BeautifulSoup as bs #網頁分析

url = "https://www.esjzone.cc/detail/1602082116.html"
cookie = 'hidden=value; _ga=GA1.2.679718639.1625623412; hidden=value; 1632454042=1632454042.9163613319; _gid=GA1.2.1684305679.1632622967; e_token=c47dce5bc1aFXVLjpOYF1zqtY3SGjYejpRox9aR2vffqEmzCGdpjVAVdBXK3tNJz2Dg-SRWflDoNSCJm4my8fxzzqZ06eXmTAX6Yn3CpG1AJZPtp2_ZcWLkTACDrA; last_visit_post=128496; last_visit_code=1602082116; _gat=1'

headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cookie':cookie,
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}  


def get_novel(url):
    req = requests.get(url, headers = headers)
    soup = bs(req.text, "html.parser")
    
    if req.status_code != 200:
        print("連接失敗")
    div_list = soup.select('div#chapterList') #整個目錄頁面

    for ele in div_list[0]:
        if ele.name == 'a':
            r2 = requests.get(ele['href'], headers = headers)
            r2.encoding = r2.apparent_encoding
            soup2 = bs(r2.text , "html.parser").select('div.forum-content.mt-3 > p')
            a_str = ele.text + '.txt' #小說檔名
            with open(a_str, 'a',encoding="utf-8") as txt:
                for s in soup2:
                    txt.write(s.text + '\n')
            txt.close
get_novel(url)
print("OVER!!")