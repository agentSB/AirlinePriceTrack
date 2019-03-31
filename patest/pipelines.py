# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from twisted.internet.threads import deferToThread
import pymysql


class TicketPricePipeline(object):
    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def join(self, args):
        if args:
            for i in range(0, len(args)):
                if args[i] is None:
                    args[i] = 'null'
            return ' '.join(args)
        else:
            return 'null'

    def _process_item(self, item, spider):
        db = pymysql.Connection(host='localhost', user='root', password='19951020', db='test_pa', charset='utf8mb4')
        try:
            cursor = db.cursor()
            info = dict(item)
            sql = 'insert into lowest_price values(null, %s, %s, %s, now())'
            cursor.execute(sql, (info['air_route'], info['date'], info['low_price']))
            if 'detail' in info:
                extra_sql = 'insert into airline values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())'
                for ele in info['detail']:
                    detail = dict(ele)
                    arglist = (
                        info['air_route'],
                        str(detail['transfer_count']),
                        self.join(detail['airline_name']),
                        self.join(detail['flight_No']),
                        info['date'],
                        self.join(detail['plane_type']),
                        self.join(detail['flight_time']),
                        self.join(detail['airports']),
                        self.join(detail['section_total_time']),
                        detail['total_time'],
                        detail['seat_type'],
                        detail['price']
                    )
                    cursor.execute(extra_sql, arglist)
            db.commit()
        finally:
            db.close()
        return item



class PatestPipeline(object):
    def __init__(self):
        self.file = codecs.open('spider.txt', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()
