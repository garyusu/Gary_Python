import requests  #用於get請求
from bs4 import BeautifulSoup as bs #網頁分析
import re

def get_info(info_id): #傳入 
    url = "http://www.getchu.com/soft.phtml?id=" + info_id #Getchu
    
    #可能需改動項目1
    cookies = {'getchu_adalt_flag' : 'getchu.com'}
    #http://www.getchu.com/soft.phtml?id=224365

    headers={ #默認
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Upgrade-Insecure-Requests':'1',#不用改
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
        # 'Connection': 'keep-alive' #保持連接用
    }  
    req = requests.get(url, headers=headers, cookies=cookies, verify=False)
    soup = bs(req.text, "html.parser")
    # print(soup)
    if req.status_code != 200:
        print("連接失敗")

    painter_name = soup.select('td:contains("原画：") + td')[0].text
       
        
    return painter_name

def get_info_number(url): #從輸入網址分割出編號部分(正則表達式)
    r = re.search(r"\d+$", url, re.I) #id=後的數字
    return r.group()

game_id = get_info_number("http://www.getchu.com/soft.phtml?id=159901") #取得遊戲編碼
info= get_info(game_id) #取得資訊

if info == False:
    print("NULL")
print(info)