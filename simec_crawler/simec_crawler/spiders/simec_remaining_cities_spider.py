# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.exceptions import CloseSpider
from simec_crawler.items import SimecCity
from selenium import webdriver


class SimecRemainingCitiesSpider(scrapy.Spider):
    name = 'simec_remaining_cities_spider'
    start_urls = ['http://simec.mec.gov.br/login.php']

    def __init__(self, *args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=options)
        super(SimecRemainingCitiesSpider, self).__init__(*args, **kwargs)

    def login_and_check(self, response):
        # Performs login to the site
        self.driver.get(response.url)
        self.driver.find_element_by_id("usucpf").send_keys("")
        self.driver.find_element_by_id("ususenha").send_keys("")
        button_access = self.driver.find_element_by_xpath("//button[@type='submit' and contains(., 'Acessar')]")
        self.driver.execute_script("arguments[0].click();", button_access)
        time.sleep(5)

        # Checks if login is correct (i.e. the name of the expected user appears)
        has_username = self.driver.find_element_by_xpath(
            "//span[@class='profile-info' and contains(., 'JOSE ARIMATHEA VALENTE NETO')]"
        )
        if not has_username:
            raise CloseSpider("Error while authenticating.")
        self.log('Login successfully performed.')

    def parse(self, response):
        self.login_and_check()
