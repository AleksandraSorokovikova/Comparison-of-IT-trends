import scrapy
import logging
from tqdm import tqdm
from w3lib.html import strip_html5_whitespace as shw
import json

class save_object(object):

    def process_item(self, item, spider):
        spider.parsed_data.append(item)
        return item
    
class career_habrSpider(scrapy.Spider):
    
    name = "career_habr"
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
        super(career_habrSpider, self).__init__(*args, **kwargs)
    
    def parse(self, response):
        yield {
                'time': response.xpath("//time[@class='basic-date']/@datetime").get(),
                'name': response.xpath("//h1[@class='page-title__title']/text()").get(),
                'skills': response.xpath("//a[@class='link-comp link-comp--appearance-dark']/text()").getall()[:-1],
                  }