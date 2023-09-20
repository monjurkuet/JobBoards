import undetected_chromedriver as uc
import platform
import json

# Constants for API URLs
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
    if SYSTEM_OS == 'Windows':
        browser_executable_path = BROWSER_EXECUTABLE_PATH_WINDOWS
    elif SYSTEM_OS == 'Linux':
        browser_executable_path = BROWSER_EXECUTABLE_PATH_LINUX
    driver = uc.Chrome(browser_executable_path=browser_executable_path, headless=False,options=options,desired_capabilities=caps)
    return driver

def clean_logs(driver,logs,target_url):
	for log in logs:
		try:
			resp_url = log["params"]["response"]["url"]
			if target_url in resp_url:
				request_id = log["params"]["requestId"]
				response_body=driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
				response_json=json.loads(response_body['body'])
				if 'jobListings' in response_json['data'].keys():
					return response_json
		except:
			pass
	return None

def ExtractData(driver):
    logs_raw = driver.get_log("performance")     
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    response_json=clean_logs(driver,logs,SEARCH_API)
    all_jobs=response_json['data']['jobListings']['jobListings']
    job_list = []
    for each_job in all_jobs:
            job_title = each_job.find('h3').text.strip()
            company = each_job.find('h4').text.strip()
            company_linkedin = each_job.find('h4').find('a').get('href').split('?')[0]
            job_location = each_job.find(class_="job-search-card__location").text.strip()
            job_posted_time = each_job.find("time").get('datetime').strip()
            job_url = each_job.find('a').get('href').split('?')[0]
            job_info = {
                'job_title': job_title,
                'company': company,
                'company_linkedin': company_linkedin,
                'job_location': job_location,
                'job_posted_time': job_posted_time,
                'job_url': job_url,
            }
            job_list.append(job_info)
    driver.get_log("performance")
    return job_list  


driver=new_browser()
driver.get('https://www.glassdoor.com/Job/united-states-forklift-operator-jobs-SRCH_IL.0,13_IN1_KO14,31.htm?fromAge=1&includeNoSalaryJobs=true')

#close popup notication
driver.find_element('xpath','//div[@id="LoginModal"]//button').click()