import unittest
from src.netids import NetIDS

class TestNetIDS(unittest.TestCase):
    def setUp(self):
        self.netids = NetIDS(config_path="config.json")

    def test_detect_tcp_syn(self):
        # Simulasi deteksi TCP SYN scan (dummy packet)
        packet = type('pkt', (), {'haslayer': lambda self, x: x == 'TCP', 'flags': 'S'})()
        detected = self.netids.detect_packet(packet)
        self.assertTrue(detected)

    def test_detect_icmp_echo(self):
        # Simulasi deteksi ICMP Echo (dummy packet)
        packet = type('pkt', (), {'haslayer': lambda self, x: x == 'ICMP'})()
        detected = self.netids.detect_packet(packet)
        self.assertTrue(detected)

if __name__ == "__main__":
    unittest.main()
