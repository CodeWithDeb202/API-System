import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

Linkedin_email = os.getenv("LINKEDIN_EMAIL")