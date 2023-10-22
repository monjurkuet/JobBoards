import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time,random
import json
from config import HOST,PORT,USERNAME,PASSWORD
import mysql.connector
import pandas as pd

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

def get_joburls():
    # Execute the SQL query to retrieve distinct values
    query = "SELECT job_url FROM linkedinjobs WHERE job_url not in (Select job_url from linkedin_jobs_details)"
    cursor.execute(query)
    # Fetch all the distinct values as a list
    job_url_list = [row[0] for row in cursor.fetchall()]
    # Close the database connection
    print(f'Total lobs list :{len(job_url_list)}')
    return job_url_list

def savetodatabase(job_url,applicants,industry):
    insert_statement = """
        INSERT IGNORE INTO linkedin_jobs_details
        (job_url,applicants,industry)
        VALUES (%s, %s, %s)
    """
    values = (job_url,applicants,industry)
    cursor.execute(insert_statement, values)
    print(values)
    # Commit the changes to the database and close the connection
    conn.commit()

job_url_list=get_joburls()

driver=uc.Chrome()

for job_url in job_url_list:
    driver.get(job_url)
    time.sleep(10)
    applicants=driver.find_element(By.XPATH,'//span[contains(@class, "num-applicants")]').text.split(' ')[0]
    industry=driver.find_element(By.XPATH,'//h3[contains(text(), "Industries")]//following::*').text
    savetodatabase(job_url,applicants,industry)

df_linkedinjobs = pd.read_sql('SELECT * from linkedinjobs left join linkedin_jobs_details on linkedinjobs.job_url=linkedin_jobs_details.job_url WHERE date(job_posted_time)=current_date()', conn)
df_linkedinjobs.to_excel('step_1_jobs_list.xlsx')

driver.close()
driver.quit()
conn.close()