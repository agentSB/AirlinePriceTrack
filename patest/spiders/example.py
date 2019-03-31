# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
# from scrapy.spiders import Spider
from scrapy_redis.spiders import RedisSpider
from scrapy_splash import SplashMiddleware
from scrapy.http import Request, HtmlResponse
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from patest.items import TicketPriceItem
from destination import destination, international
from importlib import reload
import datetime
# import sys
# reload(sys)
# sys.stdout = open('output.txt', 'w')


class TicketPriceSpider(RedisSpider):
    name = 'tp'
    redis_key = 'tp:target_urls'

    def __init__(self, f_key, t_key, date_range):
        target_date = datetime.datetime.strptime(date_range[int(len(date_range)/2)], '%Y-%m-%d')
        f_code = destination[f_key]
        t_code = international[t_key]
        url_append = f_key + '-' + t_key + '-' + f_code + '-' + t_code + '?'
        self.f_key = f_key
        self.t_key = t_key
        self.air_route = f_code + '-' + t_code
        self.date_range = date_range
        self.url = 'https://flights.ctrip.com/international/' + url_append + str(target_date.date()) + '&y_s'
        # self.url = 'http://flights.ctrip.com/international/beijing-kualalumpur-bjs-kul?2018-10-15&y_s'

    # request需要封装成SplashRequest
    def start_requests(self):
        print(self.url)
        yield SplashRequest(self.url, self.parse, args={'wait': '5'}
                            # ,endpoint='render.json'
                            )
        # yield Request(self.url, self.parse)

    def parse(self, response):

        # test = open('/Users/liangzx/Downloads/flights.ctrip.com.txt', 'r', encoding='utf-8')
        # teststr = test.read()
        # site = Selector(text=teststr)
        # print(response.text)

        site = Selector(response)
        tpi_list = list()

        items = site.css('.tbContent').xpath('.//tr')
        print(len(items))
        count = len(self.date_range)
        for i in range(count - 1, -1, -1):
            ddd = items.xpath('.//td[@data-time="{}"]'.format(self.date_range[i]))
            if len(ddd.xpath('.//div')) > 1:
                tpi = TicketPriceItem()
                price = ''.join(ddd.xpath('.//div[2]/text()').extract()).replace('\n', '')
                tpi['air_route'] = self.air_route
                tpi['date'] = self.date_range[i]
                tpi['low_price'] = price
                print(self.date_range[i], int(price))
                self.date_range.pop(i)

                if i == int(count/2):
                    detail_items = site.xpath('//div[contains(@class, "flight-item")]')
                    tpi['detail'] = self.detail_selector(detail_items)

                tpi_list.append(tpi)

        print(self.date_range)
        # if self.date_range:
        #     extra_query(self.f_key, self.t_key, self.date_range)
        # time.sleep(3)
        return tpi_list

    def detail_selector(self, detail_items):
        it_list = list()
        print(len(detail_items))
        for item in detail_items:
            flight_detail_sections = item.css('.flight-detail-section')

            it = dict()
            it['transfer_count'] = len(flight_detail_sections)
            it['airline_name'] = []
            it['flight_No'] = []
            it['plane_type'] = []
            it['flight_time'] = []
            it['airports'] = []
            it['section_total_time'] = []

            for fds in flight_detail_sections:
                airline_name = fds.css('.section-flight-base').xpath('./text()[not(parent::span)]').extract_first()
                print(airline_name)
                it['airline_name'].append(airline_name)

                flight_No = fds.css('.flight-No::text').extract_first()
                print(flight_No)
                it['flight_No'].append(flight_No)

                plane_type = fds.css('.abbr::text').extract_first()
                print(plane_type)
                it['plane_type'].append(plane_type)

                flight_time = fds.xpath('.//span[contains(@class, "section-time")]/text()').extract()
                print(flight_time)
                it['flight_time'] += flight_time

                airports = fds.css('.section-airport::text').extract()
                print(airports)
                it['airports'] += airports

                section_total_time = fds.css('.section-duration::text').extract_first()[5:]
                print(section_total_time)
                it['section_total_time'].append(section_total_time)

            total_time = item.css('.flight-total-time::text').extract_first().replace(' ', '').replace('\n', '')[1:]
            print(total_time)
            it['total_time'] = total_time

            seat_lowest_price = item.xpath('.//div[contains(@class, "seat-row")]')[0]
            seat_type = seat_lowest_price.css('.seat-type ::text').extract_first().replace('\n', '').replace(' ', '')
            print(seat_type)
            it['seat_type'] = seat_type

            price = seat_lowest_price.css('.mb5').css('span')[1].xpath('./text()[not(parent::dfn)]').extract_first()
            # price = seat_lowest_price.xpath('string(.//span[@class="price"])').extract_first()
            print(price)
            it['price'] = price

            print("******************************")
            it_list.append(it)

        return it_list
