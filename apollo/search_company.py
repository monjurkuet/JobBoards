import requests
from config import API_KEY,MONGOURL,HOST,PORT,USERNAME,PASSWORD
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import time 
import mysql.connector

client = MongoClient(MONGOURL)

db = client['companydatabase']
collection_apollo_employee = db['apollo_employee_api']
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

def get_linkedin_urls():
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
    query = "SELECT DISTINCT company_linkedin FROM linkedinjobs"
    cursor.execute(query)
    # Fetch all the distinct values as a list
    distinct_company_linkedin = [row[0] for row in cursor.fetchall()]
    # Close the database connection
    conn.close()
    # Print the list of distinct company LinkedIn URLs
    print(len(distinct_company_linkedin))
    return distinct_company_linkedin

Apolloclient = ApolloAPIClient()

person_titles=['owner','ceo','director']
person_titles=None

linkedin_urls=get_linkedin_urls()

for linkedin_url in linkedin_urls[:1]:
    response = Apolloclient.search_organization_domains(linkedin_url).json()
    if response:
        for each_people in people:
            each_people['updateAt']=datetime.now()
            collection.update_one({"id":each_people['id']}, {'$set': each_people}, upsert=True)
    print(domain,len(people),i)
    time.sleep(1)
