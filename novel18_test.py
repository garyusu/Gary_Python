from bs4 import BeautifulSoup as bs
from flask import g
import requests
import re

def connect():
    url = "https://novel18.syosetu.com/n8190hm/" 
    cookie = '_ga=GA1.2.2119806991.1639036262; over18=yes; ks2=amh1ad1bqbr; sasieno=0; lineheight=0; fontsize=0; novellayout=0; fix_menu_bar=1; autologin=1997094<>2555dc56b585055f3875535e55b44d784259e15d045c43de68492b5bd716da67; nlist3=14rtk.5-14qmt.k-14r7p.0-pszu.5-dzol.d-rz2h.10; _pbjs_userid_consent_data=3524755945110770; cto_bidid=KTq1xl9XWW5ncXZLR25SRWR4OWd5RUpLUG02S0R5QXFQRmdNSCUyRiUyQk10UFJkNERGTjBEZEhrRWdwRWNuSllCWFNRUXVMWmFOOWtZYmVtU2lEbXFNNDh2ckthSXhBNGNpUHE1ZW9CRUFGR3VPRkg4UmslM0Q; cto_bundle=1DYnUV9OcTUyOTdVSEdmYUZGWXE4TFRwOVBFeWJReEdwbU96TlkxamdFU0ZxMDRpMWU2WGZ3eHhjSHBNcm1vbGx4ZkclMkZwaG5zYjhpazdHR3p3ZTdHUFBxN2VqUjFYRHNNU21KTmRFZ094NjNOM0w1Y05mJTJCZG5xM1dzdW15a0p0Ym1hR1c4QzgzeHNMOTJrQWRqdFd5dG5wUFV3JTNEJTNE; ses=94e2slt4j5tlaq2fnlg63srlbr'
    headers={ #可能需改動項目2
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br', 
        'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Host': 'novel18.syosetu.com', #不用改
        'Cookie':cookie,
        'Upgrade-Insecure-Requests':'1',#不用改
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }  

    request = requests.get(url=url, headers=headers)
    if request.status_code != 200:
        print("連接失敗")
    
    soup = bs(request.text,"html.parser")
    novel_list = soup.select('.index_box')
    # ch = isRuby(str(ch)) #回傳string
    ch1 = remove_tag(str(novel_list))
    print(novel_list[0].contents)

#將字串註解內的強調符號"・"進行重組換位
def reDot(text): 
    text_search = re.search(r'(\(・+?\))+',text,re.I) #非貪婪匹配 (・・)，目前只能匹配一次
    t_start_index = text_search.start() #取得起始索引
    st = "" #放重組字串
    for i in text[:t_start_index]: #逐字取出並重新組字串
        st += i +"・"   #動・揺・
    st += text[t_start_index:]
    st = re.sub(r'(\(・+?\))+',"",st) #最後將(・・)消除
    return st

#消除<Tag>及強調符(・・) *?非貪婪匹配
def remove_tag(text): 
    text = re.sub(r'<.*?>',"",text)
    text = re.sub(r'\((・+?)\)',"",text)
    return text

if __name__ == "__main__":
    connect()