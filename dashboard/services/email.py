import os
import smtplib
import logging
from email.mime.text import MIMEText

def send_email(message):
    email_to = os.environ.get("EMAIL_ALERT")
    if email_to:
        try:
            msg = MIMEText(message)
            msg["Subject"] = "[IDS/IPS Alert]"
            msg["From"] = "ids-alert@localhost"
            msg["To"] = email_to
            s = smtplib.SMTP("localhost")
            s.sendmail(msg["From"], [email_to], msg.as_string())
            s.quit()
        except Exception as e:
            logging.warning(f"Email alert failed: {e}")
