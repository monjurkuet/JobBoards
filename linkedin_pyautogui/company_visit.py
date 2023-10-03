import webbrowser
import pyautogui
import time
import subprocess
import os
import random
import re
import mysql.connector
from config import API_KEY,MONGOURL,HOST,PORT,USERNAME,PASSWORD
from urllib.parse import urlparse
from tqdm import tqdm

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
    query = "SELECT DISTINCT company_linkedin FROM linkedinjobs where company_linkedin not in (Select company_linkedin from linkedincrawler_company)"
    cursor.execute(query)
    # Fetch all the distinct values as a list
    distinct_company_linkedin = [row[0] for row in cursor.fetchall()]
    # Close the database connection
    conn.close()
    # Print the list of distinct company LinkedIn URLs
    print(len(distinct_company_linkedin))
    return distinct_company_linkedin

def extract_data(htmldata):
    # Define the regular expression pattern
    pattern_website = r'websiteUrl&quot;:&quot;(http://.*?)&quot;'
    pattern_2_website = r'websiteUrl&quot;:&quot;(https://.*?)&quot;'
    # Search for the pattern in the input string
    match = re.search(pattern_website, htmldata)
    # Check if a match is found
    if match:
        # Extract the URL from the match
        url = match.group(1)
    else:
        match2 = re.search(pattern_2_website, htmldata)
        url=match2.group(1)
    if url:
        url=urlparse(url).netloc.replace("www.", "")
        print(url)
    return url

def savetodatabase(company_linkedin,domain):
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
    insert_statement = """
        INSERT IGNORE INTO linkedincrawler_company
        (company_linkedin, domain)
        VALUES (%s, %s)
    """
    values = (company_linkedin, domain)
    cursor.execute(insert_statement, values)
    print(values)
    # Commit the changes to the database and close the connection
    conn.commit()
    conn.close()

# Specify the path to your Chrome application
chrome_path = '/usr/bin/chromium-browser %s &'  # Update this path
# The URL you want to navigate to
url = 'http://linkedin.com/'

webbrowser.get(chrome_path).open(url)

def enter_navbar_text(textvalue):
    subprocess.run(['wmctrl','-xa','chromium'])
    time.sleep(.5)
    pyautogui.hotkey('alt', 'd')
    time.sleep(.5)
    pyautogui.press('backspace') 
    time.sleep(.5)
    pyautogui.write(textvalue+'/', interval=0.05)
    time.sleep(.5)
    pyautogui.press('backspace') 
    time.sleep(.5)
    pyautogui.press('enter')


mitmprocess_command = f"mitmdump -s mitmSave.py -p 2191"
browserprocess_command = f"chromium-browser --proxy-server=127.0.0.1:2191 &>/dev/null &"

linkedin_urls=get_linkedin_urls()

for linkedin_url in tqdm(linkedin_urls):
    enter_navbar_text(linkedin_url)
    time.sleep(random.uniform(10,20))
    with open('companyhtmldata.html','r') as f:
        htmldata=f.read()
    domain=extract_data(htmldata)
    savetodatabase(linkedin_url,domain)
    os.remove('companyhtmldata.html')