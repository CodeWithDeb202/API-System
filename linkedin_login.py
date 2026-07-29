import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

Linkedin_email = os.getenv("LINKEDIN_EMAIL")
Linkedin_pass = os.getenv("LINKEDIN_PASSWORD")
Session_file = "session.json"

def login_and_save_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        page = context.new_page()

        print("Opening LinkedIn login page...")
        try:
            page.goto("https://www.linkedin.com/login", timeout=60000)

            print("Please check the browser window.")
            print("If fields don't load automatically, please log in manually in the opened browser within 45 seconds...")

            try:
                page.wait_for_selector("#username", timeout=10000)
                page.fill("#username", Linkedin_email)
                page.fill("#password", Linkedin_pass)
                page.click("button[type='submit']")
            except:
                print("Manual login mode active. Please login directly in the browser window.")

            print("Waiting for you to complete login/CAPTCHA if any (45 seconds remaining)...")
            page.wait_for_timeout(45000)

            context.storage_state(path=Session_file)
            print(f"Session saved successfully to {Session_file}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    login_and_save_session()

