
import subprocess
import shutil
import ipaddress

class FirewallManager:
    def __init__(self, backend='auto'):
        self.backend = self.detect_backend(backend)

    def detect_backend(self, backend):
        if backend == 'iptables':
            return 'iptables'
        if backend == 'nftables':
            return 'nftables'
        if backend == 'ufw':
            return 'ufw'
        # auto detection
        if shutil.which('nft'):
            return 'nftables'
        if shutil.which('ufw'):
            return 'ufw'
        if shutil.which('iptables'):
            return 'iptables'
        raise RuntimeError('No supported firewall backend found (iptables, nftables, ufw)')

    def block_ip(self, ip):
        print(f"[FIREWALL] Blocking IP: {ip} using {self.backend}")
        try:
            # Validasi IP
            try:
                ipaddress.ip_address(ip)
            except Exception:
                print(f"[ERROR] IP tidak valid: {ip}")
                return
            # Cek duplikat rule
            if self.is_blocked(ip):
                print(f"[INFO] IP {ip} sudah diblokir.")
                return
            if self.backend == 'iptables':
                cmd = ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
                subprocess.run(cmd, check=True)
            elif self.backend == 'nftables':
                subprocess.run(["sudo", "nft", "add", "table", "inet", "filter"], check=False)
                subprocess.run(["sudo", "nft", "add", "chain", "inet", "filter", "input", "{ type filter hook input priority 0 ; }"], check=False)
                cmd = ["sudo", "nft", "add", "rule", "inet", "filter", "input", "ip", "saddr", ip, "drop"]
                subprocess.run(cmd, check=True)
            elif self.backend == 'ufw':
                cmd = ["sudo", "ufw", "deny", "from", ip]
                subprocess.run(cmd, check=True)
            else:
                raise RuntimeError(f"Unknown firewall backend: {self.backend}")
            print(f"[OK] IP {ip} berhasil diblokir.")
        except Exception as e:
            print(f"Failed to block IP {ip}: {e}")

    def is_blocked(self, ip):
        try:
            if self.backend == 'iptables':
                result = subprocess.run(["sudo", "iptables", "-L", "INPUT", "-n"], capture_output=True, text=True)
                return ip in result.stdout
            elif self.backend == 'nftables':
                result = subprocess.run(["sudo", "nft", "list", "ruleset"], capture_output=True, text=True)
                return f"saddr {ip}" in result.stdout
            elif self.backend == 'ufw':
                result = subprocess.run(["sudo", "ufw", "status"], capture_output=True, text=True)
                return ip in result.stdout
        except Exception:
            return False
        return False

    def unblock_ip(self, ip):
        print(f"[FIREWALL] Unblocking IP: {ip} using {self.backend}")
        try:
            if not self.is_blocked(ip):
                print(f"[INFO] IP {ip} tidak ditemukan di rules.")
                return
            if self.backend == 'iptables':
                cmd = ["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"]
                subprocess.run(cmd, check=True)
            elif self.backend == 'nftables':
                # Cari handle rule untuk hapus lebih presisi
                ruleset = subprocess.run(["sudo", "nft", "list", "chain", "inet", "filter", "input"], capture_output=True, text=True)
                for line in ruleset.stdout.splitlines():
                    if f"saddr {ip}" in line and "drop" in line:
                        parts = line.strip().split()
                        if "handle" in parts:
                            handle = parts[-1]
                            cmd = ["sudo", "nft", "delete", "rule", "inet", "filter", "input", "handle", handle]
                            subprocess.run(cmd, check=True)
                            print(f"[OK] IP {ip} berhasil di-unblock.")
                            return
                print(f"[INFO] Rule untuk IP {ip} tidak ditemukan di nftables.")
            elif self.backend == 'ufw':
                cmd = ["sudo", "ufw", "delete", "deny", "from", ip]
                subprocess.run(cmd, check=True)
                print(f"[OK] IP {ip} berhasil di-unblock.")
            else:
                raise RuntimeError(f"Unknown firewall backend: {self.backend}")
        except Exception as e:
            print(f"Failed to unblock IP {ip}: {e}")

    def list_blocked(self):
        print(f"[FIREWALL] List blocked IPs using {self.backend}")
        try:
            if self.backend == 'iptables':
                result = subprocess.run(["sudo", "iptables", "-L", "INPUT", "-n", "--line-numbers"], capture_output=True, text=True)
                print(result.stdout)
            elif self.backend == 'nftables':
                result = subprocess.run(["sudo", "nft", "list", "chain", "inet", "filter", "input"], capture_output=True, text=True)
                for line in result.stdout.splitlines():
                    if "saddr" in line and "drop" in line:
                        print(line.strip())
            elif self.backend == 'ufw':
                result = subprocess.run(["sudo", "ufw", "status", "numbered"], capture_output=True, text=True)
                print(result.stdout)
            else:
                raise RuntimeError(f"Unknown firewall backend: {self.backend}")
        except Exception as e:
            print(f"Failed to list blocked IPs: {e}")
