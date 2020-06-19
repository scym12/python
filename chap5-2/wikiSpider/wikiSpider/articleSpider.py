from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article

class ArticleSpider(CrawlSpider):
    name = 'articleItems'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [
        Rule(LinkExtractor(allow='(/wiki/)((?!:).)*$'), callback='parse_items', follow=True),
    ]

    # response객체에 해당 url의 모든 정보가 담겨있다. 
    # https://docs.scrapy.org/en/latest/topics/request-response.html#response-objects
    # response.url : 
    def parse_items(self, response):
        article = Article()
        article['url'] = response.url   
        # 태그가 h1인 항목의 text를 가져온다.
        article['title'] = response.css('h1::text').get()
        # 태그가 div이고 id가 mw-content-text 인 텍스트의 모든 값을 가져온다.
        # http://sooyoung32.github.io/dev/2016/02/07/scrapy-tutorial.html
        # https://docs.scrapy.org/en/1.0/topics/selectors.html#topics-selectors
        article['text'] = response.xpath('//div[@id="mw-content-text"]//text()').getall()
        # 태그가 li이고 id가 footer-info-lastmo 인 항목의 text를 가져온다.
        lastUpdated = response.css('li#footer-info-lastmo::text').get()
        article['lastUpdated'] = lastUpdated.replace('This page was last edited on ', '')
        return articlex
