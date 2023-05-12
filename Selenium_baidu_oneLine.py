from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import re

#Webdrvier 位址
webdriver_path = "chromedriver.exe"
#打開模擬瀏覽器(無參數則開啟同目錄下的)
driver = webdriver.Chrome()
#前往網頁
driver.get("https://fanyi.baidu.com/#jp/cht")


input_jp_list=[]
# output_cht_list=[]
file_path = "[日]呪と罪と流転の華達　～最強賢者は最愛の恋人を寝取らせる～/第※話　とある一日[作者：流星].txt"

with open(file_path, "r", encoding="utf-8") as file:
    input_jp_list = file.readlines()

with open("test.txt", "a", encoding="utf-8") as file2:
    for input_jp in input_jp_list:
        if input_jp !='\n' and input_jp != '\u3000\n':
            #一行一行輸入欲翻譯區塊
            key_input = driver.find_element_by_xpath('//*[@id="baidu_translate_input"]').send_keys(input_jp)
            #等待翻譯時間 設定秒數
            time.sleep(3.5)
            #找到輸出區塊內的文字
            output_cht = driver.find_element_by_css_selector('p.ordinary-output.target-output.clearfix').text
             #寫入檔案並加上換行
            file2.write('\n' + input_jp + output_cht + '\n')
            print( input_jp + output_cht )
            #清除框內文字
            key_input = driver.find_element_by_xpath('//*[@id="baidu_translate_input"]').clear()
        else:
            file2.write("\n")
            print("\n")

    
        