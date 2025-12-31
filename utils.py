import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

def get_notion_client():
    token = Client(auth=os.getenv('NOTION_TOKEN'))
    if not token:
        raise ValueError("CRITICAL ERROR: NOTION_TOKEN not found!")
    return token

def get_database_id(env_type):
    if env_type == 'internship':
        env_str = 'INTERNSHIP_DATABASE_ID'
    elif env_type == 'job':
        env_str = 'JOB_DATABASE_ID'
    else:
        raise ValueError(f"CRITICAL ERROR: env_type not found! | env_type: {env_type}")

    db_id = os.getenv(env_str)
    if not db_id:
        raise ValueError(f"CRITICAL ERROR: db_id not found! | env_str: {env_str}")
    return format_uuid(db_id) 

def is_test_run():
    test_run = os.getenv('TEST_RUN', 'true').lower() == 'true'
    if test_run is True:
        print("---TEST_RUN Enabled---")
    return test_run

def format_uuid(id_str):
    if not id_str:
        return None
    
    # Removes any -'s and whitespaces
    clean = id_str.replace("-", "").strip()

    # Slice it into the 5 standard groups to make the FULL database_id
    return f"{clean[:8]}-{clean[8:12]}-{clean[12:16]}-{clean[16:20]}-{clean[20:]}"
