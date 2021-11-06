import scrapy
import logging
from tqdm import tqdm
from w3lib.html import strip_html5_whitespace as shw
import json

class save_object(object):

    def process_item(self, item, spider):
        spider.parsed_data.append(item)
        return item

class habrSpider(scrapy.Spider):
    
    name = "habr"
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
        super(habrSpider, self).__init__(*args, **kwargs)
    
    def parse(self, response):
        
        saved = -1
        comments = -1
        views = -1
        
        
        try:
            raw_json = json.loads(response.xpath('//script[contains(., "window.__INITIAL_STATE__=")]/text()').get()[25:-122])['articlesList']['articlesList']
            raw_json = raw_json[str(list(raw_json.keys())[0])]['statistics']
            saved = raw_json['favoritesCount']
            comments = raw_json['commentsCount']
            views = raw_json['readingCount']
        except:
            pass
        
        if saved == -1 or comments == -1 or views == -1:
            pass
        else:
            yield {
                    'time': shw(response.xpath("//span[@class='tm-article-snippet__datetime-published']/time/@datetime").get()),
                    'tags': [shw(result.lower())
                         for result in response.xpath("//a[@class='tm-tags-list__link']/text()").getall()],
                    'habs': [shw(result.lower())
                         for result in response.xpath("//a[@class='tm-hubs-list__link']/text()").getall()],
                    'saved': saved,
                    'comments': comments,
                    'views': views,
                  }
        
