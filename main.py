import sys
import os
import time
import pandas as pd
from linkedin_login import login_and_save_session
from linkedin_scraper import scrape_linkedin_posts
from gmail_sender import send_outreach_email
from resume_customizer import customize_resume_with_ai
from imap_reply_detector import check_gmail_replies
from client_config import CLIENTS

def show_menu():
    print("\n=> LinkedIn & Gmail Automation System")
    print("=> Enter 1, Setup / Test LinkedIn Log in session")
    print("=> Enter 2, Run LinkedIn Scraper (Past 24 Hours)")
    print("=> Enter 3, To Send Personalized email to recruiters")
    print("=> Enter 4, Check Gmail Inbox Replies (IMAP)")
    print("=> Enter 5, To Quit this pipeline")

def main():
    while True:
        show_menu()
        enter_num = input("Enter option (1-5): ").strip()

        if enter_num == "1":
            login_and_save_session()
        elif enter_num == "2":
            role = input("Enter Target Role (Default: Frontend Developer): ") or "Frontend Developer"
            scrape_linkedin_posts(role)
        elif enter_num == "3":
            csv_path = "recruiters.csv"
            if not os.path.exists(csv_path):
                print("No recruiters.csv found! Please run the scraper (Option 2) first.")
                continue
            
            df = pd.read_csv(csv_path)
            
            required_cols = ["recruiter_name", "recruiter_email", "role", "job_description", "email_sent_status"]
            for col in required_cols:
                if col not in df.columns:
                    df[col] = "pending" if col == "email_sent_status" else ""
            
            df.to_csv(csv_path, index=False)
            pending_rows = df[df["email_sent_status"] == "pending"]
            
            if pending_rows.empty:
                print("No pending recruiter emails found in CSV. Please run Scraper (Option 2) to collect contacts.")
                continue

            candidate = CLIENTS.get("candidate_1")
            base_resume = candidate["resume_path"]

            print(f"Found {len(pending_rows)} recruiters to email.")
            for index, row in pending_rows.iterrows():
                recruiter_email = row["recruiter_email"]
                recruiter_name = row["recruiter_name"]
                role = row["role"]
                
                if not recruiter_email or pd.isna(recruiter_email):
                    continue

                print(f"Sending outreach email to {recruiter_email}...")
                
                try:
                    # AI resume customization skip kariki direct base resume use karucha
                    success = send_outreach_email(recruiter_email, recruiter_name, role, base_resume)
                    
                    if success:
                        df.at[index, "email_sent_status"] = "sent"
                        df.to_csv(csv_path, index=False)
                    
                    print("Waiting 5 seconds...")
                    time.sleep(5)

                except Exception as e:
                    print(f"Error processing outreach for {recruiter_email}: {e}")
                    time.sleep(5)

        elif enter_num == "4":
            check_gmail_replies()
        elif enter_num == "5":
            print("Quitting pipeline...")
            sys.exit(0)
        else:
            print("Invalid option. Try again, Please Enter correct option.")

if __name__ == "__main__":
    main()