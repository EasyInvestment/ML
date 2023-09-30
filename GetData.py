import pymysql
import pandas as pd

def connect_db(database):
    host = "investment.cu24cf6ah5lb.us-west-1.rds.amazonaws.com"
    port = 3306
    username = "someone555"
    database = database
    password = "12345asdfg"
    try:
        con = pymysql.connect(host=host, user=username, password=password,
                db=database, charset='utf8') # 한글처리 (charset = 'utf8')
    except Exception as e:
        print(">> connection 실패 ",e)
        return False

    return con

def dataAll(database,table):
    # 커서 생성
    con = connect_db(database)
    cursor = con.cursor()

    # 모든 데이터 가져오기
    cursor.execute("SELECT * FROM "+table)

    data = cursor.fetchall()

    column_names = [i[0] for i in cursor.description]

    df = pd.DataFrame(data, columns=column_names)

    # 연결 및 커서 닫기
    cursor.close()
    con.close()

    return df