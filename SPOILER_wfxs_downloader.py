#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
from requests import get ,post
import os
from tqdm import tqdm
import re

hd = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Origin': 'https://www.wfxs.org',
      'Cookie': 'jieqiVisitTime=jieqiArticlesearchTime%3D1633081170; __gads=ID=4b6211e5d7d98484-22ee8b8c07cc0099:T=1633056199:RT=1633056199:S=ALNI_MZEqD1dROi9gWKE661c4zH7ePggvg; jieqiUserCharset=big5',
      'Content-Length': '45',
      'Accept-Language': 'zh-tw',
      'Host': 'www.wfxs.org',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
      'Referer': 'https://www.wfxs.org/modules/article/search.php',
      'Accept-Encoding': 'gzip, deflate, br',
      'Connection': 'keep-alive'}


# In[6]:


# novel_id = input("請輸入微風小說網的小說完整網址 或 小說代號(https://www.wfxs.org/html/{小說代號}/):")
novel_id = 537294

novel_index_url = "https://www.wfxs.org/html/537294/"
    
index_request = get(novel_index_url)
if index_request.status_code == 200:
    index_request.encoding = index_request.apparent_encoding
    index_bs = bs(index_request.text, 'html.parser')
    store_path = os.path.join(os.getcwd(),index_bs.find("h1").text)
else:
    print("伺服器回應:" + str(index_request.status_code))


# In[ ]:


def get_novel_chapters_list(index_bs) -> list:
    chapters_url_list = []
    chapters_list = index_bs.find_all("dd")
    
    for ch in chapters_list:
        if ch.find('a').text != "" : 
            chapters_url_list.append({'name' : ch.find('a').text, 'url' : "https://www.wfxs.org" + ch.find('a')['href']})
            
    return chapters_url_list


# In[ ]:


def download_novel(chapters_url_list:list, store_path:str):
    if os.path.isdir(store_path) == False : os.mkdir(store_path)
    index = 1
    for i in tqdm(range(len(chapters_url_list))):
        #章節名
        chapter_name = os.path.join(store_path,'{:4d}'.format(index) + '-' + chapters_url_list[i]['name'].replace(' ','-')+'.txt')
        #章節網址
        chapter_url = chapters_url_list[i]['url']
        #get章節request
        chapter_request = get(chapter_url)
        if chapter_request.status_code == 200:
            #網頁轉碼
            chapter_request.encoding = chapter_request.apparent_encoding
            #網頁解析
            chapter_bs = bs(chapter_request.text, 'html.parser')
           
            #選擇內文所在標籤
            # soup2 = bs(r2.text , "html.parser").select('div#novel_honbun') #小說內文

            #正規表達
            # req = chapter_bs.text
            pattern1 = re.compile(r'\n&nbsp;&nbsp;&nbsp;&nbsp;(.*)<br /> <br />')
            result1 = pattern1.findall(chapter_request.text)
            # print(result1)
            # 寫入
            with open(chapter_name,'w',encoding='UTF-8') as file:
                for r in result1:
                    file.write('\n\n')
                    file.write(r)
            file.close()
        index = index + 1


# In[ ]:


def main():
    try:
        chapters_url_list = get_novel_chapters_list(index_bs)
        download_novel(chapters_url_list,store_path)
        print('donwload complete!!')
    except KeyboardInterrupt:
        print('cancel download process')
    finally:
        print('exit process.')


# In[ ]:


if __name__ == '__main__':
    main()

