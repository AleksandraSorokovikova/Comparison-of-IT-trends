import scrapy
import logging
from tqdm import tqdm
from w3lib.html import strip_html5_whitespace as shw
import json

class save_object(object):

    def process_item(self, item, spider):
        spider.parsed_data.append(item)
        return item
    
class tprogerSpider(scrapy.Spider):
    
    name = "tproger"
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
        super(tprogerSpider, self).__init__(*args, **kwargs)
    
    def parse(self, response):
        time = response.xpath("//time[@class='localtime']/@datetime").get()
        comments = response.xpath("//a[@class='icon-comment-empty post-comment-count post-action-button hoverable']/text()").get()
        saved = response.xpath("//div[@class='icon-bookmark-empty hoverable post-bookmark post-action-button']/text()").get()
        if not comments:
            comments = 0
        if not time:
            time = response.xpath("//time[@class='timeago']/@datetime").get()
        if not saved:
            saved = 0
        
            
        yield {
                'time': time,
                'tags': response.xpath("//span[@itemprop='name']/text()").getall()[1:],
                'views': int(response.xpath("//span[@class='post-views-count icon-eye']/@data-count").get()),
                'comments': comments,
                'saved': saved
                }