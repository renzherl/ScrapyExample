import scrapy
from ScrapyExample.jd_items import JdItem

class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["search.jd"]
    start_urls = [
        "https://search.jd.com/Search?keyword=monitor&enc="+
        "utf-8&suggest=3.his.0.0&pvid=3c0df64a9a3544c0aea06d3f5c3a30a8"
    ]

    def parse(self, response):
        for sel in response.xpath('//ul[@class="gl-warp clearfix"]/li/div[@class="gl-i-wrap"]'):
            item = JdItem()
            item['name'] = sel.xpath('.//div[@class="p-name p-name-type-2"]//em/text()').extract()
            item['price'] = sel.xpath('.//div[@class="p-price"]/strong/i/text()').extract()
            yield item