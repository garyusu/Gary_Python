from time import sleep
from turtle import color
import requests  #用於get請求
from bs4 import BeautifulSoup as bs #網頁分析
from os import mkdir #建資料夾(目錄)
import subprocess   #打開資料夾
import shutil       #刪除資料夾及內容

import tkinter as tk
import re
import os
import os.path
import unicodedata

from decimal import Decimal #處理小數位計算，避免float產生誤差


url = "https://novel18.syosetu.com" #小說18主頁

#可能需改動項目1
cookie = 'over18=yes;'

headers={ #可能需改動項目2
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    # 'Accept-Encoding':'gzip, deflate, br', 
    # 'Accept-Language':'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5',
    # 'Host': 'ncode.syosetu.com',  #有時會改這個
    # 'Host': 'novel18.syosetu.com', 
    'Cookie':cookie,
    'Upgrade-Insecure-Requests':'1',#不用改
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42'
}  

#從網頁抓取小說
def get_novel(url, novel_id): #傳入(主址,小說編號)
    url_novel = url + novel_id #小說目錄連結

    try:
        req = requests.get(url_novel, headers = headers)
    except Exception as e:
        print("連接失敗 => ", e)
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
    novel_dirName = toFileName( "[日][" + novel_writerName +']'+ novel_title[0].text )
    
    #指定下載路徑
    folderName = ''
    if 'ncode' in url:  # 成為小說家吧！ 
        folderName = '[成為小說家吧！]'
    else:               # 夜曲小說 網址包含'novel18'
        folderName = '[夜曲小說]'
    
    # 指定根目錄 [成為小說家吧！]／[夜曲小說] 下
    rootDir = 'C:/Users/garyu/OneDrive/ebook/YD/'+ folderName
    # dirName = novel_title[0].text #若 資料夾名+檔名 太長導致錯誤，切換到這個
    dirName = rootDir +'/'+ novel_dirName  +" [更新至" + str(len(novel_list)) +']'
    
    # 先將舊的小說資料夾改名，等後續建立新的後再移除 (欲查找的目錄, 關鍵字)
    rename_folders_with_keyword( rootDir, toFileName( novel_title[0].text ) )
    
    if not os.path.isdir(dirName): #檢查是否已存在
        mkdir(dirName)#建新資料夾，預設在工作區目錄
    print('\n小說目錄：\n' + dirName)

    bigChapterPaths = []
    num = 1 #大章節編號

    ##大章節##
    for chapter in bigChapter_list:
        #找出所有大章節最後一章(=大章上一節點)
        ch = chapter.find_previous_sibling('dl')
        if ch != None:
            bigChapter_lastChild += ch.select('a')    #往下找<a href>，放入陣列
        bigChapterPaths.append(getChapterPath(dirName, num, chapter))
        num += 1
    bigChapter_lastChild.append('')           #因為末尾會少bigChapter_firstChild一個，所以加上空字串
    
    #小說首頁簡介
    with open(dirName + '/' + '0-首頁導言.txt', 'w', encoding="utf-8") as f:
        f.write(remove_tag(str(novel_ex[0])))

    isBigChapter = len(bigChapter_list) > 0 #有無大章節
    tmp_dirName = dirName                  
    a = 0                       #大章節index，從0開始
    b = 1                       #總章節計數
    chapterInt = Decimal('0')   #文檔編號
    # 檢查章名中是否開頭為【第】，回傳 '第' or ''
    firstStr = checkBigChapterList(novel_list)

    for nl in novel_list: #逐一取得章節
        nl_text = toFileName(nl.text) #章節名

        # 有大章節的話，將檔案放到各大章資料夾
        if isBigChapter:
            if bigChapter_firstChild[a].text == nl.text:    # 大章第一章，重置檔案開頭編號
                tmp_dirName = bigChapterPaths[a]
                print('\n章節標題'+str(a+1)+'：'+bigChapter_list[a].text)
                chapterInt = Decimal('0')                   # 重置
                
            if bigChapter_lastChild[a] != '':               # [大章最後章]以外的，將大章計數+1
                if bigChapter_lastChild[a].text == nl.text:
                    a+=1
        # 進章節連結
        url_href = url + nl['href'] #章節連結
        r2 = requests.get(url_href, headers = headers)
        r2.encoding = r2.apparent_encoding #轉碼
        soup2 = bs(r2.text , "html.parser").select('div#novel_honbun') #小說內文

        # 取章節編號
        tmp_chapterInt =  getHeadNum(nl_text) #False

        # 文檔完整路徑
        path = tmp_dirName + '/' + nl_text + '.txt'

        # 檢查章名重複，重複則改額外給編號
        if isDuplicate(path):
            tmp_chapterInt = False
            print('章名重複，加上開頭編號')

        # 若成功取得章節編號，無須額外給編號
        if tmp_chapterInt:
            chapterInt = tmp_chapterInt
        else:
            chapterInt += Decimal('0.1')
            nl_text = firstStr + str(chapterInt) + '-' + nl_text    
        
        print(nl_text)

        # 重設文檔完整路徑
        path = tmp_dirName + '/' + nl_text + '.txt'
        
        # 寫入章節內文
        with open( path, 'w', encoding="utf-8") as txt:
            txt.write(nl.text + "\t" + po_date[b-1].text + '\n\n\n') #寫入開頭標題
            for s in soup2: #逐行處理
                sr = remove_tag(str(s)) #移除tag
                txt.write(sr + '\n')
        b += 1
    print("下載完畢!")
    
    # 刪除舊資料夾
    delete_folders_with_keyword( rootDir)

    # 使用subprocess打開資料夾，並顯示在最上層
    folder_path = dirName.replace('/','\\')+'\\'
    command = f'explorer /select,"{folder_path}"'
    # subprocess.Popen('explorer /select,"' + dirName.replace('/', '\\') + '\\0-首頁導言.txt"')
    subprocess.run(command, shell=True)
