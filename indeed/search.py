import undetected_chromedriver as uc
import requests
from bs4 import BeautifulSoup
import platform
from datetime import datetime
import time
import json

# Constants for file paths
BROWSER_EXECUTABLE_PATH_WINDOWS = "C:\\Users\\muham\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
BROWSER_EXECUTABLE_PATH_LINUX = '/usr/bin/brave-browser'
# static urls
JOB_BASE_URL='https://indeed.com/viewjob?jk='

def new_browser():
    options = uc.ChromeOptions()
    caps = options.to_capabilities()
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    SYSTEM_OS = platform.system()
    browser_executable_path = (
        BROWSER_EXECUTABLE_PATH_WINDOWS if SYSTEM_OS == 'Windows' else BROWSER_EXECUTABLE_PATH_LINUX
    )
    driver = uc.Chrome(
        browser_executable_path=browser_executable_path,
        headless=False,
        options=options,
        desired_capabilities=caps
    )
    return driver

def parse_jobs(driver):
    # Scrapping the Web
    soup = BeautifulSoup(driver.page_source)
    d = soup.find('div', attrs={'id': 'mosaic-provider-jobcards'})
    jobs = soup.find_all('div', class_='job_seen_beacon')
    job_list = []
    for job in jobs:
        job_id = job.find('a')['id'].split('_')[-1]
        job_title = job.find('span', title=True).text.strip()
        company = job.find('span', class_='companyName').text.strip()
        job_location = job.find('div', class_='companyLocation').text.strip()
        job_posted_time = datetime.now().strftime("%Y-%m-%d")
        job_url = JOB_BASE_URL + job_id
        job_info = {
                'job_title': job_title,
                'company': company,
                'job_location': job_location,
                'job_posted_time': job_posted_time,
                'job_url': job_url,
            }
        job_list.append(job_info)
        print(job_info)
    return job_list

# Skills and Place of Work
skill = input('Enter your Skill: ').strip()
place = input('Enter the location: ').strip()

driver=new_browser()
url = 'https://www.indeed.com/jobs?q=' + skill + \
        '&l=' + place + '&fromage=1&sort=date'
driver.get(url)
allJobs=[]

while True:
    job_list=parse_jobs(driver)
    allJobs.extend(job_list)
    if not driver.find_elements('xpath','//a[@aria-label="Next Page"]'):
        break
    driver.find_element('xpath','//a[@aria-label="Next Page"]').click()
    time.sleep(10)

with open('indeedJobs.json', 'w') as fout:
    json.dump(allJobs , fout)

driver.close()
driver.quit()