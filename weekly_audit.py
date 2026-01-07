#!/usr/bin/env python3
import utils
from datetime import datetime

# Constants, for easy config later if need be:
COL_STATUS = 'Applied'
COL_RESPONSE = 'Response'
COL_COMPANY = 'Company Name'
COL_ROLE = 'Role/Position'
COL_DATE_APPLIED = 'Date Applied'

STATUS_DONE = 'Done'
RESPONSE_OLD = 'Past 2+ Months'

notion = utils.get_notion_client()
internship_db_id = utils.get_database_id('internship')
job_db_id = utils.get_database_id('job')
TEST_RUN = utils.is_test_run()

def update_old_applications():
    today = datetime.now().date() # Makes it go from 2025-10-31 14:35:02 to 2025-10-31
    print(f'Fetching old applications... Date: {today}')

    filter_criteria = {
        "and": [
            {
                "property": "Applied",
                "select": {
                    "equals": STATUS_DONE
                }
            },
            {
                "property": "Response",
                "select": {
                    "is_empty": True
                }
            }
        ]
    }

    try:
        filtered_applications = []

        internship_response = notion.databases.query(
            database_id = internship_db_id, 
            filter = filter_criteria
        )

        filtered_applications.extend(internship_response["results"])
        print(f'Found {len(internship_response["results"])} internship(s) that possibly need responses changed to \"{RESPONSE_OLD}\"')

        job_response = notion.databases.query(
            database_id = job_db_id, 
            filter = filter_criteria
        )
        
        filtered_applications.extend(job_response["results"])
        print(f'Found {len(job_response["results"])} job(s) that possibly need responses changed to \"{RESPONSE_OLD}\"')

        applications_to_update = []

        for application in filtered_applications:
            page_id = application["id"]
            try:
                props = application["properties"]

                if not props[COL_COMPANY]["title"]:
                    company = 'Unknown Company'
                else:
                    company = props[COL_COMPANY]["title"][0]["plain_text"]
                
                if not props[COL_ROLE]["rich_text"]:
                    role = 'Unknown Role'
                else:
                    role = props[COL_ROLE]["rich_text"][0]["plain_text"]

                # We check this different since date is an entire object
                date_applied = props[COL_DATE_APPLIED]["date"]
                if date_applied is None:
                    print(f'This position has no date, skipping it (but fix it soon): {company} | {role}')
                    continue
                
                date_str = date_applied["start"]

            except KeyError as e:
                print(f'Error reading application properties: {e}')
                continue

            # CONVERSION & MATH
            application_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            delta = today - application_date
            days_passed = delta.days

            if days_passed >= 60:
                print(f'Old application found, appending it to applications_to_update: {company} | {role}')
                applications_to_update.append({"page_id": page_id, "company": company, "role": role})
            else:
                continue

        for application in applications_to_update:
            page_id = application["page_id"]
            company = application["company"]
            role = application["role"]
        
            if TEST_RUN:
                print(f'TEST_RUN: Updating application: {company} | {role}')
            else:
                print(f'Updating job: {company} | {role}')
            
                notion.pages.update(
                    page_id = page_id,
                    properties = {
                        "Response": {
                            "select": {
                                "name": RESPONSE_OLD
                            }
                        }
                    }
                )

    except Exception as e:
        print(f'CRITICAL ERROR: {e}')

if __name__ == '__main__':
    update_old_applications()