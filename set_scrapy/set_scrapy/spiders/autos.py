import scrapy
from selenium.webdriver import Chrome, ChromeOptions
from set_scrapy.items import AutoItem
from scrapy.utils.project import get_project_settings
from selenium import webdriver


class AutosSpider(scrapy.Spider):
    name = 'autos'
    
    def start_requests(self):
        settings = get_project_settings()
        driver_path = settings['CHROME_DRIVER_PATH']
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(driver_path, options=options)
        driver.get('https://www.tred.com/buy')
        
        code_box = driver.find_element_by_xpath("//*[@id='scrollDiv']/form/div[1]/div[2]/div[2]/input")
        code_box.send_keys('500')
        link_elements = driver.find_elements_by_xpath("//*[@id='cars']/div/div[2]/div[1]/div/div/div/div/div/a")

        for link in link_elements:
             yield scrapy.Request(link.get_attribute('href'), callback=self.parse)

        driver.quit()

    def parse(self, response, **kwargs):
        item = AutoItem()
        item['name'] = response.xpath("//h1[@class='bigger no-top-margin hidden-xs']/text()[3]").get()
        item['price'] = response.xpath('//*[@id="header-box"]/div/div/div[2]/div/div/h2/text()').get()
            


        yield item
