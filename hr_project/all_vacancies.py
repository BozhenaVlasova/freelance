from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.implicitly_wait(7)
driver.get('https://rabota.by/employer/89798?dpt=89798-89798-02&hhtmFrom=vacancy_search_list')

count = 0
c = 0
arr = []
title_all_vacancies = driver.find_elements(By.XPATH, "//button[@class='bloko-link bloko-link_with-icon bloko-link_pseudo']")

while count != len(title_all_vacancies)-1:
    try:
        count += 1
        title_all_vacancies = driver.find_elements(By.XPATH, "//button[@class='bloko-link bloko-link_with-icon bloko-link_pseudo']")
        title_all_vacancies[count].click()
        vacancies = driver.find_elements(By.XPATH, "//a[@data-qa='vacancy-serp__vacancy-title']")
        
        while c <= len(vacancies):
                vacancies = driver.find_elements(By.XPATH, "//a[@data-qa='vacancy-serp__vacancy-title']")
                vacancies[c].click()

                name_vacancy = driver.find_element(By.XPATH, "//h1[@data-qa='vacancy-title']")
                js_arr = driver.execute_script('''
                let all_data = document.querySelectorAll('[class*="wrapper-flat--"]')
                let arr = []
                for (let data of all_data) {{
                    arr.push({
                        'name': data.querySelector('[data-qa="vacancy-title"]').innerText,
                        'salary': data.querySelector('[data-qa="vacancy-salary"]').innerText,
                        'work_experience': `Требуемый опыт работы: ${data.querySelector('[data-qa="vacancy-experience"]').innerText}`,
                        'employment': data.querySelector('[data-qa="vacancy-view-employment-mode"]').innerText,
                        'how_many_watch': `Сейчас смотрят эту вакансию: ${data.querySelector(".vacancy-viewers-count")?.innerText ? data.querySelector(".vacancy-viewers-count").innerText.replace(/\s/g, '') : '0'}`,
                        'candidates': data.querySelector('[class*="badge-title-bold"]')?.innerText ? data.querySelector('[class*="badge--"]').innerText : '0'})
                }}
                return arr
                ''')

                arr.append(js_arr)
                c += 1

                driver.back()
                if len(vacancies) > 1 and c < len(vacancies):
                    count -= 1
                else:
                    c = 0
                break
    except:
        driver.refresh()
        count -=1

arr = sum(arr, [])