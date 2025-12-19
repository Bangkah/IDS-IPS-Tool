import unittest
from src.ips import IPS

class TestIPS(unittest.TestCase):
    def setUp(self):
        self.ips = IPS(config_path="config.json")

    def test_block_ip(self):
        # Simulasi blokir IP (tanpa benar-benar menjalankan iptables)
        result = self.ips.block_ip("192.168.1.100")
        self.assertTrue(result)

    def test_detect_attack(self):
        # Simulasi deteksi serangan dari log
        log_line = "Failed password for root from 192.168.1.101 port 22 ssh2"
        detected = self.ips.detect_attack(log_line)
        self.assertTrue(detected)

if __name__ == "__main__":
    unittest.main()
