# -*- coding: utf-8 -*-
import scrapy
from filer.items import FilerDetail


class FilerSpider(scrapy.Spider):
    name = 'filer'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        with open("./misc/receipt.txt") as file:
            data = file.read()
            size = len(data)
            charAt = 0
            while charAt < size:
                if data[charAt] == "2":
                    receipt = FilerDetail()
                    charAt += 1
                    receipt["uf"] = data[charAt:charAt + 2]
                    charAt += 2
                    receipt["cnpj_destinatario"] = data[charAt:charAt + 14]
                    charAt += 14
                    receipt["tipo_pessoa_emitente"] = data[charAt:charAt + 1]
                    charAt += 1
                    receipt["cnpj_cpf_emitente"] = data[charAt:charAt + 14]
                    charAt += 14
                    receipt["modelo_nota_fiscal"] = data[charAt:charAt + 2]
                    charAt += 2
                    receipt["data_emissao"] = data[charAt:charAt + 14]
                    charAt += 14
                    receipt["serie_nfe"] = data[charAt:charAt + 3]
                    charAt += 3
                    receipt["numero_nfe"] = data[charAt:charAt + 15]
                    charAt += 15
                    receipt["valor_total_nfe"] = data[charAt:charAt + 19]
                    charAt += 19
                    receipt["chave_acesso_nfe"] = data[charAt:charAt + 50]
                    charAt += 50
                    receipt["status_nota"] = data[charAt:charAt + 3]
                    charAt += 3
                    receipt["data_status_nota"] = data[charAt:charAt + 14]
                    charAt += 14
                    receipt["identificador_interno"] = data[charAt:charAt + 10]
                    charAt += 11  # Original 10 + 1 (that leads to the other position)
                    yield receipt
