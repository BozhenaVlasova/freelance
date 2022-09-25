from selenium import webdriver
from selenium.webdriver.common.by import By
import re

driver = webdriver.Chrome()
driver.implicitly_wait(10)

arr = []
for i in range(1, 1000):
    driver.get(f'https://www.wildberries.ru/brands/fast?sort=popular&page={i}')
    end_page = driver.find_element(By.ID, 'divGoodsNotFound').get_attribute('class')
    if re.findall(r'hide', end_page) == []:
        break
    js_arr = driver.execute_script('''
    let cards = document.querySelectorAll('.product-card__main.j-card-link')
    let arr = []
    for (let card of cards) {{
        arr.push({'name': card.querySelector('.goods-name').innerText.replace(';', ' '),
        'priceU': card.querySelector('.price-old-block')?.innerText ? card.querySelector('.price-old-block').innerText.replace(/\s/g, '').replace('₽', '') : '0',
        'salePriceU': card.querySelector('.lower-price').innerText.replace(/\s/g, '').replace('₽', ''),
        'sale': card.querySelector('.product-card__sale')?.innerText ? card.querySelector('.product-card__sale').innerText.replace(/-/g, '') : '0%',
        'isNew': card.querySelector('.product-card__tip-new')?.innerText ? card.querySelector('.product-card__tip-new').innerText : 'OLD'})
    }}
    return arr
    ''')
    arr.append(js_arr)

all = sum(arr, [])

with open("file.csv", "w") as file:
    headers = 'name;priceU;salePriceU;sale;isNew;\n'
    file.write(headers)
    for i in all:
        data = [f"{i['name']};{i['priceU']};{i['salePriceU']};{i['sale']};{i['isNew']}"]
        for line in data:
            file.write(line)
            file.write('\n')