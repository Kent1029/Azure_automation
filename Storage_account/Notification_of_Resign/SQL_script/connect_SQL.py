import psycopg2
import config

#建立連線
def create_connect():
    conn = psycopg2.connect(
        host=config.host,
        dbname=config.dbname,
        user=config.user,
        password=config.password,
        port=config.port
    )
    conn.autocommit = True
    return conn

def delete_yesterday_data():
    global cur
    # 執行 SQL DELETE 語句
    cur.execute("""
        DELETE FROM public.staff_list
        WHERE DATE(insert_time) < CURRENT_DATE;
    """)

def test_connection():
    try:
        global cur
        print("Database connect successfully.")

        cur.execute("SELECT COUNT(*) FROM public.staff_list")
        rows1 = cur.fetchall()
        #print(f"Number of data before deletion：{rows1[0][0]}.")

        #先刪除昨天的資料
        delete_yesterday_data()
        print("Delete yesterday's data successfully.")

        cur.execute("SELECT COUNT(*) FROM public.staff_list")
        rows2 = cur.fetchall()
        print(f"Today’s data：{rows2[0][0]}.")
        
    except Exception as e:
        print("Connection failed.")
        print("Error message:", e)

def get_resign_data():
    global cur
    # 執行 SQL 查詢
    cur.execute("""
        SELECT emplid, name, jobtitle_descr, email_address_a, termination_dt, supervisor_id 
        FROM public.staff_list 
        WHERE termination_dt IS NOT NULL 
        AND email_address_a != 'NONE' 
        AND termination_dt BETWEEN CURRENT_DATE - INTERVAL '30 days' AND CURRENT_DATE
        ORDER BY termination_dt DESC;
    """)

    # 獲取查詢結果
    rows = cur.fetchall()

    return rows

# 在應用程序結束時關閉連接和游標
def close_connection():
    global cur
    global conn

    cur.close()
    conn.close()


if __name__ == '__main__':
    # 建立連接和游標作為全局變量
    conn = create_connect()
    cur = conn.cursor()

    test_connection()

    #rows = get_resign_data()
    close_connection()



'''
# 把資料改為前一日，可以進行測試delete_yesterday_data()功能

UPDATE public.staff_list
SET insert_time = '2024-04-18'
WHERE pkid IN (
SELECT pkid
FROM public.staff_list
ORDER BY pkid
LIMIT 10000);
'''