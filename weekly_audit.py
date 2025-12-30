import os
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()
notion = Client(auth=os.getenv('NOTION_TOKEN'))
raw_db_id = os.getenv('JOB_DATABASE_ID')
# getenv second parameter is a default value if None.
TEST_RUN = os.getenv('TEST_RUN', 'true').lower() == 'true'

def format_uuid(id_str):
    if not id_str:
        return None
    
    # Removes any -'s and whitespaces
    clean = id_str.replace("-", "").strip()

    # Slice it into the 5 standard groups to make the FULL database_id
    return f"{clean[:8]}-{clean[8:12]}-{clean[12:16]}-{clean[16:20]}-{clean[20:]}"

database_id = format_uuid(raw_db_id)

def fetch_and_update_jobs():
    print("Fetching jobs...")

    filter_criteria = {
        "and": [
            {
                "property": "Applied",
                "select": {
                    "equals": "Done"
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
        response = notion.databases.query(
            database_id = database_id, 
            filter = filter_criteria
        )
        
        filtered_jobs = response["results"]
        print(f'Found {len(filtered_jobs)} jobs that possibly need responses changed to \"Past 2+ Months\"')

        jobs_to_update = []
        today = datetime.now()

        for job in filtered_jobs:
            job_id = job["id"]
            try:
                props = job["properties"]

                if not props["Company Name"]["title"]:
                    company_name = 'Unknown Company'
                else:
                    company_name = props["Company Name"]["title"][0]["plain_text"]
                
                if not props["Role/Position"]["rich_text"]:
                    role_position = 'Unknown Role'
                else:
                    role_position = props["Role/Position"]["rich_text"][0]["plain_text"]

                # We check this different since date is an entire object
                date_data = props["Date Applied"]["date"]
                if date_data is None:
                    print(f'This position has no date, skipping it (but fix it soon): {company_name} | {role_position}')
                    continue
                
                date_str = date_data["start"]

            except KeyError as e:
                print(f'Error reading job properties: {e}')
                continue

            # CONVERSION & MATH
            job_date = datetime.strptime(date_str, "%Y-%m-%d")
            delta = today - job_date
            days_passed = delta.days

            if days_passed >= 60:
                print(f'Old job found, appending it to jobs_to_update: {company_name} | {role_position}')
                jobs_to_update.append({"job_id": job_id, "company": company_name, "role": role_position})
            else:
                continue

        for job in jobs_to_update:
            page_id = job["job_id"]
            company_name = job["company"]
            role_position = job["role"]
            if TEST_RUN:
                print(f'TEST_RUN: Updating job: {company_name} | {role_position}')
            else:
                print(f'Updating job: {company_name} | {role_position}')
            
                notion.pages.update(
                    page_id = page_id,
                    properties = {
                        "Response": {
                            "select": {
                                "name": "Past 2+ Months"
                            }
                        }
                    }
                )

    except Exception as e:
        print(f'CRITICAL ERROR: {e}')

if __name__ == '__main__':
    fetch_and_update_jobs()