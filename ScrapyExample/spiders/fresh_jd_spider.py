
# -*- coding: utf-8 -*-

import scrapy
import re
import json
from scrapy.selector import Selector
from ScrapyExample.jd_items import JdItem

class QuotesSpider(scrapy.Spider):
    name = "fresh"
    start_url = 'https://fresh.jd.com/'
    property_map={}

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        if response.status==200:
            print response.url
        pids = set()
        
        head_items = response.xpath("//script[contains(., 'navFirst')]/text()") #get link from <script>
        head_items_txt = head_items.extract_first()
        start = head_items_txt.find('data:') + 6
        end = head_items_txt.find("path: 'home/widget/fresh_fs'") - 5
        json_string = head_items_txt[start:end] #not a json
        #data = json.loads(json_string)
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', json_string)

        print len(urls)

        for url in urls:
             yield scrapy.Request(url,callback=self.parse_page)    
    
    def parse_page(self, response):
        print response.url
        sel = Selector(response)
        goods = sel.xpath('//li[@class="gl-item"]')
        print len(goods) # 60 goods per page
        for good in goods:
           item1 = JdItem()
           item1['ID'] = good.xpath('./div/@data-sku').extract()
           item1['name'] = good.xpath('./div/div[@class="p-name"]/a/em/text()').extract()
           item1['shop_name'] = good.xpath('./div/div[@class="p-shop"]/@data-shop_name').extract()
           item1['link'] = good.xpath('./div/div[@class="p-img"]/a/@href').extract()
           url = "http:" + item1['link'][0] + "#comments-list"
           yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_detail)

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
            if name == u'重量':
                item1['weight'] = value
            elif name == u'商品毛重':
                item1['net_weight'] = value
            elif name == u'商品产地':
                item1['place'] = value
            elif name == u"原产地":
                item1['origin_place'] = value
            elif name == u"分类":
                item1['category'] = value
            elif name == u"国产/进口":
                item1['dome_import'] = value
            elif name == u"商品名称":
                item1['name'] = value
            elif name == u"商品编号":
                item1['ID'] = value
            else:
                print 'name'
            yield item1       
