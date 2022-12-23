import scrapy
from newscrawling.items import NewscrawlingItem
import pandas as pd

class NewsSpider(scrapy.Spider):
    name = 'Naverbot'
    base_url = 'https://m.search.naver.com/search.naver?where=m_news&query='
    headers = {"user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}

    kosdaq = pd.read_excel("C:/Users/hanah/my-venv/newscrawling/newscrawling/spiders/kosdaq_report.xlsx")
    kosdaq['대표자명'] = kosdaq['대표자명'].str.split('(').str[0]
    kosdaq['회사명_대표자'] = kosdaq[['회사명', '대표자명']].agg(' '.join, axis=1)
    pages = list(range(1, 62, 15))

    def start_requests(self):
        for keyword in self.kosdaq['회사명_대표자']:
            for page in self.pages:
                params = f'{keyword}&nso=so%3Ar%2Cp%3Afrom20200101to20211231&start={page}'
                yield scrapy.Request(url=self.base_url + params, headers= self.headers, callback=self.parse_links, cb_kwargs=dict(keyword=keyword))

    def parse_links(self, response, keyword):
        dates = response.xpath('//*[@id="news_result_list"]/li/div/div[1]/div[2]/span/text()').get()
        urls = response.xpath('//*[@id="news_result_list"]/li/div/a/@href').extract()
        for url in urls:
            if 'https://n.news.naver.com/article/' in url:
                print(url)
                yield scrapy.Request(url, headers= self.headers, callback=self.parse_articles, meta={'dates':dates, 'keyword':keyword})

    def parse_articles(self, response):
        item = NewscrawlingItem()
        articles = response.css('#dic_area::text').extract()
        item['articles'] = ''.join(article.strip() for article in articles)
        item['titles'] = response.xpath('//*[@id="title_area"]/span/text()').extract()
        item['dates'] = response.meta.get('dates')
        item['categories'] = response.meta.get('keyword')
        yield item
