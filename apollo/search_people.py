import seleniumwire.undetected_chromedriver as uc
from seleniumwire.utils import decode
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from config import MONGOURL,HOST,PORT,USERNAME,PASSWORD,APOLLO_EMAIL,APOLLO_PASSWORD
from pymongo import MongoClient
from datetime import datetime
import time 
import mysql.connector
from urllib.parse import urlparse
from tqdm import tqdm
import json
import pandas as pd

# Constants for API URLs
PEOPE_SEARCH_API = 'https://app.apollo.io/api/v1/mixed_people/search'
LOGIN_URL='https://app.apollo.io/#/login'
PEOPLE_SEARCH_URL='https://app.apollo.io/#/people'
# Constants for file paths
BROWSER_EXECUTABLE_PATH_WINDOWS = "C:\\Users\\muham\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
#BROWSER_EXECUTABLE_PATH_WINDOWS = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
BROWSER_EXECUTABLE_PATH_LINUX = '/usr/bin/brave-browser'

client = MongoClient(MONGOURL)

db = client['companydatabase']
collection_apollo_employee = db['apollo_employee_api']
collection_apollo_company = db['apollo_company_api']

def get_domains():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host=HOST,
        user=USERNAME,
        password=PASSWORD,
        database='jobboards',
        port=PORT
        )
    # Create a cursor object to execute SQL statements
    cursor = conn.cursor()
    # Execute the SQL query to retrieve distinct values
    query = "SELECT domain FROM linkedincrawler_company WHERE domain is not NULL and DATE(updatedAt)=CURDATE()"
    cursor.execute(query)
    # Fetch all the distinct values as a list
    domains = [row[0] for row in cursor.fetchall()]
    # Close the database connection
    conn.close()
    # Print the list of distinct company LinkedIn URLs
    print(len(domains))
    return domains

def login(driver):
    driver.get(LOGIN_URL)
    time.sleep(10)
    driver.find_element('xpath','//input[@name="email"]').send_keys(APOLLO_EMAIL)
    driver.find_element('xpath','//input[@name="password"]').send_keys(APOLLO_PASSWORD)
    driver.find_element('xpath','//input[@name="password"]').send_keys(Keys.ENTER)
    time.sleep(10)

def extract_realtime_data(driver):
    details_content=None
    #Fix variables for python
    null=None
    true=True
    false=False
    final_list=[]
    if driver.requests:
        for request in driver.requests:
            if request.response:
                if PEOPE_SEARCH_API in request.url and request.response.status_code == 200 :
                    details_content = eval(decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity')).decode('utf-8'))
                    if 'people' in json.dumps(details_content):
                        break
        if details_content:
            for each_people in details_content['people']+details_content['contacts']:
                final_list.append(each_people)
        del driver.requests
    return final_list

domains_mysql=get_domains()

driver=uc.Chrome()
login(driver)
PERSONA_URL='?qPersonPersonaIds[]=651d5c5c32cfc500a3a07707'
EMAIL_FILTER='&contactEmailStatus[]=verified'
driver.get(PEOPLE_SEARCH_URL+PERSONA_URL+EMAIL_FILTER)
#remove popup
driver.execute_script("arguments[0].remove();", driver.find_element(By.XPATH, '//div[@role="dialog"]'))
del driver.requests

for domain in tqdm(domains_mysql):
    driver.find_element(By.XPATH,'//input[@placeholder="Search People..."]').clear()
    driver.find_element(By.XPATH,'//input[@placeholder="Search People..."]').send_keys(domain)
    driver.find_element(By.XPATH,'//input[@placeholder="Search People..."]').send_keys(Keys.ENTER)
    time.sleep(10)
    PAGINATION=0
    while PAGINATION<4:
        details_content=extract_realtime_data(driver)
        if details_content:
            for each_people in details_content:
                each_people['updateAt']=datetime.now()
                each_people['domain']=domain.lower()
                collection_apollo_employee.update_one({"id":each_people['id']}, {'$set': each_people}, upsert=True)
        print(f'Crawled : {domain}')
        if not driver.find_elements(By.XPATH,'//button[@aria-label="right-arrow"]'):
            break
        if not driver.find_element(By.XPATH,'//button[@aria-label="right-arrow"]').is_enabled():
            break
        driver.find_element(By.XPATH,'//button[@aria-label="right-arrow"]').click()
        time.sleep(10)
        PAGINATION+=1
    
driver.quit()

#mongodb query
query = {"domain": {"$in": domains_mysql}}
projection = {"id": 1,'city':1,'country':1,'departments':1,'domain':1,'linkedin_url':1,'name':1,'organization':1,'seniority':1,'title':1,'seniority':1} 
mongodb_result = collection_apollo_employee.find(query, projection)
mongodb_result=[i for i in mongodb_result]
for each_data in mongodb_result:
    each_data['']
df_employee = pd.DataFrame(mongodb_result)
df_employee.to_excel('initial_matched_employeed.xlsx',index=None)