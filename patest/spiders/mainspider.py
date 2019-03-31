# -*- coding: utf-8 -*-
import scrapy
from patest.spiders.redisspider import MyRedisSpider
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from patest.items import TicketPriceItem
from importlib import reload
import sys
reload(sys)
sys.stdout = open('output.txt', 'w')


class TicketPriceSpider(MyRedisSpider):
    name = 'main'
    redis_url = 'redis://:19951020@127.0.0.1:6379'
    redis_key = 'main_start'

    def make_requests_from_url(self, url):
        return SplashRequest(url, callback=self.parse, args={'wait': 3, 'html': 1})

    def parse(self, response):

        # test = open('/Users/liangzx/Downloads/flights.ctrip.com.txt', 'r', encoding='utf-8')
        # teststr = test.read()
        # site = Selector(text=teststr)
        # print(response.text)
        site = Selector(response)
        tpi_list = list()
        items = site.css('.tbContent').xpath('.//tr')

        target_month = response.url[-14:-6]
        target_day = response.url[-6:-4]
        air_route = response.url[-22:-15]
        for i in range(1, 32):
            target_date = target_month + str(i).zfill(2)
            ddd = items.xpath('.//td[@data-time="{}"]'.format(target_date))
            if len(ddd.xpath('.//div')) > 1:
                tpi = TicketPriceItem()
                price = ''.join(ddd.xpath('.//div[2]/text()').extract()).replace('\n', '')
                tpi['air_route'] = air_route
                tpi['date'] = target_date
                tpi['low_price'] = price
                print(target_date, int(price))

                if i == int(target_day):
                    detail_items = site.xpath('//div[contains(@class, "flight-item")]')
                    tpi['detail'] = self.detail_selector(detail_items)

                tpi_list.append(tpi)

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
