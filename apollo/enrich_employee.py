import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from config import MONGOURL,APOLLO_EMAIL,APOLLO_PASSWORD
from pymongo import MongoClient
from datetime import datetime
import time 
from tqdm import tqdm
import json
import pandas as pd
from urllib.parse import urlparse

# Constants for API URLs
LOGIN_URL='https://app.apollo.io/#/login'

def parse_domain(url):
    urlfinal=urlparse(url).netloc.replace("www.", "")
    if not urlfinal:
        urlfinal =urlparse(url).path.replace("www.", "")
    print(urlfinal)
    return urlfinal.lower()

def login(driver):
    driver.get(LOGIN_URL)
    time.sleep(10)
    driver.find_element('xpath','//input[@name="email"]').send_keys(APOLLO_EMAIL)
    driver.find_element('xpath','//input[@name="password"]').send_keys(APOLLO_PASSWORD)
    driver.find_element('xpath','//input[@name="password"]').send_keys(Keys.ENTER)
    time.sleep(10)

client = MongoClient(MONGOURL)
db = client['companydatabase']
collection_apollo_employee = db['apollo_employee_api']
collection_apollo_employee_emails = db['apollo_employee_emails']

input_data=pd.read_excel('initial_matched_employeed.xlsx')
input_employees = [x for x in input_data.id.tolist() if pd.notnull(x)]

driver=uc.Chrome()
login(driver)
#remove popup
time.sleep(10)
#remove popup
if driver.find_elements(By.XPATH, '//div[@role="dialog"]'):
    driver.execute_script("arguments[0].remove();", driver.find_element(By.XPATH, '//div[@role="dialog"]'))

for id in tqdm(input_employees):
    url='https://app.apollo.io/#/people/'+str(id)
    driver.get(url)
    time.sleep(20)
    if driver.find_elements(By.XPATH,'//div[text()="Access Email & Phone Number"]'):
        driver.find_element(By.XPATH,'//div[text()="Access Email & Phone Number"]').click()
        time.sleep(5)
    contactid=driver.current_url.rstrip('/').split('/')[-1]
    url='https://app.apollo.io/api/v1/contacts/'+contactid
    driver.get(url)
    time.sleep(2)
    content = driver.find_element(By.TAG_NAME,'pre').text
    parsed_json = json.loads(content)['contact']
    parsed_json['updateAt']=datetime.now()
    if parsed_json:
        collection_apollo_employee_emails.update_one({"person_id":id}, {'$set': parsed_json}, upsert=True)
    print(f'Crawled : {id}')

#mongodb query
query = {"person_id": {"$in": input_employees}}
projection = {"person_id": 1,'email':1,'first_name':1,'last_name':1,'phone_numbers':1} 
mongodb_result = collection_apollo_employee_emails.find(query, projection)
mongodb_result=[i for i in mongodb_result]

df_employee = pd.DataFrame(mongodb_result)

final_data = input_data.merge(df_employee, left_on='id', right_on='person_id', how='left')

final_data.to_excel('final_data.xlsx',index=None)