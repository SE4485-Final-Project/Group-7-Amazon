from pip import main
import pymysql

_HOST = "omer-database.c2bldp7gxvil.us-east-1.rds.amazonaws.com"
_USERNAME = "omer"
_PASSWORD = "omerdatabase"
_DATABASE = "Knowledge_Base"

connection = pymysql.connect(host=_HOST,user=_USERNAME,password=_PASSWORD,database=_DATABASE);
with connection:
    with connection.cursor() as cursor:
        sql = "SELECT * from info"
        cursor.execute(sql)
        result = cursor.fetchall()
        for t in result:
            print(t)