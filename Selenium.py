from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

#Webdrvier 位址
webdriver_path = "chromedriver.exe"
#打開模擬瀏覽器
driver = webdriver.Chrome(executable_path = webdriver_path)
#前往網頁
driver.get("https://fanyi.baidu.com/#jp/cht")
#等待網頁啟動時間
time.sleep(2) 
# jp_input= chrome_browser.find_element_by_xpath("//div[@id='main-outer']/div")
first = driver.find_element_by_class_name('closedesktop-guide-close').click()
driver.find_element_by_id()
#找到輸入區塊
# jp_input= chrome_browser.find_element_by_xpath("//div[@id='main-outer']/div")

# input_jp="" #存放字串
# with open("[日]呪と罪と流転の華達　～最強賢者は最愛の恋人を寝取らせる～/第※話　とある一日[作者：流星].txt", "r+", encoding="utf-8") as file:
#     while 1:
#         input_jp=file.readline() #一行一行讀取
#         #input_jp有字串則印出，否則關閉迴圈
#         if input_jp == False:
#             break

#輸入欲翻譯文字
jp_input.send_keys("呪と罪と流転の華達")

# cht_output_path= "p .ordinary-output .target-output .clearfix"
#找到輸出區塊
    # cht_output_path_print= chrome_browser.find_element_by_xpath("//div[@id='main-outer']/div/div/div/div[2]/div/div[2]/div/div/div/p[2]")
# print(cht_output_path_print.text)
# #建檔寫入翻譯內容

#     file.write(cht_output_path_print.text)

# # 關掉頁面 和 驅動程式 
# chrome_browser.quit()