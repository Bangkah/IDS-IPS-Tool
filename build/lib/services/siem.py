import os
import requests
import logging
import threading

SIEM_ENDPOINT = os.environ.get("SIEM_ENDPOINT")

def forward_log_to_siem(msg):
    if not SIEM_ENDPOINT:
        return
    def _send():
        try:
            requests.post(SIEM_ENDPOINT, json={"log": msg})
        except Exception as e:
            logging.warning(f"Failed to forward log to SIEM: {e}")
    threading.Thread(target=_send, daemon=True).start()
