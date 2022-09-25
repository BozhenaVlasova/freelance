import requests

arr = []
for i in range(1,1000):
    response = requests.get(f'https://catalog.wb.ru/brands/f/catalog?appType=1&brand=6455&couponsGeo=12,7,3,21&curr=rub&lang=ru&locale=by&reg=1&spp=25&page={i}').json()
    
    if response['data']['products'] == []:
        break

    for j in response['data']['products']:
        obj = {}
        obj['name'] = j['name']
        obj['priceU'] = int(j['priceU']/100)
        obj['salePriceU'] = int(j['salePriceU']/100)
        obj['sale'] = j['sale']
        if 'isNew' in j.keys():
            obj['isNew'] = 'true'
        else:
            obj['isNew'] = 'false'
        arr.append(obj)

with open("file.csv", "w") as file:
    headers = 'name;priceU;salePriceU;sale;isNew;\n'
    file.write(headers)
    for i in arr:
        data = [f"{i['name']};{i['priceU']};{i['salePriceU']};{i['sale']};{i['isNew']}"]
        for line in data:
            file.write(line)
            file.write('\n')