from scrapy.selector import Selector
import datetime

test = open('/Users/liangzx/Downloads/flights.ctrip.com-3.txt', 'r', encoding='utf-8')
teststr = test.read()
site = Selector(text=teststr)


start, end = '2018-12-01', '2018-12-30'
d1, d2 = datetime.datetime.strptime(start, '%Y-%m-%d'), datetime.datetime.strptime(end, '%Y-%m-%d')
diff = d2 - d1


daterange = []
tmpdate = d1
for i in range(diff.days + 1):
    daterange.append(str(tmpdate.date()))
    tmpdate += datetime.timedelta(days=1)
print(daterange)


items = site.css('.tbContent').xpath('.//tr')
print(len(items))

for i in range(len(daterange)-1, -1, -1):
    ddd = items.xpath('.//td[@data-time="{}"]'.format(daterange[i]))
    if len(ddd.xpath('.//div')) > 1:
        price = ''.join(ddd.xpath('.//div[2]/text()').extract()).replace('\n', '')
        print(daterange[i], int(price))
        daterange.pop(i)
print(daterange)




# items = site.xpath('//div[@class="flight-item   "]').extract()
# items = site.xpath('//div[contains(@class, "flight-item")]')
# print(len(items))
#
# for item in items:
#     # # 提取航司名称
#     # airline_item = item.xpath('.//div[@class="airline-name"]')
#     # base_item = airline_item.xpath('strong/text()')
#     # if base_item:
#     #     extra_airline = airline_item.xpath('span/text()').extract_first()
#     #     print(base_item.extract_first() + extra_airline)
#     # else:
#     #     airline_name = airline_item.xpath('./text()').extract_first().replace(' ', '').replace('\n', '')
#     #     print(airline_name)
#     #
#     # # 提取航班号与机型
#     # flight_no_item = item.xpath('.//div[@class="flight-No"]')
#     # plane_type = flight_no_item.css('.abbr::text').extract_first()
#     # print(plane_type)
#     # flight_no = flight_no_item.xpath('./text()').extract_first().replace(' ', '').replace('\n', '')
#     # print(flight_no)
#
#     #
#     # flight_time = item.css('.flight-detail-time::text').extract()
#     # depart_time = flight_time[0].replace(' ', '').replace('\n', '')
#     # arr_time = flight_time[1].replace(' ', '').replace('\n', '')
#     # print(depart_time + " " + arr_time)
#     # depart_airport = item.css('.flight-detail-depart').css('.flight-detail-airport::text').extract_first().replace(' ', '').replace('\n', '')
#     # arr_airport = item.css('.flight-detail-return').css('.flight-detail-airport::text').extract_first().replace(' ', '').replace('\n', '')
#     # print(depart_airport + " " + arr_airport)
#     # more_info = item.css('.flight-col-more')
#     # total_time = more_info.css('.flight-total-time::text').extract_first().replace(' ', '').replace('\n', '')
#     # stop_info = more_info.css('.flight-stop-info::text').extract_first().replace(' ', '').replace('\n', '')
#     # print(total_time + " " + stop_info)
#
#     flight_detail_sections = item.css('.flight-detail-section')
#     for fds in flight_detail_sections:
#
#         airline_name = fds.css('.section-flight-base').xpath('./text()[not(parent::span)]').extract_first()
#         print(airline_name)
#
#         flight_no = fds.css('.flight-No::text').extract_first()
#         print(flight_no)
#
#         plane_type = fds.css('.abbr::text').extract_first()
#         print(plane_type)
#
#         flight_time = fds.xpath('.//span[contains(@class, "section-time")]/text()').extract()
#         print(flight_time)
#
#         airports = fds.css('.section-airport::text').extract()
#         print(airports)
#
#         section_total_time = fds.css('.section-duration::text').extract_first()
#         print(section_total_time)
#
#     total_time = item.css('.flight-total-time::text').extract_first().replace(' ', '').replace('\n', '')[1:]
#     print(total_time)
#
#     seat_lowest_price = item.xpath('.//div[contains(@class, "seat-row")]')[0]
#     seat_type = seat_lowest_price.css('.seat-type ::text').extract_first().replace('\n', ' ').replace(' ', '')
#     print(seat_type)
#     price = seat_lowest_price.css('.mb5').css('span')[1].xpath('./text()[not(parent::dfn)]').extract_first()
#     # price = seat_lowest_price.xpath('string(.//span[@class="price"])').extract_first()
#     print(price)
#
#     print("******************************")


