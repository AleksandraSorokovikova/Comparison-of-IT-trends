import scrapy
import logging
from tqdm import tqdm
import pandas as pd
from w3lib.html import strip_html5_whitespace as shw
import json
import re

class save_object(object):

    def process_item(self, item, spider):
        spider.parsed_data.append(item)
        return item

class stepikSpider(scrapy.Spider):
    
    name = "stepik"
    start_urls = []
    parsed_data = []
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {save_object: 0},
        'LOG_STDOUT' : True
    }
    
    
    def __init__(self, html_list, to_save, *args, **kwargs):
        self.start_urls = tqdm(html_list)
        self.parsed_data = to_save
        super(stepikSpider, self).__init__(*args, **kwargs)
    
    def parse(self, response):
        
        price = '0'
        try:
            price = re.sub('(<.*?>)|(\n)|(About this course)', '', response.xpath('//span[@class="format-price"]').get())
        except:
            pass
        
        time = []
        time = re.findall('upload_date(.*?),', response.xpath('//script[contains(., "__stepik_shoebox__")]/text()').get())
        if (time == []):
            time = re.findall('create_date(.*?),', response.xpath('//script[contains(., "__stepik_shoebox__")]/text()').get())
        try:
            time = re.sub(r'\\u002.', '', time[0])[1:10]
        except:
            pass
        yield {
            'time': time,
            'name': response.xpath("//h1[@class='course-promo__header']/text()").get(),
            'description': re.sub('(<.*?>)|(\n)|(About this course)', '', response.xpath("//section[@class='course-promo__content-block']").get()).lower(),
            'participants': shw(response.xpath('//div[@class="course-promo-summary__students"]/text()').get())[:-8],
            'price': price,
        }
        