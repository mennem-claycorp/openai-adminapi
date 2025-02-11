import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the root .env file
BASE_DIR = Path(__file__).resolve().parent.parent  # Go up one level to reach the root
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)

# Set your OpenAI API key here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Use environment variable for security
print(f"api key: {OPENAI_API_KEY}")

# OpenAI API endpoint for audit logs
AUDIT_LOGS_URL = "https://api.openai.com/v1/organization/audit_logs"

# Function to fetch audit logs with pagination
def fetch_audit_logs(limit=10):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    params = {
        "limit": limit
    }

    results = []
    next_cursor = None

    for _ in range(2):  # Iterate through two pages for testing pagination
        if next_cursor:
            params["after"] = next_cursor

        response = requests.get(AUDIT_LOGS_URL, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error fetching audit logs: {response.status_code}, {response.text}")
            return None

        data = response.json()
        results.extend(data.get("data", []))

        # Print a preview of the JSON response
        print(f"Page {_ + 1}:")
        print(data.get("data", [])[:3])  # Print the first 3 entries as a preview

        # Get pagination cursor
        next_cursor = data.get("paging", {}).get("after")

        if not next_cursor:
            break  # Exit if there's no next page

    return results

if __name__ == "__main__":
    logs = fetch_audit_logs()
    if logs:
        print(f"Total logs retrieved: {len(logs)}")

