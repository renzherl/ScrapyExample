# -*- coding: utf-8 -*-
import scrapy
import scrapy
import re
import json
from scrapy.selector import Selector
import os

class QuotesSpider(scrapy.Spider):
    name="miapp"
    
    def start_requests(self):
        start_url=[
            "http://app.mi.com/searchAll?keywords=%E5%A9%9A%E6%81%8B%E4%BA%A4%E5%8F%8B&typeall=phone&page=1",
            "http://app.mi.com/searchAll?keywords=%E5%A9%9A%E6%81%8B%E4%BA%A4%E5%8F%8B&typeall=phone&page=2",
            "http://app.mi.com/searchAll?keywords=%E5%A9%9A%E6%81%8B%E4%BA%A4%E5%8F%8B&typeall=phone&page=3",
        ]
        for url in start_url:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
            if response.status==200:
                print response.url
            sel = Selector(response)
            app_uls = sel.xpath('//ul[@class="applist"]/li')
            for app_li in app_uls:
                app_name = app_li.xpath('h5/a/text()').extract_first().strip()
                app_package_url = app_li.xpath('h5/a/@href').extract_first()
                app_package = re.search('id=(.+?)&ref=',app_package_url).group(1)
                print(app_package)
                print(app_name)
                yield{
                    'p':app_package,
                    'n':app_name
                }

         
