from scrapy_redis.spiders import RedisSpider
from scrapy_splash import SplashRequest
from patest.items import TicketPriceItem


class MyRedisSpider(RedisSpider):

    redis_url = None

    def __init__(self , *args, **kwargs):
        super(MyRedisSpider, self).__init__(*args, **kwargs)

    @classmethod
    def update_settings(cls, settings):
        redis_settings = {
            "REDIS_URL": None,
            "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
            # "DUPEFILTER_CLASS" : "scrapy_redis.dupefilter.RFPDupeFilter",
            "DUPEFILTER_CLASS": "patest.spiders.DupeFilter.SplashAwareDupeFilter",
            # redis中数据类型为set时设置此项为True，默认为False
            "REDIS_START_URLS_AS_SET": False,
            # "ITEM_PIPELINES": {
            #     'scrapy_redis.pipelines.RedisPipeline': 300
            # }
        }
        # 子类的配置可以覆盖redis_settings
        # redis_url必须配置custom_settings或类变量中
        if cls.custom_settings is not None:
            cls.custom_settings = dict(redis_settings, **cls.custom_settings)
        else:
            cls.custom_settings = redis_settings
        if cls.redis_url is not None:
            cls.custom_settings["REDIS_URL"] = cls.redis_url
        settings.setdict(cls.custom_settings or {}, priority='spider')


class MySplashSpider(MyRedisSpider):

    name = "tprs"
    # allowed_domains = ["localhost"]

    # url = "http://localhost"
    redis_url = 'redis://:19951020@127.0.0.1:6379'
    redis_key = 'tpi_start'

    '''
        redis中存储的为set类型的公司名称，使用SplashRequest去请求网页。
        注意：不能在make_request_from_data方法中直接使用SplashRequest（其他第三方的也不支持）,会导致方法无法执行，也不抛出异常
        但是同时重写make_request_from_data和make_requests_from_url方法则可以执行
    '''
    # def make_request_from_data(self, data):
    #     '''
    #     :params data bytes, Message from redis
    #     '''
    #     company = bytes_to_str(data, self.redis_encoding)
    #     url = self.url+'/company/basic.jspx?company='+company
    #     return self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        return SplashRequest(url, callback=self.parse, args={'wait': 3, 'html': 1})

    def parse(self, response):
        tpi = TicketPriceItem()
        tpi['air_route'] = 'haha'
        tpi['date'] = '2018-10-10'
        print('haha')
        yield tpi


