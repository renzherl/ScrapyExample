# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.selector import Selector
from Suning.items import SuningItem
import os

class SunningSpider(scrapy.Spider):
    name="suning"
    start_url = 'https://search.suning.com/'
    query = []

    def load_query(self):
        query = [u"海尔冰箱"]
        self.query = query

    def start_requests(self):
        self.load_query()
        for q in self.query:
            page_url = self.start_url + q + '/'
            print page_url
        yield scrapy.Request(url=page_url, callback=self.parse_page)

    def parse_page(self, response):
        if response.status==200:
            print response.url
        sel = Selector(response)
        product_list = sel.xpath('//ul[@class="general clearfix"]/li')
        for product in product_list:
           item1 = SuningItem()                 
           item1['name'] = product.xpath('./div/div/div[@class="res-info"]/div[@class="title-selling-point"]/a/@title').extract()
           item1['link'] = product.xpath('./div/div/div[@class="res-img"]/div/a/@href').extract()[0]
           yield scrapy.Request(url=item1['link'], meta={'item': item1}, callback=self.parse_detail)

    def parse_detail(self, response):
        item1 = response.meta['item']
        sel = Selector(response)
        #brand = sel.xpath('//ul[@id="parameter-brand"]/li/a/text()').extract()
        yield item1      
