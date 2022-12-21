import scrapy
from newscrawling.items import NewscrawlingItem
import pandas as pd

class NewsSpider(scrapy.Spider):
    name = 'Newsbot'
    base_url = 'https://search.daum.net/search?nil_suggest=sugsch&w=news&q='
    kosdaq = pd.read_excel("C:/Users/hanah/my-venv/newscrawling/newscrawling/spiders/kosdaq_report.xlsx")
    kosdaq['대표자명'] = kosdaq['대표자명'].str.split('(').str[0]
    kosdaq['회사명_대표자'] = kosdaq[['회사명', '대표자명']].agg(' '.join, axis=1)
    pages = list(range(1, 10))

    def start_requests(self):
        for keyword in self.kosdaq['회사명_대표자']:
            for page in self.pages:
                params = f'{keyword}&period=u&sd=20200101000000&ed=20211231235959&p={page}'
                yield scrapy.Request(url=self.base_url + params, callback=self.parse_links, cb_kwargs=dict(keyword=keyword))

    def parse_links(self, response, keyword):
        dates = response.css('span.cont_info > span::text').get()
        urls = response.xpath('//*[@id="newsColl"]/div[1]/ul/li/div/span[1]/a[2]/@href').extract()
        for url in urls:
            print(url)
            yield scrapy.Request(url, callback=self.parse_articles, meta={'dates':dates, 'keyword':keyword})

    def parse_articles(self, response):
        item = NewscrawlingItem()
        articles = response.css('div.article_view > section > p::text').extract()
        item['articles'] = ''.join(article.strip() for article in articles)
        item['titles'] = response.css('#mArticle > div.head_view > h3::text').extract()
        item['dates'] = response.meta.get('dates')
        item['categories'] = response.meta.get('keyword')
        yield item
