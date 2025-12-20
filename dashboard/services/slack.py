import os
import requests
import logging

def send_slack(message):
    webhook = os.environ.get("SLACK_WEBHOOK")
    if webhook:
        try:
            requests.post(webhook, json={"text": message}, timeout=5)
        except Exception as e:
            logging.warning(f"Slack alert failed: {e}")
