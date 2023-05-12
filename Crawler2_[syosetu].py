import turtle
import requests  #用於get請求
from bs4 import BeautifulSoup as bs #網頁分析
from os import mkdir #建資料夾(目錄)
from os import rename
url = "https://syosetu.org/novel"   #俺の妹が最高のオカズだった 主頁

cookie = 'over18=off'

headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'dnt': '1',
    # ':authority': 'syosetu.org',
    # ':path': '/novel/264928/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'cookie':cookie
}  

#字串替換 str_n_set(str, s, number) 將字串str的前number個字元 替換為s字元
def str_n_set(str, s, n):
    return s*n + str[n:]

def get_novel(url): 
    novel_id = '/264928/' #小說連結編號
    url_all = url + novel_id
    req = requests.get(url_all, headers = headers)
    soup = bs(req.text, "html.parser")
    # print(soup)
    if req.status_code != 200:
        print("連接失敗")
    
    novel_list = soup.select('a[style="text-decoration:none;"]') #tag章節連結
    a = 1 #檔案開頭編號，初始為 1
    novel_title = soup.select("span[itemprop='name']")#tag小說標題
    novel_writerName = soup.select('a[href="//syosetu.org/user/363705/"]') #tag作者名
    dirName = '[日]['+ novel_writerName[0].text +']'+ novel_title[0].text.replace(" ","　")   #資料夾名
    mkdir(dirName)#於工作區內建新資料夾
        
    #章節內文寫入
    for nl in novel_list:
        url_href = url_all + str_n_set(nl['href'], "", 2) #章節連結，字串替換前面多出的"."
        # print(url_href)
        r2 = requests.get(url_href, headers = headers)
        r2.encoding = r2.apparent_encoding #轉碼
        soup2 = bs(r2.text , "html.parser").select('.ss #honbun >p') #tag小說內文
        a_str =str(a)+ "-" + nl.text + '.txt' #章節檔名

        with open(dirName + '/' + a_str, 'a', encoding="utf-8") as txt:
            txt.write(nl.text + '\n\n\n') #寫入開頭標題
            for s in soup2:
                if bool(s.contents[0]) ==1:
                    txt.write('('+ s.contents[0] +')')
                txt.write(s.text + '\n')
        txt.close
        a = a + 1
    rename(dirName, dirName + "[更新至"+ str(a) +"]")

if __name__=='__main__':
    get_novel(url)
    print("OVER!!")