import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import platform
from datetime import datetime
import time
import json
from selenium.webdriver.common.by import By
from config import HOST,PORT,USERNAME,PASSWORD
import mysql.connector

# Constants for file paths
BROWSER_EXECUTABLE_PATH_WINDOWS = "C:\\Users\\muham\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
BROWSER_EXECUTABLE_PATH_LINUX = '/usr/bin/brave-browser'

# Static URLs
JOB_BASE_URL = 'https://indeed.com/viewjob?jk='

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
    # Scraping the Web
    soup = BeautifulSoup(driver.page_source, 'html.parser')
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

def savetodatabase(all_jobs):
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
    # Loop through the job_data list and insert data into the table
    for each_job in all_jobs:
        insert_statement = """
            INSERT IGNORE INTO indeedjobs
            (job_title, company, job_location, job_posted_time, job_url)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            each_job['job_title'],
            each_job['company'],
            each_job['job_location'],
            each_job['job_posted_time'],
            each_job['job_url']
        )
        cursor.execute(insert_statement, values)
        print(values)
    # Commit the changes to the database and close the connection
    conn.commit()
    conn.close()

def main():
    # Skills and Place of Work
    skill = input('Enter your Skill: ').strip()
    place = input('Enter the location: ').strip()

    driver = new_browser()
    url = f'https://www.indeed.com/jobs?q={skill}&l={place}&fromage=1&sort=date'
    driver.get(url)

    allJobs = []

    while True:
        job_list = parse_jobs(driver)
        allJobs.extend(job_list)

        time.sleep(5)
        next_page_button = driver.find_elements(By.XPATH, '//a[@aria-label="Next Page"]')
        if not next_page_button:
            break
        
        driver.execute_script("arguments[0].scrollIntoView();", next_page_button[0])
        driver.execute_script("arguments[0].click();", next_page_button[0])
        time.sleep(10)

    with open('indeedJobs.json', 'w') as fout:
        json.dump(allJobs, fout)
    #save to mysql
    savetodatabase(allJobs)

    driver.close()
    driver.quit()

if __name__ == "__main__":
    main()