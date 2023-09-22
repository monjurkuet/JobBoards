import undetected_chromedriver as uc
import platform
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
# Constants for API URLs
url = "https://www.glassdoor.com/Job/index.htm"
SEARCH_API = 'https://www.glassdoor.com/graph'
# Constants for file paths
BROWSER_EXECUTABLE_PATH_WINDOWS = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
BROWSER_EXECUTABLE_PATH_LINUX = '/usr/bin/brave-browser'
#Fix variables for python
null=None
true=True
false=False
#initiate browser
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
                if 'jobListings' in response_json.get('data', {}):
                    return response_json
        except Exception as e:
            pass
    return None

def  apply_filter(driver,keyword,location):
	# job title
	job_element = driver.find_element(By.ID, 'searchBar-jobTitle')
	job_element.send_keys(keyword)
	# job location
	location_element = driver.find_element(By.ID, 'searchBar-location')
	location_element.send_keys(location)
	location_element.send_keys(Keys.ENTER)
	time.sleep(10)
	# date filter
	driver.find_element(By.ID, 'filter_fromAge').click()
	driver.find_element(By.XPATH, '//button[@value="1"]').click()

#close popup notication
def check_popup(driver):
	try:
		driver.find_element(By.XPATH,'//div[@id="LoginModal"]//button')
		driver.find_element('xpath','//div[@id="LoginModal"]//button').click()
	except:
		pass

def ExtractData(driver):
	logs_raw = driver.get_log("performance")     
	logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
	response_json=parse_logs(driver,logs,SEARCH_API)
	all_jobs=response_json['data']['jobListings']['jobListings']
	job_list = []
	for each_job in all_jobs:
			job_title = each_job['jobview']['job']['jobTitleText'].strip()
			try:
				company = each_job['jobview']['overview']['name'].strip()
				company_link = f"https://www.glassdoor.com/Overview/-EI_IE{each_job['jobview']['overview']['id']}.htm"
			except:
				company = each_job['jobview']['header']['employerNameFromSearch'].strip()
				company_link = None
			job_location = each_job['jobview']['header']['locationName'].strip()
			job_posted_time = each_job['jobview']['header']['ageInDays']
			job_url = 'https://www.glassdoor.com'+each_job['jobview']['header']['jobLink'].strip()
			job_info = {
				'job_title': job_title,
				'company': company,
				'company_link': company_link,
				'job_location': job_location,
				'job_posted_time': job_posted_time,
				'job_url': job_url,
			}
			job_list.append(job_info)
	driver.get_log("performance")
	return job_list  



driver=new_browser()
driver.get(url)
time.sleep(5)
keyword='forklift operator'
location='texas, united states'

allJobs=[]
apply_filter(driver,keyword,location)
time.sleep(10)
check_popup(driver)
while True:
	allJobs.extend(ExtractData(driver))
	driver.find_element(By.XPATH,'//button[@aria-label="Next"]').click()
	time.sleep(10)
	check_popup(driver)

with open('glassdoorJobs.json', 'w') as fout:
	json.dump(allJobs , fout)

driver.quit()