# END ==============================================

# 檢查特殊字元，用全形取代特殊字元，避免不符檔名規則
def toFileName(string):
    string = full2half(string)    #全形轉半形
    string = string.strip()       #消除前後空白
    string = re.sub(r'(\d)ー(\d)', r'\1'+"-"+r'\2', string) # 替換數字間的特殊間隔線

    #替換特殊符號
    newString = ''
    before = ['\\', '/',  ':',  '*',  '?', '<',  '>',  '|']
    after  = ['＼', '／', '：', '＊', '？', '＜', '＞', '｜']
    for s in string: #逐字比對
        for i in range(len(before)):
            if s==before[i]:
                s = after[i]
        newString+=s
    return newString

# 消除<Tag>及強調符(・・) *?為非貪婪匹配，小說內文用
def remove_tag(text): 
    text = re.sub(r'<.*?>',"",text)
    text = re.sub(r'\((・+?)\)',"",text)
    return text.replace('―','—')

def get_novel_number(url): #從輸入網址分割出編號部分(正則表達式)
    r = re.search(r"/n\d{4}[A-z]{2}/$", url, re.I)
    return r.group()

# return 大章路徑
def getChapterPath(dirName, num, chapter):
    chapterPath = dirName + '/' + str(num) + "." + toFileName(chapter.text)
    createFolder(chapterPath)
    return chapterPath

# 建立大章節資料夾(路徑名, 章節節點)
def createFolder(chapterPath):
    if not os.path.isdir(chapterPath): #檢查是否已存在
        mkdir(chapterPath)#建新資料夾

# 取得指定標籤 (解析後的網頁Data, CSS選取器規則)
def getSoupTag(soup ,selectStr):
    return soup.select(selectStr)

# 全形轉半形
def full2half(c: str) -> str:
    return unicodedata.normalize("NFKC", c)

