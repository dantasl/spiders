import json


def treat_date(date):
    return "{}/{}/{} {}:{}:{}".format(date[0:2], date[2:4], date[4:8], date[8:10], date[10:12], date[12:])


def treat_emissor(date):
    return "{}/{}/{}".format(date[0:2], date[2:4], date[4:8]) if len(date) > 1 else ""


def json_treat(json_data):
    data_list = []
    for item in json_data:
        data = {}
        for key, value in item.items():
            data[key] = value.strip()  # Removes all white spaces before and after string
            if key == "valor_total_nfe" or key == "numero_nfe":
                data[key] = (value.strip()).lstrip("0")  # Removes all leading zeroes from value
            if key.startswith("data"):
                data[key] = treat_date(value)
            if key.startswith("emissor_data"):
                data[key] = treat_emissor(value)
        data_list.append(data)
    return data_list


# ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
months = ["01", "02", "03", "04", "05", "06"]
# [2016, 2017, 2018]
years = [2018]

for year in years:
    for month in months:
        receipt_in = "./receipts_json/receipt_{}{}.json".format(year, month)
        receipt_out = "./result/receipt_{}{}.json".format(year, month)
        with open(receipt_in, 'r') as inf:
            with open(receipt_out, 'w') as outf:
                json.dump(json_treat(json.load(inf)), outf)
