# LinkedIn & Gmail Automation System

An automated recruitment and job application system designed to log into LinkedIn, scrape recent job posts for specific keywords and recruiter emails, and automatically dispatch personalized cold emails with candidate resumes via Gmail.

---

## 🚀 Features

* **Automated LinkedIn Login**: Securely handles session management and browser automation.
* **Smart Job Scraping**: Searches for recent job posts (within the last 24 hours) based on custom keywords (e.g., "JAVA DEVELOPER", "CONTRACT") and extracts recruiter email addresses.
* **Automated Gmail Dispatch**: Composes and sends professional emails with candidate resumes and submission details attached to the extracted recruiter emails.
* **IMAP Reply Detection**: Monitors your inbox for recruiter responses using the IMAP protocol.

---

## 📂 Project Structure

```text
├── clients/              # Resumes and templates for registered client candidates
├── scratch/              # Target directory for temporary document conversions and customized resumes
├── .env                  # Environment variables (Credentials & API keys)
├── .gitignore            # Files and folders to ignore in Git
├── main.py               # Main control script (Menu-driven)
├── linkedin_login.py     # Automated LinkedIn login script
├── linkedin_scraper.py   # Job and recruiter email scraper
├── gmail_sender.py       # Automated email dispatch script
└── requirements.txt      # Required Python packages