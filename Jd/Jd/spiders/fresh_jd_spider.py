# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.selector import Selector
from Jd.jd_items import JdItem
import os

class QuotesSpider(scrapy.Spider):
    name = "fresh"
    start_url = 'https://fresh.jd.com/'
    property_map={u"商品名称":'name', u"商品编号":'ID', u'商品毛重':'net_weight', u'重量':'weight', 
    u'商品产地':'place', u"原产地":'origin_place', u"分类":'category', u"国产/进口":'dome_import',
    u'品种':'variety', u'店铺':'shop_name', u'包装':'packing', u'烹饪建议':'cook'
    }
    pids = set()

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        if response.status==200:
            print response.url

        head_items = response.xpath("//script[contains(., 'navFirst')]/text()") #get link from <script>
        head_items_txt = head_items.extract_first()
        start = head_items_txt.find('data:') + 6
        end = head_items_txt.find("path: 'home/widget/fresh_fs'") - 5
        json_string = head_items_txt[start:end] #not a json
        #data = json.loads(json_string)
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', json_string)

        print len(urls)
 
        #with open('url.txt', 'w') as f:
        #    for url in urls: 
        #        f.write(url + os.linesep)

        for url in urls:
            if("https://search.jd.com/search?keyword=" in url):
                for i in range(1,101):
                    page_url = url + "&page=" + str(i*2-1)     
                    yield scrapy.Request(page_url,callback=self.parse_page)
            else: 
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
            if name in self.property_map:
                item1[self.property_map[name]] = value             
            else:
                print 'name'
        yield item1       
