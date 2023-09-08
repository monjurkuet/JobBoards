import requests
from bs4 import BeautifulSoup
import time,random

class LinkedInJobSearch:
    def __init__(self):
        self.headers = {
            'authority': 'www.linkedin.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en;q=0.6',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }
    def search_jobs(self, keywords, location, start):
        params = {
            'keywords': keywords,
            'location': location,
            'locationId': '',
            'geoId': '103644278',
            'f_TPR': 'r86400',
            'start': start,
        }
        url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search'
        max_retries=3
        for _ in range(max_retries + 1):  # Include the initial attempt plus max_retries
            response = requests.get(url, params=params, headers=self.headers)
            print(f'Response status code: {response.status_code}')
            if response.status_code == 200:
                return response.text
            else:
                print('Retrying...')
                time.sleep(random.uniform(5,10))  # Wait before retrying
        return None

class LinkedInJobParser:
    def __init__(self, jobs_data):
        self.jobs_data = jobs_data
    def parse_jobs(self):
        soup = BeautifulSoup(self.jobs_data, 'html.parser')
        all_jobs = soup.find_all('li')
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
        return job_list

allJobs=[]
linkedin_search = LinkedInJobSearch()
for i in range(0,9000,25):
    jobs_data = linkedin_search.search_jobs('Forklift Operator', 'United States',i)
    linkedin_parser = LinkedInJobParser(jobs_data)
    parsed_jobs = linkedin_parser.parse_jobs()
    print(f'Crrawled : Page {i}')
    if parsed_jobs==[]:
        break
    allJobs.extend(parsed_jobs)
    time.sleep(random.uniform(5,10))