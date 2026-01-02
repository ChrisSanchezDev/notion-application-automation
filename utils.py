import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

# Validates the notion bot integration client
def get_notion_client():
    token_str = os.getenv('NOTION_TOKEN')
    if not token_str:
        raise ValueError("CRITICAL ERROR: NOTION_TOKEN not found!")
    return Client(auth=token_str)

# Validates the internship, job, etc. database ID's
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

def get_logo_dev_pkey():
    return os.getenv('LOGO_DEV_PKEY')

# Validates test runs
def is_test_run():
    return os.getenv('TEST_RUN', 'true').lower() == 'true'

# Formats an DB ID to fit Notion's DB ID format.
def format_uuid(id_str):
    if not id_str:
        return None
    
    # Removes any -'s and whitespaces
    clean = id_str.replace("-", "").strip()

    # Slice it into the 5 standard groups to make the FULL database_id
    return f"{clean[:8]}-{clean[8:12]}-{clean[12:16]}-{clean[16:20]}-{clean[20:]}"