import os
import csv
import imaplib
import email
from email.header import decode_header

RECRUITERS_CSV = "recruiters.csv"

def load_recruiter_emails():
    """recruiters.csv"""
    emails = set()
    if not os.path.exists(RECRUITERS_CSV):
        return emails
    with open(RECRUITERS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "recruiter_email" in row and row["recruiter_email"]:
                emails.add(row["recruiter_email"].strip().lower())
    return emails

def check_gmail_replies():

    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(os.getenv("GMAIL_EMAIL"), os.getenv("GMAIL_APP_PASSWORD"))
    mail.select("INBOX")

    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()

    print(f"Found {len(email_ids)} unread emails in inbox.")


    if len(email_ids) > 50:
        email_ids = email_ids[-50:]

    recruiter_emails = load_recruiter_emails()
    print(f"Checking {len(email_ids)} recent unread emails against your recruiters list...")

    replies_found = 0

    for e_id in email_ids:
        res, msg_data = mail.fetch(e_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                from_header = msg.get("From", "")
                from_email = email.utils.parseaddr(from_header)[1].lower()

                if from_email in recruiter_emails:
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                    
                    print(f"[!] Reply found from Recruiter: {from_email} | Subject: {subject}")
                    replies_found += 1

    print(f"Scan complete. Found {replies_found} replies from your recruiters.")
    mail.logout()

if __name__ == "__main__":
    check_gmail_replies()