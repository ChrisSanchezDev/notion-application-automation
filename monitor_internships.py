import os
import json
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()
notion = Client(auth=os.getenv('NOTION_TOKEN'))
raw_db_id = os.getenv('INTERNSHIP_DATABASE_ID')
TEST_RUN = os.getenv('TEST_RUN', 'true').lower() == 'true'

def format_uuid(id_str):
    if not id_str:
        return None
    
    # Removes any -'s and whitespaces
    clean = id_str.replace("-", "").strip()

    # Slice it into the 5 standard groups to make the FULL database_id
    return f"{clean[:8]}-{clean[8:12]}-{clean[12:16]}-{clean[16:20]}-{clean[20:]}"

database_id = format_uuid(raw_db_id)

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