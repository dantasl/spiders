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


class FilerDetailCnaes(scrapy.Item):
    cnae_cnpj_cpf_emitente = scrapy.Field()
    cnae_codigo_atividade = scrapy.Field()


class FilerPartner(scrapy.Item):
    socio_cnpj_cpf_emitente = scrapy.Field()
    socio_cpf_socio_emitente = scrapy.Field()
    socio_nome_socio = scrapy.Field()
    socio_eh_adm = scrapy.Field()


class FilerEmissor(scrapy.Item):
    emissor_cnpj_cpf_emitente = scrapy.Field()
    emissor_razao_social = scrapy.Field()
    emissor_nome_fantasia = scrapy.Field()
    emissor_endereco = scrapy.Field()
    emissor_bairro = scrapy.Field()
    emissor_cep = scrapy.Field()
    emissor_cidade = scrapy.Field()
    emissor_uf = scrapy.Field()
    emissor_codigo_atividade = scrapy.Field()
    emissor_data_inicio = scrapy.Field()
    emissor_data_encerramento = scrapy.Field()
    emissor_tipo_contribuinte = scrapy.Field()


