from cgitb import text
import site
import string
from turtle import color
import requests  #用於get請求
from bs4 import BeautifulSoup as bs #網頁分析
from os import mkdir #建資料夾(目錄)
import tkinter as tk
from tkinter import YView, messagebox
import re

#從網頁抓取內容
def get_info(url): #傳入 
    
    # cookies = {'path' : '/'}
    #https://www.2dfan.com/topics/7308 #2DFan

    headers={ #默認
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Upgrade-Insecure-Requests':'1',#不用改
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
        # 'Connection': 'keep-alive' #保持連接用
    }  

    proxies={
        "http":"186.67.230.45:3128",
        "https":"186.67.230.45:3128"
    }

    req = requests.get(url, headers=headers, verify=False)
    soup = bs(req.text, "html.parser")
    # print(soup)
    if req.status_code != 200:
        print("連接失敗")
    
    #抓取內容
    # guide_content = soup.select('#topic-content') #選取名稱區塊
    return soup

#GUI
def new_window():  
    window = tk.Tk()
    window.title('新視窗')
    window.geometry('500x1000') #寬x高
    window.maxsize(1280,700)

    #元件類別(父類別, 選擇性參數1 = 值1, ...) ，建立元件
    #元件.grid(row=列數, column=行數) ，設定(相對)位置
    mylabel = tk.Label(window, text='請輸入網址：')
    mylabel.grid(row=0, column=0)

    intput_website =tk.StringVar()
    myEntry = tk.Entry(window, textvariable=intput_website, width=30) #文字輸入框
    myEntry.grid(row=0, column=1)

    mylabel_start = tk.Label(window, text='')
    mylabel_start.grid(row=2, column=0)

    myText = tk.Text(window, width=60, height=40) #文字框 height=行數
    myText.grid(row=3, column=0, columnspan=50)

    #建立縱向滾動軸
    text_scrollbar = tk.Scrollbar(window)
    text_scrollbar.grid(row=3, column=50, sticky='ns') 
    #sticky 可以輸入N ,S, E, W或是 混搭例如:EW，NS，NSEW，
    #代表靠N(北方) 、S(南方)、E(東方)、W(西方)，NS(北南延伸)，EW(東西延伸)，NSEW(全方位延伸)

    myText.configure(yscrollcommand=text_scrollbar.set)#設定滾動軸
    text_scrollbar.configure(command=myText.yview)#將文字框Y軸數據放入

    #button觸發event
    def button_event():
        if intput_website.get() == '':
            tk.messagebox.showerror('message', '未輸入') #showerror 提醒訊息
        global  output_website 
        output_website = intput_website.get()
        myText.delete("1.0","end") #清空
        mylabel_start.config(text='開始抓取...')
        myText.insert(tk.END, get_info(output_website))
        mylabel_start.config(text='抓取完畢!!')
        

    myButton = tk.Button(window, text='抓取', command= button_event)
    myButton.grid(row=1, column=0)
    #inp1 = tk.Entry(window, text="Hello World", bg="yellow", fg="#263238", font=('Arial', 20))，進一步元件風格
    
    window.mainloop()


if __name__=='__main__':
    new_window()