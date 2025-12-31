import os
import json
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()
notion = Client(auth=os.getenv('NOTION_TOKEN'))
database_id = os.getenv('INTERNSHIP_DATABASE_ID')
TEST_RUN = os.getenv('TEST_RUN', 'true').lower() == 'true'

def fetch_and_update_internships():
    response = notion.databases.query(
            database_id = database_id, 
            page_size = 5
        )
    
    if not response["results"]:
        print('No jobs found with this criteria')
    
    else:
        first_internship = response["results"][0]

        print(json.dumps(first_internship, indent=2))

if __name__ == '__main__':
    fetch_and_update_internships()