#!/usr/bin/env python3
# TODO: REPLACE UNUSABLE SYMBOLS IN URLS LIKE ', ?, etc.
import requests
import time
import utils
import json # For testing
from datetime import datetime

TITLE_INTERNSHIP = 'Internship Application'
TITLE_JOB = 'Job Application'

COL_COMPANY = 'Company Name'
COL_ROLE = 'Role/Position'

DEFAULT_ICON = 'https://www.notion.so/icons/briefcase_gray.svg'

notion = utils.get_notion_client()
internship_db_id = utils.get_database_id('internship')
job_db_id = utils.get_database_id('job')
logo_dev_pkey = utils.get_logo_dev_pkey()
TEST_RUN = utils.is_test_run()
if TEST_RUN: print ('---TEST RUN ENABLED---')

print()

def update_null_icons():
    today = datetime.now().date()
    print(f'-----Updating null icons for applications... Date: {today}-----')

    filter_criteria = {
        "property": COL_COMPANY,
        "title": {
            "is_not_empty": True
        }
    }

    def pagination_loop(db_id, application_type):
        print(f'Fetching applications from: {application_type}...')
        application_collection = []
        cursor = None

        while True:
            response = notion.databases.query(
                database_id = db_id,
                filter = filter_criteria,
                start_cursor = cursor,
                page_size = 100
            )

            application_collection.extend(response['results'])

            if not response['has_more']:
                break # No more to add

            cursor = response['next_cursor']
        
        print(f'Applications fetched: {len(application_collection)}')

        return application_collection
    
    all_applications = []
    all_applications.extend(pagination_loop(internship_db_id, TITLE_INTERNSHIP))
    all_applications.extend(pagination_loop(job_db_id, TITLE_JOB))
    
    print(f'Total applications fetched: {len(all_applications)}')

    for application in all_applications:
        if application['icon'] is None:
            page_id = application['id']
            company_name = application['properties'][COL_COMPANY]['title'][0]['plain_text']
            cleaned_company_name = company_name.lower().replace(' ','')

            url = f'https://img.logo.dev/{cleaned_company_name}.com?token={logo_dev_pkey}'
            url_response = requests.get(url)
            time.sleep(0.5) # Quick pause so we don't get IP banned

            if url_response.status_code == 200:
                print(f'Image found for {company_name}! Appending URL image.')
                if not TEST_RUN: 
                    notion.pages.update(
                        page_id = page_id,
                        icon = {
                            "type": "external",
                            "external": {
                                "url": url
                            }
                        }
                    )
            else:
                print(f'Could not find image for {company_name}. Appending default image.')
                if not TEST_RUN: 
                    notion.pages.update(
                        page_id = page_id,
                        icon = {
                            "type": "external",
                            "external": {
                                "url": DEFAULT_ICON
                            }
                        }
                    )
    
    print("---------------")

if __name__ == '__main__':
    update_null_icons()

    # test_response = notion.databases.query(
    #     database_id = internship_db_id, 
    #     filter = filter_criteria
    # )

    # print(json.dumps(test_response))
