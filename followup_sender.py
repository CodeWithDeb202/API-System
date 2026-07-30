import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_threaded_followup(recruiter_email, original_msg_id, original_subject):
    
    msg = MIMEMultipart()
    msg['From'] = os.getenv("GMAIL_EMAIL")
    msg['To'] = recruiter_email
    msg['Subject'] = "Re: " + original_subject
    msg['In-Reply-To'] = original_msg_id # Link email thread
    msg['References'] = original_msg_id

    body = "Hi, Following up to check if you had a chance to review my resume for the Java Developer position."
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.getenv("GMAIL_EMAIL"), os.getenv("GMAIL_APP_PASSWORD"))
    server.sendmail(os.getenv("GMAIL_EMAIL"), recruiter_email, msg.as_string())
    server.quit()
    print(f"Follow-up sent to {recruiter_email}")