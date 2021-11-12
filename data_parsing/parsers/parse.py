import scrapydo

scrapydo.setup()

def parse_scrapy(spider, html_source_list, result):

    scrapydo.run_spider(spider, settings={
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    }, html_list = html_source_list, to_save = result)
