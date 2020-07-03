import pymysql.cursors

# Connect to the database
def insert(tingfang,ztname,ztaddr,ztstatus,testtime):
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='Video#2017!.',
                                db='VideoMonitor',
                                cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = 'INSERT INTO ztrunstatus (tingfang,ztname,ztaddr,ztstatus,testtime) VALUES (%s,%s,%s,%s,%s)'
            cursor.execute(sql,(tingfang,ztname,ztaddr,ztstatus,testtime))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()

def select(time):
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='Video#2017!.',
                                db='VideoMonitor',
                                cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = 'SELECT * FROM ztrunstatus WHERE testtime>%s'
            cursor.execute(sql,(time))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            result=cursor.fetchall()
            connection.commit()
    finally:
        connection.close()
        return result

def selectyc(time):
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='Video#2017!.',
                                db='VideoMonitor',
                                cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = 'SELECT * FROM ztrunstatus WHERE testtime>%s and ztstatus != 200'
            cursor.execute(sql,(time))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            result=cursor.fetchall()
            connection.commit()
    finally:
        connection.close()
        return result
