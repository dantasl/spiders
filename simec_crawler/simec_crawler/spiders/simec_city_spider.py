# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.exceptions import CloseSpider
from simec_crawler.items import SimecCity
from selenium import webdriver

class SimecCitySpider(scrapy.Spider):
    name = 'simec_city_spider'
    start_urls = ['http://simec.mec.gov.br/login.php']
    states = ["Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal", "Espírito Santo", "Goiás",
              "Maranhão", "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará", "Paraíba", "Paraná",
              "Pernambuco", "Piauí", "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia",
              "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'simec_crawler.pipelines.FileExporterJson': 300,
        }
    }

    def __init__(self, *args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=options)
        super(SimecCitySpider, self).__init__(*args, **kwargs)

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
        self.login_and_check(response)

        # Goes to list of cities
        self.driver.get("http://simec.mec.gov.br/par3/par3.php?modulo=principal/listaMunicipios&acao=A")
        time.sleep(5)

        # Loop through each state
        for state in self.states:
            state_options = self.driver.find_elements_by_xpath("//select[@name='estuf']/option")
            for option in state_options:
                if option.text == state:
                    option.click()
                    break
            time.sleep(1)
            self.driver.find_element_by_xpath("//input[@name='pesquisar']").click()
            time.sleep(5)

            # Loops through all cities available (sadly, simec will only show first page)
            states_table = self.driver.find_elements_by_xpath("//table[@id='listaMunicipiosTable']/tbody/tr")
            self.log("Entering now in loop cities mode...")
            for state in states_table:
                self.log("Looping...")
                city_item = SimecCity()
                city_item["city_uf"] = state.find_element_by_xpath("./td[2]").text
                city_item["city_name"] = state.find_element_by_xpath("./td[3]").text
                city_item["city_id"] = int(
                    "".join(filter(str.isdigit, state.find_element_by_xpath("./td[1]/a").get_attribute("href")))
                )
                yield city_item
