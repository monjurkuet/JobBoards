import undetected_chromedriver as uc
import requests
from bs4 import BeautifulSoup
import platform
from datetime import datetime
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

# Skills and Place of Work
skill = input('Enter your Skill: ').strip()
place = input('Enter the location: ').strip()
no_of_pages = int(input('Enter the #pages to scrape: '))

driver=new_browser()

for page in range(no_of_pages):
    url = 'https://www.indeed.com/jobs?q=' + skill + \
        '&l=' + place + '&start=' + str(page * 10)+'&fromage=1'
    driver.get(url)
    # Scrapping the Web
    soup = BeautifulSoup(driver.page_source)
    d = soup.find('div', attrs={'id': 'mosaic-provider-jobcards'})
    jobs = soup.find_all('div', class_='job_seen_beacon')
    for job in jobs:
        job_id = job.find('a')['id'].split('_')[-1]
        job_title = job.find('span', title=True).text.strip()
        company = job.find('span', class_='companyName').text.strip()
        location = job.find('div', class_='companyLocation').text.strip()
        posted = datetime.now().strftime("%Y-%m-%d")
        job_link = JOB_BASE_URL + job_id
        #print([job_title, company, location, posted, job_link])

        # Writing to CSV File
        writer.writerow(
            [job_title, company, location.title(), posted, job_link])

print(f'Jobs data written to <{file_name}> successfully.')