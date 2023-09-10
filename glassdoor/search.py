import undetected_chromedriver as uc

driver = uc.Chrome(headless=False,use_subprocess=False)
driver.get('https://www.glassdoor.com/Job/united-states-forklift-operator-jobs-SRCH_IL.0,13_IN1_KO14,31_IP2.htm?fromAge=1&includeNoSalaryJobs=true')