# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SimecCity(scrapy.Item):
    city_uf = scrapy.Field()
    city_name = scrapy.Field()
    city_id = scrapy.Field()


class SimecQuestion(scrapy.Item):
    municipio_uf = scrapy.Field()
    municipio_nome = scrapy.Field()
    municipio_id = scrapy.Field()
    questao11 = scrapy.Field()
    questao12 = scrapy.Field()
    questao13 = scrapy.Field()
