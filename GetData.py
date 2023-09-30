import pymysql
import pandas as pd
import FinanceDataReader as fdr

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

def getTableName(database):
    con = connect_db(database)
    # 커서 생성
    cursor = con.cursor()

    # 테이블 목록 조회
    cursor.execute("SHOW TABLES")

    # 결과 가져오기
    tables = cursor.fetchall()
    tables = [table[0] for table in tables]
    cursor.close()
    con.close()

    return tables

# 카테고리의 주식 이름 목록 반환
def getStockList(name):
    # 한국거래소 상장종목 전체
    df_krx = fdr.StockListing('KRX')
    table = getTableName(name)
    table = [i.replace("s","") for i in table]
    curr_sym = []
    for i in range(len(table)):
        curr_sym.append(df_krx[df_krx["Symbol"] == table[i]]["Name"].values[0])
    
    return curr_sym