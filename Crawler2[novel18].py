import requests  #用於get請求
from bs4 import BeautifulSoup as bs #網頁分析
from os import mkdir #建資料夾(目錄)
import re
import os

url = "https://novel18.syosetu.com" #小說18主頁

#可能需改動項目1
cookie = 'over18=yes;'

headers={ #可能需改動項目2
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':'gzip, deflate, br', 
    'Accept-Language':'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5',
    # 'Host': 'ncode.syosetu.com',  #有時會改這個
    # 'Host': 'novel18.syosetu.com', 
    'Cookie':cookie,
    'Upgrade-Insecure-Requests':'1',#不用改
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47'
}  

#從網頁抓取小說
def get_novel(url, novel_id, isFileNum): #傳入(主址,小說編號)
    url_novel = url + novel_id #小說目錄連結

    req = requests.get(url_novel, headers = headers)
    soup = bs(req.text, "html.parser")
    # print(soup)
    if req.status_code != 200:
        print("連接失敗")

    #取得指定標籤 (解析後的網頁Data, CSS選取器規則)
    novel_list = getSoupTag(soup, 'dd.subtitle > a')                    #所有章節節點(<a herf>)
    novel_title = getSoupTag(soup, '.novel_title')                      #小說標題
    po_date = getSoupTag(soup, '.long_update')                          #發文日期
    novel_writerName = getSoupTag(soup, '.novel_writername')[0].text    #作者名
    novel_ex = getSoupTag(soup, '#novel_ex')                            #小說前言
    bigChapter_list = getSoupTag(soup, '.chapter_title')                #大章節名
    bigChapter_firstChild = getSoupTag(soup, '.chapter_title + dl a')   #大章節下第一章
    bigChapter_lastChild = []                                           #大章節最後一章

    #建立小說資料夾
    #資料夾名 若 資料夾名+檔名 太長，可能導致錯誤
    novel_writerName = re.sub(r"[\n(作者：)　]+", "", novel_writerName) #消除多餘的字元
    dirName = "[日][" + novel_writerName +']'+ novel_title[0].text
    
    #指定下載路徑
    # dirName = novel_title[0].text #若 資料夾名+檔名 太長導致錯誤，切換到這個
    dirName = 'C:/Users/garyu/OneDrive/ebook/YD/[成為小說家吧！]/' + toFileName(dirName)
    if not os.path.isdir(dirName): #檢查是否已存在
        mkdir(dirName)#建新資料夾，預設在工作區目錄
    print('小說目錄：\n' + dirName)

    bigChapterPaths = []
    num = 1 #大章節編號
    #大章節
    for chapter in bigChapter_list:
        #找出所有大章節最後一章(=大章上一節點)
        ch = chapter.find_previous_sibling('dl')
        if ch != None:
            bigChapter_lastChild += ch.select('a')    #往下找<a href>，放入陣列
        bigChapterPaths.append(getChapterPath(dirName, num, chapter))
        num += 1
    bigChapter_lastChild.append('')           #因為末尾會少bigChapter_firstChild一個，所以加上空字串
    
    #小說首頁簡介
    with open(dirName + '/' + '0-首頁導言.txt', 'a', encoding="utf-8") as f:
        f.write(remove_tag(str(novel_ex[0])))
    
    isBigChapter = len(bigChapter_list) > 0 #有無大章節
    tmp_dirName = dirName                  
    a = 0 #大章節index，從0開始
    b = 1 #檔案開頭編號
    
    #逐一取得章節
    print('檔名：')
    for nl in novel_list: 
        #有大章節的話，將檔案放到各大章資料夾
        if isBigChapter:
            if bigChapter_firstChild[a].text == nl.text:    #大章第一章
                tmp_dirName = bigChapterPaths[a]
                # print("@@@@@@@"+ bigChapter_firstChild[a].text +" = " +nl.text)
                b = 1   #重置 檔案開頭編號
                
            if bigChapter_lastChild[a] != '':               #大章最後章
                if bigChapter_lastChild[a].text == nl.text:
                    # print("@@@@@@@"+ bigChapter_lastChild[a].text +" = " +nl.text)
                    a+=1
        
        #進章節連結
        url_href = url + nl['href'] #章節連結
        r2 = requests.get(url_href, headers = headers)
        r2.encoding = r2.apparent_encoding #轉碼
        soup2 = bs(r2.text , "html.parser").select('div#novel_honbun') #小說內文

        if isFileNum:
            ch_name = str(b) + '-' + toFileName(nl.text) + '.txt'    #檔名 (加上編號)
        else:
            ch_name = toFileName(nl.text) + '.txt'  #檔名(不加編號)
        print(ch_name)

        with open(tmp_dirName + '/' + ch_name, 'a', encoding="utf-8") as txt:
            txt.write(nl.text + "\t" + po_date[b-1].text + '\n\n\n') #寫入開頭標題
            for s in soup2: #逐行處理
                sr = remove_tag(str(s)) #移除tag
                txt.write(sr + '\n')
        b = b + 1
    os.rename(dirName + '/', dirName + " [更新至" + str(b-1) + ']/')
    print("下載完畢!")


#檢查特殊字元，用全形取代特殊字元，避免不符檔名規則
def toFileName(str):
    str = re.sub(r'^\s+?',"",str) #消除前面空白
    flag = False
    for i in str: #逐一比對
        if i=='\\' or i=='/' or i==':' or i=='*' or i=='?' or i=='<' or i=='>' or i=='|':
            flag = True
    if flag: #替換成全形
        str = str.replace('\\','＼').replace('/','／').replace(':','：')
        str = str.replace('*','＊').replace('?','？').replace('<','＜')
        str = str.replace('>','＞').replace('|','｜')
    return str.replace('―','—')

#消除<Tag>及強調符(・・) *?為非貪婪匹配，小說內文用
def remove_tag(text): 
    text = re.sub(r'<.*?>',"",text)
    text = re.sub(r'\((・+?)\)',"",text)
    return text.replace('―','—')

def get_novel_number(url): #從輸入網址分割出編號部分(正則表達式)
    r = re.search(r"/n\d{4}[A-z]{2}/$", url, re.I)
    return r.group()

#return 大章路徑
def getChapterPath(dirName, num, chapter):
    chapterPath = dirName + '/' + str(num) + "." + toFileName(chapter.text)
    createFolder(chapterPath)
    return chapterPath

#建立大章節資料夾(路徑名, 章節節點)
def createFolder(chapterPath):
    if not os.path.isdir(chapterPath): #檢查是否已存在
        mkdir(chapterPath)#建新資料夾

#取得指定標籤 (解析後的網頁Data, CSS選取器規則)
def getSoupTag(soup ,selectStr):
    return soup.select(selectStr)

if __name__=='__main__':
    #要下載的小說網址
    mainUrl = "https://novel18.syosetu.com/n5513ci/"
    num = get_novel_number(mainUrl) #擷取小說編號
    #章節是否加上編號
    selection = True  
    #開始抓取小說
    get_novel(url, num, selection) 