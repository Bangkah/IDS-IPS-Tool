#!/usr/bin/env python3
import argparse
import sys
import os
from src.config import load_config
from src.ids import IDS

def main():
    parser = argparse.ArgumentParser(description="Modular IDS - Intrusion Detection System")
    parser.add_argument('config', help='Path to config.json')
    parser.add_argument('logfile', help='Path to log file to monitor')
    parser.add_argument('--realtime', action='store_true', help='Enable real-time monitoring')
    args = parser.parse_args()

    config = load_config(args.config)
    ids = IDS(config)
    if args.realtime:
        ids.monitor_log_realtime(args.logfile)
    else:
        alerts = ids.analyze_log(args.logfile)
        if alerts:
            print("[ALERT] Potensi serangan terdeteksi:")
            for alert in alerts:
                print(f"Line {alert['line']} | {alert['pattern']} | {alert['severity']} | IP: {alert['ip']} | {alert['content']}")
        else:
            print("Tidak ada aktivitas mencurigakan.")

if __name__ == "__main__":
    main()
