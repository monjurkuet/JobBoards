import requests
import json
from fake_useragent import UserAgent
from pprint import pprint
import pandas as pd

ua = UserAgent()

url='https://api.builtin.com/services/job-retrieval/legacy-collapsed-jobs?categories=150&subcategories=&experiences=&industry=&regions=&locations=&remote=2&per_page=400&page={page}&search=&sortStrategy=recency&job_locations=&company_locations=&jobs_board=true&national=true'

def company_jobs(response):
   job_data_dict_list=[] 
   for each_company in response['company_jobs']: 
    for each_job in each_company['jobs']:
        company_id=each_job['company_id']
        postion_title=each_job['title']
        job_location=each_job['location']
        job_data_dict={'company_id':company_id,'postion_title':postion_title,'job_location':job_location}
        job_data_dict_list.append(job_data_dict)
   return job_data_dict_list    

job_data_dict_list=[] 

for page in range(1,5):
    request_url=url.format(page=page)
    response=requests.get(request_url,headers={'user-agent': ua.random}).json()
    job_data_dict_list.extend(company_jobs(response))
    print(request_url)

df_jobSearch = pd.DataFrame.from_records(job_data_dict_list)   
df_jobSearch.to_excel('jobdata.xlsx',index=None) 