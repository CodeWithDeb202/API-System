import os
import smtplib
import csv
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

Gmail_Email = os.getenv("GMAIL_EMAIL")
Gmail_App_Pass = os.getenv("GMAIL_APP_PASSWORD")
History_csv = "email_sent_history.csv"

def send_outreach_email(recruiter_email, recruiter_name, role, pdf_resume_path):
    msg = MIMEMultipart()
    msg['From'] = Gmail_Email
    msg['To'] = recruiter_email
    msg['Subject'] = f"Application for {role} Role - Entry Level / C2C"

    body = f"""Hi {recruiter_name},

I came across your post for the {role} position. 

As an enthusiastic engineering graduate with strong hands-on project experience in JavaScript, React.js, express.js, node.js and database management, I am eager to apply my technical skills to your team. 

I have built practical projects that align well with your requirements, focusing on clean code and efficient problem-solving.

Please find my updated resume attached. I am available immediately for contract or entry-level roles.

Best regards,
Candidate Team
"""
    msg.attach(MIMEText(body, 'plain'))

    if os.path.exists(pdf_resume_path):
        with open(pdf_resume_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(pdf_resume_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_resume_path)}"'
            msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(Gmail_Email, Gmail_App_Pass)
        
        text = msg.as_string()
        server.sendmail(Gmail_Email, recruiter_email, text)
        msg_id = msg.get("Message-ID", "")
        server.quit()


        log_email_history(recruiter_name, recruiter_email, role, msg['Subject'], msg_id)
        print(f"Successfully sent email to {recruiter_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {recruiter_email}: {e}")
        return False

def log_email_history(name, email, role, subject, msg_id):
    file_exists = os.path.exists(History_csv)
    with open(History_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "recruiter_name", "recruiter_email", "role", "email_sent_status", 
            "timestamp", "subject", "message_id", "followup_count", "replied"
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "recruiter_name": name,
            "recruiter_email": email,
            "role": role,
            "email_sent_status": "sent",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "subject": subject,
            "message_id": msg_id,
            "followup_count": 0,
            "replied": 0
        })

