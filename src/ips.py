import re
import subprocess
from .logger import setup_logger


import shutil

class IPS:
    def __init__(self, config):
        self.patterns = config['patterns']
        self.logger = setup_logger(config['log_file'], name="IPS")
        self.blocked_ips = set()
        self.firewall = config.get('firewall', 'auto')
        self.backend = self.detect_firewall_backend(self.firewall)

    def detect_firewall_backend(self, fw):
        if fw == 'iptables':
            return 'iptables'
        if fw == 'nftables':
            return 'nftables'
        if fw == 'ufw':
            return 'ufw'
        # auto detection
        if shutil.which('nft'):
            return 'nftables'
        if shutil.which('ufw'):
            return 'ufw'
        if shutil.which('iptables'):
            return 'iptables'
        raise RuntimeError('No supported firewall backend found (iptables, nftables, ufw)')

    def analyze_and_block(self, log_file):
        with open(log_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                for pattern in self.patterns:
                    match = re.search(pattern['regex'], line, re.IGNORECASE)
                    if match:
                        ip = match.group(1) if match.lastindex else None
                        if ip and ip not in self.blocked_ips:
                            self.block_ip(ip, pattern['name'], line_num, line.strip())
                            self.blocked_ips.add(ip)

    def block_ip(self, ip, reason, line_num, content):
        msg = f"[IPS] Blocking IP: {ip} | Reason: {reason} | Line: {line_num} | {content} | Backend: {self.backend}"
        print(msg)
        self.logger.warning(msg)
        try:
            if self.backend == 'iptables':
                cmd = ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
            elif self.backend == 'nftables':
                # Add to input chain, drop
                cmd = ["sudo", "nft", "add", "rule", "inet", "filter", "input", "ip", "saddr", ip, "drop"]
            elif self.backend == 'ufw':
                cmd = ["sudo", "ufw", "deny", "from", ip]
            else:
                raise RuntimeError(f"Unknown firewall backend: {self.backend}")
            subprocess.run(cmd, check=True)
        except Exception as e:
            err = f"Failed to block IP {ip} with {self.backend}: {e}"
            print(err)
            self.logger.error(err)
