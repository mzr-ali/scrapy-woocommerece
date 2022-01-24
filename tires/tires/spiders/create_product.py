import re

import scrapy
from itemloaders import ItemLoader
from scrapy.selector import Selector
from scrapyselenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from ..items import TiresItem
from ..utils import (login,
                     remove_tag,
                     spect_table,
                     USERNAME,
                     PASSWORD,
                     DOMAIN,
                     SCRAPING_URL
                     )

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53',
}


def get_list_of_Url(kword):
    list = kword.split('#')
    return list


def get_category(req_url):
    pattern = re.compile(r'brand=[0-9A-Z-a-z-]+', re.IGNORECASE | re.DOTALL | re.MULTILINE)
    result = pattern.findall(req_url)
    if len(result) > 0:
        cat = str(result[0]).split("=")[1]
        cat = cat.replace(' ', '-')
        return cat
    else:
        return ""


class CreateProductSpider(scrapy.Spider):
    name = 'create'
    allowed_domains = ['my.07zr.com', 'static.07zr.com']
    CAT_SET = ""
    cat_list = []
    cat_index = 0

    def __init__(self, keyword=None, category=None, **kwargs):
        self.url = keyword

        self.cat = category

    def start_requests(self):
        print(SCRAPING_URL)
        self.cat_list = get_list_of_Url(self.url)
        print("Urls Count: ", len(self.cat_list))
        yield SeleniumRequest(
            url=SCRAPING_URL,
            headers=header,
            callback=self.parse)

    def parse(self, response, **kwargs):

        category = ''
        try:
            category = response.meta['cats']
        except:
            category = ''
        driver = response.meta['driver']
        email_elem = response.css("#username_login")
        if email_elem:
            driver = login(driver, user=USERNAME, password=PASSWORD)
        if self.cat_index == 0:
            url = self.cat_list[self.cat_index]
            print('Current Url: ', url)
            category = get_category(url)
            self.cat_index += 1
            driver.get(url)

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
                dont_filter=True,
                meta={'cats': category}

            )
        if next_page:
            yield SeleniumRequest(
                url=f'{DOMAIN}{next_page}',
                headers=header,
                callback=self.parse,
                meta={"cats": category}
            )
        else:
            if self.cat_index <= len(self.cat_list) - 1:
                url = self.cat_list[self.cat_index]
                category = get_category(url)
                self.cat_index += 1

                yield SeleniumRequest(
                    url=url,
                    headers=header,
                    callback=self.parse,
                    meta={"cats": category})

    def parse_products(self, response):
        cats = response.meta['cats']
        item = TiresItem()
        loader = ItemLoader(
            item=item, selector=response, response=response)
        loader.add_xpath('ref', '(//div[@class="ref"])[1]/text()')
        loader.add_xpath('name', '(//div[@class="title"])[1]/text()')
        loader.add_xpath(
            'price', '(//div[contains(@class,"card row ")]/div[contains(@class,"col order-1")]/div/span)[1]/text()')
        loader.add_xpath(
            'regular_price',
            '(//div[contains(@class,"card row ")]/div[contains(@class,"col order-1")]/div/span)[1]/text()')
        loader.add_xpath(
            'stock',
            '(//div[contains(@class,"offre mb-3 ")])[1]/div[contains(@class,"col order-md-3 order")]/span[2]/text()')
        loader.add_xpath('image_path', '//img[contains(@class,"thumb ")]/@src')
        loader.add_xpath('type', 'simple')

        specst_table = response.xpath('//table[@class="table"]//tr')
        specs = {}
        for row in specst_table:
            attrib = remove_tag(row.xpath('.//td[1]/text()').get())
            value = remove_tag(row.xpath('.//td[2]/text()').get())
            specs[attrib] = value

        loader.add_value('description', spect_table(specs))
        loader.add_value('short_description', spect_table(specs))
        loader.add_value('cat', cats)
        yield loader.load_item()
