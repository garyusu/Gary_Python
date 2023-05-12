import tkinter as tk

#建立視窗
window = tk.Tk()

#視窗標題
window.title('window')

#設定大小(像素 寬x高)
window.geometry('600x800') 

#宣告標籤(foreground 前景，可以當作是文字顏色)
lbl_1 = tk.Label(window, text="Hello World", bg="yellow", fg="#263238", font=('Arial', 20))

#設定放置的位置(使用 grid 布局)
lbl_1.grid(column=0, row=0)


#主視窗迴圈顯示
window.mainloop()