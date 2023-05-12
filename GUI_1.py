import tkinter as tk
from tkinter import messagebox

def new_window():
        
    window = tk.Tk()
    window.title('新視窗')
    window.geometry('600x800')
    window.maxsize(1280,700)

    #元件類別(父類別, 選擇性參數1 = 值1, ...) ，建立元件
    #元件.grid(row=列數, column=行數) ，設定(相對)位置
    mylabel = tk.Label(window, text='1+1 = ')
    mylabel.grid(row=0, column=0)

    inp = tk.StringVar() #輸入的字
    myEntry = tk.Entry(window, textvariable=inp) #文字輸入框
    myEntry.grid(row=0, column=1)

    #button觸發
    def button_event():
        if inp.get() == '':
            tk.messagebox.showerror('message', '未輸入答案') #showerror 提醒訊息
        elif inp.get() == '2':
            tk.messagebox.showinfo('message', '正確') #showinfo 提醒訊息
        else:
            tk.messagebox.showerror('message', '答錯')

    myButton = tk.Button(window, text='計算', command= button_event)
    myButton.grid(row=0, column=2)



    #inp1 = tk.Entry(window, text="Hello World", bg="yellow", fg="#263238", font=('Arial', 20))，進一步元件風格

    window.mainloop()

if __name__=='__main__':
    new_window()