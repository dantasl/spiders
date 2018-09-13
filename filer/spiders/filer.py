# -*- coding: utf-8 -*-
import scrapy
from filer.items import FilerDetail
from filer.items import FilerDetailCnaes
from filer.items import FilerPartner
from filer.items import FilerEmissor


class FilerSpider(scrapy.Spider):
    name = 'filer'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        with open("./docs/receipt.txt") as file:
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
                elif data[charAt] == "6":
                    charAt += 1
                    receipt = FilerDetailCnaes()
                    receipt["cnae_cnpj_cpf_emitente"] = data[charAt:charAt + 14]
                    charAt += 14
                    receipt["cnae_codigo_atividade"] = data[charAt:charAt + 7]
                    charAt += 8  # Original 7 + 1
                    yield receipt
                elif data[charAt] == "5":
                    charAt += 1
                    receipt = FilerPartner()
                    receipt["socio_cnpj_cpf_emitente"] = data[charAt:charAt + 14]
                    charAt += 14
                    receipt["socio_cpf_socio_emitente"] = data[charAt:charAt + 14]
                    charAt += 14
                    receipt["socio_nome_socio"] = data[charAt:charAt + 60]
                    charAt += 60
                    receipt["socio_eh_adm"] = data[charAt:charAt + 1]
                    charAt += 2  # Original 1 + 1
                    yield receipt
                elif data[charAt] == "4":
                    charAt += 1
                    receipt = FilerEmissor()
                    receipt["emissor_cnpj_cpf_emitente"] = data[charAt:charAt + 14]
                    charAt += 14
                    receipt["emissor_razao_social"] = data[charAt:charAt + 100]
                    charAt += 100
                    receipt["emissor_nome_fantasia"] = data[charAt:charAt + 50]
                    charAt += 50
                    receipt["emissor_endereco"] = data[charAt:charAt + 80]
                    charAt += 80
                    receipt["emissor_bairro"] = data[charAt:charAt + 50]
                    charAt += 50
                    receipt["emissor_cep"] = data[charAt:charAt + 8]
                    charAt += 8
                    receipt["emissor_cidade"] = data[charAt:charAt + 50]
                    charAt += 50
                    receipt["emissor_uf"] = data[charAt:charAt + 2]
                    charAt += 2
                    receipt["emissor_codigo_atividade"] = data[charAt:charAt + 8]
                    charAt += 8
                    receipt["emissor_data_inicio"] = data[charAt:charAt + 8]
                    charAt += 8
                    receipt["emissor_data_encerramento"] = data[charAt:charAt + 8]
                    charAt += 8
                    endIter = 0
                    beginIter = charAt
                    while data[beginIter:charAt + endIter + 1] != "\n":
                        endIter += 1
                        beginIter += 1
                    receipt["emissor_tipo_contribuinte"] = data[charAt:charAt + endIter]
                    charAt += endIter + 1
                    yield receipt
