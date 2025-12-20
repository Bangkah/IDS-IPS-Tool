import os
import json
import requests
import logging
import smtplib
from email.mime.text import MIMEText

def send_slack_alert(message):
    webhook = os.environ.get("SLACK_WEBHOOK")
    if not webhook:
        cfg_path = os.path.abspath("config.json")
        if os.path.exists(cfg_path):
            with open(cfg_path) as f:
                cfg = json.load(f)
                webhook = cfg.get("slackWebhook")
    if webhook:
        try:
            requests.post(webhook, json={"text": message}, timeout=5)
        except Exception as e:
            logging.warning(f"Slack alert failed: {e}")

def send_telegram_alert(message):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        cfg_path = os.path.abspath("config.json")
        if os.path.exists(cfg_path):
            with open(cfg_path) as f:
                cfg = json.load(f)
                token = cfg.get("telegramToken")
                chat_id = cfg.get("telegramChatId")
    if token and chat_id:
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, data={"chat_id": chat_id, "text": message}, timeout=5)
        except Exception as e:
            logging.warning(f"Telegram alert failed: {e}")

def send_email_alert(message):
    email_to = os.environ.get("EMAIL_ALERT")
    if not email_to:
        cfg_path = os.path.abspath("config.json")
        if os.path.exists(cfg_path):
            with open(cfg_path) as f:
                cfg = json.load(f)
                email_to = cfg.get("emailAlert")
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
