
from bs4.element import NamespacedAttribute


def add_file_name(name):
    with open("轉日區開啟 "+ name +".txt", 'a', encoding="utf-8") as txt:
        txt.write("")
        print("成功!")
exeName = 'プリンセス☆シスターズ！' #exe檔名

if __name__ == '__main__':
    add_file_name(exeName)