import json
from datetime import datetime

import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess


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

    @staticmethod
    def parse_one_page(response):
        price = response.css(
            "#root > div > article > header > div:nth-child(2) > div > div:nth-child(2)::text").extract_first()
        details = response.css("#root > div > article > div > div > section.section-overview > div > ul > li").extract()
        if price is not None:
            record = {"price": price,
                      "details": details,
                      "url": response.request.url}
            real_estates.append(record)
            detailsy.append(details)



real_estates = []
detailsy = []
otodom_katowice = "https://www.otodom.pl/sprzedaz/mieszkanie/katowice/?nrAdsPerPage=72&page=1"
soup = BeautifulSoup(requests.get(otodom_katowice).text, 'html.parser')
pages_all = int(soup.select("#pagerForm > ul > li.pager-counter > strong")[0].text)
# pages_all = 1  # for test purposes
process = CrawlerProcess()
process.crawl(OtodomBot)
process.start()

filename = f"dump_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, 'w') as outfile:
    json.dump(real_estates, outfile)

print("Task finished")
