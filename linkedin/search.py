import requests

headers = {
    'authority': 'www.linkedin.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.6',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}

params = {
    'keywords': 'Forklift Operator',
    'location': 'United States',
    'locationId': '',
    'geoId': '103644278',
    'f_TPR': 'r86400',
    'position': 1,
    'pageNum': 0,
    'start': 0,
}

response = requests.get(
    'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search',
    params=params,
    headers=headers,
)