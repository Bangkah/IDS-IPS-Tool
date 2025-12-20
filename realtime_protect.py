import argparse
import time
import os
from src.config import load_config
from src.ids import IDS
from src.ips import IPS

def main():
    parser = argparse.ArgumentParser(description="Realtime IDS/IPS Protection Script")
    parser.add_argument('config', help='Path to config.json')
    parser.add_argument('logfile', help='Path to log file to monitor')
    parser.add_argument('--interval', type=int, default=5, help='Interval deteksi (detik, default: 5)')
    parser.add_argument('--ips', action='store_true', help='Aktifkan mode IPS (blokir otomatis)')
    args = parser.parse_args()

    config = load_config(args.config)
    if args.ips:
        print("[INFO] Mode: IPS (deteksi & blokir otomatis)")
        engine = IPS(config)
    else:
        print("[INFO] Mode: IDS (deteksi saja)")
        engine = IDS(config)

    print(f"[INFO] Monitoring {args.logfile} setiap {args.interval} detik. Tekan Ctrl+C untuk berhenti.")
    last_size = 0
    try:
        while True:
            if not os.path.exists(args.logfile):
                print(f"[WARNING] File log {args.logfile} tidak ditemukan. Menunggu...")
                time.sleep(args.interval)
                continue
            with open(args.logfile, 'r') as f:
                f.seek(last_size)
                new_lines = f.readlines()
                last_size = f.tell()
            if new_lines:
                temp_log = '._realtime_temp.log'
                with open(temp_log, 'w') as tf:
                    tf.writelines(new_lines)
                if args.ips:
                    engine.analyze_and_block(temp_log)
                else:
                    engine.analyze_log(temp_log)
                os.remove(temp_log)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[INFO] Realtime monitoring dihentikan.")

if __name__ == "__main__":
    main()
