import subprocess
import sys
import os

# Path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(BASE_DIR, "config.json")
LOG = os.path.join(BASE_DIR, "ids_ips.log")

# Start IDS (real-time)
subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "ids_main.py"), CONFIG, LOG, "--realtime"])
# Start IPS
subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "ips_main.py"), CONFIG, LOG])
# Start NetIDS (tanpa interface spesifik)
subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "netids_main.py"), CONFIG])

# Start dashboard
import uvicorn
uvicorn.run("dashboard.app:app", host="0.0.0.0", port=8000, reload=True)
