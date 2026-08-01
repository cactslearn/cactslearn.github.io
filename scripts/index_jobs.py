import os
import glob
import json
import time
import subprocess
import requests
from google.oauth2 import service_account
import google.auth.transport.requests

# 1. Base URL of your GitHub Pages site
DOMAIN = "https://cactslearn.github.io"
INDEXING_API_ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

IGNORE_FILES = {"404.html", "googleadedb2cbaba8a8c6.html"}

def get_access_token(service_account_info):
    """Authenticates using the Service Account JSON and fetches a Bearer token."""
    scopes = ["https://www.googleapis.com/auth/indexing"]
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=scopes
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token

def publish_url(url, access_token, action_type="URL_UPDATED"):
    """Sends a single URL notification to Google Indexing API."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "url": url,
        "type": action_type
    }
    response = requests.post(INDEXING_API_ENDPOINT, headers=headers, json=payload)
    
    if response.status_code == 200:
        print(f"[SUCCESS] Notified Google for: {url}")
    else:
        print(f"[ERROR {response.status_code}] Failed for {url}: {response.text}")

def is_job_page(filepath):
    """Verifies if the file path is a genuine JobPosting page in the jobs/ directory."""
    normalized = filepath.replace("\\", "/")
    filename = os.path.basename(normalized)
    if normalized.startswith("jobs/") and filename.endswith(".html") and filename != "index.html":
        return True
    return False

def get_changed_html_files():
    """Identifies only job posting HTML files in jobs/ that were added or modified in the push/commit."""
    changed_files = set()

    # 1. Try checking git diff for the latest commit (HEAD~1 vs HEAD in GitHub Actions)
    try:
        res = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], capture_output=True, text=True)
        if res.returncode == 0:
            for line in res.stdout.splitlines():
                filepath = line.strip().replace("\\", "/")
                if is_job_page(filepath) and os.path.exists(filepath):
                    changed_files.add(filepath)
    except Exception as e:
        print(f"Note: git diff HEAD~1 check skipped: {e}")

    # 2. If git diff returned nothing (e.g. initial commit or local run), try git status
    if not changed_files:
        try:
            res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            if res.returncode == 0:
                for line in res.stdout.splitlines():
                    if line.strip():
                        filepath = line[3:].strip().replace("\\", "/")
                        if is_job_page(filepath) and os.path.exists(filepath):
                            changed_files.add(filepath)
        except Exception as e:
            print(f"Note: git status check skipped: {e}")

    return sorted(list(changed_files))

def main():
    # Load secret from GitHub Actions environment variable
    gcp_key_raw = os.getenv("GCP_SERVICE_ACCOUNT_KEY")
    if not gcp_key_raw:
        raise ValueError("GCP_SERVICE_ACCOUNT_KEY environment variable is missing.")
    
    try:
        service_account_info = json.loads(gcp_key_raw)
    except json.JSONDecodeError as e:
        try:
            service_account_info = json.loads(gcp_key_raw.replace('\n', '\\n'))
        except Exception:
            raise ValueError(f"Invalid JSON in GCP_SERVICE_ACCOUNT_KEY secret: {e}")

    access_token = get_access_token(service_account_info)
    changed_html_files = get_changed_html_files()

    if not changed_html_files:
        print("No updated HTML files detected in this push. Skipping Indexing API submission.")
        return

    print(f"Detected {len(changed_html_files)} updated HTML file(s) in this push. Submitting to Google Indexing API:")
    for file_path in changed_html_files:
        url = f"{DOMAIN}/{file_path}"
        publish_url(url, access_token, "URL_UPDATED")
        time.sleep(0.1)

if __name__ == "__main__":
    main()