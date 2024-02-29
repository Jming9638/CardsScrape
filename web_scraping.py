import time
import pandas as pd
from datetime import datetime
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print(f"Running time: {datetime.now()}")

ua = UserAgent()
options = Options()
options.add_argument(f'user-agent={ua.random}')
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = 'https://yallacompare.com/uae/en/%D8%A8%D8%B7%D8%A7%D9%82%D8%A7%D8%AA-%D8%A7%D9%84%D8%A7%D8%A6%D8%AA%D9%85%D8%A7%D9%86/'
driver.get(url)

time.sleep(5)
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Loading time
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # Stop scrolling when reach the end of the page
    last_height = new_height

driver.execute_script("window.scrollTo(0, 0);")
product_titles = driver.find_elements(By.XPATH, '//div[@class="srpProduct-title"]')
see_more_buttons = driver.find_elements(By.XPATH, '//*[@class="more"]')
click_success = []
for title, see_more in zip(product_titles, see_more_buttons):
    try:
        see_more.click()
        click_success.append([title.text, 1])
        time.sleep(1)
    except Exception as error:
        click_success.append([title.text, 0])
        pass

time.sleep(15)

min_salaries = driver.find_elements(By.XPATH, '//*[@data-field="minimumSalary"]')
annual_fees = driver.find_elements(By.XPATH, '//*[@data-field="annualFee"]')
rates = driver.find_elements(By.XPATH, '//*[@data-field="flatRate"]')
salary_transfers = driver.find_elements(By.XPATH, '//*[@data-field="hasNoSalaryTransfer"]')
features = driver.find_elements(By.XPATH, '//*[@data-field="features"]')
details = driver.find_elements(By.XPATH, '//*[@class="col-sm-12 srpTable__viewMoreDetails_section"]')  # dynamics

# print(len(product_titles))
# print(len(min_salaries))
# print(len(annual_fees))
# print(len(rates))
# print(len(salary_transfers))
# print(len(features))
# print(len(details))

results = []
for i in range(len(product_titles)):
    results.append([
        product_titles[i].text,
        min_salaries[i].text,
        annual_fees[i].text,
        rates[i].text,
        salary_transfers[i].text,
        features[i].text,
        details[i].text
    ])

data = pd.DataFrame(data=results, columns=['product_titles', 'min_salaries', 'annual_fees', 'rates', 'salary_transfers', 'features', 'details'])
data.to_csv('./results.csv', index=False)

time.sleep(5)
driver.quit()
