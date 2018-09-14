import json


def json_treat(json_data):
    data_list = []
    for item in json_data:
        data = {}
        for key, value in item.items():
            data[key] = value.strip()  # Removes all white spaces before and after string
            if key == "valor_total_nfe" or key == "numero_nfe":
                data[key] = (value.strip()).lstrip("0")  # Removes all leading zeroes from value
        data_list.append(data)
    return data_list


months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
years = [2016, 2017, 2018]

for year in years:
    for month in months:
        receipt_in = "./receipts_json/receipts_{}{}.json".format(year, month)
        receipt_out = "./result/receipt_{}{}.json".format(year, month)
        with open(receipt_in, 'r') as inf:
            with open(receipt_out, 'w') as outf:
                json.dump(json_treat(json.load(inf)), outf)
