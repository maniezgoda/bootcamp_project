import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import requests


class OtodomBot(scrapy.Spider):
    name = "otodom_scraper"

    def start_requests(self):
        base = "https://www.otodom.pl/sprzedaz/mieszkanie/katowice/?nrAdsPerPage=72&page="
        for page_number in range(1, pages_all+1):
            url = base+str(page_number)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urls = response.css("div.offer-item-details > header > h3 > a::attr(href)").extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_one_page)

    def parse_one_page(self, response):
        price = response.css("#root > div > article > div:nth-child(1) > header > div.css-15n3v4t-AdHeader-className "
                             "> div.css-7ryazv-AdHeader-className::text").extract_first()
        details = response.css("#root > div > article > div.css-1uapnya-AdPage-className > "
                               "div.css-pvzbw2-AdPage-className > section.section-overview > div > ul > li").extract()
        if price is not None:
            record = {"price": price,
                      "details": details,
                      "url": response.request.url}
            real_estates.append(record)
            detailsy.append(details)


real_estates = []
detailsy = []
# otodom_katowice = "https://www.otodom.pl/sprzedaz/mieszkanie/katowice/?nrAdsPerPage=72&page=1"
# soup = BeautifulSoup(requests.get(otodom_katowice).text, 'html.parser')
# pages_all = int(soup.select("#pagerForm > ul > li.pager-counter > strong")[0].text)
pages_all = 2  # for test purposes
process = CrawlerProcess()
process.crawl(OtodomBot)
process.start()

