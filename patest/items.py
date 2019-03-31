# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TicketPriceItem(scrapy.Item):

    air_route = scrapy.Field()

    date = scrapy.Field()

    low_price = scrapy.Field()

    detail = scrapy.Field()

# class TicketPriceItem(scrapy.Item):
#     # transfer count
#     transfer_count = scrapy.Field()
#
#     # airline name, can be more than one
#     airline_name = scrapy.Field()
#
#     # flight number, may appear "several flight number"
#     flight_No = scrapy.Field()
#
#     # type of plane, may be none due to flight number
#     plane_type = scrapy.Field()
#
#     # flight section time
#     flight_time = scrapy.Field()
#
#     airports = scrapy.Field()
#
#     section_total_time = scrapy.Field()
#
#     total_time = scrapy.Field()
#
#     seat_type = scrapy.Field()
#
#     price = scrapy.Field()
#
#     seat_only = scrapy.Field()
