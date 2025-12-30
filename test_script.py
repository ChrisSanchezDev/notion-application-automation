import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

# We grab the ID you already have in your .env
target_id = os.getenv("DATABASE_ID")
notion = Client(auth=os.getenv("NOTION_TOKEN"))

print(f"🕵️ Testing ID: {target_id}...")

# TEST 1: Is it a Page?
try:
    print("\nAttempting to fetch as a PAGE...")
    page = notion.pages.retrieve(target_id)
    print("✅ SUCCESS! This is a PAGE ID, not a Database ID.")
    print("------------------------------------------------")
    print("PLEASE FIX YOUR .ENV FILE:")
    
    # Sometimes the page IS the database parent, let's look for it
    if page['parent']['type'] == 'database_id':
        print(f"The Real Database ID is: {page['parent']['database_id']}")
    else:
        print("This page holds the database, but isn't the database itself.")
        print("Follow the instructions below to find the real ID.")
        
except Exception as e:
    print(f"❌ Not a page. Error: {e}")

# TEST 2: Is it a Database?
try:
    print("\nAttempting to fetch as a DATABASE...")
    db = notion.databases.retrieve(target_id)
    print("✅ SUCCESS! This IS a valid Database ID.")
    print("If this worked, but Query failed, check your permissions.")
except Exception as e:
    print(f"❌ Not a database. Error: {e}")