import requests
from config import API_KEY,MONGOURL,HOST,PORT,USERNAME,PASSWORD
from pymongo import MongoClient
from datetime import datetime
import time 
import mysql.connector
from urllib.parse import urlparse
from tqdm import tqdm

client = MongoClient(MONGOURL)

db = client['companydatabase']
collection_apollo_company = db['apollo_company_api']

class ApolloAPIClient:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = "https://api.apollo.io/v1/organizations/enrich"
        self.headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json'
        }
    def search_organization_domains(self, domain):
        data = {
                "api_key": self.api_key,
                "domain": domain
            }
        response = requests.post(self.base_url, headers=self.headers, json=data)
        return response

def get_domains():
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
    # Execute the SQL query to retrieve distinct values
    query = "SELECT domain FROM linkedincrawler_company WHERE domain is not NULL"
    cursor.execute(query)
    # Fetch all the distinct values as a list
    domains = [row[0] for row in cursor.fetchall()]
    domains = [urlparse(row).netloc.replace("www.", "") for row in domains]
    # Close the database connection
    conn.close()
    # Print the list of distinct company LinkedIn URLs
    print(len(domains))
    return domains

Apolloclient = ApolloAPIClient()

domains_mysql=get_domains()
# Query to retrieve all documents and project only the "base domain" field
projection = {"base_domain": 1, "_id": 0}
# Retrieve all documents and extract the "base domain" values
base_domains_mongo = [doc["base_domain"] for doc in collection_apollo_company.find({}, projection)]

new_domains= list(set(domains_mysql).symmetric_difference(set(base_domains_mongo)))

for domain in tqdm(new_domains):
    response = Apolloclient.search_organization_domains(domain).json()
    if response:
            response['updateAt']=datetime.now()
            collection_apollo_company.update_one({"base_domain":domain}, {'$set': response}, upsert=True)
    print(f'Crawled : {domain}')
    time.sleep(1)
