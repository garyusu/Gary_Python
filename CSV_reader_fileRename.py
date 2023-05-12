import csv
from sqlite3 import dbapi2
import pymysql

def csv_readToList():
    with open("garyusu/media/ZzHjaePFb1cDxAm-likes-20180921_051206-20200505_071322-media_RE.csv", newline='', encoding="utf-8") as csvfile:
        rows = csv.reader(csvfile)
        list_rows = []
        for row in rows:
            list_rows.append(row) #串列化
        del list_rows[0:1] #刪除前n筆無用資料
        print(list_rows[0])
    csvfile.close
    return list_rows

def create_csv_mysql():
    #開啟資料庫連線
    db = pymysql.connect(
        host="localhost", 
        port=3306, 
        ser="garyusu", 
        passwd="garyusu", 
        db="csv_schema", 
        charset="utf8")
    #使用cursor()方法建立一個游標物件cursor
    with db.cursor() as cursor:
        #使用execute()方法執行SQL，如果表存在則刪除
        cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
        #SQL語法
        sql = """CREATE TABLE EMPLOYEE(
            Tweet_date DATETIME NOT NULL,
            Action_date DATETIME NOT NULL,
            Display_name VARCHAR(20),
            Username VARCHAR(20),
            Tweet_URL VARCHAR(20),
            Media_type VARCHAR(10),
            Media_URL VARCHAR(20),
            Saved_filename VARCHAR(20),
            Tweet_content VARCHAR(20),
            Replies INT,
            Likes INT
        )"""
        cursor.execute(sql)
        print("CREATE TABLE over!")

def insert_csvList_to_DB(csv_list):
    db = pymysql.connect(
        host="localhost", 
        port=3306, 
        user="garyusu", 
        passwd="garyusu", 
        db="csv_schema", 
        charset="utf8")
    with db.cursor() as cursor:
        sql = """LOAD DATA INFILE "D:\myProject\garyusu\media\ZzHjaePFb1cDxAm-likes-20180921_051206-20200505_071322-media_RE.csv"
        INTO TABLE csv_table
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\\r\\n'
        IGNORE 1 LINES"""

        cursor.execute(sql)
        print("INSERT TABLE over!")

if __name__=='__main__':
    # create_csv_mysql()
    insert_csvList_to_DB(csv_readToList())

     
