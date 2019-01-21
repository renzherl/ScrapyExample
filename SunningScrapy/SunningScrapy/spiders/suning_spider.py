# -*- coding: utf-8 -*-

import scrapy
import re
import json
from scrapy.selector import Selector
from SunningScrapy.items import SunningscrapyItem
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
        product_list = sel.css('div#id::product-list').extract
        print(product_list)
        goods = []
        print len(goods) # 60 goods per page
        for good in goods:
           item1 = SunningscrapyItem()                 
           item1['name'] = good.xpath('./div/div[@class="p-name"]/a/em/text()').extract()
           item1['category'] = good.xpath('./div/div[@class="p-shop"]/@data-shop_name').extract()
           item1['link'] = good.xpath('./div/div[@class="p-img"]/a/@href').extract()
           url = "http:" + item1['link'][0] + "#comments-list"
           #yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_detail)

    def parse_detail(self, response):
        item1 = response.meta['item']
        sel = Selector(response)
        brand = sel.xpath('//ul[@id="parameter-brand"]/li/a/text()').extract()
        item1['brand'] = brand
        intros = sel.xpath('//ul[@class="parameter2 p-parameter-list"]/li')
        for intro in intros:
            text = intro.xpath('text()').extract()
            text_s = ''.join(text)
            name, value = text_s.split(u'：')
            if name in self.property_map:
                item1[self.property_map[name]] = value             
            else:
                print 'name'
        yield item1      
