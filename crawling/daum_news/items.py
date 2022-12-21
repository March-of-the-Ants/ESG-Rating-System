# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NewscrawlingItem(scrapy.Item):
    categories = scrapy.Field()
    media = scrapy.Field()
    titles = scrapy.Field()
    urls = scrapy.Field()
    photo_urls = scrapy.Field()
    dates = scrapy.Field()
    articles = scrapy.Field()
    comment_urls = scrapy.Field()
    comments = scrapy.Field()
    users = scrapy.Field()
    userIDs = scrapy.Field()
    pass
