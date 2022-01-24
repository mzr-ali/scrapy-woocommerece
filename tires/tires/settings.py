from webdriver_manager.chrome import ChromeDriverManager

BOT_NAME = 'tires'
SPIDER_MODULES = ['tires.spiders']
NEWSPIDER_MODULE = 'tires.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 10
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

ITEM_PIPELINES = {
    'tires.pipelines.TiresPipeline': 300,

}
DOWNLOADER_MIDDLEWARES = {
    'scrapyselenium.SeleniumMiddleware': 800,
}

DOWNLOAD_TIMEOUT = 1200
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = ChromeDriverManager().install()
SELENIUM_DRIVER_ARGUMENTS = ['--start-maximized']
