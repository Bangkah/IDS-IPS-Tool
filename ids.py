// File removed: legacy, all logic migrated to src/ids.py
import re
import sys


import time
from utils import load_config, setup_logger

try:
    import notify2
    notify2_inited = False
except ImportError:
    notify2 = None
    notify2_inited = False

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    Observer = None
    FileSystemEventHandler = object

class ModularIDS:
    def __init__(self, config):
        self.patterns = config['patterns']
        self.logger = setup_logger(config['log_file'])

    def notify(self, title, message):
        if notify2:
            global notify2_inited
            if not notify2_inited:
                notify2.init("IDS Alert")
                notify2_inited = True
            n = notify2.Notification(title, message)
            n.set_urgency(notify2.URGENCY_CRITICAL)
            n.show()

    def analyze_line(self, line, line_num=None):
        alerts = []
        for pattern in self.patterns:
            match = re.search(pattern['regex'], line, re.IGNORECASE)
            if match:
                ip = match.group(1) if match.lastindex else '-'
                alert = {
                    'line': line_num,
                    'pattern': pattern['name'],
                    'severity': pattern['severity'],
                    'ip': ip,
                    'content': line.strip()
                }
                alerts.append(alert)
                self.logger.warning(f"[IDS] {alert}")
                # Notifikasi desktop jika real-time
                if notify2:
                    title = f"[IDS] {pattern['name']} ({pattern['severity']})"
                    msg = f"Line {line_num} | IP: {ip}\n{line.strip()}"
                    self.notify(title, msg)
        return alerts

    def analyze_log(self, log_file):
        alerts = []
        with open(log_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                alerts.extend(self.analyze_line(line, line_num))
        return alerts

    def monitor_log_realtime(self, log_file):
        if Observer is None:
            print("watchdog belum terinstall. Jalankan: pip install watchdog")
            return

        class LogHandler(FileSystemEventHandler):
            def __init__(self, ids, log_file):
                self.ids = ids
                self.log_file = log_file
                self._seek_end()

            def _seek_end(self):
                self.f = open(self.log_file, 'r')
                self.f.seek(0, 2)
                self.line_num = sum(1 for _ in open(self.log_file, 'r'))

            def on_modified(self, event):
                if event.src_path.endswith(self.log_file):
                    while True:
                        line = self.f.readline()
                        if not line:
                            break
                        self.line_num += 1
                        alerts = self.ids.analyze_line(line, self.line_num)
                        for alert in alerts:
                            print(f"[REALTIME ALERT] Line {alert['line']} | {alert['pattern']} | {alert['severity']} | IP: {alert['ip']} | {alert['content']}")

        print(f"[IDS] Monitoring {log_file} secara real-time. Tekan Ctrl+C untuk berhenti.")
        event_handler = LogHandler(self, log_file)
        observer = Observer()
        import os
        observer.schedule(event_handler, os.path.dirname(os.path.abspath(log_file)) or '.', recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ids.py <config.json> <log_file> [--realtime]")
        exit(1)
    config = load_config(sys.argv[1])
    ids = ModularIDS(config)
    if len(sys.argv) > 3 and sys.argv[3] == "--realtime":
        ids.monitor_log_realtime(sys.argv[2])
    else:
        alerts = ids.analyze_log(sys.argv[2])
        if alerts:
            print("[ALERT] Potensi serangan terdeteksi:")
            for alert in alerts:
                print(f"Line {alert['line']} | {alert['pattern']} | {alert['severity']} | IP: {alert['ip']} | {alert['content']}")
        else:
            print("Tidak ada aktivitas mencurigakan.")