# 取第一個連續數字，含小數
def getHeadNum(string):
    match = re.search(r'^\s*第?[\d\.]+', string)
    if match:
        return Decimal(match.group().replace('第', ''))
    else:
        return False

# 將含有關鍵字的資料夾改名為tmp開頭 (根目錄路徑, 關鍵字)
def rename_folders_with_keyword(root_folder, keyword):

    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path) and keyword in folder_name:
            new_folder_path = folder_path +'temp'
            # 資料夾改名
            try:
                os.rename(folder_path, new_folder_path)
            except Exception as e:  #若發生重複，刪掉重複的，再改一次
                print("資料夾改名時發生異常，將會嘗試移除重複 => ", e)    
                shutil.rmtree(new_folder_path)
                print("移除成功")    
                os.rename(folder_path, new_folder_path)
            print("資料夾改名:\n\t原本", folder_path)
            print("\t改為", new_folder_path)

# 刪除暫存資料夾(根目錄路徑, 關鍵字)
def delete_folders_with_keyword(root_folder):
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path) and folder_name[len(folder_name)-4:len(folder_name):] == 'temp':
            # 遞迴刪除資料夾及其內容
            shutil.rmtree(folder_path)
            print("刪除資料夾:", folder_path)

# 檔案是否重複
def isDuplicate(path):
    if os.path.isfile(path):
        return True
    else:
        return False

# 檢查章名開頭是否為'第xx'
def checkBigChapterList(strList):
    for s in strList:
        s = s.text.strip()
        if s[:1] == '第':
            print("章名開頭為【第】")
            return '第'
    return ''

#GUI ===============
def new_window():  
    window = tk.Tk()
    window.title('新視窗')
    window.geometry('450x150') #寬x高
    window.maxsize(1280,700)

    #元件類別(父類別, 選擇性參數1 = 值1, ...) ，建立元件
    #元件.grid(row=列數, column=行數) ，設定(相對)位置
    # ---------- row=0 ---------- 
    mylabel = tk.Label(window, text='請輸入網址：')
    mylabel.grid(row=0, column=0,  ipadx=10, ipady=20)

    # ---------- row=4 ---------- 
    intput_website =tk.StringVar()
    myEntry = tk.Entry(window, textvariable=intput_website, width=40, bg='lightcyan') #文字輸入框
    myEntry.focus() #放入游標
    myEntry.grid(row=0, column=1, columnspan=3, ipadx=30, ipady=10)

    # ---------- row=6 ---------- 
    #正在下載
    mylabel_start = tk.Label(window, text='')
    mylabel_start.grid(row=6, column=0, rowspan=1, columnspan=3)

    #下載按鈕
    def button_event():
        if intput_website.get() == '':
            tk.messagebox.showerror('message', '未輸入') #showerror 提醒訊息
        else:
            global  output_website 
            output_website = intput_website.get()

            #call get_novel開始抓取小說
            mylabel_start.config(text='正在下載...')
            try:
                get_novel( url, get_novel_number(output_website) ) 
                mylabel_start.config(text='下載完畢!!')
            except Exception as e:
                mylabel_start.config(text='下載失敗!! 請重試')
                print('下載失敗!! 請重試 => ', e)
    
    # ---------- row=7 ----------
    myButton = tk.Button(window, text='開始', command= button_event, bg='orange')
    myButton.grid(row=7, column=0, rowspan=1, columnspan=4, ipadx=40, ipady=10)

    #inp1 = tk.Entry(window, text="Hello World", bg="yellow", fg="#263238", font=('Arial', 20))，進一步元件風格
    
    window.mainloop()

def get_novel_number(url): #從輸入網址分割出編號部分(正則表達式)
    r = re.search(r"/n\d{4}[A-z]{2}/$", url, re.I)
    return r.group()


if __name__=='__main__':
    new_window()
    