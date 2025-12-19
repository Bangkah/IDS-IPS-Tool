import unittest


from src.netids import NetIDS, IP, TCP, ICMP
import unittest

class DummyPacket:
    def __init__(self, layers=None, flags=None, icmp_type=None, src='1.1.1.1', dst='2.2.2.2', sport=1234, dport=22):
        self._layers = layers or []
        self.flags = flags
        self.type = icmp_type
        self.src = src
        self.dst = dst
        self.sport = sport
        self.dport = dport
    def haslayer(self, x):
        # x is a class (IP, TCP, ICMP)
        return x.__name__ in self._layers

    def __contains__(self, item):
        # item is a class (IP, TCP, ICMP)
        return item.__name__ in self._layers

    def __getitem__(self, item):
        # item is a class (IP, TCP, ICMP)
        if item == TCP:
            class _TCP:
                pass
            t = _TCP()
            t.flags = self.flags
            t.sport = self.sport
            t.dport = self.dport
            return t
        if item == ICMP:
            class _ICMP:
                pass
            i = _ICMP()
            i.type = self.type
            return i
        if item == IP:
            class _IP:
                pass
            ip = _IP()
            ip.src = self.src
            ip.dst = self.dst
            ip.proto = 6
            return ip
        return None
    def summary(self):
        return "Dummy packet"

class TestNetIDS(unittest.TestCase):
    def setUp(self):
        self.config = {
            "net_patterns": [
                {"name": "TCP SYN Scan", "type": "tcp_syn"},
                {"name": "ICMP Echo", "type": "icmp_echo"}
            ],
            "log_file": "test.log"
        }
        self.netids = NetIDS(self.config)


    def test_packet_callback_tcp_syn(self):
        pkt = DummyPacket(layers=['IP', 'TCP'], flags='S')
        self.netids.packet_callback(pkt)

    def test_packet_callback_icmp_echo(self):
        pkt = DummyPacket(layers=['IP', 'ICMP'], icmp_type=8)
        self.netids.packet_callback(pkt)

if __name__ == "__main__":
    unittest.main()
