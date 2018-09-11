# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.exceptions import CloseSpider
from simec_crawler.items import SimecQuestion
from selenium import webdriver


class SimecQuestionSpider(scrapy.Spider):
    name = 'simec_question_spider'
    start_urls = ['http://simec.mec.gov.br/login.php']
    custom_settings = {
        'ITEM_PIPELINES': {
            'simec_crawler.pipelines.FileExporterJson': 300,
        }
    }

    def __init__(self, *args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=options)
        super(SimecQuestionSpider, self).__init__(*args, **kwargs)

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
            "//span[@class='profile-info' and contains(., '')]"
        )
        if not has_username:
            raise CloseSpider("Error while authenticating.")
        self.log('Login successfully performed.')

    def treat_radio_button(self, question_id, value_id):
        buffer = self.driver.find_elements_by_xpath(
            "//input[@name='perg[{}]' and @checked='checked']".format(question_id)
        )
        if buffer:
            return "Sim" if buffer[0].get_attribute("value") == value_id else "Não"
        return "-"

    def parse(self, response):
        self.login_and_check(response)

        with open("./results/states/.json", "r", encoding="utf-8",) as data_cities:
            data = json.load(data_cities)
            for field in data:
                q_item = SimecQuestion()
                q_item["municipio_uf"] = field['city_uf']
                q_item["municipio_nome"] = field['city_name']
                q_item["municipio_id"] = field['city_id']

                # Goes to strategic questions for an specific city
                self.driver.get(
                    "http://simec.mec.gov.br/par3/par3.php?modulo=principal/planoTrabalho/questoesEstrategicas&acao=A"
                    "&inuid={}".format(field['city_id'])
                )
                self.log("Waiting for Strategic Questions to load...")
                time.sleep(3)

                # Create dicts for questions
                q11, q12 = {}, {}

                # Extract question 11
                self.driver.execute_script("javascript: quest.atualizaTela(4546);")
                time.sleep(2)
                q11["a"] = self.treat_radio_button(4656, "6335")
                q11["b"] = self.treat_radio_button(4657, "6337")
                q11["c"] = self.treat_radio_button(4658, "6339")
                q11["d"] = self.treat_radio_button(4659, "6341")
                q_item["questao11"] = q11

                # Extract question 12
                self.driver.execute_script("javascript: quest.atualizaTela(4549);")
                time.sleep(3)
                q12["a"] = self.treat_radio_button(4660, "6344")
                q12["b"] = self.treat_radio_button(4661, "6346")
                q12["c"] = self.treat_radio_button(4662, "6348")
                q12["d"] = self.treat_radio_button(4663, "6350")
                q12["e"] = self.treat_radio_button(4664, "6352")
                q12["f"] = self.treat_radio_button(4665, "6354")
                q12["g"] = self.treat_radio_button(4666, "6356")
                q_item["questao12"] = q12

                # Extract question 13
                self.driver.execute_script("javascript: quest.atualizaTela(4888);")
                time.sleep(3)
                q_item["questao13"] = self.treat_radio_button(4888, "6672")

                yield q_item
