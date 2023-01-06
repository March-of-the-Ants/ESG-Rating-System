import scrapy
from news_search_esg.items import NewsSearchEsgItem
import pandas as pd
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import re


base_url='https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%s&sort=0&photo=0&field=0&pd=3&ds=2020.01.01&de=2021.12.31&cluster_rank=43&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20200101to20211231,a:all&start=%s'


#회사이름 불러오기
kosdaq_df=pd.read_csv(r'C:\Users\Choi\workspace\sesac\1212~final_project_ESG\news_search_esg\코스닥기업리스트_target.csv',encoding='cp949')
#cmp_name_list=list(kosdaq_df['회사명'])
kosdaq_df['대표자명'] = kosdaq_df['대표자명'].str.split('(').str[0]
kosdaq_df['회사명_대표자'] = kosdaq_df[['회사명', '대표자명']].agg(' '.join, axis=1)
cmp_ceo_list=list(kosdaq_df['회사명_대표자'])

class NewsEsgSpider(scrapy.Spider):
    name = 'news_esg'
    #allowed_domains = ['search.naver.com']
    #start_urls = ['http://search.naver.com/']
    headers = {"user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}


    def start_requests(self):
        for cmp_ceo in cmp_ceo_list : # 회사명 검색 
            for page in range(1,100,10): # 각 회사별 페이지 지정(10개씩 기사 있음)->10p까지 크롤링 실행
                #print('요청한 url :',base_url %(cmp_ceo,page))
                yield scrapy.Request(base_url %(cmp_ceo,page),headers= self.headers,callback=self.parse_links,cb_kwargs=dict(keyword=cmp_ceo))
    
    
#각각의 네이버 뉴스 url 접속
    def parse_links(self,response,keyword):
        urls=response.xpath('/html/body/div[3]/div[2]/div/div[1]/section/div/div[2]/ul/li/div/div/div[1]/div[2]/a[2]/@href').getall() #li가 변함, 페이지별 네이버 뉴스url만 크롤링 
        for url in urls:
            print('뉴스개별 url',url)
            yield scrapy.Request(url, method='GET',headers=self.headers,callback=self.parse_articles, meta={'keyword':keyword,'url':url})



# 뉴스 url접속 후 데이터 크롤링
# 연예, 스포츠는 잘 안뽑힘 
    def parse_articles(self, response):
        #items=[]
        item=NewsSearchEsgItem()
        item['URL']=response.meta.get('url')
        item['Title'] =response.xpath('//*[@id="title_area"]/span/text()').get()
        item['WritedDate']=response.xpath('//*[@id="ct"]/div[1]/div[3]/div[1]/div/span/text()').get()
        contents=response.xpath('//*[@id="dic_area"]/text()').extract() #list
        item['Content']=''.join([re.sub('[^a-z가-힣ㄱ-ㅎ0-9., ]', '', content).strip() for content in contents])#불용어1차제거, 리스트 이어붙이기
        item['Keyword']=response.meta.get('keyword')
        print(item)
        yield item
       

        