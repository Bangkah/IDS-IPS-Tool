
from scapy.all import sniff, TCP, IP, ICMP
from .logger import setup_logger
from .alert import print_alert
import re
import threading

import datetime

class NetIDS:
    def __init__(self, config):
        self.patterns = config.get('net_patterns', [])
        self.logger = setup_logger(config['log_file'], name="NetIDS")
        self.alerted = set()
        self.stats = {}
        self.ip_stats = {}
        self.first_alert = None
        self.last_alert = None

    def packet_callback(self, pkt):
        if IP in pkt:
            src = pkt[IP].src
            dst = pkt[IP].dst
            proto = pkt[IP].proto
            summary = pkt.summary()
            now = datetime.datetime.now()
            for pattern in self.patterns:
                # Custom rule: TCP SYN
                if pattern['type'] == 'tcp_syn' and pkt.haslayer(TCP):
                    if pkt[TCP].flags == 'S':
                        sport = pkt[TCP].sport
                        dport = pkt[TCP].dport
                        key = (src, dst, 'SYN', sport, dport)
                        msg = f"{now:%Y-%m-%d %H:%M:%S} | TCP SYN {src}:{sport} -> {dst}:{dport}"
                        self._alert_once(key, msg, pattern, severity='warning', src=src)
                # Custom rule: ICMP echo
                elif pattern['type'] == 'icmp_echo' and pkt.haslayer(ICMP):
                    if pkt[ICMP].type == 8:  # Echo-request
                        key = (src, dst, 'ICMP-ECHO')
                        msg = f"{now:%Y-%m-%d %H:%M:%S} | ICMP Echo {src} -> {dst}"
                        self._alert_once(key, msg, pattern, severity='info', src=src)
                # Regex on summary
                elif pattern['type'] == 'ip_regex':
                    if re.search(pattern['regex'], summary):
                        key = (src, dst, pattern['regex'])
                        msg = f"{now:%Y-%m-%d %H:%M:%S} | Pattern {pattern['name']} matched: {summary}"
                        self._alert_once(key, msg, pattern, severity='critical', src=src)

    def _alert_once(self, key, msg, pattern, severity='info', src=None):
        if key not in self.alerted:
            print_alert(f"[NetIDS] {msg}", severity)
            self.logger.warning(f"[NetIDS] {msg}")
            self.alerted.add(key)
            # Statistik per rule
            pname = pattern.get('name', str(key))
            self.stats[pname] = self.stats.get(pname, 0) + 1
            # Statistik per IP
            if src:
                self.ip_stats[src] = self.ip_stats.get(src, 0) + 1
            # Waktu serangan
            now = datetime.datetime.now()
            if not self.first_alert:
                self.first_alert = now
            self.last_alert = now

    def print_stats(self):
        print("\n=== Statistik Serangan ===")
        total = sum(self.stats.values())
        print(f"Total serangan: {total}")

        if self.first_alert:
            print(f"Waktu serangan pertama: {self.first_alert:%Y-%m-%d %H:%M:%S}")
            print(f"Waktu serangan terakhir: {self.last_alert:%Y-%m-%d %H:%M:%S}")
        if not self.stats:
            print("Tidak ada serangan terdeteksi.")
        else:
            print("\nStatistik per rule:")
            for k, v in self.stats.items():
                print(f"  {k}: {v} kali")
            print("\nStatistik per IP sumber:")
            for ip, v in self.ip_stats.items():
                print(f"  {ip}: {v} kali")

    def start(self, iface=None):
        print_alert("[NetIDS] Monitoring all interfaces for suspicious traffic. Press Ctrl+C to stop.", 'info')
        try:
            sniff(prn=self.packet_callback, store=0, iface=iface)
        except KeyboardInterrupt:
            self.print_stats()
