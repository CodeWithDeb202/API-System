# 🚀 LinkedIn & Gmail Automation System

An automated recruitment and job application pipeline designed to streamline the outreach process. It logs into LinkedIn, scrapes recent job postings for target roles and recruiter emails, dynamically tailors resumes, and automatically dispatches personalized cold emails via Gmail.

---

## ✨ Features

* **Automated LinkedIn Session Management**: Securely handles browser automation and keeps your login session active.
* **Smart Job & Contact Scraping**: Searches for recent job posts (within the past 24 hours) based on custom keywords and extracts recruiter email addresses.
* **AI-Powered Resume Customization**: Dynamically tailors your base resume to align with specific job descriptions using advanced AI.
* **Automated Gmail Outreach**: Composes and sends professional, personalized emails with your tailored resume attached directly to the extracted recruiter emails.
* **IMAP Inbox Monitoring**: Monitors your Gmail inbox for recruiter replies and responses using the IMAP protocol.

---

## 📂 Project Structure

```text
├── clients/              # Master base resumes and candidate configuration templates
├── scratch/              # Temporary folder for generated files and tailored resumes
├── .env                  # Environment variables (Credentials & API keys)
├── .gitignore            # Files and directories ignored by Git
├── main.py               # Main control script (Interactive menu-driven pipeline)
├── linkedin_login.py     # Automated LinkedIn login and session handler
├── linkedin_scraper.py   # Job post and recruiter email scraper
├── resume_customizer.py  # AI-based resume tailoring module
├── gmail_sender.py       # Automated email dispatch script
├── imap_reply_detector.py# Inbox reply monitoring module
└── requirements.txt      # Required Python dependencies