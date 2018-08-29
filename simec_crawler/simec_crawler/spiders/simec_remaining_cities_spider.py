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
    custom_settings = {
        'ITEM_PIPELINES': {
            'simec_crawler.pipelines.FileExporterJson': 300,
        }
    }

    cidades4 = [
        "Registro",
        "Restinga",
        "Ribeira",
        "Ribeirão Bonito",
        "Ribeirão Branco",
        "Ribeirão Corrente",
        "Ribeirão do Sul",
        "Ribeirão dos Índios",
        "Ribeirão Grande",
        "Ribeirão Pires",
        "Ribeirão Preto",
        "Rifaina",
        "Rincão",
        "Rinópolis",
        "Rio Claro",
        "Rio das Pedras",
        "Rio Grande da Serra",
        "Riolândia",
        "Riversul",
        "Rosana",
        "Roseira",
        "Rubiácea",
        "Rubinéia",
        "Sabino",
    ]
    cidades5 = [
        "Suzanápolis",
        "Suzano",
        "Tabapuã",
        "Tabatinga",
        "Taboão da Serra",
        "Taciba",
        "Taguaí",
        "Taiaçu",
        "Taiúva",
        "Tambaú",
        "Tanabi",
        "Tapiraí",
        "Tapiratiba",
        "Taquaral",
        "Taquaritinga",
        "Taquarituba",
        "Taquarivaí",
        "Tarabai",
    ]
    cidades6 = [
        "Turmalina",
        "Ubarana",
        "Ubatuba",
        "Ubirajara",
        "Uchoa",
        "União Paulista",
        "Urânia",
        "Uru",
        "Urupês",
        "Valentim Gentil",
        "Valinhos",
        "Valparaíso",
        "Vargem",
        "Vargem Grande do Sul",
        "Vargem Grande Paulista",
        "Várzea Paulista",
        "Vera Cruz",
        "Vinhedo",
        "Viradouro",
        "Vista Alegre do Alto",
        "Vitória Brasil",
        "Votorantim",
        "Votuporanga",
        "Zacarias"
    ]

    def __init__(self, *args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=options)
        super(SimecRemainingCitiesSpider, self).__init__(*args, **kwargs)

    def login_and_check(self, response):
        # Performs login to the site
        self.driver.get(response.url)
        self.driver.find_element_by_id("usucpf").send_keys("007.391.501-70")
        self.driver.find_element_by_id("ususenha").send_keys("temp240718")
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

        for cidade in self.cidades4:
            # Goes to list of cities
            self.driver.get("http://simec.mec.gov.br/par3/par3.php?modulo=principal/listaMunicipios&acao=A")
            time.sleep(3)

            # Goes to specific state
            state_options = self.driver.find_elements_by_xpath("//select[@name='estuf']/option")
            for option in state_options:
                if option.text == "São Paulo":
                    option.click()
                    break
            time.sleep(1)

            # Searches for city
            self.driver.find_element_by_id("mundescricao").send_keys(cidade)
            self.driver.find_element_by_xpath("//input[@name='pesquisar']").click()
            time.sleep(2)

            # Get information on the city
            city_item = SimecCity()
            city_item["city_uf"] = self.driver.find_element_by_xpath(
                "//table[@id='listaMunicipiosTable']/tbody/tr/td[2]"
            ).text
            city_item["city_name"] = self.driver.find_element_by_xpath(
                "//table[@id='listaMunicipiosTable']/tbody/tr/td[3]"
            ).text
            city_item["city_id"] = int(
                "".join(filter(str.isdigit, self.driver.find_element_by_xpath(
                    "//table[@id='listaMunicipiosTable']/tbody/tr/td[1]/a"
                ).get_attribute("href")))
            )
            yield city_item
