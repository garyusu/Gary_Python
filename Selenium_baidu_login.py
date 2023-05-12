import profile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


profile_directory = r'--user-data-dir=C:/Users/garyu/AppData/Local/Google/Chrome/User Data'
option = webdriver.ChromeOptions()
option.add_argument(profile_directory)

#打開模擬瀏覽器(無參數則開啟工作區下的chromedriver.exe)
driver = webdriver.Chrome(chrome_options=option)
#前往網頁(此時為保持登入狀態)
driver.get("https://www.baidu.com/")
#等待網頁啟動時間
time.sleep(2) 
