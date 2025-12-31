import utils
from datetime import datetime

notion = utils.get_notion_client()
internship_db_id = utils.get_database_id('internship')
job_db_id = utils.get_database_id('job')
TEST_RUN = utils.is_test_run

def update_old_applications():
    print("Fetching old applications...")

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
        filtered_applications = []

        response = notion.databases.query(
            database_id = internship_db_id, 
            filter = filter_criteria
        )

        filtered_applications.extend(response["results"])
        print(f'Found {len(response["results"])} internship(s) that possibly need responses changed to \"Past 2+ Months\"')

        response = notion.databases.query(
            database_id = job_db_id, 
            filter = filter_criteria
        )
        
        filtered_applications.extend(response["results"])
        print(f'Found {len(response["results"])} job(s) that possibly need responses changed to \"Past 2+ Months\"')

        applications_to_update = []
        today = datetime.now()

        for application in filtered_applications:
            page_id = application["id"]
            try:
                props = application["properties"]

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
                print(f'Error reading application properties: {e}')
                continue

            # CONVERSION & MATH
            application_date = datetime.strptime(date_str, "%Y-%m-%d")
            delta = today - application_date
            days_passed = delta.days

            if days_passed >= 60:
                print(f'Old application found, appending it to applications_to_update: {company_name} | {role_position}')
                applications_to_update.append({"page_id": page_id, "company": company_name, "role": role_position})
            else:
                continue

        for application in applications_to_update:
            page_id = application["page_id"]
            company_name = application["company"]
            role_position = application["role"]
        
            if TEST_RUN:
                print(f'TEST_RUN: Updating application: {company_name} | {role_position}')
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
    update_old_applications()