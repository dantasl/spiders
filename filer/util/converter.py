import csv
import json


# ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
months = ["01", "02"]
# [2016, 2017, 2018]
years = [2016]
model_two = ["uf", "cnpj_destinatario", "tipo_pessoa_emitente", "cnpj_cpf_emitente", "modelo_nota_fiscal",
             "data_emissao", "serie_nfe", "numero_nfe", "valor_total_nfe", "chave_acesso_nfe", "status_nota",
             "data_status_nota", "identificador_interno"]
model_six = ["cnae_cnpj_cpf_emitente", "cnae_codigo_atividade"]
model_five = ["socio_cnpj_cpf_emitente", "socio_cpf_socio_emitente", "socio_nome_socio", "socio_eh_adm"]
model_four = ["emissor_cnpj_cpf_emitente", "emissor_razao_social", "emissor_nome_fantasia", "emissor_endereco",
              "emissor_bairro", "emissor_cep", "emissor_cidade", "emissor_uf", "emissor_codigo_atividade",
              "emissor_data_inicio", "emissor_data_encerramento"]

for year in years:
    for month in months:
        receipt_in = "./receipts_json/receipt_{}{}.json".format(year, month)
        receipt_out = "./result/receipt_header_{}_{}{}.csv".format("two", year, month)
        with open(receipt_in, 'r') as inf:
            with open(receipt_out, 'w') as outf:
                json_data = json.load(inf)
                csv_format = csv.writer(outf)
                csv_format.writerow(
                    ["uf", "cnpj_destinatario", "tipo_pessoa_emitente", "cnpj_cpf_emitente", "modelo_nota_fiscal",
                     "data_emissao", "serie_nfe", "numero_nfe", "valor_total_nfe", "chave_acesso_nfe", "status_nota",
                     "data_status_nota", "identificador_interno", "ano_nota", "mes_nota"]
                )
                for item in json_data:
                    if list(item.keys())[0] in model_two:
                        csv_format.writerow([
                            item["uf"], item["cnpj_destinatario"], item["tipo_pessoa_emitente"],
                            item["cnpj_cpf_emitente"], item["modelo_nota_fiscal"], item["data_emissao"],
                            item["serie_nfe"], item["numero_nfe"], item["valor_total_nfe"], item["chave_acesso_nfe"],
                            item["status_nota"], item["data_status_nota"], item["identificador_interno"], year, month
                        ])
