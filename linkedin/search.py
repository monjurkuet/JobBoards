import requests

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
        response = requests.get(url, params=params, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
        
# Example usage:
linkedin_search = LinkedInJobSearch()
jobs_data = linkedin_search.search_jobs('Forklift Operator', 'United States',0)
if jobs_data:
    print(jobs_data)
else:
    print("Failed to fetch job data.")