import scrapy
from newscrawling.items import NewscrawlingItem
import pandas as pd

class NewsSpider(scrapy.Spider):
    name = 'Trainbot'
    headers = {"user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}

    def start_requests(self):
        kostat = pd.read_excel("C:/Users/hanah/my-venv/newscrawling/newscrawling/spiders/train_df.xlsx")
        urls = list(kostat.URL)
        for url in urls:
            yield scrapy.Request(url, headers= self.headers, callback=self.parse_articles, dont_filter=True)

    def parse_articles(self, response):
        item = NewscrawlingItem()
        articles = response.css('#dic_area::text').extract()
        item['articles'] = ''.join(article.strip() for article in articles)
        yield item
