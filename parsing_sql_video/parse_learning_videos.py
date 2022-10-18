import time, re
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.implicitly_wait(2)

driver.get('https://www.obuka.org/course/go-it-qa-engineer/33195-1-it-specialisty-i-programmnyy-produkt-kto-takie-i-chto-takoe-chast-1/')
r = 0
while True:
    driver.find_elements(By.XPATH, "//li[@class='jump']")[1].click()
    time.sleep(2)
    res2 = driver.execute_script('''
    let arr = []
    let a = document.querySelectorAll("[class*='page']")
    for (let b of a) {{
        arr.push(Number(b.innerText))
    }}
    return arr
    ''')
    if max(res2) > r:
        r = max(res2)
    else:
        break

for i in range(1,r+1):
    driver.get(f'https://www.obuka.org/course/go-it-qa-engineer/33195-1-it-specialisty-i-programmnyy-produkt-kto-takie-i-chto-takoe-chast-1/?mode=async&function=get_block&block_id=list_videos_channel_videos&sort_by=dvd_sort_id&p=0{i}')
    main_ = driver.find_element(By.ID, 'list_videos_channel_videos_items')
    a = main_.find_elements(By.CLASS_NAME ,'item  ')
    count = 0
    while count<len(a):
        main_ = driver.find_element(By.ID, 'list_videos_channel_videos_items')
        a = main_.find_elements(By.CLASS_NAME ,'item  ')
        a[count].click()
        name = driver.find_element(By.XPATH, "//div[@class='headline']/h1").text
        n = re.findall(r'-\s\d+.*', name)[0]
        url = driver.find_element(By.CLASS_NAME, 'fp-engine').get_attribute('src')
        print(f'{n}:\n{url}')
        driver.back()
        count += 1