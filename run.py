from patest.spiders.example import TicketPriceSpider
from patest.spiders.redisspider import MySplashSpider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from destination import destination, international
import random
import time
import datetime
import redis
import pymysql


def date_range(start, end):
    d1, d2 = datetime.datetime.strptime(start, '%Y-%m-%d'), datetime.datetime.strptime(end, '%Y-%m-%d')
    diff = d2 - d1
    date_array = []
    tmpdate = d1
    for i in range(diff.days + 1):
        date_array.append(str(tmpdate.date()))
        tmpdate += datetime.timedelta(days=1)
    return date_array


def query(f, t, date_array):

    f_code = destination[f]
    t_code = international[t]

    connection = pymysql.Connection(host='localhost', user='root', password='19951020', db='test_pa', charset='utf8')
    try:
        cursor = connection.cursor()
        while date_array:
            date = date_array.pop()
            sql = 'select * from lowest_price where air_route = %s and date = %s and hour(timediff(now(), update_time)) < 12'
            cursor.execute(sql, (f_code+'-'+t_code, date))
            result = cursor.fetchone()
            if result:
                print(result)
            else:
                date_array.append(date)
                make_request(f, t, date)
                print('make request!')
                time.sleep(8)
                query(f, t, date_array)
    finally:
        connection.close()


def make_request(f_key, t_key, target_date):
    # target_date = datetime.datetime.strptime(date_array[int(len(date_array) / 2)], '%Y-%m-%d')
    f_code = destination[f_key]
    t_code = international[t_key]
    url_head = 'https://flights.ctrip.com/international/'
    url_append = f_key + '-' + t_key + '-' + f_code + '-' + t_code + '?' + target_date + '&y_s'
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='19951020')
    r = redis.Redis(connection_pool=pool)
    r.lpush('main_start', url_head + url_append)
    print(url_head + url_append)


d1 = '2018-10-28'
# d2 = '2018-11-0' + str(random.randint(1, 5))
d2 = '2018-11-04'
print(d1, d2)
dep = random.choice(list(destination.keys()))
arr = random.choice(list(international.keys()))

query(dep, arr, date_range(d1, d2))


# pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='19951020')
# r = redis.Redis(connection_pool=pool)
# pipe = r.pipeline(transaction=True)
# r.lpush('tpi_start', 'http://example.com')
# r.lpush('tpi_start', 'http://example.com')
# pipe.execute()

# runner = CrawlerRunner(get_project_settings())
# d = runner.crawl(TicketPriceSpider, f_key=f, t_key=t, date_range=daterange)
# d.addBoth(lambda _: reactor.stop())
# reactor.run()
