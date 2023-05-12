from time import sleep
from turtle import color
import requests  #用於get請求
from bs4 import BeautifulSoup as bs #網頁分析
from os import mkdir #建資料夾(目錄)
import tkinter as tk
import re
import os
import unicodedata

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
def get_novel(url, novel_id, isFileNum, webSelect): #傳入(主址,小說編號)
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
    folderName = ''
    if webSelect: # T:成為小說家吧！  F:夜曲小說
        folderName = '[成為小說家吧！]'
    else:
        folderName = '[夜曲小說]'
    # dirName = novel_title[0].text #若 資料夾名+檔名 太長導致錯誤，切換到這個
    dirName = 'C:/Users/garyu/OneDrive/ebook/YD/'+ folderName +'/'+ toFileName(dirName)  +" [更新至" + str(len(novel_list)) +']'
    if not os.path.isdir(dirName): #檢查是否已存在
        mkdir(dirName)#建新資料夾，預設在工作區目錄
    print('\n小說目錄：\n' + dirName)

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
    b = 1 #檔案開頭編號(選取 "是")
    headNumStr = '' #章節開頭編號
    c = 1 #章節開頭編號加上小數點的計數
    # print('\n檔名：',end="")
    for nl in novel_list: #逐一取得章節
        nl_text = toFileName(nl.text) #章節名

        #有大章節的話，將檔案放到各大章資料夾
        if isBigChapter:
            if bigChapter_firstChild[a].text == nl.text:    #大章第一章
                tmp_dirName = bigChapterPaths[a]
                # print("@@@@@@@"+ bigChapter_firstChild[a].text +" = " +nl.text)
                print('\n章節標題'+str(a+1)+'：'+bigChapter_list[a].text)
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

        if isFileNum:   #檔名 (加上編號)
            ch_name = str(b) + '-' + nl_text + '.txt'    
        else:           #檔名 (不加編號)
            #擷取章節開頭的數字，開頭不是數字就上一章編號加上小數
            if headIsInt(nl_text):
                headNumStr = getHeadInt(nl_text)
                ch_name = nl_text + '.txt'  
                c = 1 #重置小數
            else:
                headNumStr += '-' + str(c) + ' '
                c += 1 #有連續多個沒編號
                ch_name = headNumStr + nl_text + '.txt' 
        print(ch_name)

        with open(tmp_dirName + '/' + ch_name, 'a', encoding="utf-8") as txt:
            txt.write(nl.text + "\t" + po_date[b-1].text + '\n\n\n') #寫入開頭標題
            for s in soup2: #逐行處理
                sr = remove_tag(str(s)) #移除tag
                txt.write(sr + '\n')
        b = b + 1
    # os.rename(dirName + '/', dirName + " [更新至" + str(b-1) + ']/')
    print("下載完畢!")

#檢查特殊字元，用全形取代特殊字元，避免不符檔名規則
def toFileName(string):
    string = full2half(string)            #全形轉半形
    string = re.sub(r'^\s+?',"",string)   #消除前面空白
    flag = False
    for i in string: #逐一比對
        if i=='\\' or i=='/' or i==':' or i=='*' or i=='?' or i=='<' or i=='>' or i=='|':
            flag = True
    if flag: #替換成全形
        string = string.replace('\\','＼').replace('/','／').replace(':','：')
        string = string.replace('*','＊').replace('?','？').replace('<','＜')
        string = string.replace('>','＞').replace('|','｜')
    return string.replace('―','—')
    # return string

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

#全形轉半形
def full2half(c: str) -> str:
    return unicodedata.normalize("NFKC", c)

#擷取開頭，判斷是否數字
def headIsInt(string):
    i = string[0:1].isnumeric() #Ture/False
    # if i:
    #     print(string[0:1] + '：是數字')
    # else:
    #     print(string[0:1] + '：不是數字')
    return i

#取得章節開頭的數字
def getHeadInt(string):
    i = ""
    for s in string:
        if not headIsInt(s):
            break
        i += s   
    # print("取得的數字為：" + i)
    return i

#GUI ===============
def new_window():  
    window = tk.Tk()
    window.title('新視窗')
    window.geometry('400x200') #寬x高
    window.maxsize(1280,700)

    #元件類別(父類別, 選擇性參數1 = 值1, ...) ，建立元件
    #元件.grid(row=列數, column=行數) ，設定(相對)位置
    # ---------- row=0 ---------- 
    tk.Label(window, relief="raised", text='加上編號：\n(有章節標題請選取"是")').grid(row=0, column=0)

    #單選按鈕RDO 是/否
    var = tk.IntVar()
    #回傳選取 T or F，切換時觸發
    def selection(): 
        return False if var.get()==0 else True
    myradiobutton1 = tk.Radiobutton(window, text='是', variable=var, value=1, command=selection)
    myradiobutton1.grid(row=0, column=1, sticky='W')
    myradiobutton2 = tk.Radiobutton(window, text='否', variable=var, value=0, command=selection)
    myradiobutton2.grid(row=0, column=2, sticky='W')
    myradiobutton2.select() #選取狀態

    # ---------- row=1 ---------- 
    tk.Label(window, relief="raised", text='來自哪個網站：').grid(row=2, column=0)
    #單選按鈕RDO [成為小說家吧！]/[夜曲小說]
    var2 = tk.IntVar()
    #回傳選取 T or F，切換時觸發
    def selection2(): 
        return False if var2.get()==0 else True
    myradiobutton3 = tk.Radiobutton(window, text='成為小說家吧！', variable=var2, value=1, command=selection2)
    myradiobutton3.grid(row=2, column=1, sticky='W')
    myradiobutton4 = tk.Radiobutton(window, text='夜曲小說', variable=var2, value=0, command=selection2)
    myradiobutton4.grid(row=2, column=2, sticky='W')
    myradiobutton4.select() #選取狀態
    
    # ---------- row=4 ---------- 
    mylabel = tk.Label(window, text='請輸入網址：')
    mylabel.grid(row=4, column=0)

    intput_website =tk.StringVar()
    myEntry = tk.Entry(window, textvariable=intput_website, width=40, bg='lightcyan') #文字輸入框
    myEntry.focus() #放入游標
    myEntry.grid(row=4, column=1, rowspan=1, columnspan=3)

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
            get_novel(url, get_novel_number(output_website), selection(), selection2()) 
            mylabel_start.config(text='下載完畢!!')
    
    # ---------- row=7 ----------
    myButton = tk.Button(window, text='開始', command= button_event, bg='orange')
    myButton.grid(row=7, column=0, rowspan=1, columnspan=3, ipadx=40, ipady=10)

    #inp1 = tk.Entry(window, text="Hello World", bg="yellow", fg="#263238", font=('Arial', 20))，進一步元件風格
    
    window.mainloop()

def get_novel_number(url): #從輸入網址分割出編號部分(正則表達式)
    r = re.search(r"/n\d{4}[A-z]{2}/$", url, re.I)
    return r.group()


if __name__=='__main__':
    new_window()
    