import os
import re
import csv
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

Session_file = "session.json"
Recruiters_csv = "recruiters.csv"

Email_Regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

def is_usa_job(text):
    non_usa = ["pune", "noida", "bangalore", "hyderabad", "india", "kolkata", "cannada", "delhi", "mumbai"]

    text_lower = text.lower()
    if any(loc in text_lower for loc in non_usa):
        return False
    if "bench" in text_lower or "on my bench" in text_lower:
        return False
    return True

def scrape_linkedin_posts(role_keyword='Java Developer'):
    if not os.path.exists(Session_file):
        print("Session file missing. Please run linkedin_login.py first.")
        return

    query = f"{role_keyword} C2C"
    search_url = f"https://www.linkedin.com/search/results/content/?keywords={query}&origin=GLOBAL_SEARCH_HEADER&sortBy=%22date_posted%22"

    scraped_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_page(
            storage_state=Session_file,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print(f"Searching LinkedIn for: {role_keyword}...")

        page.goto(search_url)
        page.wait_for_timeout(8000)

        for i in range(5):
            page.evaluate("window.scrollBy(0, 1000);")
            time.sleep(3)

        page_text = page.inner_text("body")

        all_emails = re.findall(Email_Regex, page_text)
        unique_emails = list(set(all_emails))

        print(f"Found {len(unique_emails)} potential emails on the page. Processing...")

        for email in unique_emails:
            if "linkedin.com" in email or "sentry" in email or "support" in email:
                continue

            scraped_data.append({
                "recruiter_name": "LinkedIn Recruiter",
                "recruiter_email": email,
                "role": role_keyword,
                "post_url": search_url,
                "job_description": f"Direct scraped email for {role_keyword}",
                "email_sent_status": "pending",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        browser.close()

        file_exists = os.path.exists(Recruiters_csv)
        with open(Recruiters_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["recruiter_name", "recruiter_email", "role", "post_url", "job_description", "email_sent_status", "timestamp"])
            if not file_exists:
                writer.writeheader()
            for row in scraped_data:
                writer.writerow(row)
                
            print(f"Scraped and saved {len(scraped_data)} recruiter contacts.")

if __name__ == "__main__":
    scrape_linkedin_posts("Java Developer")