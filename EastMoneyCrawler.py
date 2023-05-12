from typing import Pattern
import requests
import time
import re
#抓天天基金網站
class EastMoneyCrawler:
    def request(self, page):
        dt = int(round(time.time() * 1000)) #獲取時間戳
        url = f"http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page={page},200&dt={dt}&atfc=&onlySale=0"
        heads ={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
        }
        response = requests.get(url, headers=heads)
        self.convertStr2List(response.text)

    #-----------將資料整理為陣列
    def convertStr2List(self, resText): 
        pattern = re.compile(r"datas:(.*), count") #只取datas,count的所有內容
        resStr = pattern.search(resText).group(1) #取得正則表達式內容
        resStr = re.sub(r"\[", '', resStr) #替換左右括號為空
        resStr = re.sub(r'\]', '', resStr)
        resStrList = resStr.split(',') #根據逗號做切割
        
        result = []
        tmpList = []
        i = 0 #索引值
        for resStr in resStrList: #逐一取所有data值，把取得值丟到暫存
            tmpList.append(resStr) 
            i = i + 1 #計算索引值
            if i%21 ==0: #因為data內容有21欄，取得21個值後放入result[]並清空tmpList
                result.append(tmpList)
                tmpList = []
        print("將字串轉為列表:",result)

if __name__ == "__main__":
    moneyCrawler = EastMoneyCrawler()
    for page in range(1,3): #取3頁
        print(f"Spider page{page}---")
        m=moneyCrawler.request(page)
        print(m)