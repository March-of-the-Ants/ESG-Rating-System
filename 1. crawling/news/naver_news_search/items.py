# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSearchEsgItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title=scrapy.Field()
    #URL = scrapy.Field()
    WritedDate=scrapy.Field()
    Content=scrapy.Field()
    URL=scrapy.Field()
    Keyword=scrapy.Field()
    pass
