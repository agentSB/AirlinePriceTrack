import pymysql


connection = pymysql.Connection(host='localhost', user='root', password='19951020', db='test_pa', charset='utf8')
try:
    cursor = connection.cursor()
    sql = 'update lowest_price set lwest_price=1000 where air_route=%s and date=%s'
    cursor.execute(sql, ('can-lax', '2018-10-01'))
    connection.commit()
except Exception as e:
    print('haha')
    print(e)
finally:
    connection.close()
