import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapyselenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from ..items import TiresItem
from ..utils import login, SCRAPING_URL, PASSWORD, USERNAME, DOMAIN

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53',
}


class TireCrawlerSpider(scrapy.Spider):
    name = 'update'
    allowed_domains = ['07zr.com']

    def __init__(self, keyword=None, category=None, **kwargs):
        self.url = keyword
        self.cat = category

    def start_requests(self):

        print(SCRAPING_URL)
        yield SeleniumRequest(
            url=SCRAPING_URL,
            headers=header,
            callback=self.parse
        )

    def parse(self, response):

        driver = response.meta['driver']
        email_elem = response.css("#username_login")
        if email_elem:
            driver = login(driver, user=USERNAME, password=PASSWORD)
        driver.get(self.url)

        WebDriverWait(driver, 30).until(
            lambda driver: driver.find_elements(By.XPATH, '//a[@class="title"]'))
        source_code = driver.page_source
        html = Selector(text=source_code)
        products = html.xpath('//a[@class="title"]')
        next_page = html.xpath(
            '//a[@class="page-link" and @aria-label="Next"]/@href').get()
        for product in products:
            link = product.xpath('.//@href').get()
            yield response.follow(
                url=f"{DOMAIN}{link}#details",
                cookies=driver.get_cookies(),
                callback=self.parse_products,
                dont_filter=True

            )
        if next_page:
            yield SeleniumRequest(
                url=f'{DOMAIN}{next_page}',
                headers=header,
                callback=self.parse
            )

    def parse_products(self, response):
        item = TiresItem()
        loader = ItemLoader(
            item=item, selector=response, response=response)
        loader.add_xpath('ref', '(//div[@class="ref"])[1]/text()')

        loader.add_xpath(
            'price', '(//div[contains(@class,"card row ")]/div[contains(@class,"col order-1")]/div/span)[1]/text()')
        loader.add_xpath(
            'regular_price',
            '(//div[contains(@class,"card row ")]/div[contains(@class,"col order-1")]/div/span)[1]/text()')
        loader.add_xpath(
            'stock',
            '(//div[contains(@class,"offre mb-3 ")])[1]/div[contains(@class,"col order-md-3 order")]/span[2]/text()')

        yield loader.load_item()
