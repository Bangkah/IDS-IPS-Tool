
import re
import sys
import subprocess
from utils import load_config, setup_logger

class ModularIPS:
    def __init__(self, config):
        self.patterns = config['patterns']
        self.logger = setup_logger(config['log_file'])
        self.blocked_ips = set()
        self.block_command_template = ["sudo", "iptables", "-A", "INPUT", "-s", "{ip}", "-j", "DROP"]

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
        cmd = [c.format(ip=ip) if c == "{ip}" else c for c in self.block_command_template]
        msg = f"[IPS] Blocking IP: {ip} | Reason: {reason} | Line: {line_num} | {content}"
        print(msg)
        self.logger.warning(msg)
        try:
            subprocess.run(cmd, check=True)
        except Exception as e:
            err = f"Failed to block IP {ip}: {e}"
            print(err)
            self.logger.error(err)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ips.py <config.json> <log_file>")
        exit(1)
    config = load_config(sys.argv[1])
    ips = ModularIPS(config)
    ips.analyze_and_block(sys.argv[2])
    print("IPS processing complete.")
