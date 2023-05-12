from turtle import color
import requests  #用於get請求
from bs4 import BeautifulSoup as bs #網頁分析
from os import mkdir #建資料夾(目錄)
import tkinter as tk
from tkinter import messagebox
import re
import pyperclip3 as pc3


def get_info(url): #傳入 
    # url = "https://www.dlsite.com/home/work/=/product_id/" + info_id #Getchu
    
    #可能需改動項目1
    cookies = {
        #滿18
        'adultchecked' : '1',                     
        #切換繁體
        # "wovn_selected_lang":"zh-CHS",
        # "wovn_mtm_showed_langs":"[\"zh-CHS\"]",
        "locale":"zh-tw"
    }

    headers={ #默認
        'Accept':'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Upgrade-Insecure-Requests':'1',#不用改
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'
        # 'Connection': 'keep-alive' #保持連接用
    }  
    req = requests.get(url, headers=headers, cookies=cookies, verify=False)
    soup = bs(req.text, "html.parser")
    # print(soup)
    if req.status_code != 200:
        print("連接失敗")

    errorStr = ""
    
    try:
        #遊戲名
        game_name = soup.select('#work_name')[0].text #選取名稱區塊
        game_name = re.sub(r'(^\s*)|(\s*$)', "", game_name) #消除前後空白
    except:
        errorStr += '抓取遊戲名失敗\n' #showerror 提醒訊息
        print("抓取遊戲名失敗")
        game_name = ""

    try:
        #品牌名
        # company_name = soup.select('td > a.glance')[0].text
        company_name = soup.select('.maker_name')[0].text
        company_name = re.sub(r'(^\s*)|(\s*$)', "", company_name) #消除前後空白
        company_name = "["+ company_name +"]"
    except:
        errorStr += '抓取品牌名失敗\n' #showerror 提醒訊息
        print("抓取品牌名失敗")
        company_name = ""

    try:
        #發售年
        sale_year = soup.select('th:contains("販賣日") + td')[0].text
        sale_year = re.sub(r'[年].+', "", sale_year) #消除年以外的字元
        sale_year = "("+sale_year+")"
    except:
        errorStr += '抓取發售年失敗\n' #showerror 提醒訊息
        print("抓取發售年失敗")
        sale_year = ""    

    try:
        #劇本
        screenwriter = soup.select('th:contains("劇本") + td')[0].text
        screenwriter = re.sub(r'[\n\s]+', "", screenwriter) #消除換行字元
        screenwriter = "_劇本：" + screenwriter
    except:
        errorStr += '抓取劇本失敗\n' #showerror 提醒訊息
        print("抓取劇本失敗")
        screenwriter = ""     
    
    try:
        #插畫
        illustrator = soup.select('th:contains("插畫") + td')[0].text
        illustrator = re.sub(r'[\n\s]+', "", illustrator) #消除換行字元
        if screenwriter != illustrator:
            illustrator = "／插畫：" + illustrator
        else:
            illustrator = "_插畫：" + illustrator
        # print(illustrator)
    except:
        errorStr += '抓取插畫失敗' #showerror 提醒訊息
        print("抓取插畫失敗")
        illustrator = ""    
    # https://www.dlsite.com/maniax/work/=/product_id/RJ435614.html

    file_name = '[同人]'+company_name + game_name + sale_year + screenwriter + illustrator
    if errorStr != "" :
        tk.messagebox.showerror('message', errorStr) #showerror 提醒訊息
    return file_name
    

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

if __name__=='__main__':
    new_window()