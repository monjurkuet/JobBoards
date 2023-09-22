import requests

headers = {
    'authority': 'www.glassdoor.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.6',
    'apollographql-client-name': 'job-search',
    'apollographql-client-version': '0.39.2',
    'content-type': 'application/json',
    'origin': 'https://www.glassdoor.com',
    'referer': 'https://www.glassdoor.com/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
}

json_data = {
    'operationName': 'JobSearchQuery',
    'variables': {
        'searchParams': {
            'keyword': 'forklift operator',
            'locationId': 1,
            'locationType': 'COUNTRY',
            'numPerPage': 30,
            'searchType': 'SR',
            'pageNumber': 1,
            'filterParams': [
                {
                    'filterKey': 'includeNoSalaryJobs',
                    'values': 'true',
                },
                {
                    'filterKey': 'fromAge',
                    'values': '1',
                },
                {
                    'filterKey': 'sc.keyword',
                    'values': 'forklift operator',
                },
                {
                    'filterKey': 'locT',
                    'values': 'N',
                },
                {
                    'filterKey': 'locId',
                    'values': '1',
                },
            ],
            'seoUrl': False,
        },
    },
    'query': 'query JobSearchQuery($searchParams: SearchParams) {\n  jobListings(contextHolder: {searchParams: $searchParams}) {\n    ...SearchFragment\n    __typename\n  }\n}\n\nfragment SearchFragment on JobListingSearchResults {\n  adOrderJobLinkImpressionTracking\n  totalJobsCount\n  filterOptions\n  companiesLink\n  searchQueryGuid\n  indeedCtk\n  jobSearchTrackingKey\n  paginationCursors {\n    pageNumber\n    cursor\n    __typename\n  }\n  searchResultsMetadata {\n    cityPages {\n      cityBlurb\n      cityPagesStats {\n        bestCitiesForJobsRank\n        meanBaseSalary\n        population\n        unemploymentRate\n        __typename\n      }\n      displayName\n      employmentResources {\n        addressLine1\n        addressLine2\n        cityName\n        name\n        phoneNumber\n        state\n        zipCode\n        __typename\n      }\n      heroImage\n      isLandingExperience\n      locationId\n      numJobOpenings\n      popularSearches {\n        text\n        url\n        __typename\n      }\n      __typename\n    }\n    copyrightYear\n    footerVO {\n      countryMenu {\n        childNavigationLinks {\n          id\n          link\n          textKey\n          __typename\n        }\n        id\n        link\n        textKey\n        __typename\n      }\n      __typename\n    }\n    helpCenterDomain\n    helpCenterLocale\n    isPotentialBot\n    jobAlert {\n      jobAlertExists\n      promptedOnJobsSearch\n      promptingForJobClicks\n      __typename\n    }\n    jobSearchQuery\n    loggedIn\n    searchCriteria {\n      implicitLocation {\n        id\n        localizedDisplayName\n        type\n        __typename\n      }\n      keyword\n      location {\n        id\n        localizedDisplayName\n        shortName\n        localizedShortName\n        type\n        __typename\n      }\n      __typename\n    }\n    showMachineReadableJobs\n    showMissingSearchFieldTooltip\n    __typename\n  }\n  companyFilterOptions {\n    id\n    shortName\n    __typename\n  }\n  pageImpressionGuid\n  pageSlotId\n  relatedCompaniesLRP\n  relatedCompaniesZRP\n  relatedJobTitles\n  resourceLink\n  seoTableEnabled\n  jobListingSeoLinks {\n    linkItems {\n      position\n      url\n      __typename\n    }\n    __typename\n  }\n  jobListings {\n    jobview {\n      job {\n        descriptionFragments\n        eolHashCode\n        jobReqId\n        jobSource\n        jobTitleId\n        jobTitleText\n        listingId\n        __typename\n      }\n      gdJobAttributes {\n        salarySource\n        basePay {\n          p25\n          p75\n          __typename\n        }\n        additionalPay {\n          p25\n          p75\n          __typename\n        }\n        __typename\n      }\n      jobListingAdminDetails {\n        adOrderId\n        cpcVal\n        importConfigId\n        jobListingId\n        jobSourceId\n        userEligibleForAdminJobDetails\n        __typename\n      }\n      overview {\n        id\n        name\n        shortName\n        squareLogoUrl\n        __typename\n      }\n      gaTrackerData {\n        trackingUrl\n        jobViewDisplayTimeMillis\n        requiresTracking\n        isIndeedJob\n        searchTypeCode\n        pageRequestGuid\n        isSponsoredFromJobListingHit\n        isSponsoredFromIndeed\n        __typename\n      }\n      header {\n        adOrderId\n        adOrderSponsorshipLevel\n        advertiserType\n        ageInDays\n        applyUrl\n        autoLoadApplyForm\n        easyApply\n        easyApplyMethod\n        employerNameFromSearch\n        jobLink\n        jobCountryId\n        jobResultTrackingKey\n        locId\n        locationName\n        locationType\n        needsCommission\n        normalizedJobTitle\n        organic\n        payPercentile90\n        payPercentile50\n        payPercentile10\n        hourlyWagePayPercentile {\n          payPercentile90\n          payPercentile50\n          payPercentile10\n          __typename\n        }\n        rating\n        salarySource\n        sponsored\n        payPeriod\n        payCurrency\n        savedJobId\n        sgocId\n        categoryMgocId\n        urgencySignal {\n          labelKey\n          messageKey\n          normalizedCount\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n',
}

def ExtractData(response):
    all_jobs=response['data']['jobListings']['jobListings']
    job_list = []
    for each_job in all_jobs:
            job_title = each_job['jobview']['job']['jobTitleText'].strip()
            try:
                company = each_job['jobview']['overview']['name'].strip()
                company_link = f"https://www.glassdoor.com/Overview/-EI_IE{each_job['jobview']['overview']['id']}.htm"
            except:
                company = each_job['jobview']['header']['employerNameFromSearch'].strip()
                company_link = None
            job_location = each_job['jobview']['header']['locationName'].strip()
            job_posted_time = each_job['jobview']['header']['ageInDays']
            job_url = 'https://www.glassdoor.com'+each_job['jobview']['header']['jobLink'].strip()
            job_info = {
                'job_title': job_title,
                'company': company,
				'company_link': company_link,
                'job_location': job_location,
                'job_posted_time': job_posted_time,
                'job_url': job_url,
            }
            job_list.append(job_info)
    return job_list  

response = requests.post('https://www.glassdoor.com/graph', headers=headers, json=json_data, timeout=10).json()
job_list=ExtractData(response)