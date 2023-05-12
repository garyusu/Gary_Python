from turtle import color
import requests  #用於get請求
from bs4 import BeautifulSoup as bs #網頁分析
from os import mkdir #建資料夾(目錄)
import tkinter as tk
from tkinter import messagebox
import re
import pyperclip3 as pc3


#從網頁抓取小說
def get_info(url): #傳入 
    # url = "http://www.getchu.com/soft.phtml?id=" + info_id #Getchu
    
    #可能需改動項目1
    cookies = {'getchu_adalt_flag' : 'getchu.com'}
    #http://www.getchu.com/soft.phtml?id=224365

    headers={ #默認
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Upgrade-Insecure-Requests':'1',#不用改
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
        # 'Connection': 'keep-alive' #保持連接用
    }  
    req = requests.get(url, headers=headers, cookies=cookies, verify=False)
    soup = bs(req.text, "html.parser")
    # print(soup)
    if req.status_code != 200:
        print("連接失敗")

    #遊戲類型  同人/ゲーム
    gameType = soup.select('[class = "genretab current"]')[0].text
    
    if gameType == "同人":
        print("遊戲類型 同人")
    elif gameType == "ゲーム":
        print("遊戲類型 ゲーム")
    else:
        print("遊戲類型 Error!!!!")
    #組合字串
    file_name = company_name(soup, gameType) + game_name(soup) + sale_year(soup) + painter_name(soup, gameType)
    file_name = toFileName(file_name)
    print(file_name)
    return file_name

def company_name(soup, gameType):
    try:
        #品牌名
        if gameType == "同人":
            company_name = soup.select('td:contains("サークル：") + td')[0].text
            company_name = removeSpaces(company_name).replace('（このサークルの作品一覧）', '')#消除多餘的字
            company_name = "[同人][" + company_name + "]"
        elif gameType == "ゲーム":
            company_name = soup.select('td:contains("ブランド：") + td')[0].text
            company_name = removeSpaces(company_name).replace('（このブランドの作品一覧）', '')#消除多餘的字
            company_name = "[" + company_name + "]"
    except:
        tk.messagebox.showerror('message', '抓取品牌名失敗') #showerror 提醒訊息
        company_name = ""
    return company_name

def game_name(soup):
    try:
        #遊戲名
        game_name = soup.select('th > h1#soft-title')[0].text #選取名稱區塊
        game_name = game_name.replace('（このタイトルの関連商品）', '')
        game_name = game_name.replace('豪華限定版','').replace('初回限定版','').replace('通常版','')
    except:
        tk.messagebox.showerror('message', '抓取名稱失敗') #showerror 提醒訊息
        game_name = ""
    return removeSpaces(game_name)

def sale_year(soup):
    try:
        #發售年
        sale_year = soup.select('a[title="同じ発売日の同ジャンル商品を開く"]')[0].text
        sale_year = re.sub(r"/.+", "", sale_year) #消除年以外的字元
        sale_year = '('+sale_year+')'
    except:
        tk.messagebox.showerror('message', '抓取發售年失敗') #showerror 提醒訊息
        sale_year = ""
    return sale_year

def painter_name(soup, gameType):
    try:   
        #原畫
        if gameType == "同人":
            painter_name = soup.select('td:contains("原画／作家：") + td')[0].text
        elif gameType == "ゲーム":
            painter_name = soup.select('td:contains("原画：") + td')[0].text
        painter_name = '_原畫 '+ painter_name
    except:
        tk.messagebox.showerror('message', '抓取原畫失敗') #showerror 提醒訊息
        painter_name = ""
    return painter_name

#消除前後空白
def removeSpaces(str):
    return re.sub(r'(^\s*)|(\s*$)', "", str)

#GUI
def new_window():  
    window = tk.Tk()
    window.title('新視窗')
    window.geometry('300x400') #寬x高
    window.maxsize(1280,700)

    #元件類別(父類別, 選擇性參數1 = 值1, ...) ，建立元件
    #元件.grid(row=列數, column=行數) ，設定(相對)位置
    mylabel = tk.Label(window, text='請輸入網址：')
    mylabel.grid(row=0, column=0)

    intput_website =tk.StringVar()
    myEntry = tk.Entry(window, textvariable=intput_website, width=30) #文字輸入框
    myEntry.grid(row=0, column=1)
    myEntry.focus() #放入游標

    mylabel_start = tk.Label(window, text='')
    mylabel_start.grid(row=2, column=0, columnspan=10, sticky="w") #橫跨10欄 靠W(西)對齊

    myText = tk.Text(window, width=40, height=10) #文字框 height=行數
    myText.grid(row=3, column=0, columnspan=50)

    #button觸發event
    def button_event():
        if intput_website.get() == '':
            tk.messagebox.showerror('message', '未輸入') #showerror 提醒訊息
        global  output_website 
        output_website = intput_website.get()

        mylabel_start.config(text='開始抓取...')
        myText.delete("1.0","end") #先清空
        info= get_info(output_website) #取得資訊

        if info != False:
            mylabel_start.config(text='抓取完畢!!，已複製到剪貼簿')
            myText.insert(tk.END, info)#在尾端插入info
            pc3.copy(info)
        else:
            mylabel_start.config(text='抓取失敗')


    myButton = tk.Button(window, text='計算', command= button_event)
    myButton.grid(row=1, column=0)
    #inp1 = tk.Entry(window, text="Hello World", bg="yellow", fg="#263238", font=('Arial', 20))，進一步元件風格
    
    window.mainloop()

# def get_info_number(url): #從輸入網址分割出編號部分(正則表達式)
#     r = re.search(r"\d+$", url, re.I) #id=後的數字
#     return r.group()

def toFileName(str):
    flag = False
    for i in str: #逐一比對
        if i=='\\' or i=='/' or i==':' or i=='*' or i=='?' or i=='<' or i=='>' or i=='|':
            flag = True
    if flag: #替換成全形
        str = str.replace('\\','＼').replace('/','／').replace(':','：')
        str = str.replace('*','＊').replace('?','？').replace('<','＜')
        str = str.replace('>','＞').replace('|','｜')
    return str.replace('―','—')


if __name__=='__main__':
    new_window()
    