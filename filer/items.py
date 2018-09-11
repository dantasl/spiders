# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FilerDetail(scrapy.Item):
    uf = scrapy.Field()
    cnpj_destinatario = scrapy.Field()
    tipo_pessoa_emitente = scrapy.Field()
    cnpj_cpf_emitente = scrapy.Field()
    modelo_nota_fiscal = scrapy.Field()
    data_emissao = scrapy.Field()
    serie_nfe = scrapy.Field()
    numero_nfe = scrapy.Field()
    valor_total_nfe = scrapy.Field()
    chave_acesso_nfe = scrapy.Field()
    status_nota = scrapy.Field()
    data_status_nota = scrapy.Field()
    identificador_interno = scrapy.Field()
