import undetected_chromedriver as uc
import platform
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
from config import HOST,PORT,USERNAME,PASSWORD
import mysql.connector
# Constants for API URLs and file paths
URL = "https://www.glassdoor.com/Job/index.htm"
SEARCH_API = 'https://www.glassdoor.com/graph'
#BROWSER_EXECUTABLE_PATH_WINDOWS = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
BROWSER_EXECUTABLE_PATH_WINDOWS = "C:\\Users\\muham\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
BROWSER_EXECUTABLE_PATH_LINUX = '/usr/bin/brave-browser'

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

def parse_logs(driver, logs, target_url):
	for log in logs:
		try:
			resp_url = log["params"]["response"]["url"]
			if target_url in resp_url:
				request_id = log["params"]["requestId"]
				response_body = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
				response_json = json.loads(response_body['body'])
				if 'jobListings' in json.dumps(response_json):
					#print(response_json)
					return response_json
		except Exception as e:
			pass
	return None

def apply_filter(driver, keyword, location):
	job_element = driver.find_element(By.ID, 'searchBar-jobTitle')
	job_element.send_keys(keyword)
	#
	location_element = driver.find_element(By.ID, 'searchBar-location')
	location_element.send_keys(location)
	location_element.send_keys(Keys.ENTER)
	time.sleep(10)
	#
	driver.find_element(By.XPATH, '//button[text()="Date posted"]').click()
	driver.find_element(By.XPATH, '//*[text()="Last day"]').click()

def check_popup(driver):
	try:
		driver.find_element(By.XPATH, '//div[@id="LoginModal"]//button').click()
	except Exception as e:
		pass

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
            INSERT IGNORE INTO glassdoorjobs
            (job_title, company, company_link, job_location, job_posted_time, job_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            each_job['job_title'],
            each_job['company'],
            each_job['company_link'],
            each_job['job_location'],
            each_job['job_posted_time'],
            each_job['job_url']
        )
        cursor.execute(insert_statement, values)
        print(values)
    # Commit the changes to the database and close the connection
    conn.commit()
    conn.close()

def extract_data(driver):
	logs_raw = driver.get_log("performance")
	logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
	response_json = parse_logs(driver, logs, SEARCH_API)
	#
	if response_json is None:
		return []
	#
	all_jobs = response_json[0]['data']['jobListings']['jobListings']
	job_list = []
	#
	for each_job in all_jobs:
		job_title = each_job['jobview']['job']['jobTitleText'].strip()
		#
		try:
			company = each_job['jobview']['overview']['name'].strip()
			company_link = f"https://www.glassdoor.com/Overview/-EI_IE{each_job['jobview']['overview']['id']}.htm"
		except:
			company = each_job['jobview']['header']['employerNameFromSearch'].strip()
			company_link = None
		#
		job_location = each_job['jobview']['header']['locationName'].strip()
		#job_posted_time = each_job['jobview']['header']['ageInDays']
		job_posted_time = datetime.now().strftime("%Y-%m-%d")
		job_url = 'https://www.glassdoor.com' + each_job['jobview']['header']['jobLink'].strip()
		#
		job_info = {
			'job_title': job_title,
			'company': company,
			'company_link': company_link,
			'job_location': job_location,
			'job_posted_time': job_posted_time,
			'job_url': job_url,
		}
		print(job_info)
		job_list.append(job_info)
	#
	driver.get_log("performance")
	return job_list

def main():
	driver = new_browser()
	driver.get(URL)
	time.sleep(5)
	skill = input('Enter your Skill: ').strip()
	location = input('Enter the location: ').strip()
	all_jobs = []

	apply_filter(driver, skill, location)
	time.sleep(10)
	check_popup(driver)

	while True:
		job_list=extract_data(driver)
		if not job_list:
			break
		all_jobs.extend(job_list)
		try:
			next_button = driver.find_element(By.XPATH, '//button[@aria-label="Next"]')
			next_button.click()
			time.sleep(10)
			check_popup(driver)
		except Exception as e:
			break

	with open('glassdoorJobs.json', 'w') as fout:
		json.dump(all_jobs, fout)
	# save to mysql
	savetodatabase(all_jobs)

	driver.quit()

if __name__ == "__main__":
	main()