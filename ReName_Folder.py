import os

#該層所有檔案、資料夾
def getDirList(dirPath):
    return os.listdir(dirPath)

#篩選出資料夾 
# 參數                                  --要判斷的目錄路徑
# os.path.isfile()                      --判斷是否檔案
# os.path.join(目錄路徑, 目錄下的其中檔案)--組合檔案/資料夾路徑
def getFolderList(dirList):
    #回傳資料夾路徑list
    # return [f for f in dirList if not os.path.isfile(os.path.join(dirPath, f))]
    #回傳資料夾list
    return [f for f in dirList if not os.path.isfile(f)]

#重命名資料夾(目錄路徑, 檔名/資料夾list)，要先知道替換的字位置前後索引值、替換成甚麼字
def reFolderName(dirPath, fileNameList):
    start = 3           #開頭索引
    end =5              #末端索引
    replaceStr = '短篇' #替換為?
    errorFlag = False   #有錯誤，標記True
    flag = False       #有執行替換:True

    print("\n運行目錄為："+dirPath)
    for f in fileNameList:
        headStr = f[0:start]    #擷取檔名前端
        # print('headStr：' + headStr)
        endStr = f[end:len(f)]  #擷取檔名後端
        # print('endStr：' + endStr)

        if '同人' == f[start:end]:
            reStr = headStr + replaceStr + endStr
            beforePath = dirPath + '\\' + f 
            afterPath = dirPath + '\\' + reStr 
            print (afterPath)
            flag=True
            try:
                os.rename(beforePath, afterPath)
                print("\n" + f + "\n已變更為\n" + reStr)
            except Exception as e :
                print(f"\n更名失敗，錯誤內容\n{e}")
                errorFlag = True
            finally:
                continue

    if errorFlag:
        print("\n執行完成，有錯誤請檢查!")
    elif not flag : 
        print("\n沒有可替換名稱的檔案/資料夾")
    else:
        print("\n執行完成!")

if __name__ == '__main__':
    #要搜尋的目錄路徑
    dirPath = "F:\Taboo_\PICsuchi\【畫家】\[姫屋 (阿部いのり)]#人妻背德#調教墮落"

    folderList = getFolderList(getDirList(dirPath))
    reFolderName(dirPath, folderList)
    